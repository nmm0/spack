# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import json
import os
import sys
from textwrap import dedent

import pytest

import spack.cmd as cmd
import spack.cmd.find
import spack.concretize
import spack.environment as ev
import spack.repo
import spack.store
import spack.user_environment as uenv
from spack.enums import InstallRecordStatus
from spack.main import SpackCommand
from spack.test.conftest import create_test_repo
from spack.test.utilities import SpackCommandArgs
from spack.util.pattern import Bunch

find = SpackCommand("find")
env = SpackCommand("env")
install = SpackCommand("install")

base32_alphabet = "abcdefghijklmnopqrstuvwxyz234567"


@pytest.fixture(scope="module")
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.find.setup_parser(prs)
    return prs


@pytest.fixture()
def specs():
    s = []
    return s


@pytest.fixture()
def mock_display(monkeypatch, specs):
    """Monkeypatches the display function to return its first argument"""

    def display(x, *args, **kwargs):
        specs.extend(x)

    monkeypatch.setattr(spack.cmd, "display_specs", display)


def test_query_arguments():
    query_arguments = spack.cmd.find.query_arguments

    # Default arguments
    args = Bunch(
        only_missing=False,
        missing=False,
        only_deprecated=False,
        deprecated=False,
        unknown=False,
        explicit=False,
        implicit=False,
        start_date="2018-02-23",
        end_date=None,
        install_tree="all",
    )

    q_args = query_arguments(args)
    assert "installed" in q_args
    assert "predicate_fn" in q_args
    assert "explicit" in q_args
    assert q_args["installed"] == InstallRecordStatus.INSTALLED
    assert q_args["predicate_fn"] is None
    assert q_args["explicit"] is None
    assert "start_date" in q_args
    assert "end_date" not in q_args
    assert q_args["install_tree"] == "all"

    # Check that explicit works correctly
    args.explicit = True
    q_args = query_arguments(args)
    assert q_args["explicit"] is True

    args.explicit = False
    args.implicit = True
    q_args = query_arguments(args)
    assert q_args["explicit"] is False


@pytest.mark.db
@pytest.mark.usefixtures("database", "mock_display")
def test_tag1(parser, specs):
    args = parser.parse_args(["--tag", "tag1"])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 2
    assert "mpich" in [x.name for x in specs]
    assert "mpich2" in [x.name for x in specs]


@pytest.mark.db
@pytest.mark.usefixtures("database", "mock_display")
def test_tag2(parser, specs):
    args = parser.parse_args(["--tag", "tag2"])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 1
    assert "mpich" in [x.name for x in specs]


@pytest.mark.db
@pytest.mark.usefixtures("database", "mock_display")
def test_tag2_tag3(parser, specs):
    args = parser.parse_args(["--tag", "tag2", "--tag", "tag3"])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 0


@pytest.mark.parametrize(
    "args,with_namespace", [([], False), (["--namespace"], True), (["--namespaces"], True)]
)
@pytest.mark.db
def test_namespaces_shown_correctly(args, with_namespace, database):
    """Test that --namespace(s) works. Old syntax is --namespace"""
    assert ("builtin.mock.zmpi" in find(*args)) == with_namespace


@pytest.mark.db
def test_find_cli_output_format(database, mock_tty_stdout):
    # Currently logging on Windows detaches stdout
    # from the terminal so we miss some output during tests
    # TODO: (johnwparent): Once logging is amended on Windows,
    # restore this test
    out = find("zmpi")
    if not sys.platform == "win32":
        assert out.endswith(
            dedent(
                """\
      zmpi@1.0
      ==> 1 installed package
      """
            )
        )
    else:
        assert out.endswith(
            dedent(
                """\
      zmpi@1.0
      """
            )
        )


def _check_json_output(spec_list):
    assert len(spec_list) == 3
    assert all(spec["name"] == "mpileaks" for spec in spec_list)
    assert all(spec["hash"] for spec in spec_list)

    deps = [spec["dependencies"] for spec in spec_list]
    assert sum(["zmpi" in [node["name"] for d in deps for node in d]]) == 1
    assert sum(["mpich" in [node["name"] for d in deps for node in d]]) == 1
    assert sum(["mpich2" in [node["name"] for d in deps for node in d]]) == 1


def _check_json_output_deps(spec_list):
    assert len(spec_list) == 13

    names = [spec["name"] for spec in spec_list]
    assert names.count("mpileaks") == 3
    assert names.count("callpath") == 3
    assert names.count("zmpi") == 1
    assert names.count("mpich") == 1
    assert names.count("mpich2") == 1
    assert names.count("fake") == 1
    assert names.count("dyninst") == 1
    assert names.count("libdwarf") == 1
    assert names.count("libelf") == 1


@pytest.mark.db
def test_find_json(database):
    output = find("--json", "mpileaks")
    spec_list = json.loads(output)
    _check_json_output(spec_list)


@pytest.mark.db
def test_find_json_deps(database):
    output = find("-d", "--json", "mpileaks")
    spec_list = json.loads(output)
    _check_json_output_deps(spec_list)


@pytest.mark.db
def test_display_json(database, capsys):
    specs = [
        spack.concretize.concretize_one(s)
        for s in ["mpileaks ^zmpi", "mpileaks ^mpich", "mpileaks ^mpich2"]
    ]

    cmd.display_specs_as_json(specs)
    spec_list = json.loads(capsys.readouterr()[0])
    _check_json_output(spec_list)

    cmd.display_specs_as_json(specs + specs + specs)
    spec_list = json.loads(capsys.readouterr()[0])
    _check_json_output(spec_list)


@pytest.mark.db
def test_display_json_deps(database, capsys):
    specs = [
        spack.concretize.concretize_one(s)
        for s in ["mpileaks ^zmpi", "mpileaks ^mpich", "mpileaks ^mpich2"]
    ]

    cmd.display_specs_as_json(specs, deps=True)
    spec_list = json.loads(capsys.readouterr()[0])
    _check_json_output_deps(spec_list)

    cmd.display_specs_as_json(specs + specs + specs, deps=True)
    spec_list = json.loads(capsys.readouterr()[0])
    _check_json_output_deps(spec_list)


@pytest.mark.db
def test_find_format(database, config):
    output = find("--format", "{name}-{^mpi.name}", "mpileaks")
    assert set(output.strip().split("\n")) == {
        "mpileaks-zmpi",
        "mpileaks-mpich",
        "mpileaks-mpich2",
    }

    output = find("--format", "{name}-{version}-{compiler.name}-{^mpi.name}", "mpileaks")
    assert "installed package" not in output
    assert set(output.strip().split("\n")) == {
        "mpileaks-2.3-gcc-zmpi",
        "mpileaks-2.3-gcc-mpich",
        "mpileaks-2.3-gcc-mpich2",
    }

    output = find("--format", "{name}-{^mpi.name}-{hash:7}", "mpileaks")
    elements = output.strip().split("\n")
    assert set(e[:-7] for e in elements) == {
        "mpileaks-zmpi-",
        "mpileaks-mpich-",
        "mpileaks-mpich2-",
    }

    # hashes are in base32
    for e in elements:
        for c in e[-7:]:
            assert c in base32_alphabet


@pytest.mark.db
def test_find_format_deps(database, config):
    output = find("-d", "--format", "{name}-{version}", "mpileaks", "^zmpi")
    assert (
        output
        == """\
mpileaks-2.3
    callpath-1.0
        dyninst-8.2
            libdwarf-20130729
            libelf-0.8.13
    zmpi-1.0
        fake-1.0

"""
    )


@pytest.mark.db
def test_find_format_deps_paths(database, config):
    output = find("-dp", "--format", "{name}-{version}", "mpileaks", "^zmpi")

    spec = spack.concretize.concretize_one("mpileaks ^zmpi")
    prefixes = [s.prefix for s in spec.traverse()]

    assert (
        output
        == """\
mpileaks-2.3                   {0}
    callpath-1.0               {1}
        dyninst-8.2            {2}
            libdwarf-20130729  {3}
            libelf-0.8.13      {4}
    zmpi-1.0                   {5}
        fake-1.0               {6}

""".format(
            *prefixes
        )
    )


@pytest.mark.db
def test_find_very_long(database, config):
    output = find("-L", "--no-groups", "mpileaks")

    specs = [
        spack.concretize.concretize_one(s)
        for s in ["mpileaks ^zmpi", "mpileaks ^mpich", "mpileaks ^mpich2"]
    ]

    assert set(output.strip().split("\n")) == set(
        [("%s mpileaks@2.3" % s.dag_hash()) for s in specs]
    )


@pytest.mark.db
def test_find_show_compiler(database, config):
    output = find("--no-groups", "--show-full-compiler", "mpileaks")
    assert "mpileaks@2.3 %gcc@10.2.1" in output


@pytest.mark.db
def test_find_not_found(database, config, capsys):
    with capsys.disabled():
        output = find("foobarbaz", fail_on_error=False)
    assert "No package matches the query: foobarbaz" in output
    assert find.returncode == 1


@pytest.mark.db
def test_find_no_sections(database, config):
    output = find()
    assert "-----------" in output

    output = find("--no-groups")
    assert "-----------" not in output
    assert "==>" not in output


@pytest.mark.db
def test_find_command_basic_usage(database):
    output = find()
    assert "mpileaks" in output


@pytest.mark.regression("9875")
def test_find_prefix_in_env(
    mutable_mock_env_path, install_mockery, mock_fetch, mock_packages, mock_archive
):
    """Test `find` formats requiring concrete specs work in environments."""
    env("create", "test")
    with ev.read("test"):
        install("--fake", "--add", "mpileaks")
        find("-p")
        find("-l")
        find("-L")
        # Would throw error on regression


def test_find_specs_include_concrete_env(mutable_mock_env_path, mutable_mock_repo, tmpdir):
    path = tmpdir.join("spack.yaml")

    with tmpdir.as_cwd():
        with open(str(path), "w", encoding="utf-8") as f:
            f.write(
                """\
spack:
  specs:
  - mpileaks
"""
            )
        env("create", "test1", "spack.yaml")

    test1 = ev.read("test1")
    test1.concretize()
    test1.write()

    with tmpdir.as_cwd():
        with open(str(path), "w", encoding="utf-8") as f:
            f.write(
                """\
spack:
  specs:
  - libelf
"""
            )
        env("create", "test2", "spack.yaml")

    test2 = ev.read("test2")
    test2.concretize()
    test2.write()

    env("create", "--include-concrete", "test1", "--include-concrete", "test2", "combined_env")

    with ev.read("combined_env"):
        output = find()

    assert "No root specs" in output
    assert "Included specs" in output
    assert "mpileaks" in output
    assert "libelf" in output


def test_find_specs_nested_include_concrete_env(mutable_mock_env_path, mutable_mock_repo, tmpdir):
    path = tmpdir.join("spack.yaml")

    with tmpdir.as_cwd():
        with open(str(path), "w", encoding="utf-8") as f:
            f.write(
                """\
spack:
  specs:
  - mpileaks
"""
            )
        env("create", "test1", "spack.yaml")

    test1 = ev.read("test1")
    test1.concretize()
    test1.write()

    env("create", "--include-concrete", "test1", "test2")
    test2 = ev.read("test2")
    test2.add("libelf")
    test2.concretize()
    test2.write()

    env("create", "--include-concrete", "test2", "test3")

    with ev.read("test3"):
        output = find()

    assert "No root specs" in output
    assert "Included specs" in output
    assert "mpileaks" in output
    assert "libelf" in output


def test_find_loaded(database, working_env):
    output = find("--loaded", "--group")
    assert output == ""

    os.environ[uenv.spack_loaded_hashes_var] = os.pathsep.join(
        [x.dag_hash() for x in spack.store.STORE.db.query()]
    )
    output = find("--loaded")
    expected = find()
    assert output == expected


@pytest.mark.regression("37712")
def test_environment_with_version_range_in_compiler_doesnt_fail(tmp_path):
    """Tests that having an active environment with a root spec containing a compiler constrained
    by a version range (i.e. @X.Y rather the single version than @=X.Y) doesn't result in an error
    when invoking "spack find".
    """
    test_environment = ev.create_in_dir(tmp_path)
    test_environment.add("zlib %gcc@12.1.0")
    test_environment.write()

    with test_environment:
        output = find()
    assert "zlib %gcc@12.1.0" in output


_pkga = (
    "a0",
    """\
from spack.package import *

class A0(Package):
    version("1.2")
    version("1.1")

    depends_on("b0")
    depends_on("c0")
""",
)


_pkgb = (
    "b0",
    """\
from spack.package import *

class B0(Package):
    version("1.2")
    version("1.1")
""",
)


_pkgc = (
    "c0",
    """\
from spack.package import *

class C0(Package):
    version("1.2")
    version("1.1")

    tags = ["tag0", "tag1"]
""",
)


_pkgd = (
    "d0",
    """\
from spack.package import *

class D0(Package):
    version("1.2")
    version("1.1")

    depends_on("c0")
    depends_on("e0")
""",
)


_pkge = (
    "e0",
    """\
from spack.package import *

class E0(Package):
    tags = ["tag1", "tag2"]

    version("1.2")
    version("1.1")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    r"""
      a0  d0
     / \ / \
    b0  c0  e0
    """
    yield create_test_repo(tmpdir, [_pkga, _pkgb, _pkgc, _pkgd, _pkge])


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


def test_find_concretized_not_installed(
    mutable_mock_env_path, install_mockery, mock_fetch, test_repo, mock_archive
):
    """Test queries against installs of specs against fake repo.

    Given A, B, C, D, E, create an environment and install A.
    Add and concretize (but do not install) D.
    Test a few queries after force uninstalling a dependency of A (but not
    A itself).
    """
    add = SpackCommand("add")
    concretize = SpackCommand("concretize")
    uninstall = SpackCommand("uninstall")

    def _query(_e, *args):
        return spack.cmd.find._find_query(SpackCommandArgs("find")(*args), _e)

    def _nresults(_qresult):
        return len(_qresult[0]), len(_qresult[1])

    env("create", "test")
    with ev.read("test") as e:
        install("--fake", "--add", "a0")

        assert _nresults(_query(e)) == (3, 0)
        assert _nresults(_query(e, "--explicit")) == (1, 0)

        add("d0")
        concretize("--reuse")

        # At this point d0 should use existing c0, but d/e
        # are not installed in the env

        # --explicit, --deprecated, --start-date, etc. are all
        # filters on records, and therefore don't apply to
        # concretized-but-not-installed results
        assert _nresults(_query(e, "--explicit")) == (1, 2)

        assert _nresults(_query(e)) == (3, 2)
        assert _nresults(_query(e, "-c", "d0")) == (0, 1)

        uninstall("-f", "-y", "b0")

        # b0 is now missing (it is not installed, but has an
        # installed parent)

        assert _nresults(_query(e)) == (2, 3)
        # b0 is "double-counted" here: it meets the --missing
        # criteria, and also now qualifies as a
        # concretized-but-not-installed spec
        assert _nresults(_query(e, "--missing")) == (3, 3)
        assert _nresults(_query(e, "--only-missing")) == (1, 3)

        # Tags are not attached to install records, so they
        # can modify the concretized-but-not-installed results

        assert _nresults(_query(e, "--tag=tag0")) == (1, 0)
        assert _nresults(_query(e, "--tag=tag1")) == (1, 1)
        assert _nresults(_query(e, "--tag=tag2")) == (0, 1)

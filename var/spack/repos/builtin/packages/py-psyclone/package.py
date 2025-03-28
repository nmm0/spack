# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsyclone(PythonPackage):
    """
    A source-to-source Fortran compiler designed to programmatically optimise,
    parallelise and instrument HPC applications (written in Fortran) via user-
    provided transformation scripts. Additionally, PSyclone supports the
    development of kernel-based, Fortran-embedded DSLs and is used in the UK
    Met Office's next-generation modelling system, LFRic.

    """

    # Links
    homepage = "https://github.com/stfc/PSyclone"
    git = "https://github.com/stfc/PSyclone.git"
    pypi = "PSyclone/psyclone-3.1.0.tar.gz"

    # Maintainers
    maintainers("arporter", "sergisiso", "TeranIvy", "hiker")

    # License
    license("BSD-3-Clause")

    # Releases
    version("master", branch="master")
    version("3.1.0", sha256="7b369353942358afcb93b199ef2b11116d756cf9d671667ca95fa83fb31f0355")
    version("3.0.0", sha256="25085a6d0dad36c03ec1f06becf7e2f915ded26603d4a1a2981392f5752fdb3e")
    version("2.5.0", sha256="dd1b40d635423c6b23effd2c569908d319afa6153680692e1cbae27f7b5bf4dc")
    version("2.4.0", sha256="14fd3717f99b317471356c59c1d4c4c22c41fd264af11b78ed831dd2eb71a270")
    version("2.3.1", sha256="eee70b3069d71fcf95e9bc8796f0333bd502e0202a98df051b635b133432a082")
    version("2.3.0", sha256="a2cb3f03ad827de99af6acef794d354146443f21623830e4ff62282a81b7cdb3")
    version("2.2.0", sha256="da829e3b88bf8df7bdb1f261cfc9b20c119eae79fbbd92d970eefee7390ca159")
    version("2.1.0", sha256="7ef967146d0e2f4662d1d68472242d12f2097adb90646c5646c962ea2e0f187c")
    version("2.0.0", sha256="94766ffda760404af99f85d70341376192e4a1b8e16e7ae5df980038898a9c41")
    version("1.5.1", sha256="f053ad7316623b2a4002afc79607abda3b22306645e86f2312d9f3fe56d312dc")

    # Current dependencies
    depends_on("py-setuptools", type="build")
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-fparser@0.2.0:", type=("build", "run"), when="@3.0.0:")
    depends_on("py-graphviz", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-jinja2", type="build")
    depends_on("py-jsonschema", type=("build", "run"), when="@2.5.0:")
    depends_on("py-sympy", type=("build", "run"), when="@2.2.0:")
    depends_on("py-termcolor", type=("build", "run"))

    # Historical dependencies
    depends_on("py-six", type=("build", "run"), when="@2.0.0:2.3.1")
    depends_on("py-jsonschema@3.0.2", type=("build", "run"), when="@2.1.0:2.4.0")

    # Test cases fail without compatible versions of py-fparser:
    depends_on("py-fparser@0.1.4", type=("build", "run"), when="@2.5.0")
    depends_on("py-fparser@0.1.3", type=("build", "run"), when="@2.4.0")
    depends_on("py-fparser@0.0.16", type=("build", "run"), when="@2.3.1")
    depends_on("py-fparser@0.0.15", type=("build", "run"), when="@2.3.0")
    depends_on("py-fparser@0.0.14", type=("build", "run"), when="@2.2.0")
    depends_on("py-fparser@0.0.13", type=("build", "run"), when="@2.1.0")
    depends_on("py-fparser@0.0.12", type=("build", "run"), when="@2.0.0")

    # Dependencies only required for tests:
    depends_on("py-flake8", type="test")
    depends_on("py-pylint@:2", type="test")
    depends_on("py-pytest-cov", type="test")
    depends_on("py-pytest-xdist", type="test")
    depends_on("py-pytest", type="test")

    def url_for_version(self, version):
        # As of version 3.0.0, the name of the tarball on pypi is all lowercase.
        name = "psyclone" if version >= Version("3.0.0") else "PSyclone"
        return f"https://files.pythonhosted.org/packages/source/P/PSyclone/{name}-{version}.tar.gz"

    # Test
    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        pytest = which("pytest")
        # Limit pytest to search inside the build tree
        with working_dir("src"):
            pytest()

    def setup_build_environment(self, env):
        # Allow testing with installed executables
        env.prepend_path("PATH", self.prefix.bin)

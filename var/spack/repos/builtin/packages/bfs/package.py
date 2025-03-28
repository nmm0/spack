# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bfs(MakefilePackage):
    """BFS is a breadth-first variant of the UNIX find command that offers
    consistent, intuitive behavior and improved performance."""

    homepage = "https://github.com/tavianator/bfs"
    url = "https://github.com/tavianator/bfs/archive/refs/tags/3.0.1.tar.gz"
    git = "https://github.com/tavianator/bfs.git"

    maintainers("alecbcs")

    license("0BSD")

    sanity_check_is_file = ["bin/bfs"]

    version("main", branch="main")
    version("4.0.6", sha256="446a0a1a5bcbf8d026aab2b0f70f3d99c08e5fe18d3c564a8b7d9acde0792112")
    version("4.0.5", sha256="f7d9ebff00d9a010a5d6cc9b7bf1933095d7e5c0b11a8ec48c96c7ed8f993e5f")
    version("4.0.4", sha256="209da9e9f43d8fe30fd689c189ea529e9d6b5358ce84a63a44721003aea3e1ca")
    version("4.0.1", sha256="8117b76b0a967887278a11470cbfa9e7aeae98f11a7eeb136f456ac462e5ba23")
    version("3.1.1", sha256="d73f345c1021e0630e0db930a3fa68dd1f968833037d8471ee1096e5040bf91b")
    version("3.1", sha256="aa6a94231915d3d37e5dd62d194cb58a575a8f45270020f2bdd5ab41e31d1492")
    version("3.0.4", sha256="7196f5a624871c91ad051752ea21043c198a875189e08c70ab3167567a72889d")
    version("3.0.2", sha256="d3456a9aeecc031064db0dbe012e55a11eb97be88d0ab33a90e570fe66457f92")
    version("3.0.1", sha256="a38bb704201ed29f4e0b989fb2ab3791ca51c3eff90acfc31fff424579bbf962")

    # Build dependencies
    depends_on("c", type="build")

    # System dependencies
    depends_on("acl", when="platform=linux")
    depends_on("attr", when="platform=linux")
    depends_on("libcap", when="platform=linux")
    depends_on("liburing@2.4:", when="platform=linux @3.1:")

    # Required dependencies
    depends_on("oniguruma")

    @run_before("build", when="@4:")
    def configure(self):
        args = ["--enable-release", f"--prefix={self.prefix}"]

        configure_exe = Executable("./configure")
        configure_exe(*args)

    def install(self, spec, prefix):
        """Install the package."""
        if spec.satisfies("@:3"):
            make("install", f"PREFIX={prefix}")
        else:
            make("install")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppcheck(CMakePackage):
    """A tool for static C/C++ code analysis."""

    homepage = "https://cppcheck.sourceforge.net/"
    url = "https://github.com/danmar/cppcheck/archive/2.17.0.tar.gz"

    maintainers("white238")

    license("GPL-3.0-or-later")

    version("2.17.1", sha256="bfd681868248ec03855ca7c2aea7bcb1f39b8b18860d76aec805a92a967b966c")

    with default_args(deprecated=True):
        version("2.9", sha256="d89f3282c70814fa66669e1ea0323c0484563b3f8249c7a2dcaac2ad07651dc7")
        version("2.8", sha256="a5ed97a99173d2952cd93fcb028a3405a7b3b992e7168e2ae9d527b991770203")
        version("2.7", sha256="ac74c0973c46a052760f4ff7ca6a84616ca5795510542d195a6f122c53079291")
        version("2.1", sha256="ab26eeef039e5b58aac01efb8cb664f2cc16bf9879c61bc93cd00c95be89a5f7")
        version("2.0", sha256="5f77d36a37ed9ef58ea8b499e4b1db20468114c9ca12b5fb39b95906cab25a3f")
        version("1.90", sha256="43758d56613596c29440e55ea96a5a13e36f81ca377a8939648b5242faf61883")
        version("1.89", sha256="5f02389cb24554f5a7ac3d29db8ac19c740f23c92e97eb7fec3881fe86c26f2c")
        version("1.88", sha256="bb25441749977713476dc630dfe7617b3d9e95c46fec0edbec4ff8ff6fda38ca")
        version("1.87", sha256="e3b0a46747822471df275417d4b74b56ecac88367433e7428f39288a32c581ca")
        version("1.81", sha256="bb694f37ae0b5fed48c6cdc2fb5e528daf32cefc64e16b1a520c5411323cf27e")
        version("1.78", sha256="e42696f7d6321b98cb479ad9728d051effe543b26aca8102428f60b9850786b1")
        version("1.72", sha256="9460b184ff2d8dd15344f3e2f42f634c86e4dd3303e1e9b3f13dc67536aab420")
        version("1.68", sha256="add6e5e12b05ca02b356cd0ec7420ae0dcafddeaef183b4dfbdef59c617349b1")

    def url_for_version(self, version):
        if version <= Version("2.9"):
            return f"https://downloads.sourceforge.net/project/cppcheck/cppcheck/{version}/cppcheck-{version}.tar.bz2"
        return f"https://github.com/danmar/cppcheck/archive/{version}.tar.gz"

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("rules", default=False, description="Enable rules (requires PCRE)")

    depends_on("pcre", when="+rules", type="build")
    depends_on("py-pygments", type="run")
    extends("python")

    def cmake_args(self):
        return [
            self.define("BUILD_TESTS", self.run_tests),
            self.define_from_variant("HAVE_RULES", "rules"),
        ]

    @run_after("install", when="@:2.9")
    def install_cppcheck_htmlreport(self):
        install("htmlreport/cppcheck-htmlreport", self.prefix.bin)

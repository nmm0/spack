# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mold(CMakePackage):
    """mold: A Modern Linker"""

    homepage = "https://github.com/rui314/mold"
    url = "https://github.com/rui314/mold/archive/refs/tags/v1.11.0.tar.gz"

    maintainers("msimberg")

    license("MIT")

    version("2.37.1", sha256="b8e36086c95bd51e9829c9755c138f5c4daccdd63b6c35212b84229419f3ccbe")
    version("2.37.0", sha256="28372bbc2ce069aa0362ba84ad5d1b0f2c0bcf84e95a0f533ecf79cb3aff232c")
    version("2.36.0", sha256="3f57fe75535500ecce7a80fa1ba33675830b7d7deb1e5ee9a737e2bc43cdb1c7")
    version("2.35.1", sha256="912b90afe7fde03e53db08d85a62c7b03a57417e54afc72c08e2fa07cab421ff")
    version("2.35.0", sha256="2703f1c88c588523815886478950bcae1ef02190dc4787e0d120a293b1a46e3b")
    version("2.34.1", sha256="a8cf638045b4a4b2697d0bcc77fd96eae93d54d57ad3021bf03b0333a727a59d")
    version("2.34.0", sha256="6067f41f624c32cb0f4e959ae7fabee5dd71dd06771e2c069c2b3a6a8eca3c8c")
    version("2.33.0", sha256="37b3aacbd9b6accf581b92ba1a98ca418672ae330b78fe56ae542c2dcb10a155")
    version("2.32.1", sha256="f3c9a527d884c635834fe7d79b3de959b00783bf9446280ea274d996f0335825")
    version("2.32.0", sha256="4b7e4146ea0f52be9adae8b417399f3676a041e65b55e3f25f088120d30a320b")
    version("2.31.0", sha256="3dc3af83a5d22a4b29971bfad17261851d426961c665480e2ca294e5c74aa1e5")
    version("2.30.0", sha256="6e5178ccafe828fdb4ba0dd841d083ff6004d3cb41e56485143eb64c716345fd")
    version("2.4.1", sha256="c9853d007d6a1b4f3e36b7314346751f4cc91bc43c76e30db51709b53b44dd68")
    version("2.4.0", sha256="be65f3d785d32ece7b3204ecaa57810847fdd25c232cf704cbfff2dafb1ac107")
    version("2.3.0", sha256="6cfc1af0214f993be1b0ae4a2f0278d32b7fc48155c15b2d03758f6d81e7250b")
    version("2.2.0", sha256="78ddddaaa004e50f8d92a13d8e792a46a1b37745fab48d39ad16aeb5a776e7c6")
    version("2.1.0", sha256="a32bec1282671b18ea4691855aed925ea2f348dfef89cb7689cd81273ea0c5df")
    version("2.0.0", sha256="2ae8a22db09cbff626df74c945079fa29c1e5f60bbe02502dcf69191cf43527b")
    version("1.11.0", sha256="99318eced81b09a77e4c657011076cc8ec3d4b6867bd324b8677974545bc4d6f")
    version("1.7.1", sha256="fa2558664db79a1e20f09162578632fa856b3cde966fbcb23084c352b827dfa9")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("blake3", when="@2.2:")
    depends_on("mimalloc")
    depends_on("openssl", when="@:2.1")
    depends_on("tbb")
    depends_on("zlib-api")
    depends_on("zstd")

    def cmake_args(self):
        return [
            self.define("MOLD_USE_SYSTEM_MIMALLOC", True),
            self.define("MOLD_USE_SYSTEM_TBB", True),
        ]

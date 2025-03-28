# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HipTensor(CMakePackage, ROCmPackage):
    """AMD’s C++ library for accelerating tensor primitives"""

    homepage = "https://github.com/ROCm/hipTensor"
    git = "https://github.com/ROCm/hipTensor.git"
    url = "https://github.com/ROCm/hipTensor/archive/refs/tags/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "afzpatel")

    version("master", branch="master")
    version("6.3.2", sha256="094db6d759eb32e9d15c36fce7f5b5d46ba81416953a8d9435b2fb9c161d8c83")
    version("6.3.1", sha256="142401331526e6da3fa172cce283f1c053056cb59cf431264443da76cee2f168")
    version("6.3.0", sha256="9a4acef722e838ec702c6b111ebc1fff9d5686ae5c79a9f5a82e5fac2a5e406a")
    version("6.2.4", sha256="54c378b440ede7a07c93b5ed8d16989cc56283a56ea35e41f3666bb05b6bc984")
    version("6.2.1", sha256="592dbe73f5f95ba512f7fbe9975a68dbea85846be74da15344d74952b286f243")
    version("6.2.0", sha256="adb7459416864fb2664064f5bea5fb669839247b702209a6415b396813626b31")
    version("6.1.2", sha256="ac0e07a3019bcce4a0a98aafa4922d5fc9e953bed07084abef5306c851717783")
    version("6.1.1", sha256="09bcdbf6b1d20dc4d75932abd335a9a534b16a8343858121daa5813a38f5ad3a")
    version("6.1.0", sha256="9cc43b1b3394383f22f30e194d8753ca6ff1887c83ec1de5823cb2e94976eeed")
    version("6.0.2", sha256="6e6e7530eabbd1fb28b83efa5a49c19a6642d40e1554224ebb1e0a5999045e27")
    version("6.0.0", sha256="268d7f114784b7e824f89c21c65c2efedbb5486f09a356a56dca1b89bde1ef7a")
    version("5.7.1", sha256="96743d4e695fe865aef4097ae31d9b4e42a2d5a92135a005b0d187d9c0b17645")
    version("5.7.0", sha256="4b17f6d43b17fe2dc1d0c61e9663d4752006f7898cc94231206444a1663eb252")

    depends_on("cxx", type="build")  # generated

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")
    for ver in [
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
        "6.2.4",
        "6.3.0",
        "6.3.1",
        "6.3.2",
        "master",
    ]:
        depends_on(f"composable-kernel@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", when=f"@{ver}")

    for ver in ["6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1", "6.2.4", "6.3.0", "6.3.1", "6.3.2"]:
        depends_on(f"hipcc@{ver}", when=f"@{ver}")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@6.1"):
            env.set("CXX", self.spec["hipcc"].prefix.bin.hipcc)
        else:
            env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.url
from spack.package import *


class PyRadicalEntk(PythonPackage):
    """RADICAL Ensemble Toolkit is used for developing and executing
    large-scale ensemble-based workflows."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.entk.git"
    pypi = "radical_entk/radical_entk-1.92.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.92.0", sha256="908a5d35cbc801c8b064837a21cbf5ad1a9b4aed0db48f2db84ef85d4e529cef")

    version(
        "1.47.0",
        sha256="a4338e3a87147c032fb3a16a03990155742cc64c6625cfb4e1588ae0e51aafda",
        deprecated=True,
    )
    version(
        "1.39.0",
        sha256="72d64b25df9f3cb1dcbc32323a669d86d947cf07d15bed91cfedca2a99fb3ef1",
        deprecated=True,
    )

    depends_on("py-radical-utils@1.90:1.99", type=("build", "run"), when="@1.90:")
    depends_on("py-radical-pilot@1.90:1.99", type=("build", "run"), when="@1.90:")

    depends_on("py-radical-utils@1.40:1.52", type=("build", "run"), when="@1.40:1.52")
    depends_on("py-radical-pilot@1.40:1.52.1", type=("build", "run"), when="@1.40:1.52")

    depends_on("py-radical-utils@1.39", type=("build", "run"), when="@1.39")
    depends_on("py-radical-pilot@1.39", type=("build", "run"), when="@1.39")

    depends_on("python@3.7:", type=("build", "run"), when="@1.53:")
    depends_on("python@3.6:", type=("build", "run"), when="@:1.52")

    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        if version >= Version("1.48.1"):
            return super().url_for_version(version)
        url = self.url.replace("_", ".")
        return spack.url.substitute_version(url, self.url_version(version))

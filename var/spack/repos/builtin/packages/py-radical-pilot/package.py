# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.url
from spack.package import *


class PyRadicalPilot(PythonPackage):
    """RADICAL-Pilot is a Pilot system specialized in executing applications
    composed of many computational tasks on high performance computing (HPC)
    platforms."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.pilot.git"
    pypi = "radical_pilot/radical_pilot-1.92.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.92.0", sha256="5c65df02ec097f71648259db8ed8638580ea8e4c1c7f360879afff7f99e56134")

    version(
        "1.47.0",
        sha256="58f41a0c42fe61381f15263a63424294732606ab7cee717540c0b730308f7908",
        deprecated=True,
    )
    version(
        "1.39.0",
        sha256="7ba0bfa3258b861db71e73d52f0915bfb8b3ac1099badacf69628307cab3b913",
        deprecated=True,
    )

    depends_on("py-radical-utils@1.90:1.99", type=("build", "run"), when="@1.90:")
    depends_on("py-radical-gtod@1.90:1.99", type=("build", "run"), when="@1.90:")

    depends_on("py-radical-utils@1.44:1.52", type=("build", "run"), when="@1.47:1.52.1")
    depends_on("py-radical-saga@1.40:", type=("build", "run"), when="@1.47")
    depends_on("py-radical-gtod@:1.52", type=("build", "run"), when="@1.14:1.52.1")

    depends_on("py-radical-utils@1.39", type=("build", "run"), when="@1.39")
    depends_on("py-radical-saga@1.39", type=("build", "run"), when="@1.39")
    depends_on("py-radical-gtod@1.39", type=("build", "run"), when="@1.39")

    depends_on("py-pymongo@:3", type=("build", "run"), when="@:1.39")

    depends_on("python@3.7:", type=("build", "run"), when="@1.48:")
    depends_on("python@3.6:", type=("build", "run"), when="@:1.47")

    depends_on("py-requests", type=("build", "run"), when="@1.90:")
    depends_on("py-psij-python", type=("build", "run"), when="@1.48:")
    depends_on("py-dill", type=("build", "run"), when="@1.14:")
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        if version >= Version("1.49.3"):
            return super().url_for_version(version)
        url = self.url.replace("_", ".")
        return spack.url.substitute_version(url, self.url_version(version))

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.url
from spack.package import *


class PyRadicalUtils(PythonPackage):
    """RADICAL-Utils contains shared code and tools for various
    RADICAL-Cybertools packages."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.utils.git"
    pypi = "radical_utils/radical_utils-1.91.1.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.91.1", sha256="5293f375f699161e451982b2e7668613c24e2562252f65e765ebbc83d8ae0118")

    version(
        "1.47.0",
        sha256="f85a4a452561dd018217f1ed38d97c9be96fa448437cfeb1b879121174fd5311",
        deprecated=True,
    )
    version(
        "1.39.0",
        sha256="fade87ee4c6ccf335d5e26d5158ce22ee891e4d4c576464274999ddf36dc4977",
        deprecated=True,
    )

    depends_on("python@3.7:", type=("build", "run"), when="@1.53:")
    depends_on("python@3.6:", type=("build", "run"), when="@:1.52")

    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-netifaces", type=("build", "run"))
    depends_on("py-ntplib", type=("build", "run"))
    depends_on("py-pyzmq", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-setproctitle", type=("build", "run"))
    with default_args(type="build"):
        depends_on("py-setuptools")
        # https://github.com/radical-cybertools/radical.utils/issues/403
        depends_on("py-setuptools@:69.2", when="@:1.51")

    def url_for_version(self, version):
        if version >= Version("1.48.1"):
            return super().url_for_version(version)
        url = self.url.replace("_", ".")
        return spack.url.substitute_version(url, self.url_version(version))

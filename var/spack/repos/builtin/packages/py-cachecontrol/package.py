# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachecontrol(PythonPackage):
    """CacheControl is a port of the caching algorithms in httplib2
    for use with requests session object."""

    homepage = "https://github.com/ionrock/cachecontrol"
    pypi = "CacheControl/CacheControl-0.12.10.tar.gz"

    license("Apache-2.0")

    version("0.14.2", sha256="7d47d19f866409b98ff6025b6a0fca8e4c791fb31abbd95f622093894ce903a2")
    version("0.14.0", sha256="7db1195b41c81f8274a7bbd97c956f44e8348265a1bc7641c37dfebc39f0c938")
    version("0.13.1", sha256="f012366b79d2243a6118309ce73151bf52a38d4a5dac8ea57f09bd29087e506b")
    version("0.13.0", sha256="fd3fd2cb0ca66b9a6c1d56cc9709e7e49c63dbd19b1b1bcbd8d3f94cedfe8ce5")
    version("0.12.11", sha256="a5b9fcc986b184db101aa280b42ecdcdfc524892596f606858e0b7a8b4d9e144")
    version("0.12.10", sha256="d8aca75b82eec92d84b5d6eb8c8f66ea16f09d2adb09dbca27fe2d5fc8d3732d")

    variant("filecache", default=False, description="Add lockfile dependency")
    variant("redis", default=False, description="Add redis dependency")

    depends_on("py-flit-core@3.2:3", when="@0.13.1:", type="build")
    depends_on("py-setuptools", when="@:0.13.0", type="build")
    depends_on("py-requests@2.16.0:", when="@0.13:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-msgpack@0.5.2:", type=("build", "run"))
    depends_on("py-msgpack@0.5.2:1", when="@0.14:", type=("build", "run"))
    depends_on("py-filelock@3.8.0:", when="@0.13:+filecache", type=("build", "run"))
    depends_on("py-lockfile@0.9:", when="@0.12+filecache", type=("build", "run"))
    depends_on("py-redis@2.10.5:", when="+redis", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/c/cachecontrol/{0}-{1}.tar.gz"
        if version <= Version("0.13.0"):
            letter = "CacheControl"
        else:
            letter = "cachecontrol"
        return url.format(letter, version)

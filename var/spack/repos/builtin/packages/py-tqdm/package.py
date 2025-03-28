# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    pypi = "tqdm/tqdm-4.45.0.tar.gz"

    version("4.67.1", sha256="f8aef9c52c08c13a65f30ea34f4e5aac3fd1a34959879d7e59e63027286627f2")
    version("4.67.0", sha256="fe5a6f95e6fe0b9755e9469b77b9c3cf850048224ecaa8293d7d2d31f97d869a")
    version("4.66.6", sha256="4bdd694238bef1485ce839d67967ab50af8f9272aab687c0d7702a01da0be090")
    version("4.66.5", sha256="e1020aef2e5096702d8a025ac7d16b1577279c9d63f8375b63083e9a5f0fcbad")
    version("4.66.4", sha256="e4d936c9de8727928f3be6079590e97d9abfe8d39a590be678eb5919ffc186bb")
    version("4.66.3", sha256="23097a41eba115ba99ecae40d06444c15d1c0c698d527a01c6c8bd1c5d0647e5")
    version("4.66.1", sha256="d88e651f9db8d8551a62556d3cff9e3034274ca5d66e93197cf2490e2dcb69c7")
    version("4.65.0", sha256="1871fb68a86b8fb3b59ca4cdd3dcccbc7e6d613eeed31f4c332531977b89beb5")
    version("4.64.1", sha256="5f4f682a004951c1b450bc753c710e9280c5746ce6ffedee253ddbcbf54cf1e4")
    version("4.64.0", sha256="40be55d30e200777a307a7585aee69e4eabb46b4ec6a4b4a5f2d9f11e7d5408d")
    version("4.62.3", sha256="d359de7217506c9851b7869f3708d8ee53ed70a1b8edbba4dbcb47442592920d")
    version("4.59.0", sha256="d666ae29164da3e517fcf125e41d4fe96e5bb375cd87ff9763f6b38b5592fe33")
    version("4.58.0", sha256="c23ac707e8e8aabb825e4d91f8e17247f9cc14b0d64dd9e97be0781e9e525bba")
    version("4.56.2", sha256="11d544652edbdfc9cc41aa4c8a5c166513e279f3f2d9f1a9e1c89935b51de6ff")
    version("4.46.0", sha256="4733c4a10d0f2a4d098d801464bdaf5240c7dadd2a7fde4ee93b0a0efd9fb25e")
    version("4.45.0", sha256="00339634a22c10a7a22476ee946bbde2dbe48d042ded784e4d88e0236eca5d81")
    version("4.36.1", sha256="abc25d0ce2397d070ef07d8c7e706aede7920da163c64997585d42d3537ece3d")
    version("4.8.4", sha256="bab05f8bb6efd2702ab6c532e5e6a758a66c0d2f443e09784b73e4066e6b3a37")

    variant("telegram", default=False, description="Enable Telegram bot support")
    variant("notebook", default=False, description="Enable Jupyter Notebook support")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@4.65.0:")
        depends_on("python@2.7:2,3.4:", when="@4.53.0:")
        depends_on("python@2.6:2,3.2:", when="@4.8.4:")

        # not in original requirements, but pyproject.toml [project] requires py-setuptools@61:
        depends_on("py-setuptools@61:", when="@4.65.1:")
        depends_on("py-setuptools@42:")

        depends_on("py-colorama", when="platform=windows")

        depends_on("py-requests", when="+telegram")
        depends_on("py-ipywidgets@6:", when="+notebook")

    with default_args(type=("build")):
        depends_on("py-setuptools-scm@3.4:+toml")
        depends_on("py-wheel", when="@4.53.0:")

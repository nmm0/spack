# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SmeeClient(Package):
    """
    Client and CLI for smee.io, a service that delivers webhooks to your
    local development environment.
    """

    homepage = "https://smee.io"
    url = "https://github.com/probot/smee-client/archive/refs/tags/v1.2.5.tar.gz"

    maintainers("alecbcs")

    license("ISC")

    version("3.1.1", sha256="ceefab820d8da57c1b485a15c024eb875569b5dfccdee13b135bed594b9dcf41")
    version("2.0.4", sha256="b0c959f52e384bbd3f913955cb68102fef11d85b7cc8e5a83404ee325f1ccfe4")
    version("2.0.3", sha256="98ca658cf3214c5116651f2a788c793bc2fe76543f24ada20e8751fcf1de8e1a")
    version("1.2.3", sha256="b9afff843fc7a3c2b5d6659acf45357b5db7a739243b99f6d18a9b110981a328")

    depends_on("node-js", type=("build", "link", "run"))
    depends_on("npm", type="build")
    depends_on("typescript", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        npm = which("npm", required=True)

        # Install node-js dependencies of smee-client
        npm("install")

        # Allow tsc to fail with typing "errors" which don't affect results
        output = npm("run", "build", output=str, error=str, fail_on_error=False)
        if npm.returncode not in (0, 2):
            raise InstallError(output)

    def install(self, spec, prefix):
        npm = which("npm", required=True)
        npm("install", "--global", f"--prefix={prefix}")

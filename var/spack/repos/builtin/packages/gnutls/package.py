# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnutls(AutotoolsPackage):
    """GnuTLS: The GNU Transport Layer Security Library

    A secure communications library implementing SSL, TLS and DTLS protocols
    with a simple C API for accessing secure communications protocols. Provides
    APIs for X.509, PKCS #12, OpenPGP and other security structures. Designed
    for portability and efficiency with focus on security and interoperability.
    """

    homepage = "https://www.gnutls.org"
    url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.19.tar.xz"
    git = "https://gitlab.com/gnutls/gnutls.git"
    list_depth = 2

    maintainers("alecbcs")

    license("LGPL-2.1-or-later")

    sanity_check_is_file = ["include/gnutls/gnutls.h"]
    sanity_check_is_dir = ["lib", "share"]

    # Version definitions
    version("master", branch="master")
    version("3.8.9", sha256="69e113d802d1670c4d5ac1b99040b1f2d5c7c05daec5003813c049b5184820ed")
    version("3.8.8", sha256="ac4f020e583880b51380ed226e59033244bc536cad2623f2e26f5afa2939d8fb")
    version("3.8.4", sha256="2bea4e154794f3f00180fa2a5c51fe8b005ac7a31cd58bd44cdfa7f36ebc3a9b")
    version("3.8.3", sha256="f74fc5954b27d4ec6dfbb11dea987888b5b124289a3703afcada0ee520f4173e")
    version("3.7.8", sha256="c58ad39af0670efe6a8aee5e3a8b2331a1200418b64b7c51977fb396d4617114")
    version("3.6.15", sha256="0ea8c3283de8d8335d7ae338ef27c53a916f15f382753b174c18b45ffd481558")
    version("3.6.14", sha256="5630751adec7025b8ef955af4d141d00d252a985769f51b4059e5affa3d39d63")
    version("3.6.8", sha256="aa81944e5635de981171772857e72be231a7e0f559ae0292d2737de475383e83")
    version("3.6.7.1", sha256="881b26409ecd8ea4c514fd3fbdb6fae5fab422ca7b71116260e263940a4bbbad")
    version("3.5.19", sha256="1936eb64f03aaefd6eb16cef0567457777618573826b94d03376bb6a4afadc44")
    version("3.5.13", sha256="79f5480ad198dad5bc78e075f4a40c4a315a1b2072666919d2d05a08aec13096")
    version("3.5.10", sha256="af443e86ba538d4d3e37c4732c00101a492fe4b56a55f4112ff0ab39dbe6579d")
    version("3.5.9", sha256="82b10f0c4ef18f4e64ad8cef5dbaf14be732f5095a41cf366b4ecb4050382951")
    version("3.3.9", sha256="39166de5293a9d30ef1cd0a4d97f01fdeed7d7dbf8db95392e309256edcb13c1")

    # Variants
    variant("zlib", default=True, description="Enable zlib compression support")
    variant("zstd", default=True, description="Enable zstd compression support", when="@3.7:")
    variant("guile", default=False, description="Enable Guile bindings", when="@:3.7")
    variant(
        "brotli", default=True, description="Enable brotli compression support", when="@3.7.4:"
    )

    # Conflicts
    conflicts(
        "+guile",
        when="platform=darwin",
        msg="gnutls+guile is currently broken on MacOS. See Issue #11668",
    )
    conflicts("%clang@16:", when="@:3.7", msg="-Wimplicit-int is an error in newer clang versions")
    conflicts(
        "%apple-clang@15:",
        when="@:3.7",
        msg="-Wimplicit-int is an error in newer Apple clang versions",
    )

    # Build dependencies
    depends_on("pkgconfig", type="build")
    depends_on("libtool", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Required dependencies
    depends_on("gettext")
    depends_on("libidn2@:2.0", when="@:3.5")
    depends_on("libidn2")
    depends_on("nettle@3.4.1:", when="@3.6.7.1:")
    depends_on("nettle@:2.9", when="@3.3.9")
    depends_on("nettle", when="@3.5:")

    # Optional dependencies
    depends_on("guile", when="+guile")
    depends_on("zlib-api", when="+zlib")
    depends_on("brotli", when="+brotli")
    depends_on("zstd", when="+zstd")

    build_directory = "spack-build"

    def url_for_version(self, version):
        url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v{0}/gnutls-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        if self.spec.satisfies("+guile"):
            env.set("GUILE", self.spec["guile"].prefix.bin.guile)

        if self.spec.satisfies("platform=linux @3.8:"):
            env.set("LDFLAGS", "-ldl")

    def configure_args(self):
        args = ["--enable-static"]

        if self.spec.satisfies("@3.5:"):
            args.extend(
                ["--with-included-libtasn1", "--with-included-unistring", "--without-p11-kit"]
            )

        args.extend(self.with_or_without("zlib"))
        args.extend(self.with_or_without("brotli"))

        if self.spec.satisfies("@:3.7"):
            args.extend(self.enable_or_disable("guile"))

        if self.spec.satisfies("@3.7:"):
            args.extend(self.with_or_without("zstd"))

        if self.run_tests:
            args.extend(["--enable-tests", "--enable-valgrind-tests", "--enable-full-test-suite"])
        else:
            args.extend(
                ["--disable-tests", "--disable-valgrind-tests", "--disable-full-test-suite"]
            )

        return args

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include]
        return headers

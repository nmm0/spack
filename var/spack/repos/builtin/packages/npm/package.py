# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shutil

from spack.package import *


class Npm(Package):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/cli"
    url = "https://registry.npmjs.org/npm/-/npm-9.3.1.tgz"
    git = "https://github.com/npm/cli.git"

    tags = ["build-tools"]

    license("Artistic-2.0")

    version("11.2.0", sha256="1a947c2f9f3bc8c227dd3d30c39338214598dd7da6b4771b7c735c56401d5fb8")
    version("11.1.0", sha256="0f144846f78cc0eb230b0e228f736d5c06362e4ea867c72f059790568454abb7")
    version("10.9.2", sha256="5cd1e5ab971ea6333f910bc2d50700167c5ef4e66da279b2a3efc874c6b116e4")
    version("9.9.4", sha256="640bdd76a0b9d92e9da6e391abae75fd2f168478e416847f3acdb8373737e0ee")
    version("9.3.1", sha256="41caa26a340b0562bc5429d28792049c980fe3e872b42b82cad94e8f70e37f40")
    version("8.19.3", sha256="634bf4e0dc87be771ebf48a058629960e979a209c20a51ebdbc4897ca6a25260")
    version("7.24.2", sha256="5b9eeea011f8bc3b76e55cc33339e87213800677f37e0756ad13ef0e9eaccd64")
    version("6.14.18", sha256="c9b15f277e2a0b1b57e05bad04504296a27024555d56c2aa967f862e957ad2ed")

    depends_on("cxx", type="build")  # generated

    # Based on https://registry.npmjs.org/npm/x.y.z engines.node
    with default_args(type=("build", "run")):
        depends_on("node-js@20.17.0:20,22.9.0:", when="@11")
        depends_on("node-js@18.17.0:18,20.5.0:", when="@10")
        depends_on("node-js@14.17.0:14,16.14.0:16,18.0.0:", when="@9")
        depends_on("node-js@12.13.0:12,14.15.0:14,16:", when="@8")
        depends_on("node-js@10:", when="@7")
        depends_on("node-js@6.2.0:6,8,9.3.0:", when="@6")

    depends_on("libvips", when="@:7")

    # npm 6.13.4 ships with node-gyp 5.0.5, which contains several Python 3
    # compatibility issues on macOS. Manually update to node-gyp 6.0.1 for
    # full Python 3 support.
    resource(
        name="node-gyp",
        destination="node-gyp",
        url="https://registry.npmjs.org/node-gyp/-/node-gyp-6.0.1.tgz",
        sha256="bbc0e137e17a63676efc97a0e3b1fcf101498a1c2c01c3341cd9491f248711b8",
        when="@6",
    )
    resource(
        name="env-paths",
        destination="env-paths",
        url="https://registry.npmjs.org/env-paths/-/env-paths-2.2.0.tgz",
        sha256="168b394fbca60ea81dc84b1824466df96246b9eb4d671c2541f55f408a264b4c",
        when="@6",
    )

    executables = ["^npm$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str).strip()
        match = re.match(r"([\d.]+)\s*", output)
        return match.group(1) if match else None

    @when("@6")
    def patch(self):
        shutil.rmtree("node_modules/node-gyp")
        install_tree("node-gyp/package", "node_modules/node-gyp")
        filter_file(r'"node-gyp": "\^5\..*"', '"node-gyp": "^6.0.1"', "package.json")
        install_tree("env-paths/package", "node_modules/env-paths")

    @when("@:8")
    def install(self, spec, prefix):
        # `npm install .` doesn't work properly out of the box on npm up to 8, so we do
        # what it would do manually. The only thing we seem to miss is docs. In
        # particular, it will end up symlinking into the stage, which spack then
        # deletes. You can avoid that with `npm install $(npm pack .)`, but `npm pack`
        # also seems to fail when run from the tarball on macos. So we just copy manually.
        to_install = [
            "LICENSE",
            "README.md",
            "bin",
            "docs",
            "index.js",
            "lib",
            "node_modules",
            "package.json",
        ]

        mkdirp(prefix.bin)
        mkdirp(prefix.lib.node_modules.npm)

        # manually install all the files above (if they exist for a particular node version)
        for filename in to_install:
            if os.path.exists(filename):
                install_fn = install if os.path.isfile(filename) else install_tree
                install_fn(filename, os.path.join(prefix.lib.node_modules.npm, filename))

        # set up symlinks in bin
        node_modules_bin = os.path.relpath(prefix.lib.node_modules.npm.bin, prefix.bin)
        symlink(os.path.join(node_modules_bin, "npm-cli.js"), prefix.bin.npm)
        symlink(os.path.join(node_modules_bin, "npx-cli.js"), prefix.bin.npx)

    @when("@9:")
    def install(self, spec, prefix):
        # in npm 9, `npm install .` finally works within the repo, so we can just call it.
        node = which("node", required=True)
        node(
            "bin/npm-cli.js",
            "install",
            "--loglevel=silly",
            "--install-links",
            "--global",
            f"--prefix={prefix}",
            ".",
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdirp(npm_config_cache_dir)
        env.set("npm_config_cache", npm_config_cache_dir)
        env.set("npm_config_install_links", "true")

    def setup_dependent_run_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        env.set("npm_config_cache", npm_config_cache_dir)
        env.set("npm_config_install_links", "true")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qwt(QMakePackage):
    """The Qwt library contains GUI Components and utility classes which are
    primarily useful for programs with a technical background. Beside a
    framework for 2D plots it provides scales, sliders, dials, compasses,
    thermometers, wheels and knobs to control or display values, arrays, or
    ranges of type double.
    """

    homepage = "https://qwt.sourceforge.net/"
    url = "https://sourceforge.net/projects/qwt/files/qwt/6.1.3/qwt-6.1.3.tar.bz2"

    license("custom")

    version("6.3.0", sha256="dcb085896c28aaec5518cbc08c0ee2b4e60ada7ac929d82639f6189851a6129a")
    version("6.2.0", sha256="9194f6513955d0fd7300f67158175064460197abab1a92fa127a67a4b0b71530")
    version("6.1.6", sha256="99460d31c115ee4117b0175d885f47c2c590d784206f09815dc058fbe5ede1f6")
    version("6.1.4", sha256="1529215329e51fc562e0009505a838f427919a18b362afff441f035b2d9b5bd9")
    version("6.1.3", sha256="f3ecd34e72a9a2b08422fb6c8e909ca76f4ce5fa77acad7a2883b701f4309733")
    version("5.2.2", sha256="36bf2ee51ca9c74fde1322510ffd39baac0db60d5d410bb157968a78d9c1464b")

    depends_on("cxx", type="build")  # generated

    variant("designer", default=False, description="Build extensions to QT designer")
    variant("opengl", default=False, description="Build OpenGL plot canvas")

    patch("no-designer.patch", when="~designer")
    patch("no-opengl_6_1.patch", when="@6.1 ~opengl")

    depends_on("qmake")
    with when("^[virtuals=qmake] qt-base"):
        depends_on("qt-svg")
        depends_on("qt-tools", when="+designer")
        depends_on("qt-base+opengl+widgets", when="+opengl")
    with when("^[virtuals=qmake] qt"):
        depends_on("qt+tools", when="+designer")
        depends_on("qt+opengl", when="+opengl")

    # Qwt@:6.1 does not support Qt6; this picks the right qmake provider
    conflicts(
        "^[virtuals=qmake] qt-base", when="@:6.1", msg="Qwt support for Qt6 was added in v6.2.0"
    )

    # the qt@5.14.2 limitation was lifted in qwt@6.1.5
    # https://sourceforge.net/p/qwt/code/HEAD/tree/tags/qwt-6.1.6/CHANGES-6.1
    depends_on("qt@:5.14.2", when="@:6.1.4")
    # Qwt 6.1.1 and older use a constant that was removed in Qt 5.4
    # https://bugs.launchpad.net/ubuntu/+source/qwt-qt5/+bug/1485213
    depends_on("qt@:5.3", when="@:6.1.1")

    def patch(self):
        # Subvert hardcoded prefix
        filter_file(r"/usr/local/qwt-\$\$(QWT_)?VERSION.*", self.prefix, "qwtconfig.pri")

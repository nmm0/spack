# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class EtsfIo(Package):
    """ETSF_IO is a library implementing the Nanoquanta/ETSF file
    format specifications.

    ETSF_IO enables an architecture-independent exchange of crystallographic
    data, electronic wavefunctions, densities and potentials, as well as
    spectroscopic data. It is meant to be used by quantum-physical and
    quantum-chemical applications relying upon Density Functional Theory (DFT).
    """

    homepage = "https://github.com/ElectronicStructureLibrary/libetsf_io"
    url = "https://launchpad.net/etsf-io/1.0/1.0.4/+download/etsf_io-1.0.4.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.0.4", sha256="3140c2cde17f578a0e6b63acb27a5f6e9352257a1371a17b9c15c3d0ef078fa4")

    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Add MPI support")

    depends_on("netcdf-fortran")
    depends_on("hdf5+mpi~cxx", when="+mpi")  # required for NetCDF-4 support
    depends_on("gmake", type="build")

    patch("tests_module.patch")
    patch("tests_init.patch")

    def flag_handler(self, name, flags):
        if name == "fflags":
            flags.append(self.compiler.f77_pic_flag)
        elif name == "fcflags":
            flags.append(self.compiler.fc_pic_flag)
        return flags, None, None

    def install(self, spec, prefix):
        # Specify installation directory for Fortran module files
        # Default is [INCLUDEDIR/FC_TYPE]
        options = [f"--prefix={prefix}", f"--with-moduledir={prefix.include}"]

        # Netcdf4/HDF
        hdf_libs = f"-L{spec['hdf5'].prefix.lib} -lhdf5_hl -lhdf5"
        options.extend(
            [
                f"--with-netcdf-incs=-I{spec['netcdf-fortran'].prefix.include}",
                f"--with-netcdf-libs=-L{spec['netcdf-fortran'].prefix.lib} "
                f"-lnetcdff -lnetcdf {hdf_libs}",
            ]
        )

        configure(*options)

        make()
        make("check")
        make("install")

    def test_etsf_io_help(self):
        """check etsf_io can execute (--help)"""

        etsfio = which(self.prefix.bin.etsf_io)
        out = etsfio("--help", output=str.split, error=str.split)
        assert "Usage: etsf_io" in out

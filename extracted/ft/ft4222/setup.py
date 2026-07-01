#  _____ _____ _____
# |_    |   __| __  |
# |_| | |__   |    -|
# |_|_|_|_____|__|__|
# MSR Electronics GmbH
# SPDX-License-Identifier: MIT
#

from setuptools import setup, Extension
from Cython.Distutils.build_ext import build_ext
from platform import system, machine, architecture
import shutil


if system() == "Linux":
    if machine() == "x86_64":
        libdir = "linux/build-x86_64"
    elif machine() in ["i386", "i686"]:
        libdir = "linux/build-x86_32"
    elif machine() == "armv7l":
        libdir = "linux/build-arm-v7-hf"
    elif machine().startswith("arm"):
        if architecture()[0] == "64bit":
            libdir = "linux/build-arm-v8"
        else:
            libdir = "linux/build-arm-v6-hf"
    elif machine() == "aarch64":
        libdir = "linux/build-arm-v8"
    else:
        raise Exception("Unsupported machine and or architecture")

    libs = ["ft4222"]
    incdirs = ["linux"]
    libdirs = [libdir]
    rlibdirs = ["$ORIGIN/."]
    libs_to_copy = ["libft4222.so"]
elif system() == "Darwin":
    libdir = "./osx"
    ft4222_dll = "libft4222.dylib"

    libs = ["ft4222"]  # , "ftd2xx"]
    incdirs = ["osx"]
    libdirs = [libdir]
    rlibdirs = []  #'$ORIGIN/.']
    libs_to_copy = [ft4222_dll, "libftd2xx.dylib"]
else:
    if architecture()[0] == "64bit":
        libdir = "win/amd64"
        libs = ["LibFT4222-64", "ftd2xx"]
        libs_to_copy = ["LibFT4222-64.dll", "ftd2xx.dll"]
    else:
        libdir = "win/i386"
        libs = ["LibFT4222", "ftd2xx"]
        libs_to_copy = ["LibFT4222.dll", "ftd2xx.dll"]

    incdirs = ["win"]
    libdirs = [libdir]
    rlibdirs = []


class mybuild(build_ext):
    def run(self):
        super().run()
        print("running mybuild")
        build_py = self.get_finalized_command("build_py")
        for package, _, build_dir, _ in build_py.data_files:
            if package == "ft4222":
                for lib in libs_to_copy:
                    print("copying {} -> {}".format(libdir + "/" + lib, "ft4222/" + lib))
                    shutil.copyfile(libdir + "/" + lib, build_dir + "/" + lib)
                break


extensions = [
    Extension(
        "ft4222.ft4222",
        ["ft4222/ft4222.pyx"],
        libraries=libs,
        include_dirs=incdirs,
        library_dirs=libdirs,
        runtime_library_dirs=rlibdirs,
    ),
]

setup(
    ext_modules=extensions,
    cmdclass={"build_ext": mybuild},
)

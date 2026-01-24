import pathlib
import platform
import os


from cffi import FFI

ffi = FFI()
data_dir = pathlib.Path(os.path.dirname(__file__)).absolute().parent / "data"

arch = platform.machine()
if arch == "AMD64":
    platform_dir = data_dir / "x86_64"
elif arch == "x86_64":
    platform_dir = data_dir / "x86_64"
elif arch == "arm64" or arch == "aarch64":
    platform_dir = data_dir / "aarch64"
else:
    raise ValueError("Hypertune SDK is not supported on architecture:", arch)

system = platform.system()
if system == "Darwin":
    lib_name = "libhypertune.dylib"
elif system == "Linux":
    lib_name = "libhypertune.so"
elif system == "Windows":
    lib_name = "hypertune.dll"
else:
    raise ValueError("Hypertune SDK is not supported on system:", system)

with open(data_dir / "hypertune.h") as header:
    ffi.cdef(header.read())

lib = platform_dir / lib_name
clib = ffi.dlopen(str(lib))

import sys
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Pybind11Extension already adds /EHsc and /bigobj on Windows and
# -fvisibility=hidden and -g0 elsewhere.
if sys.platform == 'win32':
    compile_args = ['/W4']
else:
    compile_args = ['-O3', '-Wall', '-Wextra']

ext_modules = [
    Pybind11Extension(
        '_icet',
        sorted(glob('src/*.cpp')),
        include_dirs=[
            'src/3rdparty/eigen3/'
        ],
        language='c++',
        cxx_std=17,
        extra_compile_args=compile_args
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)

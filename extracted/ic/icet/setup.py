import sys
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

if sys.platform == 'win32':
    compile_args = ['/EHsc']
else:
    compile_args = ['-std=c++14', '-O3', '-fvisibility=hidden']

ext_modules = [
    Pybind11Extension(
        '_icet',
        sorted(glob('src/*.cpp')),
        include_dirs=[
            'src/3rdparty/boost_1_68_0/',
            'src/3rdparty/eigen3/'
        ],
        language='c++',
        extra_compile_args=compile_args
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)

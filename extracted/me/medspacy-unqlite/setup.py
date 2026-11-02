import glob
import sys
import warnings

from setuptools import setup
from setuptools.extension import Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cython_installed = False
    warnings.warn('Cython not installed, using pre-generated C source file.')
else:
    cython_installed = True


if cython_installed:
    python_source = 'unqlite.pyx'
else:
    python_source = 'unqlite.c'
    cythonize = lambda obj: obj

if sys.platform.find('win') < 0:
    libs = ['pthread']
else:
    libs = []

library_source = ['src/unqlite.c']
unqlite_extension = Extension(
    'unqlite',
    define_macros=[('UNQLITE_ENABLE_THREADS', '1')],
    libraries=libs,
    sources=[python_source] + library_source)

setup(
    name='medspacy_unqlite',
    version='0.9.8',
    description='Fast Python bindings for the UnQLite embedded NoSQL database.',
    author=['Charles Leifer','medspacy'],
    author_email='',
    url='https://github.com/medspacy/medspacy-unqlite',
    #install_requires=['Cython'],
    #setup_requires=['cython'],
    ext_modules=cythonize([unqlite_extension])
)

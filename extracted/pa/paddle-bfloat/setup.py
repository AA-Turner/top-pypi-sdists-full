import os
import sys
import shutil
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

PACKAGE_NAME='paddle_bfloat'

if 'clean' in sys.argv:
    curdir = os.path.dirname(os.path.realpath(__file__))
    for filepath in ['build', 'dist', PACKAGE_NAME + '.egg-info', 'MANIFEST']:
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                os.remove(filepath)
            else:
                shutil.rmtree(filepath)

def set_builtin(name, value):
    if isinstance(__builtins__, dict):
        __builtins__[name] = value
    else:
        setattr(__builtins__, name, value)

class my_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        set_builtin('__NUMPY_SETUP__', False)
        import numpy
        self.include_dirs.append(numpy.get_include())

    def build_extensions(self):
        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except (AttributeError, ValueError):
            pass
        build_ext.build_extensions(self)

module1 = Extension(PACKAGE_NAME,
                    sources=['bfloat16.cc'],
                    extra_compile_args=['-std=c++11'])

setup(name=PACKAGE_NAME,
      version='0.1.7',
      description='Paddle numpy bfloat16 package',
      license='Apache',
      author='Jakub Piasecki',
      author_email='jakub1.piasecki@intel.com',
      setup_requires=['numpy>=1.13'],
      ext_modules=[module1],
      packages=find_packages(),
      cmdclass={'build_ext': my_build_ext})

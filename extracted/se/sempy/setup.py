#from distutils.core import setup
#from distutils.extension import Extension

import ez_setup
ez_setup.use_setuptools()

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
      name     = 'sempy',
      version = '0.0.18',
      packages = find_packages(),
      include_package_data = True,
      package_data={'': ['*.so','*.f90','*.geo','*.msh']},
      url = 'http://www.sempy.org',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Fortran',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
       ],
      #install_requires = ['numpy>=1.5','scipy>=0.7'],
      #dependency_links = ["https://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.0.1/"],
      # metadata for upload to PyPI
      author = 'Stian Jensen',
      author_email = 'stianjnsn@gmail.com',
      description = 'A Python implementation of the spectral element method',
      long_description = read("README.rst"),
      license= 'GPL',
      )

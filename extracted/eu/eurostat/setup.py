# -*- coding: utf-8 -*-
"""
@author: Noemi E. Cazzaniga - 2023
@email: noemi.cazzaniga@polimi.it
"""


from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_descr = f.read()

setup(name='eurostat',
      version='1.1.1',
      license='MIT',
      date='2024',
      description="Eurostat Python Package",
      long_description=long_descr,
      long_description_content_type='text/markdown',
      author='Noemi Emanuela Cazzaniga',
      author_email='noemi.cazzaniga@polimi.it',
      keywords='eurostat comext prodcom statistics data economics science',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Science/Research',
          'Topic :: Office/Business',
          'Topic :: Office/Business :: Financial',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Utilities',
          ],
      project_urls={
          'Source': 'https://bitbucket.org/noemicazzaniga/eurostat/src/master/',
      },
      packages=find_packages(),
      python_requires='>=3.5',
      install_requires=[
          'pandas',
          'requests',
          ],
      )

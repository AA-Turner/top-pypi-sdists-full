#!/usr/bin/env python

from distutils.core import setup

setup(name='common',
      version='0.1.2',
      description='Common tools and data structures implemented in pure python.',
      author='Marcel Hellkamp',
      author_email='marc@gsites.de',
      url='https://pypi.python.org/pypi/common',
      packages=['common', 'common.term'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
      ],
)

import os
import sys
from setuptools import setup

sys.path.insert(0, os.path.join('.', 'src'))


def requirements():
    with open('requirements.txt', 'r') as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


__version__ = read('version')


setup(
    name='dnutils',
    packages=['dnutils', 'dnutils.version'],
    package_dir={
        '': 'src',
    },
    version=__version__,
    description='A collection of convenience tools for everyday Python programming',
    long_description=read('README.md'),
    author='Daniel Nyga',
    author_email='nyga@cs.uni-bremen.de',
    download_url='https://github.com/danielnyga/dnutils/archive/%s.tar.gz' % __version__,
    keywords=['testing', 'logging', 'threading', 'multithreading', 'debugging', 'tools', 'utilities'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=requirements(),
)

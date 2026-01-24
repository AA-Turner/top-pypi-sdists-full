from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

requirements = ['pyxlsb', 'xlrd', 'pandas', 'openpyxl', 'scipy']
test_requirements = ['pytest']

v_temp = {}
with open("mrio_common_metadata/version.py") as fp:
    exec(fp.read(), v_temp)
version = ".".join((str(x) for x in v_temp['version']))


setup(
    name='mrio_common_metadata',
    version=version,
    packages=find_packages(exclude=['tests', 'docs']),
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license="BSD 3-clause",
    # Only if you have non-python data (CSV, etc.). Might need to change the directory name as well.
    # package_data={'your_name_here': package_files(os.path.join('bw_exiobase', 'data'))},
    install_requires=requirements,
    url="https://github.com/brightway-lca/mrio_common_metadata",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    description='Common Datapackage schema and utilities for MRIO tables',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

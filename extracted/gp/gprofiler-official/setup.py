import setuptools
import pathlib


with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = None
version = exec(open(pathlib.Path(__file__).parent / 'gprofiler' / 'version.py').read())

setuptools.setup(
    name="gprofiler-official",
    version=__version__,
    author="Uku Raudvere",
    author_email="biit.support@ut.ee",
    description="Functional enrichment analysis and more via the g:Profiler toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://biit.cs.ut.ee/gprofiler/",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    install_requires=[
        'requests',
    ],

)

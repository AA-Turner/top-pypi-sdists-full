import sys

import numpy
from Cython.Build import cythonize
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

class _build_ext(build_ext):
    """build_ext command for use when numpy and Cython are needed.

    https://stackoverflow.com/a/42163080/8083313

    """

    def run(self):
        # Cythonize the extension (and path the `_needs_stub` attribute,
        # which is not set by Cython but required by `setuptools`)
        self.extensions = cythonize(self.extensions, force=self.force)
        for extension in self.extensions:
            extension._needs_stub = False

        # Call original build_ext command
        build_ext.run(self)


doc = open("README.md").read()
cfisher_ext = Extension(
    "fishersrc.cfisher",
    ["src/cfisher.pyx"], 
    extra_compile_args=["-O3"],
    include_dirs=[numpy.get_include()],
)
cmdclass = {"build_ext": _build_ext}

setup_options = dict(
    name="fishersrc",
    version="0.1.15",
    description="Fast Fisher's Exact Test",
    url="http://github.com/mmore500/fishersrc",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="maintainer Matthew Andres Moreno (original authors Haibao Tang, Brent Pedersen)",
    author_email="m.more500@gmail.com",
    ext_modules=[cfisher_ext],
    cmdclass=cmdclass,
    install_requires=['numpy'],
    setup_requires=["numpy", "cython"],
    keywords="statistics cython",
    license="BSD",
    packages=["fishersrc"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

setup(**setup_options)

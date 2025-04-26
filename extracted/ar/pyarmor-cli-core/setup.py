import sys
from setuptools import setup

__VERSION__ = '7.6.6'

with open('README.rst') as f:
    long_description = f.read()

is_android = hasattr(sys, 'getandroidapilevel')
is_freebsd = sys.platform.startswith(('freebsd', 'openbsd', 'isilon onefs'))

setup(
    name="pyarmor.cli.core",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version=__VERSION__,
    description="Provide extension module pytransform3 for Pyarmor",
    long_description=long_description,

    license='Free To Use But Restricted',

    url="https://github.com/dashingsoft/pyarmor",
    author="Jondy Zhao",
    author_email="pyarmor@163.com",

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        # Pick your license as you wish
        "License :: Free To Use But Restricted",

        # Support platforms
        "Operating System :: Android",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Topic :: Security",
        "Topic :: System :: Software Distribution",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="protect obfuscate encrypt obfuscation distribute",

    packages=["pyarmor.cli.core"],
    package_dir={"pyarmor.cli.core": "pyarmor/cli/core"},
    package_data={"pyarmor.cli.core": ["pytransform3*", "pyarmor_runtime*"]},
    install_requires=(
        ['pyarmor.cli.core.android==%s' % __VERSION__] if is_android else
        ['pyarmor.cli.core.freebsd==%s' % __VERSION__] if is_freebsd else
        []
    )
)

# -*- coding: utf-8 -*-

"""
RapidPE: The original low-latency gravitational wave parameter estimation code.

RapidPE was the first piece of software written for rapidly measuring the
parameters of compact binary mergers observed via gravitational waves.  It
leverages properties of general relativity in order to minimize the number of
simulations needed, thereby reducing the dominant cost of parameter estimation.

To install, run::

    $ pip install rapid-pe
"""

import datetime
import os
import re
import sys
from glob import glob

from setuptools import (setup, find_packages)


# -- description --------------------------------
description = (
    "The original low-latency gravitational wave parameter estimation code."
)

def find_version(path):
    """Parse the __version__ metadata in the given file.
    """
    with open(path, "r") as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        version = version_match.group(1)

        if "NIGHTLY_BUILD" in os.environ:
            timestamp = datetime.datetime.today().strftime("%Y%m%d")
            version = f"{version}.dev{timestamp}"

        return version

    else:
        raise RuntimeError("Unable to find version string.")


# -- dependencies -------------------------------

setup_requires = [
    "setuptools",
]
install_requires = [
    "bilby",
    "h5py",
    "healpy",
    "lalsuite",
    "ligo.skymap",
    "lscsoft-glue",
    "matplotlib",
    "numpy",
    "python-ligo-lw>=1.8.1,<1.9",
    "scikit-learn",
    "scipy",
    "six",
]

# run setup
setup(
    # metadata
    name="rapid_pe",
    version=find_version(os.path.join("rapid_pe", "__init__.py")),
    description=__doc__.strip().split('\n')[0],
    long_description='\n'.join(__doc__.strip().split('\n')[1:]).strip(),
    license="GPL-2+",
    url="https://git.ligo.org/rapidpe-rift/rapidpe/",
    project_urls={
        "Bug Tracker": "https://git.ligo.org/rapidpe-rift/rapidpe/-/issues/",
        "Source Code": "https://git.ligo.org/rapidpe-rift/rapidpe/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    # content
    packages=find_packages(),
    scripts=list(glob(os.path.join("bin", "rapidpe*"))),
    # dependencies
    setup_requires=setup_requires,
    install_requires=install_requires,
)

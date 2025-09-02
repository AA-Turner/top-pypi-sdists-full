#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

import codecs
import shlex
import subprocess
import time

from pathlib import Path

from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.install_scripts import install_scripts

from package_info import __version__

from package_info import __package_name__
from package_info import __contact_names__
from package_info import __contact_emails__
from package_info import __repository_url__
from package_info import __download_url__
from package_info import __description__
from package_info import __license__
from package_info import __keywords__

from edit_pip_configuration import create_pip_config_file
from edit_pip_configuration import maybe_edit_pip_config_file

from nvidia_pyindex.utils import get_configuration_files
from nvidia_pyindex.utils import get_configuration_files_by_priority

SUPPORTED_PLATFORMS = [
    "linux",
    "win32",  # Windows
    "darwin",  # Mac OS X
]


def _install_nvidia_pypi_index():
    try:
        subprocess.call(
            shlex.split("nvidia_pyindex uninstall"),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

    debug_mode = bool(os.environ.get("DEBUG_MODE", False))

    config_filedict = get_configuration_files()
    config_filelist = get_configuration_files_by_priority()

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Setting User Pip Configuration ...")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("\n######################\n")

    pre_existing_configfile = None
    for config_file in config_filelist:
        try:
            if os.path.isfile(config_file):
                print("Editing pip conf file: %s ..." % config_file)
                maybe_edit_pip_config_file(
                    config_file,
                    config_filedict=config_filedict,
                    debug_mode=debug_mode
                )
                pre_existing_configfile = config_file
                break
        except (FileNotFoundError, PermissionError) as e:
            print("Error: {}: {}".format(e.__class__.__name__, str(e)))
            pass

    if pre_existing_configfile is None:
        for config_file in config_filelist:
            print("\nProcessing pip conf file: %s ..." % config_file)
            try:
                if not os.path.exists(config_file):
                    print("Creating pip conf file: %s ..." % config_file)
                    create_pip_config_file(
                        filepath=config_file,
                        config_filedict=config_filedict
                    )
            except (FileNotFoundError, PermissionError) as e:
                print("Error: {}: {}".format(e.__class__.__name__, str(e)))
                pass
    else:
        with open(pre_existing_configfile, 'r') as _file:
            original_content = _file.readlines()

        for config_file in config_filelist:
            print("\nProcessing pip conf file: %s ..." % config_file)
            try:

                try:
                    with open(config_file, 'r') as _file:
                        backup_content = _file.readlines()
                except:
                    pass

                try:
                    os.remove(config_file)
                    os.remove(config_file.old)
                    with open("%s.old" % config_file, 'w') as _file:
                        _file.writelines(backup_content)
                except:
                    pass

                with open(config_file, 'w') as _file:
                    _file.writelines(original_content)

            except (FileNotFoundError, PermissionError) as e:
                print("Error: {}: {}".format(e.__class__.__name__, str(e)))
                pass

    print("\n######################\n")

    time.sleep(2)  # allow readable logs in verbose logs. Please do not delete.


def _force_clean_cache_whl(pkg_name):
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Cleaning Potential Wheel Cache ...")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    if sys.argv[1] == "sdist":
        return

    pkg_names = [pkg_name, pkg_name.replace("-", "_")]

    import appdirs
    for path in Path(appdirs.user_cache_dir("pip/wheels")).rglob('*.whl'):
        if any([pkg in path.name for pkg in pkg_names]):
            print("Removing: `%s`" % path)
            path.unlink()

    time.sleep(2)  # allow readable logs in verbose logs. Please do not delete.


class InstallCommand(install):
    """A class for "pip install".
    Handled by "pip install rpm-py-installer",
    when the package is published to PyPI as a source distribution (sdist).
    """

    def run(self):
        """Run install process."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("COMMAND: %s" % InstallCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        _install_nvidia_pypi_index()
        super(InstallCommand, self).run()
        _force_clean_cache_whl(__package_name__)


class DevelopCommand(develop):
    """A class for setuptools development mode.
    Handled by "pip install -e".
    """

    def run(self):
        """Run install process with development mode."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("COMMAND: %s" % DevelopCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        _install_nvidia_pypi_index()
        super(DevelopCommand, self).run()
        _force_clean_cache_whl(__package_name__)


class InstallScriptsCommand(install_scripts):
    """A class for setuptools development mode.
    Handled by "pip install -e".
    """

    def run(self):
        """Run install process with development mode."""
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("COMMAND: %s" % InstallScriptsCommand.__name__)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        super(InstallScriptsCommand, self).run()
        _force_clean_cache_whl(__package_name__)


if __name__ == "__main__":

    # ┍━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━┑
    # │ System              │ `sys.platform` Value │
    # ┝━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━┥
    # │ Linux               │ linux                │
    # │ Windows             │ win32                │
    # │ Windows/Cygwin      │ cygwin               │
    # │ Windows/MSYS2       │ msys                 │
    # │ Mac OS X            │ darwin               │
    # │ OS/2                │ os2                  │
    # │ OS/2 EMX            │ os2emx               │
    # │ RiscOS              │ riscos               │
    # │ AtheOS              │ atheos               │
    # │ FreeBSD 7           │ freebsd7             │
    # │ FreeBSD 8           │ freebsd8             │
    # │ FreeBSD N           │ freebsdN             │
    # │ OpenBSD 6           │ openbsd6             │
    # ┕━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━┙
    if sys.platform not in SUPPORTED_PLATFORMS:
        raise OSError("Your operating system is not supported by "
                      "`nvidia-pyindex`: {}.\nOnly these systems are "
                      "supported: `{}`.".format(
                        sys.platform, SUPPORTED_PLATFORMS
                      )
        )

    # Get the long description
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    setup(
        name=__package_name__,
        version=__version__,
        description=__description__,
        long_description=long_description,
        url=__repository_url__,
        download_url=__download_url__,
        author=__contact_names__,
        author_email=__contact_emails__,
        maintainer=__contact_names__,
        maintainer_email=__contact_emails__,
        license=__license__,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Information Technology',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Image Recognition',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: OS Independent',
        ],
        keywords=__keywords__,
        setup_requires=[
            'appdirs>=1.4,<1.5',
        ],
        cmdclass={
            'install': InstallCommand,
            'develop': DevelopCommand
        },
        entry_points={
            'console_scripts': [
                'nvidia_pyindex=nvidia_pyindex.cmdline:main',
            ],
        },
        platforms=["Linux"],
        include_package_data=True,
        packages=find_packages(),
    )

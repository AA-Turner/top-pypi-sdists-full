import sys
from packaging import version
from setuptools.build_meta import *

def _check_python_version():
    current_version = version.parse(f"{sys.version_info.major}.{sys.version_info.minor}")
    max_version = version.parse("3.13")
    
    if current_version > max_version:
        sys.stderr.write(f"Python {current_version} is not supported. Please use Python 3.13 or lower.\n")
        sys.exit(1)

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    _check_python_version()
    return __legacy__.prepare_metadata_for_build_wheel(metadata_directory, config_settings)

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _check_python_version()
    return __legacy__.build_wheel(wheel_directory, config_settings, metadata_directory)

def build_sdist(sdist_directory, config_settings=None):
    _check_python_version()
    return __legacy__.build_sdist(sdist_directory, config_settings) 
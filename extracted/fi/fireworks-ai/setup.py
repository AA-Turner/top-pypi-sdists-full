import os
from setuptools import setup
import versioneer

version = os.getenv("FIREWORKS_BUILD_VERSION") or versioneer.get_version()

setup(version=version, cmdclass=versioneer.get_cmdclass())

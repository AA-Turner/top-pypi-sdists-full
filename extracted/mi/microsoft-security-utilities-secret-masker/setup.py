#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Azure Command Diff Tools package that can be installed using setuptools"""
import os
import re
from setuptools import setup, find_packages

root_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(root_path, 'microsoft_security_utilities_secret_masker', '__init__.py'), 'r') as version_file:
    __VERSION__ = re.search(r'^__VERSION__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            version_file.read(), re.MULTILINE).group(1)

with open('README.rst', 'r', encoding='utf-8') as f:
    README = f.read()
with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    HISTORY = f.read()

setup(name="microsoft-security-utilities-secret-masker",
      version=__VERSION__,
      description="A tool for detecting and masking secrets",
      long_description=README + '\n\n' + HISTORY,
      license='MIT',
      author='Microsoft Corporation',
      author_email='azpycli@microsoft.com',
      packages=find_packages(exclude=["*.test*"]),
      include_package_data=True,
      install_requires=[],
      package_data={
        "microsoft_security_utilities_secret_masker.GeneratedRegexPatterns": ["*.json"]
      }
      )

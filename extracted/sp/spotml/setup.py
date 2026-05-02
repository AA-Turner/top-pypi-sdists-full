#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages

REQUIRED = []
with open('requirements.txt') as f:
    for line in f.readlines():
        REQUIRED.append(line.replace('\n', ''))
REQUIRES_PYTHON = '>=3.6.0'


def get_version():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root_dir, 'spotml', '__init__.py')) as f:
        content = f.read()

    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.M)
    if not version_match:
        raise RuntimeError('Unable to find version string.')

    return version_match.group(1)


def get_description():
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Pypi.md'))
    with open(readme_path, encoding='utf-8') as f:
        description = f.read()

    return description


setup(name='spotml',
      version=get_version(),
      description='Automate ML training on spot instances easily.',
      url='https://spotml.io/',
      author='Vishnu',
      author_email='vishnu@spotml.io',
      long_description=get_description(),
      long_description_content_type='text/markdown',
      install_requires=REQUIRED,
      python_requires=REQUIRES_PYTHON,
      entry_points={
          'console_scripts': ['spotml=spotml.cli:main']
      },
      packages=find_packages(exclude=['tests*']),
      package_data={
          'spotml.deployment.container.docker.scripts': ['data/*', 'data/*/*'],
          'spotml.providers.aws.cfn_templates.instance': ['data/*', 'data/*/*'],
          'spotml.providers.aws.cfn_templates.instance_profile': ['data/*', 'data/*/*'],
          'spotml.providers.gcp.dm_templates.instance': ['data/*', 'data/*/*'],
      },
      tests_require=['moto'],
      test_suite='tests',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ])

import os
import shutil

from setuptools import setup, find_packages

src_dir = 'main'
package_directory = 'oauth2_client'
package_name = 'oauth2-client'

__version__ = None
version_file = '%s/%s/__init__.py' % (src_dir, package_directory)
with open(version_file, 'r') as f:
    for line in f.readlines():
        if line.find('__version__') >= 0:
            exec(line)

if __version__ is None:
    raise AssertionError('Failed to load version from %s' % version_file)


def purge_sub_dir(path):
    shutil.rmtree(os.path.join(os.path.dirname(__file__), path))


setup(name=package_name,
      version=__version__,
      zip_safe=False,
      packages=find_packages(where=src_dir),
      author='Benjamin Einaudi',
      author_email='antechrestos@gmail.com',
      description='A client library for OAuth2',
      long_description=open('README.rst').read(),
      url='http://github.com/antechrestos/OAuth2Client',
      classifiers=[
          "Programming Language :: Python",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Topic :: Communications",
      ],
      package_dir={package_directory: '%s/%s' % (src_dir, package_directory)},
      install_requires=[requirement.rstrip(' \r\n') for requirement in open('requirements.txt').readlines()],
      )

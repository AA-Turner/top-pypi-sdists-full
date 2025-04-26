from setuptools import setup

import io

long_description = io.open('README.rst', encoding='utf8').read()

setup(
  name='lzstring',
  version='1.0.4',
  description='lz-string for python',
  author='Geza Kovacs',
  author_email='geza0kovacs@gmail.com',
  packages=['lzstring'],
  package_dir={'lzstring': 'lzstring'},
  package_data={},
  long_description=long_description,
  url='https://github.com/gkovacs/lz-string-python',
  download_url='https://github.com/gkovacs/lz-string-python',
  keywords=['lz-string', 'lzstring', 'compression'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    ],
    install_requires=['future>=0.14.0'],
)
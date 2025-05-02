from setuptools import setup, find_packages
import os

# compatible for py27
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    long_description = '{}\n{}\nDownload\n======\n'.format(
        open('README.md').read(),
        open('CHANGES.md').read()
    )
except FileNotFoundError:
    long_description = ''

setup(
    name="calmsize",
    version="0.1.3",
    description="Fork from hurry.filesize, A simple Python library for human readable file sizes (or anything sized in bytes).",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='file size bytes',
    author='Kaiyu Shi',
    author_email='skyisno.1@gmail.com',
    url='https://github.com/Stonesjtu/calmsize',
    license='ZPL 2.1',
    packages=['calmsize'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
    ],
)

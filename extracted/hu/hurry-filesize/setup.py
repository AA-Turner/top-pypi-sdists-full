from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('src', 'hurry', 'filesize', 'README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '========\n'
    )

setup(
    name="hurry.filesize",
    version="0.9",
    description="A simple Python library for human readable file sizes (or anything sized in bytes).",
    long_description=long_description,    
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='file size bytes',
    author='Martijn Faassen, Startifact',
    author_email='faassen@startifact.com',
    url='',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir= {'':'src'},
    namespace_packages=['hurry'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       'setuptools',
       ],
    )

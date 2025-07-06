import os
from setuptools import setup

with open('README.rst') as F:
    README = F.read()

setup(
    name='python-dataporten-auth',
    version='2.0.0',
    packages=['dataporten'],
    include_package_data=True,
    package_dir = {'': 'src',},
    platforms=['any'],
    zip_safe=False,
    license='MIT',
    description='A plugin for python-social-auth to authenticate with dataporten',
    long_description=README,
    install_requires=['social-auth-core'],
    url='https://github.com/UNINETT/python-dataporten-auth',
    author='Hanne Moa',
    author_email='hanne.moa@uninett.no',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Flask',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords=['django', 'oauth2',],
)

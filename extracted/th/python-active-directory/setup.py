#
# This file is part of Python-AD. Python-AD is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# Python-AD is copyright (c) 2007 by the Python-AD authors. See the file
# "AUTHORS" for a complete overview.
from setuptools import setup, Extension


setup(
    name='python-active-directory',
    version='2.0.1',
    description='An Active Directory client library for Python',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Geert Jansen',
    author_email='programmers@theatlantic.com',
    maintainer='The Atlantic',
    maintainer_email='programmers@theatlantic.com',
    url='https://github.com/theatlantic/python-active-directory',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'lib'},
    packages=[
        'activedirectory',
        'activedirectory.core',
        'activedirectory.protocol',
        'activedirectory.util'
    ],
    install_requires=['python-ldap>=3.0', 'dnspython', 'ply>=3.8'],
    ext_modules=[Extension(
        'activedirectory.protocol.krb5',
        ['lib/activedirectory/protocol/krb5.c'],
        libraries=['krb5']
    )],
    zip_safe=False,  # eggs are the devil.
)

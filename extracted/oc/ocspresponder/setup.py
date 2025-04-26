from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Load README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Load requirements
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    lines = f.readlines()
    requirements = [l.strip().strip('\n') for l in lines
                    if l.strip() and not l.strip().startswith('#')]

setup(
    name='ocspresponder',
    version='0.5.0',

    description='RFC 6960 compliant OCSP Responder framework written in Python 3.5+.',
    long_description=long_description,

    url='https://github.com/threema-ch/ocspresponder/',

    author='Threema GmbH',
    author_email='github@threema.ch',

    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ocsp responder server ssl tls pki',

    packages=['ocspresponder'],
    install_requires=requirements,
    package_data={
        '': ['README.md', 'LICENSE.txt', 'CHANGELOG.md', 'requirements.txt'],
    },
)

import os
from setuptools import setup
import nrt_pytest_soft_asserts


PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(PATH, 'README.md')) as f:
    readme = f.read()

setup(
    name='nrt-pytest-soft-asserts',
    version=nrt_pytest_soft_asserts.__version__,
    author='Eyal Tuzon',
    author_email='eyal.tuzon.dev@gmail.com',
    description='Soft asserts for pytest',
    keywords='python python3 python-3 pytest soft assert asserts assertion'
             ' assertions soft-assert soft-asserts soft-assertion soft-assertions'
             'test test-framework unit-test',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://github.com/etuzon/python-nrt-pytest-soft-asserts',
    packages=['nrt_pytest_soft_asserts'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 5 - Production/Stable'
    ],
    install_requires=[requirements],
    data_files=[('', ['requirements.txt'])],
)

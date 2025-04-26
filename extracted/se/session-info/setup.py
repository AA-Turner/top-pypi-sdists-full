from os import path
from setuptools import setup, find_packages
import versioneer


# Read the contents of the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='session_info',
    url='https://gitlab.com/joelostblom/session_info',
    author='Joel Ostblom',
    author_email='joel.ostblom@protonmail.com',
    packages=find_packages(),
    install_requires=['stdlib_list'],
    python_requires='>=3.6',
    # Automatic version number
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3',
    description='session_info outputs version information for modules loaded in the current session, Python, and the OS.',
    # Include readme in markdown format, GFM markdown style by default
    long_description=long_description,
    long_description_content_type='text/markdown'
)

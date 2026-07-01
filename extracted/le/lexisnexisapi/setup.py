import os
from setuptools import setup, find_packages

VERSION = '3.0.3.13'

#I think I can get rid of this, but I'll test next time.
#def read(fname):
#    return open(os.path.join(os.getcwd(), fname)).read()

setup(
    name="lexisnexisapi",
    version= VERSION,
    license='MIT',
    author="Robert Cuffney",
    author_email='Robert Cuffney <robert.cuffney@lexisnexis.com>',
    description = 'a module to support lexisnexis api(s)',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown', 
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://pypi.org/project/lexisnexisapi/',
    keywords='metabase webservices lexisnexis',
    install_requires=['pandas','requests','xmltodict',],
)

import re
import os
import sys
import codecs
import stat

from setuptools import setup, find_packages

def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()

# with open('requirements.txt') as f:
#     install_requires = f.read().splitlines()
# python setup.py sdist upload -r pypi

def get_data_files(*dirs):
    results = []
    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            res = (root, map(lambda f:root + "/" + f, files))
            results.append(res)
    # print results
    return results

tests_require = ['pytest', 'virtualenv>=1.10', 'scripttest>=1.3', 'mock']

setup(
    name='mm',
    version='0.2.6',
    packages=find_packages(exclude=["test*","build","dist"]),
    data_files = get_data_files("mm/bin"),
    install_requires=['Jinja2', 'suds==0.4', 'keyring', 'MarkupSafe==0.18', 'requests==2.3.0'],
    entry_points={
        'console_scripts':
            ['mm = mm:main']
    },
    url='https://github.com/joeferraro/mm',
    include_package_data=True,
    author='@joeferraro',
    author_email='info@mavensmate.com',
    description='CLI for MavensMate',
    license='GNU v2',
    keywords='mavensmate salesforce salesorce1 force.com ide cli',
    test_suite='test'
)

if 'darwin' in sys.platform:
    #make MavensMateWindowServer executable
    st = os.stat('mm/bin/MavensMateWindowServer.app/Contents/MacOS/MavensMateWindowServer')
    os.chmod('mm/bin/MavensMateWindowServer.app/Contents/MacOS/MavensMateWindowServer', st.st_mode | stat.S_IEXEC)
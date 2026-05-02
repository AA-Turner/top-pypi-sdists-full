"""
Publish a new version:
$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags
$ # edit setup.py for new version
$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel --universal
$ twine upload dist/*
"""
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '1.0.3'
DOWNLOAD_URL = (
    'https://github.com/ruru4143/spotify-webapi' + VERSION
)

setup(
    name='spotify_webapi',
    packages=['spotify_webapi'],
    version=VERSION,
    url='https://github.com/ruru4143/spotify-webapi',
    license='GPLv3',
    author='ruru4143',
    author_email='pypi@ruru.pw',
    description='get tracks of spotify playlists without using the official api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["beautifulsoup4"],
    download_url=DOWNLOAD_URL,
    keywords=[
        'spotify', 'track', 'scaping', 'webapi', 'webscraper',
        'song', 'scraper'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
)

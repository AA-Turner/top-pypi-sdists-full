from pathlib import Path
from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'A simple ML model to classify Spotify tracks using audio features.'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

setup(
    name='spotifymoods',
    version=VERSION,
    author='Ammar Oker',
    author_email='<oker.ammar@gmail.com>',
    url='https://github.com/ammar-oker/spotifymoods',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas', 'scikit_learn'],
    keywords=['spotify', 'machine learning', 'spotify moods', 'spotify emotions'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
    ]
)

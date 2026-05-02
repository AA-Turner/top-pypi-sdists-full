"""
CLI client for Spotify using Web API

(Thanks to cookiecutter and chriswarrick.com)
"""
from setuptools import find_packages, setup

dependencies = ['click', 'requests', 'configparser']

setup(
    name='spotipy-cli',
    version='0.3.0',
    url='https://github.com/kandrelczyk/spotipy-cli',
    license='Apache',
    author='Krzysztof Andrelczyk',
    author_email='cristof@vivaldi.net',
    description='CLI client for Spotify using Web API',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'spotipy-cli = spotipy_cli.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

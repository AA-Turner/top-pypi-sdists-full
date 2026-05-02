from setuptools import setup


with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name='spotifytracker',
    version='0.0.18',
    packages=['spotify_tracker'],
    url='http://github.com/eriktaubeneck/spotifytracker',
    license='MIT',
    author='Erik Taubeneck',
    author_email='erik.taubeneck@gmail.com',
    description='Track your Spotify play history.',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['spotify_tracker'],
    zip_safe=False,
    include_package_data=True,
    platforms='OS X',
    install_requires=[
        'pyyaml >=3.0, <4.a0',
        'docopt >=0.6.0, <0.7.0',
        'spotipy >=2.3.7, <2.4.0',
        'arrow > 0.7.0, < 1.0.0',
    ],
    entry_points="""
    [console_scripts]
    spotifytracker = spotify_tracker.runner:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)

from setuptools import setup
from os import path
import glob


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="springheel",
    version="7.0.2",
    description="Static site generator for webcomics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet",
    ],
    keywords="website, webcomic, static",
    url="https://www.twinkle-night.net/Code/springheel.html",
    author="Garrick",
    author_email="earthisthering@posteo.de",
    license="GPLv3+",
    packages=["springheel"],
    install_requires=[
        "feedgen",
        "python-slugify",
        "tqdm",
        "html-sanitizer",
        "Pillow"
    ],
    extras_require={
        "docs": ["sphinx>=3.4.1", "numpydoc"],
    },
    entry_points={
        "console_scripts": [
            "springheel-init=springheel.command_line:cinit",
            "springheel-build=springheel.command_line:cbuild",
            "springheel=springheel.command_line:cversion",
            "springheel-addimg=springheel.command_line:caddimg"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)

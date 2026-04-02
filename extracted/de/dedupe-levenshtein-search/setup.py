from setuptools import setup, Extension

setup(
    name="dedupe_Levenshtein_search",
    url="https://github.com/dedupeio/Levenshtein_search",
    version="1.4.5",
    author="Matt Anderson",
    maintainer="Forest Gregg",
    description="Search through documents for approximately matching strings. A fork of Matt Anderson's library for MIT licensing",
    packages=[],
    ext_modules=[Extension("Levenshtein_search", ["Lev_search.c"])],
    install_requires=[],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)

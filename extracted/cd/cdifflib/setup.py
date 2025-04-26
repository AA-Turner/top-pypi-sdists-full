from setuptools import setup, Extension

ext_modules = [Extension("_cdifflib", sources=["_cdifflib.c", "_cdifflib3.c"]),]

with open("README.md") as f:
    long_description = f.read()

setup(
    name="cdifflib",
    version="1.2.9",
    description="C implementation of parts of difflib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    py_modules=["cdifflib"],
    author="Matthew Duggan",
    author_email="mgithub@guarana.org",
    license="BSD",
    url="https://github.com/mduggan/cdifflib",
    keywords="difflib c diff",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Text Processing :: General",
    ],
)

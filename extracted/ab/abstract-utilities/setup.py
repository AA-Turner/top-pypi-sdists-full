from time import time
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abstract_utilities",
    version='0.2.2.733',
    author="putkoff",
    author_email="partners@abstractendeavors.com",
    description="Utility modules for data comparison, JSON handling, string manipulation, math operations, and general automation tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbstractEndeavors/abstract_utilities",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],

    python_requires=">=3.10",

    install_requires=[
        "lxml",
        "ezodf",
        "tiktoken",
        "geopandas",
        "abstract_windows",
        "PyPDF2",
        "pdfplumber",
        "pytesseract",
        "flask",
        "pdf2image",
        "abstract_paths",
        "pathlib>=1.0.1",
        "abstract_security>=0.0.1",
        "yt_dlp>=2023.10.13",
        "pexpect>=4.8.0",
    ],

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)

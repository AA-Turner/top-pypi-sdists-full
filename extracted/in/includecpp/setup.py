from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="IncludeCPP",
    version="4.6.5",
    author="Lilias Hatterscheidt",
    author_email="lilias@includecpp.dev",
    description="Professional C++ Python bindings with type-generic templates and native threading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liliassg/IncludeCPP",
    packages=find_packages(),
    install_requires=[
        "pybind11>=2.11.0",
        "click>=8.0.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        'console_scripts': [
            'includecpp=includecpp.cli.commands:cli',
        ],
    },
    include_package_data=True,
    package_data={
        'includecpp': [
            'templates/*',
            'generator/*.cpp',
            'generator/*.h',
            'py.typed',
            '*.pyi',
            '*.md',
        ],
        'includecpp.core': ['*.pyi'],
        'includecpp.core.cssl': ['*.pyi', '*.md'],
        'includecpp.cli': ['*.pyi'],
        'includecpp.vscode.cssl': [
            '*.json',
            'syntaxes/*.json',
            'snippets/*.json',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="c++ python bindings pybind11 template performance native threading",
    project_urls={
        "Bug Reports": "https://github.com/liliassg/IncludeCPP/issues",
    },
)

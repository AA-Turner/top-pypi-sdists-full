import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Add the current directory to the Python path so we can import compile_kaitai_parsers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_kaitai_parsers


POLYFILE_DIR: Path = Path(__file__).absolute().parent
README_PATH: Path = POLYFILE_DIR / "README.md"

compile_kaitai_parsers.rebuild()

with open(README_PATH, "r", encoding="utf8") as readme:
    README = readme.read()

setup(
    name='polyfile-weave',
    description='A utility to recursively map the structure of a file.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/zbirenbaum/polyfile-weave',
    author='Trail of Bits',
    version="0.5.9",
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.8',
    install_requires=[
        "abnf~=2.2.0",
        "chardet>=5.0.0",
        "cint>=1.0.0",
        "fickling>=0.0.8",
        # Python 3.9: filelock 3.20.3+ requires Python>=3.10, so we use 3.19.1
        # KNOWN VULNERABILITIES IN 3.19.1:
        # - CVE-2025-68146 (GHSA-w853-jp5j-5j7f): TOCTOU symlink attack - fixed in 3.20.1
        # - CVE-2026-22701 (GHSA-qmgc-5h2g-mvrw): TOCTOU in SoftFileLock - fixed in 3.20.3
        # Risk accepted for Python 3.9. Users requiring security should upgrade to Python 3.10+
        "filelock>=3.13.0,<3.20.0;python_version<'3.10'",
        "filelock>=3.20.3;python_version>='3.10'",
        "graphviz>=0.20.1",
        "intervaltree>=2.4.0",
        "jinja2>=2.1.0",
        "kaitaistruct>=0.11",
        "networkx>=2.6.3",
        "Pillow>=5.0.0",
        "pyreadline3;platform_system=='Windows'",
        "pyyaml>=3.13",
        "pdfminer.six>=20251230;python_version>='3.10'"
    ],
    extras_require={
        'demangle': ['cxxfilt'],
        "dev": ["mypy", "pytest", "flake8"]
    },
    entry_points={
        'console_scripts': [
            'polyfile = polyfile.__main__:main'
        ]
    },
    package_data={"polyfile": [
        os.path.join("templates", "*"),
        os.path.join("kaitai", "parsers", "*.py"),
        os.path.join("kaitai", "parsers", "manifest.json"),
        os.path.join("magic_defs", "*")
    ]},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ]
)

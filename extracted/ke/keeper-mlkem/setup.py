from setuptools import setup, find_packages, Extension
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from __init__.py
with open(os.path.join(this_directory, 'mlkem', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"').strip("'")
            break

setup(
    name="keeper-mlkem",
    version=version,
    author="Keeper Security",
    author_email="ops@keepersecurity.com",
    description="Fast ML-KEM (FIPS 203) implementation with C extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keeper-Security/commander-qrc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license="MIT",
    python_requires=">=3.11",
    ext_modules=[
        Extension(
            "mlkem.fastmath",
            sources=["mlkem/fastmathmodule.c"],
            extra_compile_args=["-std=c99", "-O3"],
            optional=True,  # Allow installation without C compiler (will fail at runtime if used)
        )
    ],
    package_data={
        "mlkem": ["*.c", "py.typed"],
    },
    include_package_data=True,
    keywords="cryptography, post-quantum, kyber, ml-kem, lattice-based, key-encapsulation, pqc, fips-203",
    project_urls={
        "Bug Reports": "https://github.com/Keeper-Security/commander-qrc/issues",
        "Source": "https://github.com/Keeper-Security/commander-qrc",
        "Documentation": "https://github.com/Keeper-Security/commander-qrc/blob/master/README.md",
    },
    zip_safe=False,
)


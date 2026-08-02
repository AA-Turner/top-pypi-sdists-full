import sys
from setuptools import setup, Extension
from Cython.Build import cythonize

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

is_macos   = sys.platform == "darwin"
is_windows = sys.platform == "win32"
is_linux   = not is_macos and not is_windows

sources = [
    "xpress8.pyx",
    "src/Xpress8Wrapper.c",
    "src/xencode.c",
    "src/xdecode.c",
]

if is_windows:
    optimization_flag = "/O2"
elif is_linux:
    optimization_flag = "-O2"
else:
    optimization_flag = "-O3"

extra_compile_args = [optimization_flag]
extra_link_args = []

if is_linux:
    extra_compile_args.append("-fPIC")
elif is_windows:
    # CODING_ALG=1 by default; nothing extra needed.
    pass

xpress8_module = Extension(
    "xpress8",
    sources=sources,
    include_dirs=["include"],
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
)

setup(
    name="xpress8",
    version="0.1.0",
    description="Python bindings for the Microsoft Xpress8 (ESE) compression library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Igor Cotruta",
    author_email="hugoberry314@gmail.com",
    url="https://github.com/Hugoberry/xpress8-python",
    ext_modules=cythonize([xpress8_module]),
    packages=[],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Compression",
    ],
    keywords="compression, xpress8, microsoft, ese, pbix",
    zip_safe=False,
)

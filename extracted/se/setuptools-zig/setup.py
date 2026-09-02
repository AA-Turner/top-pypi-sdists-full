
from setuptools import setup

setup(
    name='setuptools_zig',
    version="0.5.3",
    author_email='a.van.der.neut@ruamel.eu',
    description='A setuptools extension, for building cpython extensions in Zig or C with the Zig compiler',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://sourceforge.net/p/setuptools-zig/code/ref/default/',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3',
    # install_requires='setuptools>=0.80.4',
    py_modules=['setuptools_zig'],
    keywords='',
    entry_points={"distutils.setup_keywords": ['build_zig=setuptools_zig:setup_build_zig']},
)

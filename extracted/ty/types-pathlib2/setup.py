from setuptools import setup

name = "types-pathlib2"
description = "Typing stubs for pathlib2"
long_description = '''
## Typing stubs for pathlib2

This is a PEP 561 type stub package for the `pathlib2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pathlib2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pathlib2. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `b50ebafa7913cf572ed1d4a87926b49f34fd2dc0`.
'''.lstrip()

setup(name=name,
      version="2.3.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['pathlib2-python2-stubs'],
      package_data={'pathlib2-python2-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

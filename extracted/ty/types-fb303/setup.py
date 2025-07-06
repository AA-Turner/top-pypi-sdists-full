from setuptools import setup

name = "types-fb303"
description = "Typing stubs for fb303"
long_description = '''
## Typing stubs for fb303

This is a PEP 561 type stub package for the `fb303` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `fb303`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/fb303. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `b50ebafa7913cf572ed1d4a87926b49f34fd2dc0`.
'''.lstrip()

setup(name=name,
      version="1.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['fb303-python2-stubs'],
      package_data={'fb303-python2-stubs': ['FacebookService.pyi', '__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

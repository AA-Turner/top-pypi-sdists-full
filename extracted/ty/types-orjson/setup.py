from setuptools import setup

name = "types-orjson"
description = "Typing stubs for orjson"
long_description = '''
## Typing stubs for orjson

This is a PEP 561 type stub package for the `orjson` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `orjson`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/orjson. All fixes for
types and metadata should be contributed there.

*Note:* The `orjson` package includes type annotations or type stubs
since version 3.6.1. Please uninstall the `types-orjson`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="3.6.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['orjson-stubs'],
      package_data={'orjson-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)

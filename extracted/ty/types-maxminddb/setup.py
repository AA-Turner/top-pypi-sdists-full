from setuptools import setup

name = "types-maxminddb"
description = "Typing stubs for maxminddb"
long_description = '''
## Typing stubs for maxminddb

This is a PEP 561 type stub package for the `maxminddb` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `maxminddb`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/maxminddb. All fixes for
types and metadata should be contributed there.

*Note:* The `maxminddb` package includes type annotations or type stubs
since version 2.0.2. Please uninstall the `types-maxminddb`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `8ea6d6f33176d23bf29fb4213bd0c48e4013a721`.
'''.lstrip()

setup(name=name,
      version="1.5.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-ipaddress'],
      packages=['maxminddb-stubs'],
      package_data={'maxminddb-stubs': ['__init__.pyi', 'compat.pyi', 'const.pyi', 'decoder.pyi', 'errors.pyi', 'extension.pyi', 'reader.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

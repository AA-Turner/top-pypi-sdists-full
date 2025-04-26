from setuptools import setup

name = "types-geoip2"
description = "Typing stubs for geoip2"
long_description = '''
## Typing stubs for geoip2

This is a PEP 561 type stub package for the `geoip2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `geoip2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/geoip2. All fixes for
types and metadata should be contributed there.

*Note:* The `geoip2` package includes type annotations or type stubs
since version 4.0.2. Please uninstall the `types-geoip2`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `27af44fee2670fb946882616579ae465e46cae0d`.
'''.lstrip()

setup(name=name,
      version="3.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-maxminddb'],
      packages=['geoip2-stubs'],
      package_data={'geoip2-stubs': ['__init__.pyi', 'records.pyi', 'models.pyi', 'database.pyi', 'mixins.pyi', 'errors.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

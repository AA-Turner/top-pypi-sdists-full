from setuptools import setup

name = "types-itsdangerous"
description = "Typing stubs for itsdangerous"
long_description = '''
## Typing stubs for itsdangerous

This is a PEP 561 type stub package for the `itsdangerous` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `itsdangerous`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/itsdangerous. All fixes for
types and metadata should be contributed there.

*Note:* The `itsdangerous` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-itsdangerous`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a5bc1e037fa9fb541d81de92ad27fa8543c65be4`.
'''.lstrip()

setup(name=name,
      version="1.1.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['itsdangerous-stubs'],
      package_data={'itsdangerous-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

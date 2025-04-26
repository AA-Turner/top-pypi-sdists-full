from setuptools import setup

name = "types-PyJWT"
description = "Typing stubs for PyJWT"
long_description = '''
## Typing stubs for PyJWT

This is an auto-generated PEP 561 type stub package for `PyJWT` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `PyJWT`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/PyJWT. All fixes for
types and metadata should be contributed there.

*Note:* The `PyJWT` package includes type annotations or type stubs
since version 2.0.0. Please uninstall the `types-PyJWT`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `64f463172b27d7321461890dd3edf416a103ace7`.
'''.lstrip()

setup(name=name,
      version="1.7.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-cryptography'],
      packages=['jwt-stubs'],
      package_data={'jwt-stubs': ['algorithms.pyi', '__init__.pyi', 'contrib/__init__.pyi', 'contrib/algorithms/py_ecdsa.pyi', 'contrib/algorithms/pycrypto.pyi', 'contrib/algorithms/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

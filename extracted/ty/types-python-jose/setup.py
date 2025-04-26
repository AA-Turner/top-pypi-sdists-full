from setuptools import setup

name = "types-python-jose"
description = "Typing stubs for python-jose"
long_description = '''
## Typing stubs for python-jose

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-jose`](https://github.com/mpdavis/python-jose) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `python-jose`. This version of
`types-python-jose` aims to provide accurate annotations for
`python-jose==3.4.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/python-jose`](https://github.com/python/typeshed/tree/main/stubs/python-jose)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`c27e41c33b47edc624ca456e673c7d29a46c7e5c`](https://github.com/python/typeshed/commit/c27e41c33b47edc624ca456e673c7d29a46c7e5c).
'''.lstrip()

setup(name=name,
      version="3.4.0.20250224",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-jose.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pyasn1'],
      packages=['jose-stubs'],
      package_data={'jose-stubs': ['__init__.pyi', 'backends/__init__.pyi', 'backends/_asn1.pyi', 'backends/base.pyi', 'backends/cryptography_backend.pyi', 'backends/ecdsa_backend.pyi', 'backends/native.pyi', 'backends/rsa_backend.pyi', 'constants.pyi', 'exceptions.pyi', 'jwe.pyi', 'jwk.pyi', 'jws.pyi', 'jwt.pyi', 'utils.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

from setuptools import setup

name = "types-pyOpenSSL"
description = "Typing stubs for pyOpenSSL"
long_description = '''
## Typing stubs for pyOpenSSL

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pyOpenSSL`](https://github.com/pyca/pyopenssl) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyOpenSSL`.

This version of `types-pyOpenSSL` aims to provide accurate annotations
for `pyOpenSSL==24.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyOpenSSL. All fixes for
types and metadata should be contributed there.

*Note:* The `pyOpenSSL` package includes type annotations or type stubs
since version 24.2.1. Please uninstall the `types-pyOpenSSL`
package if you use this or a newer version.


This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`964d1d73ae46b310c58de363ed687d15b9792793`](https://github.com/python/typeshed/commit/964d1d73ae46b310c58de363ed687d15b9792793) and was tested
with mypy 1.10.1, pyright 1.1.372, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="24.1.0.20240722",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyOpenSSL.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-cffi', 'cryptography>=35.0.0'],
      packages=['OpenSSL-stubs'],
      package_data={'OpenSSL-stubs': ['SSL.pyi', '__init__.pyi', 'crypto.pyi', 'rand.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

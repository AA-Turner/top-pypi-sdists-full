from setuptools import setup

name = "types-unidiff"
description = "Typing stubs for unidiff"
long_description = '''
## Typing stubs for unidiff

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`unidiff`](https://github.com/matiasb/python-unidiff) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`unidiff`.

This version of `types-unidiff` aims to provide accurate annotations
for `unidiff==0.7.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/unidiff. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `9c8c9c769cf05d66cc2240d43f2691c84e274fb6` and was tested
with mypy 1.10.0, pyright 1.1.361, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="0.7.0.20240505",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/unidiff.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['unidiff-stubs'],
      package_data={'unidiff-stubs': ['__init__.pyi', '__version__.pyi', 'constants.pyi', 'errors.pyi', 'patch.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

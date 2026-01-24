from setuptools import setup

name = "types-objgraph"
description = "Typing stubs for objgraph"
long_description = '''
## Typing stubs for objgraph

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`objgraph`](https://github.com/mgedmin/objgraph) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`objgraph`.

This version of `types-objgraph` aims to provide accurate annotations
for `objgraph==3.6.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/objgraph. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`e8e9291c76f50c3bcde79e7bb61060f5c24c054e`](https://github.com/python/typeshed/commit/e8e9291c76f50c3bcde79e7bb61060f5c24c054e) and was tested
with mypy 1.11.1, pyright 1.1.379, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="3.6.0.20240907",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/objgraph.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['objgraph-stubs'],
      package_data={'objgraph-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

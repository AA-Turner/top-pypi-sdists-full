from setuptools import setup

name = "types-defusedxml"
description = "Typing stubs for defusedxml"
long_description = '''
## Typing stubs for defusedxml

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`defusedxml`](https://github.com/tiran/defusedxml) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`defusedxml`.

This version of `types-defusedxml` aims to provide accurate annotations
for `defusedxml==0.7.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/defusedxml. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `e961db9492aee8afc998ed9e95e055503d96dcfe` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2024.2.13.
'''.lstrip()

setup(name=name,
      version="0.7.0.20240218",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/defusedxml.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['defusedxml-stubs'],
      package_data={'defusedxml-stubs': ['ElementTree.pyi', '__init__.pyi', 'cElementTree.pyi', 'common.pyi', 'expatbuilder.pyi', 'expatreader.pyi', 'lxml.pyi', 'minidom.pyi', 'pulldom.pyi', 'sax.pyi', 'xmlrpc.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

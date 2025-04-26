from setuptools import setup

name = "types-html5lib"
description = "Typing stubs for html5lib"
long_description = '''
## Typing stubs for html5lib

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`html5lib`](https://github.com/html5lib/html5lib-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`html5lib`.

This version of `types-html5lib` aims to provide accurate annotations
for `html5lib==1.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/html5lib. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`559ae9730ba3dab1305cdbaf2c29786ff38d740d`](https://github.com/python/typeshed/commit/559ae9730ba3dab1305cdbaf2c29786ff38d740d) and was tested
with mypy 1.11.2, pyright 1.1.385, and
pytype 2024.10.11.
'''.lstrip()

setup(name=name,
      version="1.1.11.20241018",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/html5lib.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['html5lib-stubs'],
      package_data={'html5lib-stubs': ['__init__.pyi', '_ihatexml.pyi', '_inputstream.pyi', '_tokenizer.pyi', '_trie/__init__.pyi', '_trie/_base.pyi', '_trie/py.pyi', '_utils.pyi', 'constants.pyi', 'filters/__init__.pyi', 'filters/alphabeticalattributes.pyi', 'filters/base.pyi', 'filters/inject_meta_charset.pyi', 'filters/lint.pyi', 'filters/optionaltags.pyi', 'filters/sanitizer.pyi', 'filters/whitespace.pyi', 'html5parser.pyi', 'serializer.pyi', 'treeadapters/__init__.pyi', 'treeadapters/genshi.pyi', 'treeadapters/sax.pyi', 'treebuilders/__init__.pyi', 'treebuilders/base.pyi', 'treebuilders/dom.pyi', 'treebuilders/etree.pyi', 'treebuilders/etree_lxml.pyi', 'treewalkers/__init__.pyi', 'treewalkers/base.pyi', 'treewalkers/dom.pyi', 'treewalkers/etree.pyi', 'treewalkers/etree_lxml.pyi', 'treewalkers/genshi.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

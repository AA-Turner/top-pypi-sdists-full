from setuptools import setup

name = "types-python-slugify"
description = "Typing stubs for python-slugify"
long_description = '''
## Typing stubs for python-slugify

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`python-slugify`](https://github.com/un33k/python-slugify) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`python-slugify`.

This version of `types-python-slugify` aims to provide accurate annotations
for `python-slugify==8.0.2`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-slugify. All fixes for
types and metadata should be contributed there.

*Note:* The `python-slugify` package includes type annotations or type stubs
since version 8.0.2. Please uninstall the `types-python-slugify`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `f94bbfbcc4c3b2b289425ea793beda0822e702f8` and was tested
with mypy 1.9.0, pyright 1.1.350, and
pytype 2024.2.27.
'''.lstrip()

setup(name=name,
      version="8.0.2.20240310",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-slugify.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['slugify-stubs'],
      package_data={'slugify-stubs': ['__init__.pyi', '__version__.pyi', 'slugify.pyi', 'special.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

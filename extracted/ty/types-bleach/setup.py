from setuptools import setup

name = "types-bleach"
description = "Typing stubs for bleach"
long_description = '''
## Typing stubs for bleach

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`bleach`](https://github.com/mozilla/bleach) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `bleach`. This version of
`types-bleach` aims to provide accurate annotations for
`bleach==6.2.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/bleach`](https://github.com/python/typeshed/tree/main/stubs/bleach)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`055857c318543f557bf2a6cbc08e26c25a81140b`](https://github.com/python/typeshed/commit/055857c318543f557bf2a6cbc08e26c25a81140b).
'''.lstrip()

setup(name=name,
      version="6.2.0.20241123",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/bleach.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-html5lib'],
      packages=['bleach-stubs'],
      package_data={'bleach-stubs': ['__init__.pyi', 'callbacks.pyi', 'css_sanitizer.pyi', 'html5lib_shim.pyi', 'linkifier.pyi', 'parse_shim.pyi', 'sanitizer.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

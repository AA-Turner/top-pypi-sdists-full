from setuptools import setup

name = "types-appdirs"
description = "Typing stubs for appdirs"
long_description = '''
## Typing stubs for appdirs

This is a PEP 561 type stub package for the `appdirs` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`appdirs`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/appdirs. All fixes for
types and metadata should be contributed there.

The `appdirs` package has been deprecated in favour of the `platformdirs` package, which ships with a `py.typed` file. Users should migrate their `appdirs` code to use `platformdirs` instead, which will remove the need for the `types-appdirs` package.

*Note:* `types-appdirs` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `7e0b9b44dea0b170081cafd596c2804089dc2125`.
'''.lstrip()

setup(name=name,
      version="1.4.3.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/appdirs.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['appdirs-stubs'],
      package_data={'appdirs-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

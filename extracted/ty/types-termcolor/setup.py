from setuptools import setup

name = "types-termcolor"
description = "Typing stubs for termcolor"
long_description = '''
## Typing stubs for termcolor

This is a PEP 561 type stub package for the `termcolor` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`termcolor`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/termcolor. All fixes for
types and metadata should be contributed there.

*Note:* The `termcolor` package includes type annotations or type stubs
since version 2.0.0. Please uninstall the `types-termcolor`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `72456da2a3546044508828dc9075fa25cbdb3645`.
'''.lstrip()

setup(name=name,
      version="1.1.6.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/termcolor.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['termcolor-stubs'],
      package_data={'termcolor-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

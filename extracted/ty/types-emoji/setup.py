from setuptools import setup

name = "types-emoji"
description = "Typing stubs for emoji"
long_description = '''
## Typing stubs for emoji

This is a PEP 561 type stub package for the `emoji` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`emoji`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/emoji. All fixes for
types and metadata should be contributed there.

*Note:* The `emoji` package includes type annotations or type stubs
since version 2.2.0. Please uninstall the `types-emoji`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6fd7e36e80e0448d9199d62d582c659c147be149`.
'''.lstrip()

setup(name=name,
      version="2.1.0.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/emoji.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['emoji-stubs'],
      package_data={'emoji-stubs': ['__init__.pyi', 'core.pyi', 'unicode_codes/__init__.pyi', 'unicode_codes/data_dict.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

from setuptools import setup

name = "types-certifi"
description = "Typing stubs for certifi"
long_description = '''
## Typing stubs for certifi

This is a PEP 561 type stub package for the `certifi` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `certifi`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/certifi. All fixes for
types and metadata should be contributed there.

*Note:* The `certifi` package includes type annotations or type stubs
since version 2022.5.18.1. Please uninstall the `types-certifi`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `95128e61ec82c2ca8ec32d6c03bd9dad9ab68e65`.
'''.lstrip()

setup(name=name,
      version="2021.10.8.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/certifi.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['certifi-stubs'],
      package_data={'certifi-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

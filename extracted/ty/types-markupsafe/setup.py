from setuptools import setup

name = "types-MarkupSafe"
description = "Typing stubs for MarkupSafe"
long_description = '''
## Typing stubs for MarkupSafe

This is a PEP 561 type stub package for the `MarkupSafe` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `MarkupSafe`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/MarkupSafe. All fixes for
types and metadata should be contributed there.

*Note:* The `MarkupSafe` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-MarkupSafe`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `98af7d667fa668dec9dc640f0f2669c6e3453e86`.
'''.lstrip()

setup(name=name,
      version="1.1.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['markupsafe-stubs'],
      package_data={'markupsafe-stubs': ['__init__.pyi', '_compat.pyi', '_constants.pyi', '_native.pyi', '_speedups.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

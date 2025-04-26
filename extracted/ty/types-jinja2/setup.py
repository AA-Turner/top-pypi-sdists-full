from setuptools import setup

name = "types-Jinja2"
description = "Typing stubs for Jinja2"
long_description = '''
## Typing stubs for Jinja2

This is a PEP 561 type stub package for the `Jinja2` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Jinja2`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Jinja2. All fixes for
types and metadata should be contributed there.

*Note:* The `Jinja2` package includes type annotations or type stubs
since version 3.0. Please uninstall the `types-Jinja2`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a5bc1e037fa9fb541d81de92ad27fa8543c65be4`.
'''.lstrip()

setup(name=name,
      version="2.11.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-MarkupSafe'],
      packages=['jinja2-stubs'],
      package_data={'jinja2-stubs': ['__init__.pyi', '_compat.pyi', '_stringdefs.pyi', 'bccache.pyi', 'compiler.pyi', 'constants.pyi', 'debug.pyi', 'defaults.pyi', 'environment.pyi', 'exceptions.pyi', 'ext.pyi', 'filters.pyi', 'lexer.pyi', 'loaders.pyi', 'meta.pyi', 'nodes.pyi', 'optimizer.pyi', 'parser.pyi', 'runtime.pyi', 'sandbox.pyi', 'tests.pyi', 'utils.pyi', 'visitor.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

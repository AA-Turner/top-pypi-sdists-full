from setuptools import setup

name = "types-Flask"
description = "Typing stubs for Flask"
long_description = '''
## Typing stubs for Flask

This is a PEP 561 type stub package for the `Flask` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Flask`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Flask. All fixes for
types and metadata should be contributed there.

*Note:* The `Flask` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-Flask`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a5bc1e037fa9fb541d81de92ad27fa8543c65be4`.
'''.lstrip()

setup(name=name,
      version="1.1.6",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-Jinja2', 'types-Werkzeug', 'types-click'],
      packages=['flask-stubs'],
      package_data={'flask-stubs': ['__init__.pyi', 'app.pyi', 'blueprints.pyi', 'cli.pyi', 'config.pyi', 'ctx.pyi', 'debughelpers.pyi', 'globals.pyi', 'helpers.pyi', 'json/__init__.pyi', 'json/tag.pyi', 'logging.pyi', 'sessions.pyi', 'signals.pyi', 'templating.pyi', 'testing.pyi', 'views.pyi', 'wrappers.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

from setuptools import setup

name = "types-Werkzeug"
description = "Typing stubs for Werkzeug"
long_description = '''
## Typing stubs for Werkzeug

This is a PEP 561 type stub package for the `Werkzeug` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Werkzeug`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Werkzeug. All fixes for
types and metadata should be contributed there.

*Note:* The `Werkzeug` package includes type annotations or type stubs
since version 2.0. Please uninstall the `types-Werkzeug`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `a5bc1e037fa9fb541d81de92ad27fa8543c65be4`.
'''.lstrip()

setup(name=name,
      version="1.0.9",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['werkzeug-stubs'],
      package_data={'werkzeug-stubs': ['__init__.pyi', '_compat.pyi', '_internal.pyi', '_reloader.pyi', 'contrib/__init__.pyi', 'contrib/atom.pyi', 'contrib/cache.pyi', 'contrib/fixers.pyi', 'contrib/iterio.pyi', 'contrib/jsrouting.pyi', 'contrib/limiter.pyi', 'contrib/lint.pyi', 'contrib/profiler.pyi', 'contrib/securecookie.pyi', 'contrib/sessions.pyi', 'contrib/testtools.pyi', 'contrib/wrappers.pyi', 'datastructures.pyi', 'debug/__init__.pyi', 'debug/console.pyi', 'debug/repr.pyi', 'debug/tbtools.pyi', 'exceptions.pyi', 'filesystem.pyi', 'formparser.pyi', 'http.pyi', 'local.pyi', 'middleware/__init__.pyi', 'middleware/dispatcher.pyi', 'middleware/http_proxy.pyi', 'middleware/lint.pyi', 'middleware/profiler.pyi', 'middleware/proxy_fix.pyi', 'middleware/shared_data.pyi', 'posixemulation.pyi', 'routing.pyi', 'script.pyi', 'security.pyi', 'serving.pyi', 'test.pyi', 'testapp.pyi', 'urls.pyi', 'useragents.pyi', 'utils.pyi', 'wrappers.pyi', 'wsgi.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

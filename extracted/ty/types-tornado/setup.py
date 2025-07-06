from setuptools import setup

name = "types-tornado"
description = "Typing stubs for tornado"
long_description = '''
## Typing stubs for tornado

This is a PEP 561 type stub package for the `tornado` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `tornado`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/tornado. All fixes for
types and metadata should be contributed there.

*Note:* The `tornado` package includes type annotations or type stubs
since version 6.0. Please uninstall the `types-tornado`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `b50ebafa7913cf572ed1d4a87926b49f34fd2dc0`.
'''.lstrip()

setup(name=name,
      version="5.1.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['tornado-python2-stubs'],
      package_data={'tornado-python2-stubs': ['util.pyi', 'testing.pyi', 'httpclient.pyi', 'locks.pyi', '__init__.pyi', 'ioloop.pyi', 'tcpserver.pyi', 'web.pyi', 'netutil.pyi', 'process.pyi', 'gen.pyi', 'concurrent.pyi', 'httputil.pyi', 'httpserver.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)

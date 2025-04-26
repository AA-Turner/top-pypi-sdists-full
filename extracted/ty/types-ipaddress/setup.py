from setuptools import setup

name = "types-ipaddress"
description = "Typing stubs for ipaddress"
long_description = '''
## Typing stubs for ipaddress

This is a PEP 561 type stub package for the `ipaddress` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `ipaddress`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/ipaddress. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `45a2dad83cc372cd066a91fc04ab44297b714e69`.
'''.lstrip()

setup(name=name,
      version="1.0.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/ipaddress.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['ipaddress-python2-stubs'],
      package_data={'ipaddress-python2-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)

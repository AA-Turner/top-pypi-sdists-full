from setuptools import setup

name = "types-google-cloud-ndb"
description = "Typing stubs for google-cloud-ndb"
long_description = '''
## Typing stubs for google-cloud-ndb

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`google-cloud-ndb`](https://github.com/googleapis/python-ndb) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `google-cloud-ndb`. This version of
`types-google-cloud-ndb` aims to provide accurate annotations for
`google-cloud-ndb==2.3.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/google-cloud-ndb`](https://github.com/python/typeshed/tree/main/stubs/google-cloud-ndb)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.396,
and pytype 2024.10.11.
It was generated from typeshed commit
[`da50b5c4112bc44dce08685f9e30708b8cb88489`](https://github.com/python/typeshed/commit/da50b5c4112bc44dce08685f9e30708b8cb88489).
'''.lstrip()

setup(name=name,
      version="2.3.0.20250317",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/google-cloud-ndb.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['google-stubs'],
      package_data={'google-stubs': ['cloud/ndb/__init__.pyi', 'cloud/ndb/_batch.pyi', 'cloud/ndb/_cache.pyi', 'cloud/ndb/_datastore_api.pyi', 'cloud/ndb/_datastore_query.pyi', 'cloud/ndb/_eventloop.pyi', 'cloud/ndb/_options.pyi', 'cloud/ndb/_transaction.pyi', 'cloud/ndb/blobstore.pyi', 'cloud/ndb/client.pyi', 'cloud/ndb/context.pyi', 'cloud/ndb/django_middleware.pyi', 'cloud/ndb/exceptions.pyi', 'cloud/ndb/global_cache.pyi', 'cloud/ndb/key.pyi', 'cloud/ndb/metadata.pyi', 'cloud/ndb/model.pyi', 'cloud/ndb/msgprop.pyi', 'cloud/ndb/polymodel.pyi', 'cloud/ndb/query.pyi', 'cloud/ndb/stats.pyi', 'cloud/ndb/tasklets.pyi', 'cloud/ndb/utils.pyi', 'cloud/ndb/version.pyi', 'METADATA.toml', 'cloud/ndb/py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

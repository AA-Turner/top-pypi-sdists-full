from setuptools import setup

name = "types-ldap3"
description = "Typing stubs for ldap3"
long_description = '''
## Typing stubs for ldap3

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`ldap3`](https://github.com/cannatag/ldap3) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`ldap3`.

This version of `types-ldap3` aims to provide accurate annotations
for `ldap3==2.9.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/ldap3. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `a2a6aee89213d87ed6f86cf723a7fc4ed3c219a2` and was tested
with mypy 1.8.0, pyright 1.1.342, and
pytype 2024.1.24.
'''.lstrip()

setup(name=name,
      version="2.9.13.20240205",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/ldap3.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pyasn1'],
      packages=['ldap3-stubs'],
      package_data={'ldap3-stubs': ['__init__.pyi', 'abstract/__init__.pyi', 'abstract/attrDef.pyi', 'abstract/attribute.pyi', 'abstract/cursor.pyi', 'abstract/entry.pyi', 'abstract/objectDef.pyi', 'core/__init__.pyi', 'core/connection.pyi', 'core/exceptions.pyi', 'core/pooling.pyi', 'core/rdns.pyi', 'core/results.pyi', 'core/server.pyi', 'core/timezone.pyi', 'core/tls.pyi', 'core/usage.pyi', 'extend/__init__.pyi', 'extend/microsoft/__init__.pyi', 'extend/microsoft/addMembersToGroups.pyi', 'extend/microsoft/dirSync.pyi', 'extend/microsoft/modifyPassword.pyi', 'extend/microsoft/persistentSearch.pyi', 'extend/microsoft/removeMembersFromGroups.pyi', 'extend/microsoft/unlockAccount.pyi', 'extend/novell/__init__.pyi', 'extend/novell/addMembersToGroups.pyi', 'extend/novell/checkGroupsMemberships.pyi', 'extend/novell/endTransaction.pyi', 'extend/novell/getBindDn.pyi', 'extend/novell/listReplicas.pyi', 'extend/novell/nmasGetUniversalPassword.pyi', 'extend/novell/nmasSetUniversalPassword.pyi', 'extend/novell/partition_entry_count.pyi', 'extend/novell/removeMembersFromGroups.pyi', 'extend/novell/replicaInfo.pyi', 'extend/novell/startTransaction.pyi', 'extend/operation.pyi', 'extend/standard/PagedSearch.pyi', 'extend/standard/PersistentSearch.pyi', 'extend/standard/__init__.pyi', 'extend/standard/modifyPassword.pyi', 'extend/standard/whoAmI.pyi', 'operation/__init__.pyi', 'operation/abandon.pyi', 'operation/add.pyi', 'operation/bind.pyi', 'operation/compare.pyi', 'operation/delete.pyi', 'operation/extended.pyi', 'operation/modify.pyi', 'operation/modifyDn.pyi', 'operation/search.pyi', 'operation/unbind.pyi', 'protocol/__init__.pyi', 'protocol/controls.pyi', 'protocol/convert.pyi', 'protocol/formatters/__init__.pyi', 'protocol/formatters/formatters.pyi', 'protocol/formatters/standard.pyi', 'protocol/formatters/validators.pyi', 'protocol/microsoft.pyi', 'protocol/novell.pyi', 'protocol/oid.pyi', 'protocol/persistentSearch.pyi', 'protocol/rfc2696.pyi', 'protocol/rfc2849.pyi', 'protocol/rfc3062.pyi', 'protocol/rfc4511.pyi', 'protocol/rfc4512.pyi', 'protocol/rfc4527.pyi', 'protocol/sasl/__init__.pyi', 'protocol/sasl/digestMd5.pyi', 'protocol/sasl/external.pyi', 'protocol/sasl/kerberos.pyi', 'protocol/sasl/plain.pyi', 'protocol/sasl/sasl.pyi', 'protocol/schemas/__init__.pyi', 'protocol/schemas/ad2012R2.pyi', 'protocol/schemas/ds389.pyi', 'protocol/schemas/edir888.pyi', 'protocol/schemas/edir914.pyi', 'protocol/schemas/slapd24.pyi', 'strategy/__init__.pyi', 'strategy/asyncStream.pyi', 'strategy/asynchronous.pyi', 'strategy/base.pyi', 'strategy/ldifProducer.pyi', 'strategy/mockAsync.pyi', 'strategy/mockBase.pyi', 'strategy/mockSync.pyi', 'strategy/restartable.pyi', 'strategy/reusable.pyi', 'strategy/safeRestartable.pyi', 'strategy/safeSync.pyi', 'strategy/sync.pyi', 'utils/__init__.pyi', 'utils/asn1.pyi', 'utils/ciDict.pyi', 'utils/config.pyi', 'utils/conv.pyi', 'utils/dn.pyi', 'utils/hashed.pyi', 'utils/log.pyi', 'utils/ntlm.pyi', 'utils/port_validators.pyi', 'utils/repr.pyi', 'utils/tls_backport.pyi', 'utils/uri.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

from setuptools import setup

name = "types-paramiko"
description = "Typing stubs for paramiko"
long_description = '''
## Typing stubs for paramiko

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`paramiko`](https://github.com/paramiko/paramiko) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`paramiko`.

This version of `types-paramiko` aims to provide accurate annotations
for `paramiko==3.5.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/paramiko. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`119cd09655dcb4ed7fb2021654ba809b8d88846f`](https://github.com/python/typeshed/commit/119cd09655dcb4ed7fb2021654ba809b8d88846f) and was tested
with mypy 1.11.1, pyright 1.1.382.post1, and
pytype 2024.9.13.
'''.lstrip()

setup(name=name,
      version="3.5.0.20240928",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/paramiko.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['cryptography>=37.0.0'],
      packages=['paramiko-stubs'],
      package_data={'paramiko-stubs': ['__init__.pyi', '_version.pyi', '_winapi.pyi', 'agent.pyi', 'auth_handler.pyi', 'auth_strategy.pyi', 'ber.pyi', 'buffered_pipe.pyi', 'channel.pyi', 'client.pyi', 'common.pyi', 'compress.pyi', 'config.pyi', 'dsskey.pyi', 'ecdsakey.pyi', 'ed25519key.pyi', 'file.pyi', 'hostkeys.pyi', 'kex_curve25519.pyi', 'kex_ecdh_nist.pyi', 'kex_gex.pyi', 'kex_group1.pyi', 'kex_group14.pyi', 'kex_group16.pyi', 'kex_gss.pyi', 'message.pyi', 'packet.pyi', 'pipe.pyi', 'pkey.pyi', 'primes.pyi', 'proxy.pyi', 'rsakey.pyi', 'server.pyi', 'sftp.pyi', 'sftp_attr.pyi', 'sftp_client.pyi', 'sftp_file.pyi', 'sftp_handle.pyi', 'sftp_server.pyi', 'sftp_si.pyi', 'ssh_exception.pyi', 'ssh_gss.pyi', 'transport.pyi', 'util.pyi', 'win_openssh.pyi', 'win_pageant.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

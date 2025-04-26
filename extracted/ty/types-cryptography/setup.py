from setuptools import setup

name = "types-cryptography"
description = "Typing stubs for cryptography"
long_description = '''
## Typing stubs for cryptography

This is a PEP 561 type stub package for the `cryptography` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `cryptography`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/cryptography. All fixes for
types and metadata should be contributed there.

*Note:* The `cryptography` package includes type annotations or type stubs
since version 3.4.4. Please uninstall the `types-cryptography`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `c0e9038f0d71a38efc672ac5ef11aae0292c0a96`.
'''.lstrip()

setup(name=name,
      version="3.3.23.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/cryptography.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['cryptography-stubs'],
      package_data={'cryptography-stubs': ['__init__.pyi', 'exceptions.pyi', 'fernet.pyi', 'hazmat/__init__.pyi', 'hazmat/backends/__init__.pyi', 'hazmat/backends/interfaces.pyi', 'hazmat/bindings/__init__.pyi', 'hazmat/bindings/openssl/__init__.pyi', 'hazmat/bindings/openssl/binding.pyi', 'hazmat/primitives/__init__.pyi', 'hazmat/primitives/asymmetric/__init__.pyi', 'hazmat/primitives/asymmetric/dh.pyi', 'hazmat/primitives/asymmetric/dsa.pyi', 'hazmat/primitives/asymmetric/ec.pyi', 'hazmat/primitives/asymmetric/ed25519.pyi', 'hazmat/primitives/asymmetric/ed448.pyi', 'hazmat/primitives/asymmetric/padding.pyi', 'hazmat/primitives/asymmetric/rsa.pyi', 'hazmat/primitives/asymmetric/utils.pyi', 'hazmat/primitives/asymmetric/x25519.pyi', 'hazmat/primitives/asymmetric/x448.pyi', 'hazmat/primitives/ciphers/__init__.pyi', 'hazmat/primitives/ciphers/aead.pyi', 'hazmat/primitives/ciphers/algorithms.pyi', 'hazmat/primitives/ciphers/modes.pyi', 'hazmat/primitives/cmac.pyi', 'hazmat/primitives/constant_time.pyi', 'hazmat/primitives/hashes.pyi', 'hazmat/primitives/hmac.pyi', 'hazmat/primitives/kdf/__init__.pyi', 'hazmat/primitives/kdf/concatkdf.pyi', 'hazmat/primitives/kdf/hkdf.pyi', 'hazmat/primitives/kdf/kbkdf.pyi', 'hazmat/primitives/kdf/pbkdf2.pyi', 'hazmat/primitives/kdf/scrypt.pyi', 'hazmat/primitives/kdf/x963kdf.pyi', 'hazmat/primitives/keywrap.pyi', 'hazmat/primitives/padding.pyi', 'hazmat/primitives/poly1305.pyi', 'hazmat/primitives/serialization/__init__.pyi', 'hazmat/primitives/serialization/pkcs12.pyi', 'hazmat/primitives/serialization/pkcs7.pyi', 'hazmat/primitives/twofactor/__init__.pyi', 'hazmat/primitives/twofactor/hotp.pyi', 'hazmat/primitives/twofactor/totp.pyi', 'x509/__init__.pyi', 'x509/extensions.pyi', 'x509/oid.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

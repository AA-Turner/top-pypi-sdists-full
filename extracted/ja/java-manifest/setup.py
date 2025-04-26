# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['java_manifest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'java-manifest',
    'version': '1.1.0',
    'description': "Encode/decode Java's META-INF/MANIFEST.MF in Python",
    'long_description': '# java-manifest-py\n\n[![Build Status](https://travis-ci.com/elihunter173/java-manifest-py.svg?branch=master)](https://travis-ci.com/elihunter173/java-manifest-py)\n[![PyPI version](https://badge.fury.io/py/java-manifest.svg)](https://badge.fury.io/py/java-manifest)\n\nEncode/decode Java\'s `META-INF/MANIFEST.MF` in Python.\n\n## Installation\n\nTo install the latest release on PyPI, run:\n\n```sh\n$ pip install java-manifest\n```\n\n## Usage\n\nA MANIFEST is represented by a list of dictionaries, where each dictionary\ncorresponds to an empty-line delimited section of the MANIFEST and each\ndictionary has `str` keys and either `str` or `bool` values.\n\n`java_manifest.loads` takes a string containing MANIFEST-formatted data and\nreturns a list of dictionaries, where each dictionary is a section in the\nMANIFEST. `java_manifest.load` does the same, using any `typing.TextIO`\nreadable object.\n\n```python\n>>> import java_manifest\n>>> manifest_str = """\n... Name: README-Example-1\n... Long-Line: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n...  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n...\n... Name: README-Example-2\n... Foo: Bar\n... """\n>>> manifest = java_manifest.loads(manifest_str)\n>>> print(manifest)\n[{\'Name\': \'README-Example-1\', \'Long-Line\': \'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\'}, {\'Name\': \'README-Example-2\', \'Foo\': \'Bar\'}]\n\n```\n\nSimilarly, `java_manifest.dumps` returns a string of MANIFEST-formatted data\nfrom a list of dictionaries, where each dictionary is a section in the\nMANIFEST. `java_manifest.dump` does the same, writing into any `typing.TextIO`\nwritable object.\n\n```python\n>>> import java_manifest\n>>> manifest = [\n...     {\n...         "Name": "README-Example",\n...         "Some-Str": "Some random string",\n...     },\n... ]\n>>> manifest_str = java_manifest.dumps(manifest)\n>>> print(manifest_str)\nName: README-Example\nSome-Str: Some random string\n<BLANKLINE>\n\n```\n\nThere is also a `from_jar` function that finds the `META-INF/MANIFEST.MF` file\nwithin the jar and `java_manifest.load`s that.\n\n```python\n>>> import java_manifest\n>>> manifest = java_manifest.from_jar("test_files/simple.jar")\n\n```\n\n### Custom Encoders/Decoders\n\nBecause Java\'s manifest file format doesn\'t deal with structured values within\na section, specific uses of the format create ad-hoc encoding/decoding rules\nthat can convert some structured data into a basic string so it can be encoded\ninto a manifest and vice versa. The `encoder` and `decoder` arguments for\ndumping and loading respectively are responsible for handling this. An encoder\nand decoder both take in a key-value pair. However, an encoder receives\npotentially structured data as the value and returns plain string, while a\ndecode receives string values and returns potentially structured data.\n\nAs we have already see, the default encoder and decoder does no transformation\nand prevents you from attempting to dump non-string data.\n\n```python\n>>> import java_manifest\n>>> print(java_manifest.dumps([{"foo": "bar"}]))\nfoo: bar\n\n>>> print(java_manifest.dumps([{"int": 1}]))\nTraceback (most recent call last):\n  ...\nValueError: key \'int\' has type <class \'int\'> value, expected str\n\n```\n\nYou can however describe more custom encoders that support for example lists of\nstrings.\n\n```python\n>>> def encode(key, val):\n...     if isinstance(val, list):\n...         return ",".join(val)\n...     return val\n>>> print(java_manifest.dumps([{"foo": "bar", "names": ["alice", "bob", "charlie"]}], encoder=encode))\nfoo: bar\nnames: alice,bob,charlie\n<BLANKLINE>\n\n```\n\nSimilarly for custom decoders.\n\n```python\n>>> import java_manifest\n>>> def decode(key, val):\n...     # In reality you\'d probably want to target only specific keys, to avoid\n...     # messing up random strings containing commas. This is just an example.\n...     vals = val.split(",")\n...     if len(vals) == 1:\n...         return val\n...     else:\n...         return vals\n>>> manifest = java_manifest.loads("foo: bar\\r\\nnames: alice,bob,charlie", decoder=decode)\n>>> print(manifest)\n[{\'foo\': \'bar\', \'names\': [\'alice\', \'bob\', \'charlie\']}]\n\n```\n',
    'author': 'Eli W. Hunter',
    'author_email': 'elihunter173@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elihunter173/java-manifest-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

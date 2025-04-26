# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypruningradixtrie', 'pypruningradixtrie.input']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypruningradixtrie',
    'version': '2.1.0',
    'description': 'Radix trie for fast prefix search.',
    'long_description': '# PyPruningRadixTrie\n![GitHub CI](https://github.com/otto-de/PyPruningRadixTrie/actions/workflows/pipeline.yml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/pypruningradixtrie.svg)](https://badge.fury.io/py/pypruningradixtrie)\n\nPython Port of [Pruning Radix Trie](https://github.com/wolfgarbe/PruningRadixTrie) by Wolf Garbe.\n\n**Changes compared to original version**\n* Removed parameter to disable pruning behavior.\n  * See `test/non_pruning_radix_trie.py` for a non-pruning version that you can use to see the speed improvement.\n* Added outline for more generic `InputProvider` and providers that read CSV or JSON as examples\n\n\n## What and Why\n\nA [**Trie**](https://en.wikipedia.org/wiki/Trie) is a tree data structure that is commonly used for searching terms\nthat start with a given prefix.  \nIt starts with an empty string at the base of the trie, the _root node_.        \nAdding a new entry to the trie creates a new branch. This branch shares already present characters with existing nodes\nand creates new nodes when it\'s prefix diverges from the present entries.\n```text\n# trie containing flower & flowchart (1 char = 1 node)\n\n\'\' - f - l - o - w - e - r\n                 |\n                 c - h - a - r - t\n```\n\nA [**RadixTrie**](https://en.wikipedia.org/wiki/Radix_tree) is the space optimized version of a Trie.   \nIt combines the nodes with only one sub-node into one, containing more than one character.\n\n```text\n# radix trie containing flower & flowchart\n\n\'\' - flow - er\n      |\n     chart\n```\n\nThe prefix **Pruning** references the algorithm to query the RadixTrie.   \nIn order for the pruning to work, the nodes in RadixTrie are stored in a sorted manner.     \nThis structure allows **cutting off unpromising branches** during querying the trie which **makes the algorithm way faster**\ncompared to a non-pruning trie.\n\n\n## Usage\n\nGet from PyPI:\n```shell\npip install pypruningradixtrie\n```\n\n**Create the PRT:**\n```python\n# empty trie\ntrie = PruningRadixTrie()\n\n# fill with data from CSV file on creation\ntrie = PruningRadixTrie(\'./test_data.csv\', CSVInputProvider(\',\', lambda x: float(x[1])))\n```\n\n**Add entries:**    \nCSV:\n```python\n# fill with data from CSV file, score is at position 1, term at position 0\nfill_trie_from_file(trie, \'./test_data.csv\', CSVInputProvider(\',\', lambda x: float(x[1]), 0))\n```\n\nJSON:\n```python\n# define a functon to calculate the score out of a JSON entry\ndef score_fun(json_entry: Dict[str, Any]) -> float:\n  return json_entry["pages"] * json_entry["year"] / 10.0\n\n# "title" = key for term to insert into PRT\nfill_trie_from_file(trie, \'./test_data.json\', JSONInputProvider("title", score_fun))\n```\n\nSingle Entry:\n```python\n# insert single entry\ninsert_term(trie, term="flower", score=20)\n```\n\n**Use the PRT:**\n```python\n# get the top 10 entries that start with \'flower\'\ntrie.get_top_k_for_prefix(\'flower\', 10)\n```\n',
    'author': 'tomglk',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/otto-de/PyPruningRadixTrie',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

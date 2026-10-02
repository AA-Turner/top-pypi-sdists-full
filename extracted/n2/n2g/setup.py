# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['n2g',
 'n2g.plugins',
 'n2g.plugins.data',
 'n2g.plugins.diagrams',
 'n2g.plugins.viewers',
 'n2g.plugins.viewers.v3d_viewer',
 'n2g.plugins.viewers.yed_viewer',
 'n2g.utils']

package_data = \
{'': ['*'],
 'n2g.plugins': ['viewers/yed_viewer/css/*',
                 'viewers/yed_viewer/css/images/*',
                 'viewers/yed_viewer/javascript/*']}

extras_require = \
{'full:python_version >= "3.6"': ['ttp>=0.9.0,<0.10.0',
                                  'ttp_templates>=0.3.0,<0.4.0',
                                  'python-igraph>=0.10.0,<0.11.0'],
 'full:python_version >= "3.7"': ['flask==2.2.2', 'openpyxl>=3.1.0,<3.2.0']}

entry_points = \
{'console_scripts': ['n2g = N2G.utils.N2G_cli:cli_tool']}

setup_kwargs = {
    'name': 'n2g',
    'version': '0.3.3',
    'description': 'Need To Graph',
    'long_description': '[![Downloads](https://pepy.tech/badge/n2g)](https://pepy.tech/project/n2g)\n[![Documentation Status](https://readthedocs.org/projects/n2g/badge/?version=latest)](https://n2g.readthedocs.io/en/latest/?badge=latest)\n\n# Need To Graph\n\nN2G is a library to generate diagrams in [yWorks](https://www.yworks.com/) graphml or [Diagrams](https://www.diagrams.net/)\ndrawio formats or produce JSON data compatible with [3d-force-graph JSON input syntax](https://github.com/vasturiano/3d-force-graph#input-json-syntax)\nallowing 3D visualization.\n\n<details><summary>Demo</summary>\n<img src="example.gif">\n</details>\n\n## Why?\n\nTo save your time on producing consistently looking, editable diagrams of arbitrary size and complexity in a programmatic way helping to satisfy your "Need To Graph" desire.\n\n## How?\n\nNot a secret that many applications use XML structured text to save their diagrams content, then why not to do the opposite - produce XML structured text that applications can open and understand and work with. N2G does exactly that, it takes structured data - csv, dictionary, list or api calls and gives back XML text that can be opened and edited by application of choice.\n\n## What?\n\nAll formats supported so far have very similar API capable of:\n\n* adding nodes and links with various attributes such as shape, labels, urls, data, styles\n* bulk graph creation using from_x methods supporting lists, dictionaries or csv data\n* existing nodes and links attributes manipulation and update\n* loading existing XML diagram files for processing and modification\n* deletion of nodes and links from diagrams\n* comparing two diagrams to highlight the difference between them\n* layout your diagram with algorithms available in [igraph](https://igraph.org/2020/02/14/igraph-0.8.0-python.html) library\n* returning results in text format or saving directly into the file\n\nReference [documentation](https://n2g.readthedocs.io/en/0.1.2/index.html) for more information.\n\n## What it\'s not?\n\nN2G is not a magic bullet that will produce perfect diagrams for you, it can help to simplify the process of adding elements to your diagrams. However, (manual) efforts required to put all the elements in positions where they will satisfy your inner sense of perfection, as a result, keep in mind that (normally) the more elements you have on your diagram, the more efforts required to make it looks good.\n\nQuite unlikely it would ever be a tool with support of all capabilities available in subject applications, however, feature requests are welcomed.\n\n## Example\n\n```python\nfrom N2G import yed_diagram\n\ndiagram = yed_diagram()\nsample_list_graph = [\n    {\'source\': {\'id\': \'SW1\', \'top_label\': \'CORE\', \'bottom_label\': \'1,1,1,1\'}, \'src_label\': \'Gig0/0\', \'target\': \'R1\', \'trgt_label\': \'Gig0/1\'},\n    {\'source\': {\'id\': \'R2\', \'top_label\': \'DC-PE\'}, \'src_label\': \'Gig0/0\', \'target\': \'SW1\', \'trgt_label\': \'Gig0/2\'},\n    {\'source\': {\'id\':\'R3\', \'bottom_label\': \'1.1.1.3\'}, \'src_label\': \'Gig0/0\', \'target\': \'SW1\', \'trgt_label\': \'Gig0/3\'},\n    {\'source\': \'SW1\', \'src_label\': \'Gig0/4\', \'target\': \'R4\', \'trgt_label\': \'Gig0/1\'},\n    {\'source\': \'SW1\', \'src_label\': \'Gig0/5\', \'target\': \'R5\', \'trgt_label\': \'Gig0/7\'},\n    {\'source\': \'SW1\', \'src_label\': \'Gig0/6\', \'target\': \'R6\', \'trgt_label\': \'Gig0/11\'}\n]\ndiagram.from_list(sample_list_graph)\ndiagram.dump_file(filename="Sample_graph.graphml", folder="./")\n```\n\n# Disclaimer\n\nAuthor of this module not affiliated with any of the application Vendors mentioned so far. The choice of formats to support was primarily driven by the fact of how much functionality available in particular application for free. Moreover, this module does not use any aforementioned (diagramming) applications in any programmatic way to produce its results, in other words, none of the aforementioned applications required to be installed on the system for this (N2G) module to work.\n\n# Contributions\nFeel free to submit an issue, to report a bug or ask a question, feature requests are welcomed or [buy](https://paypal.me/dmulyalin) Author a coffee\n',
    'author': 'Denis Mulyalin',
    'author_email': 'd.mulyalin@gmail.com',
    'maintainer': 'Denis Mulyalin',
    'maintainer_email': 'd.mulyalin@gmail.com',
    'url': 'https://github.com/dmulyalin/N2G',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_diagrams']

package_data = \
{'': ['*']}

install_requires = \
['diagrams>=0.16.0']

setup_kwargs = {
    'name': 'sphinx-diagrams',
    'version': '0.4.0',
    'description': 'Rendering Diagrams in Sphinx',
    'long_description': '# sphinx-diagrams\n\nThis is a rough (incomplete, but working) Sphinx extension for\n[Diagrams](https://github.com/mingrammer/diagrams). Please refer to the [open\nissue for Sphinx support](https://github.com/mingrammer/diagrams/issues/2) for\nthe latest up-to-date version when officially supported.\n\n## Usage\n\n### Install\n\n```bash\n$ pip3 install sphinx-diagrams\n```\n\n### Adding the extension\n\n`conf.py`\n\n```conf.py\nextensions = [\n    "sphinx_diagrams",\n]\n```\n\n### Adding the diagram (inline)\n\nThe simplest way is to use `SphinxDiagram` and inline the code in your document.\nConsider using an external diagram/python script (see below) as it has much\nshorter iteration loop than running sphinx and most likely better supported by\nyour editor or IDE.\n\n`source/index.rst`\n\n```rst\nDiagram - Deployment\n====================\n\n.. diagrams::\n  from diagrams import Cluster\n  from diagrams.k8s.compute import Deployment\n  from sphinx_diagrams import SphinxDiagram\n\n  with SphinxDiagram(title="GKE"):\n      with Cluster("GCP Project"):\n          KubernetesEngine("Primary Cluster")\n```\n\n\n### Adding a diagram (external python code)\n\n\n#### Write the code\n\n`source/diagrams_infrastructure.py`\n\nYou can still use `SphinxDiagram` in your own code. This class handles arguments\nlike `:filename:` and visibility (showing the diagram via `xdg-open/open`) for\nyou.\n\n```python\nfrom diagrams import Cluster\nfrom diagrams.k8s.compute import Deployment\nfrom sphinx_diagrams import SphinxDiagram\n\nwith SphinxDiagram(title="GKE"):\n    with Cluster("GCP Project"):\n        KubernetesEngine("Primary Cluster")\n\n```\n\nAlternatively, you can use `Diagram` (from `diagrams`) directly. Note that the\nextension will pass two arguments to your diagram script. The first one is the\n`filename` as `sys.argv[1]` it expects (it needs to match the one outputted by\n`diagrams`) and the value `false` as `sys.argv[2]`. The later can be used to\ntell your script not to show (open) the generate diagram.\n\n```python\nimport sys\n\nfrom diagrams import Diagram, Cluster\nfrom diagrams.gcp.compute import KubernetesEngine\n\nwith Diagram("GKE", filename=sys.argv[1], show=sys.argv[2].lower() == \'true\'):\n    with Cluster("GCP Project"):\n        KubernetesEngine("Primary Cluster")\n```\n\n\n#### Referencing the diagram\n\n`source/index.rst`\n\n```rst\nDiagram - Deployment\n====================\n\n.. diagrams:: diagrams_infrastructure.py\n  :filename: diagram-deployment.png\n```\n\nIf using `SphinxDiagram` (above) or if the filename of the diagram script is the\nsame as the output file (e.g.: `diagrams_infrastructure.py =>\ndiagrams_infrastructure.png`) then the `:filename:` is not necessary.\n\n```rst\nDiagram - Deployment\n====================\n\n.. diagrams:: diagrams_infrastructure.py\n```\n## Credit\n\nThis code is based on\n[sphinx.graphviz](https://github.com/buildthedocs/sphinx.graphviz/).\n\nSPDX-License-Identifier: BSD-2-Clause\n',
    'author': 'Jean-Martin Archer',
    'author_email': 'jm@jmartin.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j-martin/sphinx-diagrams',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

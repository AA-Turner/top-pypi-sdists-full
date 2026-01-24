# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['retentioneering',
 'retentioneering.backend',
 'retentioneering.backend.callback',
 'retentioneering.backend.tracker',
 'retentioneering.backend.tracker.connector',
 'retentioneering.constants',
 'retentioneering.data_processor',
 'retentioneering.data_processors_lib',
 'retentioneering.datasets',
 'retentioneering.datasets.data',
 'retentioneering.edgelist',
 'retentioneering.eventstream',
 'retentioneering.eventstream.helpers',
 'retentioneering.exceptions',
 'retentioneering.nodelist',
 'retentioneering.params_model',
 'retentioneering.preprocessing_graph',
 'retentioneering.preprocessor',
 'retentioneering.templates',
 'retentioneering.templates.preprocessing_graph',
 'retentioneering.templates.transition_graph',
 'retentioneering.tooling',
 'retentioneering.tooling._describe',
 'retentioneering.tooling._describe_events',
 'retentioneering.tooling._transition_matrix',
 'retentioneering.tooling.clusters',
 'retentioneering.tooling.cohorts',
 'retentioneering.tooling.constants',
 'retentioneering.tooling.event_timestamp_hist',
 'retentioneering.tooling.funnel',
 'retentioneering.tooling.mixins',
 'retentioneering.tooling.sequences',
 'retentioneering.tooling.stattests',
 'retentioneering.tooling.step_matrix',
 'retentioneering.tooling.step_sankey',
 'retentioneering.tooling.timedelta_hist',
 'retentioneering.tooling.transition_graph',
 'retentioneering.tooling.typing',
 'retentioneering.tooling.typing.transition_graph',
 'retentioneering.tooling.user_lifetime_hist',
 'retentioneering.utils',
 'retentioneering.widget']

package_data = \
{'': ['*']}

install_requires = \
['docrep>=0.3.2,<0.4.0',
 'ipykernel==5.5.6',
 'ipython==7.34.0',
 'ipywidgets>=8.0.4,!=8.0.5',
 'jupyterlab>=3.4.7',
 'matplotlib==3.7.2',
 'nanoid>=2.0.0,<3.0.0',
 'networkx==2.8.6',
 'notebook>=6.5.6',
 'numpy>=1.22,!=1.24',
 'pandas>=1.5.0,<2.0.0',
 'plotly>=5.10.0',
 'pydantic>=1.10.2,<2',
 'pyzmq==23.2.1',
 'scikit-learn>=1.2.0,<1.3.0',
 'seaborn>=0.12.1',
 'statsmodels>=0.14.0',
 'tornado==6.3.2',
 'umap-learn>=0.5.3',
 'virtualenv>=20.17']

extras_require = \
{':python_version < "3.9"': ['scipy==1.10.1'],
 ':python_version >= "3.9"': ['scipy>=1.11.2']}

setup_kwargs = {
    'name': 'retentioneering',
    'version': '3.3.0',
    'description': 'Retentioneering is a Python library that makes analyzing clickstreams, user paths (trajectories), and event logs much easier, and yields much broader and deeper insights than funnel analysis. You can use Retentioneering to explore user behavior, segment users, and form hypotheses about what drives users to desirable actions or to churning away from a product.',
    'long_description': '[![Rete logo](https://raw.githubusercontent.com/retentioneering/pics/master/pics/logo_long_black.png)](https://github.com/retentioneering/retentioneering-tools)\n[![Discord](https://img.shields.io/badge/server-on%20discord-blue)](https://discord.com/invite/hBnuQABEV2)\n[![Telegram](https://img.shields.io/badge/chat-on%20telegram-blue)](https://t.me/retentioneering_support)\n[![Python version](https://img.shields.io/pypi/pyversions/retentioneering)](https://pypi.org/project/retentioneering/)\n[![Pipi version](https://img.shields.io/pypi/v/retentioneering)](https://pypi.org/project/retentioneering/)\n[![Downloads](https://pepy.tech/badge/retentioneering)](https://pepy.tech/project/retentioneering)\n[![Downloads](https://static.pepy.tech/badge/retentioneering/month)](https://pepy.tech/project/retentioneering)\n\n## What is Retentioneering?\n\nRetentioneering is a Python library that makes analyzing clickstreams, user paths (trajectories), and event logs much easier, and yields much broader and deeper insights than funnel analysis.\n\nYou can use Retentioneering to explore user behavior, segment users, and form hypotheses about what drives users to desirable actions or to churning away from a product.\n\nRetentioneering uses clickstream data to build behavioral segments, highlighting the events and patterns in user behavior that impact your conversion rates, retention, and revenue. The Retentioneering library is created for data analysts, marketing analysts, product owners, managers, and anyone else whose job is to improve a product’s quality.\n\n[![A simplified scenario of user behavior exploration with Retentioneering.](https://raw.githubusercontent.com/retentioneering/pics/master/pics/rete20/intro_0.png)](https://github.com/retentioneering/retentioneering-tools)\n\n\nAs a natural part of the [Jupyter](https://jupyter.org/) environment, Retentioneering extends the abilities of [pandas](https://pandas.pydata.org), [NetworkX](https://networkx.org/), [scikit-learn](https://scikit-learn.org) libraries to process sequential events data more efficiently. Retentioneering tools are interactive and tailored for analytical research, so you do not have to be a Python expert to use it. With just a few lines of code, you can wrangle data, explore customer journey maps, and make visualizations.\n\n### Retentioneering structure\n\nRetentioneering consists of two major parts: [the preprocessing module](https://doc.retentioneering.com/stable/doc/getting_started/quick_start.html#quick-start-preprocessing) and [the path analysis tools](https://doc.retentioneering.com/stable/doc/getting_started/quick_start.html#quick-start-rete-tools).\n\nThe **preprocessing module** provides a wide range of hands-on methods specifically designed for processing clickstream data, which can be called either using code, or via the preprocessing GUI. With separate methods for grouping or filtering events, splitting a clickstream into sessions, and much more, the Retentioneering preprocessing module enables you to dramatically reduce the amount of code, and therefore potential errors. Plus, if you’re dealing with a branchy analysis, which often happens, the preprocessing methods will help you make the calculations structured and reproducible, and organize them as a calculation graph. This is especially helpful for working with a team.\n\nThe **path analysis tools** bring behavior-driven segmentation of users to product analysis by providing a powerful set of techniques for performing in-depth analysis of customer journey maps. The tools feature informative and interactive visualizations that make it possible to quickly understand in very high resolution the complex structure of a clickstream.\n\n## Documentation\n\nComplete documentation is available [here](https://doc.retentioneering.com/stable/doc/index.html).\n\n## Installation\n\nRetentioneering can be installed via pip using [PyPI](https://pypi.org/project/retentioneering/).\n\n```bash\npip install retentioneering\n```\n\nOr directly from Jupyter notebook or [google.colab](https://colab.research.google.com/).\n\n```bash\n!pip install retentioneering\n```\n\n## Quick start\n\nWe recommend starting your Retentioneering journey with the [Quick Start document](https://doc.retentioneering.com/stable/doc/getting_started/quick_start.html).\n\n\n## Step-by-step guides\n\n- [Eventstream](https://doc.retentioneering.com/stable/doc/user_guides/eventstream.html)\n\n### Preprocessing\n\n- [Data processors](https://doc.retentioneering.com/stable/doc/user_guides/dataprocessors.html)\n- [Preprocessing graph](https://doc.retentioneering.com/stable/doc/user_guides/preprocessing.html)\n- [Preprocessing tutorial](https://colab.research.google.com/drive/1WwVI5oQF81xp9DJ6rP5HyM_UjuNPjUk0?usp=sharing)\n\n### Path analysis tools\n\n- [Transition graph](https://doc.retentioneering.com/stable/doc/user_guides/transition_graph.html)\n- [Step matrix](https://doc.retentioneering.com/stable/doc/user_guides/step_matrix.html)\n- [Step Sankey](https://doc.retentioneering.com/stable/doc/user_guides/step_sankey.html)\n- [Clusters](https://doc.retentioneering.com/stable/doc/user_guides/clusters.html)\n- [Funnel](https://doc.retentioneering.com/stable/doc/user_guides/funnel.html)\n- [Cohorts](https://doc.retentioneering.com/stable/doc/user_guides/cohorts.html)\n- [Stattests](https://doc.retentioneering.com/stable/doc/user_guides/stattests.html)\n\n## Raw data type\nRaw data can be downloaded from Google Analytics BigQuery stream, or any other such streams. Just convert that data to the list of triples - user_id, event, and timestamp - and pass it to Retentioneering tools. The package also includes some datasets for a quick start.\n\n## Changelog\n\n- [Version 3.3.0](https://doc.retentioneering.com/stable/doc/whatsnew/v3.3.0.html)\n- [Version 3.2.1](https://doc.retentioneering.com/stable/doc/whatsnew/v3.2.1.html)\n- [Version 3.2](https://doc.retentioneering.com/stable/doc/whatsnew/v3.2.0.html)\n- [Version 3.1](https://doc.retentioneering.com/stable/doc/whatsnew/v3.1.0.html)\n- [Version 3.0](https://doc.retentioneering.com/3.0/doc/whatsnew/v3.0.0.html)\n- [Version 2.0 (archive)](https://github.com/retentioneering/retentioneering-tools-2-archive)\n\n## Contributing\n\nThis is community-driven open source project in active development. Any contributions,\nnew ideas, bug reports, bug fixes, documentation improvements are very welcome.\n\nRetentioneering now provides several opensource solutions for data-driven product\nanalytics and web analytics. Please checkout [this repository](https://github.com/retentioneering/retentioneering-dom-observer) for JS library to track the mutations of the website elements.\n\nApps are better with math! :)\nRetentioneering is a research laboratory, analytics methodology and opensource\ntools founded by [Maxim Godzi](https://www.linkedin.com/in/godsie/) in 2015.\nPlease feel free to contact us at retentioneering@gmail.com if you have any\nquestions regarding this repo.\n',
    'author': 'Retentioneering User Trajectory Analysis Lab',
    'author_email': 'retentioneering@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

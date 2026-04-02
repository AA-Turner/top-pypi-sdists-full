# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ratio',
 'ratio.application',
 'ratio.authentication',
 'ratio.database',
 'ratio.database.fields',
 'ratio.database.migrations',
 'ratio.database.models',
 'ratio.database.seeders',
 'ratio.http',
 'ratio.router',
 'ratio.router.resolvers',
 'ratio.util']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'ratio',
    'version': '0.4.0',
    'description': 'The Python Web Framework for developers who like to get shit done',
    'long_description': '<h1 align="center">Ratio</h1>\n<p align="center">\n  The Python web framework for developers who want to get shit done.\n</p>\n\n---\n\n**Ratio is currently being developed and all releases in this phase may introduce breaking changes until further notice.\nPlease do not use Ratio in production without carefully considering the consequences.**\n\n---\n\n## What is Ratio?\nRatio is an asynchronous Python web framework that was built with developer experience in mind. Quick to learn for those\nwho just start out with programming and powerful so that senior developers can build high performance web applications \nwith it. The framework is designed with the Goldilocks principle in mind: just enough. Enough power to run high performance\nweb applications, enough intuitive design, so that developers can easily pick up on the principles.\n\nRatio borrows ideas from great frameworks, like [Django](https://github.com/django/django), [FastAPI](https://github.com/tiangolo/fastapi)\nand [Next.js](https://github.com/vercel/next.js). It combines those ideas with original concepts to improve the life of \na developer when building web applications for any purpose.\n\n## Ready out of the box \nRatio will be shipped with a custom and extensible command line interface, which can be used to perform actions within a\nproject.\n  \nThis is what we aim Ratio to do:\n\n- **File based routing:** Intuitive routing for each incoming request, based on file system.\n- **Integrates with databases:** Connect to SQL or SQLite databases from within the application controllers.\n- **Write once, use everywhere:** Do not repeat yourself, by defining models, routes and actions you can use them throughout the application.\n- **Adheres to standards:** API views are based on [OpenAPI]() and the [JSON schema standard]().\n\n_This list is not complete and will be extended after certain releases in the pre-release phase._\n\n\n## Minimal external dependencies\nCurrently, Ratio only requires the `rich` package from outside the Python standard library, which is used \nfor rendering beautiful output to the command line. In a future version of Ratio, we might want to remove this direct\ndependency for users who really want to have no external dependencies.\n',
    'author': 'Job Veldhuis',
    'author_email': 'job@baukefrederik.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

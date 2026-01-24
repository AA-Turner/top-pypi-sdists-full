# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luzmo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'luzmo-sdk',
    'version': '1.0.0',
    'description': 'Luzmo Python SDK for the Core API',
    'long_description': '#Luzmo-Python-SDK\n\n### Python Package\n\nYou will need `Python Version >= 3.6`\n\n```console\npip install luzmo-sdk\n```\n\n### Documentation\n\nFor detailed documentation, please visit the [Luzmo Developer Docs](https://developer.luzmo.com/)\n\n### Usage and Examples\n\nCreate a Luzmo dataset:\n\n```console\nfrom luzmo.luzmo import Luzmo\n\nkey = "Your Luzmo key"\ntoken = "Your Luzmo token"\n\nclient = Luzmo(key, token)\ndataset = client.create("securable", {"type": "dataset", "name" : {"en":"Example with python sdk"}})\nclient.update("securable", dataset[" "], {"description":{"en":"This is an example description"}})\n```\n\nOptionally for people working with VPC or on our US multitenant environment, you can also define an api_host while creating the client. If not it will default to "https://api.luzmo.com"\n\nE.g.:\n\n```console\nclient = Luzmo(key, token, "https://api.us.luzmo.com")\n```\n\nThere is also the option of adding a dictionary of proxies while creating the API client.\n\nUpdate description of dataset:\n\n```console\nclient.update("securable", dataset["id"], {"description":{"en":"Joost edited"}})\n```\n\nCreate a column in the dataset:\n\n```console\nburrito_column = client.create(\'column\', { "type": \'hierarchy\', "format": \'\',"informat": \'hierarchy\', "order": 0,"name": {"nl": \'Type burrito\'}})\nclient.associate("securable", dataset["id"], "Columns", burrito_column["id"])\n```\n\nAdd Values to the column:\n\n```console\nclient.create("data", dataset["id"], {"securable_id": dataset["id"],"type": "append", "data": [["sweet"], ["sour"]]})\n```\n\nReplace Values in the column:\n\n```console\nclient.create("data", {"securable_id": dataset["id"],"type": "replace", "data": [["bitter"], ["salty"]]})\n```\n\n### Documentation\n\nThe API documentation (available services and methods) can be found at https://developer.luzmo.com\n',
    'author': 'Luzmo team',
    'author_email': 'engineering@luzmo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luzmo-official/luzmo-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

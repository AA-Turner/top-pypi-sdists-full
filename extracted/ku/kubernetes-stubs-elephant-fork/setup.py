# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubernetes-stubs', 'kubernetes_ext']

package_data = \
{'': ['*'],
 'kubernetes-stubs': ['client/*',
                      'client/api/*',
                      'client/models/*',
                      'config/*']}

setup_kwargs = {
    'name': 'kubernetes-stubs-elephant-fork',
    'version': '32.0.1',
    'description': 'Type stubs for the Kubernetes Python API client',
    'long_description': '# kubernetes-stubs-elephant-fork\n\nfork of [kubernetes-stubs][1]\n\n## why fork?\n\n[kubernetes-stubs][1] has not provided stubs for [kubernetes][2] >= 23.0 yet (2023-05-30).\n\n`kubernetes-stubs-elephant-fork` provides stubs for all releases after 7.0 of [kubernetes][2],\neven includes any release in the future automatically.\n\nI run a crontab by github actions which looks for new releases of [kubernetes][2]\nand build stubs for it.\n\n[1]: https://pypi.org/project/kubernetes-stubs\n[2]: https://pypi.org/project/kubernetes\n',
    'author': 'Nikhil Benesch',
    'author_email': 'nikhil.benesch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lexdene/kubernetes-stubs',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

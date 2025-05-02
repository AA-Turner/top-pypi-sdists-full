# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['none',
 'none.collection',
 'none.hash',
 'none.hash.cdc',
 'none.task',
 'none.text']

package_data = \
{'': ['*']}

install_requires = \
['rfc3986[url]>=2.0.0,<3.0.0', 'sphinx[docs]>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'none',
    'version': '0.1.1',
    'description': 'An extensive library providing additional facilities to the Python Standard Library.',
    'long_description': '.. README.rst\n.. ==========\n..\n.. Copying\n.. -------\n..\n.. Copyright (c) 2020 none authors and contributors.\n..\n.. This file is part of the *none* project.\n..\n.. None is a free software project. You can redistribute it and/or\n.. modify it following the terms of the MIT License.\n..\n.. This software project is distributed *as is*, WITHOUT WARRANTY OF ANY\n.. KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.\n..\n.. You should have received a copy of the MIT License along with\n.. *none*. If not, see <http://opensource.org/licenses/MIT>.\n\n.. image:: https://circleci.com/gh/spack971/none.svg\n  :alt: CircleCI status\n  :target: https://circleci.com/gh/spack971/none\n\n\nnone\n====\n\nIn the beginning there was none, and then bang a bunch of extra batteries\nstarted to fill the Python universe.\n\n*None* is an extensive Python library offering a range of extra facilities not\nfound in the `Python Standard Library\n<https://docs.python.org/3/library/index.html>`_.\n\n\nLicensing\n---------\n\nThis software project is provided under the licensing terms of the\nMIT License stated in the file ``LICENSE.rst``.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE\nLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION\nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION\nWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'See AUTHORS.rst',
    'author_email': 'dev@jimmy.lt',
    'maintainer': 'Jimmy Thrasibule',
    'maintainer_email': 'dev@jimmy.lt',
    'url': 'https://github.com/spack971/none',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

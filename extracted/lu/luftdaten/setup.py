# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['luftdaten']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<1']

setup_kwargs = {
    'name': 'luftdaten',
    'version': '0.7.4',
    'description': 'Python API for interacting with luftdaten.info',
    'long_description': 'python-luftdaten\n================\n\nPython client for interacting with `sensor.community <https://sensor.community/>`_ (previously known as `luftdaten.info <http://luftdaten.info/>`_.\n\nThis module is not official, developed, supported or endorsed by sensor.community/luftdaten.info.\n\nInstallation\n------------\n\nThe module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.\n\n.. code:: bash\n\n    $ pip3 install luftdaten\n\nOn a Fedora-based system or on a CentOS/RHEL machine with has EPEL enabled.\n\n.. code:: bash\n\n    $ sudo dnf -y install python3-luftdaten\n\nFor Nix or NixOS is `pre-packed module <https://search.nixos.org/packages?channel=unstable&from=0&size=50&sort=relevance&query=luftdaten>`_\navailable. The lastest release is usually present in the ``unstable`` channel.\n\n.. code:: bash\n\n    $ nix-env -iA nixos.python39Packages.luftdaten\n\nUsage\n-----\n\nThe file ``example.py`` contains an example about how to use this module.\n\nLicense\n-------\n\n``python-luftdaten`` is licensed under MIT, for more details check LICENSE.\n',
    'author': 'Fabian Affolter',
    'author_email': 'mail@fabian-affolter.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/home-assistant-ecosystem/python-luftdaten',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

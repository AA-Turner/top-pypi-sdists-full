# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nvsmi']
entry_points = \
{'console_scripts': ['nvsmi = nvsmi:_main']}

setup_kwargs = {
    'name': 'nvsmi',
    'version': '0.4.2',
    'description': 'A (user-)friendly wrapper to nvidia-smi',
    'long_description': '# nvsmi\n\nA (user-)friendly wrapper to `nvidia-smi`.\n\nIt can be used to filter the GPUs based on resource usage (e.g. to choose the least utilized GPU on a multi-GPU system).\n\n## Usage\n\n### CLI\n\n```\nnvsmi --help\nnvsmi ls --help\nnvsmi ps --help\n```\n\n### As a library\n\n```\nimport nvsmi\n\nnvsmi.get_gpus()\nnvsmi.get_available_gpus()\nnvsmi.get_gpu_processes()\n```\n\n## Prerequisites\n\n- An nvidia GPU\n- `nvidia-smi`\n- Python 2.7 or 3.6+\n\n## Installation\n\n### pipx\n\nThe recommended installation method is [pipx](https://github.com/pipxproject/pipx).\nMore specifically, you can install `nvsmi` for your user with:\n\n``` shell\npipx install nvsmi\n```\n\nThe above command will create a virtual environment in `~/.local/pipx/venvs/nvsmi` and\nadd the `nvsmi` executable in `~/.local/bin`.\n\n### pip\n\nAlternatively you can use good old `pip` but this is more fragile than `pipx`:\n\n```\npip install --user nvsmi\n```\n',
    'author': 'Panos Mavrogiorgos',
    'author_email': 'pmav99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pmav99/nvsmi',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

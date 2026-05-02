# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sprint_datapusher']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'jsonpickle>=1.4.1,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'watchdog>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['sprint_datapusher = sprint_datapusher.datapusher:cli']}

setup_kwargs = {
    'name': 'sprint-datapusher',
    'version': '0.1.2',
    'description': 'A tool to read csv files, transform to json and push to sprint_excel_webserver.',
    'long_description': '# datapusher\n\nOvervåker folder og sender data i nye/endrede filer som json til sprint-webserver.\n\n## Overvåke folder for endringer i filer\n\n```\n% pip install sprint-datapusher\n% sprint_datapusher --help                                 \nUsage: sprint_datapusher [OPTIONS] URL\n\n  CLI for monitoring directory and send content of files as json to\n  webserver URL.\n\n  URL is the url to a webserver exposing an endpoint accepting your json.\n\n  To stop the datapusher, press Control-C.\n\nOptions:\n  --version                  Show the version and exit.\n  -d, --directory DIRECTORY  Relative path to the directory to watch\n                             [default: /home/stigbd/src/heming-\n                             langrenn/sprint-excel/datapusher]\n\n  -h, --help                 Show this message and exit.\n\n```\n\n## Development\n### Requirements\n- [pyenv](https://github.com/pyenv/pyenv-installer)\n- [pipx](https://github.com/pipxproject/pipx)\n- [poetry](https://python-poetry.org/)\n- [nox](https://nox.thea.codes/en/stable/)\n- [nox-poetry](https://github.com/cjolowicz/nox-poetry)\n\n```\n% curl https://pyenv.run | bash\n% pyenv install 3.9.1\n% pyenv install 3.7.9\n% python3 -m pip install --user pipx\n% python3 -m pipx ensurepath\n% pipx install poetry\n% pipx install nox\n% pipx inject nox nox-poetry\n```\n\n### Install\n```\n% git clone https://github.com/heming-langrenn/sprint-excel.git\n% cd sprint-excel/datapusher\n% pyenv local 3.9.1 3.7.9\n% poetry install\n```\n### Run all sessions\n```\n% nox\n```\n### Run all tests with coverage reporting\n```\n% nox -rs tests\n```\n## Run cli script\n```\n% poetry shell\n% sprint_datapusher --help\n```\nAlternatively you can use `poetry run`:\n```\n% poetry run sprint_datapusher --help\n```\n',
    'author': 'Stig B. Dørmænen',
    'author_email': 'stigbd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/heming-langrenn/sprint-excel/tree/main/datapusher',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

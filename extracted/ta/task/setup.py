# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<2.0.0',
 'click-aliases>=1.0.1,<2.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click-help-colors>=0.9,<0.10',
 'click>=7.1.2,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'rich>=9.8.2,<10.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['pytask = task.main:main', 'task = task.main:main']}

setup_kwargs = {
    'name': 'task',
    'version': '0.2.5',
    'description': 'Task cli tool',
    'long_description': '# task\n\n[![Build Status](http://drone.matteyeux.com/api/badges/matteyeux/task/status.svg)](http://drone.matteyeux.com/matteyeux/task)\n\nTaskwarrior-like CLI tool\n\n```\nUsage: task [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -v, --version  print version\n  --help         Show this message and exit.\n\nCommands:\n  add       Add task\n  describe  Describe task.\n  done      Finished task.\n  ls        List tasks.\n  rm        Remove a task.\n```\n\n### Installation\n\nMake sure to have [poetry](https://pypi.org/project/poetry)\n\n#### Github repository\n```bash\n$ git clone https://github.com/matteyeux/task\n$ cd task\n$ poetry install\n```\n\n#### PyPI\n- Installation : `pip3 install task`\n- Update : `pip3 install --upgrade task`\n\n### Setup\n\nMake sure to have `~/.local/bin` in your `$PATH` (`export PATH=$PATH:~/.local/bin`)\n\nThe first time you run `task add` command it will setup the SQLite3 database.\n\n\n### Examples\n\n#### Add\n- Add task: `task add "Start TIC-BLK4" -p BLK4`\n- Add task in project: `task add "Start TIC-BLK4" -p BLK4`\n\n#### List\nList tasks :\n```\nλ ~ » task ls\n  ID  Project    Task                          Urgency  Due    Age\n   1  etna_cli   fix my bug                          0         4 minutes\n   2  etna_cli   add tabulate to list stuff          0         4 minutes\n   3  Master2    Get that diploma                    0         3 minutes\n   4             Buy a new iPhone                    0         2 minutes\n   5             Patch the covid-19 bug              0         41 seconds\n   6  BLK4       Start TIC-BLK4                      0         9 seconds\n```\n\n#### Done\n\nSet task to done :\n```\nλ ~ » task done 6\nDone 6\n```\n\n#### Remove\n\nDelete row from database :\n```\nλ ~ » task rm 5\nDone\n```\n\n### Credits\n- Task Warrior :  because it\'s a pretty cool project\n- me : cuz I wrote it\n',
    'author': 'matteyeux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matteyeux/task',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

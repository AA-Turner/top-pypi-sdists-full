# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_use_pathlib']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.6']

entry_points = \
{'flake8.extension': ['PL = flake8_use_pathlib:PathlibChecker']}

setup_kwargs = {
    'name': 'flake8-use-pathlib',
    'version': '0.3.0',
    'description': 'A plugin for flake8 finding use of functions that can be replaced by pathlib module.',
    'long_description': '# flake8-use-pathlib\n\n[![pypi][pypi-badge]](https://pypi.org/project/flake8-use-pathlib/)\n[![black][black-badge]](https://github.com/psf/black)\n\nA plugin for flake8 finding use of functions that can be replaced by pathlib module.\n\n[pypi-badge]: https://badgen.net/pypi/v/flake8-use-pathlib\n[black-badge]: https://badgen.net/badge/code%20style/black/black/\n\n## Installation\n\nInstall from `pip` with:\n\n`pip install flake8-use-pathlib`\n\n## Rules\n\n| Code  | Rule                                                                                         |\n| ----- | -------------------------------------------------------------------------------------------- |\n| PL100 | os.path.abspath("foo") should be replaced by foo_path.resolve()                              |\n| PL101 | os.chmod("foo", 0o444) should be replaced by foo_path.chmod(0o444)                           |\n| PL102 | os.mkdir("foo") should be replaced by foo_path.mkdir()                                       |\n| PL103 | os.makedirs("foo/bar") should be replaced by bar_path.mkdir(parents=True)                    |\n| PL104 | os.rename("foo", "bar") should be replaced by foo_path.rename(Path("bar"))                   |\n| PL105 | os.replace("foo", "bar") should be replaced by foo_path.replace(Path("bar"))                 |\n| PL106 | os.rmdir("foo") should be replaced by foo_path.rmdir()                                       |\n| PL107 | os.remove("foo") should be replaced by foo_path.unlink()                                     |\n| PL108 | os.unlink("foo") should be replaced by foo_path.unlink()                                     |\n| PL109 | os.getcwd() should be replaced by Path.cwd()                                                 |\n| PL110 | os.path.exists("foo") should be replaced by foo_path.exists()                                |\n| PL111 | os.path.expanduser("~/foo") should be replaced by foo_path.expanduser()                      |\n| PL112 | os.path.isdir("foo") should be replaced by foo_path.is_dir()                                 |\n| PL113 | os.path.isfile("foo") should be replaced by foo_path.is_file()                               |\n| PL114 | os.path.islink("foo") should be replaced by foo_path.is_symlink()                            |\n| PL115 | os.readlink("foo") should be replaced by foo_path.readlink()                                 |\n| PL116 | os.stat("foo") should be replaced by foo_path.stat() or foo_path.owner() or foo_path.group() |\n| PL117 | os.path.isabs should be replaced by foo_path.is_absolute()                                   |\n| PL118 | os.path.join("foo", "bar") should be replaced by foo_path / "bar"                            |\n| PL119 | os.path.basename("foo/bar") should be replaced by bar_path.name                              |\n| PL120 | os.path.dirname("foo/bar") should be replaced by bar_path.parent                             |\n| PL121 | os.path.samefile("foo", "bar") should be replaced by foo_path.samefile(bar_path)             |\n| PL122 | os.path.splitext("foo.bar") should be replaced by foo_path.suffix                            |\n| PL123 | open("foo") should be replaced by Path("foo").open()                                         |\n| PL124 | py.path.local is in maintenance mode, use pathlib instead                                    |\n',
    'author': 'Rodolphe Pelloux-Prayer',
    'author_email': 'rodolphe@damsy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/RoPP/flake8-use-pathlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

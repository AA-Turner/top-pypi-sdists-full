# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvsslib',
 'cvsslib.contrib',
 'cvsslib.cvss2',
 'cvsslib.cvss3',
 'cvsslib.cvss31']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cvss = cvsslib.command:main']}

setup_kwargs = {
    'name': 'cvsslib',
    'version': '1.0.0',
    'description': 'CVSS 2/3 utilities',
    'long_description': '# CVSSlib ![Main workflow](https://github.com/orf/cvsslib/workflows/Tests/badge.svg)\n\nA Python 3 library for calculating CVSS v2, CVSS v3 and CVSS v3.1 vectors, with tests. Examples on how to use\nthe library is shown below, and there is some documentation on the internals within the `docs` directory. The library \nis designed to be completely extendable, so it is possible to implement your own custom scoring systems (or those of your clients)\nand have it work with the same API, and with the same bells and whistles.\n\n**Python 3 only**\n\n## API\n\nIt\'s pretty simple to use. `cvsslib` has a `cvss2`, `cvss3` and `cvss31` sub modules that contains all of the enums\nand calculation code. There are also some functions to manipulate vectors that take these cvss modules\nas arguments. E.G:\n\n```python\nfrom cvsslib import cvss2, cvss31, calculate_vector\n\nvector_v2 = "AV:L/AC:M/Au:S/C:N/I:P/A:C/E:U/RL:OF/RC:UR/CDP:N/TD:L/CR:H/IR:H/AR:H"\ncalculate_vector(vector_v2, cvss2)\n>> (5, 3.5, 1.2)\n\nvector_v3 = "CVSS:3.0/AV:L/AC:L/PR:H/UI:R/S:U/C:H/I:N/A:H/MPR:N"\ncalculate_vector(vector_v3, cvss31)\n>> (5.8, 5.8, 7.1)\n```\n\nYou can access every CVSS enum through the `cvss2`, `cvss3` or `cvss31` modules:\n\n```python\nfrom cvsslib import cvss2\n# In this case doing from \'cvsslib.cvss2.enums import *\' might be less verbose.\nvalue = cvss2.ReportConfidence.CONFIRMED\n\nif value != cvss2.ReportConfidence.NOT_DEFINED:\n    do_something()\n```  \n        \nThere are some powerful mixin functions if you need a class with CVSS members. These functions\ntake a cvss version and return a base class you can inherit from. This class hassome utility functions like \n`to_vector()` and `from_vector()` you can use.\n\n```python\nfrom cvsslib import cvss3, class_mixin\n\nBaseClass = class_mixin(cvss3)  # Can pass cvss2 module instead\n\nclass SomeObject(BaseClass):\n    def print_stats(self):\n        for item, value in self.enums:\n            print("{0} is {1}".format(item, value)\n \nstate = SomeObject()\nprint("\\n".join(state.debug()))\nprint(state.calculate())\nstate.from_vector("CVSS:3.0/AV:L/AC:L/PR:H/UI:R/S:U/C:H/I:N/A:H/MPR:N")\nprint("Vector: " + state.to_vector())\n\n# Access members:\nif state.report_confidence == ReportConfidence.NOT_DEFINED:\n    do_something()\n```\n\nIt also supports Django models. Requires the `django-enumfields` package.\n\n```python\nfrom cvsslib.contrib.django_model import django_mixin\nfrom cvsslib import cvss2\nfrom django.db import models\n\nCVSSBase = django_mixin(cvss2)\n\nclass CVSSModel(models.Model, metaclass=CVSSBase)\n    pass\n    \n# CVSSModel now has lots of enum you can use\nx = CVSSModel()\nx.save()\nx.exploitability\n```\n\nIf you want it to work with django Migrations you need to give an attribute name to the `django_mixin` function. This\nshould match the attribute name it is being assigned to:\n\n```python\nCVSSBase = django_mixin(cvss2, attr_name="CVSSBase")\n```\n \nAnd there is a command line tool available:\n \n```python\n> cvss CVSS:3.0/AV:L/AC:H/PR:H/UI:N/S:C/C:N/I:H/A:N/E:P/RL:U/RC:U/CR:H/IR:L/AR:H/MAV:L/MUI:R/MS:C/MC:N/MI:L/MA:N\nBase Score:     5.3\nTemporal:       4.6\nEnvironment:    1.3\n```\n \n## Custom Scoring Systems\n\nCreating a new scoring system is very simple. First create a Python file with the correct name, e.g `super_scores.py`. \nNext create some enums with the correct values for your system:\n \n```python\n from cvsslib.base_enum import BaseEnum\n \n \n class Risk(BaseEnum):\n     """\n     Vector: S\n     """\n     HIGH = 1\n     MEDIUM = 2\n     LOW = 3\n     \n class Difficulty(BaseEnum):\n     """\n     Vector: D\n     """\n     DIFFICULT = 1\n     MODERATE = 2\n     EASY = 3\n```\n \nAnd lastly add a `calculate` function in the module that accepts some vector values and \nreturns a result of some kind:\n\n```python\n\ndef calculate(difficulty: Difficulty, risk: Risk):\n   if difficulty == Difficulty.EASY and risk == Risk.CRITICAL:\n       return "oh nuts you\'re screwed"\n   \n   return "You\'re probs ok m8"\n```\n\nOnce you define this you can pass your `super_scores` module to any \ncvsslib function like `calculate_vector` or `django_mixin` and it will \nall just work. You can even serialize the data to and from a vector \nif you define the correct `vector: X` in the enum docstrings.\n',
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orf/cvsslib/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

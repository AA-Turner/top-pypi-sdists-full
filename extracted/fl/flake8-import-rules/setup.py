# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_import_rules']
entry_points = \
{'flake8.extension': ['I013 = flake8_import_rules:ImportRulesChecker']}

setup_kwargs = {
    'name': 'flake8-import-rules',
    'version': '1.0.0',
    'description': '',
    'long_description': 'Helps to prevent import of certain modules from certain modules.\n\nIt\'s useful if you have many modules in your project and want to keep them kind of\nisolated.\n\nAfter installing just add `import-rules` option to your `setup.cfg` file.\n\n```\n[flake8]\n...\nimport-rules= \n\t# yaml format here\n\t- module_one: [\n\t\tmodule_two allow,\n\t\tany deny\n\t]\n\t- module_two: [\n\t\tmodule_one.sub.submodule deny\n\t]\n\t- module_two.sumbodule: module_one deny\n\t- module_three: any allow\n\n\t# many section for the same module are allowed\n\t# for example\n\t- module_two: [\n\t\tdeny some_other_module\n\t]\n\n\t# this will prevent any import everywhere\n\t- any: [\n\t\tany deny\n\t]\n\n\t# default behaviour is\n\t- any: [\n\t\tany allow\n\t]\n\n\t# For each module (among foo bar baz) allow import from self submodules \n\t# and top module of others but not from submodules\n\t- X | Y | foo | bar | baz : [\n\t\tY.ANY deny,\n\t\tY     allow,\n\t\tX \t  allow\n\n\t]\n\n...\n```\nRules are checking top-down. The Order Matters.\n\nIf current module name match section name or is submodule, then it will check all imports by rules from the section.\n\nThere can be one or more rules in section.\nThere can be one or more sections for the same module/submodule.\n\n`modulepath allow` - means allow imports from `modulepath` and its submodules\n\n`modulepath deny` - means deny imports from `modulepath` and its submodules.\n\nKeyword `any` or `ANY` or `all` or `ALL` - menas any module (like `*`)\n\nTo combine different module paths in one rule we can use `|` symbol. For example\nto define rule for foo.hi foo.low bar.hi bar.low we can use \n`foo|bar.hi|low` . \n\nWe can "define" variable that will be valid only during one section and its rules.\n```\nA | B | foo | bar | baz : [\n\t...\n]\n```\nmeans if current module name is foo or bar or baz then A is equal to current module name\nand B will correspond other names from group foo|bar|baz without current module name.\n\nVariable name can be only single uppercase character. You can use variable name in section rule and inside section.\n\nYou can use variables for different module level for example\n\n```\nX|mod_a|mod_b.domain.Y : [\n\tX.infra.Y allow\n\tX.infra.ANY deny\n]\n```\n\n   \nCAUTION. As .INI configparser ignores indentation use `[ ... , .. ]` flow for lists as in example.\n\n',
    'author': 'VL',
    'author_email': '1844144@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

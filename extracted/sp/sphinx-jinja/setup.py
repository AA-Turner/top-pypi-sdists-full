# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_jinja']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11', 'docutils>=0.16', 'sphinx>4.2.0']

setup_kwargs = {
    'name': 'sphinx-jinja',
    'version': '2.0.2',
    'description': 'includes jinja templates in a documentation',
    'long_description': "\n.. image:: https://github.com/tardyp/sphinx-jinja/actions/workflows/ci.yml/badge.svg\n\nsphinx-jinja\n============\n\nA sphinx extension to include jinja based templates based documentation into a sphinx doc\n\nUsage\n=====\n\nIn your rst doc, you can use the following snippet to use a jinja template to generate your doc\n\n.. code:: rst\n\n    .. jinja:: first_ctx\n\n        {% for k, v in topics.items() %}\n\n        {{k}}\n        ~~~~~\n        {{v}}\n        {% endfor %}\n\nIn your sphinx ``conf.py`` file, you can create or load the contexts needed for your jinja templates\n\n.. code:: python\n\n    extensions = ['sphinx_jinja']\n\n    jinja_contexts = {\n        'first_ctx': {'topics': {'a': 'b', 'c': 'd'}}\n    }\n\nYou can also customize the jinja ``Environment`` by passing custom kwargs, adding filters, tests, and globals, and setting policies:\n\n.. code:: python\n\n    jinja_env_kwargs = {\n        'lstrip_blocks': True,\n    }\n\n    jinja_filters = {\n        'bold': lambda value: f'**{value}**',\n    }\n\n    jinja_tests = {\n        'instanceof': lambda value, type: isinstance(value, type),\n    }\n\n    jinja_globals = {\n        'list': list,\n    }\n\n    jinja_policies = {\n        'compiler.ascii_str': False,\n    }\n\nWhich can then be used in the templates:\n\n.. code:: rst\n\n    Lists\n    -----\n\n    {% for o in objects -%}\n        {%- if o is instanceof list -%}\n            {%- for x in o -%}\n                - {{ x|bold }}\n            {% endfor -%}\n        {%- endif -%}\n    {%- endfor %}\n\n\nAvailable options\n=================\n\n- ``file``: allow to specify a path to Jinja instead of writing it into the content of the\n  directive. Path is relative to the current directory of sphinx-build tool, typically the directory\n  where the ``conf.py`` file is located.\n\n- ``header_char``: character to use for the the headers. You can use it in your template to set your\n  own title character:\n\n  For example:\n\n  .. code:: rst\n\n      Title\n      {{ options.header_char * 5 }}\n\n- ``header_update_levels``: If set, a header in the template will appear as the same level as a\n  header of the same style in the source document, equivalent to when you use the ``include``\n  directive. If not set, headers from the template will be in levels below whatever level is active\n  in the source document.\n\n- ``debug``: print debugging information during sphinx-build. This allows you to see the generated\n  rst before sphinx builds it into another format.\n\nExample of declaration in your RST file:\n\n.. code:: rst\n\n      .. jinja:: approval_checks_api\n         :file: relative/path/to/template.jinja\n         :header_char: -\n\nEach element of the ``jinja_contexts`` dictionary is a context dict for use in your jinja templates.\n\n\nRunning tests\n=============\n\n* pip install tox\n* tox\n",
    'author': 'Pierre Tardy',
    'author_email': 'tardyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tardyp/sphinx-jinja',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)

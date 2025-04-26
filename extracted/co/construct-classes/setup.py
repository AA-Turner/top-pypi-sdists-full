# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['construct_classes']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10,<3.0']

setup_kwargs = {
    'name': 'construct-classes',
    'version': '0.1.2',
    'description': 'Parse your binary structs into dataclasses',
    'long_description': '=================\nconstruct-classes\n=================\n\n.. image:: https://img.shields.io/pypi/v/construct-classes.svg\n        :target: https://pypi.python.org/pypi/construct-classes\n\n.. .. image:: https://readthedocs.org/projects/construct-classes/badge/?version=latest\n..         :target: https://construct-classes.readthedocs.io/en/latest/?badge=latest\n..         :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/trezor/construct-classes/shield.svg\n     :target: https://pyup.io/repos/github/trezor/construct-classes/\n     :alt: Updates\n\n\nParse your binary data into dataclasses. Pack your dataclasses into binary data.\n\n:code:`construct-classes` rely on `construct`_ for parsing and packing. The\nprogrammer needs to manually write the Construct expressions. There is also no type\nverification, so it is the programmer\'s responsibility that the dataclass and the\nConstruct expression match.\n\nFor fully type annotated experience, install `construct-typing`_.\n\nThis package typechecks with `mypy`_ and `pyright`_.\n\n.. _construct: https://construct.readthedocs.io/en/latest/\n.. _construct-typing: https://github.com/timrid/construct-typing\n.. _mypy: https://mypy.readthedocs.io/en/stable/\n.. _pyright: https://github.com/microsoft/pyright\n\nUsage\n-----\n\nAny child of :code:`Struct` is a Python dataclass. It expects a Construct :code:`Struct`\nexpression in the :code:`SUBCON` attribute. The names of the attributes of the dataclass\nmust match the names of the fields in the Construct struct.\n\n.. code-block:: python\n\n    import construct as c\n    from construct_classes import Struct, subcon\n\n    class BasicStruct(Struct):\n        x: int\n        y: int\n        description: str\n\n        SUBCON = c.Struct(\n            "x" / c.Int32ul,\n            "y" / c.Int32ul,\n            "description" / c.PascalString(c.Int8ul, "utf8"),\n        )\n\n\n    data = b"\\x01\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x05hello"\n    parsed = BasicStruct.parse(data)\n    print(parsed)  # BasicStruct(x=1, y=2, description=\'hello\')\n\n    new_data = BasicStruct(x=100, y=200, description="world")\n    print(new_data.build())  # b\'\\x64\\x00\\x00\\x00\\xc8\\x00\\x00\\x00\\x05world\'\n\n\n:code:`construct-classes` support nested structs, but you need to declare them explicitly:\n\n.. code-block:: python\n\n    class LargerStruct(Struct):\n        # specify the subclass type:\n        basic: BasicStruct = subcon(BasicStruct)\n        # in case of a list, specify the item type:\n        basic_array: List[BasicStruct] = subcon(BasicStruct)\n        # the `subcon()` function supports all arguments of `dataclass.field`:\n        default_array: List[BasicStruct] = subcon(BasicStruct, default_factory=list)\n\n        # to refer to the subcon, use the `SUBCON` class attribute:\n        SUBCON = c.Struct(\n            "basic" / BasicStruct.SUBCON,\n            "basic_array" / c.Array(2, BasicStruct.SUBCON),\n            "default_array" / c.PrefixedArray(c.Int8ul, BasicStruct.SUBCON),\n        )\n\nUse :code:`dataclasses.field()` to specify attributes on fields that are not subcons.\n\nThere are currently no other features. In particular, the resulting class is a Python\ndataclass, but you cannot specify its parameters like :code:`frozen` etc.\n\n\nInstalling\n----------\n\nInstall using pip:\n\n    $ pip install construct-classes\n\n\nChangelog\n~~~~~~~~~\n\nSee `CHANGELOG.rst`_.\n\n.. _CHANGELOG.rst: https://github.com/matejcik/construct-classes/blob/master/CHANGELOG.rst\n\n\nFooter\n------\n\n* Free software: MIT License\n\n.. * Documentation: https://construct-classes.readthedocs.io.\n',
    'author': 'matejcik',
    'author_email': 'ja@matejcik.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matejcik/construct-classes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)

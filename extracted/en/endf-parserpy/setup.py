# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['endf_parserpy',
 'endf_parserpy.cli',
 'endf_parserpy.cli.actions',
 'endf_parserpy.compiler',
 'endf_parserpy.compiler.cpp_templates',
 'endf_parserpy.compiler.cpp_types',
 'endf_parserpy.compiler.cpp_types.cpp_type_matrix2d',
 'endf_parserpy.compiler.cpp_types.cpp_type_nested_vector',
 'endf_parserpy.compiler.cpp_types.cpp_type_scalar',
 'endf_parserpy.compiler.cpp_types.cpp_type_template',
 'endf_parserpy.compiler.expr_utils',
 'endf_parserpy.cpp_parsers',
 'endf_parserpy.endf_recipes',
 'endf_parserpy.endf_recipes.endf6',
 'endf_parserpy.endf_recipes.endf6_ext',
 'endf_parserpy.endf_recipes.jendl',
 'endf_parserpy.endf_recipes.pendf',
 'endf_parserpy.interpreter',
 'endf_parserpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.0', 'lark>=1.0.0']

entry_points = \
{'console_scripts': ['endf-cli = endf_parserpy.cli.cmd:cli_interface']}

setup_kwargs = {
    'name': 'endf-parserpy',
    'version': '0.13.1',
    'description': 'A Python package for reading, writing, verifying and translating ENDF-6 files',
    'long_description': '# endf-parserpy - an ENDF-6 toolkit for Python\n\n`endf-parserpy` is a Python package for reading\nand writing [ENDF-6](https://doi.org/10.2172/1425114) files.\nThis functionality in combination with Python\'s\npowerful facilities for data handling enables you to\nperform various actions on ENDF-6 files, such as:\n\n- Easily access any information\n- Modify, delete and insert data\n- Perform format validation\n- Convert from and to other file formats, such as JSON\n- Merge data from various ENDF-6 files into a single one\n- Compare ENDF-6 files with meaningful reporting on differences\n- Construct ENDF-6 files from scratch\n- Many of these actions can be performed via the command line\n\n\nThe support for the [ENDF-6 format]((https://doi.org/10.2172/1425114))\nis comprehensive.\nThe package has been tested on the various sublibraries\nof the major nuclear data libraries, such as\n[ENDF/B](https://www.nndc.bnl.gov/endf/),\n[JEFF](https://www.oecd-nea.org/dbdata/jeff/),\nand [JENDL](https://wwwndc.jaea.go.jp/jendl/jendl.html).\nNote that the package does not support several materials\nin a single ENDF-6 file.\n\n\n## Install endf-parserpy\n\nThis package is available on the\n[Python Package Index](https://pypi.org/project/endf-parserpy/)\nand can be installed using ``pip``:\n\n```sh\npip install endf-parserpy\n```\n\n\n## Documentation\n\nThe documentation is available online\n[@readthedocs](https://endf-parserpy.readthedocs.io).\nConsider the ``README.md`` in the ``docs/`` subdirectory\nfor instructions on how to generate the help files locally.\n\n\n## Simple example\n\nThe following code snippet demonstrates\nhow to read an ENDF-6 file, change the\n``AWR`` variable in the MF3/MT1 section\nand write the modified data to a new\nENDF-6 file:\n\n```\nfrom endf_parserpy import EndfParser\nparser = EndfParser()\nendf_dict = parser.parsefile(\'input.endf\')\nendf_dict[3][1][\'AWR\'] = 99.99\nparser.writefile(\'output.endf\', endf_dict)\n```\n\n\n## Citation\n\nIf you want to cite this package,\nplease use the following reference:\n\n```\nG. Schnabel, D. L. Aldama, R. Capote, "How to explain ENDF-6 to computers: A formal ENDF format description language", arXiv:2312.08249, DOI:10.48550/arXiv.2312.08249\n```\n\n\n## License\n\nThis code is distributed under the MIT license augmented\nby an IAEA clause, see the accompanying license file for more information.\n\nCopyright (c) International Atomic Energy Agency (IAEA)\n\n\n## Acknowledgments\n\nDaniel Lopez Aldama made significant contributions\nto the development of this package. He debugged the\nENDF-6 recipe files and helped in numerous discussions\nto convey a good understanding of the technical details of\nthe ENDF-6 format that enabled the creation of this package.\n',
    'author': 'Georg Schnabel',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iaea-nds/endf-parserpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

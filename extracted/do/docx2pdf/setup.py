# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docx2pdf']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.41.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.3.0'],
 ':sys_platform == "darwin"': ['appscript>=1.1.0'],
 ':sys_platform == "win32"': ['pywin32>=227']}

entry_points = \
{'console_scripts': ['docx2pdf = docx2pdf:cli']}

setup_kwargs = {
    'name': 'docx2pdf',
    'version': '0.1.8',
    'description': 'Convert docx to pdf on Windows or macOS directly using Microsoft Word (must be installed).',
    'long_description': '# docx2pdf\n\n[![PyPI](https://img.shields.io/pypi/v/docx2pdf)](https://pypi.org/project/docx2pdf/)\n\nConvert `docx` to `pdf` on Windows or macOS directly using Microsoft Word (must be installed).\n\nOn Windows, this is implemented via [`win32com`](https://pypi.org/project/pywin32/) while on macOS this is implemented via [JXA](https://github.com/JXA-Cookbook/JXA-Cookbook) (Javascript for Automation, aka AppleScript in JS).\n\n## Install\n\nOn macOS:\n\n```\nbrew install aljohri/-/docx2pdf\n```\n\nVia [pipx](https://pipxproject.github.io/pipx/):\n\n```\npipx install docx2pdf\n```\n\nVia pip:\n\n```\npip install docx2pdf\n```\n\n## CLI\n\n```\nusage: docx2pdf [-h] [--keep-active] [--version] input [output]\n\nExample Usage:\n\nConvert single docx file in-place from myfile.docx to myfile.pdf:\n    docx2pdf myfile.docx\n\nBatch convert docx folder in-place. Output PDFs will go in the same folder:\n    docx2pdf myfolder/\n\nConvert single docx file with explicit output filepath:\n    docx2pdf input.docx output.docx\n\nConvert single docx file and output to a different explicit folder:\n    docx2pdf input.docx output_dir/\n\nBatch convert docx folder. Output PDFs will go to a different explicit folder:\n    docx2pdf input_dir/ output_dir/\n\npositional arguments:\n  input          input file or folder. batch converts entire folder or convert\n                 single file\n  output         output file or folder\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --keep-active  prevent closing word after conversion\n  --version      display version and exit\n```\n\n## Library\n\n```python\nfrom docx2pdf import convert\n\nconvert("input.docx")\nconvert("input.docx", "output.pdf")\nconvert("my_docx_folder/")\n```\n\nSee CLI docs above (or in `docx2pdf --help`) for all the different invocations. It is the same for the CLI and python library.\n\n## Jupyter Notebook\n\nIf you are using this in the context of jupyter notebook, you will need `ipywidgets` for the tqdm progress bar to render properly.\n\n```\npip install ipywidgets\njupyter nbextension enable --py widgetsnbextension\n``\n',
    'author': 'Al Johri',
    'author_email': 'al.johri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlJohri/docx2pdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)

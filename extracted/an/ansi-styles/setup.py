# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansi_styles']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ansi-styles',
    'version': '0.2.2',
    'description': 'ANSI escape codes for styling strings in the terminal',
    'long_description': '# ansi-styles\n\n> [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors_and_Styles) for styling strings in the terminal\n\nA port of the Node.js package [`ansi-styles`](https://github.com/chalk/ansi-styles) to Python.\n\n## Install\n\n```\npython3 -m pip install -U ansi-styles\n```\n\n## Usage\n\n```py\nfrom ansi_styles import ansiStyles as styles\n\nprint(f\'{styles.green.open}Hello world!{styles.green.close}\')\n\n# Color conversion between 256/truecolor\n# NOTE: When converting from truecolor to 256 colors, the original color\n#       may be degraded to fit the new color palette. This means terminals\n#       that do not support 16 million colors will best-match the\n#       original color.\nprint(f\'{styles.color.ansi(styles.rgbToAnsi(199, 20, 250))}Hello World{styles.color.close}\')\nprint(f\'{styles.color.ansi256(styles.rgbToAnsi256(199, 20, 250))}Hello World{styles.color.close}\')\nprint(f\'{styles.color.ansi16m(*styles.hexToRgb("#abcdef"))}Hello World{styles.color.close}\')\n```\n\n## License\n\nMIT\n\n## Contact\n\nA library by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!\n\nMy Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It\'s the best way to reach me, and I\'m always happy to hear from you.\n\n- Twitter: [@theshawwn](https://twitter.com/theshawwn)\n- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)\n- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)\n- Website: [shawwn.com](https://www.shawwn.com)\n\n',
    'author': 'Shawn Presser',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shawwn/ansi-styles-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

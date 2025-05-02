# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediatype']

package_data = \
{'': ['*']}

install_requires = \
['enumb>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'mediatype',
    'version': '0.1.6',
    'description': 'Media Type parsing and creation',
    'long_description': "# mediatype\nMedia Type (aka MIME Type) parsing and creation\n\n## Installation\n```console\npip install mediatype\n```\n\n## Usage\n```python\n>>> import mediatype\n```\n\n### Parsing\n```python\n>>> media_type = mediatype.parse('application/manifest+json')\n>>>\n>>> media_type\nMediaType(\n    type='application',\n    subtype='manifest',\n    suffix='json',\n    parameters=None\n)\n>>>\n>>> str(media_type)\n'application/manifest+json'\n```\n\n### Creation\n```python\n>>> media_type = mediatype.MediaType(\n    type='application',\n    subtype='manifest',\n    suffix='json',\n    parameters=None\n)\n>>>\n>>> str(media_type)\n'application/manifest+json'\n```\n\n## References\n* [IANA - Media Types](https://www.iana.org/assignments/media-types/media-types.xhtml)\n* [RFC-6838 - Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838.html)\n* [Mozilla - MIME types (IANA media types)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)\n* [Wikipedia - Media type](https://en.wikipedia.org/wiki/Media_type)\n",
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tombulled/mediatype',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_oidc']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.1.1',
 'fastapi>=0.61.0',
 'pydantic>=2.0.0',
 'python-jose[cryptography]>=3.2.0',
 'requests>=2.24.0']

setup_kwargs = {
    'name': 'fastapi-oidc',
    'version': '0.0.10',
    'description': 'A simple library for parsing and verifying externally issued OIDC ID tokens in fastapi.',
    'long_description': '# FastAPI OIDC\n\n<p align="left">\n    <a href="https://github.com/HarryMWinters/fastapi-oidc/actions?query=workflow%3ATest"\n       target="_blank">\n       <img src="https://github.com/HarryMWinters/fastapi-oidc/workflows/Test/badge.svg"  \n            alt="Test">\n    </a>\n    <a href=\'https://fastapi-oidc.readthedocs.io/en/latest/?badge=latest\'>\n        <img src=\'https://readthedocs.org/projects/fastapi-oidc/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n    <a href="https://pypi.org/project/fastapi-oidc" \n       target="_blank">\n       <img src="https://img.shields.io/pypi/v/fastapi-oidc?color=%2334D058&label=pypi%20package" \n            alt="Package version">\n    </a>\n</p>\n\n---\n\n:warning: **See [this issue](https://github.com/HarryMWinters/fastapi-oidc/issues/1) for\nsimple role-your-own example of checking OIDC tokens.**\n\nVerify and decrypt 3rd party OIDC ID tokens to protect your\n[fastapi](https://github.com/tiangolo/fastapi) endpoints.\n\n**Documentation:** [ReadTheDocs](https://fastapi-oidc.readthedocs.io/en/latest/)\n\n**Source code:** [Github](https://github.com/HarryMWinters/fastapi-oidc)\n\n## Installation\n\n`pip install fastapi-oidc`\n\n## Usage\n\n### Verify ID Tokens Issued by Third Party\n\nThis is great if you just want to use something like Okta or google to handle\nyour auth. All you need to do is verify the token and then you can extract user ID info\nfrom it.\n\n```python3\nfrom fastapi import Depends\nfrom fastapi import FastAPI\n\n# Set up our OIDC\nfrom fastapi_oidc import IDToken\nfrom fastapi_oidc import get_auth\n\nOIDC_config = {\n    "client_id": "0oa1e3pv9opbyq2Gm4x7",\n    # Audience can be omitted in which case the aud value defaults to client_id\n    "audience": "https://yourapi.url.com/api",\n    "base_authorization_server_uri": "https://dev-126594.okta.com",\n    "issuer": "dev-126594.okta.com",\n    "signature_cache_ttl": 3600,\n}\n\nauthenticate_user: Callable = get_auth(**OIDC_config)\n\napp = FastAPI()\n\n@app.get("/protected")\ndef protected(id_token: IDToken = Depends(authenticate_user)):\n    return {"Hello": "World", "user_email": id_token.email}\n```\n\n#### Using your own tokens\n\nThe IDToken class will accept any number of extra field but if you want to craft your\nown token class and validation that\'s accounted for too.\n\n```python3\nclass CustomIDToken(fastapi_oidc.IDToken):\n    custom_field: str\n    custom_default: float = 3.14\n\n\nauthenticate_user: Callable = get_auth(**OIDC_config, token_type=CustomIDToken)\n\napp = FastAPI()\n\n\n@app.get("/protected")\ndef protected(id_token: CustomIDToken = Depends(authenticate_user)):\n    return {"Hello": "World", "user_email": id_token.custom_default}\n```\n',
    'author': 'HarryMWinters',
    'author_email': 'harrymcwinters@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HarryMWinters/fastapi-oidc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

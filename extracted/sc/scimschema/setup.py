# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scimschema', 'scimschema._model', 'scimschema.core_schemas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scimschema',
    'version': '0.3.1',
    'description': 'A validator for System for Cross domain Identity Management (SCIM) responses given predefine schemas',
    'long_description': '.. image:: https://raw.githubusercontent.com/GordonSo/scimschema/master/scimschema-logo.png\n   :target: https://github.com/GordonSo/scimschema\n   :align: center\n   :alt: scimschema-logo\n\n------\n\nScimSchema\n==========\n.. image:: https://github.com/GordonSo/scimschema/workflows/Upload%20Python%20Package/badge.svg\n    :target: https://github.com/GordonSo/scimschema/actions\n\nValidate JSon content given a predefined set of SCIM Schemas (in JSON representation format) as specified in `SCIM <http://www.simplecloud.info/>`_ (supporting Python 3+).\n\nExample use case\n----------------\n\n1) Install the library via pip:\n\n.. code-block:: python\n\n    pip install scimschema\n\n2) Specify any custom schemas in json format as per the rfc requirement: https://tools.ietf.org/html/rfc7643#section-2\n\n3) Put the json files under a Python package as per our examples here: https://github.com/GordonSo/scimschema/tree/master/tests/extension (also checkout our __init__() file which is handy for loading the json)\n\n4) Import the ```validate``` method from scimschema and pass in json response/request content and the extension schemas to assert its validness\n\nTo step through the above in working code, check out this test: `test_scim_schema.py <https://github.com/GordonSo/scimschema/blob/master/tests/test_scim_schema.py>`_.\n\n.. code-block:: python\n\n    from scimschema import validate\n    from . import extension # <- this is the custom schemas define by your: see https://github.com/GordonSo/scimschema/tree/master/tests/extension for example\n\n    # A sample schema, like what we\'d get from response.get(<scim entity url>).json()\n    content = {\n        "schemas": ["urn:ietf:params:scim:schemas:core2:2.0:Group", "urn:huddle:params:scim:schemas:extension:2.0:SimpleAccount"],\n        "id": "2819c223-7f76-453a-919d-413861904646",\n        "externalId": 9,\n        "meta": {\n            "resourceType": "User",\n            "created": "2011-08-01T18:29:49.793Z",\n            "lastModified": "Invalid date",\n            "location": "https://example.com/v2/Users/2819c223...",\n            "version": "W\\/\\"f250dd84f0671c3\\""\n        }\n    }\n    validate(\n        data=content,\n        extension_schema_definitions=extension.schema\n    )\n\n    >>>    E   _scimschema._model.scim_exceptions.AggregatedScimMultValueAttributeValidationExceptions: Found 1 aggregated exceptions at Scim response:\n    >>>    E    ScimAttributeValueNotFoundException:\n    >>>    E    \t \'Single-value attribute:ipRestrictionsEnabled\' is required at the following location \'[\'urn:huddle:params:scim:schemas:extension:2.0:Account\', \'ipRestrictionsEnabled\']\' but found \'{}\'\n    >>>    !!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!\n\n\nFeatures\n--------\n\nSupport for `SCIM 2.0 <http://www.simplecloud.info/#Specification>`_,\n  - Validate SCIM Schema definition\n     - Validate Model (schema) Id, Name, description, attributes\n     - Validate Attribute (schema) Name, Type, Required, Canonical Values, Mutability, Returned, Uniqueness\n\n  - Validate JSON Content against SCIM Schema\n     - Validate significant value against Type (Binary, Boolean, Datetime, Decimal, Integer, Reference, String, Complex, MultiValued)\n     - Characteristics Required, Canonical Values, Uniqueness\n\n\nUpcoming features\n-----------------\n\n  - Validate JSON Content for characteristics below:\n     - Mutability, Returned\n\n\n\nRunning the Test Suite\n----------------------\n\nThe project requires `poetry`\nThe project requires `pytest` to discover tests, and it complies to PEP 517 via Poetry (see pyproject.toml)\nGithub Actions are to run on commit as part of CI and automatic deployments.\n\n\nCreating new release\n--------------------\n\nUpdate scimschema/VERSION and pyproject.toml\nMerge into `release` branch\n\nContributing\n------------\n\nThis project is powered by the QA department at `Huddle <https://twitter.com/HuddleEng>`_\n\nThe source code is available on `GitHub <https://github.com/GordonSo/scimschema>`_.\n\nGet in touch, via GitHub or otherwise, contributors are also welcome!\n',
    'author': 'Gordon So',
    'author_email': 'gordonkwso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GordonSo/scimschema',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

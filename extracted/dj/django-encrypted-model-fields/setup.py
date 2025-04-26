# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['encrypted_model_fields',
 'encrypted_model_fields.management',
 'encrypted_model_fields.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'cryptography>=3.4']

setup_kwargs = {
    'name': 'django-encrypted-model-fields',
    'version': '0.6.5',
    'description': 'A set of fields that wrap standard Django fields with encryption provided by the python cryptography library.',
    'long_description': '# Django Encrypted Model Fields\n\n[![image](https://travis-ci.org/lanshark/django-encrypted-model-fields.png)](https://travis-ci.org/lanshark/django-encrypted-model-fields)\n\n## About\n\nThis is a fork of\n<https://github.com/foundertherapy/django-cryptographic-fields>. It has\nbeen renamed, and updated to properly support Python3 and latest\nversions of Django.\n\n`django-encrypted-model-fields` is set of fields that wrap standard\nDjango fields with encryption provided by the python cryptography\nlibrary. These fields are much more compatible with a 12-factor design\nsince they take their encryption key from the settings file instead of a\nfile on disk used by `keyczar`.\n\nWhile keyczar is an excellent tool to use for encryption, it\'s not\ncompatible with Python 3, and it requires, for hosts like Heroku, that\nyou either check your key file into your git repository for deployment,\nor implement manual post-deployment processing to write the key stored\nin an environment variable into a file that keyczar can read.\n\n## Generating an Encryption Key\n\nThere is a Django management command `generate_encryption_key` provided\nwith the `encrypted_model_fields` library. Use this command to generate\na new encryption key to set as `settings.FIELD_ENCRYPTION_KEY`:\n\n    ./manage.py generate_encryption_key\n\nRunning this command will print an encryption key to the terminal, which\ncan be configured in your environment or settings file.\n\n*NOTE: This command will ONLY work in a CLEAN, NEW django project that\ndoes NOT import encrypted_model_fields in any of it\'s apps.* IF you are\nalready importing encrypted_model_fields, try running this in a python\nshell instead:\n\n    import os\n    import base64\n\n    new_key = base64.urlsafe_b64encode(os.urandom(32))\n    print(new_key)\n\n## Getting Started\n\n> $ pip install django-encrypted-model-fields\n\nAdd "encrypted_model_fields" to your INSTALLED_APPS setting like this:\n\n    INSTALLED_APPS = (\n        ...\n        \'encrypted_model_fields\',\n    )\n\n`django-encrypted-model-fields` expects the encryption key to be\nspecified using `FIELD_ENCRYPTION_KEY` in your project\'s `settings.py`\nfile. For example, to load it from the local environment:\n\n    import os\n\n    FIELD_ENCRYPTION_KEY = os.environ.get(\'FIELD_ENCRYPTION_KEY\', \'\')\n\nTo use an encrypted field in a Django model, use one of the fields from\nthe `encrypted_model_fields` module:\n\n    from encrypted_model_fields.fields import EncryptedCharField\n\n    class EncryptedFieldModel(models.Model):\n        encrypted_char_field = EncryptedCharField(max_length=100)\n\nFor fields that require `max_length` to be specified, the `Encrypted`\nvariants of those fields will automatically increase the size of the\ndatabase field to hold the encrypted form of the content. For example, a\n3 character CharField will automatically specify a database field size\nof 100 characters when `EncryptedCharField(max_length=3)` is specified.\n\nDue to the nature of the encrypted data, filtering by values contained\nin encrypted fields won\'t work properly. Sorting is also not supported.\n\n## Development Environment\n\nAdded Tox for testing with different versions of Django and Python. To get started:\npip install -r requirements/dev.txt\n\nusing `pyenv` add the requisite python interpreters::\npyenv install 3.6.15\n\npyenv install 3.7.12\n\npyenv install 3.8.12\n\npyenv install 3.9.10\n\npyenv install 3.10.2\n\nAdd the requisite versions to the local version::\npyenv local 3.6.15 3.7.12 3.8.12 3.9.10 3.10.2\n\nRun `tox`::\ntox\n',
    'author': 'Scott Sharkey',
    'author_email': 'ssharkey@lanshark.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lansharkconsulting/django/django-encrypted-model-fields',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

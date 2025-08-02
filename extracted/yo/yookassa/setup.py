# -*- coding: utf-8 -*-
import re
import sys
from setuptools import setup, find_packages

long_description = """
# YooKassa API Python Client Library

[![Build Status](https://travis-ci.org/yoomoney/yookassa-sdk-python.svg?branch=master)](https://travis-ci.org/yoomoney/yookassa-sdk-python)
[![Latest Stable Version](https://img.shields.io/pypi/v/yookassa.svg)](https://pypi.org/project/yookassa/)
[![Total Downloads](https://img.shields.io/pypi/dm/yookassa.svg)](https://pypi.org/project/yookassa/)
[![License](https://img.shields.io/pypi/l/yookassa.svg)](https://git.yoomoney.ru/projects/SDK/repos/yookassa-sdk-python)

[Russian](README.md) | English

This product is used for managing payments under [The YooKassa API](https://yookassa.ru/en/developers/api)
For usage by those who implemented YooKassa using the API method.

## Features

* Version 3.x supports Python >=3.7. To work on earlier versions of Python, use versions of yookassa 2.x
* Changing the directory/file structure affected some package imports. When switching from the version of yookassa 2.x, check the imports in your project:
  * `yookassa.domain.models.airline` → `yookassa.domain.models.payment_data.request.airline`
  * `yookassa.domain.models.authorization_details` → `yookassa.domain.models.payment_data.response.authorization_details`
  * `yookassa.domain.models.receipt_customer` → `yookassa.domain.models.receipt_data.receipt_customer`
  * `yookassa.domain.models.receipt_item` → `yookassa.domain.models.receipt_data.receipt_item`
  * `yookassa.domain.models.receipt_item_supplier` → `yookassa.domain.models.receipt_data.receipt_item_supplier`
  * `yookassa.domain.models.recipient` → `yookassa.domain.models.payment_data.recipient`
  * `yookassa.domain.models.refund_source` → `yookassa.domain.models.refund_data.refund_source`
* `Settings.get_account_settings()` now returns the `Me` object. To support compatibility, object fields can be accessed as an array - `me.account_id = me['account_id']`
* The `me.fiscalization_enabled` field is deprecated, but it is still supported. The `me.fiscalization` object has been added instead..

## Requirements
1. Python >=3.7
2. pip

## Installation
### Under console using pip

1. Install pip.
2. In the console, run the following command:
```bash
pip install --upgrade yookassa
```

### Under console using easy_install
1. Install easy_install.
2. In the console, run the following command:
```bash
easy_install --upgrade yookassa
```

## Commencing work

1. Import module
```python
import yookassa
```

2. Configure a Client
```python
from yookassa import Configuration

Configuration.configure('<Account Id>', '<Secret Key>')
```

or

```python
from yookassa import Configuration

Configuration.account_id = '<Account Id>'
Configuration.secret_key = '<Secret Key>'
```

or via oauth

```python
from yookassa import Configuration

Configuration.configure_auth_token('<Oauth Token>')
```

If you agree to participate in the development of the SDK, you can submit data about your framework, cms or module:

```python
from yookassa import Configuration
from yookassa.domain.common.user_agent import Version

Configuration.configure('<Account Id>', '<Secret Key>')
Configuration.configure_user_agent(
    framework=Version('Django', '2.2.3'),
    cms=Version('Wagtail', '2.6.2'),
    module=Version('Y.CMS', '0.0.1')
)
```

3. Call the required API method. [More details in our documentation for the YooKassa API](https://yookassa.ru/en/developers/api)
"""

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Requests requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.

If you can't upgrade your Python version, you'll need to
pin to an older version of YooKassa (<3.0).
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)


with open('src/yookassa/__init__.py') as fp:
    version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

setup(
    name="yookassa",
    author="YooMoney",
    author_email="cms@yoomoney.ru",
    version=version,
    keywords="yoomoney, yookassa, payout, sdk, python",
    description="YooKassa API SDK Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.yoomoney.ru/projects/SDK/repos/yookassa-sdk-python",
    package_dir={"": "src"},
    packages=find_packages('src'),
    install_requires=["requests", "urllib3", "netaddr", "distro", "deprecated"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only"
    ]
)

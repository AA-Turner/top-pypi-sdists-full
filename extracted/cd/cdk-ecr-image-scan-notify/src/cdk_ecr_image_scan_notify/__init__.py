'''
[![NPM version](https://badge.fury.io/js/cdk-ecr-image-scan-notify.svg)](https://badge.fury.io/js/cdk-ecr-image-scan-notify)
[![PyPI version](https://badge.fury.io/py/cdk-ecr-image-scan-notify.svg)](https://badge.fury.io/py/cdk-ecr-image-scan-notify)
![Release](https://github.com/hayao-k/cdk-ecr-image-scan-notify/workflows/release/badge.svg)

# cdk-ecr-image-scan-notify

cdk-ecr-image-scan-notify is an AWS CDK construct library that notify the slack channel of Amazon ECR image scan results.

## Overview

Amazon EventBridge (CloudWatch Events) detects the image scan execution and starts the Lambda function.
The Lambda function summarizes the scan results, formatting them and notifying Slack.

Basic scanning

![](https://raw.githubusercontent.com/hayao-k/cdk-ecr-image-scan-notify/main/images/basic-scanning.png)

Enhanced scanning (Support for initial scan only)

![](https://raw.githubusercontent.com/hayao-k/cdk-ecr-image-scan-notify/main/images/enhanced-scanning.png)

Click on an image name to go to the scan results page.

![](https://github.com/hayao-k/ecr-image-scan-findings-to-slack/raw/master/docs/images/scan-result.png)

## Getting Started

### TypeScript

Installation

```
$ yarn add cdk-ecr-image-scan-notify
```

Usage

```python
import * as cdk from 'aws-cdk-lib';
import { EcrImageScanNotify } from 'cdk-ecr-image-scan-notify';

const mockApp = new cdk.App();
const stack = new cdk.Stack(mockApp, '<your-stack-name>');

new EcrImageScanNotify(stack, 'ecr-image-scan-notify', {
  webhookUrl: '<your-incoming-webhook-url>',
});
```

Deploy!

```
$ cdk deploy
```

### Python

Installation

```
$ pip install cdk-ecr-image-scan-notify
```

Usage

```py
import aws_cdk as cdk
from cdk_ecr_image_scan_notify import EcrImageScanNotify

app = cdk.App()
stack = cdk.Stack(app, "<your-stack-name>", env={'region': 'ap-northeast-1'})

EcrImageScanNotify(stack, "EcrImageScanNotify",
    webhook_url = '<your-incoming-webhook-url>',
)
```

Deploy!

```
$ cdk deploy
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


class EcrImageScanNotify(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ecr-image-scan-notify.EcrImageScanNotify",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        webhook_url: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param webhook_url: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059467cfb9fc4b182ba16cd007f8696e1215628490db00671f6dc7905e1ca4b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcrImageScanNotifyProps(webhook_url=webhook_url)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-ecr-image-scan-notify.EcrImageScanNotifyProps",
    jsii_struct_bases=[],
    name_mapping={"webhook_url": "webhookUrl"},
)
class EcrImageScanNotifyProps:
    def __init__(self, *, webhook_url: builtins.str) -> None:
        '''
        :param webhook_url: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bef84440431af0c8b1eb9aed741cba5edc10a885334c9b35b484c6c15cbdc5a)
            check_type(argname="argument webhook_url", value=webhook_url, expected_type=type_hints["webhook_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "webhook_url": webhook_url,
        }

    @builtins.property
    def webhook_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("webhook_url")
        assert result is not None, "Required property 'webhook_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrImageScanNotifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EcrImageScanNotify",
    "EcrImageScanNotifyProps",
]

publication.publish()

def _typecheckingstub__059467cfb9fc4b182ba16cd007f8696e1215628490db00671f6dc7905e1ca4b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    webhook_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bef84440431af0c8b1eb9aed741cba5edc10a885334c9b35b484c6c15cbdc5a(
    *,
    webhook_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

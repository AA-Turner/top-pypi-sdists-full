r'''
[![NPM version](https://badge.fury.io/js/cdk-events-notify.svg)](https://badge.fury.io/js/cdk-events-notify)
[![PyPI version](https://badge.fury.io/py/cdk-events-notify.svg)](https://badge.fury.io/py/cdk-events-notify)
![Release](https://github.com/neilkuan/cdk-s3bucket/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-events-notify?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-events-notify?label=pypi&color=blue)

# cdk-events-notify

`cdk-events-notify` is an AWS CDK Construct Library that provides you know who login in your aws console.

## Why

It's just a small feature at the moment,
Provides you to trigger Lambda Function push notifications to Slack when you discover Console Login event or switch role event through Cloudtrail.

> Welcome to contribute another event notify case you want.

## Overview

![](./images/overview.png)

### Now support

* Slack ([webhooks](https://api.slack.com/messaging/webhooks#posting_with_webhooks))

## You need enable one `Management events` in your account.

> more see https://aws.amazon.com/tw/cloudtrail/pricing/
> ![](./images/management-events.png)

## Install

```bash
// for CDKv2
npm install cdk-events-notify
or
npm install cdk-events-notify@latest
```

## Usage

```python
import * as cdk from 'aws-cdk-lib';
import { EventNotify } from 'cdk-events-notify';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'integ-stack', { env });
new EventNotify(stack, 'SlackEventNotify', {
  slack: {
    slackChannelName: 'your-channel-name',
    slackWebhookUrl: 'https://hooks.slack.com/services/xxx/xxx/xxx',
  },
});
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```

### Finally

* slack
  ![](./images/slack.jpg)

## More about EventBridge and Lambda

* [EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/aws-events.html)
* [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

> Note: Event Bridge can not cross region , if you console sign in not the cdk-events-notify region will not get the evnet in cloudtrail see this [docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html#cloudtrail-integration_signin-regions)

## :clap:  Supporters

[![Stargazers repo roster for @neilkuan/cdk-events-notify](https://reporoster.com/stars/neilkuan/cdk-events-notify)](https://github.com/neilkuan/cdk-events-notify/stargazers)
[![Forkers repo roster for @neilkuan/cdk-events-notify](https://reporoster.com/forks/neilkuan/cdk-events-notify)](https://github.com/neilkuan/cdk-events-notify/network/members)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import constructs as _constructs_77d1e7e8


class EventNotify(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-events-notify.EventNotify",
):
    '''(experimental) Event Notfiy Construct Class.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        slack: "ISlackEventNotify",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param slack: (experimental) Notify target to Slack channel.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983697ae0c841ff9396c872569908503f3b178d3ccafd540d76c1c1fec6cdd4c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EventNotifyProps(slack=slack)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-events-notify.EventNotifyProps",
    jsii_struct_bases=[],
    name_mapping={"slack": "slack"},
)
class EventNotifyProps:
    def __init__(self, *, slack: "ISlackEventNotify") -> None:
        '''(experimental) event notify interface.

        :param slack: (experimental) Notify target to Slack channel.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ebe07fa9d1a749f691d8c3e288afaed85beeefaf28fccccb71a6d2a71fb24b)
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "slack": slack,
        }

    @builtins.property
    def slack(self) -> "ISlackEventNotify":
        '''(experimental) Notify target to Slack channel.

        :stability: experimental
        '''
        result = self._values.get("slack")
        assert result is not None, "Required property 'slack' is missing"
        return typing.cast("ISlackEventNotify", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventNotifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-events-notify.ISlackEventNotify")
class ISlackEventNotify(typing_extensions.Protocol):
    '''(experimental) slack event notify interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="slackChannelName")
    def slack_channel_name(self) -> builtins.str:
        '''(experimental) slack Channel Name for Lambda send message to slack.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="slackWebhookUrl")
    def slack_webhook_url(self) -> builtins.str:
        '''(experimental) slack Webhook Url for Lambda send message to slack.

        :stability: experimental
        '''
        ...


class _ISlackEventNotifyProxy:
    '''(experimental) slack event notify interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-events-notify.ISlackEventNotify"

    @builtins.property
    @jsii.member(jsii_name="slackChannelName")
    def slack_channel_name(self) -> builtins.str:
        '''(experimental) slack Channel Name for Lambda send message to slack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelName"))

    @builtins.property
    @jsii.member(jsii_name="slackWebhookUrl")
    def slack_webhook_url(self) -> builtins.str:
        '''(experimental) slack Webhook Url for Lambda send message to slack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackWebhookUrl"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISlackEventNotify).__jsii_proxy_class__ = lambda : _ISlackEventNotifyProxy


__all__ = [
    "EventNotify",
    "EventNotifyProps",
    "ISlackEventNotify",
]

publication.publish()

def _typecheckingstub__983697ae0c841ff9396c872569908503f3b178d3ccafd540d76c1c1fec6cdd4c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    slack: ISlackEventNotify,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ebe07fa9d1a749f691d8c3e288afaed85beeefaf28fccccb71a6d2a71fb24b(
    *,
    slack: ISlackEventNotify,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ISlackEventNotify]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])

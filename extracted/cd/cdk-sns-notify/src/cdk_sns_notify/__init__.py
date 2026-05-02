r'''
[![NPM version](https://badge.fury.io/js/cdk-sns-notify.svg)](https://badge.fury.io/js/cdk-sns-notify)
[![PyPI version](https://badge.fury.io/py/cdk-sns-notify.svg)](https://badge.fury.io/py/cdk-sns-notify)
![Release](https://github.com/clarencetw/cdk-sns-notify/workflows/Release/badge.svg)

# cdk-sns-notify

A CDK construct library to send line notify or discord webhook

# Sample

```python
import * as sns from "@aws-cdk/aws-sns";
import * as cloudwatch from "@aws-cdk/aws-cloudwatch";
import * as cw_actions from "@aws-cdk/aws-cloudwatch-actions";

import { SnsNotify } from "cdk-sns-notify";

const topic = new sns.Topic(stack, "Topic");

const metric = new cloudwatch.Metric({
  namespace: "AWS/EC2",
  metricName: "CPUUtilization",
  dimensions: {
    InstanceId: instance.instanceId,
  },
  period: cdk.Duration.minutes(1),
});

const alarm = new cloudwatch.Alarm(stack, "Alarm", {
  metric,
  threshold: 5,
  evaluationPeriods: 1,
});

alarm.addAlarmAction(new cw_actions.SnsAction(topic));

const snsLineNotify = new SnsNotify(stack, "sns-line-notify", {
  lineNotifyToken: "lineNotifyToken",
});

topic.addSubscription(snsLineNotify.lambdaSubscription);
```

# Deploy

```sh
cdk deploy
```
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

import aws_cdk.aws_sns_subscriptions as _aws_cdk_aws_sns_subscriptions_d19397b0
import aws_cdk.core as _aws_cdk_core_f4b25747


class SnsNotify(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sns-notify.SnsNotify",
):
    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        line_notify_token: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param line_notify_token: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ef0c3b3bf76805aeada37f42068a38876b6fa8f48b269bef3b01d34d394866)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNotifyProps(line_notify_token=line_notify_token)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaSubscription")
    def lambda_subscription(
        self,
    ) -> _aws_cdk_aws_sns_subscriptions_d19397b0.LambdaSubscription:
        return typing.cast(_aws_cdk_aws_sns_subscriptions_d19397b0.LambdaSubscription, jsii.get(self, "lambdaSubscription"))


@jsii.data_type(
    jsii_type="cdk-sns-notify.SnsNotifyProps",
    jsii_struct_bases=[],
    name_mapping={"line_notify_token": "lineNotifyToken"},
)
class SnsNotifyProps:
    def __init__(self, *, line_notify_token: builtins.str) -> None:
        '''
        :param line_notify_token: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c73f21e101155acb1fe58f772cfd374076e38c0dacd52491731e5877d4f9cf)
            check_type(argname="argument line_notify_token", value=line_notify_token, expected_type=type_hints["line_notify_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "line_notify_token": line_notify_token,
        }

    @builtins.property
    def line_notify_token(self) -> builtins.str:
        result = self._values.get("line_notify_token")
        assert result is not None, "Required property 'line_notify_token' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNotifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SnsNotify",
    "SnsNotifyProps",
]

publication.publish()

def _typecheckingstub__b8ef0c3b3bf76805aeada37f42068a38876b6fa8f48b269bef3b01d34d394866(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    line_notify_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c73f21e101155acb1fe58f772cfd374076e38c0dacd52491731e5877d4f9cf(
    *,
    line_notify_token: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

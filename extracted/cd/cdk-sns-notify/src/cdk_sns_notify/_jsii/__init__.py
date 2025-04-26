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

import aws_cdk.aws_cloudwatch._jsii
import aws_cdk.aws_cloudwatch_actions._jsii
import aws_cdk.aws_ec2._jsii
import aws_cdk.aws_iam._jsii
import aws_cdk.aws_lambda._jsii
import aws_cdk.aws_lambda_nodejs._jsii
import aws_cdk.aws_sns._jsii
import aws_cdk.aws_sns_subscriptions._jsii
import aws_cdk.core._jsii
import constructs._jsii

__jsii_assembly__ = jsii.JSIIAssembly.load(
    "cdk-sns-notify", "0.0.948", __name__[0:-6], "cdk-sns-notify@0.0.948.jsii.tgz"
)

__all__ = [
    "__jsii_assembly__",
]

publication.publish()

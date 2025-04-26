'''
# AWS CloudWatch Logs Subscription Destination Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This library contains destinations for AWS CloudWatch Logs SubscriptionFilters. You
can send log data to Kinesis Streams or Lambda Functions.

See the documentation of the `logs` module for more information.
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_0674c215
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_logs as _aws_cdk_aws_logs_6c4320fb
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_logs_6c4320fb.ILogSubscriptionDestination)
class KinesisDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs-destinations.KinesisDestination",
):
    '''Use a Kinesis stream as the destination for a log subscription.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_kinesis as kinesis
        import aws_cdk.aws_logs_destinations as logs_destinations
        
        # role: iam.Role
        # stream: kinesis.Stream
        
        kinesis_destination = logs_destinations.KinesisDestination(stream,
            role=role
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_0674c215.IStream,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param stream: The Kinesis stream to use as destination.
        :param role: The role to assume to write log events to the destination. Default: - A new Role is created
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c1fc1e74b65f4712e89c4da0bc617dea03f0d103b6d5ca34d70a034ee992f15)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisDestinationProps(role=role)

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        _source_log_group: _aws_cdk_aws_logs_6c4320fb.ILogGroup,
    ) -> _aws_cdk_aws_logs_6c4320fb.LogSubscriptionDestinationConfig:
        '''Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param _source_log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c036c7cb7cf460a876c094390792817933a81fdf009c1e122eac612b990bc23d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument _source_log_group", value=_source_log_group, expected_type=type_hints["_source_log_group"])
        return typing.cast(_aws_cdk_aws_logs_6c4320fb.LogSubscriptionDestinationConfig, jsii.invoke(self, "bind", [scope, _source_log_group]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs-destinations.KinesisDestinationProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class KinesisDestinationProps:
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Customize the Kinesis Logs Destination.

        :param role: The role to assume to write log events to the destination. Default: - A new Role is created

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_logs_destinations as logs_destinations
            
            # role: iam.Role
            
            kinesis_destination_props = logs_destinations.KinesisDestinationProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70edd2e2361dad9ce17031d23675b0d1700425bd13f9b6b2318cf360863cc596)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The role to assume to write log events to the destination.

        :default: - A new Role is created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_logs_6c4320fb.ILogSubscriptionDestination)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-logs-destinations.LambdaDestination",
):
    '''Use a Lambda Function as the destination for a log subscription.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_logs_destinations as destinations
        # fn: lambda.Function
        # log_group: logs.LogGroup
        
        
        logs.SubscriptionFilter(self, "Subscription",
            log_group=log_group,
            destination=destinations.LambdaDestination(fn),
            filter_pattern=logs.FilterPattern.all_terms("ERROR", "MainThread")
        )
    '''

    def __init__(
        self,
        fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        add_permissions: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''LambdaDestinationOptions.

        :param fn: -
        :param add_permissions: Whether or not to add Lambda Permissions. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e9710da2f352eb7ad07824e7b66d1ebed3cc7d064cf10765da4b89bba002b6)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        options = LambdaDestinationOptions(add_permissions=add_permissions)

        jsii.create(self.__class__, self, [fn, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        log_group: _aws_cdk_aws_logs_6c4320fb.ILogGroup,
    ) -> _aws_cdk_aws_logs_6c4320fb.LogSubscriptionDestinationConfig:
        '''Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba2efb1140cf6ba20e3f95e28c51159452ea50ab55b1c99c71c674565a2eeaf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(_aws_cdk_aws_logs_6c4320fb.LogSubscriptionDestinationConfig, jsii.invoke(self, "bind", [scope, log_group]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-logs-destinations.LambdaDestinationOptions",
    jsii_struct_bases=[],
    name_mapping={"add_permissions": "addPermissions"},
)
class LambdaDestinationOptions:
    def __init__(
        self,
        *,
        add_permissions: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options that may be provided to LambdaDestination.

        :param add_permissions: Whether or not to add Lambda Permissions. Default: true

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_logs_destinations as logs_destinations
            
            lambda_destination_options = logs_destinations.LambdaDestinationOptions(
                add_permissions=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7123c240d0039fa7cbf58a80b76d5efafce8333f0c03a85148eeaf9ccfce30fc)
            check_type(argname="argument add_permissions", value=add_permissions, expected_type=type_hints["add_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_permissions is not None:
            self._values["add_permissions"] = add_permissions

    @builtins.property
    def add_permissions(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to add Lambda Permissions.

        :default: true
        '''
        result = self._values.get("add_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDestinationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KinesisDestination",
    "KinesisDestinationProps",
    "LambdaDestination",
    "LambdaDestinationOptions",
]

publication.publish()

def _typecheckingstub__4c1fc1e74b65f4712e89c4da0bc617dea03f0d103b6d5ca34d70a034ee992f15(
    stream: _aws_cdk_aws_kinesis_0674c215.IStream,
    *,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c036c7cb7cf460a876c094390792817933a81fdf009c1e122eac612b990bc23d(
    scope: _aws_cdk_core_f4b25747.Construct,
    _source_log_group: _aws_cdk_aws_logs_6c4320fb.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70edd2e2361dad9ce17031d23675b0d1700425bd13f9b6b2318cf360863cc596(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e9710da2f352eb7ad07824e7b66d1ebed3cc7d064cf10765da4b89bba002b6(
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    add_permissions: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba2efb1140cf6ba20e3f95e28c51159452ea50ab55b1c99c71c674565a2eeaf(
    scope: _aws_cdk_core_f4b25747.Construct,
    log_group: _aws_cdk_aws_logs_6c4320fb.ILogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7123c240d0039fa7cbf58a80b76d5efafce8333f0c03a85148eeaf9ccfce30fc(
    *,
    add_permissions: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

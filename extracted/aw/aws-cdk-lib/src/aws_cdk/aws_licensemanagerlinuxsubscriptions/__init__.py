r'''
# AWS::LicenseManagerLinuxSubscriptions Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_licensemanagerlinuxsubscriptions as licensemanagerlinuxsubscriptions
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for LicenseManagerLinuxSubscriptions construct libraries](https://constructs.dev/search?q=licensemanagerlinuxsubscriptions)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::LicenseManagerLinuxSubscriptions resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManagerLinuxSubscriptions.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::LicenseManagerLinuxSubscriptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManagerLinuxSubscriptions.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from .._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_0cae9daa
    import aws_cdk.interfaces.aws_licensemanagerlinuxsubscriptions as _aws_licensemanagerlinuxsubscriptions_72bdf7ae
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_licensemanagerlinuxsubscriptions_72bdf7ae = _LazyImport("aws_cdk.interfaces.aws_licensemanagerlinuxsubscriptions")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_licensemanagerlinuxsubscriptions_72bdf7ae.ISubscriptionProviderRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnSubscriptionProvider(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_licensemanagerlinuxsubscriptions.CfnSubscriptionProvider",
):
    '''Resource Type definition for AWS::LicenseManagerLinuxSubscriptions::SubscriptionProvider.

    Registers a third-party Linux subscription provider so that License Manager can retrieve subscription details for the discovered Linux instances in an account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerlinuxsubscriptions-subscriptionprovider.html
    :cloudformationResource: AWS::LicenseManagerLinuxSubscriptions::SubscriptionProvider
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_licensemanagerlinuxsubscriptions as licensemanagerlinuxsubscriptions
        
        cfn_subscription_provider = licensemanagerlinuxsubscriptions.CfnSubscriptionProvider(self, "MyCfnSubscriptionProvider",
            secret_arn="secretArn",
            subscription_provider_source="subscriptionProviderSource",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        secret_arn: builtins.str,
        subscription_provider_source: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManagerLinuxSubscriptions::SubscriptionProvider``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param secret_arn: The Amazon Resource Name (ARN) of the Secrets Manager secret that contains the access token for the third-party Linux subscription provider.
        :param subscription_provider_source: The Linux subscription provider that the registration is for.
        :param tags: The metadata tags assigned to the registered subscription provider.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a44ae5ca48384cd8cfb4882935ba640bf96ec7d1cd592a79e1e6fe75e5b32886)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionProviderProps(
            secret_arn=secret_arn,
            subscription_provider_source=subscription_provider_source,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSubscriptionProvider")
    @builtins.classmethod
    def arn_for_subscription_provider(
        cls,
        resource: "_aws_licensemanagerlinuxsubscriptions_72bdf7ae.ISubscriptionProviderRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__87c273175f0447e5c0452a142246f9f0a1a3d636664e4bcc291c6fc90c1d48c5)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSubscriptionProvider", [resource]))

    @jsii.member(jsii_name="isCfnSubscriptionProvider")
    @builtins.classmethod
    def is_cfn_subscription_provider(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSubscriptionProvider.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__69a047ab1772884129753ebdebd18a003e07173840e40d5f2a369b9859c3b815)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSubscriptionProvider", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c14cdd63de1abb13b00966be31cddc27342959d2d8df560997c7b950446956cd)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bf682728f1927fb2d64da5e48e4387a16aeca0f66b3ec0f91de45adfa05d7607)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLastSuccessfulDataRetrievalTime")
    def attr_last_successful_data_retrieval_time(self) -> builtins.str:
        '''The timestamp from the last time that License Manager retrieved subscription details from the registered third-party Linux subscription provider.

        :cloudformationAttribute: LastSuccessfulDataRetrievalTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastSuccessfulDataRetrievalTime"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionProviderArn")
    def attr_subscription_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Linux subscription provider resource that you registered.

        :cloudformationAttribute: SubscriptionProviderArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSubscriptionProviderArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionProviderStatus")
    def attr_subscription_provider_status(self) -> builtins.str:
        '''The status of the third-party subscription provider access token from the last subscription data request.

        :cloudformationAttribute: SubscriptionProviderStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSubscriptionProviderStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrSubscriptionProviderStatusMessage")
    def attr_subscription_provider_status_message(self) -> builtins.str:
        '''A message that describes the status of the third-party subscription provider access token.

        :cloudformationAttribute: SubscriptionProviderStatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSubscriptionProviderStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionProviderRef")
    def subscription_provider_ref(
        self,
    ) -> "_aws_licensemanagerlinuxsubscriptions_72bdf7ae.SubscriptionProviderReference":
        '''A reference to a SubscriptionProvider resource.'''
        return typing.cast("_aws_licensemanagerlinuxsubscriptions_72bdf7ae.SubscriptionProviderReference", jsii.get(self, "subscriptionProviderRef"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Secrets Manager secret that contains the access token for the third-party Linux subscription provider.'''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8fbf0a5c1af2f6037b1c66414a2ceb036013c96d3982e260af44c9eebba6da57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionProviderSource")
    def subscription_provider_source(self) -> builtins.str:
        '''The Linux subscription provider that the registration is for.'''
        return typing.cast(builtins.str, jsii.get(self, "subscriptionProviderSource"))

    @subscription_provider_source.setter
    def subscription_provider_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c52ad86981dbe92dca660af842513edd4a58958186c7397a6629b5fa27e297fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionProviderSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The metadata tags assigned to the registered subscription provider.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aeb0fa9de96fb77f7b71ab9ed9d2ab060a3f123974261db456e6c4e4553721ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_licensemanagerlinuxsubscriptions.CfnSubscriptionProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_arn": "secretArn",
        "subscription_provider_source": "subscriptionProviderSource",
        "tags": "tags",
    },
)
class CfnSubscriptionProviderProps:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        subscription_provider_source: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubscriptionProvider``.

        :param secret_arn: The Amazon Resource Name (ARN) of the Secrets Manager secret that contains the access token for the third-party Linux subscription provider.
        :param subscription_provider_source: The Linux subscription provider that the registration is for.
        :param tags: The metadata tags assigned to the registered subscription provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerlinuxsubscriptions-subscriptionprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_licensemanagerlinuxsubscriptions as licensemanagerlinuxsubscriptions
            
            cfn_subscription_provider_props = licensemanagerlinuxsubscriptions.CfnSubscriptionProviderProps(
                secret_arn="secretArn",
                subscription_provider_source="subscriptionProviderSource",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b109a13b6cc28ca3d5924b16b20b2022c544df742414c29d0e386e17c9a7b92d)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument subscription_provider_source", value=subscription_provider_source, expected_type=type_hints["subscription_provider_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "subscription_provider_source": subscription_provider_source,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Secrets Manager secret that contains the access token for the third-party Linux subscription provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerlinuxsubscriptions-subscriptionprovider.html#cfn-licensemanagerlinuxsubscriptions-subscriptionprovider-secretarn
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_provider_source(self) -> builtins.str:
        '''The Linux subscription provider that the registration is for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerlinuxsubscriptions-subscriptionprovider.html#cfn-licensemanagerlinuxsubscriptions-subscriptionprovider-subscriptionprovidersource
        '''
        result = self._values.get("subscription_provider_source")
        assert result is not None, "Required property 'subscription_provider_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The metadata tags assigned to the registered subscription provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerlinuxsubscriptions-subscriptionprovider.html#cfn-licensemanagerlinuxsubscriptions-subscriptionprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSubscriptionProvider",
    "CfnSubscriptionProviderProps",
]

publication.publish()

def _typecheckingstub__a44ae5ca48384cd8cfb4882935ba640bf96ec7d1cd592a79e1e6fe75e5b32886(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret_arn: builtins.str,
    subscription_provider_source: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c273175f0447e5c0452a142246f9f0a1a3d636664e4bcc291c6fc90c1d48c5(
    resource: _aws_licensemanagerlinuxsubscriptions_72bdf7ae.ISubscriptionProviderRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a047ab1772884129753ebdebd18a003e07173840e40d5f2a369b9859c3b815(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14cdd63de1abb13b00966be31cddc27342959d2d8df560997c7b950446956cd(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf682728f1927fb2d64da5e48e4387a16aeca0f66b3ec0f91de45adfa05d7607(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbf0a5c1af2f6037b1c66414a2ceb036013c96d3982e260af44c9eebba6da57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52ad86981dbe92dca660af842513edd4a58958186c7397a6629b5fa27e297fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb0fa9de96fb77f7b71ab9ed9d2ab060a3f123974261db456e6c4e4553721ce(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b109a13b6cc28ca3d5924b16b20b2022c544df742414c29d0e386e17c9a7b92d(
    *,
    secret_arn: builtins.str,
    subscription_provider_source: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

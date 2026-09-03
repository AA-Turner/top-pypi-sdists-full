r'''
# AWS::DRS Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_drs as drs
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DRS construct libraries](https://constructs.dev/search?q=drs)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DRS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DRS.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DRS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DRS.html).

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
    import aws_cdk.interfaces.aws_drs as _aws_drs_f93ad3cc
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_drs_f93ad3cc = _LazyImport("aws_cdk.interfaces.aws_drs")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_drs_f93ad3cc.ISourceNetworkRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnSourceNetwork(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_drs.CfnSourceNetwork",
):
    '''A Source Network resource represents a VPC that is protected by AWS Elastic Disaster Recovery.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html
    :cloudformationResource: AWS::DRS::SourceNetwork
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_drs as drs
        
        cfn_source_network = drs.CfnSourceNetwork(self, "MyCfnSourceNetwork",
            origin_account_id="originAccountId",
            origin_region="originRegion",
            vpc_id="vpcId",
        
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
        origin_account_id: builtins.str,
        origin_region: builtins.str,
        vpc_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DRS::SourceNetwork``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param origin_account_id: The account ID containing the VPC to protect.
        :param origin_region: The region containing the VPC to protect.
        :param vpc_id: The VPC ID to protect.
        :param tags: A set of tags associated with the Source Network.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d97ad57f2522dd0411c6b55ae55d73d746b282dc5d1e831e927a90539c24fd9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSourceNetworkProps(
            origin_account_id=origin_account_id,
            origin_region=origin_region,
            vpc_id=vpc_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForSourceNetwork")
    @builtins.classmethod
    def arn_for_source_network(
        cls,
        resource: "_aws_drs_f93ad3cc.ISourceNetworkRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c05fc634112ac58c78160fc830d41e79942f87c8e226f9bca445eea84d55aec3)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForSourceNetwork", [resource]))

    @jsii.member(jsii_name="isCfnSourceNetwork")
    @builtins.classmethod
    def is_cfn_source_network(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSourceNetwork.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__617565c2120521824646c6e53646bdc8869c274398d52eef3fe38c5d33c46c15)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSourceNetwork", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f77637dd897a244a753e0003c12a01dde9b56b7d772f5cd19fae616409a67b6)
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
            type_hints = cached_type_hints(_typecheckingstub__c7c6ec2fe694506d506546a55e76ad6c986ed9d2bbb34f7cb114c4cbec12022d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the Source Network.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceNetworkId")
    def attr_source_network_id(self) -> builtins.str:
        '''The ID of the Source Network.

        :cloudformationAttribute: SourceNetworkID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceNetworkId"))

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
    @jsii.member(jsii_name="sourceNetworkRef")
    def source_network_ref(self) -> "_aws_drs_f93ad3cc.SourceNetworkReference":
        '''A reference to a SourceNetwork resource.'''
        return typing.cast("_aws_drs_f93ad3cc.SourceNetworkReference", jsii.get(self, "sourceNetworkRef"))

    @builtins.property
    @jsii.member(jsii_name="originAccountId")
    def origin_account_id(self) -> builtins.str:
        '''The account ID containing the VPC to protect.'''
        return typing.cast(builtins.str, jsii.get(self, "originAccountId"))

    @origin_account_id.setter
    def origin_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c72d6d69d5d8da72514116ae9d75a13c86212f82245dc854ea2f277bb8f94fba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="originRegion")
    def origin_region(self) -> builtins.str:
        '''The region containing the VPC to protect.'''
        return typing.cast(builtins.str, jsii.get(self, "originRegion"))

    @origin_region.setter
    def origin_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__68976ddfc0bd35d074c8413345f3cd461035cf818143a1e1e739b68adacfa4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''The VPC ID to protect.'''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ec5656c25085a2061c8f8578569bf7dab822eb4a6fd4f07d214e1b9cf6b77da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags associated with the Source Network.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f459ea64bac22a86b151bf3be9ffe44eb2341eeec168d352034f5a234ae3f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_drs.CfnSourceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "origin_account_id": "originAccountId",
        "origin_region": "originRegion",
        "vpc_id": "vpcId",
        "tags": "tags",
    },
)
class CfnSourceNetworkProps:
    def __init__(
        self,
        *,
        origin_account_id: builtins.str,
        origin_region: builtins.str,
        vpc_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSourceNetwork``.

        :param origin_account_id: The account ID containing the VPC to protect.
        :param origin_region: The region containing the VPC to protect.
        :param vpc_id: The VPC ID to protect.
        :param tags: A set of tags associated with the Source Network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_drs as drs
            
            cfn_source_network_props = drs.CfnSourceNetworkProps(
                origin_account_id="originAccountId",
                origin_region="originRegion",
                vpc_id="vpcId",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f60a1e02b93ca008ca4dd333cf7c4cc38ea03fd8d1bf4b81057a2ce8902533bb)
            check_type(argname="argument origin_account_id", value=origin_account_id, expected_type=type_hints["origin_account_id"])
            check_type(argname="argument origin_region", value=origin_region, expected_type=type_hints["origin_region"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_account_id": origin_account_id,
            "origin_region": origin_region,
            "vpc_id": vpc_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def origin_account_id(self) -> builtins.str:
        '''The account ID containing the VPC to protect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html#cfn-drs-sourcenetwork-originaccountid
        '''
        result = self._values.get("origin_account_id")
        assert result is not None, "Required property 'origin_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_region(self) -> builtins.str:
        '''The region containing the VPC to protect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html#cfn-drs-sourcenetwork-originregion
        '''
        result = self._values.get("origin_region")
        assert result is not None, "Required property 'origin_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The VPC ID to protect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html#cfn-drs-sourcenetwork-vpcid
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags associated with the Source Network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-drs-sourcenetwork.html#cfn-drs-sourcenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSourceNetwork",
    "CfnSourceNetworkProps",
]

publication.publish()

def _typecheckingstub__d97ad57f2522dd0411c6b55ae55d73d746b282dc5d1e831e927a90539c24fd9a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    origin_account_id: builtins.str,
    origin_region: builtins.str,
    vpc_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05fc634112ac58c78160fc830d41e79942f87c8e226f9bca445eea84d55aec3(
    resource: _aws_drs_f93ad3cc.ISourceNetworkRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617565c2120521824646c6e53646bdc8869c274398d52eef3fe38c5d33c46c15(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f77637dd897a244a753e0003c12a01dde9b56b7d772f5cd19fae616409a67b6(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c6ec2fe694506d506546a55e76ad6c986ed9d2bbb34f7cb114c4cbec12022d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72d6d69d5d8da72514116ae9d75a13c86212f82245dc854ea2f277bb8f94fba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68976ddfc0bd35d074c8413345f3cd461035cf818143a1e1e739b68adacfa4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5656c25085a2061c8f8578569bf7dab822eb4a6fd4f07d214e1b9cf6b77da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f459ea64bac22a86b151bf3be9ffe44eb2341eeec168d352034f5a234ae3f32(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60a1e02b93ca008ca4dd333cf7c4cc38ea03fd8d1bf4b81057a2ce8902533bb(
    *,
    origin_account_id: builtins.str,
    origin_region: builtins.str,
    vpc_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

r'''
# AWS::DataExchange Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_dataexchange as dataexchange
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DataExchange construct libraries](https://constructs.dev/search?q=dataexchange)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DataExchange resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataExchange.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DataExchange](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataExchange.html).

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
    import aws_cdk.interfaces.aws_dataexchange as _aws_dataexchange_7cdcf7e6
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_dataexchange_7cdcf7e6 = _LazyImport("aws_cdk.interfaces.aws_dataexchange")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_dataexchange_7cdcf7e6.IEntitledDataSetsRef)
class CfnEntitledDataSets(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_dataexchange.CfnEntitledDataSets",
):
    '''Resource Type definition for AWS::DataExchange::EntitledDataSets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dataexchange-entitleddatasets.html
    :cloudformationResource: AWS::DataExchange::EntitledDataSets
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_dataexchange as dataexchange
        
        cfn_entitled_data_sets = dataexchange.CfnEntitledDataSets(self, "MyCfnEntitledDataSets",
            asset_type="assetType",
            description="description",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        asset_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DataExchange::EntitledDataSets``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param asset_type: 
        :param description: 
        :param name: 
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__64d51c094c129be2c94cc86489d5090490ba199ad66931d3f670cca6d0e4c5a1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEntitledDataSetsProps(
            asset_type=asset_type, description=description, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForEntitledDataSets")
    @builtins.classmethod
    def arn_for_entitled_data_sets(
        cls,
        resource: "_aws_dataexchange_7cdcf7e6.IEntitledDataSetsRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fa5c98928b0a66cff97bd802d09dc87d7f34bdf5bb57b3b3cc313172cd3fbda4)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForEntitledDataSets", [resource]))

    @jsii.member(jsii_name="isCfnEntitledDataSets")
    @builtins.classmethod
    def is_cfn_entitled_data_sets(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnEntitledDataSets.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6c069dc24b9dcd8c90c0e220ac985bd68bbc0a6a606ab6a8277bf59e11242ce2)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnEntitledDataSets", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d7782ae33497505c5c2105b86746a1f2c47706108e0c196dc74b8c59a5106746)
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
            type_hints = cached_type_hints(_typecheckingstub__d2a3c2694e7dac5ea3174d4c8a0a97626d13adf0ed5ecab17af77b310c8ed7a5)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSetId")
    def attr_data_set_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: DataSetId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSetId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrOrigin")
    def attr_origin(self) -> builtins.str:
        '''
        :cloudformationAttribute: Origin
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOrigin"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceId")
    def attr_source_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: SourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="entitledDataSetsRef")
    def entitled_data_sets_ref(
        self,
    ) -> "_aws_dataexchange_7cdcf7e6.EntitledDataSetsReference":
        '''A reference to a EntitledDataSets resource.'''
        return typing.cast("_aws_dataexchange_7cdcf7e6.EntitledDataSetsReference", jsii.get(self, "entitledDataSetsRef"))

    @builtins.property
    @jsii.member(jsii_name="assetType")
    def asset_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetType"))

    @asset_type.setter
    def asset_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__362a2bb902ad1896064e1c73ade9c2fa9f1ddc29b73332e0f503317e6e46d2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b52225792bfacfb50b93fc4b57b2cbb033a288fcf5845b834f55e068039c92c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8a4b02439386bbe03a82177236e6c267166116805bf86abb38373257714504bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_dataexchange.CfnEntitledDataSetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_type": "assetType",
        "description": "description",
        "name": "name",
    },
)
class CfnEntitledDataSetsProps:
    def __init__(
        self,
        *,
        asset_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEntitledDataSets``.

        :param asset_type: 
        :param description: 
        :param name: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dataexchange-entitleddatasets.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_dataexchange as dataexchange
            
            cfn_entitled_data_sets_props = dataexchange.CfnEntitledDataSetsProps(
                asset_type="assetType",
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dca2eeadf7fc78874b200a5af92e848c21592515c12223b950e669531066fc3f)
            check_type(argname="argument asset_type", value=asset_type, expected_type=type_hints["asset_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_type is not None:
            self._values["asset_type"] = asset_type
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def asset_type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dataexchange-entitleddatasets.html#cfn-dataexchange-entitleddatasets-assettype
        '''
        result = self._values.get("asset_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dataexchange-entitleddatasets.html#cfn-dataexchange-entitleddatasets-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dataexchange-entitleddatasets.html#cfn-dataexchange-entitleddatasets-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntitledDataSetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnEntitledDataSets",
    "CfnEntitledDataSetsProps",
]

publication.publish()

def _typecheckingstub__64d51c094c129be2c94cc86489d5090490ba199ad66931d3f670cca6d0e4c5a1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    asset_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5c98928b0a66cff97bd802d09dc87d7f34bdf5bb57b3b3cc313172cd3fbda4(
    resource: _aws_dataexchange_7cdcf7e6.IEntitledDataSetsRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c069dc24b9dcd8c90c0e220ac985bd68bbc0a6a606ab6a8277bf59e11242ce2(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7782ae33497505c5c2105b86746a1f2c47706108e0c196dc74b8c59a5106746(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a3c2694e7dac5ea3174d4c8a0a97626d13adf0ed5ecab17af77b310c8ed7a5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362a2bb902ad1896064e1c73ade9c2fa9f1ddc29b73332e0f503317e6e46d2f2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52225792bfacfb50b93fc4b57b2cbb033a288fcf5845b834f55e068039c92c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4b02439386bbe03a82177236e6c267166116805bf86abb38373257714504bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca2eeadf7fc78874b200a5af92e848c21592515c12223b950e669531066fc3f(
    *,
    asset_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

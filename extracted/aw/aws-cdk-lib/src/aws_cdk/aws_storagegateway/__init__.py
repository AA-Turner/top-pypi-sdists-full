r'''
# AWS::StorageGateway Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_storagegateway as storagegateway
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for StorageGateway construct libraries](https://constructs.dev/search?q=storagegateway)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::StorageGateway resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_StorageGateway.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::StorageGateway](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_StorageGateway.html).

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
    import aws_cdk.interfaces.aws_storagegateway as _aws_storagegateway_f426d4c4
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_storagegateway_f426d4c4 = _LazyImport("aws_cdk.interfaces.aws_storagegateway")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_storagegateway_f426d4c4.ITapePoolRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnTapePool(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTapePool",
):
    '''Creates a custom tape pool for archiving virtual tapes with optional retention lock.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html
    :cloudformationResource: AWS::StorageGateway::TapePool
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_storagegateway as storagegateway
        
        cfn_tape_pool = storagegateway.CfnTapePool(self, "MyCfnTapePool",
            pool_name="poolName",
            storage_class="storageClass",
        
            # the properties below are optional
            retention_lock_time_in_days=123,
            retention_lock_type="retentionLockType",
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
        pool_name: builtins.str,
        storage_class: builtins.str,
        retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
        retention_lock_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::StorageGateway::TapePool``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param pool_name: The name of the custom tape pool.
        :param storage_class: The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).
        :param retention_lock_time_in_days: Tape retention lock time in days (up to 36,500 days / 100 years).
        :param retention_lock_type: Tape retention lock type. Governance mode allows authorized removal; compliance mode prevents all removal.
        :param tags: A list of up to 50 tags for the tape pool.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ac2c1692ba4edccb604aef75af4b88463d090c7db3c8f08741d200a884adedac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTapePoolProps(
            pool_name=pool_name,
            storage_class=storage_class,
            retention_lock_time_in_days=retention_lock_time_in_days,
            retention_lock_type=retention_lock_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForTapePool")
    @builtins.classmethod
    def arn_for_tape_pool(
        cls,
        resource: "_aws_storagegateway_f426d4c4.ITapePoolRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3bdaa23426ff87911afa19f9997f4ea57420c29c61fc1892987875628fdf638b)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForTapePool", [resource]))

    @jsii.member(jsii_name="fromPoolId")
    @builtins.classmethod
    def from_pool_id(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        pool_id: builtins.str,
    ) -> "_aws_storagegateway_f426d4c4.ITapePoolRef":
        '''Creates a new ITapePoolRef from a poolId.

        :param scope: -
        :param id: -
        :param pool_id: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8b4c436c83b9aad89b0f338e63d3ef15cdc1d6880fa6e5c24369f59ab7d5e34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pool_id", value=pool_id, expected_type=type_hints["pool_id"])
        return typing.cast("_aws_storagegateway_f426d4c4.ITapePoolRef", jsii.sinvoke(cls, "fromPoolId", [scope, id, pool_id]))

    @jsii.member(jsii_name="isCfnTapePool")
    @builtins.classmethod
    def is_cfn_tape_pool(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnTapePool.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f4ac6b6ba23515dcc27d4c5a84961fe7a159a83305f9188d9b81d341eac359a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnTapePool", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb3a41212781376c4f3874b92a3aeae3808be50104fb587f50096ee25d9cbdfe)
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
            type_hints = cached_type_hints(_typecheckingstub__9a89e9380fc69f21f542d0c5d15978f09dbb5fc7563f2badbf156059dafb2775)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolArn")
    def attr_pool_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the custom tape pool.

        :cloudformationAttribute: PoolARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPoolId")
    def attr_pool_id(self) -> builtins.str:
        '''The unique identifier of the custom tape pool, extracted from the ARN.

        :cloudformationAttribute: PoolId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPoolId"))

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
    @jsii.member(jsii_name="tapePoolRef")
    def tape_pool_ref(self) -> "_aws_storagegateway_f426d4c4.TapePoolReference":
        '''A reference to a TapePool resource.'''
        return typing.cast("_aws_storagegateway_f426d4c4.TapePoolReference", jsii.get(self, "tapePoolRef"))

    @builtins.property
    @jsii.member(jsii_name="poolName")
    def pool_name(self) -> builtins.str:
        '''The name of the custom tape pool.'''
        return typing.cast(builtins.str, jsii.get(self, "poolName"))

    @pool_name.setter
    def pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e2aa2850a80df094617446432f9ff1341cc436487f9fdcde124fff6e23224b3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageClass")
    def storage_class(self) -> builtins.str:
        '''The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).'''
        return typing.cast(builtins.str, jsii.get(self, "storageClass"))

    @storage_class.setter
    def storage_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__59e6b638819f00096b40770703546150877b22e670bd72107418a00ab661a3c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionLockTimeInDays")
    def retention_lock_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Tape retention lock time in days (up to 36,500 days / 100 years).'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionLockTimeInDays"))

    @retention_lock_time_in_days.setter
    def retention_lock_time_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f9a75e037e394e1a483c9c37c628c1a3fd5236ed311d296563d7c92ed300cf84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionLockTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionLockType")
    def retention_lock_type(self) -> typing.Optional[builtins.str]:
        '''Tape retention lock type.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionLockType"))

    @retention_lock_type.setter
    def retention_lock_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4607d71dfda14f2f335c62ade52d5f18924d070d446cf3004dcb39ec784be160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionLockType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags for the tape pool.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3795fcc974a44ec324d8e597cdf4de7162f69066e260ed1f4273fc3bc7275cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_storagegateway.CfnTapePoolProps",
    jsii_struct_bases=[],
    name_mapping={
        "pool_name": "poolName",
        "storage_class": "storageClass",
        "retention_lock_time_in_days": "retentionLockTimeInDays",
        "retention_lock_type": "retentionLockType",
        "tags": "tags",
    },
)
class CfnTapePoolProps:
    def __init__(
        self,
        *,
        pool_name: builtins.str,
        storage_class: builtins.str,
        retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
        retention_lock_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTapePool``.

        :param pool_name: The name of the custom tape pool.
        :param storage_class: The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).
        :param retention_lock_time_in_days: Tape retention lock time in days (up to 36,500 days / 100 years).
        :param retention_lock_type: Tape retention lock type. Governance mode allows authorized removal; compliance mode prevents all removal.
        :param tags: A list of up to 50 tags for the tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_storagegateway as storagegateway
            
            cfn_tape_pool_props = storagegateway.CfnTapePoolProps(
                pool_name="poolName",
                storage_class="storageClass",
            
                # the properties below are optional
                retention_lock_time_in_days=123,
                retention_lock_type="retentionLockType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__313c929df3254bd85bbd9d06cbd71bce8cccb516d3867f49894385585d8f30e9)
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            check_type(argname="argument retention_lock_time_in_days", value=retention_lock_time_in_days, expected_type=type_hints["retention_lock_time_in_days"])
            check_type(argname="argument retention_lock_type", value=retention_lock_type, expected_type=type_hints["retention_lock_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pool_name": pool_name,
            "storage_class": storage_class,
        }
        if retention_lock_time_in_days is not None:
            self._values["retention_lock_time_in_days"] = retention_lock_time_in_days
        if retention_lock_type is not None:
            self._values["retention_lock_type"] = retention_lock_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def pool_name(self) -> builtins.str:
        '''The name of the custom tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-poolname
        '''
        result = self._values.get("pool_name")
        assert result is not None, "Required property 'pool_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_class(self) -> builtins.str:
        '''The storage class associated with the custom pool (S3 Glacier or S3 Glacier Deep Archive).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-storageclass
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_lock_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Tape retention lock time in days (up to 36,500 days / 100 years).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-retentionlocktimeindays
        '''
        result = self._values.get("retention_lock_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_lock_type(self) -> typing.Optional[builtins.str]:
        '''Tape retention lock type.

        Governance mode allows authorized removal; compliance mode prevents all removal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-retentionlocktype
        '''
        result = self._values.get("retention_lock_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A list of up to 50 tags for the tape pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-storagegateway-tapepool.html#cfn-storagegateway-tapepool-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTapePoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnTapePool",
    "CfnTapePoolProps",
]

publication.publish()

def _typecheckingstub__ac2c1692ba4edccb604aef75af4b88463d090c7db3c8f08741d200a884adedac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    pool_name: builtins.str,
    storage_class: builtins.str,
    retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
    retention_lock_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdaa23426ff87911afa19f9997f4ea57420c29c61fc1892987875628fdf638b(
    resource: _aws_storagegateway_f426d4c4.ITapePoolRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b4c436c83b9aad89b0f338e63d3ef15cdc1d6880fa6e5c24369f59ab7d5e34(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4ac6b6ba23515dcc27d4c5a84961fe7a159a83305f9188d9b81d341eac359a(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3a41212781376c4f3874b92a3aeae3808be50104fb587f50096ee25d9cbdfe(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a89e9380fc69f21f542d0c5d15978f09dbb5fc7563f2badbf156059dafb2775(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2aa2850a80df094617446432f9ff1341cc436487f9fdcde124fff6e23224b3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e6b638819f00096b40770703546150877b22e670bd72107418a00ab661a3c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a75e037e394e1a483c9c37c628c1a3fd5236ed311d296563d7c92ed300cf84(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4607d71dfda14f2f335c62ade52d5f18924d070d446cf3004dcb39ec784be160(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3795fcc974a44ec324d8e597cdf4de7162f69066e260ed1f4273fc3bc7275cc1(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313c929df3254bd85bbd9d06cbd71bce8cccb516d3867f49894385585d8f30e9(
    *,
    pool_name: builtins.str,
    storage_class: builtins.str,
    retention_lock_time_in_days: typing.Optional[jsii.Number] = None,
    retention_lock_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

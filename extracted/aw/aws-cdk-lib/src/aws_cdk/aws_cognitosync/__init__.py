r'''
# AWS::CognitoSync Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_cognitosync as cognitosync
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for CognitoSync construct libraries](https://constructs.dev/search?q=cognitosync)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::CognitoSync resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CognitoSync.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::CognitoSync](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_CognitoSync.html).

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
    import aws_cdk.interfaces.aws_cognitosync as _aws_cognitosync_601422b8
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_cognitosync_601422b8 = _LazyImport("aws_cdk.interfaces.aws_cognitosync")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_cognitosync_601422b8.IDatasetRef)
class CfnDataset(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_cognitosync.CfnDataset",
):
    '''Resource type definition for a Cognito Sync Dataset.

    A dataset is a collection of key-value pairs per identity that can store up to 1 MB of data and sync across devices.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognitosync-dataset.html
    :cloudformationResource: AWS::CognitoSync::Dataset
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_cognitosync as cognitosync
        
        cfn_dataset = cognitosync.CfnDataset(self, "MyCfnDataset",
            dataset_name="datasetName",
            identity_id="identityId",
            identity_pool_id="identityPoolId"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        dataset_name: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CognitoSync::Dataset``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param dataset_name: A string of up to 128 characters. Allowed characters are a-z, A-Z, 0-9, underscore, dash, and dot.
        :param identity_id: A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.
        :param identity_pool_id: A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__908b4ff1be6d798c03a00d23ccacf30f8bf4a197002b2ea1af4f729a80cb0437)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatasetProps(
            dataset_name=dataset_name,
            identity_id=identity_id,
            identity_pool_id=identity_pool_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForDataset")
    @builtins.classmethod
    def arn_for_dataset(
        cls,
        resource: "_aws_cognitosync_601422b8.IDatasetRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__52b718b32ace0e0df9d675805147ce381b901227f7caa3be2e068513355317fa)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForDataset", [resource]))

    @jsii.member(jsii_name="isCfnDataset")
    @builtins.classmethod
    def is_cfn_dataset(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnDataset.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c3ce740f3af585db1f46c0d685adc1b74400754f70c29c80d54d5e02dc5b0a90)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnDataset", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__551928de9e453c6c674667a6aee04f19fb8597b6471d54d135350b7787ce1f63)
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
            type_hints = cached_type_hints(_typecheckingstub__d0880cbddb56ef6c8487f22e85a636b99cc9f6b2dd3fceec7fed79578942b369)
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
        '''The Amazon Resource Name (ARN) of the dataset.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        '''Date on which the dataset was created.

        :cloudformationAttribute: CreationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrDataStorage")
    def attr_data_storage(self) -> jsii.Number:
        '''Total size in bytes of the records in this dataset.

        :cloudformationAttribute: DataStorage
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrDataStorage"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModifiedBy")
    def attr_last_modified_by(self) -> builtins.str:
        '''The device that made the last change to this dataset.

        :cloudformationAttribute: LastModifiedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModifiedBy"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModifiedDate")
    def attr_last_modified_date(self) -> builtins.str:
        '''Date when the dataset was last modified.

        :cloudformationAttribute: LastModifiedDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModifiedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrNumRecords")
    def attr_num_records(self) -> jsii.Number:
        '''Number of records in this dataset.

        :cloudformationAttribute: NumRecords
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrNumRecords"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="datasetRef")
    def dataset_ref(self) -> "_aws_cognitosync_601422b8.DatasetReference":
        '''A reference to a Dataset resource.'''
        return typing.cast("_aws_cognitosync_601422b8.DatasetReference", jsii.get(self, "datasetRef"))

    @builtins.property
    @jsii.member(jsii_name="datasetName")
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''A string of up to 128 characters.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetName"))

    @dataset_name.setter
    def dataset_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fba289548a336f0df310d0a6178fc0fe5ffa3eea52916484cbb05c05396a01b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityId")
    def identity_id(self) -> typing.Optional[builtins.str]:
        '''A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityId"))

    @identity_id.setter
    def identity_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__75791287d88143c451c03ca9bcccefb5bf91bebb4ec625e623aeb63fa0fdff42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        '''A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityPoolId"))

    @identity_pool_id.setter
    def identity_pool_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__033ef60fb52107f7abe8edfd8a351c3f83d9f378931f82248cb72526d093c138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityPoolId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_cognitosync.CfnDatasetProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_name": "datasetName",
        "identity_id": "identityId",
        "identity_pool_id": "identityPoolId",
    },
)
class CfnDatasetProps:
    def __init__(
        self,
        *,
        dataset_name: typing.Optional[builtins.str] = None,
        identity_id: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataset``.

        :param dataset_name: A string of up to 128 characters. Allowed characters are a-z, A-Z, 0-9, underscore, dash, and dot.
        :param identity_id: A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.
        :param identity_pool_id: A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognitosync-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_cognitosync as cognitosync
            
            cfn_dataset_props = cognitosync.CfnDatasetProps(
                dataset_name="datasetName",
                identity_id="identityId",
                identity_pool_id="identityPoolId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__84604b05249153efc7b77635ed4af2328d3e5135500e580a94cbabee532fa326)
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument identity_id", value=identity_id, expected_type=type_hints["identity_id"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if identity_id is not None:
            self._values["identity_id"] = identity_id
        if identity_pool_id is not None:
            self._values["identity_pool_id"] = identity_pool_id

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''A string of up to 128 characters.

        Allowed characters are a-z, A-Z, 0-9, underscore, dash, and dot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognitosync-dataset.html#cfn-cognitosync-dataset-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_id(self) -> typing.Optional[builtins.str]:
        '''A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognitosync-dataset.html#cfn-cognitosync-dataset-identityid
        '''
        result = self._values.get("identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        '''A name-spaced GUID (for example, us-east-1:23EC4050-6AEA-7089-A2DD-08002EXAMPLE) created by Amazon Cognito.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognitosync-dataset.html#cfn-cognitosync-dataset-identitypoolid
        '''
        result = self._values.get("identity_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataset",
    "CfnDatasetProps",
]

publication.publish()

def _typecheckingstub__908b4ff1be6d798c03a00d23ccacf30f8bf4a197002b2ea1af4f729a80cb0437(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dataset_name: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b718b32ace0e0df9d675805147ce381b901227f7caa3be2e068513355317fa(
    resource: _aws_cognitosync_601422b8.IDatasetRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ce740f3af585db1f46c0d685adc1b74400754f70c29c80d54d5e02dc5b0a90(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551928de9e453c6c674667a6aee04f19fb8597b6471d54d135350b7787ce1f63(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0880cbddb56ef6c8487f22e85a636b99cc9f6b2dd3fceec7fed79578942b369(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba289548a336f0df310d0a6178fc0fe5ffa3eea52916484cbb05c05396a01b4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75791287d88143c451c03ca9bcccefb5bf91bebb4ec625e623aeb63fa0fdff42(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033ef60fb52107f7abe8edfd8a351c3f83d9f378931f82248cb72526d093c138(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84604b05249153efc7b77635ed4af2328d3e5135500e580a94cbabee532fa326(
    *,
    dataset_name: typing.Optional[builtins.str] = None,
    identity_id: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

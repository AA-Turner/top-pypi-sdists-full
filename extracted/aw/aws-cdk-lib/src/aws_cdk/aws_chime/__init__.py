r'''
# AWS::Chime Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_chime as chime
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Chime construct libraries](https://constructs.dev/search?q=chime)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Chime resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Chime.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Chime](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Chime.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_9df397a6,
    CfnTag as _CfnTag_f6864754,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    ITaggableV2 as _ITaggableV2_4e6798f8,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)
from ..interfaces.aws_chime import (
    AppInstanceReference as _AppInstanceReference_8414b2a0,
    IAppInstanceRef as _IAppInstanceRef_43d18bab,
)


@jsii.implements(_IInspectable_c2943556, _IAppInstanceRef_43d18bab, _ITaggableV2_4e6798f8)
class CfnAppInstance(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstance",
):
    '''Resource Type definition for AWS::Chime::AppInstance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html
    :cloudformationResource: AWS::Chime::AppInstance
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_chime as chime
        
        cfn_app_instance = chime.CfnAppInstance(self, "MyCfnAppInstance",
            name="name",
        
            # the properties below are optional
            metadata="metadata",
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
        name: builtins.str,
        metadata: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Chime::AppInstance``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the AppInstance.
        :param metadata: The metadata of the AppInstance. Limited to a 1KB string in UTF-8.
        :param tags: Tags assigned to the AppInstance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d337d6c149cc789c0b6f05ba4ba90f831464295606b004354b7815daaed0c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppInstanceProps(name=name, metadata=metadata, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAppInstance")
    @builtins.classmethod
    def arn_for_app_instance(
        cls,
        resource: "_IAppInstanceRef_43d18bab",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f74b0e7014ea5c23e28103a5fb5867813697fd8201279c330a3aa769bc126a1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAppInstance", [resource]))

    @jsii.member(jsii_name="isCfnAppInstance")
    @builtins.classmethod
    def is_cfn_app_instance(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAppInstance.

        :param x: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a664656abafe2adc6e2a0a9db5e06dc33b5b3b6a0fa2a5ca0b61b7b95d0c32)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAppInstance", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_TreeInspector_488e0dd5") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400a60274a57ac76d314b93fb263163beba6942cc730e90588d6f74e739f4eb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4ccf5db0f869956272a9d89ee82b1cfb49e2aacbbc94b43a595151f8b37e60)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceRef")
    def app_instance_ref(self) -> "_AppInstanceReference_8414b2a0":
        '''A reference to a AppInstance resource.'''
        return typing.cast("_AppInstanceReference_8414b2a0", jsii.get(self, "appInstanceRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAppInstanceArn")
    def attr_app_instance_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the AppInstance.

        :cloudformationAttribute: AppInstanceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppInstanceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTimestamp")
    def attr_created_timestamp(self) -> "_IResolvable_da3f097b":
        '''The time at which an AppInstance was created.

        In epoch milliseconds.

        :cloudformationAttribute: CreatedTimestamp
        '''
        return typing.cast("_IResolvable_da3f097b", jsii.get(self, "attrCreatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTimestamp")
    def attr_last_updated_timestamp(self) -> "_IResolvable_da3f097b":
        '''The time an AppInstance was last updated.

        In epoch milliseconds.

        :cloudformationAttribute: LastUpdatedTimestamp
        '''
        return typing.cast("_IResolvable_da3f097b", jsii.get(self, "attrLastUpdatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_TagManager_0a598cb3":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_TagManager_0a598cb3", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the AppInstance.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72de3b84f85f89b400c53dced98e7828184761f13429f1028134b5727fe38e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the AppInstance.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d28a89759474ddf9cf296e1da1bbf9afe7e7c1413d9a4d175db15deaca419f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the AppInstance.'''
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["_CfnTag_f6864754"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc357af54a794ca273668787f93dac3a63d2f85c8108d86aa56926b60d6aac5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "metadata": "metadata", "tags": "tags"},
)
class CfnAppInstanceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        metadata: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_CfnTag_f6864754", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAppInstance``.

        :param name: The name of the AppInstance.
        :param metadata: The metadata of the AppInstance. Limited to a 1KB string in UTF-8.
        :param tags: Tags assigned to the AppInstance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_chime as chime
            
            cfn_app_instance_props = chime.CfnAppInstanceProps(
                name="name",
            
                # the properties below are optional
                metadata="metadata",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551f6928f9d6a158547ebe3a9d4b368b45ad66d983bfb330b063b77c078ca90e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the AppInstance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html#cfn-chime-appinstance-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the AppInstance.

        Limited to a 1KB string in UTF-8.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html#cfn-chime-appinstance-metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_CfnTag_f6864754"]]:
        '''Tags assigned to the AppInstance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html#cfn-chime-appinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_CfnTag_f6864754"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAppInstance",
    "CfnAppInstanceProps",
]

publication.publish()

def _typecheckingstub__6d337d6c149cc789c0b6f05ba4ba90f831464295606b004354b7815daaed0c77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    metadata: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f74b0e7014ea5c23e28103a5fb5867813697fd8201279c330a3aa769bc126a1(
    resource: _IAppInstanceRef_43d18bab,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a664656abafe2adc6e2a0a9db5e06dc33b5b3b6a0fa2a5ca0b61b7b95d0c32(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400a60274a57ac76d314b93fb263163beba6942cc730e90588d6f74e739f4eb0(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4ccf5db0f869956272a9d89ee82b1cfb49e2aacbbc94b43a595151f8b37e60(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72de3b84f85f89b400c53dced98e7828184761f13429f1028134b5727fe38e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d28a89759474ddf9cf296e1da1bbf9afe7e7c1413d9a4d175db15deaca419f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc357af54a794ca273668787f93dac3a63d2f85c8108d86aa56926b60d6aac5a(
    value: typing.Optional[typing.List[_CfnTag_f6864754]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551f6928f9d6a158547ebe3a9d4b368b45ad66d983bfb330b063b77c078ca90e(
    *,
    name: builtins.str,
    metadata: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

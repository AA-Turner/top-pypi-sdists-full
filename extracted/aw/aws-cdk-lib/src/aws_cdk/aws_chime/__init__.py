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
    import aws_cdk.interfaces.aws_chime as _aws_chime_58870695
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_chime_58870695 = _LazyImport("aws_cdk.interfaces.aws_chime")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_chime_58870695.IAppInstanceRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnAppInstance(
    _aws_cdk_0cae9daa.CfnResource,
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
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Chime::AppInstance``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the AppInstance.
        :param metadata: The metadata of the AppInstance. Limited to a 1KB string in UTF-8.
        :param tags: Tags assigned to the AppInstance.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6d337d6c149cc789c0b6f05ba4ba90f831464295606b004354b7815daaed0c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppInstanceProps(name=name, metadata=metadata, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAppInstance")
    @builtins.classmethod
    def arn_for_app_instance(
        cls,
        resource: "_aws_chime_58870695.IAppInstanceRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f74b0e7014ea5c23e28103a5fb5867813697fd8201279c330a3aa769bc126a1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAppInstance", [resource]))

    @jsii.member(jsii_name="isCfnAppInstance")
    @builtins.classmethod
    def is_cfn_app_instance(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAppInstance.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c0a664656abafe2adc6e2a0a9db5e06dc33b5b3b6a0fa2a5ca0b61b7b95d0c32)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAppInstance", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__400a60274a57ac76d314b93fb263163beba6942cc730e90588d6f74e739f4eb0)
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
            type_hints = cached_type_hints(_typecheckingstub__9c4ccf5db0f869956272a9d89ee82b1cfb49e2aacbbc94b43a595151f8b37e60)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceRef")
    def app_instance_ref(self) -> "_aws_chime_58870695.AppInstanceReference":
        '''A reference to a AppInstance resource.'''
        return typing.cast("_aws_chime_58870695.AppInstanceReference", jsii.get(self, "appInstanceRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAppInstanceArn")
    def attr_app_instance_arn(self) -> builtins.str:
        '''The Amazon Resource Number (ARN) of the AppInstance.

        :cloudformationAttribute: AppInstanceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppInstanceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTimestamp")
    def attr_created_timestamp(self) -> builtins.str:
        '''The time at which an AppInstance was created, as an ISO 8601 timestamp.

        :cloudformationAttribute: CreatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTimestamp")
    def attr_last_updated_timestamp(self) -> builtins.str:
        '''The time an AppInstance was last updated, as an ISO 8601 timestamp.

        :cloudformationAttribute: LastUpdatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTimestamp"))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the AppInstance.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b72de3b84f85f89b400c53dced98e7828184761f13429f1028134b5727fe38e7)
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
            type_hints = cached_type_hints(_typecheckingstub__a4d28a89759474ddf9cf296e1da1bbf9afe7e7c1413d9a4d175db15deaca419f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the AppInstance.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dc357af54a794ca273668787f93dac3a63d2f85c8108d86aa56926b60d6aac5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_chime_58870695.IAppInstanceBotRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnAppInstanceBot(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceBot",
):
    '''Resource Type definition for AWS::Chime::AppInstanceBot.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html
    :cloudformationResource: AWS::Chime::AppInstanceBot
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_chime as chime
        
        cfn_app_instance_bot = chime.CfnAppInstanceBot(self, "MyCfnAppInstanceBot",
            app_instance_arn="appInstanceArn",
            configuration=chime.CfnAppInstanceBot.ConfigurationProperty(
                lex=chime.CfnAppInstanceBot.LexConfigurationProperty(
                    lex_bot_alias_arn="lexBotAliasArn",
                    locale_id="localeId",
        
                    # the properties below are optional
                    invoked_by=chime.CfnAppInstanceBot.InvokedByProperty(
                        standard_messages="standardMessages",
                        targeted_messages="targetedMessages"
                    ),
                    responds_to="respondsTo",
                    welcome_intent="welcomeIntent"
                )
            ),
        
            # the properties below are optional
            metadata="metadata",
            name="name",
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
        app_instance_arn: builtins.str,
        configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceBot.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Chime::AppInstanceBot``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param app_instance_arn: The ARN of the AppInstance.
        :param configuration: A structure that contains configuration data.
        :param metadata: The metadata of the AppInstanceBot.
        :param name: The name of the AppInstanceBot.
        :param tags: The tags assigned to the AppInstanceBot.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fca75944f6ceb69180d3b0f352517267777aeee7ffaa12b2f1a465cf9b6a3e00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppInstanceBotProps(
            app_instance_arn=app_instance_arn,
            configuration=configuration,
            metadata=metadata,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAppInstanceBot")
    @builtins.classmethod
    def arn_for_app_instance_bot(
        cls,
        resource: "_aws_chime_58870695.IAppInstanceBotRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__49c5faf3dcf2887594ff746db96b49d9757db79f86e9d6f358d9f275ee8c8210)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAppInstanceBot", [resource]))

    @jsii.member(jsii_name="isCfnAppInstanceBot")
    @builtins.classmethod
    def is_cfn_app_instance_bot(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAppInstanceBot.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0255372b69a195b0351367c082f9533519223c17e242b93716f61ed8e55dea62)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAppInstanceBot", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__427e24f474e9d78b560301eb631ab4ec523303c4565f63f29c83299fe5abafb1)
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
            type_hints = cached_type_hints(_typecheckingstub__d0f31284f1d604da54c34b53acb2ff3863b786fb7370f15d19da68df814cd8ad)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceBotRef")
    def app_instance_bot_ref(self) -> "_aws_chime_58870695.AppInstanceBotReference":
        '''A reference to a AppInstanceBot resource.'''
        return typing.cast("_aws_chime_58870695.AppInstanceBotReference", jsii.get(self, "appInstanceBotRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAppInstanceBotArn")
    def attr_app_instance_bot_arn(self) -> builtins.str:
        '''The ARN of the AppInstanceBot.

        :cloudformationAttribute: AppInstanceBotArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppInstanceBotArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTimestamp")
    def attr_created_timestamp(self) -> builtins.str:
        '''The time at which the AppInstanceBot was created, as an ISO 8601 timestamp.

        :cloudformationAttribute: CreatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTimestamp")
    def attr_last_updated_timestamp(self) -> builtins.str:
        '''The time at which the AppInstanceBot was last updated, as an ISO 8601 timestamp.

        :cloudformationAttribute: LastUpdatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTimestamp"))

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
    @jsii.member(jsii_name="appInstanceArn")
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the AppInstance.'''
        return typing.cast(builtins.str, jsii.get(self, "appInstanceArn"))

    @app_instance_arn.setter
    def app_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__13a53900f75f263ec868d4efe44340a9273169b155a8e54a68fe8cde3818baec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.ConfigurationProperty"]:
        '''A structure that contains configuration data.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.ConfigurationProperty"], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.ConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d36a14f99ec95cd590d6c1757bb41c8b9235cf6b317fa73e6692074ed033195a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the AppInstanceBot.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__45024baca15a880d713b7458c08c15471a9b4b4bc485fcaa496535c2d75a30a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AppInstanceBot.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__13ad6a83eab879d92eb2609e2f37735b3c2383bb2e7e24c6cefbec192e42c39e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags assigned to the AppInstanceBot.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d87e45b7d9459784717058ca252a094c146e5656ea14d9da51f1cf05f4aa56d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceBot.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"lex": "lex"},
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            lex: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceBot.LexConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A structure that contains configuration data.

            :param lex: The configuration for an Amazon Lex V2 bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                configuration_property = chime.CfnAppInstanceBot.ConfigurationProperty(
                    lex=chime.CfnAppInstanceBot.LexConfigurationProperty(
                        lex_bot_alias_arn="lexBotAliasArn",
                        locale_id="localeId",
                
                        # the properties below are optional
                        invoked_by=chime.CfnAppInstanceBot.InvokedByProperty(
                            standard_messages="standardMessages",
                            targeted_messages="targetedMessages"
                        ),
                        responds_to="respondsTo",
                        welcome_intent="welcomeIntent"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__09ff343ee28319a719419e7819c467b339964da524abd8a8f50f44edd43b11a8)
                check_type(argname="argument lex", value=lex, expected_type=type_hints["lex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lex": lex,
            }

        @builtins.property
        def lex(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.LexConfigurationProperty"]:
            '''The configuration for an Amazon Lex V2 bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-configuration.html#cfn-chime-appinstancebot-configuration-lex
            '''
            result = self._values.get("lex")
            assert result is not None, "Required property 'lex' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.LexConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceBot.InvokedByProperty",
        jsii_struct_bases=[],
        name_mapping={
            "standard_messages": "standardMessages",
            "targeted_messages": "targetedMessages",
        },
    )
    class InvokedByProperty:
        def __init__(
            self,
            *,
            standard_messages: builtins.str,
            targeted_messages: builtins.str,
        ) -> None:
            '''Specifies the type of message that triggers a bot.

            :param standard_messages: Sets standard messages as the bot trigger.
            :param targeted_messages: Sets targeted messages as the bot trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-invokedby.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                invoked_by_property = chime.CfnAppInstanceBot.InvokedByProperty(
                    standard_messages="standardMessages",
                    targeted_messages="targetedMessages"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e0a8291bb53d368f6b1012fdd17317226c377241787e7d74d9371e641c527be4)
                check_type(argname="argument standard_messages", value=standard_messages, expected_type=type_hints["standard_messages"])
                check_type(argname="argument targeted_messages", value=targeted_messages, expected_type=type_hints["targeted_messages"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "standard_messages": standard_messages,
                "targeted_messages": targeted_messages,
            }

        @builtins.property
        def standard_messages(self) -> builtins.str:
            '''Sets standard messages as the bot trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-invokedby.html#cfn-chime-appinstancebot-invokedby-standardmessages
            '''
            result = self._values.get("standard_messages")
            assert result is not None, "Required property 'standard_messages' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def targeted_messages(self) -> builtins.str:
            '''Sets targeted messages as the bot trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-invokedby.html#cfn-chime-appinstancebot-invokedby-targetedmessages
            '''
            result = self._values.get("targeted_messages")
            assert result is not None, "Required property 'targeted_messages' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvokedByProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceBot.LexConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lex_bot_alias_arn": "lexBotAliasArn",
            "locale_id": "localeId",
            "invoked_by": "invokedBy",
            "responds_to": "respondsTo",
            "welcome_intent": "welcomeIntent",
        },
    )
    class LexConfigurationProperty:
        def __init__(
            self,
            *,
            lex_bot_alias_arn: builtins.str,
            locale_id: builtins.str,
            invoked_by: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceBot.InvokedByProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            responds_to: typing.Optional[builtins.str] = None,
            welcome_intent: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for an Amazon Lex V2 bot.

            :param lex_bot_alias_arn: The ARN of the Amazon Lex V2 bot's alias.
            :param locale_id: Identifies the Amazon Lex V2 bot's language and locale.
            :param invoked_by: Specifies the type of message that triggers a bot.
            :param responds_to: Determines whether the Amazon Lex V2 bot responds to all standard messages. Control messages are not supported.
            :param welcome_intent: The name of the welcome intent configured in the Amazon Lex V2 bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                lex_configuration_property = chime.CfnAppInstanceBot.LexConfigurationProperty(
                    lex_bot_alias_arn="lexBotAliasArn",
                    locale_id="localeId",
                
                    # the properties below are optional
                    invoked_by=chime.CfnAppInstanceBot.InvokedByProperty(
                        standard_messages="standardMessages",
                        targeted_messages="targetedMessages"
                    ),
                    responds_to="respondsTo",
                    welcome_intent="welcomeIntent"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__59e9097c00a1cff69d67ed6937aea0b11010ff23c371f50b9ae25d98378dbf55)
                check_type(argname="argument lex_bot_alias_arn", value=lex_bot_alias_arn, expected_type=type_hints["lex_bot_alias_arn"])
                check_type(argname="argument locale_id", value=locale_id, expected_type=type_hints["locale_id"])
                check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                check_type(argname="argument responds_to", value=responds_to, expected_type=type_hints["responds_to"])
                check_type(argname="argument welcome_intent", value=welcome_intent, expected_type=type_hints["welcome_intent"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lex_bot_alias_arn": lex_bot_alias_arn,
                "locale_id": locale_id,
            }
            if invoked_by is not None:
                self._values["invoked_by"] = invoked_by
            if responds_to is not None:
                self._values["responds_to"] = responds_to
            if welcome_intent is not None:
                self._values["welcome_intent"] = welcome_intent

        @builtins.property
        def lex_bot_alias_arn(self) -> builtins.str:
            '''The ARN of the Amazon Lex V2 bot's alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html#cfn-chime-appinstancebot-lexconfiguration-lexbotaliasarn
            '''
            result = self._values.get("lex_bot_alias_arn")
            assert result is not None, "Required property 'lex_bot_alias_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def locale_id(self) -> builtins.str:
            '''Identifies the Amazon Lex V2 bot's language and locale.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html#cfn-chime-appinstancebot-lexconfiguration-localeid
            '''
            result = self._values.get("locale_id")
            assert result is not None, "Required property 'locale_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def invoked_by(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.InvokedByProperty"]]:
            '''Specifies the type of message that triggers a bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html#cfn-chime-appinstancebot-lexconfiguration-invokedby
            '''
            result = self._values.get("invoked_by")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.InvokedByProperty"]], result)

        @builtins.property
        def responds_to(self) -> typing.Optional[builtins.str]:
            '''Determines whether the Amazon Lex V2 bot responds to all standard messages.

            Control messages are not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html#cfn-chime-appinstancebot-lexconfiguration-respondsto
            '''
            result = self._values.get("responds_to")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def welcome_intent(self) -> typing.Optional[builtins.str]:
            '''The name of the welcome intent configured in the Amazon Lex V2 bot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstancebot-lexconfiguration.html#cfn-chime-appinstancebot-lexconfiguration-welcomeintent
            '''
            result = self._values.get("welcome_intent")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LexConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceBotProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "configuration": "configuration",
        "metadata": "metadata",
        "name": "name",
        "tags": "tags",
    },
)
class CfnAppInstanceBotProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceBot.ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAppInstanceBot``.

        :param app_instance_arn: The ARN of the AppInstance.
        :param configuration: A structure that contains configuration data.
        :param metadata: The metadata of the AppInstanceBot.
        :param name: The name of the AppInstanceBot.
        :param tags: The tags assigned to the AppInstanceBot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_chime as chime
            
            cfn_app_instance_bot_props = chime.CfnAppInstanceBotProps(
                app_instance_arn="appInstanceArn",
                configuration=chime.CfnAppInstanceBot.ConfigurationProperty(
                    lex=chime.CfnAppInstanceBot.LexConfigurationProperty(
                        lex_bot_alias_arn="lexBotAliasArn",
                        locale_id="localeId",
            
                        # the properties below are optional
                        invoked_by=chime.CfnAppInstanceBot.InvokedByProperty(
                            standard_messages="standardMessages",
                            targeted_messages="targetedMessages"
                        ),
                        responds_to="respondsTo",
                        welcome_intent="welcomeIntent"
                    )
                ),
            
                # the properties below are optional
                metadata="metadata",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d900ae3a9eb6a587e47f3e534920839a7bec4e3fc41d625d3e3b8eb9d31d4eae)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "configuration": configuration,
        }
        if metadata is not None:
            self._values["metadata"] = metadata
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the AppInstance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html#cfn-chime-appinstancebot-appinstancearn
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.ConfigurationProperty"]:
        '''A structure that contains configuration data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html#cfn-chime-appinstancebot-configuration
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceBot.ConfigurationProperty"], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''The metadata of the AppInstanceBot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html#cfn-chime-appinstancebot-metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AppInstanceBot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html#cfn-chime-appinstancebot-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags assigned to the AppInstanceBot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstancebot.html#cfn-chime-appinstancebot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppInstanceBotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = cached_type_hints(_typecheckingstub__551f6928f9d6a158547ebe3a9d4b368b45ad66d983bfb330b063b77c078ca90e)
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
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags assigned to the AppInstance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstance.html#cfn-chime-appinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_chime_58870695.IAppInstanceUserRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnAppInstanceUser(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceUser",
):
    '''Resource Type definition for AWS::Chime::AppInstanceUser.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html
    :cloudformationResource: AWS::Chime::AppInstanceUser
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_chime as chime
        
        cfn_app_instance_user = chime.CfnAppInstanceUser(self, "MyCfnAppInstanceUser",
            app_instance_arn="appInstanceArn",
            app_instance_user_id="appInstanceUserId",
        
            # the properties below are optional
            expiration_settings=chime.CfnAppInstanceUser.ExpirationSettingsProperty(
                expiration_criterion="expirationCriterion",
                expiration_days=123
            ),
            metadata="metadata",
            name="name",
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
        app_instance_arn: builtins.str,
        app_instance_user_id: builtins.str,
        expiration_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceUser.ExpirationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Chime::AppInstanceUser``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param app_instance_arn: 
        :param app_instance_user_id: 
        :param expiration_settings: 
        :param metadata: 
        :param name: 
        :param tags: 
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2085cb61a0928e322527b02fa835e93ae1473637b82fc400d98124c9f4ea85ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppInstanceUserProps(
            app_instance_arn=app_instance_arn,
            app_instance_user_id=app_instance_user_id,
            expiration_settings=expiration_settings,
            metadata=metadata,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAppInstanceUser")
    @builtins.classmethod
    def arn_for_app_instance_user(
        cls,
        resource: "_aws_chime_58870695.IAppInstanceUserRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__834453efdb4b627060834867c4d4be14cef2b1616cd26510f95ad19700c58e71)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAppInstanceUser", [resource]))

    @jsii.member(jsii_name="isCfnAppInstanceUser")
    @builtins.classmethod
    def is_cfn_app_instance_user(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAppInstanceUser.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b8249e724ed1b8ced6af4d14e2e058e7d87c556d2f34822d2c13ef2eae05db6f)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAppInstanceUser", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__863252a597952f489269b67d81cb8b94673d4899994aee030ef3ab18f84474cf)
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
            type_hints = cached_type_hints(_typecheckingstub__2319035bf7a04fca46bccb72f782d57c44957ca4561f7cd63c521a103cb24570)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceUserRef")
    def app_instance_user_ref(self) -> "_aws_chime_58870695.AppInstanceUserReference":
        '''A reference to a AppInstanceUser resource.'''
        return typing.cast("_aws_chime_58870695.AppInstanceUserReference", jsii.get(self, "appInstanceUserRef"))

    @builtins.property
    @jsii.member(jsii_name="attrAppInstanceUserArn")
    def attr_app_instance_user_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AppInstanceUserArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppInstanceUserArn"))

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
    @jsii.member(jsii_name="appInstanceArn")
    def app_instance_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceArn"))

    @app_instance_arn.setter
    def app_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b20a22b966f7df8751e06019df44b290ea5ac0f00632c5f0800d1ac32bc198eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appInstanceUserId")
    def app_instance_user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appInstanceUserId"))

    @app_instance_user_id.setter
    def app_instance_user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cfdd12ef0fd7a56e531e08fb8f66900a90956c52b40bad7b1a5bc196cc3b9f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstanceUserId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationSettings")
    def expiration_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceUser.ExpirationSettingsProperty"]]:
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceUser.ExpirationSettingsProperty"]], jsii.get(self, "expirationSettings"))

    @expiration_settings.setter
    def expiration_settings(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceUser.ExpirationSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__11df1f0a14380b6e64d70d38f2d2279aa0cad03492a1c3ea2c336851c1379cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__503686b1a9877ef8aef136c790c2be6a495abcde2081aa874974aba213155b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94ed3eda3e56547fc67748fa6d649fea23db4fd56781e44025b0e46a5857c8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9051ba4c8c7a02ae24d26117b6b0c144f5b530848f9f9411655d4461d5883b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceUser.ExpirationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expiration_criterion": "expirationCriterion",
            "expiration_days": "expirationDays",
        },
    )
    class ExpirationSettingsProperty:
        def __init__(
            self,
            *,
            expiration_criterion: builtins.str,
            expiration_days: jsii.Number,
        ) -> None:
            '''
            :param expiration_criterion: 
            :param expiration_days: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstanceuser-expirationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                expiration_settings_property = chime.CfnAppInstanceUser.ExpirationSettingsProperty(
                    expiration_criterion="expirationCriterion",
                    expiration_days=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e650d9ca25019153fe4e2391b149c6b4c2a2336449a5886a3b94f66bf8ccb812)
                check_type(argname="argument expiration_criterion", value=expiration_criterion, expected_type=type_hints["expiration_criterion"])
                check_type(argname="argument expiration_days", value=expiration_days, expected_type=type_hints["expiration_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "expiration_criterion": expiration_criterion,
                "expiration_days": expiration_days,
            }

        @builtins.property
        def expiration_criterion(self) -> builtins.str:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstanceuser-expirationsettings.html#cfn-chime-appinstanceuser-expirationsettings-expirationcriterion
            '''
            result = self._values.get("expiration_criterion")
            assert result is not None, "Required property 'expiration_criterion' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def expiration_days(self) -> jsii.Number:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-appinstanceuser-expirationsettings.html#cfn-chime-appinstanceuser-expirationsettings-expirationdays
            '''
            result = self._values.get("expiration_days")
            assert result is not None, "Required property 'expiration_days' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpirationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_chime.CfnAppInstanceUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "app_instance_user_id": "appInstanceUserId",
        "expiration_settings": "expirationSettings",
        "metadata": "metadata",
        "name": "name",
        "tags": "tags",
    },
)
class CfnAppInstanceUserProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        app_instance_user_id: builtins.str,
        expiration_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAppInstanceUser.ExpirationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metadata: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAppInstanceUser``.

        :param app_instance_arn: 
        :param app_instance_user_id: 
        :param expiration_settings: 
        :param metadata: 
        :param name: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_chime as chime
            
            cfn_app_instance_user_props = chime.CfnAppInstanceUserProps(
                app_instance_arn="appInstanceArn",
                app_instance_user_id="appInstanceUserId",
            
                # the properties below are optional
                expiration_settings=chime.CfnAppInstanceUser.ExpirationSettingsProperty(
                    expiration_criterion="expirationCriterion",
                    expiration_days=123
                ),
                metadata="metadata",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c191e7d70c48f14aeb5305a9541ebc0cb899fc4cc9efe9e64a380ae2098e7b6e)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument app_instance_user_id", value=app_instance_user_id, expected_type=type_hints["app_instance_user_id"])
            check_type(argname="argument expiration_settings", value=expiration_settings, expected_type=type_hints["expiration_settings"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "app_instance_user_id": app_instance_user_id,
        }
        if expiration_settings is not None:
            self._values["expiration_settings"] = expiration_settings
        if metadata is not None:
            self._values["metadata"] = metadata
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-appinstancearn
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_instance_user_id(self) -> builtins.str:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-appinstanceuserid
        '''
        result = self._values.get("app_instance_user_id")
        assert result is not None, "Required property 'app_instance_user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceUser.ExpirationSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-expirationsettings
        '''
        result = self._values.get("expiration_settings")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAppInstanceUser.ExpirationSettingsProperty"]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-metadata
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-appinstanceuser.html#cfn-chime-appinstanceuser-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppInstanceUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_chime_58870695.IChannelFlowRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnChannelFlow(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_chime.CfnChannelFlow",
):
    '''Creates a channel flow in the Amazon Chime SDK Messaging service.

    A channel flow is a container for processors (Lambda functions) that perform actions on chat messages.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html
    :cloudformationResource: AWS::Chime::ChannelFlow
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_chime as chime
        
        cfn_channel_flow = chime.CfnChannelFlow(self, "MyCfnChannelFlow",
            app_instance_arn="appInstanceArn",
            name="name",
            processors=[chime.CfnChannelFlow.ProcessorProperty(
                configuration=chime.CfnChannelFlow.ProcessorConfigurationProperty(
                    lambda_=chime.CfnChannelFlow.LambdaConfigurationProperty(
                        invocation_type="invocationType",
                        resource_arn="resourceArn"
                    )
                ),
                execution_order=123,
                fallback_action="fallbackAction",
                name="name"
            )],
        
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
        app_instance_arn: builtins.str,
        name: builtins.str,
        processors: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnChannelFlow.ProcessorProperty", typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Chime::ChannelFlow``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param app_instance_arn: The ARN of the app instance.
        :param name: The name of the channel flow.
        :param processors: Information about the processor Lambda functions.
        :param tags: The tags for the channel flow.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__553e37c55476a947075ca59056beea348820f4c9d0001731f2dc6df208e46aac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnChannelFlowProps(
            app_instance_arn=app_instance_arn,
            name=name,
            processors=processors,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForChannelFlow")
    @builtins.classmethod
    def arn_for_channel_flow(
        cls,
        resource: "_aws_chime_58870695.IChannelFlowRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__215e52bbdaf64af19e7a78a4c16ecf1be25619c25b0f1f560edef98f17fd074f)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForChannelFlow", [resource]))

    @jsii.member(jsii_name="isCfnChannelFlow")
    @builtins.classmethod
    def is_cfn_channel_flow(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnChannelFlow.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7cd9c6e628c1ed57d7d45231f8fd40a59294a2cfe8e8086a494a43b0dfbcb348)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnChannelFlow", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__95d931527d027465cc783a90101afd59c6d28ac9549723ed78d381411c1f152c)
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
            type_hints = cached_type_hints(_typecheckingstub__c315bd571cdd659263f798212f27154c2c646ef9c193834f07a863a925933999)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppInstanceId")
    def attr_app_instance_id(self) -> builtins.str:
        '''The ID of the app instance, extracted from the channel flow ARN.

        :cloudformationAttribute: AppInstanceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppInstanceId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the channel flow.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrChannelFlowId")
    def attr_channel_flow_id(self) -> builtins.str:
        '''The ID of the channel flow, extracted from the channel flow ARN.

        :cloudformationAttribute: ChannelFlowId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrChannelFlowId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTimestamp")
    def attr_created_timestamp(self) -> builtins.str:
        '''The time at which the channel flow was created.

        :cloudformationAttribute: CreatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTimestamp")
    def attr_last_updated_timestamp(self) -> builtins.str:
        '''The time at which the channel flow was last updated.

        :cloudformationAttribute: LastUpdatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTimestamp"))

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
    @jsii.member(jsii_name="channelFlowRef")
    def channel_flow_ref(self) -> "_aws_chime_58870695.ChannelFlowReference":
        '''A reference to a ChannelFlow resource.'''
        return typing.cast("_aws_chime_58870695.ChannelFlowReference", jsii.get(self, "channelFlowRef"))

    @builtins.property
    @jsii.member(jsii_name="appInstanceArn")
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the app instance.'''
        return typing.cast(builtins.str, jsii.get(self, "appInstanceArn"))

    @app_instance_arn.setter
    def app_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2952f13ac0bef71a3fce903cbe1c25737bd7625917778a93a03dac2015fa2104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appInstanceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the channel flow.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__411cc8fb86020950b5c9e5844fb80dccb3d2c00b763b9ab9a8f9b5cc719d9451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processors")
    def processors(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorProperty"]]]:
        '''Information about the processor Lambda functions.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorProperty"]]], jsii.get(self, "processors"))

    @processors.setter
    def processors(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__87728ae9e5da9fcebfef150b2b1326c7b3106255781f7f53de411ad39a29a508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the channel flow.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__56a722312beda48b0dba71e0a7247be1089c7db33dfb3f22b8eb02c0cea9adc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnChannelFlow.LambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invocation_type": "invocationType",
            "resource_arn": "resourceArn",
        },
    )
    class LambdaConfigurationProperty:
        def __init__(
            self,
            *,
            invocation_type: builtins.str,
            resource_arn: builtins.str,
        ) -> None:
            '''Stores metadata about a Lambda processor.

            :param invocation_type: Controls how the Lambda function is invoked.
            :param resource_arn: The ARN of the Lambda message processing function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-lambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                lambda_configuration_property = chime.CfnChannelFlow.LambdaConfigurationProperty(
                    invocation_type="invocationType",
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__285ed0bc098587d57e9f94632c1cb3c1c76fff652d29fd8997a47c3b2cc1cc09)
                check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "invocation_type": invocation_type,
                "resource_arn": resource_arn,
            }

        @builtins.property
        def invocation_type(self) -> builtins.str:
            '''Controls how the Lambda function is invoked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-lambdaconfiguration.html#cfn-chime-channelflow-lambdaconfiguration-invocationtype
            '''
            result = self._values.get("invocation_type")
            assert result is not None, "Required property 'invocation_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''The ARN of the Lambda message processing function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-lambdaconfiguration.html#cfn-chime-channelflow-lambdaconfiguration-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnChannelFlow.ProcessorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_": "lambda"},
    )
    class ProcessorConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnChannelFlow.LambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A processor's metadata.

            :param lambda_: Stores metadata about a Lambda processor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                processor_configuration_property = chime.CfnChannelFlow.ProcessorConfigurationProperty(
                    lambda_=chime.CfnChannelFlow.LambdaConfigurationProperty(
                        invocation_type="invocationType",
                        resource_arn="resourceArn"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__9fdc1fc093fa01b9277bf2dd738d6f6237e1cce994cac73e6f7d4e62ab99ac5c)
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_": lambda_,
            }

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.LambdaConfigurationProperty"]:
            '''Stores metadata about a Lambda processor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processorconfiguration.html#cfn-chime-channelflow-processorconfiguration-lambda
            '''
            result = self._values.get("lambda_")
            assert result is not None, "Required property 'lambda_' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.LambdaConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_chime.CfnChannelFlow.ProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "execution_order": "executionOrder",
            "fallback_action": "fallbackAction",
            "name": "name",
        },
    )
    class ProcessorProperty:
        def __init__(
            self,
            *,
            configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnChannelFlow.ProcessorConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
            execution_order: jsii.Number,
            fallback_action: builtins.str,
            name: builtins.str,
        ) -> None:
            '''Information about a processor in a channel flow.

            :param configuration: A processor's metadata.
            :param execution_order: The sequence in which processors run.
            :param fallback_action: Determines whether to continue or stop processing when communication with a processor fails.
            :param name: The name of the processor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_chime as chime
                
                processor_property = chime.CfnChannelFlow.ProcessorProperty(
                    configuration=chime.CfnChannelFlow.ProcessorConfigurationProperty(
                        lambda_=chime.CfnChannelFlow.LambdaConfigurationProperty(
                            invocation_type="invocationType",
                            resource_arn="resourceArn"
                        )
                    ),
                    execution_order=123,
                    fallback_action="fallbackAction",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__be4dcd983ce00e19de1c1ec7124b3517157f895d6121f59f1ca204a7a59f7fc1)
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument execution_order", value=execution_order, expected_type=type_hints["execution_order"])
                check_type(argname="argument fallback_action", value=fallback_action, expected_type=type_hints["fallback_action"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "configuration": configuration,
                "execution_order": execution_order,
                "fallback_action": fallback_action,
                "name": name,
            }

        @builtins.property
        def configuration(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorConfigurationProperty"]:
            '''A processor's metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processor.html#cfn-chime-channelflow-processor-configuration
            '''
            result = self._values.get("configuration")
            assert result is not None, "Required property 'configuration' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorConfigurationProperty"], result)

        @builtins.property
        def execution_order(self) -> jsii.Number:
            '''The sequence in which processors run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processor.html#cfn-chime-channelflow-processor-executionorder
            '''
            result = self._values.get("execution_order")
            assert result is not None, "Required property 'execution_order' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def fallback_action(self) -> builtins.str:
            '''Determines whether to continue or stop processing when communication with a processor fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processor.html#cfn-chime-channelflow-processor-fallbackaction
            '''
            result = self._values.get("fallback_action")
            assert result is not None, "Required property 'fallback_action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the processor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-chime-channelflow-processor.html#cfn-chime-channelflow-processor-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_chime.CfnChannelFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_instance_arn": "appInstanceArn",
        "name": "name",
        "processors": "processors",
        "tags": "tags",
    },
)
class CfnChannelFlowProps:
    def __init__(
        self,
        *,
        app_instance_arn: builtins.str,
        name: builtins.str,
        processors: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnChannelFlow.ProcessorProperty", typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnChannelFlow``.

        :param app_instance_arn: The ARN of the app instance.
        :param name: The name of the channel flow.
        :param processors: Information about the processor Lambda functions.
        :param tags: The tags for the channel flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_chime as chime
            
            cfn_channel_flow_props = chime.CfnChannelFlowProps(
                app_instance_arn="appInstanceArn",
                name="name",
                processors=[chime.CfnChannelFlow.ProcessorProperty(
                    configuration=chime.CfnChannelFlow.ProcessorConfigurationProperty(
                        lambda_=chime.CfnChannelFlow.LambdaConfigurationProperty(
                            invocation_type="invocationType",
                            resource_arn="resourceArn"
                        )
                    ),
                    execution_order=123,
                    fallback_action="fallbackAction",
                    name="name"
                )],
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__04fab589c36890507658f03e0daf5dda656b997e99d4f0f5d449cfb4324279d2)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument processors", value=processors, expected_type=type_hints["processors"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
            "name": name,
            "processors": processors,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The ARN of the app instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html#cfn-chime-channelflow-appinstancearn
        '''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the channel flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html#cfn-chime-channelflow-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def processors(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorProperty"]]]:
        '''Information about the processor Lambda functions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html#cfn-chime-channelflow-processors
        '''
        result = self._values.get("processors")
        assert result is not None, "Required property 'processors' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnChannelFlow.ProcessorProperty"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the channel flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chime-channelflow.html#cfn-chime-channelflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAppInstance",
    "CfnAppInstanceBot",
    "CfnAppInstanceBotProps",
    "CfnAppInstanceProps",
    "CfnAppInstanceUser",
    "CfnAppInstanceUserProps",
    "CfnChannelFlow",
    "CfnChannelFlowProps",
]

publication.publish()

def _typecheckingstub__6d337d6c149cc789c0b6f05ba4ba90f831464295606b004354b7815daaed0c77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    metadata: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f74b0e7014ea5c23e28103a5fb5867813697fd8201279c330a3aa769bc126a1(
    resource: _aws_chime_58870695.IAppInstanceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a664656abafe2adc6e2a0a9db5e06dc33b5b3b6a0fa2a5ca0b61b7b95d0c32(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400a60274a57ac76d314b93fb263163beba6942cc730e90588d6f74e739f4eb0(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
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
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca75944f6ceb69180d3b0f352517267777aeee7ffaa12b2f1a465cf9b6a3e00(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceBot.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c5faf3dcf2887594ff746db96b49d9757db79f86e9d6f358d9f275ee8c8210(
    resource: _aws_chime_58870695.IAppInstanceBotRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0255372b69a195b0351367c082f9533519223c17e242b93716f61ed8e55dea62(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427e24f474e9d78b560301eb631ab4ec523303c4565f63f29c83299fe5abafb1(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f31284f1d604da54c34b53acb2ff3863b786fb7370f15d19da68df814cd8ad(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a53900f75f263ec868d4efe44340a9273169b155a8e54a68fe8cde3818baec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36a14f99ec95cd590d6c1757bb41c8b9235cf6b317fa73e6692074ed033195a(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnAppInstanceBot.ConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45024baca15a880d713b7458c08c15471a9b4b4bc485fcaa496535c2d75a30a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ad6a83eab879d92eb2609e2f37735b3c2383bb2e7e24c6cefbec192e42c39e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87e45b7d9459784717058ca252a094c146e5656ea14d9da51f1cf05f4aa56d4(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ff343ee28319a719419e7819c467b339964da524abd8a8f50f44edd43b11a8(
    *,
    lex: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceBot.LexConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a8291bb53d368f6b1012fdd17317226c377241787e7d74d9371e641c527be4(
    *,
    standard_messages: builtins.str,
    targeted_messages: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e9097c00a1cff69d67ed6937aea0b11010ff23c371f50b9ae25d98378dbf55(
    *,
    lex_bot_alias_arn: builtins.str,
    locale_id: builtins.str,
    invoked_by: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceBot.InvokedByProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    responds_to: typing.Optional[builtins.str] = None,
    welcome_intent: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d900ae3a9eb6a587e47f3e534920839a7bec4e3fc41d625d3e3b8eb9d31d4eae(
    *,
    app_instance_arn: builtins.str,
    configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceBot.ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551f6928f9d6a158547ebe3a9d4b368b45ad66d983bfb330b063b77c078ca90e(
    *,
    name: builtins.str,
    metadata: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2085cb61a0928e322527b02fa835e93ae1473637b82fc400d98124c9f4ea85ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    app_instance_user_id: builtins.str,
    expiration_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceUser.ExpirationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834453efdb4b627060834867c4d4be14cef2b1616cd26510f95ad19700c58e71(
    resource: _aws_chime_58870695.IAppInstanceUserRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8249e724ed1b8ced6af4d14e2e058e7d87c556d2f34822d2c13ef2eae05db6f(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863252a597952f489269b67d81cb8b94673d4899994aee030ef3ab18f84474cf(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2319035bf7a04fca46bccb72f782d57c44957ca4561f7cd63c521a103cb24570(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20a22b966f7df8751e06019df44b290ea5ac0f00632c5f0800d1ac32bc198eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdd12ef0fd7a56e531e08fb8f66900a90956c52b40bad7b1a5bc196cc3b9f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11df1f0a14380b6e64d70d38f2d2279aa0cad03492a1c3ea2c336851c1379cd8(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnAppInstanceUser.ExpirationSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503686b1a9877ef8aef136c790c2be6a495abcde2081aa874974aba213155b4a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ed3eda3e56547fc67748fa6d649fea23db4fd56781e44025b0e46a5857c8a5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9051ba4c8c7a02ae24d26117b6b0c144f5b530848f9f9411655d4461d5883b41(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e650d9ca25019153fe4e2391b149c6b4c2a2336449a5886a3b94f66bf8ccb812(
    *,
    expiration_criterion: builtins.str,
    expiration_days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c191e7d70c48f14aeb5305a9541ebc0cb899fc4cc9efe9e64a380ae2098e7b6e(
    *,
    app_instance_arn: builtins.str,
    app_instance_user_id: builtins.str,
    expiration_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAppInstanceUser.ExpirationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553e37c55476a947075ca59056beea348820f4c9d0001731f2dc6df208e46aac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_instance_arn: builtins.str,
    name: builtins.str,
    processors: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnChannelFlow.ProcessorProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215e52bbdaf64af19e7a78a4c16ecf1be25619c25b0f1f560edef98f17fd074f(
    resource: _aws_chime_58870695.IChannelFlowRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd9c6e628c1ed57d7d45231f8fd40a59294a2cfe8e8086a494a43b0dfbcb348(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d931527d027465cc783a90101afd59c6d28ac9549723ed78d381411c1f152c(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c315bd571cdd659263f798212f27154c2c646ef9c193834f07a863a925933999(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2952f13ac0bef71a3fce903cbe1c25737bd7625917778a93a03dac2015fa2104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411cc8fb86020950b5c9e5844fb80dccb3d2c00b763b9ab9a8f9b5cc719d9451(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87728ae9e5da9fcebfef150b2b1326c7b3106255781f7f53de411ad39a29a508(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnChannelFlow.ProcessorProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a722312beda48b0dba71e0a7247be1089c7db33dfb3f22b8eb02c0cea9adc2(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285ed0bc098587d57e9f94632c1cb3c1c76fff652d29fd8997a47c3b2cc1cc09(
    *,
    invocation_type: builtins.str,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdc1fc093fa01b9277bf2dd738d6f6237e1cce994cac73e6f7d4e62ab99ac5c(
    *,
    lambda_: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnChannelFlow.LambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4dcd983ce00e19de1c1ec7124b3517157f895d6121f59f1ca204a7a59f7fc1(
    *,
    configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnChannelFlow.ProcessorConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    execution_order: jsii.Number,
    fallback_action: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fab589c36890507658f03e0daf5dda656b997e99d4f0f5d449cfb4324279d2(
    *,
    app_instance_arn: builtins.str,
    name: builtins.str,
    processors: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnChannelFlow.ProcessorProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

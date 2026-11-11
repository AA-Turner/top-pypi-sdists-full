r'''
# AWS::MGN Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_mgn as mgn
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for MGN construct libraries](https://constructs.dev/search?q=mgn)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::MGN resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MGN.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::MGN](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MGN.html).

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
    import aws_cdk.interfaces.aws_mgn as _aws_mgn_7f0ba49e
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_mgn_7f0ba49e = _LazyImport("aws_cdk.interfaces.aws_mgn")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.IApplicationRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnApplication(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnApplication",
):
    '''An MGN Application is a logical grouping of source servers being migrated together using AWS Application Migration Service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-application.html
    :cloudformationResource: AWS::MGN::Application
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_application = mgn.CfnApplication(self, "MyCfnApplication",
            name="name",
        
            # the properties below are optional
            description="description",
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
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::Application``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the application.
        :param description: The description of the application.
        :param tags: A set of tags to associate with the application.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3dda22f820c3748889315357f7f8d8808142d4bbe6e78fa2169f112bb0f1aab4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForApplication")
    @builtins.classmethod
    def arn_for_application(
        cls,
        resource: "_aws_mgn_7f0ba49e.IApplicationRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bda45874557c2da2d1cb406c9e553d28f4a4f0bce1860372b45e0a67699cdd2d)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForApplication", [resource]))

    @jsii.member(jsii_name="isCfnApplication")
    @builtins.classmethod
    def is_cfn_application(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnApplication.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__499dd71a3d3df5437f9a4e19a080f3b5db107fd9b022a77e34e59bf0caf6eff1)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnApplication", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ee867837d27bb3d1e190e3a8ed61c22c3cccbfcc32ab5a63dece4b96783fe1b9)
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
            type_hints = cached_type_hints(_typecheckingstub__89d7bb6250ea5535971502f33ae78665bfc5b20337d5bdf66f16a0438bf00472)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="applicationRef")
    def application_ref(self) -> "_aws_mgn_7f0ba49e.ApplicationReference":
        '''A reference to a Application resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.ApplicationReference", jsii.get(self, "applicationRef"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationId")
    def attr_application_id(self) -> builtins.str:
        '''The ID of the application.

        :cloudformationAttribute: ApplicationID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time the application was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrIsArchived")
    def attr_is_archived(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Whether the application is archived.

        :cloudformationAttribute: IsArchived
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrIsArchived"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModifiedDateTime")
    def attr_last_modified_date_time(self) -> builtins.str:
        '''The date and time the application was last modified.

        :cloudformationAttribute: LastModifiedDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModifiedDateTime"))

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
        '''The name of the application.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9eca8e4ce863fae79d00a7dd6e50472226240b48abaee7eef8b8c78512ac2cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e666f8444740767b11735b73024aa0a6477f77e2eececae78a7318ab87ca0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to associate with the application.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8dff4ca7b322d329ac080906ceecb610d62b9f6784d7997eb261041c910a0e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param name: The name of the application.
        :param description: The description of the application.
        :param tags: A set of tags to associate with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-application.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_application_props = mgn.CfnApplicationProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f1a40f46582952499bc335293aa0de7470b33b01b5ce361f3cdb38bab496e97)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-application.html#cfn-mgn-application-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-application.html#cfn-mgn-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to associate with the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-application.html#cfn-mgn-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.IConnectorRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnConnector(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnConnector",
):
    '''Resource schema for AWS::MGN::Connector.

    A Connector provides connectivity between a source environment and Application Migration Service (MGN) via AWS Systems Manager (SSM).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html
    :cloudformationResource: AWS::MGN::Connector
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_connector = mgn.CfnConnector(self, "MyCfnConnector",
            name="name",
            ssm_instance_id="ssmInstanceId",
        
            # the properties below are optional
            ssm_command_config=mgn.CfnConnector.ConnectorSsmCommandConfigProperty(
                cloud_watch_output_enabled=False,
                s3_output_enabled=False,
        
                # the properties below are optional
                cloud_watch_log_group_name="cloudWatchLogGroupName",
                output_s3_bucket_name="outputS3BucketName"
            ),
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
        ssm_instance_id: builtins.str,
        ssm_command_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnConnector.ConnectorSsmCommandConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::Connector``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the connector.
        :param ssm_instance_id: The SSM instance ID associated with this connector.
        :param ssm_command_config: SSM command configuration for the connector.
        :param tags: Tags to assign to the connector.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1009ba5960ab3691b98cd0782c80f689e21000b6c903683a2672ab7ba794a126)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorProps(
            name=name,
            ssm_instance_id=ssm_instance_id,
            ssm_command_config=ssm_command_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForConnector")
    @builtins.classmethod
    def arn_for_connector(
        cls,
        resource: "_aws_mgn_7f0ba49e.IConnectorRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__92a32287b1f062fc70060093299724663384337cf9ca819fefad38cec6bd0af8)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForConnector", [resource]))

    @jsii.member(jsii_name="isCfnConnector")
    @builtins.classmethod
    def is_cfn_connector(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnConnector.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__611e506d864ec2ff274adc77ee1de6c2387eaa38a610ca5aaa2e770b659cb5ec)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnConnector", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d28142cdb5dd62e111bc45361cbd48636711889d6b2e8eeebad0834c32bba1d9)
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
            type_hints = cached_type_hints(_typecheckingstub__35e2086da01ebdadad16f108ac3cbba59789ba2a0c0180ca8b358812507016e9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the connector.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectorId")
    def attr_connector_id(self) -> builtins.str:
        '''The unique identifier of the connector.

        :cloudformationAttribute: ConnectorID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorId"))

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
    @jsii.member(jsii_name="connectorRef")
    def connector_ref(self) -> "_aws_mgn_7f0ba49e.ConnectorReference":
        '''A reference to a Connector resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.ConnectorReference", jsii.get(self, "connectorRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the connector.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c2360c01e39e2abd04cc142761ec5ad9bf2014769e3feee71dee12b936589b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ssmInstanceId")
    def ssm_instance_id(self) -> builtins.str:
        '''The SSM instance ID associated with this connector.'''
        return typing.cast(builtins.str, jsii.get(self, "ssmInstanceId"))

    @ssm_instance_id.setter
    def ssm_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__51c969ac30ea400d91a13596c32a88e67342e3e494560406753557e40b0c5414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssmInstanceId", value)

    @builtins.property
    @jsii.member(jsii_name="ssmCommandConfig")
    def ssm_command_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnConnector.ConnectorSsmCommandConfigProperty"]]:
        '''SSM command configuration for the connector.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnConnector.ConnectorSsmCommandConfigProperty"]], jsii.get(self, "ssmCommandConfig"))

    @ssm_command_config.setter
    def ssm_command_config(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnConnector.ConnectorSsmCommandConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__41e391c1b5ed08e4613fd1ce7e6af8aa16512f8ef8b60d6cf6ed5ea6a360e67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssmCommandConfig", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the connector.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bbcdd84ad1148215dd898e861326eb4847251dc142e777f24c36d87887edd9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnConnector.ConnectorSsmCommandConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_output_enabled": "cloudWatchOutputEnabled",
            "s3_output_enabled": "s3OutputEnabled",
            "cloud_watch_log_group_name": "cloudWatchLogGroupName",
            "output_s3_bucket_name": "outputS3BucketName",
        },
    )
    class ConnectorSsmCommandConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_output_enabled: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
            s3_output_enabled: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
            cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
            output_s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''SSM command configuration for the connector.

            :param cloud_watch_output_enabled: Whether SSM command output is sent to CloudWatch Logs.
            :param s3_output_enabled: Whether SSM command output is stored in S3.
            :param cloud_watch_log_group_name: The CloudWatch Logs group name for SSM command output.
            :param output_s3_bucket_name: The S3 bucket name for SSM command output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-connector-connectorssmcommandconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                connector_ssm_command_config_property = mgn.CfnConnector.ConnectorSsmCommandConfigProperty(
                    cloud_watch_output_enabled=False,
                    s3_output_enabled=False,
                
                    # the properties below are optional
                    cloud_watch_log_group_name="cloudWatchLogGroupName",
                    output_s3_bucket_name="outputS3BucketName"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8be748cf81b7c3877ac0c5a8c6889e285776316c0f9a45b5c0907407ccadfcd9)
                check_type(argname="argument cloud_watch_output_enabled", value=cloud_watch_output_enabled, expected_type=type_hints["cloud_watch_output_enabled"])
                check_type(argname="argument s3_output_enabled", value=s3_output_enabled, expected_type=type_hints["s3_output_enabled"])
                check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
                check_type(argname="argument output_s3_bucket_name", value=output_s3_bucket_name, expected_type=type_hints["output_s3_bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cloud_watch_output_enabled": cloud_watch_output_enabled,
                "s3_output_enabled": s3_output_enabled,
            }
            if cloud_watch_log_group_name is not None:
                self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
            if output_s3_bucket_name is not None:
                self._values["output_s3_bucket_name"] = output_s3_bucket_name

        @builtins.property
        def cloud_watch_output_enabled(
            self,
        ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
            '''Whether SSM command output is sent to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-connector-connectorssmcommandconfig.html#cfn-mgn-connector-connectorssmcommandconfig-cloudwatchoutputenabled
            '''
            result = self._values.get("cloud_watch_output_enabled")
            assert result is not None, "Required property 'cloud_watch_output_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

        @builtins.property
        def s3_output_enabled(
            self,
        ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
            '''Whether SSM command output is stored in S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-connector-connectorssmcommandconfig.html#cfn-mgn-connector-connectorssmcommandconfig-s3outputenabled
            '''
            result = self._values.get("s3_output_enabled")
            assert result is not None, "Required property 's3_output_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

        @builtins.property
        def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
            '''The CloudWatch Logs group name for SSM command output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-connector-connectorssmcommandconfig.html#cfn-mgn-connector-connectorssmcommandconfig-cloudwatchloggroupname
            '''
            result = self._values.get("cloud_watch_log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket name for SSM command output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-connector-connectorssmcommandconfig.html#cfn-mgn-connector-connectorssmcommandconfig-outputs3bucketname
            '''
            result = self._values.get("output_s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorSsmCommandConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnConnectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "ssm_instance_id": "ssmInstanceId",
        "ssm_command_config": "ssmCommandConfig",
        "tags": "tags",
    },
)
class CfnConnectorProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        ssm_instance_id: builtins.str,
        ssm_command_config: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnConnector.ConnectorSsmCommandConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnector``.

        :param name: The name of the connector.
        :param ssm_instance_id: The SSM instance ID associated with this connector.
        :param ssm_command_config: SSM command configuration for the connector.
        :param tags: Tags to assign to the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_connector_props = mgn.CfnConnectorProps(
                name="name",
                ssm_instance_id="ssmInstanceId",
            
                # the properties below are optional
                ssm_command_config=mgn.CfnConnector.ConnectorSsmCommandConfigProperty(
                    cloud_watch_output_enabled=False,
                    s3_output_enabled=False,
            
                    # the properties below are optional
                    cloud_watch_log_group_name="cloudWatchLogGroupName",
                    output_s3_bucket_name="outputS3BucketName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__adfdf7308d5e774a55e16d6f427b8f1b29b8342ea3eafbf72d21afc99670bb48)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ssm_instance_id", value=ssm_instance_id, expected_type=type_hints["ssm_instance_id"])
            check_type(argname="argument ssm_command_config", value=ssm_command_config, expected_type=type_hints["ssm_command_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "ssm_instance_id": ssm_instance_id,
        }
        if ssm_command_config is not None:
            self._values["ssm_command_config"] = ssm_command_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html#cfn-mgn-connector-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssm_instance_id(self) -> builtins.str:
        '''The SSM instance ID associated with this connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html#cfn-mgn-connector-ssminstanceid
        '''
        result = self._values.get("ssm_instance_id")
        assert result is not None, "Required property 'ssm_instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ssm_command_config(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnConnector.ConnectorSsmCommandConfigProperty"]]:
        '''SSM command configuration for the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html#cfn-mgn-connector-ssmcommandconfig
        '''
        result = self._values.get("ssm_command_config")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnConnector.ConnectorSsmCommandConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-connector.html#cfn-mgn-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.ILaunchConfigurationTemplateRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnLaunchConfigurationTemplate(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate",
):
    '''Account level Launch Configuration Template for AWS Application Migration Service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html
    :cloudformationResource: AWS::MGN::LaunchConfigurationTemplate
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_launch_configuration_template = mgn.CfnLaunchConfigurationTemplate(self, "MyCfnLaunchConfigurationTemplate",
            associate_public_ip_address=False,
            boot_mode="bootMode",
            copy_private_ip=False,
            copy_tags=False,
            enable_map_auto_tagging=False,
            enable_parameters_encryption=False,
            large_volume_conf=mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty(
                iops=123,
                throughput=123,
                volume_type="volumeType"
            ),
            launch_disposition="launchDisposition",
            licensing=mgn.CfnLaunchConfigurationTemplate.LicensingProperty(
                os_byol=False
            ),
            map_auto_tagging_mpe_id="mapAutoTaggingMpeId",
            parameters_encryption_key="parametersEncryptionKey",
            post_launch_actions=mgn.CfnLaunchConfigurationTemplate.PostLaunchActionsProperty(
                cloud_watch_log_group_name="cloudWatchLogGroupName",
                deployment="deployment",
                s3_log_bucket="s3LogBucket",
                s3_output_key_prefix="s3OutputKeyPrefix",
                ssm_documents=[mgn.CfnLaunchConfigurationTemplate.SsmDocumentProperty(
                    action_name="actionName",
                    ssm_document_name="ssmDocumentName",
        
                    # the properties below are optional
                    external_parameters={
                        "external_parameters_key": mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty(
                            dynamic_path="dynamicPath"
                        )
                    },
                    must_succeed_for_cutover=False,
                    parameters={
                        "parameters_key": [mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty(
                            parameter_name="parameterName",
                            parameter_type="parameterType"
                        )]
                    },
                    timeout_seconds=123
                )]
            ),
            small_volume_conf=mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty(
                iops=123,
                throughput=123,
                volume_type="volumeType"
            ),
            small_volume_max_size=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_instance_type_right_sizing_method="targetInstanceTypeRightSizingMethod"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        boot_mode: typing.Optional[builtins.str] = None,
        copy_private_ip: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        enable_map_auto_tagging: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        enable_parameters_encryption: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        large_volume_conf: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        launch_disposition: typing.Optional[builtins.str] = None,
        licensing: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LicensingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        map_auto_tagging_mpe_id: typing.Optional[builtins.str] = None,
        parameters_encryption_key: typing.Optional[builtins.str] = None,
        post_launch_actions: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.PostLaunchActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        small_volume_conf: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        small_volume_max_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_instance_type_right_sizing_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::LaunchConfigurationTemplate``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param associate_public_ip_address: Whether to associate a public IP address with the launched instance.
        :param boot_mode: Launch configuration template boot mode.
        :param copy_private_ip: Whether to copy the private IP of the source server.
        :param copy_tags: Whether to copy the tags of the source server.
        :param enable_map_auto_tagging: Whether to enable map auto tagging.
        :param enable_parameters_encryption: Whether to enable encryption of the AWS Systems Manager parameters used by post launch actions.
        :param large_volume_conf: Launch template disk configuration.
        :param launch_disposition: Launch disposition.
        :param licensing: Configuration of a machine's license.
        :param map_auto_tagging_mpe_id: Launch configuration template map auto tagging MPE ID.
        :param parameters_encryption_key: ARN of the KMS key used to encrypt the AWS Systems Manager parameters used by post launch actions.
        :param post_launch_actions: Post launch actions to execute on the Test or Cutover instance.
        :param small_volume_conf: Launch template disk configuration.
        :param small_volume_max_size: Small volume maximum size, in GiB.
        :param tags: A set of tags to be associated with the Launch Configuration Template.
        :param target_instance_type_right_sizing_method: Target instance type right-sizing method.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bef03edb0bde55472bcaf13434e6be51dd9adda59fef8102636df1985b9dcffa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLaunchConfigurationTemplateProps(
            associate_public_ip_address=associate_public_ip_address,
            boot_mode=boot_mode,
            copy_private_ip=copy_private_ip,
            copy_tags=copy_tags,
            enable_map_auto_tagging=enable_map_auto_tagging,
            enable_parameters_encryption=enable_parameters_encryption,
            large_volume_conf=large_volume_conf,
            launch_disposition=launch_disposition,
            licensing=licensing,
            map_auto_tagging_mpe_id=map_auto_tagging_mpe_id,
            parameters_encryption_key=parameters_encryption_key,
            post_launch_actions=post_launch_actions,
            small_volume_conf=small_volume_conf,
            small_volume_max_size=small_volume_max_size,
            tags=tags,
            target_instance_type_right_sizing_method=target_instance_type_right_sizing_method,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLaunchConfigurationTemplate")
    @builtins.classmethod
    def arn_for_launch_configuration_template(
        cls,
        resource: "_aws_mgn_7f0ba49e.ILaunchConfigurationTemplateRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__936a4c3d3f9a54bc73dcff3c5bfeece8f7d89a1cc33560737c4b7d43de8b13a1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForLaunchConfigurationTemplate", [resource]))

    @jsii.member(jsii_name="isCfnLaunchConfigurationTemplate")
    @builtins.classmethod
    def is_cfn_launch_configuration_template(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnLaunchConfigurationTemplate.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8cac804cc2774e9b12bd440713e222c4096569266c27eddc711f0ed55f6c44ae)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnLaunchConfigurationTemplate", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ae22e88eb3ea69da7242e66f7efd25627741fb6b41166eaa0d6d51cf70a264a7)
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
            type_hints = cached_type_hints(_typecheckingstub__0e1a19d7a92eb4f026bfdb0d4bf32234d656210d1c3b1623d9168fd575e8fb68)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''ARN of the Launch Configuration Template.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEc2LaunchTemplateId")
    def attr_ec2_launch_template_id(self) -> builtins.str:
        '''ID of the EC2 launch template backing the Launch Configuration Template.

        :cloudformationAttribute: Ec2LaunchTemplateID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEc2LaunchTemplateId"))

    @builtins.property
    @jsii.member(jsii_name="attrLaunchConfigurationTemplateId")
    def attr_launch_configuration_template_id(self) -> builtins.str:
        '''ID of the Launch Configuration Template.

        :cloudformationAttribute: LaunchConfigurationTemplateID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLaunchConfigurationTemplateId"))

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
    @jsii.member(jsii_name="launchConfigurationTemplateRef")
    def launch_configuration_template_ref(
        self,
    ) -> "_aws_mgn_7f0ba49e.LaunchConfigurationTemplateReference":
        '''A reference to a LaunchConfigurationTemplate resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.LaunchConfigurationTemplateReference", jsii.get(self, "launchConfigurationTemplateRef"))

    @builtins.property
    @jsii.member(jsii_name="associatePublicIpAddress")
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to associate a public IP address with the launched instance.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "associatePublicIpAddress"))

    @associate_public_ip_address.setter
    def associate_public_ip_address(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6cb81319ccde12f4ac3668a4f6626e97f42379e2ade48439e00ddad50d11e307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatePublicIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="bootMode")
    def boot_mode(self) -> typing.Optional[builtins.str]:
        '''Launch configuration template boot mode.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootMode"))

    @boot_mode.setter
    def boot_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3e305a35308d10974f4c7a6a48ebc4fb2a4b26a3409d1782b174b2a18e677545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootMode", value)

    @builtins.property
    @jsii.member(jsii_name="copyPrivateIp")
    def copy_private_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to copy the private IP of the source server.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "copyPrivateIp"))

    @copy_private_ip.setter
    def copy_private_ip(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__33bf06397f65bbd180b94f01ce0500f7399108c26d5215412920d73d3a59ebd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyPrivateIp", value)

    @builtins.property
    @jsii.member(jsii_name="copyTags")
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to copy the tags of the source server.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "copyTags"))

    @copy_tags.setter
    def copy_tags(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3d53f514011c8a6bdffff82fa33f170118d61fbfd1388e3a7a679a28728571c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTags", value)

    @builtins.property
    @jsii.member(jsii_name="enableMapAutoTagging")
    def enable_map_auto_tagging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to enable map auto tagging.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "enableMapAutoTagging"))

    @enable_map_auto_tagging.setter
    def enable_map_auto_tagging(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__354911b4a5f7f8fff29d172315e37e7b5f20d742bc5f92908958c433167176ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMapAutoTagging", value)

    @builtins.property
    @jsii.member(jsii_name="enableParametersEncryption")
    def enable_parameters_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to enable encryption of the AWS Systems Manager parameters used by post launch actions.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "enableParametersEncryption"))

    @enable_parameters_encryption.setter
    def enable_parameters_encryption(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b4cceff17d854c4f1d187787cb0c0a0ee834cb58817e70612eb85cc9252d4a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableParametersEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="largeVolumeConf")
    def large_volume_conf(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]]:
        '''Launch template disk configuration.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]], jsii.get(self, "largeVolumeConf"))

    @large_volume_conf.setter
    def large_volume_conf(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3d52d2fb041c92f68ccc20bca1ea4a0c8bf709639403b9fcbddf00d30a61af89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "largeVolumeConf", value)

    @builtins.property
    @jsii.member(jsii_name="launchDisposition")
    def launch_disposition(self) -> typing.Optional[builtins.str]:
        '''Launch disposition.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchDisposition"))

    @launch_disposition.setter
    def launch_disposition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b6fc80841b1f61d5996ccbe63dd8a32adb8ad48cb95185b0f3e47f721efa75e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchDisposition", value)

    @builtins.property
    @jsii.member(jsii_name="licensing")
    def licensing(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LicensingProperty"]]:
        '''Configuration of a machine's license.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LicensingProperty"]], jsii.get(self, "licensing"))

    @licensing.setter
    def licensing(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LicensingProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6940030110ee61928330e31366dbd86895fb9f347ce228cbc5d86014e793367b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licensing", value)

    @builtins.property
    @jsii.member(jsii_name="mapAutoTaggingMpeId")
    def map_auto_tagging_mpe_id(self) -> typing.Optional[builtins.str]:
        '''Launch configuration template map auto tagging MPE ID.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mapAutoTaggingMpeId"))

    @map_auto_tagging_mpe_id.setter
    def map_auto_tagging_mpe_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__458175bde67d8b9fdd0494380089b0fcaa65acfa66aafd3c7386014665a577b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapAutoTaggingMpeId", value)

    @builtins.property
    @jsii.member(jsii_name="parametersEncryptionKey")
    def parameters_encryption_key(self) -> typing.Optional[builtins.str]:
        '''ARN of the KMS key used to encrypt the AWS Systems Manager parameters used by post launch actions.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parametersEncryptionKey"))

    @parameters_encryption_key.setter
    def parameters_encryption_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__986d2dc3edffc815aebca3b17e5f9279c3ee1a0a064600363e4fb25f2f83f042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parametersEncryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="postLaunchActions")
    def post_launch_actions(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.PostLaunchActionsProperty"]]:
        '''Post launch actions to execute on the Test or Cutover instance.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.PostLaunchActionsProperty"]], jsii.get(self, "postLaunchActions"))

    @post_launch_actions.setter
    def post_launch_actions(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.PostLaunchActionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a0c86780add8d852573d56138f583eb5d0a7a12af7b08260bd94bad8b5cd45c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postLaunchActions", value)

    @builtins.property
    @jsii.member(jsii_name="smallVolumeConf")
    def small_volume_conf(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]]:
        '''Launch template disk configuration.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]], jsii.get(self, "smallVolumeConf"))

    @small_volume_conf.setter
    def small_volume_conf(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c198de7f2c124d8f95b560b0aca1e4227407e8d801f1b4cd5d1581e9851ed1b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smallVolumeConf", value)

    @builtins.property
    @jsii.member(jsii_name="smallVolumeMaxSize")
    def small_volume_max_size(self) -> typing.Optional[jsii.Number]:
        '''Small volume maximum size, in GiB.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "smallVolumeMaxSize"))

    @small_volume_max_size.setter
    def small_volume_max_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8ce6bf16723f22750621375344c1b6d55a2a252fa135d330e3cb305f1c44059f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smallVolumeMaxSize", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to be associated with the Launch Configuration Template.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__99936035b36e5b429e8ca3e56383b1c9339040797d1488a3d5019762e9374a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="targetInstanceTypeRightSizingMethod")
    def target_instance_type_right_sizing_method(self) -> typing.Optional[builtins.str]:
        '''Target instance type right-sizing method.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInstanceTypeRightSizingMethod"))

    @target_instance_type_right_sizing_method.setter
    def target_instance_type_right_sizing_method(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__21669f94c81d0f530fc8b55385817623a899258e521f5b2153209ba9d6eae4b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetInstanceTypeRightSizingMethod", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iops": "iops",
            "throughput": "throughput",
            "volume_type": "volumeType",
        },
    )
    class LaunchTemplateDiskConfProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Launch template disk configuration.

            :param iops: Launch template disk IOPS configuration.
            :param throughput: Launch template disk throughput configuration, in MiB/s.
            :param volume_type: Launch template disk volume type configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-launchtemplatediskconf.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                launch_template_disk_conf_property = mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty(
                    iops=123,
                    throughput=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__452a08df9218a99bbd69bf2e96cb39dee9a26fae627afc9f33be4136fd02cfd1)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''Launch template disk IOPS configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-launchtemplatediskconf.html#cfn-mgn-launchconfigurationtemplate-launchtemplatediskconf-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''Launch template disk throughput configuration, in MiB/s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-launchtemplatediskconf.html#cfn-mgn-launchconfigurationtemplate-launchtemplatediskconf-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''Launch template disk volume type configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-launchtemplatediskconf.html#cfn-mgn-launchconfigurationtemplate-launchtemplatediskconf-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateDiskConfProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.LicensingProperty",
        jsii_struct_bases=[],
        name_mapping={"os_byol": "osByol"},
    )
    class LicensingProperty:
        def __init__(
            self,
            *,
            os_byol: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        ) -> None:
            '''Configuration of a machine's license.

            :param os_byol: Whether to configure BYOL OS licensing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-licensing.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                licensing_property = mgn.CfnLaunchConfigurationTemplate.LicensingProperty(
                    os_byol=False
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__f6122ea07854f4031df2ac73f0d80dbc3cd6e14b76db0d9c407c2f8c168c6cc3)
                check_type(argname="argument os_byol", value=os_byol, expected_type=type_hints["os_byol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if os_byol is not None:
                self._values["os_byol"] = os_byol

        @builtins.property
        def os_byol(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Whether to configure BYOL OS licensing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-licensing.html#cfn-mgn-launchconfigurationtemplate-licensing-osbyol
            '''
            result = self._values.get("os_byol")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicensingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.PostLaunchActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_name": "cloudWatchLogGroupName",
            "deployment": "deployment",
            "s3_log_bucket": "s3LogBucket",
            "s3_output_key_prefix": "s3OutputKeyPrefix",
            "ssm_documents": "ssmDocuments",
        },
    )
    class PostLaunchActionsProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
            deployment: typing.Optional[builtins.str] = None,
            s3_log_bucket: typing.Optional[builtins.str] = None,
            s3_output_key_prefix: typing.Optional[builtins.str] = None,
            ssm_documents: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.SsmDocumentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Post launch actions to execute on the Test or Cutover instance.

            :param cloud_watch_log_group_name: AWS Systems Manager Command's CloudWatch log group name.
            :param deployment: Deployment type in which AWS Systems Manager Documents will be executed.
            :param s3_log_bucket: AWS Systems Manager Command's logs S3 log bucket.
            :param s3_output_key_prefix: AWS Systems Manager Command's logs S3 output key prefix.
            :param ssm_documents: AWS Systems Manager Documents to execute, in order.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                post_launch_actions_property = mgn.CfnLaunchConfigurationTemplate.PostLaunchActionsProperty(
                    cloud_watch_log_group_name="cloudWatchLogGroupName",
                    deployment="deployment",
                    s3_log_bucket="s3LogBucket",
                    s3_output_key_prefix="s3OutputKeyPrefix",
                    ssm_documents=[mgn.CfnLaunchConfigurationTemplate.SsmDocumentProperty(
                        action_name="actionName",
                        ssm_document_name="ssmDocumentName",
                
                        # the properties below are optional
                        external_parameters={
                            "external_parameters_key": mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty(
                                dynamic_path="dynamicPath"
                            )
                        },
                        must_succeed_for_cutover=False,
                        parameters={
                            "parameters_key": [mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty(
                                parameter_name="parameterName",
                                parameter_type="parameterType"
                            )]
                        },
                        timeout_seconds=123
                    )]
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__37b06c309fc890fd02f67a5bd15c8bd3846009f539439bbed5263f060daff549)
                check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
                check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
                check_type(argname="argument s3_log_bucket", value=s3_log_bucket, expected_type=type_hints["s3_log_bucket"])
                check_type(argname="argument s3_output_key_prefix", value=s3_output_key_prefix, expected_type=type_hints["s3_output_key_prefix"])
                check_type(argname="argument ssm_documents", value=ssm_documents, expected_type=type_hints["ssm_documents"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_group_name is not None:
                self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
            if deployment is not None:
                self._values["deployment"] = deployment
            if s3_log_bucket is not None:
                self._values["s3_log_bucket"] = s3_log_bucket
            if s3_output_key_prefix is not None:
                self._values["s3_output_key_prefix"] = s3_output_key_prefix
            if ssm_documents is not None:
                self._values["ssm_documents"] = ssm_documents

        @builtins.property
        def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
            '''AWS Systems Manager Command's CloudWatch log group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions-cloudwatchloggroupname
            '''
            result = self._values.get("cloud_watch_log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment(self) -> typing.Optional[builtins.str]:
            '''Deployment type in which AWS Systems Manager Documents will be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions-deployment
            '''
            result = self._values.get("deployment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_log_bucket(self) -> typing.Optional[builtins.str]:
            '''AWS Systems Manager Command's logs S3 log bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions-s3logbucket
            '''
            result = self._values.get("s3_log_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_key_prefix(self) -> typing.Optional[builtins.str]:
            '''AWS Systems Manager Command's logs S3 output key prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions-s3outputkeyprefix
            '''
            result = self._values.get("s3_output_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssm_documents(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmDocumentProperty"]]]]:
            '''AWS Systems Manager Documents to execute, in order.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-postlaunchactions.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions-ssmdocuments
            '''
            result = self._values.get("ssm_documents")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmDocumentProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PostLaunchActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.SsmDocumentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_name": "actionName",
            "ssm_document_name": "ssmDocumentName",
            "external_parameters": "externalParameters",
            "must_succeed_for_cutover": "mustSucceedForCutover",
            "parameters": "parameters",
            "timeout_seconds": "timeoutSeconds",
        },
    )
    class SsmDocumentProperty:
        def __init__(
            self,
            *,
            action_name: builtins.str,
            ssm_document_name: builtins.str,
            external_parameters: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.SsmExternalParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            must_succeed_for_cutover: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            parameters: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
            timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An AWS Systems Manager Document to execute as a post launch action.

            :param action_name: User-friendly name for the AWS Systems Manager Document.
            :param ssm_document_name: AWS Systems Manager Document name or full ARN.
            :param external_parameters: AWS Systems Manager Document external parameters.
            :param must_succeed_for_cutover: Whether Cutover is blocked when the document has failed.
            :param parameters: AWS Systems Manager Document parameters, each resolved from AWS Systems Manager Parameter Store.
            :param timeout_seconds: AWS Systems Manager Document timeout, in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                ssm_document_property = mgn.CfnLaunchConfigurationTemplate.SsmDocumentProperty(
                    action_name="actionName",
                    ssm_document_name="ssmDocumentName",
                
                    # the properties below are optional
                    external_parameters={
                        "external_parameters_key": mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty(
                            dynamic_path="dynamicPath"
                        )
                    },
                    must_succeed_for_cutover=False,
                    parameters={
                        "parameters_key": [mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty(
                            parameter_name="parameterName",
                            parameter_type="parameterType"
                        )]
                    },
                    timeout_seconds=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__fa6135a5510bec3a9f6e1828dcdbef9dfb0d4653faf46390b91f21350ffc8477)
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
                check_type(argname="argument ssm_document_name", value=ssm_document_name, expected_type=type_hints["ssm_document_name"])
                check_type(argname="argument external_parameters", value=external_parameters, expected_type=type_hints["external_parameters"])
                check_type(argname="argument must_succeed_for_cutover", value=must_succeed_for_cutover, expected_type=type_hints["must_succeed_for_cutover"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_name": action_name,
                "ssm_document_name": ssm_document_name,
            }
            if external_parameters is not None:
                self._values["external_parameters"] = external_parameters
            if must_succeed_for_cutover is not None:
                self._values["must_succeed_for_cutover"] = must_succeed_for_cutover
            if parameters is not None:
                self._values["parameters"] = parameters
            if timeout_seconds is not None:
                self._values["timeout_seconds"] = timeout_seconds

        @builtins.property
        def action_name(self) -> builtins.str:
            '''User-friendly name for the AWS Systems Manager Document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-actionname
            '''
            result = self._values.get("action_name")
            assert result is not None, "Required property 'action_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ssm_document_name(self) -> builtins.str:
            '''AWS Systems Manager Document name or full ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-ssmdocumentname
            '''
            result = self._values.get("ssm_document_name")
            assert result is not None, "Required property 'ssm_document_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def external_parameters(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmExternalParameterProperty"]]]]:
            '''AWS Systems Manager Document external parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-externalparameters
            '''
            result = self._values.get("external_parameters")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmExternalParameterProperty"]]]], result)

        @builtins.property
        def must_succeed_for_cutover(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Whether Cutover is blocked when the document has failed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-mustsucceedforcutover
            '''
            result = self._values.get("must_succeed_for_cutover")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty"]]]]]]:
            '''AWS Systems Manager Document parameters, each resolved from AWS Systems Manager Parameter Store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty"]]]]]], result)

        @builtins.property
        def timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''AWS Systems Manager Document timeout, in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmdocument.html#cfn-mgn-launchconfigurationtemplate-ssmdocument-timeoutseconds
            '''
            result = self._values.get("timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmDocumentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"dynamic_path": "dynamicPath"},
    )
    class SsmExternalParameterProperty:
        def __init__(self, *, dynamic_path: builtins.str) -> None:
            '''An AWS Systems Manager Document external parameter.

            :param dynamic_path: AWS Systems Manager Document external parameter dynamic path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmexternalparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                ssm_external_parameter_property = mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty(
                    dynamic_path="dynamicPath"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__a3a4180a313c1557a092c3453e69b3520041a0d5e63f452ca7878fc8d2c410d3)
                check_type(argname="argument dynamic_path", value=dynamic_path, expected_type=type_hints["dynamic_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dynamic_path": dynamic_path,
            }

        @builtins.property
        def dynamic_path(self) -> builtins.str:
            '''AWS Systems Manager Document external parameter dynamic path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmexternalparameter.html#cfn-mgn-launchconfigurationtemplate-ssmexternalparameter-dynamicpath
            '''
            result = self._values.get("dynamic_path")
            assert result is not None, "Required property 'dynamic_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmExternalParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_type": "parameterType",
        },
    )
    class SsmParameterStoreParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: builtins.str,
            parameter_type: builtins.str,
        ) -> None:
            '''An AWS Systems Manager Parameter Store parameter.

            :param parameter_name: AWS Systems Manager Parameter Store parameter name.
            :param parameter_type: AWS Systems Manager Parameter Store parameter type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmparameterstoreparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                ssm_parameter_store_parameter_property = mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty(
                    parameter_name="parameterName",
                    parameter_type="parameterType"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__8343fa74b4c119ea1e29e2decf1b3e6d44bcd2fa2e29d1390bfe9f1eaa1e2004)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_type", value=parameter_type, expected_type=type_hints["parameter_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "parameter_name": parameter_name,
                "parameter_type": parameter_type,
            }

        @builtins.property
        def parameter_name(self) -> builtins.str:
            '''AWS Systems Manager Parameter Store parameter name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmparameterstoreparameter.html#cfn-mgn-launchconfigurationtemplate-ssmparameterstoreparameter-parametername
            '''
            result = self._values.get("parameter_name")
            assert result is not None, "Required property 'parameter_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameter_type(self) -> builtins.str:
            '''AWS Systems Manager Parameter Store parameter type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-launchconfigurationtemplate-ssmparameterstoreparameter.html#cfn-mgn-launchconfigurationtemplate-ssmparameterstoreparameter-parametertype
            '''
            result = self._values.get("parameter_type")
            assert result is not None, "Required property 'parameter_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsmParameterStoreParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnLaunchConfigurationTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_public_ip_address": "associatePublicIpAddress",
        "boot_mode": "bootMode",
        "copy_private_ip": "copyPrivateIp",
        "copy_tags": "copyTags",
        "enable_map_auto_tagging": "enableMapAutoTagging",
        "enable_parameters_encryption": "enableParametersEncryption",
        "large_volume_conf": "largeVolumeConf",
        "launch_disposition": "launchDisposition",
        "licensing": "licensing",
        "map_auto_tagging_mpe_id": "mapAutoTaggingMpeId",
        "parameters_encryption_key": "parametersEncryptionKey",
        "post_launch_actions": "postLaunchActions",
        "small_volume_conf": "smallVolumeConf",
        "small_volume_max_size": "smallVolumeMaxSize",
        "tags": "tags",
        "target_instance_type_right_sizing_method": "targetInstanceTypeRightSizingMethod",
    },
)
class CfnLaunchConfigurationTemplateProps:
    def __init__(
        self,
        *,
        associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        boot_mode: typing.Optional[builtins.str] = None,
        copy_private_ip: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        copy_tags: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        enable_map_auto_tagging: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        enable_parameters_encryption: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        large_volume_conf: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        launch_disposition: typing.Optional[builtins.str] = None,
        licensing: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LicensingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        map_auto_tagging_mpe_id: typing.Optional[builtins.str] = None,
        parameters_encryption_key: typing.Optional[builtins.str] = None,
        post_launch_actions: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.PostLaunchActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        small_volume_conf: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        small_volume_max_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_instance_type_right_sizing_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLaunchConfigurationTemplate``.

        :param associate_public_ip_address: Whether to associate a public IP address with the launched instance.
        :param boot_mode: Launch configuration template boot mode.
        :param copy_private_ip: Whether to copy the private IP of the source server.
        :param copy_tags: Whether to copy the tags of the source server.
        :param enable_map_auto_tagging: Whether to enable map auto tagging.
        :param enable_parameters_encryption: Whether to enable encryption of the AWS Systems Manager parameters used by post launch actions.
        :param large_volume_conf: Launch template disk configuration.
        :param launch_disposition: Launch disposition.
        :param licensing: Configuration of a machine's license.
        :param map_auto_tagging_mpe_id: Launch configuration template map auto tagging MPE ID.
        :param parameters_encryption_key: ARN of the KMS key used to encrypt the AWS Systems Manager parameters used by post launch actions.
        :param post_launch_actions: Post launch actions to execute on the Test or Cutover instance.
        :param small_volume_conf: Launch template disk configuration.
        :param small_volume_max_size: Small volume maximum size, in GiB.
        :param tags: A set of tags to be associated with the Launch Configuration Template.
        :param target_instance_type_right_sizing_method: Target instance type right-sizing method.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_launch_configuration_template_props = mgn.CfnLaunchConfigurationTemplateProps(
                associate_public_ip_address=False,
                boot_mode="bootMode",
                copy_private_ip=False,
                copy_tags=False,
                enable_map_auto_tagging=False,
                enable_parameters_encryption=False,
                large_volume_conf=mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty(
                    iops=123,
                    throughput=123,
                    volume_type="volumeType"
                ),
                launch_disposition="launchDisposition",
                licensing=mgn.CfnLaunchConfigurationTemplate.LicensingProperty(
                    os_byol=False
                ),
                map_auto_tagging_mpe_id="mapAutoTaggingMpeId",
                parameters_encryption_key="parametersEncryptionKey",
                post_launch_actions=mgn.CfnLaunchConfigurationTemplate.PostLaunchActionsProperty(
                    cloud_watch_log_group_name="cloudWatchLogGroupName",
                    deployment="deployment",
                    s3_log_bucket="s3LogBucket",
                    s3_output_key_prefix="s3OutputKeyPrefix",
                    ssm_documents=[mgn.CfnLaunchConfigurationTemplate.SsmDocumentProperty(
                        action_name="actionName",
                        ssm_document_name="ssmDocumentName",
            
                        # the properties below are optional
                        external_parameters={
                            "external_parameters_key": mgn.CfnLaunchConfigurationTemplate.SsmExternalParameterProperty(
                                dynamic_path="dynamicPath"
                            )
                        },
                        must_succeed_for_cutover=False,
                        parameters={
                            "parameters_key": [mgn.CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty(
                                parameter_name="parameterName",
                                parameter_type="parameterType"
                            )]
                        },
                        timeout_seconds=123
                    )]
                ),
                small_volume_conf=mgn.CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty(
                    iops=123,
                    throughput=123,
                    volume_type="volumeType"
                ),
                small_volume_max_size=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_instance_type_right_sizing_method="targetInstanceTypeRightSizingMethod"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__049d62ecccf18ceb0b801ca363d50fe7c2d95486a27446b157bea4507dd7b77f)
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument boot_mode", value=boot_mode, expected_type=type_hints["boot_mode"])
            check_type(argname="argument copy_private_ip", value=copy_private_ip, expected_type=type_hints["copy_private_ip"])
            check_type(argname="argument copy_tags", value=copy_tags, expected_type=type_hints["copy_tags"])
            check_type(argname="argument enable_map_auto_tagging", value=enable_map_auto_tagging, expected_type=type_hints["enable_map_auto_tagging"])
            check_type(argname="argument enable_parameters_encryption", value=enable_parameters_encryption, expected_type=type_hints["enable_parameters_encryption"])
            check_type(argname="argument large_volume_conf", value=large_volume_conf, expected_type=type_hints["large_volume_conf"])
            check_type(argname="argument launch_disposition", value=launch_disposition, expected_type=type_hints["launch_disposition"])
            check_type(argname="argument licensing", value=licensing, expected_type=type_hints["licensing"])
            check_type(argname="argument map_auto_tagging_mpe_id", value=map_auto_tagging_mpe_id, expected_type=type_hints["map_auto_tagging_mpe_id"])
            check_type(argname="argument parameters_encryption_key", value=parameters_encryption_key, expected_type=type_hints["parameters_encryption_key"])
            check_type(argname="argument post_launch_actions", value=post_launch_actions, expected_type=type_hints["post_launch_actions"])
            check_type(argname="argument small_volume_conf", value=small_volume_conf, expected_type=type_hints["small_volume_conf"])
            check_type(argname="argument small_volume_max_size", value=small_volume_max_size, expected_type=type_hints["small_volume_max_size"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_instance_type_right_sizing_method", value=target_instance_type_right_sizing_method, expected_type=type_hints["target_instance_type_right_sizing_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if boot_mode is not None:
            self._values["boot_mode"] = boot_mode
        if copy_private_ip is not None:
            self._values["copy_private_ip"] = copy_private_ip
        if copy_tags is not None:
            self._values["copy_tags"] = copy_tags
        if enable_map_auto_tagging is not None:
            self._values["enable_map_auto_tagging"] = enable_map_auto_tagging
        if enable_parameters_encryption is not None:
            self._values["enable_parameters_encryption"] = enable_parameters_encryption
        if large_volume_conf is not None:
            self._values["large_volume_conf"] = large_volume_conf
        if launch_disposition is not None:
            self._values["launch_disposition"] = launch_disposition
        if licensing is not None:
            self._values["licensing"] = licensing
        if map_auto_tagging_mpe_id is not None:
            self._values["map_auto_tagging_mpe_id"] = map_auto_tagging_mpe_id
        if parameters_encryption_key is not None:
            self._values["parameters_encryption_key"] = parameters_encryption_key
        if post_launch_actions is not None:
            self._values["post_launch_actions"] = post_launch_actions
        if small_volume_conf is not None:
            self._values["small_volume_conf"] = small_volume_conf
        if small_volume_max_size is not None:
            self._values["small_volume_max_size"] = small_volume_max_size
        if tags is not None:
            self._values["tags"] = tags
        if target_instance_type_right_sizing_method is not None:
            self._values["target_instance_type_right_sizing_method"] = target_instance_type_right_sizing_method

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to associate a public IP address with the launched instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-associatepublicipaddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def boot_mode(self) -> typing.Optional[builtins.str]:
        '''Launch configuration template boot mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-bootmode
        '''
        result = self._values.get("boot_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_private_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to copy the private IP of the source server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-copyprivateip
        '''
        result = self._values.get("copy_private_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def copy_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to copy the tags of the source server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-copytags
        '''
        result = self._values.get("copy_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def enable_map_auto_tagging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to enable map auto tagging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-enablemapautotagging
        '''
        result = self._values.get("enable_map_auto_tagging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def enable_parameters_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to enable encryption of the AWS Systems Manager parameters used by post launch actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-enableparametersencryption
        '''
        result = self._values.get("enable_parameters_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def large_volume_conf(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]]:
        '''Launch template disk configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-largevolumeconf
        '''
        result = self._values.get("large_volume_conf")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]], result)

    @builtins.property
    def launch_disposition(self) -> typing.Optional[builtins.str]:
        '''Launch disposition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-launchdisposition
        '''
        result = self._values.get("launch_disposition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def licensing(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LicensingProperty"]]:
        '''Configuration of a machine's license.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-licensing
        '''
        result = self._values.get("licensing")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LicensingProperty"]], result)

    @builtins.property
    def map_auto_tagging_mpe_id(self) -> typing.Optional[builtins.str]:
        '''Launch configuration template map auto tagging MPE ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-mapautotaggingmpeid
        '''
        result = self._values.get("map_auto_tagging_mpe_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters_encryption_key(self) -> typing.Optional[builtins.str]:
        '''ARN of the KMS key used to encrypt the AWS Systems Manager parameters used by post launch actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-parametersencryptionkey
        '''
        result = self._values.get("parameters_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_launch_actions(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.PostLaunchActionsProperty"]]:
        '''Post launch actions to execute on the Test or Cutover instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-postlaunchactions
        '''
        result = self._values.get("post_launch_actions")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.PostLaunchActionsProperty"]], result)

    @builtins.property
    def small_volume_conf(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]]:
        '''Launch template disk configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-smallvolumeconf
        '''
        result = self._values.get("small_volume_conf")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty"]], result)

    @builtins.property
    def small_volume_max_size(self) -> typing.Optional[jsii.Number]:
        '''Small volume maximum size, in GiB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-smallvolumemaxsize
        '''
        result = self._values.get("small_volume_max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to be associated with the Launch Configuration Template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def target_instance_type_right_sizing_method(self) -> typing.Optional[builtins.str]:
        '''Target instance type right-sizing method.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-launchconfigurationtemplate.html#cfn-mgn-launchconfigurationtemplate-targetinstancetyperightsizingmethod
        '''
        result = self._values.get("target_instance_type_right_sizing_method")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchConfigurationTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.INetworkMigrationDefinitionRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnNetworkMigrationDefinition(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinition",
):
    '''Resource schema for AWS::MGN::NetworkMigrationDefinition.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html
    :cloudformationResource: AWS::MGN::NetworkMigrationDefinition
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_network_migration_definition = mgn.CfnNetworkMigrationDefinition(self, "MyCfnNetworkMigrationDefinition",
            name="name",
            source_configurations=[mgn.CfnNetworkMigrationDefinition.SourceConfigurationProperty(
                source_environment="sourceEnvironment",
                source_s3_configuration=mgn.CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner",
                    s3_key="s3Key"
                )
            )],
            target_network=mgn.CfnNetworkMigrationDefinition.TargetNetworkProperty(
                topology="topology",
        
                # the properties below are optional
                inbound_cidr="inboundCidr",
                inspection_cidr="inspectionCidr",
                outbound_cidr="outboundCidr"
            ),
            target_s3_configuration=mgn.CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty(
                s3_bucket="s3Bucket",
                s3_bucket_owner="s3BucketOwner"
            ),
        
            # the properties below are optional
            description="description",
            scope_tags={
                "scope_tags_key": "scopeTags"
            },
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_deployment="targetDeployment"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        name: builtins.str,
        source_configurations: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]],
        target_network: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.TargetNetworkProperty", typing.Dict[builtins.str, typing.Any]]],
        target_s3_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        scope_tags: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_deployment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::NetworkMigrationDefinition``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the network migration definition.
        :param source_configurations: A list of source configurations for the network migration.
        :param target_network: Configuration for the target network topology and addressing.
        :param target_s3_configuration: S3 configuration for storing target network artifacts.
        :param description: A description of the network migration definition.
        :param scope_tags: Scope tags map for the network migration definition.
        :param tags: Tags to assign to the network migration definition.
        :param target_deployment: The target deployment configuration for the migrated network.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d0281edcee00498148c7ba7f314fa799a30c9cdc3b6426d2f772de0035e619f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNetworkMigrationDefinitionProps(
            name=name,
            source_configurations=source_configurations,
            target_network=target_network,
            target_s3_configuration=target_s3_configuration,
            description=description,
            scope_tags=scope_tags,
            tags=tags,
            target_deployment=target_deployment,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForNetworkMigrationDefinition")
    @builtins.classmethod
    def arn_for_network_migration_definition(
        cls,
        resource: "_aws_mgn_7f0ba49e.INetworkMigrationDefinitionRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__149dd6c760e0d5dd62132512d09ad41e09534515b194919d50fe45e71c5e5b63)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForNetworkMigrationDefinition", [resource]))

    @jsii.member(jsii_name="isCfnNetworkMigrationDefinition")
    @builtins.classmethod
    def is_cfn_network_migration_definition(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnNetworkMigrationDefinition.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__20189b7c7a331a0b80c6992064c1d31d7feefcb9e90eda07363eecfd4c52c078)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnNetworkMigrationDefinition", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8aa25ba733421d0f71f5451003b6ac4ff710428a39c26b30fec8f369543ce50f)
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
            type_hints = cached_type_hints(_typecheckingstub__648966bc98e578f126765169f37f44bcd259b27a939d861bd8d9724fe439512b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the network migration definition.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the network migration definition was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkMigrationDefinitionId")
    def attr_network_migration_definition_id(self) -> builtins.str:
        '''The unique identifier of the network migration definition.

        :cloudformationAttribute: NetworkMigrationDefinitionID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkMigrationDefinitionId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the network migration definition was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

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
    @jsii.member(jsii_name="networkMigrationDefinitionRef")
    def network_migration_definition_ref(
        self,
    ) -> "_aws_mgn_7f0ba49e.NetworkMigrationDefinitionReference":
        '''A reference to a NetworkMigrationDefinition resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.NetworkMigrationDefinitionReference", jsii.get(self, "networkMigrationDefinitionRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the network migration definition.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8fb9a7cae80221f9f6a6a2c0b6651db1bf5e6824cb80b97c9c70aa7c444ab28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sourceConfigurations")
    def source_configurations(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceConfigurationProperty"]]]:
        '''A list of source configurations for the network migration.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceConfigurationProperty"]]], jsii.get(self, "sourceConfigurations"))

    @source_configurations.setter
    def source_configurations(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceConfigurationProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f70b4cfffce0b8aaebb121b276c89bc1e9ab93c05852aad015b3a23a22760f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="targetNetwork")
    def target_network(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetNetworkProperty"]:
        '''Configuration for the target network topology and addressing.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetNetworkProperty"], jsii.get(self, "targetNetwork"))

    @target_network.setter
    def target_network(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetNetworkProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__df1cbcd24cf20a1903c584f1e4eda1240e760fc13799b9c8f33e898857360ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetNetwork", value)

    @builtins.property
    @jsii.member(jsii_name="targetS3Configuration")
    def target_s3_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty"]:
        '''S3 configuration for storing target network artifacts.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty"], jsii.get(self, "targetS3Configuration"))

    @target_s3_configuration.setter
    def target_s3_configuration(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__33aaf0e4432fb060b80bb283536a477edb3c1abe8dd20da2fd8bb7f9fbae5cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetS3Configuration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the network migration definition.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__be6550bf9f89012ac37c95d11e738384a548b37599732330f4724f5f30291703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="scopeTags")
    def scope_tags(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]]:
        '''Scope tags map for the network migration definition.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "scopeTags"))

    @scope_tags.setter
    def scope_tags(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f034fd9414240cb5468ffdcfb046caf9c51f5a4b5f67455118206514533d0b1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeTags", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the network migration definition.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1d5cbcf1364554341e91a14e2f83599f70dc4d6829c2b9d5f539517e76e80179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="targetDeployment")
    def target_deployment(self) -> typing.Optional[builtins.str]:
        '''The target deployment configuration for the migrated network.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDeployment"))

    @target_deployment.setter
    def target_deployment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7d1ea8c1d9f889b5c5f0d0f564932da09f5aa885de39152f07e4b3f2ca32fc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDeployment", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinition.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_environment": "sourceEnvironment",
            "source_s3_configuration": "sourceS3Configuration",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            source_environment: builtins.str,
            source_s3_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Configuration for a migration source environment.

            :param source_environment: The source environment type.
            :param source_s3_configuration: S3 configuration for source network data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                source_configuration_property = mgn.CfnNetworkMigrationDefinition.SourceConfigurationProperty(
                    source_environment="sourceEnvironment",
                    source_s3_configuration=mgn.CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty(
                        s3_bucket="s3Bucket",
                        s3_bucket_owner="s3BucketOwner",
                        s3_key="s3Key"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__f03ccb7f1f8f26d65f3920a7a637ebeb3713faac932af41434a59fee43a702bd)
                check_type(argname="argument source_environment", value=source_environment, expected_type=type_hints["source_environment"])
                check_type(argname="argument source_s3_configuration", value=source_s3_configuration, expected_type=type_hints["source_s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source_environment": source_environment,
                "source_s3_configuration": source_s3_configuration,
            }

        @builtins.property
        def source_environment(self) -> builtins.str:
            '''The source environment type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sourceconfiguration.html#cfn-mgn-networkmigrationdefinition-sourceconfiguration-sourceenvironment
            '''
            result = self._values.get("source_environment")
            assert result is not None, "Required property 'source_environment' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_s3_configuration(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty"]:
            '''S3 configuration for source network data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sourceconfiguration.html#cfn-mgn-networkmigrationdefinition-sourceconfiguration-sources3configuration
            '''
            result = self._values.get("source_s3_configuration")
            assert result is not None, "Required property 'source_s3_configuration' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_bucket_owner": "s3BucketOwner",
            "s3_key": "s3Key",
        },
    )
    class SourceS3ConfigurationProperty:
        def __init__(
            self,
            *,
            s3_bucket: builtins.str,
            s3_bucket_owner: builtins.str,
            s3_key: builtins.str,
        ) -> None:
            '''S3 configuration for source network data.

            :param s3_bucket: The name of the S3 bucket containing source data.
            :param s3_bucket_owner: The AWS account ID of the S3 bucket owner.
            :param s3_key: The S3 key (path) for the source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sources3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                source_s3_configuration_property = mgn.CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__1fd02649169db7f73886bfccb202933332f616adc6cdc671056a5a274724646e)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_bucket_owner", value=s3_bucket_owner, expected_type=type_hints["s3_bucket_owner"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_bucket_owner": s3_bucket_owner,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The name of the S3 bucket containing source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sources3configuration.html#cfn-mgn-networkmigrationdefinition-sources3configuration-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_owner(self) -> builtins.str:
            '''The AWS account ID of the S3 bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sources3configuration.html#cfn-mgn-networkmigrationdefinition-sources3configuration-s3bucketowner
            '''
            result = self._values.get("s3_bucket_owner")
            assert result is not None, "Required property 's3_bucket_owner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The S3 key (path) for the source data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-sources3configuration.html#cfn-mgn-networkmigrationdefinition-sources3configuration-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceS3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinition.TargetNetworkProperty",
        jsii_struct_bases=[],
        name_mapping={
            "topology": "topology",
            "inbound_cidr": "inboundCidr",
            "inspection_cidr": "inspectionCidr",
            "outbound_cidr": "outboundCidr",
        },
    )
    class TargetNetworkProperty:
        def __init__(
            self,
            *,
            topology: builtins.str,
            inbound_cidr: typing.Optional[builtins.str] = None,
            inspection_cidr: typing.Optional[builtins.str] = None,
            outbound_cidr: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for the target network topology and addressing.

            :param topology: The network topology type for the target environment.
            :param inbound_cidr: The CIDR block for inbound traffic in the target network.
            :param inspection_cidr: The CIDR block for inspection traffic in the target network.
            :param outbound_cidr: The CIDR block for outbound traffic in the target network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targetnetwork.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                target_network_property = mgn.CfnNetworkMigrationDefinition.TargetNetworkProperty(
                    topology="topology",
                
                    # the properties below are optional
                    inbound_cidr="inboundCidr",
                    inspection_cidr="inspectionCidr",
                    outbound_cidr="outboundCidr"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__4bb70ad8195a8a3b6bdaf88f7cb9324c35874b1a254ee13a628f7e5442cd0c82)
                check_type(argname="argument topology", value=topology, expected_type=type_hints["topology"])
                check_type(argname="argument inbound_cidr", value=inbound_cidr, expected_type=type_hints["inbound_cidr"])
                check_type(argname="argument inspection_cidr", value=inspection_cidr, expected_type=type_hints["inspection_cidr"])
                check_type(argname="argument outbound_cidr", value=outbound_cidr, expected_type=type_hints["outbound_cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topology": topology,
            }
            if inbound_cidr is not None:
                self._values["inbound_cidr"] = inbound_cidr
            if inspection_cidr is not None:
                self._values["inspection_cidr"] = inspection_cidr
            if outbound_cidr is not None:
                self._values["outbound_cidr"] = outbound_cidr

        @builtins.property
        def topology(self) -> builtins.str:
            '''The network topology type for the target environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targetnetwork.html#cfn-mgn-networkmigrationdefinition-targetnetwork-topology
            '''
            result = self._values.get("topology")
            assert result is not None, "Required property 'topology' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def inbound_cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block for inbound traffic in the target network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targetnetwork.html#cfn-mgn-networkmigrationdefinition-targetnetwork-inboundcidr
            '''
            result = self._values.get("inbound_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inspection_cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block for inspection traffic in the target network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targetnetwork.html#cfn-mgn-networkmigrationdefinition-targetnetwork-inspectioncidr
            '''
            result = self._values.get("inspection_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def outbound_cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block for outbound traffic in the target network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targetnetwork.html#cfn-mgn-networkmigrationdefinition-targetnetwork-outboundcidr
            '''
            result = self._values.get("outbound_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetNetworkProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_bucket_owner": "s3BucketOwner"},
    )
    class TargetS3ConfigurationProperty:
        def __init__(
            self,
            *,
            s3_bucket: builtins.str,
            s3_bucket_owner: builtins.str,
        ) -> None:
            '''S3 configuration for storing target network artifacts.

            :param s3_bucket: The name of the S3 bucket for target artifacts.
            :param s3_bucket_owner: The AWS account ID of the S3 bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targets3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                target_s3_configuration_property = mgn.CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__5b0f2d69075166bf24090489d67f01d6cb44e7c61cae821ea446243318f9e1bf)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_bucket_owner", value=s3_bucket_owner, expected_type=type_hints["s3_bucket_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_bucket_owner": s3_bucket_owner,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The name of the S3 bucket for target artifacts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targets3configuration.html#cfn-mgn-networkmigrationdefinition-targets3configuration-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket_owner(self) -> builtins.str:
            '''The AWS account ID of the S3 bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-networkmigrationdefinition-targets3configuration.html#cfn-mgn-networkmigrationdefinition-targets3configuration-s3bucketowner
            '''
            result = self._values.get("s3_bucket_owner")
            assert result is not None, "Required property 's3_bucket_owner' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetS3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnNetworkMigrationDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_configurations": "sourceConfigurations",
        "target_network": "targetNetwork",
        "target_s3_configuration": "targetS3Configuration",
        "description": "description",
        "scope_tags": "scopeTags",
        "tags": "tags",
        "target_deployment": "targetDeployment",
    },
)
class CfnNetworkMigrationDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_configurations: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Sequence[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]],
        target_network: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.TargetNetworkProperty", typing.Dict[builtins.str, typing.Any]]],
        target_s3_configuration: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        scope_tags: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_deployment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNetworkMigrationDefinition``.

        :param name: The name of the network migration definition.
        :param source_configurations: A list of source configurations for the network migration.
        :param target_network: Configuration for the target network topology and addressing.
        :param target_s3_configuration: S3 configuration for storing target network artifacts.
        :param description: A description of the network migration definition.
        :param scope_tags: Scope tags map for the network migration definition.
        :param tags: Tags to assign to the network migration definition.
        :param target_deployment: The target deployment configuration for the migrated network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_network_migration_definition_props = mgn.CfnNetworkMigrationDefinitionProps(
                name="name",
                source_configurations=[mgn.CfnNetworkMigrationDefinition.SourceConfigurationProperty(
                    source_environment="sourceEnvironment",
                    source_s3_configuration=mgn.CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty(
                        s3_bucket="s3Bucket",
                        s3_bucket_owner="s3BucketOwner",
                        s3_key="s3Key"
                    )
                )],
                target_network=mgn.CfnNetworkMigrationDefinition.TargetNetworkProperty(
                    topology="topology",
            
                    # the properties below are optional
                    inbound_cidr="inboundCidr",
                    inspection_cidr="inspectionCidr",
                    outbound_cidr="outboundCidr"
                ),
                target_s3_configuration=mgn.CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty(
                    s3_bucket="s3Bucket",
                    s3_bucket_owner="s3BucketOwner"
                ),
            
                # the properties below are optional
                description="description",
                scope_tags={
                    "scope_tags_key": "scopeTags"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_deployment="targetDeployment"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e818ac919a41cc3b4e605f6633f673a768f2462b9a4b3d1966d51ea457840d55)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_configurations", value=source_configurations, expected_type=type_hints["source_configurations"])
            check_type(argname="argument target_network", value=target_network, expected_type=type_hints["target_network"])
            check_type(argname="argument target_s3_configuration", value=target_s3_configuration, expected_type=type_hints["target_s3_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument scope_tags", value=scope_tags, expected_type=type_hints["scope_tags"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_deployment", value=target_deployment, expected_type=type_hints["target_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source_configurations": source_configurations,
            "target_network": target_network,
            "target_s3_configuration": target_s3_configuration,
        }
        if description is not None:
            self._values["description"] = description
        if scope_tags is not None:
            self._values["scope_tags"] = scope_tags
        if tags is not None:
            self._values["tags"] = tags
        if target_deployment is not None:
            self._values["target_deployment"] = target_deployment

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the network migration definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_configurations(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceConfigurationProperty"]]]:
        '''A list of source configurations for the network migration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-sourceconfigurations
        '''
        result = self._values.get("source_configurations")
        assert result is not None, "Required property 'source_configurations' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.List[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.SourceConfigurationProperty"]]], result)

    @builtins.property
    def target_network(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetNetworkProperty"]:
        '''Configuration for the target network topology and addressing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-targetnetwork
        '''
        result = self._values.get("target_network")
        assert result is not None, "Required property 'target_network' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetNetworkProperty"], result)

    @builtins.property
    def target_s3_configuration(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty"]:
        '''S3 configuration for storing target network artifacts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-targets3configuration
        '''
        result = self._values.get("target_s3_configuration")
        assert result is not None, "Required property 'target_s3_configuration' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the network migration definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_tags(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]]:
        '''Scope tags map for the network migration definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-scopetags
        '''
        result = self._values.get("scope_tags")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the network migration definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def target_deployment(self) -> typing.Optional[builtins.str]:
        '''The target deployment configuration for the migrated network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-networkmigrationdefinition.html#cfn-mgn-networkmigrationdefinition-targetdeployment
        '''
        result = self._values.get("target_deployment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNetworkMigrationDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.IReplicationConfigurationTemplateRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnReplicationConfigurationTemplate(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnReplicationConfigurationTemplate",
):
    '''Account level Replication Configuration Template for AWS Application Migration Service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html
    :cloudformationResource: AWS::MGN::ReplicationConfigurationTemplate
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_replication_configuration_template = mgn.CfnReplicationConfigurationTemplate(self, "MyCfnReplicationConfigurationTemplate",
            associate_default_security_group=False,
            bandwidth_throttling=123,
            create_public_ip=False,
            data_plane_routing="dataPlaneRouting",
            default_large_staging_disk_type="defaultLargeStagingDiskType",
            ebs_encryption="ebsEncryption",
            replication_server_instance_type="replicationServerInstanceType",
            replication_servers_security_groups_i_ds=["replicationServersSecurityGroupsIDs"],
            staging_area_subnet_id="stagingAreaSubnetId",
            staging_area_tags={
                "staging_area_tags_key": "stagingAreaTags"
            },
            use_dedicated_replication_server=False,
        
            # the properties below are optional
            ebs_encryption_key_arn="ebsEncryptionKeyArn",
            internet_protocol="internetProtocol",
            store_snapshot_on_local_zone=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_fips_endpoint=False
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        associate_default_security_group: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        bandwidth_throttling: jsii.Number,
        create_public_ip: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        data_plane_routing: builtins.str,
        default_large_staging_disk_type: builtins.str,
        ebs_encryption: builtins.str,
        replication_server_instance_type: builtins.str,
        replication_servers_security_groups_i_ds: typing.Sequence[builtins.str],
        staging_area_subnet_id: builtins.str,
        staging_area_tags: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]],
        use_dedicated_replication_server: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        ebs_encryption_key_arn: typing.Optional[builtins.str] = None,
        internet_protocol: typing.Optional[builtins.str] = None,
        store_snapshot_on_local_zone: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::ReplicationConfigurationTemplate``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param associate_default_security_group: Whether to associate the default Application Migration Service Security Group with the Replication Configuration Template.
        :param bandwidth_throttling: Configure bandwidth throttling for the outbound data transfer rate of the Source Server in Mbps.
        :param create_public_ip: Whether to create a Public IP for the Recovery Instance by default.
        :param data_plane_routing: The data plane routing mechanism that will be used for replication.
        :param default_large_staging_disk_type: The Staging Disk EBS volume type to be used during replication.
        :param ebs_encryption: The type of EBS encryption to be used during replication.
        :param replication_server_instance_type: The instance type to be used for the replication server.
        :param replication_servers_security_groups_i_ds: The security group IDs that will be used by the replication server.
        :param staging_area_subnet_id: The subnet to be used by the replication staging area.
        :param staging_area_tags: A set of tags to be associated with all resources created in the replication staging area: EC2 replication server, EBS volumes, EBS snapshots, etc.
        :param use_dedicated_replication_server: Whether to use a dedicated Replication Server in the replication staging area.
        :param ebs_encryption_key_arn: The ARN of the EBS encryption key to be used during replication.
        :param internet_protocol: Which internet protocol to use for replication of data.
        :param store_snapshot_on_local_zone: Whether to store the Snapshot in the Local Zone of the replication staging area subnet.
        :param tags: A set of tags to be associated with the Replication Configuration Template resource.
        :param use_fips_endpoint: Whether to use a FIPS endpoint when initiating the agent connection to the Application Migration Service service.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__32781f2f14c2c8d78bf4abf6a87ecc6d75bdddae1b176c9dad46570e16b33554)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReplicationConfigurationTemplateProps(
            associate_default_security_group=associate_default_security_group,
            bandwidth_throttling=bandwidth_throttling,
            create_public_ip=create_public_ip,
            data_plane_routing=data_plane_routing,
            default_large_staging_disk_type=default_large_staging_disk_type,
            ebs_encryption=ebs_encryption,
            replication_server_instance_type=replication_server_instance_type,
            replication_servers_security_groups_i_ds=replication_servers_security_groups_i_ds,
            staging_area_subnet_id=staging_area_subnet_id,
            staging_area_tags=staging_area_tags,
            use_dedicated_replication_server=use_dedicated_replication_server,
            ebs_encryption_key_arn=ebs_encryption_key_arn,
            internet_protocol=internet_protocol,
            store_snapshot_on_local_zone=store_snapshot_on_local_zone,
            tags=tags,
            use_fips_endpoint=use_fips_endpoint,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForReplicationConfigurationTemplate")
    @builtins.classmethod
    def arn_for_replication_configuration_template(
        cls,
        resource: "_aws_mgn_7f0ba49e.IReplicationConfigurationTemplateRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6ce02e2e66678132e4b85bde22953af2748eeef1a1e29d5089f014b0e45314d1)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForReplicationConfigurationTemplate", [resource]))

    @jsii.member(jsii_name="isCfnReplicationConfigurationTemplate")
    @builtins.classmethod
    def is_cfn_replication_configuration_template(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnReplicationConfigurationTemplate.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2e3ea8c3b6b49ef0aaa70705290180af97287bde7698aad469382d3659bd7baa)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnReplicationConfigurationTemplate", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__92ba19201ca3be736cb2cd473ef0360b28a0144aac66f932fbf8d3e4ff1eeb45)
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
            type_hints = cached_type_hints(_typecheckingstub__55ff7d01d178f0a65b3f089922c8b9f27155d901a6fb80057dd8fc2be0eae63b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Replication Configuration Template ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrReplicationConfigurationTemplateId")
    def attr_replication_configuration_template_id(self) -> builtins.str:
        '''The Replication Configuration Template ID.

        :cloudformationAttribute: ReplicationConfigurationTemplateID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReplicationConfigurationTemplateId"))

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
    @jsii.member(jsii_name="replicationConfigurationTemplateRef")
    def replication_configuration_template_ref(
        self,
    ) -> "_aws_mgn_7f0ba49e.ReplicationConfigurationTemplateReference":
        '''A reference to a ReplicationConfigurationTemplate resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.ReplicationConfigurationTemplateReference", jsii.get(self, "replicationConfigurationTemplateRef"))

    @builtins.property
    @jsii.member(jsii_name="associateDefaultSecurityGroup")
    def associate_default_security_group(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to associate the default Application Migration Service Security Group with the Replication Configuration Template.'''
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], jsii.get(self, "associateDefaultSecurityGroup"))

    @associate_default_security_group.setter
    def associate_default_security_group(
        self,
        value: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4a55a312add5ea1721846ac96c6979bd7df2cbb9d83fa93c5dfcbdbf58930dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associateDefaultSecurityGroup", value)

    @builtins.property
    @jsii.member(jsii_name="bandwidthThrottling")
    def bandwidth_throttling(self) -> jsii.Number:
        '''Configure bandwidth throttling for the outbound data transfer rate of the Source Server in Mbps.'''
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthThrottling"))

    @bandwidth_throttling.setter
    def bandwidth_throttling(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bc06316b5649417905f9b57846849e0aaa1269d3630aff4c13953561835a25cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthThrottling", value)

    @builtins.property
    @jsii.member(jsii_name="createPublicIp")
    def create_public_ip(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to create a Public IP for the Recovery Instance by default.'''
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], jsii.get(self, "createPublicIp"))

    @create_public_ip.setter
    def create_public_ip(
        self,
        value: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__211b56ab254fa8ef4afb7a2dbff296a15ac8d2cf107513874ca73d4307dea17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createPublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="dataPlaneRouting")
    def data_plane_routing(self) -> builtins.str:
        '''The data plane routing mechanism that will be used for replication.'''
        return typing.cast(builtins.str, jsii.get(self, "dataPlaneRouting"))

    @data_plane_routing.setter
    def data_plane_routing(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6877e5d1200a4f43704b5b44c71a2cfc89de1f5ae1bd0989e6589b770431e329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataPlaneRouting", value)

    @builtins.property
    @jsii.member(jsii_name="defaultLargeStagingDiskType")
    def default_large_staging_disk_type(self) -> builtins.str:
        '''The Staging Disk EBS volume type to be used during replication.'''
        return typing.cast(builtins.str, jsii.get(self, "defaultLargeStagingDiskType"))

    @default_large_staging_disk_type.setter
    def default_large_staging_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__08cf51473da8d81e72be572ec79fbe911d8b3c6403e1ea79f5cabb9ba5643cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLargeStagingDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="ebsEncryption")
    def ebs_encryption(self) -> builtins.str:
        '''The type of EBS encryption to be used during replication.'''
        return typing.cast(builtins.str, jsii.get(self, "ebsEncryption"))

    @ebs_encryption.setter
    def ebs_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4e6b181e2afd8523796a1c0dc8443f9849298c251e7964a5c1bedc21ee55de88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="replicationServerInstanceType")
    def replication_server_instance_type(self) -> builtins.str:
        '''The instance type to be used for the replication server.'''
        return typing.cast(builtins.str, jsii.get(self, "replicationServerInstanceType"))

    @replication_server_instance_type.setter
    def replication_server_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e97289041da4c1488dce37170b0c27c277b3c8f68a2e9864ffbb35846ca21fea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationServerInstanceType", value)

    @builtins.property
    @jsii.member(jsii_name="replicationServersSecurityGroupsIDs")
    def replication_servers_security_groups_i_ds(self) -> typing.List[builtins.str]:
        '''The security group IDs that will be used by the replication server.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicationServersSecurityGroupsIDs"))

    @replication_servers_security_groups_i_ds.setter
    def replication_servers_security_groups_i_ds(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__434ca76c12e7dfbc3d2ce3e607dae750c93b082c986f74085b27a7af357c9c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationServersSecurityGroupsIDs", value)

    @builtins.property
    @jsii.member(jsii_name="stagingAreaSubnetId")
    def staging_area_subnet_id(self) -> builtins.str:
        '''The subnet to be used by the replication staging area.'''
        return typing.cast(builtins.str, jsii.get(self, "stagingAreaSubnetId"))

    @staging_area_subnet_id.setter
    def staging_area_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__080cf09c8d82c8e3639c95e1c8ba7990a7e214a9e9d6a9cd072f2eac7b993898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingAreaSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="stagingAreaTags")
    def staging_area_tags(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]:
        '''A set of tags to be associated with all resources created in the replication staging area: EC2 replication server, EBS volumes, EBS snapshots, etc.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "stagingAreaTags"))

    @staging_area_tags.setter
    def staging_area_tags(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__22073edbb351ba0a52e2970959f907982c21731f202bb57e0e8a7c954e99de5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingAreaTags", value)

    @builtins.property
    @jsii.member(jsii_name="useDedicatedReplicationServer")
    def use_dedicated_replication_server(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to use a dedicated Replication Server in the replication staging area.'''
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], jsii.get(self, "useDedicatedReplicationServer"))

    @use_dedicated_replication_server.setter
    def use_dedicated_replication_server(
        self,
        value: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0a3b2e27a1397fe936891f77b2ce8a3ab9a417c7410c1f4174e1a25be12e9333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDedicatedReplicationServer", value)

    @builtins.property
    @jsii.member(jsii_name="ebsEncryptionKeyArn")
    def ebs_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the EBS encryption key to be used during replication.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsEncryptionKeyArn"))

    @ebs_encryption_key_arn.setter
    def ebs_encryption_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9d6ef3ac289c132d986af48a46eccc060ede11b30ec8001b93fa0711cf8ac3bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsEncryptionKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="internetProtocol")
    def internet_protocol(self) -> typing.Optional[builtins.str]:
        '''Which internet protocol to use for replication of data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "internetProtocol"))

    @internet_protocol.setter
    def internet_protocol(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__749fb38fd993044faf9648334266aad28bbe9a6beba7c27bd7df1012b3a22c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internetProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="storeSnapshotOnLocalZone")
    def store_snapshot_on_local_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to store the Snapshot in the Local Zone of the replication staging area subnet.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "storeSnapshotOnLocalZone"))

    @store_snapshot_on_local_zone.setter
    def store_snapshot_on_local_zone(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aead1c6d5757434932bae9edfc4409ceefa91a40ce545c6ebde335cc21b5899e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeSnapshotOnLocalZone", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to be associated with the Replication Configuration Template resource.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6aac53cd61c0cb107d4cac5f134cbbe611ef811d92ae056f3b7a560a36e92e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="useFipsEndpoint")
    def use_fips_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to use a FIPS endpoint when initiating the agent connection to the Application Migration Service service.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "useFipsEndpoint"))

    @use_fips_endpoint.setter
    def use_fips_endpoint(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1dec32218d9ce20c2a207e4f2bc3c2f7c4e6a2015566a72f4f6304d21e838483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFipsEndpoint", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnReplicationConfigurationTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "associate_default_security_group": "associateDefaultSecurityGroup",
        "bandwidth_throttling": "bandwidthThrottling",
        "create_public_ip": "createPublicIp",
        "data_plane_routing": "dataPlaneRouting",
        "default_large_staging_disk_type": "defaultLargeStagingDiskType",
        "ebs_encryption": "ebsEncryption",
        "replication_server_instance_type": "replicationServerInstanceType",
        "replication_servers_security_groups_i_ds": "replicationServersSecurityGroupsIDs",
        "staging_area_subnet_id": "stagingAreaSubnetId",
        "staging_area_tags": "stagingAreaTags",
        "use_dedicated_replication_server": "useDedicatedReplicationServer",
        "ebs_encryption_key_arn": "ebsEncryptionKeyArn",
        "internet_protocol": "internetProtocol",
        "store_snapshot_on_local_zone": "storeSnapshotOnLocalZone",
        "tags": "tags",
        "use_fips_endpoint": "useFipsEndpoint",
    },
)
class CfnReplicationConfigurationTemplateProps:
    def __init__(
        self,
        *,
        associate_default_security_group: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        bandwidth_throttling: jsii.Number,
        create_public_ip: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        data_plane_routing: builtins.str,
        default_large_staging_disk_type: builtins.str,
        ebs_encryption: builtins.str,
        replication_server_instance_type: builtins.str,
        replication_servers_security_groups_i_ds: typing.Sequence[builtins.str],
        staging_area_subnet_id: builtins.str,
        staging_area_tags: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]],
        use_dedicated_replication_server: typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"],
        ebs_encryption_key_arn: typing.Optional[builtins.str] = None,
        internet_protocol: typing.Optional[builtins.str] = None,
        store_snapshot_on_local_zone: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
        use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReplicationConfigurationTemplate``.

        :param associate_default_security_group: Whether to associate the default Application Migration Service Security Group with the Replication Configuration Template.
        :param bandwidth_throttling: Configure bandwidth throttling for the outbound data transfer rate of the Source Server in Mbps.
        :param create_public_ip: Whether to create a Public IP for the Recovery Instance by default.
        :param data_plane_routing: The data plane routing mechanism that will be used for replication.
        :param default_large_staging_disk_type: The Staging Disk EBS volume type to be used during replication.
        :param ebs_encryption: The type of EBS encryption to be used during replication.
        :param replication_server_instance_type: The instance type to be used for the replication server.
        :param replication_servers_security_groups_i_ds: The security group IDs that will be used by the replication server.
        :param staging_area_subnet_id: The subnet to be used by the replication staging area.
        :param staging_area_tags: A set of tags to be associated with all resources created in the replication staging area: EC2 replication server, EBS volumes, EBS snapshots, etc.
        :param use_dedicated_replication_server: Whether to use a dedicated Replication Server in the replication staging area.
        :param ebs_encryption_key_arn: The ARN of the EBS encryption key to be used during replication.
        :param internet_protocol: Which internet protocol to use for replication of data.
        :param store_snapshot_on_local_zone: Whether to store the Snapshot in the Local Zone of the replication staging area subnet.
        :param tags: A set of tags to be associated with the Replication Configuration Template resource.
        :param use_fips_endpoint: Whether to use a FIPS endpoint when initiating the agent connection to the Application Migration Service service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_replication_configuration_template_props = mgn.CfnReplicationConfigurationTemplateProps(
                associate_default_security_group=False,
                bandwidth_throttling=123,
                create_public_ip=False,
                data_plane_routing="dataPlaneRouting",
                default_large_staging_disk_type="defaultLargeStagingDiskType",
                ebs_encryption="ebsEncryption",
                replication_server_instance_type="replicationServerInstanceType",
                replication_servers_security_groups_i_ds=["replicationServersSecurityGroupsIDs"],
                staging_area_subnet_id="stagingAreaSubnetId",
                staging_area_tags={
                    "staging_area_tags_key": "stagingAreaTags"
                },
                use_dedicated_replication_server=False,
            
                # the properties below are optional
                ebs_encryption_key_arn="ebsEncryptionKeyArn",
                internet_protocol="internetProtocol",
                store_snapshot_on_local_zone=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_fips_endpoint=False
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5b57e63d8f29aa082c5b0b13e008f60fbc91e8012065b7e95c46e52799f7c90a)
            check_type(argname="argument associate_default_security_group", value=associate_default_security_group, expected_type=type_hints["associate_default_security_group"])
            check_type(argname="argument bandwidth_throttling", value=bandwidth_throttling, expected_type=type_hints["bandwidth_throttling"])
            check_type(argname="argument create_public_ip", value=create_public_ip, expected_type=type_hints["create_public_ip"])
            check_type(argname="argument data_plane_routing", value=data_plane_routing, expected_type=type_hints["data_plane_routing"])
            check_type(argname="argument default_large_staging_disk_type", value=default_large_staging_disk_type, expected_type=type_hints["default_large_staging_disk_type"])
            check_type(argname="argument ebs_encryption", value=ebs_encryption, expected_type=type_hints["ebs_encryption"])
            check_type(argname="argument replication_server_instance_type", value=replication_server_instance_type, expected_type=type_hints["replication_server_instance_type"])
            check_type(argname="argument replication_servers_security_groups_i_ds", value=replication_servers_security_groups_i_ds, expected_type=type_hints["replication_servers_security_groups_i_ds"])
            check_type(argname="argument staging_area_subnet_id", value=staging_area_subnet_id, expected_type=type_hints["staging_area_subnet_id"])
            check_type(argname="argument staging_area_tags", value=staging_area_tags, expected_type=type_hints["staging_area_tags"])
            check_type(argname="argument use_dedicated_replication_server", value=use_dedicated_replication_server, expected_type=type_hints["use_dedicated_replication_server"])
            check_type(argname="argument ebs_encryption_key_arn", value=ebs_encryption_key_arn, expected_type=type_hints["ebs_encryption_key_arn"])
            check_type(argname="argument internet_protocol", value=internet_protocol, expected_type=type_hints["internet_protocol"])
            check_type(argname="argument store_snapshot_on_local_zone", value=store_snapshot_on_local_zone, expected_type=type_hints["store_snapshot_on_local_zone"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_fips_endpoint", value=use_fips_endpoint, expected_type=type_hints["use_fips_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "associate_default_security_group": associate_default_security_group,
            "bandwidth_throttling": bandwidth_throttling,
            "create_public_ip": create_public_ip,
            "data_plane_routing": data_plane_routing,
            "default_large_staging_disk_type": default_large_staging_disk_type,
            "ebs_encryption": ebs_encryption,
            "replication_server_instance_type": replication_server_instance_type,
            "replication_servers_security_groups_i_ds": replication_servers_security_groups_i_ds,
            "staging_area_subnet_id": staging_area_subnet_id,
            "staging_area_tags": staging_area_tags,
            "use_dedicated_replication_server": use_dedicated_replication_server,
        }
        if ebs_encryption_key_arn is not None:
            self._values["ebs_encryption_key_arn"] = ebs_encryption_key_arn
        if internet_protocol is not None:
            self._values["internet_protocol"] = internet_protocol
        if store_snapshot_on_local_zone is not None:
            self._values["store_snapshot_on_local_zone"] = store_snapshot_on_local_zone
        if tags is not None:
            self._values["tags"] = tags
        if use_fips_endpoint is not None:
            self._values["use_fips_endpoint"] = use_fips_endpoint

    @builtins.property
    def associate_default_security_group(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to associate the default Application Migration Service Security Group with the Replication Configuration Template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-associatedefaultsecuritygroup
        '''
        result = self._values.get("associate_default_security_group")
        assert result is not None, "Required property 'associate_default_security_group' is missing"
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

    @builtins.property
    def bandwidth_throttling(self) -> jsii.Number:
        '''Configure bandwidth throttling for the outbound data transfer rate of the Source Server in Mbps.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-bandwidththrottling
        '''
        result = self._values.get("bandwidth_throttling")
        assert result is not None, "Required property 'bandwidth_throttling' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def create_public_ip(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to create a Public IP for the Recovery Instance by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-createpublicip
        '''
        result = self._values.get("create_public_ip")
        assert result is not None, "Required property 'create_public_ip' is missing"
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

    @builtins.property
    def data_plane_routing(self) -> builtins.str:
        '''The data plane routing mechanism that will be used for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-dataplanerouting
        '''
        result = self._values.get("data_plane_routing")
        assert result is not None, "Required property 'data_plane_routing' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_large_staging_disk_type(self) -> builtins.str:
        '''The Staging Disk EBS volume type to be used during replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-defaultlargestagingdisktype
        '''
        result = self._values.get("default_large_staging_disk_type")
        assert result is not None, "Required property 'default_large_staging_disk_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ebs_encryption(self) -> builtins.str:
        '''The type of EBS encryption to be used during replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-ebsencryption
        '''
        result = self._values.get("ebs_encryption")
        assert result is not None, "Required property 'ebs_encryption' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_server_instance_type(self) -> builtins.str:
        '''The instance type to be used for the replication server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-replicationserverinstancetype
        '''
        result = self._values.get("replication_server_instance_type")
        assert result is not None, "Required property 'replication_server_instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_servers_security_groups_i_ds(self) -> typing.List[builtins.str]:
        '''The security group IDs that will be used by the replication server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-replicationserverssecuritygroupsids
        '''
        result = self._values.get("replication_servers_security_groups_i_ds")
        assert result is not None, "Required property 'replication_servers_security_groups_i_ds' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def staging_area_subnet_id(self) -> builtins.str:
        '''The subnet to be used by the replication staging area.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-stagingareasubnetid
        '''
        result = self._values.get("staging_area_subnet_id")
        assert result is not None, "Required property 'staging_area_subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def staging_area_tags(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]]:
        '''A set of tags to be associated with all resources created in the replication staging area: EC2 replication server, EBS volumes, EBS snapshots, etc.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-stagingareatags
        '''
        result = self._values.get("staging_area_tags")
        assert result is not None, "Required property 'staging_area_tags' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def use_dedicated_replication_server(
        self,
    ) -> typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]:
        '''Whether to use a dedicated Replication Server in the replication staging area.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-usededicatedreplicationserver
        '''
        result = self._values.get("use_dedicated_replication_server")
        assert result is not None, "Required property 'use_dedicated_replication_server' is missing"
        return typing.cast(typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"], result)

    @builtins.property
    def ebs_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the EBS encryption key to be used during replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-ebsencryptionkeyarn
        '''
        result = self._values.get("ebs_encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_protocol(self) -> typing.Optional[builtins.str]:
        '''Which internet protocol to use for replication of data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-internetprotocol
        '''
        result = self._values.get("internet_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def store_snapshot_on_local_zone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to store the Snapshot in the Local Zone of the replication staging area subnet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-storesnapshotonlocalzone
        '''
        result = self._values.get("store_snapshot_on_local_zone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''A set of tags to be associated with the Replication Configuration Template resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    @builtins.property
    def use_fips_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Whether to use a FIPS endpoint when initiating the agent connection to the Application Migration Service service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-replicationconfigurationtemplate.html#cfn-mgn-replicationconfigurationtemplate-usefipsendpoint
        '''
        result = self._values.get("use_fips_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationConfigurationTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_mgn_7f0ba49e.IWaveRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnWave(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_mgn.CfnWave",
):
    '''Resource schema for AWS::MGN::Wave.

    A Wave is a logical grouping used in Application Migration Service to organize and manage the migration of applications.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-wave.html
    :cloudformationResource: AWS::MGN::Wave
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_mgn as mgn
        
        cfn_wave = mgn.CfnWave(self, "MyCfnWave",
            name="name",
        
            # the properties below are optional
            description="description",
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
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MGN::Wave``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: The name of the wave.
        :param description: A description of the wave.
        :param tags: Tags to assign to the wave.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1590471d8db8f7f297f18abcb280be0d6095ac004e7b789cc90367527db059f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWaveProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForWave")
    @builtins.classmethod
    def arn_for_wave(cls, resource: "_aws_mgn_7f0ba49e.IWaveRef") -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2b32cd2dcb853be5ea0d24d79674138f2c7b64139d9367f640784777533c362a)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForWave", [resource]))

    @jsii.member(jsii_name="isCfnWave")
    @builtins.classmethod
    def is_cfn_wave(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnWave.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c43beb17d137546057a6d0c8e47963d0c516425b5e80eec8110014b54d5a72f1)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnWave", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ab6a4c6fdb22694cafc6881ef37ce5ed10f3a9b99e52a5a81cf970300bcfd830)
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
            type_hints = cached_type_hints(_typecheckingstub__8fc9d8fc03707b068c3e9c53bb4b96dab2a58d188d19944aaaddd06599245815)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the wave.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The timestamp when the wave was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrIsArchived")
    def attr_is_archived(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Whether the wave is archived.

        :cloudformationAttribute: IsArchived
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrIsArchived"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModifiedDateTime")
    def attr_last_modified_date_time(self) -> builtins.str:
        '''The timestamp when the wave was last modified.

        :cloudformationAttribute: LastModifiedDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModifiedDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrWaveAggregatedStatus")
    def attr_wave_aggregated_status(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The aggregated migration status of the wave.

        :cloudformationAttribute: WaveAggregatedStatus
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrWaveAggregatedStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrWaveId")
    def attr_wave_id(self) -> builtins.str:
        '''The unique identifier of the wave.

        :cloudformationAttribute: WaveID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWaveId"))

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
    @jsii.member(jsii_name="waveRef")
    def wave_ref(self) -> "_aws_mgn_7f0ba49e.WaveReference":
        '''A reference to a Wave resource.'''
        return typing.cast("_aws_mgn_7f0ba49e.WaveReference", jsii.get(self, "waveRef"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the wave.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ffa1dfc40562bada1a2343392a53725ce5001079945064c1d398dc125540f65b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the wave.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__37d9976edfcbf92c898e2fec40cc39475b9665ea8f2addf01ba95e256ee70a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the wave.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b6c237acb5b1c135957b67915b5c8da7a6fe1c008a169f51e6dee951c03da970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_mgn.CfnWave.WaveAggregatedStatusProperty",
        jsii_struct_bases=[],
        name_mapping={
            "health_status": "healthStatus",
            "progress_status": "progressStatus",
            "total_applications": "totalApplications",
        },
    )
    class WaveAggregatedStatusProperty:
        def __init__(
            self,
            *,
            health_status: typing.Optional[builtins.str] = None,
            progress_status: typing.Optional[builtins.str] = None,
            total_applications: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The aggregated migration status of the wave.

            :param health_status: The health status of the wave.
            :param progress_status: The progress status of the wave.
            :param total_applications: The total number of applications in the wave.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-wave-waveaggregatedstatus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_mgn as mgn
                
                wave_aggregated_status_property = mgn.CfnWave.WaveAggregatedStatusProperty(
                    health_status="healthStatus",
                    progress_status="progressStatus",
                    total_applications=123
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__e306721fd72b0a018a7dc6c2fb77110be58a4234b0bd0f229da2f720ed5e3a40)
                check_type(argname="argument health_status", value=health_status, expected_type=type_hints["health_status"])
                check_type(argname="argument progress_status", value=progress_status, expected_type=type_hints["progress_status"])
                check_type(argname="argument total_applications", value=total_applications, expected_type=type_hints["total_applications"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_status is not None:
                self._values["health_status"] = health_status
            if progress_status is not None:
                self._values["progress_status"] = progress_status
            if total_applications is not None:
                self._values["total_applications"] = total_applications

        @builtins.property
        def health_status(self) -> typing.Optional[builtins.str]:
            '''The health status of the wave.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-wave-waveaggregatedstatus.html#cfn-mgn-wave-waveaggregatedstatus-healthstatus
            '''
            result = self._values.get("health_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def progress_status(self) -> typing.Optional[builtins.str]:
            '''The progress status of the wave.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-wave-waveaggregatedstatus.html#cfn-mgn-wave-waveaggregatedstatus-progressstatus
            '''
            result = self._values.get("progress_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def total_applications(self) -> typing.Optional[jsii.Number]:
            '''The total number of applications in the wave.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mgn-wave-waveaggregatedstatus.html#cfn-mgn-wave-waveaggregatedstatus-totalapplications
            '''
            result = self._values.get("total_applications")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WaveAggregatedStatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_mgn.CfnWaveProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnWaveProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWave``.

        :param name: The name of the wave.
        :param description: A description of the wave.
        :param tags: Tags to assign to the wave.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-wave.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_mgn as mgn
            
            cfn_wave_props = mgn.CfnWaveProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__68968c8c0cb4c03172bfd9d3608c9b579d5042521a8611cb30247839f57f6b05)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the wave.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-wave.html#cfn-mgn-wave-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the wave.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-wave.html#cfn-mgn-wave-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Tags to assign to the wave.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mgn-wave.html#cfn-mgn-wave-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnConnector",
    "CfnConnectorProps",
    "CfnLaunchConfigurationTemplate",
    "CfnLaunchConfigurationTemplateProps",
    "CfnNetworkMigrationDefinition",
    "CfnNetworkMigrationDefinitionProps",
    "CfnReplicationConfigurationTemplate",
    "CfnReplicationConfigurationTemplateProps",
    "CfnWave",
    "CfnWaveProps",
]

publication.publish()

def _typecheckingstub__3dda22f820c3748889315357f7f8d8808142d4bbe6e78fa2169f112bb0f1aab4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda45874557c2da2d1cb406c9e553d28f4a4f0bce1860372b45e0a67699cdd2d(
    resource: _aws_mgn_7f0ba49e.IApplicationRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499dd71a3d3df5437f9a4e19a080f3b5db107fd9b022a77e34e59bf0caf6eff1(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee867837d27bb3d1e190e3a8ed61c22c3cccbfcc32ab5a63dece4b96783fe1b9(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d7bb6250ea5535971502f33ae78665bfc5b20337d5bdf66f16a0438bf00472(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eca8e4ce863fae79d00a7dd6e50472226240b48abaee7eef8b8c78512ac2cbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e666f8444740767b11735b73024aa0a6477f77e2eececae78a7318ab87ca0ce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dff4ca7b322d329ac080906ceecb610d62b9f6784d7997eb261041c910a0e85(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1a40f46582952499bc335293aa0de7470b33b01b5ce361f3cdb38bab496e97(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1009ba5960ab3691b98cd0782c80f689e21000b6c903683a2672ab7ba794a126(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    ssm_instance_id: builtins.str,
    ssm_command_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnConnector.ConnectorSsmCommandConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a32287b1f062fc70060093299724663384337cf9ca819fefad38cec6bd0af8(
    resource: _aws_mgn_7f0ba49e.IConnectorRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611e506d864ec2ff274adc77ee1de6c2387eaa38a610ca5aaa2e770b659cb5ec(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28142cdb5dd62e111bc45361cbd48636711889d6b2e8eeebad0834c32bba1d9(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e2086da01ebdadad16f108ac3cbba59789ba2a0c0180ca8b358812507016e9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2360c01e39e2abd04cc142761ec5ad9bf2014769e3feee71dee12b936589b7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c969ac30ea400d91a13596c32a88e67342e3e494560406753557e40b0c5414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e391c1b5ed08e4613fd1ce7e6af8aa16512f8ef8b60d6cf6ed5ea6a360e67b(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnConnector.ConnectorSsmCommandConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbcdd84ad1148215dd898e861326eb4847251dc142e777f24c36d87887edd9ab(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be748cf81b7c3877ac0c5a8c6889e285776316c0f9a45b5c0907407ccadfcd9(
    *,
    cloud_watch_output_enabled: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    s3_output_enabled: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    output_s3_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfdf7308d5e774a55e16d6f427b8f1b29b8342ea3eafbf72d21afc99670bb48(
    *,
    name: builtins.str,
    ssm_instance_id: builtins.str,
    ssm_command_config: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnConnector.ConnectorSsmCommandConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef03edb0bde55472bcaf13434e6be51dd9adda59fef8102636df1985b9dcffa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    boot_mode: typing.Optional[builtins.str] = None,
    copy_private_ip: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    enable_map_auto_tagging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    enable_parameters_encryption: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    large_volume_conf: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    launch_disposition: typing.Optional[builtins.str] = None,
    licensing: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LicensingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    map_auto_tagging_mpe_id: typing.Optional[builtins.str] = None,
    parameters_encryption_key: typing.Optional[builtins.str] = None,
    post_launch_actions: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.PostLaunchActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    small_volume_conf: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    small_volume_max_size: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_instance_type_right_sizing_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936a4c3d3f9a54bc73dcff3c5bfeece8f7d89a1cc33560737c4b7d43de8b13a1(
    resource: _aws_mgn_7f0ba49e.ILaunchConfigurationTemplateRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cac804cc2774e9b12bd440713e222c4096569266c27eddc711f0ed55f6c44ae(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae22e88eb3ea69da7242e66f7efd25627741fb6b41166eaa0d6d51cf70a264a7(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1a19d7a92eb4f026bfdb0d4bf32234d656210d1c3b1623d9168fd575e8fb68(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb81319ccde12f4ac3668a4f6626e97f42379e2ade48439e00ddad50d11e307(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e305a35308d10974f4c7a6a48ebc4fb2a4b26a3409d1782b174b2a18e677545(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33bf06397f65bbd180b94f01ce0500f7399108c26d5215412920d73d3a59ebd1(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d53f514011c8a6bdffff82fa33f170118d61fbfd1388e3a7a679a28728571c3(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354911b4a5f7f8fff29d172315e37e7b5f20d742bc5f92908958c433167176ef(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cceff17d854c4f1d187787cb0c0a0ee834cb58817e70612eb85cc9252d4a04(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d52d2fb041c92f68ccc20bca1ea4a0c8bf709639403b9fcbddf00d30a61af89(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fc80841b1f61d5996ccbe63dd8a32adb8ad48cb95185b0f3e47f721efa75e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6940030110ee61928330e31366dbd86895fb9f347ce228cbc5d86014e793367b(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnLaunchConfigurationTemplate.LicensingProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458175bde67d8b9fdd0494380089b0fcaa65acfa66aafd3c7386014665a577b4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986d2dc3edffc815aebca3b17e5f9279c3ee1a0a064600363e4fb25f2f83f042(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c86780add8d852573d56138f583eb5d0a7a12af7b08260bd94bad8b5cd45c9(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnLaunchConfigurationTemplate.PostLaunchActionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c198de7f2c124d8f95b560b0aca1e4227407e8d801f1b4cd5d1581e9851ed1b2(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce6bf16723f22750621375344c1b6d55a2a252fa135d330e3cb305f1c44059f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99936035b36e5b429e8ca3e56383b1c9339040797d1488a3d5019762e9374a99(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21669f94c81d0f530fc8b55385817623a899258e521f5b2153209ba9d6eae4b2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452a08df9218a99bbd69bf2e96cb39dee9a26fae627afc9f33be4136fd02cfd1(
    *,
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6122ea07854f4031df2ac73f0d80dbc3cd6e14b76db0d9c407c2f8c168c6cc3(
    *,
    os_byol: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b06c309fc890fd02f67a5bd15c8bd3846009f539439bbed5263f060daff549(
    *,
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    deployment: typing.Optional[builtins.str] = None,
    s3_log_bucket: typing.Optional[builtins.str] = None,
    s3_output_key_prefix: typing.Optional[builtins.str] = None,
    ssm_documents: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.SsmDocumentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6135a5510bec3a9f6e1828dcdbef9dfb0d4653faf46390b91f21350ffc8477(
    *,
    action_name: builtins.str,
    ssm_document_name: builtins.str,
    external_parameters: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.SsmExternalParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    must_succeed_for_cutover: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.SsmParameterStoreParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a4180a313c1557a092c3453e69b3520041a0d5e63f452ca7878fc8d2c410d3(
    *,
    dynamic_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8343fa74b4c119ea1e29e2decf1b3e6d44bcd2fa2e29d1390bfe9f1eaa1e2004(
    *,
    parameter_name: builtins.str,
    parameter_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049d62ecccf18ceb0b801ca363d50fe7c2d95486a27446b157bea4507dd7b77f(
    *,
    associate_public_ip_address: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    boot_mode: typing.Optional[builtins.str] = None,
    copy_private_ip: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    copy_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    enable_map_auto_tagging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    enable_parameters_encryption: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    large_volume_conf: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    launch_disposition: typing.Optional[builtins.str] = None,
    licensing: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LicensingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    map_auto_tagging_mpe_id: typing.Optional[builtins.str] = None,
    parameters_encryption_key: typing.Optional[builtins.str] = None,
    post_launch_actions: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.PostLaunchActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    small_volume_conf: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLaunchConfigurationTemplate.LaunchTemplateDiskConfProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    small_volume_max_size: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_instance_type_right_sizing_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0281edcee00498148c7ba7f314fa799a30c9cdc3b6426d2f772de0035e619f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    source_configurations: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    target_network: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.TargetNetworkProperty, typing.Dict[builtins.str, typing.Any]]],
    target_s3_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    scope_tags: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_deployment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149dd6c760e0d5dd62132512d09ad41e09534515b194919d50fe45e71c5e5b63(
    resource: _aws_mgn_7f0ba49e.INetworkMigrationDefinitionRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20189b7c7a331a0b80c6992064c1d31d7feefcb9e90eda07363eecfd4c52c078(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa25ba733421d0f71f5451003b6ac4ff710428a39c26b30fec8f369543ce50f(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648966bc98e578f126765169f37f44bcd259b27a939d861bd8d9724fe439512b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb9a7cae80221f9f6a6a2c0b6651db1bf5e6824cb80b97c9c70aa7c444ab28f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70b4cfffce0b8aaebb121b276c89bc1e9ab93c05852aad015b3a23a22760f5f(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.List[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnNetworkMigrationDefinition.SourceConfigurationProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1cbcd24cf20a1903c584f1e4eda1240e760fc13799b9c8f33e898857360ed6(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnNetworkMigrationDefinition.TargetNetworkProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33aaf0e4432fb060b80bb283536a477edb3c1abe8dd20da2fd8bb7f9fbae5cb9(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6550bf9f89012ac37c95d11e738384a548b37599732330f4724f5f30291703(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f034fd9414240cb5468ffdcfb046caf9c51f5a4b5f67455118206514533d0b1f(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5cbcf1364554341e91a14e2f83599f70dc4d6829c2b9d5f539517e76e80179(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1ea8c1d9f889b5c5f0d0f564932da09f5aa885de39152f07e4b3f2ca32fc61(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03ccb7f1f8f26d65f3920a7a637ebeb3713faac932af41434a59fee43a702bd(
    *,
    source_environment: builtins.str,
    source_s3_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.SourceS3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd02649169db7f73886bfccb202933332f616adc6cdc671056a5a274724646e(
    *,
    s3_bucket: builtins.str,
    s3_bucket_owner: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb70ad8195a8a3b6bdaf88f7cb9324c35874b1a254ee13a628f7e5442cd0c82(
    *,
    topology: builtins.str,
    inbound_cidr: typing.Optional[builtins.str] = None,
    inspection_cidr: typing.Optional[builtins.str] = None,
    outbound_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0f2d69075166bf24090489d67f01d6cb44e7c61cae821ea446243318f9e1bf(
    *,
    s3_bucket: builtins.str,
    s3_bucket_owner: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e818ac919a41cc3b4e605f6633f673a768f2462b9a4b3d1966d51ea457840d55(
    *,
    name: builtins.str,
    source_configurations: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Sequence[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]],
    target_network: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.TargetNetworkProperty, typing.Dict[builtins.str, typing.Any]]],
    target_s3_configuration: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnNetworkMigrationDefinition.TargetS3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    scope_tags: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_deployment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32781f2f14c2c8d78bf4abf6a87ecc6d75bdddae1b176c9dad46570e16b33554(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    associate_default_security_group: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    bandwidth_throttling: jsii.Number,
    create_public_ip: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    data_plane_routing: builtins.str,
    default_large_staging_disk_type: builtins.str,
    ebs_encryption: builtins.str,
    replication_server_instance_type: builtins.str,
    replication_servers_security_groups_i_ds: typing.Sequence[builtins.str],
    staging_area_subnet_id: builtins.str,
    staging_area_tags: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    use_dedicated_replication_server: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    ebs_encryption_key_arn: typing.Optional[builtins.str] = None,
    internet_protocol: typing.Optional[builtins.str] = None,
    store_snapshot_on_local_zone: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce02e2e66678132e4b85bde22953af2748eeef1a1e29d5089f014b0e45314d1(
    resource: _aws_mgn_7f0ba49e.IReplicationConfigurationTemplateRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3ea8c3b6b49ef0aaa70705290180af97287bde7698aad469382d3659bd7baa(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ba19201ca3be736cb2cd473ef0360b28a0144aac66f932fbf8d3e4ff1eeb45(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ff7d01d178f0a65b3f089922c8b9f27155d901a6fb80057dd8fc2be0eae63b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a55a312add5ea1721846ac96c6979bd7df2cbb9d83fa93c5dfcbdbf58930dcc(
    value: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc06316b5649417905f9b57846849e0aaa1269d3630aff4c13953561835a25cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211b56ab254fa8ef4afb7a2dbff296a15ac8d2cf107513874ca73d4307dea17d(
    value: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6877e5d1200a4f43704b5b44c71a2cfc89de1f5ae1bd0989e6589b770431e329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cf51473da8d81e72be572ec79fbe911d8b3c6403e1ea79f5cabb9ba5643cc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6b181e2afd8523796a1c0dc8443f9849298c251e7964a5c1bedc21ee55de88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97289041da4c1488dce37170b0c27c277b3c8f68a2e9864ffbb35846ca21fea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434ca76c12e7dfbc3d2ce3e607dae750c93b082c986f74085b27a7af357c9c29(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080cf09c8d82c8e3639c95e1c8ba7990a7e214a9e9d6a9cd072f2eac7b993898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22073edbb351ba0a52e2970959f907982c21731f202bb57e0e8a7c954e99de5b(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3b2e27a1397fe936891f77b2ce8a3ab9a417c7410c1f4174e1a25be12e9333(
    value: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6ef3ac289c132d986af48a46eccc060ede11b30ec8001b93fa0711cf8ac3bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749fb38fd993044faf9648334266aad28bbe9a6beba7c27bd7df1012b3a22c55(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aead1c6d5757434932bae9edfc4409ceefa91a40ce545c6ebde335cc21b5899e(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aac53cd61c0cb107d4cac5f134cbbe611ef811d92ae056f3b7a560a36e92e18(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dec32218d9ce20c2a207e4f2bc3c2f7c4e6a2015566a72f4f6304d21e838483(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b57e63d8f29aa082c5b0b13e008f60fbc91e8012065b7e95c46e52799f7c90a(
    *,
    associate_default_security_group: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    bandwidth_throttling: jsii.Number,
    create_public_ip: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    data_plane_routing: builtins.str,
    default_large_staging_disk_type: builtins.str,
    ebs_encryption: builtins.str,
    replication_server_instance_type: builtins.str,
    replication_servers_security_groups_i_ds: typing.Sequence[builtins.str],
    staging_area_subnet_id: builtins.str,
    staging_area_tags: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    use_dedicated_replication_server: typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable],
    ebs_encryption_key_arn: typing.Optional[builtins.str] = None,
    internet_protocol: typing.Optional[builtins.str] = None,
    store_snapshot_on_local_zone: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_fips_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1590471d8db8f7f297f18abcb280be0d6095ac004e7b789cc90367527db059f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b32cd2dcb853be5ea0d24d79674138f2c7b64139d9367f640784777533c362a(
    resource: _aws_mgn_7f0ba49e.IWaveRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43beb17d137546057a6d0c8e47963d0c516425b5e80eec8110014b54d5a72f1(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6a4c6fdb22694cafc6881ef37ce5ed10f3a9b99e52a5a81cf970300bcfd830(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc9d8fc03707b068c3e9c53bb4b96dab2a58d188d19944aaaddd06599245815(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa1dfc40562bada1a2343392a53725ce5001079945064c1d398dc125540f65b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d9976edfcbf92c898e2fec40cc39475b9665ea8f2addf01ba95e256ee70a69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c237acb5b1c135957b67915b5c8da7a6fe1c008a169f51e6dee951c03da970(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e306721fd72b0a018a7dc6c2fb77110be58a4234b0bd0f229da2f720ed5e3a40(
    *,
    health_status: typing.Optional[builtins.str] = None,
    progress_status: typing.Optional[builtins.str] = None,
    total_applications: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68968c8c0cb4c03172bfd9d3608c9b579d5042521a8611cb30247839f57f6b05(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

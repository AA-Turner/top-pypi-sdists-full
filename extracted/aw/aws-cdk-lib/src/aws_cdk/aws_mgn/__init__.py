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
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "sourceConfigurations", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "targetNetwork", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "targetS3Configuration", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "scopeTags", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

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
        jsii.set(self, "targetDeployment", value) # pyright: ignore[reportArgumentType]

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


__all__ = [
    "CfnNetworkMigrationDefinition",
    "CfnNetworkMigrationDefinitionProps",
]

publication.publish()

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

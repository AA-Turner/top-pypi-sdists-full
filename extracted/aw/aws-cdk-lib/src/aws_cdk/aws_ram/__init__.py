r'''
# AWS Resource Access Manager Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ram as ram
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RAM construct libraries](https://constructs.dev/search?q=ram)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RAM resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RAM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html).

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
    import aws_cdk.interfaces.aws_ram as _aws_ram_73155c9b
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_ram_73155c9b = _LazyImport("aws_cdk.interfaces.aws_ram")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.IPermissionRef, _aws_cdk_0cae9daa.ITaggable)
class CfnPermission(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnPermission",
):
    '''Creates a customer managed permission for a specified resource type that you can attach to resource shares.

    It is created in the AWS Region in which you call the operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html
    :cloudformationResource: AWS::RAM::Permission
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        # policy_template: Any
        
        cfn_permission = ram.CfnPermission(self, "MyCfnPermission",
            name="name",
            policy_template=policy_template,
            resource_type="resourceType",
        
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
        name: builtins.str,
        policy_template: typing.Any,
        resource_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::Permission``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: Specifies the name of the customer managed permission. The name must be unique within the AWS Region .
        :param policy_template: A string in JSON format string that contains the following elements of a resource-based policy:. - *Effect* : must be set to ``ALLOW`` . - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* . - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* . This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.
        :param resource_type: Specifies the name of the resource type that this customer managed permission applies to. The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.
        :param tags: Specifies a list of one or more tag key and value pairs to attach to the permission.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4e6fe3eae2e441449bee4fa9cdbdbd3fa3faa77d6312d1d0b6173f4ab5e4f62c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPermissionProps(
            name=name,
            policy_template=policy_template,
            resource_type=resource_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForPermission")
    @builtins.classmethod
    def arn_for_permission(
        cls,
        resource: "_aws_ram_73155c9b.IPermissionRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fd9650545c65b77576c422e40dcbb81abb763828b97edf304b5a8786a7902334)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForPermission", [resource]))

    @jsii.member(jsii_name="isCfnPermission")
    @builtins.classmethod
    def is_cfn_permission(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnPermission.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3280cb41e56a951983fc454e18ff5fd2dd3a4c608ee7d9882b7275effb3b2b58)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnPermission", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d951b94e05f47918844ee4c94dafebba369732ccc302f7ad923dca32b5000fc7)
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
            type_hints = cached_type_hints(_typecheckingstub__b815722571219a975ded0c832e480c433d1106c5c3874c31f41a623df4840bef)
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
        '''The Amazon Resource Name (ARN) of the new permission.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIsResourceTypeDefault")
    def attr_is_resource_type_default(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Specifies whether this permission is the default for new resource shares that include resources of the associated resource type.

        :cloudformationAttribute: IsResourceTypeDefault
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrIsResourceTypeDefault"))

    @builtins.property
    @jsii.member(jsii_name="attrPermissionType")
    def attr_permission_type(self) -> builtins.str:
        '''The type of managed permission. This can be one of the following values:.

        - *AWS_MANAGED_PERMISSION* – AWS created and manages this managed permission. You can associate it with your resource shares, but you can't modify it.
        - *CUSTOMER_MANAGED_PERMISSION* – You, or another principal in your account created this managed permission. You can associate it with your resource shares and create new versions that have different permissions.

        :cloudformationAttribute: PermissionType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPermissionType"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''The version number for this version of the permission.

        :cloudformationAttribute: Version
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="permissionRef")
    def permission_ref(self) -> "_aws_ram_73155c9b.PermissionReference":
        '''A reference to a Permission resource.'''
        return typing.cast("_aws_ram_73155c9b.PermissionReference", jsii.get(self, "permissionRef"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the customer managed permission.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__952aaf926012eb44626e889296cc608af4a071943b783cc37c41445ba67cacbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policyTemplate")
    def policy_template(self) -> typing.Any:
        '''A string in JSON format string that contains the following elements of a resource-based policy:.'''
        return typing.cast(typing.Any, jsii.get(self, "policyTemplate"))

    @policy_template.setter
    def policy_template(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d786ce0393d6d5e9b23b457d7d296ea4e1b64dde74cbe0351155d84dbe06a21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        '''Specifies the name of the resource type that this customer managed permission applies to.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d012bd3d642b7557eafa85e0a130a59f59fd9bf570abb055165847be25a9e515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="tagsRaw")
    def tags_raw(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Specifies a list of one or more tag key and value pairs to attach to the permission.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tagsRaw"))

    @tags_raw.setter
    def tags_raw(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4e38f5af40d9dfeea4630580bc03fc46db30f305dafe61dc85a0a22e71eb103d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsRaw", value)


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.IPermissionAssociationRef)
class CfnPermissionAssociation(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnPermissionAssociation",
):
    '''Associates a specified AWS RAM permission with a resource share.

    You can only associate one permission with each resource type in a resource share.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permissionassociation.html
    :cloudformationResource: AWS::RAM::PermissionAssociation
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_permission_association = ram.CfnPermissionAssociation(self, "MyCfnPermissionAssociation",
            permission_arn="permissionArn",
            resource_share_arn="resourceShareArn",
        
            # the properties below are optional
            replace=False
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        permission_arn: builtins.str,
        resource_share_arn: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::PermissionAssociation``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param permission_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share.
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        :param replace: Specifies whether to replace the existing permission on the resource share. Use ``true`` to replace the current permission. Use ``false`` to add the permission when no permission is currently associated. The default value is ``false``. Updating an existing association also requires ``true``, because AWS RAM applies the change by re-associating the permission. Default: - false
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__55170c3893afd4a69bb857322a5c0a8bbb7a258a41a29ea799f0d684d6f1ac49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPermissionAssociationProps(
            permission_arn=permission_arn,
            resource_share_arn=resource_share_arn,
            replace=replace,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnPermissionAssociation")
    @builtins.classmethod
    def is_cfn_permission_association(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnPermissionAssociation.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bee5371dcb1f472f38d83f3439920b641641a05c6c8c30fc573dcd90aed623ac)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnPermissionAssociation", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__236f1b28ccdb6f44b711830c533c434910ebcdf201c33c6f00ee65175c7203a0)
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
            type_hints = cached_type_hints(_typecheckingstub__6859c137b99a0cae574854d38a306fface552ca813f81f89c160a2087b891f4b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationStatus")
    def attr_association_status(self) -> builtins.str:
        '''The current status of the association between the permission and the resource share.

        :cloudformationAttribute: AssociationStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrFeatureSet")
    def attr_feature_set(self) -> builtins.str:
        '''The feature set of the resource share.

        :cloudformationAttribute: FeatureSet
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFeatureSet"))

    @builtins.property
    @jsii.member(jsii_name="attrIsDefault")
    def attr_is_default(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Indicates whether the associated resource share is using the default version of the permission.

        :cloudformationAttribute: IsDefault
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrIsDefault"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''The date and time when the association between the permission and the resource share was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrPermissionVersion")
    def attr_permission_version(self) -> builtins.str:
        '''The version of the permission currently associated with the resource share.

        :cloudformationAttribute: PermissionVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPermissionVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceType")
    def attr_resource_type(self) -> builtins.str:
        '''The resource type to which the permission applies.

        :cloudformationAttribute: ResourceType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="permissionAssociationRef")
    def permission_association_ref(
        self,
    ) -> "_aws_ram_73155c9b.PermissionAssociationReference":
        '''A reference to a PermissionAssociation resource.'''
        return typing.cast("_aws_ram_73155c9b.PermissionAssociationReference", jsii.get(self, "permissionAssociationRef"))

    @builtins.property
    @jsii.member(jsii_name="permissionArn")
    def permission_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "permissionArn"))

    @permission_arn.setter
    def permission_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dec9cb2d24bcc763c95bc5c0e9a4d3c54474c8ccee5fdafc459f877b60d9d5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceShareArn")
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceShareArn"))

    @resource_share_arn.setter
    def resource_share_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__06f6e1d2b4173ba82558c200223bd367dc45f5bf20751b62d744a55747a0c59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceShareArn", value)

    @builtins.property
    @jsii.member(jsii_name="replace")
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Specifies whether to replace the existing permission on the resource share.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "replace"))

    @replace.setter
    def replace(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9688c50ad4e97c5784ee43cc13d98585ca207713bc22e93dd2cef28fa134cb91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnPermissionAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "permission_arn": "permissionArn",
        "resource_share_arn": "resourceShareArn",
        "replace": "replace",
    },
)
class CfnPermissionAssociationProps:
    def __init__(
        self,
        *,
        permission_arn: builtins.str,
        resource_share_arn: builtins.str,
        replace: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPermissionAssociation``.

        :param permission_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share.
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        :param replace: Specifies whether to replace the existing permission on the resource share. Use ``true`` to replace the current permission. Use ``false`` to add the permission when no permission is currently associated. The default value is ``false``. Updating an existing association also requires ``true``, because AWS RAM applies the change by re-associating the permission. Default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permissionassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_permission_association_props = ram.CfnPermissionAssociationProps(
                permission_arn="permissionArn",
                resource_share_arn="resourceShareArn",
            
                # the properties below are optional
                replace=False
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ad3c33a67f9263182c64da640c265ea40d51e9cd79298ae24ef9180fd8a70ac7)
            check_type(argname="argument permission_arn", value=permission_arn, expected_type=type_hints["permission_arn"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permission_arn": permission_arn,
            "resource_share_arn": resource_share_arn,
        }
        if replace is not None:
            self._values["replace"] = replace

    @builtins.property
    def permission_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permissionassociation.html#cfn-ram-permissionassociation-permissionarn
        '''
        result = self._values.get("permission_arn")
        assert result is not None, "Required property 'permission_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permissionassociation.html#cfn-ram-permissionassociation-resourcesharearn
        '''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Specifies whether to replace the existing permission on the resource share.

        Use ``true`` to replace the current permission. Use ``false`` to add the permission when no permission is currently associated. The default value is ``false``. Updating an existing association also requires ``true``, because AWS RAM applies the change by re-associating the permission.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permissionassociation.html#cfn-ram-permissionassociation-replace
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnPermissionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "policy_template": "policyTemplate",
        "resource_type": "resourceType",
        "tags": "tags",
    },
)
class CfnPermissionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        policy_template: typing.Any,
        resource_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPermission``.

        :param name: Specifies the name of the customer managed permission. The name must be unique within the AWS Region .
        :param policy_template: A string in JSON format string that contains the following elements of a resource-based policy:. - *Effect* : must be set to ``ALLOW`` . - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* . - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* . This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.
        :param resource_type: Specifies the name of the resource type that this customer managed permission applies to. The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.
        :param tags: Specifies a list of one or more tag key and value pairs to attach to the permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            # policy_template: Any
            
            cfn_permission_props = ram.CfnPermissionProps(
                name="name",
                policy_template=policy_template,
                resource_type="resourceType",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c9e72a90559f1f4c0f547098b5369dbfeed98afe29faf887a6f20cad208db7e3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_template", value=policy_template, expected_type=type_hints["policy_template"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_template": policy_template,
            "resource_type": resource_type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the customer managed permission.

        The name must be unique within the AWS Region .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_template(self) -> typing.Any:
        '''A string in JSON format string that contains the following elements of a resource-based policy:.

        - *Effect* : must be set to ``ALLOW`` .
        - *Action* : specifies the actions that are allowed by this customer managed permission. The list must contain only actions that are supported by the specified resource type. For a list of all actions supported by each resource type, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *AWS Identity and Access Management User Guide* .
        - *Condition* : (optional) specifies conditional parameters that must evaluate to true when a user attempts an action for that action to be allowed. For more information about the Condition element, see `IAM policies: Condition element <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_ in the *AWS Identity and Access Management User Guide* .

        This template can't include either the ``Resource`` or ``Principal`` elements. Those are both filled in by AWS RAM when it instantiates the resource-based policy on each resource shared using this managed permission. The ``Resource`` comes from the ARN of the specific resource that you are sharing. The ``Principal`` comes from the list of identities added to the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-policytemplate
        '''
        result = self._values.get("policy_template")
        assert result is not None, "Required property 'policy_template' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''Specifies the name of the resource type that this customer managed permission applies to.

        The format is ``*<service-code>* : *<resource-type>*`` and is not case sensitive. For example, to specify an Amazon EC2 Subnet, you can use the string ``ec2:subnet`` . To see the list of valid values for this parameter, query the `ListResourceTypes <https://docs.aws.amazon.com/ram/latest/APIReference/API_ListResourceTypes.html>`_ operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-resourcetype
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Specifies a list of one or more tag key and value pairs to attach to the permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-permission.html#cfn-ram-permission-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.IPrincipalAssociationRef)
class CfnPrincipalAssociation(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnPrincipalAssociation",
):
    '''Associates a specified principal with a resource share.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-principalassociation.html
    :cloudformationResource: AWS::RAM::PrincipalAssociation
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_principal_association = ram.CfnPrincipalAssociation(self, "MyCfnPrincipalAssociation",
            principal="principal",
            resource_share_arn="resourceShareArn"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        principal: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::RAM::PrincipalAssociation``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param principal: Specifies the principal to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e52a6d3bedeae5d48e10d33c864aeb726059da8bc8f7d22c9043bb2844d1b562)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPrincipalAssociationProps(
            principal=principal, resource_share_arn=resource_share_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnPrincipalAssociation")
    @builtins.classmethod
    def is_cfn_principal_association(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnPrincipalAssociation.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0c0dd7ba7bd6617bf07bc778416506200bcf0f1c2bc254bb9f8ca109657ae095)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnPrincipalAssociation", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e9718a47c679d376429b2ed5c73b3b7d4c3bad36e25dfe9233b8fc29b772cd39)
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
            type_hints = cached_type_hints(_typecheckingstub__5e764644f03954c7388e269c989d300d15df9247cad6b003e5a9879fcffca008)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationType")
    def attr_association_type(self) -> builtins.str:
        '''The type of entity included in this association.

        :cloudformationAttribute: AssociationType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationType"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time when the association was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrExternal")
    def attr_external(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Indicates whether the principal belongs to the same organization in AWS Organizations as the AWS account that owns the resource share.

        :cloudformationAttribute: External
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrExternal"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''The date and time when the association was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="principalAssociationRef")
    def principal_association_ref(
        self,
    ) -> "_aws_ram_73155c9b.PrincipalAssociationReference":
        '''A reference to a PrincipalAssociation resource.'''
        return typing.cast("_aws_ram_73155c9b.PrincipalAssociationReference", jsii.get(self, "principalAssociationRef"))

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        '''Specifies the principal to associate with the resource share.

        The possible values are:.
        '''
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__70f0bf39a80714daa70d2a8f4ee257259de64f7c7bf145c6a34df87886bff096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="resourceShareArn")
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceShareArn"))

    @resource_share_arn.setter
    def resource_share_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__178f622a86fda00cda5e53fd5981473e59e604bac16b65efadda327c9a00bbe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceShareArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnPrincipalAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"principal": "principal", "resource_share_arn": "resourceShareArn"},
)
class CfnPrincipalAssociationProps:
    def __init__(
        self,
        *,
        principal: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnPrincipalAssociation``.

        :param principal: Specifies the principal to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-principalassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_principal_association_props = ram.CfnPrincipalAssociationProps(
                principal="principal",
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__081ebcc6a0561c062c69bd672de60061c0857ce4c695a9c13d2b9b18111f150f)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal": principal,
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def principal(self) -> builtins.str:
        '''Specifies the principal to associate with the resource share. The possible values are:.

        - An AWS account ID
        - An Amazon Resource Name (ARN) of an organization in AWS Organizations
        - An ARN of an organizational unit (OU) in AWS Organizations
        - An ARN of an IAM role
        - An ARN of an IAM user

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-principalassociation.html#cfn-ram-principalassociation-principal
        '''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-principalassociation.html#cfn-ram-principalassociation-resourcesharearn
        '''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrincipalAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.IResourceAssociationRef)
class CfnResourceAssociation(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceAssociation",
):
    '''Associates a specified resource with a resource share.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceassociation.html
    :cloudformationResource: AWS::RAM::ResourceAssociation
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_resource_association = ram.CfnResourceAssociation(self, "MyCfnResourceAssociation",
            resource_arn="resourceArn",
            resource_share_arn="resourceShareArn"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        resource_arn: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::RAM::ResourceAssociation``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param resource_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource to associate with the resource share.
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__253b51e3073e6df9c86d547e32c9bd421565bb97647669fbe9900baaffacc111)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceAssociationProps(
            resource_arn=resource_arn, resource_share_arn=resource_share_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnResourceAssociation")
    @builtins.classmethod
    def is_cfn_resource_association(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnResourceAssociation.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c80dce2634de17baabe5f1e8427a7b27495efdd2b66f922061aed5cebc52a053)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnResourceAssociation", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e42b948e69010b795dfce33aa760343612d8da67cf413d6f36fc3a2ac45fcc31)
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
            type_hints = cached_type_hints(_typecheckingstub__994741b0772e3c5194e6a97c5ca9f025e3e273c23a756612f7f6ec4dfe03b0d2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationType")
    def attr_association_type(self) -> builtins.str:
        '''The type of entity included in this association.

        :cloudformationAttribute: AssociationType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationType"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time when the association was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrExternal")
    def attr_external(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''Indicates whether the principal belongs to the same organization in AWS Organizations as the AWS account that owns the resource share.

        :cloudformationAttribute: External
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrExternal"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''The date and time when the association was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="resourceAssociationRef")
    def resource_association_ref(
        self,
    ) -> "_aws_ram_73155c9b.ResourceAssociationReference":
        '''A reference to a ResourceAssociation resource.'''
        return typing.cast("_aws_ram_73155c9b.ResourceAssociationReference", jsii.get(self, "resourceAssociationRef"))

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource to associate with the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0bd2388c68650875a18bdb4a57ba11aa5f731ddb0deb1a16ac65854a47330e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceShareArn")
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceShareArn"))

    @resource_share_arn.setter
    def resource_share_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__84c8fcbc9756e48306bd853652b7ec84ec65ad6365aeaa69b522c7c95720ed25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceShareArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_arn": "resourceArn",
        "resource_share_arn": "resourceShareArn",
    },
)
class CfnResourceAssociationProps:
    def __init__(
        self,
        *,
        resource_arn: builtins.str,
        resource_share_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnResourceAssociation``.

        :param resource_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource to associate with the resource share.
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_resource_association_props = ram.CfnResourceAssociationProps(
                resource_arn="resourceArn",
                resource_share_arn="resourceShareArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6614a7a21689067cef22faad0a46ce598961f15ffd3d533f5c6d7a0071445f64)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_arn": resource_arn,
            "resource_share_arn": resource_share_arn,
        }

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource to associate with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceassociation.html#cfn-ram-resourceassociation-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceassociation.html#cfn-ram-resourceassociation-resourcesharearn
        '''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.IResourceShareRef, _aws_cdk_0cae9daa.ITaggable)
class CfnResourceShare(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceShare",
):
    '''Creates a resource share.

    You can provide a list of the Amazon Resource Names (ARNs) for the resources that you want to share, a list of principals you want to share the resources with, and the permissions to grant those principals.
    .. epigraph::

       Sharing a resource makes it available for use by principals outside of the AWS account that created the resource. Sharing doesn't change any permissions or quotas that apply to the resource in the account that created it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
    :cloudformationResource: AWS::RAM::ResourceShare
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_resource_share = ram.CfnResourceShare(self, "MyCfnResourceShare",
            name="name",
        
            # the properties below are optional
            allow_external_principals=False,
            permission_arns=["permissionArns"],
            principals=["principals"],
            resource_arns=["resourceArns"],
            resource_share_configuration=ram.CfnResourceShare.ResourceShareConfigurationProperty(
                exclusive_account_access=False,
                retain_sharing_on_account_leave_organization=False
            ),
            sources=["sources"],
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
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_share_configuration: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnResourceShare.ResourceShareConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::ResourceShare``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies the principals to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param resource_share_configuration: The configuration for a resource share.
        :param sources: Specifies from which source accounts the service principal has access to the resources in this resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1fea9cca1996f068f8dde2c34bf4c41d370ee8638f9da1d855f8b0022d75af5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceShareProps(
            name=name,
            allow_external_principals=allow_external_principals,
            permission_arns=permission_arns,
            principals=principals,
            resource_arns=resource_arns,
            resource_share_configuration=resource_share_configuration,
            sources=sources,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForResourceShare")
    @builtins.classmethod
    def arn_for_resource_share(
        cls,
        resource: "_aws_ram_73155c9b.IResourceShareRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2465c7da6b1c48b2189a3540bb11f2d7763d8b628f6f5095ae15b4b34de4c14e)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForResourceShare", [resource]))

    @jsii.member(jsii_name="isCfnResourceShare")
    @builtins.classmethod
    def is_cfn_resource_share(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnResourceShare.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e7b78a9719eeef0b1e7174c7dedf9623a922048240bb0ee41197b83f526301b4)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnResourceShare", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8defbc280b992fb09ff90651c627ce1c4211d498c66f7c4b62a4b3a5285f92d)
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
            type_hints = cached_type_hints(_typecheckingstub__e124e85df525ca5d702f0b9a2b5bb739a12519bf552f8ea08a9f673f4077d696)
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
        '''The Amazon Resource Name (ARN) of the resource share.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time when the resource share was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrFeatureSet")
    def attr_feature_set(self) -> builtins.str:
        '''Indicates what features are available for this resource share. This parameter can have one of the following values:.

        - *STANDARD* – A resource share that supports all functionality. These resource shares are visible to all principals you share the resource share with. You can modify these resource shares in AWS RAM using the console or APIs. This resource share might have been created by AWS RAM , or it might have been *CREATED_FROM_POLICY* and then promoted.
        - *CREATED_FROM_POLICY* – The customer manually shared a resource by attaching a resource-based policy. That policy did not match any existing managed permissions, so AWS RAM created this customer managed permission automatically on the customer's behalf based on the attached policy document. This type of resource share is visible only to the AWS account that created it. You can't modify it in AWS RAM unless you promote it. For more information, see ``PromoteResourceShareCreatedFromPolicy`` .
        - *PROMOTING_TO_STANDARD* – This resource share was originally ``CREATED_FROM_POLICY`` , but the customer ran the ``PromoteResourceShareCreatedFromPolicy`` and that operation is still in progress. This value changes to ``STANDARD`` when complete.

        :cloudformationAttribute: FeatureSet
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFeatureSet"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''The date and time when the resource share was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrOwningAccountId")
    def attr_owning_account_id(self) -> builtins.str:
        '''The ID of the AWS account that owns the resource share.

        :cloudformationAttribute: OwningAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwningAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the resource share.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="resourceShareRef")
    def resource_share_ref(self) -> "_aws_ram_73155c9b.ResourceShareReference":
        '''A reference to a ResourceShare resource.'''
        return typing.cast("_aws_ram_73155c9b.ResourceShareReference", jsii.get(self, "resourceShareRef"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb76bd909afa4dee66debdd78e087883e909ff481a0f08820b4aee17388a74e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.'''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], jsii.get(self, "allowExternalPrincipals"))

    @allow_external_principals.setter
    def allow_external_principals(
        self,
        value: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1a8ac8ee18a992b418a8b6fc421772eee1a5d5b0b675ccfe6c0ce0c7f18b40e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowExternalPrincipals", value)

    @builtins.property
    @jsii.member(jsii_name="permissionArns")
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permissionArns"))

    @permission_arns.setter
    def permission_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__411d88d3990f34296ef5770eb3cb3792a55b6b7805c6e7381207750e8fa15042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionArns", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the principals to associate with the resource share.

        The possible values are:.
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__27e4971e92d1679357249799c9998f6cde7d19d4a39eec3a7d952e11f95d0b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ebcfa059a044b9468256f95fd1dc2d90bce40e3d6d96d59d1755b38b7d15db67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value)

    @builtins.property
    @jsii.member(jsii_name="resourceShareConfiguration")
    def resource_share_configuration(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnResourceShare.ResourceShareConfigurationProperty"]]:
        '''The configuration for a resource share.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnResourceShare.ResourceShareConfigurationProperty"]], jsii.get(self, "resourceShareConfiguration"))

    @resource_share_configuration.setter
    def resource_share_configuration(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnResourceShare.ResourceShareConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8bbe169a562bf96addb295092d013df62468e87386fc039d6a6fa805db687e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceShareConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies from which source accounts the service principal has access to the resources in this resource share.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__df7ab5400bf3b8953cb4a0db7747c4174b63b9e7963dfae4ea6eda15e4f55030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)

    @builtins.property
    @jsii.member(jsii_name="tagsRaw")
    def tags_raw(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Specifies one or more tags to attach to the resource share itself.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tagsRaw"))

    @tags_raw.setter
    def tags_raw(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2e8df76745e5c0758e8b5233e879c50ee5a6f6f817a0850af55da2744c10ef55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsRaw", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_ram.CfnResourceShare.ResourceShareConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclusive_account_access": "exclusiveAccountAccess",
            "retain_sharing_on_account_leave_organization": "retainSharingOnAccountLeaveOrganization",
        },
    )
    class ResourceShareConfigurationProperty:
        def __init__(
            self,
            *,
            exclusive_account_access: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
            retain_sharing_on_account_leave_organization: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        ) -> None:
            '''The configuration for a resource share.

            :param exclusive_account_access: The resource share restricts access to an account.
            :param retain_sharing_on_account_leave_organization: Specifies whether the consumer account retains access to the resource share after leaving the organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ram-resourceshare-resourceshareconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_ram as ram
                
                resource_share_configuration_property = ram.CfnResourceShare.ResourceShareConfigurationProperty(
                    exclusive_account_access=False,
                    retain_sharing_on_account_leave_organization=False
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__2bbbef5e59aed180189cb70a7793cc23294faff4b1b27ba21be73f05a9da1512)
                check_type(argname="argument exclusive_account_access", value=exclusive_account_access, expected_type=type_hints["exclusive_account_access"])
                check_type(argname="argument retain_sharing_on_account_leave_organization", value=retain_sharing_on_account_leave_organization, expected_type=type_hints["retain_sharing_on_account_leave_organization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclusive_account_access is not None:
                self._values["exclusive_account_access"] = exclusive_account_access
            if retain_sharing_on_account_leave_organization is not None:
                self._values["retain_sharing_on_account_leave_organization"] = retain_sharing_on_account_leave_organization

        @builtins.property
        def exclusive_account_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''The resource share restricts access to an account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ram-resourceshare-resourceshareconfiguration.html#cfn-ram-resourceshare-resourceshareconfiguration-exclusiveaccountaccess
            '''
            result = self._values.get("exclusive_account_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        @builtins.property
        def retain_sharing_on_account_leave_organization(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
            '''Specifies whether the consumer account retains access to the resource share after leaving the organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ram-resourceshare-resourceshareconfiguration.html#cfn-ram-resourceshare-resourceshareconfiguration-retainsharingonaccountleaveorganization
            '''
            result = self._values.get("retain_sharing_on_account_leave_organization")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceShareConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_external_principals": "allowExternalPrincipals",
        "permission_arns": "permissionArns",
        "principals": "principals",
        "resource_arns": "resourceArns",
        "resource_share_configuration": "resourceShareConfiguration",
        "sources": "sources",
        "tags": "tags",
    },
)
class CfnResourceShareProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_share_configuration: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnResourceShare.ResourceShareConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceShare``.

        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies the principals to associate with the resource share. The possible values are:. - An AWS account ID - An Amazon Resource Name (ARN) of an organization in AWS Organizations - An ARN of an organizational unit (OU) in AWS Organizations - An ARN of an IAM role - An ARN of an IAM user .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param resource_share_configuration: The configuration for a resource share.
        :param sources: Specifies from which source accounts the service principal has access to the resources in this resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_resource_share_props = ram.CfnResourceShareProps(
                name="name",
            
                # the properties below are optional
                allow_external_principals=False,
                permission_arns=["permissionArns"],
                principals=["principals"],
                resource_arns=["resourceArns"],
                resource_share_configuration=ram.CfnResourceShare.ResourceShareConfigurationProperty(
                    exclusive_account_access=False,
                    retain_sharing_on_account_leave_organization=False
                ),
                sources=["sources"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a74e87907f43c8b632de2f93b4560b166f51134fc5a47c6f4892e716a268961a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument permission_arns", value=permission_arns, expected_type=type_hints["permission_arns"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource_share_configuration", value=resource_share_configuration, expected_type=type_hints["resource_share_configuration"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if permission_arns is not None:
            self._values["permission_arns"] = permission_arns
        if principals is not None:
            self._values["principals"] = principals
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if resource_share_configuration is not None:
            self._values["resource_share_configuration"] = resource_share_configuration
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, "_aws_cdk_0cae9daa.IResolvable"]], result)

    @builtins.property
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-permissionarns
        '''
        result = self._values.get("permission_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the principals to associate with the resource share. The possible values are:.

        - An AWS account ID
        - An Amazon Resource Name (ARN) of an organization in AWS Organizations
        - An ARN of an organizational unit (OU) in AWS Organizations
        - An ARN of an IAM role
        - An ARN of an IAM user

        .. epigraph::

           Not all resource types can be shared with IAM roles and users. For more information, see the column *Can share with IAM roles and users* in the tables on `Shareable AWS resources <https://docs.aws.amazon.com/ram/latest/userguide/shareable.html>`_ in the *AWS Resource Access Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        '''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_share_configuration(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnResourceShare.ResourceShareConfigurationProperty"]]:
        '''The configuration for a resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourceshareconfiguration
        '''
        result = self._values.get("resource_share_configuration")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnResourceShare.ResourceShareConfigurationProperty"]], result)

    @builtins.property
    def sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies from which source accounts the service principal has access to the resources in this resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''Specifies one or more tags to attach to the resource share itself.

        It doesn't attach the tags to the resources associated with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_ram_73155c9b.ISourceAssociationRef)
class CfnSourceAssociation(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnSourceAssociation",
):
    '''Associates a specified source account with a resource share.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-sourceassociation.html
    :cloudformationResource: AWS::RAM::SourceAssociation
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_source_association = ram.CfnSourceAssociation(self, "MyCfnSourceAssociation",
            resource_share_arn="resourceShareArn",
            source_id="sourceId"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        resource_share_arn: builtins.str,
        source_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::RAM::SourceAssociation``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        :param source_id: Specifies the ID of the source account to associate with the resource share.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__95294b2a173790c912193856e23233b95d77795a5807cd0d77c4cc3f39cf5c50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSourceAssociationProps(
            resource_share_arn=resource_share_arn, source_id=source_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isCfnSourceAssociation")
    @builtins.classmethod
    def is_cfn_source_association(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnSourceAssociation.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bfb3308a1d31f0520d40b8f191e39010d3c590aea47ef63c20a970c70870010c)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnSourceAssociation", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f49c80bed08b5444197d91d617e24bd7d809f9747edcd6abd8340646f7a9fb2)
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
            type_hints = cached_type_hints(_typecheckingstub__53dbe498299e36c2f861e2393f68eb83ffdeacf830150ae94b8abff47e507b1a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time when the association was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''The date and time when the association was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceType")
    def attr_source_type(self) -> builtins.str:
        '''The type of the source.

        :cloudformationAttribute: SourceType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceType"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="sourceAssociationRef")
    def source_association_ref(self) -> "_aws_ram_73155c9b.SourceAssociationReference":
        '''A reference to a SourceAssociation resource.'''
        return typing.cast("_aws_ram_73155c9b.SourceAssociationReference", jsii.get(self, "sourceAssociationRef"))

    @builtins.property
    @jsii.member(jsii_name="resourceShareArn")
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "resourceShareArn"))

    @resource_share_arn.setter
    def resource_share_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__73f1a02acbe2c3340c9ebe73b9de407b85c630cd10868adfcfe76fc3cedefa19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceShareArn", value)

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> builtins.str:
        '''Specifies the ID of the source account to associate with the resource share.'''
        return typing.cast(builtins.str, jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3925bda5d3d2d5005837c3280d164cced370e7a608fb382f4e2158d7ef23b8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnSourceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"resource_share_arn": "resourceShareArn", "source_id": "sourceId"},
)
class CfnSourceAssociationProps:
    def __init__(
        self,
        *,
        resource_share_arn: builtins.str,
        source_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnSourceAssociation``.

        :param resource_share_arn: Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.
        :param source_id: Specifies the ID of the source account to associate with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-sourceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_source_association_props = ram.CfnSourceAssociationProps(
                resource_share_arn="resourceShareArn",
                source_id="sourceId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ff3738c70c00052935a836353180ff5dea09accf59e4c6f95f0b140537352203)
            check_type(argname="argument resource_share_arn", value=resource_share_arn, expected_type=type_hints["resource_share_arn"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_share_arn": resource_share_arn,
            "source_id": source_id,
        }

    @builtins.property
    def resource_share_arn(self) -> builtins.str:
        '''Specifies the `Amazon Resource Name (ARN) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-sourceassociation.html#cfn-ram-sourceassociation-resourcesharearn
        '''
        result = self._values.get("resource_share_arn")
        assert result is not None, "Required property 'resource_share_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_id(self) -> builtins.str:
        '''Specifies the ID of the source account to associate with the resource share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-sourceassociation.html#cfn-ram-sourceassociation-sourceid
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSourceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnPermission",
    "CfnPermissionAssociation",
    "CfnPermissionAssociationProps",
    "CfnPermissionProps",
    "CfnPrincipalAssociation",
    "CfnPrincipalAssociationProps",
    "CfnResourceAssociation",
    "CfnResourceAssociationProps",
    "CfnResourceShare",
    "CfnResourceShareProps",
    "CfnSourceAssociation",
    "CfnSourceAssociationProps",
]

publication.publish()

def _typecheckingstub__4e6fe3eae2e441449bee4fa9cdbdbd3fa3faa77d6312d1d0b6173f4ab5e4f62c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    policy_template: typing.Any,
    resource_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9650545c65b77576c422e40dcbb81abb763828b97edf304b5a8786a7902334(
    resource: _aws_ram_73155c9b.IPermissionRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3280cb41e56a951983fc454e18ff5fd2dd3a4c608ee7d9882b7275effb3b2b58(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d951b94e05f47918844ee4c94dafebba369732ccc302f7ad923dca32b5000fc7(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b815722571219a975ded0c832e480c433d1106c5c3874c31f41a623df4840bef(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952aaf926012eb44626e889296cc608af4a071943b783cc37c41445ba67cacbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d786ce0393d6d5e9b23b457d7d296ea4e1b64dde74cbe0351155d84dbe06a21b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d012bd3d642b7557eafa85e0a130a59f59fd9bf570abb055165847be25a9e515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e38f5af40d9dfeea4630580bc03fc46db30f305dafe61dc85a0a22e71eb103d(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55170c3893afd4a69bb857322a5c0a8bbb7a258a41a29ea799f0d684d6f1ac49(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    permission_arn: builtins.str,
    resource_share_arn: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee5371dcb1f472f38d83f3439920b641641a05c6c8c30fc573dcd90aed623ac(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236f1b28ccdb6f44b711830c533c434910ebcdf201c33c6f00ee65175c7203a0(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6859c137b99a0cae574854d38a306fface552ca813f81f89c160a2087b891f4b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec9cb2d24bcc763c95bc5c0e9a4d3c54474c8ccee5fdafc459f877b60d9d5ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f6e1d2b4173ba82558c200223bd367dc45f5bf20751b62d744a55747a0c59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9688c50ad4e97c5784ee43cc13d98585ca207713bc22e93dd2cef28fa134cb91(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3c33a67f9263182c64da640c265ea40d51e9cd79298ae24ef9180fd8a70ac7(
    *,
    permission_arn: builtins.str,
    resource_share_arn: builtins.str,
    replace: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e72a90559f1f4c0f547098b5369dbfeed98afe29faf887a6f20cad208db7e3(
    *,
    name: builtins.str,
    policy_template: typing.Any,
    resource_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52a6d3bedeae5d48e10d33c864aeb726059da8bc8f7d22c9043bb2844d1b562(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    principal: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0dd7ba7bd6617bf07bc778416506200bcf0f1c2bc254bb9f8ca109657ae095(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9718a47c679d376429b2ed5c73b3b7d4c3bad36e25dfe9233b8fc29b772cd39(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e764644f03954c7388e269c989d300d15df9247cad6b003e5a9879fcffca008(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f0bf39a80714daa70d2a8f4ee257259de64f7c7bf145c6a34df87886bff096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178f622a86fda00cda5e53fd5981473e59e604bac16b65efadda327c9a00bbe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081ebcc6a0561c062c69bd672de60061c0857ce4c695a9c13d2b9b18111f150f(
    *,
    principal: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253b51e3073e6df9c86d547e32c9bd421565bb97647669fbe9900baaffacc111(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource_arn: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80dce2634de17baabe5f1e8427a7b27495efdd2b66f922061aed5cebc52a053(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42b948e69010b795dfce33aa760343612d8da67cf413d6f36fc3a2ac45fcc31(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994741b0772e3c5194e6a97c5ca9f025e3e273c23a756612f7f6ec4dfe03b0d2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd2388c68650875a18bdb4a57ba11aa5f731ddb0deb1a16ac65854a47330e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c8fcbc9756e48306bd853652b7ec84ec65ad6365aeaa69b522c7c95720ed25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6614a7a21689067cef22faad0a46ce598961f15ffd3d533f5c6d7a0071445f64(
    *,
    resource_arn: builtins.str,
    resource_share_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fea9cca1996f068f8dde2c34bf4c41d370ee8638f9da1d855f8b0022d75af5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_share_configuration: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnResourceShare.ResourceShareConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2465c7da6b1c48b2189a3540bb11f2d7763d8b628f6f5095ae15b4b34de4c14e(
    resource: _aws_ram_73155c9b.IResourceShareRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b78a9719eeef0b1e7174c7dedf9623a922048240bb0ee41197b83f526301b4(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8defbc280b992fb09ff90651c627ce1c4211d498c66f7c4b62a4b3a5285f92d(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e124e85df525ca5d702f0b9a2b5bb739a12519bf552f8ea08a9f673f4077d696(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb76bd909afa4dee66debdd78e087883e909ff481a0f08820b4aee17388a74e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8ac8ee18a992b418a8b6fc421772eee1a5d5b0b675ccfe6c0ce0c7f18b40e7(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411d88d3990f34296ef5770eb3cb3792a55b6b7805c6e7381207750e8fa15042(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e4971e92d1679357249799c9998f6cde7d19d4a39eec3a7d952e11f95d0b64(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcfa059a044b9468256f95fd1dc2d90bce40e3d6d96d59d1755b38b7d15db67(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbe169a562bf96addb295092d013df62468e87386fc039d6a6fa805db687e32(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnResourceShare.ResourceShareConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7ab5400bf3b8953cb4a0db7747c4174b63b9e7963dfae4ea6eda15e4f55030(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8df76745e5c0758e8b5233e879c50ee5a6f6f817a0850af55da2744c10ef55(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbbef5e59aed180189cb70a7793cc23294faff4b1b27ba21be73f05a9da1512(
    *,
    exclusive_account_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    retain_sharing_on_account_leave_organization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74e87907f43c8b632de2f93b4560b166f51134fc5a47c6f4892e716a268961a(
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _aws_cdk_0cae9daa.IResolvable]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_share_configuration: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnResourceShare.ResourceShareConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95294b2a173790c912193856e23233b95d77795a5807cd0d77c4cc3f39cf5c50(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource_share_arn: builtins.str,
    source_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb3308a1d31f0520d40b8f191e39010d3c590aea47ef63c20a970c70870010c(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f49c80bed08b5444197d91d617e24bd7d809f9747edcd6abd8340646f7a9fb2(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dbe498299e36c2f861e2393f68eb83ffdeacf830150ae94b8abff47e507b1a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f1a02acbe2c3340c9ebe73b9de407b85c630cd10868adfcfe76fc3cedefa19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3925bda5d3d2d5005837c3280d164cced370e7a608fb382f4e2158d7ef23b8a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3738c70c00052935a836353180ff5dea09accf59e4c6f95f0b140537352203(
    *,
    resource_share_arn: builtins.str,
    source_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

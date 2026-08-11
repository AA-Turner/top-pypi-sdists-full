r'''
# AWS::UserNotifications Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_usernotifications as usernotifications
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for UserNotifications construct libraries](https://constructs.dev/search?q=usernotifications)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::UserNotifications resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_UserNotifications.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::UserNotifications](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_UserNotifications.html).

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
    import aws_cdk.interfaces.aws_usernotifications as _aws_usernotifications_48e518a2
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_usernotifications_48e518a2 = _LazyImport("aws_cdk.interfaces.aws_usernotifications")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_usernotifications_48e518a2.IManagedNotificationConfigurationRef)
class CfnManagedNotificationConfiguration(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_usernotifications.CfnManagedNotificationConfiguration",
):
    '''Resource type definition for AWS User Notifications ManagedNotificationConfiguration.

    This is a read-only resource representing AWS-managed notification configurations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-usernotifications-managednotificationconfiguration.html
    :cloudformationResource: AWS::UserNotifications::ManagedNotificationConfiguration
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_usernotifications as usernotifications
        
        cfn_managed_notification_configuration = usernotifications.CfnManagedNotificationConfiguration(self, "MyCfnManagedNotificationConfiguration",
            category="category",
            sub_category="subCategory"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        category: typing.Optional[builtins.str] = None,
        sub_category: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::UserNotifications::ManagedNotificationConfiguration``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param category: The category of the ManagedNotificationConfiguration.
        :param sub_category: The subCategory of the ManagedNotificationConfiguration.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a043496630b4e7941136ffd471086811d4add3f355744af29f476688ffc99eaf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnManagedNotificationConfigurationProps(
            category=category, sub_category=sub_category
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForManagedNotificationConfiguration")
    @builtins.classmethod
    def arn_for_managed_notification_configuration(
        cls,
        resource: "_aws_usernotifications_48e518a2.IManagedNotificationConfigurationRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94af00cc5ab45f19b4f54a037eb7ec65279c06900c2b0c724c99eeff8c46da25)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForManagedNotificationConfiguration", [resource]))

    @jsii.member(jsii_name="isCfnManagedNotificationConfiguration")
    @builtins.classmethod
    def is_cfn_managed_notification_configuration(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnManagedNotificationConfiguration.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3826d538e2bb7434a6bd938c55d66122060a736b5fac6fd8fe6d40e92d587497)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnManagedNotificationConfiguration", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2f214d52a8bd60860ce3b0cdd241a7b71d2b79db3750829453090213b280bf65)
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
            type_hints = cached_type_hints(_typecheckingstub__9d7800493c5dadecab3e3b0116cc88b0e8a06e869972adbbf62ee21de5b1181b)
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
        '''The ARN of the ManagedNotificationConfiguration.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDescription")
    def attr_description(self) -> builtins.str:
        '''The description of the ManagedNotificationConfiguration.

        :cloudformationAttribute: Description
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescription"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ManagedNotificationConfiguration.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="managedNotificationConfigurationRef")
    def managed_notification_configuration_ref(
        self,
    ) -> "_aws_usernotifications_48e518a2.ManagedNotificationConfigurationReference":
        '''A reference to a ManagedNotificationConfiguration resource.'''
        return typing.cast("_aws_usernotifications_48e518a2.ManagedNotificationConfigurationReference", jsii.get(self, "managedNotificationConfigurationRef"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> typing.Optional[builtins.str]:
        '''The category of the ManagedNotificationConfiguration.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "category"))

    @category.setter
    def category(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8d58ebdd9774ef67562943832bafc13740ff86a9281f83df24dd9c0cfc2e5e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subCategory")
    def sub_category(self) -> typing.Optional[builtins.str]:
        '''The subCategory of the ManagedNotificationConfiguration.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subCategory"))

    @sub_category.setter
    def sub_category(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__adc24f9712a99cf9a161c3d342a09d61552e3b19a201e5984946ab3949cfa2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subCategory", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_usernotifications.CfnManagedNotificationConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"category": "category", "sub_category": "subCategory"},
)
class CfnManagedNotificationConfigurationProps:
    def __init__(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        sub_category: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnManagedNotificationConfiguration``.

        :param category: The category of the ManagedNotificationConfiguration.
        :param sub_category: The subCategory of the ManagedNotificationConfiguration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-usernotifications-managednotificationconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_usernotifications as usernotifications
            
            cfn_managed_notification_configuration_props = usernotifications.CfnManagedNotificationConfigurationProps(
                category="category",
                sub_category="subCategory"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ed668cc0904908639dd9e6fe6fead7965831b8f92757075641d4520b6d8ea74a)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument sub_category", value=sub_category, expected_type=type_hints["sub_category"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if category is not None:
            self._values["category"] = category
        if sub_category is not None:
            self._values["sub_category"] = sub_category

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''The category of the ManagedNotificationConfiguration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-usernotifications-managednotificationconfiguration.html#cfn-usernotifications-managednotificationconfiguration-category
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sub_category(self) -> typing.Optional[builtins.str]:
        '''The subCategory of the ManagedNotificationConfiguration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-usernotifications-managednotificationconfiguration.html#cfn-usernotifications-managednotificationconfiguration-subcategory
        '''
        result = self._values.get("sub_category")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedNotificationConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnManagedNotificationConfiguration",
    "CfnManagedNotificationConfigurationProps",
]

publication.publish()

def _typecheckingstub__a043496630b4e7941136ffd471086811d4add3f355744af29f476688ffc99eaf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    category: typing.Optional[builtins.str] = None,
    sub_category: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94af00cc5ab45f19b4f54a037eb7ec65279c06900c2b0c724c99eeff8c46da25(
    resource: _aws_usernotifications_48e518a2.IManagedNotificationConfigurationRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3826d538e2bb7434a6bd938c55d66122060a736b5fac6fd8fe6d40e92d587497(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f214d52a8bd60860ce3b0cdd241a7b71d2b79db3750829453090213b280bf65(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7800493c5dadecab3e3b0116cc88b0e8a06e869972adbbf62ee21de5b1181b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d58ebdd9774ef67562943832bafc13740ff86a9281f83df24dd9c0cfc2e5e2d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc24f9712a99cf9a161c3d342a09d61552e3b19a201e5984946ab3949cfa2e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed668cc0904908639dd9e6fe6fead7965831b8f92757075641d4520b6d8ea74a(
    *,
    category: typing.Optional[builtins.str] = None,
    sub_category: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

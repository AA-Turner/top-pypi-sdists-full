r'''
# AWS::IdentityStore Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_identitystore as identitystore
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IdentityStore construct libraries](https://constructs.dev/search?q=identitystore)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IdentityStore resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IdentityStore.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IdentityStore](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IdentityStore.html).

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
    import aws_cdk.interfaces.aws_identitystore as _aws_identitystore_22a099c6
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_identitystore_22a099c6 = _LazyImport("aws_cdk.interfaces.aws_identitystore")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_identitystore_22a099c6.IAllGroupMembershipsRef)
class CfnAllGroupMemberships(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_identitystore.CfnAllGroupMemberships",
):
    '''Retrieves membership metadata and attributes for a group membership in an identity store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-allgroupmemberships.html
    :cloudformationResource: AWS::IdentityStore::AllGroupMemberships
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_identitystore as identitystore
        
        cfn_all_group_memberships = identitystore.CfnAllGroupMemberships(self, "MyCfnAllGroupMemberships",
            group_id="groupId",
            identity_store_id="identityStoreId",
            member_id=identitystore.CfnAllGroupMemberships.MemberIdProperty(
                user_id="userId"
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        group_id: typing.Optional[builtins.str] = None,
        identity_store_id: typing.Optional[builtins.str] = None,
        member_id: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAllGroupMemberships.MemberIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IdentityStore::AllGroupMemberships``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param group_id: The identifier for a group in the identity store.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__726fbf37f0bbccb7100b4ac116388440833ff8a7717519444c9c4deb0cd1a990)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAllGroupMembershipsProps(
            group_id=group_id, identity_store_id=identity_store_id, member_id=member_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForAllGroupMemberships")
    @builtins.classmethod
    def arn_for_all_group_memberships(
        cls,
        resource: "_aws_identitystore_22a099c6.IAllGroupMembershipsRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__610ce132deff2a8112195141339fe497d66f782bf05c16580f4889d6a4fd5568)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForAllGroupMemberships", [resource]))

    @jsii.member(jsii_name="isCfnAllGroupMemberships")
    @builtins.classmethod
    def is_cfn_all_group_memberships(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnAllGroupMemberships.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__586732dee037c740a7229d32bf691880ba827a7f1aff5a168be2d1af42f0abb7)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnAllGroupMemberships", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__598118fdbae99d41621dbde57f44f0f1cbad3514e7abf06f0107b2e72cb8704e)
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
            type_hints = cached_type_hints(_typecheckingstub__6e7cae6dc888afa97f3256d438af8db88d15eb200f77217f55189e41621051c6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="allGroupMembershipsRef")
    def all_group_memberships_ref(
        self,
    ) -> "_aws_identitystore_22a099c6.AllGroupMembershipsReference":
        '''A reference to a AllGroupMemberships resource.'''
        return typing.cast("_aws_identitystore_22a099c6.AllGroupMembershipsReference", jsii.get(self, "allGroupMembershipsRef"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the group membership.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time the group membership was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedBy")
    def attr_created_by(self) -> builtins.str:
        '''The identifier of the user or system that created the group membership.

        :cloudformationAttribute: CreatedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedBy"))

    @builtins.property
    @jsii.member(jsii_name="attrMembershipId")
    def attr_membership_id(self) -> builtins.str:
        '''The identifier for a GroupMembership in an identity store.

        :cloudformationAttribute: MembershipId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The date and time the group membership was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedBy")
    def attr_updated_by(self) -> builtins.str:
        '''The identifier of the user or system that last updated the group membership.

        :cloudformationAttribute: UpdatedBy
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedBy"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for a group in the identity store.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1b48f1c2d444de2e073be6f95e0017a5ddc9386affa4db4609d5b3966886c725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> typing.Optional[builtins.str]:
        '''The globally unique identifier for the identity store.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityStoreId"))

    @identity_store_id.setter
    def identity_store_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f45e2605c774b954759e01bcde51d66bc01c5e889f06766ff88cb4491d21fa93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAllGroupMemberships.MemberIdProperty"]]:
        '''An object containing the identifier of a group member.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAllGroupMemberships.MemberIdProperty"]], jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAllGroupMemberships.MemberIdProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__57b8066dfeaad0e983a2ea751771d288814700fcbe769010e6ec2f29d45399aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_identitystore.CfnAllGroupMemberships.MemberIdProperty",
        jsii_struct_bases=[],
        name_mapping={"user_id": "userId"},
    )
    class MemberIdProperty:
        def __init__(self, *, user_id: builtins.str) -> None:
            '''An object containing the identifier of a group member.

            :param user_id: The identifier for a user in the identity store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-allgroupmemberships-memberid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_identitystore as identitystore
                
                member_id_property = identitystore.CfnAllGroupMemberships.MemberIdProperty(
                    user_id="userId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__2b255b4c2b0d6f46f54625d2a67f4380154147a7986fd772390b6e5232ce5b8e)
                check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "user_id": user_id,
            }

        @builtins.property
        def user_id(self) -> builtins.str:
            '''The identifier for a user in the identity store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-allgroupmemberships-memberid.html#cfn-identitystore-allgroupmemberships-memberid-userid
            '''
            result = self._values.get("user_id")
            assert result is not None, "Required property 'user_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_identitystore.CfnAllGroupMembershipsProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "identity_store_id": "identityStoreId",
        "member_id": "memberId",
    },
)
class CfnAllGroupMembershipsProps:
    def __init__(
        self,
        *,
        group_id: typing.Optional[builtins.str] = None,
        identity_store_id: typing.Optional[builtins.str] = None,
        member_id: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnAllGroupMemberships.MemberIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAllGroupMemberships``.

        :param group_id: The identifier for a group in the identity store.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-allgroupmemberships.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_identitystore as identitystore
            
            cfn_all_group_memberships_props = identitystore.CfnAllGroupMembershipsProps(
                group_id="groupId",
                identity_store_id="identityStoreId",
                member_id=identitystore.CfnAllGroupMemberships.MemberIdProperty(
                    user_id="userId"
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dfdb8340ca8bdf07e0c621229c66d30ad01568d482f094d9044a3b9f4a93efae)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_id is not None:
            self._values["group_id"] = group_id
        if identity_store_id is not None:
            self._values["identity_store_id"] = identity_store_id
        if member_id is not None:
            self._values["member_id"] = member_id

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for a group in the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-allgroupmemberships.html#cfn-identitystore-allgroupmemberships-groupid
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_store_id(self) -> typing.Optional[builtins.str]:
        '''The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-allgroupmemberships.html#cfn-identitystore-allgroupmemberships-identitystoreid
        '''
        result = self._values.get("identity_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_id(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAllGroupMemberships.MemberIdProperty"]]:
        '''An object containing the identifier of a group member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-allgroupmemberships.html#cfn-identitystore-allgroupmemberships-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnAllGroupMemberships.MemberIdProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAllGroupMembershipsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_identitystore_22a099c6.IGroupRef)
class CfnGroup(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_identitystore.CfnGroup",
):
    '''A group object, which contains a specified group’s metadata and attributes.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html
    :cloudformationResource: AWS::IdentityStore::Group
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_identitystore as identitystore
        
        cfn_group = identitystore.CfnGroup(self, "MyCfnGroup",
            display_name="displayName",
            identity_store_id="identityStoreId",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        display_name: builtins.str,
        identity_store_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IdentityStore::Group``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param display_name: The display name value for the group. The length limit is 1,024 characters. This value can consist of letters, accented characters, symbols, numbers, punctuation, tab, new line, carriage return, space, and nonbreaking space in this attribute. This value is specified at the time the group is created and stored as an attribute of the group object in the identity store. Prefix search supports a maximum of 1,000 characters for the string.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param description: A string containing the description of the group.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__37e27ff46dfa4082cad1981cc4ade1e2a9ce445cf9aad4a8eb75e162b9b429f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            display_name=display_name,
            identity_store_id=identity_store_id,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForGroup")
    @builtins.classmethod
    def arn_for_group(
        cls,
        resource: "_aws_identitystore_22a099c6.IGroupRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__01ab3c0d3cca733429f775beb080c97f01d0699872b9a2cf17cb7dec5795d17c)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForGroup", [resource]))

    @jsii.member(jsii_name="isCfnGroup")
    @builtins.classmethod
    def is_cfn_group(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnGroup.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b25553d499e3434e811a8393022add9b93718a56b976df383923e4e30e5c468f)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnGroup", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fd30cf433d0f11c47c01b425898b3b3494dae8561dd252ec97cb62a6f3ea01c0)
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
            type_hints = cached_type_hints(_typecheckingstub__181a3492db49132403d11a30d4f4ede267eaa3675413217fae9f2a57427d93a5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGroupId")
    def attr_group_id(self) -> builtins.str:
        '''The identifier of the newly created group in the identity store.

        :cloudformationAttribute: GroupId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGroupId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="groupRef")
    def group_ref(self) -> "_aws_identitystore_22a099c6.GroupReference":
        '''A reference to a Group resource.'''
        return typing.cast("_aws_identitystore_22a099c6.GroupReference", jsii.get(self, "groupRef"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''The display name value for the group.'''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5e2f0d1e640344318d6ca1684bf877149c58a04ff3b658cc26437fd42577ae42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> builtins.str:
        '''The globally unique identifier for the identity store.'''
        return typing.cast(builtins.str, jsii.get(self, "identityStoreId"))

    @identity_store_id.setter
    def identity_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1ec5af9bcaa29b5bd7b1489efc7cb2d8be21651e7c0abc6581d713983f718c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A string containing the description of the group.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__adb1a463b108d61759d25cd969fb5fed9a681bdbfadbf09cefe6655715c026df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_identitystore_22a099c6.IGroupMembershipRef)
class CfnGroupMembership(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_identitystore.CfnGroupMembership",
):
    '''Creates a relationship between a member and a group.

    The following identifiers must be specified: ``GroupId`` , ``IdentityStoreId`` , and ``MemberId`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html
    :cloudformationResource: AWS::IdentityStore::GroupMembership
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_identitystore as identitystore
        
        cfn_group_membership = identitystore.CfnGroupMembership(self, "MyCfnGroupMembership",
            group_id="groupId",
            identity_store_id="identityStoreId",
            member_id=identitystore.CfnGroupMembership.MemberIdProperty(
                user_id="userId"
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        group_id: builtins.str,
        identity_store_id: builtins.str,
        member_id: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnGroupMembership.MemberIdProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Create a new ``AWS::IdentityStore::GroupMembership``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param group_id: The identifier for a group in the identity store.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member. Setting the ``MemberId`` 's ``UserId`` field to a specific User's ID indicates that user is a member of the group.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__76d55a804ce565c6f3a413944bff86b3236786318808951cf53ad4eff71316db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupMembershipProps(
            group_id=group_id, identity_store_id=identity_store_id, member_id=member_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForGroupMembership")
    @builtins.classmethod
    def arn_for_group_membership(
        cls,
        resource: "_aws_identitystore_22a099c6.IGroupMembershipRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7ff9fad22921b91752db10653f5c61dd0bc13a0bf8a3b3888623273813a4e50c)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForGroupMembership", [resource]))

    @jsii.member(jsii_name="isCfnGroupMembership")
    @builtins.classmethod
    def is_cfn_group_membership(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnGroupMembership.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dc267ec839f05f7b319ddb3ef057abfd744e9c55e1ac011a7d51c236a00817e1)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnGroupMembership", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9bbe599298882f9cb39ad950a183df2f00325817213542a0979da08b15e837de)
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
            type_hints = cached_type_hints(_typecheckingstub__f8c6b11b08fd290fc0948df25fb4993347b63ee62d6cc093b9fdb1639f9be8e9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrMembershipId")
    def attr_membership_id(self) -> builtins.str:
        '''The identifier for a ``GroupMembership`` in the identity store.

        :cloudformationAttribute: MembershipId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="groupMembershipRef")
    def group_membership_ref(
        self,
    ) -> "_aws_identitystore_22a099c6.GroupMembershipReference":
        '''A reference to a GroupMembership resource.'''
        return typing.cast("_aws_identitystore_22a099c6.GroupMembershipReference", jsii.get(self, "groupMembershipRef"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''The identifier for a group in the identity store.'''
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__84854d3f76ffaf3fcbc3f65a33c1661f74f5b69424e248ef1e8272d270ac7f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> builtins.str:
        '''The globally unique identifier for the identity store.'''
        return typing.cast(builtins.str, jsii.get(self, "identityStoreId"))

    @identity_store_id.setter
    def identity_store_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cbe6d44611bf93ff14a416179e20aded09542ea5eeadef3315ca4e2b9610a458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityStoreId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnGroupMembership.MemberIdProperty"]:
        '''An object containing the identifier of a group member.'''
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnGroupMembership.MemberIdProperty"], jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(
        self,
        value: typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnGroupMembership.MemberIdProperty"],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1cf491e3e3c3bfc7f52caab31db7140718db94dfca804458b592c7195b7552ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value) # pyright: ignore[reportArgumentType]

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_identitystore.CfnGroupMembership.MemberIdProperty",
        jsii_struct_bases=[],
        name_mapping={"user_id": "userId"},
    )
    class MemberIdProperty:
        def __init__(self, *, user_id: builtins.str) -> None:
            '''An object that contains the identifier of a group member.

            Setting the ``UserID`` field to the specific identifier for a user indicates that the user is a member of the group.

            :param user_id: An object containing the identifiers of resources that can be members.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-groupmembership-memberid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_identitystore as identitystore
                
                member_id_property = identitystore.CfnGroupMembership.MemberIdProperty(
                    user_id="userId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__aa85e069965fcc2401129e3357a969b039233bb2ccffdd9a02afd5dde1c53e25)
                check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "user_id": user_id,
            }

        @builtins.property
        def user_id(self) -> builtins.str:
            '''An object containing the identifiers of resources that can be members.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-groupmembership-memberid.html#cfn-identitystore-groupmembership-memberid-userid
            '''
            result = self._values.get("user_id")
            assert result is not None, "Required property 'user_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_identitystore.CfnGroupMembershipProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "identity_store_id": "identityStoreId",
        "member_id": "memberId",
    },
)
class CfnGroupMembershipProps:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        identity_store_id: builtins.str,
        member_id: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnGroupMembership.MemberIdProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Properties for defining a ``CfnGroupMembership``.

        :param group_id: The identifier for a group in the identity store.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member. Setting the ``MemberId`` 's ``UserId`` field to a specific User's ID indicates that user is a member of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_identitystore as identitystore
            
            cfn_group_membership_props = identitystore.CfnGroupMembershipProps(
                group_id="groupId",
                identity_store_id="identityStoreId",
                member_id=identitystore.CfnGroupMembership.MemberIdProperty(
                    user_id="userId"
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__44a916716d7f3a98b073b5f0337cf90a6d86bd04dc851e6b431e842d7c7184b8)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "identity_store_id": identity_store_id,
            "member_id": member_id,
        }

    @builtins.property
    def group_id(self) -> builtins.str:
        '''The identifier for a group in the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-groupid
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        '''The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-identitystoreid
        '''
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_id(
        self,
    ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnGroupMembership.MemberIdProperty"]:
        '''An object containing the identifier of a group member.

        Setting the ``MemberId`` 's ``UserId`` field to a specific User's ID indicates that user is a member of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-memberid
        '''
        result = self._values.get("member_id")
        assert result is not None, "Required property 'member_id' is missing"
        return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnGroupMembership.MemberIdProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMembershipProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_identitystore.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "display_name": "displayName",
        "identity_store_id": "identityStoreId",
        "description": "description",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        display_name: builtins.str,
        identity_store_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param display_name: The display name value for the group. The length limit is 1,024 characters. This value can consist of letters, accented characters, symbols, numbers, punctuation, tab, new line, carriage return, space, and nonbreaking space in this attribute. This value is specified at the time the group is created and stored as an attribute of the group object in the identity store. Prefix search supports a maximum of 1,000 characters for the string.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param description: A string containing the description of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_identitystore as identitystore
            
            cfn_group_props = identitystore.CfnGroupProps(
                display_name="displayName",
                identity_store_id="identityStoreId",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__84bf79ae8bc719d02791d6f72a1b629f44562f761a2049ee295009880b02ea18)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "identity_store_id": identity_store_id,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name value for the group.

        The length limit is 1,024 characters. This value can consist of letters, accented characters, symbols, numbers, punctuation, tab, new line, carriage return, space, and nonbreaking space in this attribute. This value is specified at the time the group is created and stored as an attribute of the group object in the identity store.

        Prefix search supports a maximum of 1,000 characters for the string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-displayname
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_store_id(self) -> builtins.str:
        '''The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-identitystoreid
        '''
        result = self._values.get("identity_store_id")
        assert result is not None, "Required property 'identity_store_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A string containing the description of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAllGroupMemberships",
    "CfnAllGroupMembershipsProps",
    "CfnGroup",
    "CfnGroupMembership",
    "CfnGroupMembershipProps",
    "CfnGroupProps",
]

publication.publish()

def _typecheckingstub__726fbf37f0bbccb7100b4ac116388440833ff8a7717519444c9c4deb0cd1a990(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_id: typing.Optional[builtins.str] = None,
    identity_store_id: typing.Optional[builtins.str] = None,
    member_id: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAllGroupMemberships.MemberIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610ce132deff2a8112195141339fe497d66f782bf05c16580f4889d6a4fd5568(
    resource: _aws_identitystore_22a099c6.IAllGroupMembershipsRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586732dee037c740a7229d32bf691880ba827a7f1aff5a168be2d1af42f0abb7(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598118fdbae99d41621dbde57f44f0f1cbad3514e7abf06f0107b2e72cb8704e(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7cae6dc888afa97f3256d438af8db88d15eb200f77217f55189e41621051c6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b48f1c2d444de2e073be6f95e0017a5ddc9386affa4db4609d5b3966886c725(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45e2605c774b954759e01bcde51d66bc01c5e889f06766ff88cb4491d21fa93(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b8066dfeaad0e983a2ea751771d288814700fcbe769010e6ec2f29d45399aa(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnAllGroupMemberships.MemberIdProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b255b4c2b0d6f46f54625d2a67f4380154147a7986fd772390b6e5232ce5b8e(
    *,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdb8340ca8bdf07e0c621229c66d30ad01568d482f094d9044a3b9f4a93efae(
    *,
    group_id: typing.Optional[builtins.str] = None,
    identity_store_id: typing.Optional[builtins.str] = None,
    member_id: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnAllGroupMemberships.MemberIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e27ff46dfa4082cad1981cc4ade1e2a9ce445cf9aad4a8eb75e162b9b429f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    display_name: builtins.str,
    identity_store_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ab3c0d3cca733429f775beb080c97f01d0699872b9a2cf17cb7dec5795d17c(
    resource: _aws_identitystore_22a099c6.IGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25553d499e3434e811a8393022add9b93718a56b976df383923e4e30e5c468f(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd30cf433d0f11c47c01b425898b3b3494dae8561dd252ec97cb62a6f3ea01c0(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181a3492db49132403d11a30d4f4ede267eaa3675413217fae9f2a57427d93a5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2f0d1e640344318d6ca1684bf877149c58a04ff3b658cc26437fd42577ae42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec5af9bcaa29b5bd7b1489efc7cb2d8be21651e7c0abc6581d713983f718c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb1a463b108d61759d25cd969fb5fed9a681bdbfadbf09cefe6655715c026df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d55a804ce565c6f3a413944bff86b3236786318808951cf53ad4eff71316db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_id: builtins.str,
    identity_store_id: builtins.str,
    member_id: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnGroupMembership.MemberIdProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ff9fad22921b91752db10653f5c61dd0bc13a0bf8a3b3888623273813a4e50c(
    resource: _aws_identitystore_22a099c6.IGroupMembershipRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc267ec839f05f7b319ddb3ef057abfd744e9c55e1ac011a7d51c236a00817e1(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbe599298882f9cb39ad950a183df2f00325817213542a0979da08b15e837de(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c6b11b08fd290fc0948df25fb4993347b63ee62d6cc093b9fdb1639f9be8e9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84854d3f76ffaf3fcbc3f65a33c1661f74f5b69424e248ef1e8272d270ac7f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe6d44611bf93ff14a416179e20aded09542ea5eeadef3315ca4e2b9610a458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf491e3e3c3bfc7f52caab31db7140718db94dfca804458b592c7195b7552ec(
    value: typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnGroupMembership.MemberIdProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa85e069965fcc2401129e3357a969b039233bb2ccffdd9a02afd5dde1c53e25(
    *,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a916716d7f3a98b073b5f0337cf90a6d86bd04dc851e6b431e842d7c7184b8(
    *,
    group_id: builtins.str,
    identity_store_id: builtins.str,
    member_id: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnGroupMembership.MemberIdProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bf79ae8bc719d02791d6f72a1b629f44562f761a2049ee295009880b02ea18(
    *,
    display_name: builtins.str,
    identity_store_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

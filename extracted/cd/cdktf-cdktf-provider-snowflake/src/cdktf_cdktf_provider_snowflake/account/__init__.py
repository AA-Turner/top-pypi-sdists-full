r'''
# `snowflake_account`

Refer to the Terraform Registry for docs: [`snowflake_account`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Account(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.account.Account",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account snowflake_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_name: builtins.str,
        edition: builtins.str,
        email: builtins.str,
        grace_period_in_days: jsii.Number,
        name: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_rsa_public_key: typing.Optional[builtins.str] = None,
        admin_user_type: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_org_admin: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        must_change_password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        region_group: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account snowflake_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_name: Login name of the initial administrative user of the account. A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_name Account#admin_name}
        :param edition: Snowflake Edition of the account. See more about Snowflake Editions in the `official documentation <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Valid options are: ``STANDARD`` | ``ENTERPRISE`` | ``BUSINESS_CRITICAL`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#edition Account#edition}
        :param email: Email address of the initial administrative user of the account. This email address is used to send any notifications about the account. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#email Account#email}
        :param grace_period_in_days: Specifies the number of days during which the account can be restored (“undropped”). The minimum is 3 days and the maximum is 90 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#grace_period_in_days Account#grace_period_in_days}
        :param name: Specifies the identifier (i.e. name) for the account. It must be unique within an organization, regardless of which Snowflake Region the account is in and must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#name Account#name}
        :param admin_password: Password for the initial administrative user of the account. Either admin_password or admin_rsa_public_key has to be specified. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_password Account#admin_password}
        :param admin_rsa_public_key: Assigns a public key to the initial administrative user of the account. Either admin_password or admin_rsa_public_key has to be specified. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_rsa_public_key Account#admin_rsa_public_key}
        :param admin_user_type: Used for setting the type of the first user that is assigned the ACCOUNTADMIN role during account creation. Valid options are: ``PERSON`` | ``SERVICE`` | ``LEGACY_SERVICE`` External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_user_type Account#admin_user_type}
        :param comment: Specifies a comment for the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#comment Account#comment}
        :param first_name: First name of the initial administrative user of the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#first_name Account#first_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#id Account#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_org_admin: Sets an account property that determines whether the ORGADMIN role is enabled in the account. Only an organization administrator (i.e. user with the ORGADMIN role) can set the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#is_org_admin Account#is_org_admin}
        :param last_name: Last name of the initial administrative user of the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#last_name Account#last_name}
        :param must_change_password: Specifies whether the new user created to administer the account is forced to change their password upon first login into the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#must_change_password Account#must_change_password}
        :param region: `Snowflake Region ID <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-snowflake-region-ids>`_ of the region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region Account#region}
        :param region_group: ID of the region group where the account is created. To retrieve the region group ID for existing accounts in your organization, execute the `SHOW REGIONS <https://docs.snowflake.com/en/sql-reference/sql/show-regions>`_ command. For information about when you might need to specify region group, see `Region groups <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-region-groups>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region_group Account#region_group}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29373c62148b7ac2a789ffbf18a14e4d195a99589893aeffac7dc5a22d115b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccountConfig(
            admin_name=admin_name,
            edition=edition,
            email=email,
            grace_period_in_days=grace_period_in_days,
            name=name,
            admin_password=admin_password,
            admin_rsa_public_key=admin_rsa_public_key,
            admin_user_type=admin_user_type,
            comment=comment,
            first_name=first_name,
            id=id,
            is_org_admin=is_org_admin,
            last_name=last_name,
            must_change_password=must_change_password,
            region=region,
            region_group=region_group,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Account resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Account to import.
        :param import_from_id: The id of the existing Account that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Account to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbfe875f0c4c6ad93184fd38e96e502441e2d5000eae5428207a96cff2233bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetAdminRsaPublicKey")
    def reset_admin_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminRsaPublicKey", []))

    @jsii.member(jsii_name="resetAdminUserType")
    def reset_admin_user_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminUserType", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsOrgAdmin")
    def reset_is_org_admin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsOrgAdmin", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetMustChangePassword")
    def reset_must_change_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMustChangePassword", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRegionGroup")
    def reset_region_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionGroup", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "AccountShowOutputList":
        return typing.cast("AccountShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="adminNameInput")
    def admin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminNameInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminRsaPublicKeyInput")
    def admin_rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminRsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUserTypeInput")
    def admin_user_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUserTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gracePeriodInDaysInput")
    def grace_period_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gracePeriodInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isOrgAdminInput")
    def is_org_admin_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isOrgAdminInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mustChangePasswordInput")
    def must_change_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mustChangePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionGroupInput")
    def region_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="adminName")
    def admin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminName"))

    @admin_name.setter
    def admin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6163896dcab16fd16710ad2a40753a473079e78d9b67ce04bf4dbed3a726f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee2b0b668d131877584b9b9f9bd9da91a8ac0eca865697428e50b2b89506a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminRsaPublicKey")
    def admin_rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminRsaPublicKey"))

    @admin_rsa_public_key.setter
    def admin_rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11a9794d08aae08f0874f8bb161a0d04cb2000de018e83ae779ea9a9c22e016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminRsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adminUserType")
    def admin_user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminUserType"))

    @admin_user_type.setter
    def admin_user_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c235b2cd2ffeba0f766c96be90a91a33ec790ea723f5c79d440f8f6f09614eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUserType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a94eae3c2f6cd2ca32ce95ce2a6580cc790172582322a761973d10bdc00dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b9d86cbfe589f174d83611b9465f4e6f97436bd46332f4671738317c42e443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4846ef9e4d5a8ef166e502a46f05815a04fc0e6104db37c342759fa565ee3ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd203ab91e49886cb22a6a9cf5ffd1227a7766264ff521c812715aeb5a4e66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gracePeriodInDays")
    def grace_period_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gracePeriodInDays"))

    @grace_period_in_days.setter
    def grace_period_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e54f37f20e4b38306cea76770905f2d585ae3948c7bea582830210bb8276b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracePeriodInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b05546c806723aa39bfad5745dceca46c711b42c16da6a1db578590683d3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isOrgAdmin")
    def is_org_admin(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isOrgAdmin"))

    @is_org_admin.setter
    def is_org_admin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b953fd7f7d5b8f16a99cb4b1b2c4fa0db7b346c6477223c513ed157d44373c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isOrgAdmin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77031a3ec032fc044313626f58e6a8bd2d831b0009f7d0c082026edbbf1d3e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mustChangePassword")
    def must_change_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mustChangePassword"))

    @must_change_password.setter
    def must_change_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f8af34993e19c693a1b86d42507c5976d12738fdac85ef4a1db7b55cab0ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130b2230470ce387b43ae3af7d427b002bd349da116bdc4a39bb859343f7bb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f04cdb119dfe3481568784effa2b7792d51e15551c3ab67e3ade1bac345caab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regionGroup")
    def region_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionGroup"))

    @region_group.setter
    def region_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f239fabc136776fcbdb4e1b736f0f2f370000b96e28fb0e1c0d458365ad1c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionGroup", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.account.AccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "admin_name": "adminName",
        "edition": "edition",
        "email": "email",
        "grace_period_in_days": "gracePeriodInDays",
        "name": "name",
        "admin_password": "adminPassword",
        "admin_rsa_public_key": "adminRsaPublicKey",
        "admin_user_type": "adminUserType",
        "comment": "comment",
        "first_name": "firstName",
        "id": "id",
        "is_org_admin": "isOrgAdmin",
        "last_name": "lastName",
        "must_change_password": "mustChangePassword",
        "region": "region",
        "region_group": "regionGroup",
    },
)
class AccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        admin_name: builtins.str,
        edition: builtins.str,
        email: builtins.str,
        grace_period_in_days: jsii.Number,
        name: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_rsa_public_key: typing.Optional[builtins.str] = None,
        admin_user_type: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_org_admin: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        must_change_password: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        region_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_name: Login name of the initial administrative user of the account. A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_name Account#admin_name}
        :param edition: Snowflake Edition of the account. See more about Snowflake Editions in the `official documentation <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Valid options are: ``STANDARD`` | ``ENTERPRISE`` | ``BUSINESS_CRITICAL`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#edition Account#edition}
        :param email: Email address of the initial administrative user of the account. This email address is used to send any notifications about the account. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#email Account#email}
        :param grace_period_in_days: Specifies the number of days during which the account can be restored (“undropped”). The minimum is 3 days and the maximum is 90 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#grace_period_in_days Account#grace_period_in_days}
        :param name: Specifies the identifier (i.e. name) for the account. It must be unique within an organization, regardless of which Snowflake Region the account is in and must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#name Account#name}
        :param admin_password: Password for the initial administrative user of the account. Either admin_password or admin_rsa_public_key has to be specified. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_password Account#admin_password}
        :param admin_rsa_public_key: Assigns a public key to the initial administrative user of the account. Either admin_password or admin_rsa_public_key has to be specified. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_rsa_public_key Account#admin_rsa_public_key}
        :param admin_user_type: Used for setting the type of the first user that is assigned the ACCOUNTADMIN role during account creation. Valid options are: ``PERSON`` | ``SERVICE`` | ``LEGACY_SERVICE`` External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_user_type Account#admin_user_type}
        :param comment: Specifies a comment for the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#comment Account#comment}
        :param first_name: First name of the initial administrative user of the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#first_name Account#first_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#id Account#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_org_admin: Sets an account property that determines whether the ORGADMIN role is enabled in the account. Only an organization administrator (i.e. user with the ORGADMIN role) can set the property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#is_org_admin Account#is_org_admin}
        :param last_name: Last name of the initial administrative user of the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#last_name Account#last_name}
        :param must_change_password: Specifies whether the new user created to administer the account is forced to change their password upon first login into the account. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#must_change_password Account#must_change_password}
        :param region: `Snowflake Region ID <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-snowflake-region-ids>`_ of the region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region Account#region}
        :param region_group: ID of the region group where the account is created. To retrieve the region group ID for existing accounts in your organization, execute the `SHOW REGIONS <https://docs.snowflake.com/en/sql-reference/sql/show-regions>`_ command. For information about when you might need to specify region group, see `Region groups <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-region-groups>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region_group Account#region_group}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b266165bc094077007b82aaae53c2057678021a29a5a57ee79781990bc91348)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_name", value=admin_name, expected_type=type_hints["admin_name"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument grace_period_in_days", value=grace_period_in_days, expected_type=type_hints["grace_period_in_days"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_rsa_public_key", value=admin_rsa_public_key, expected_type=type_hints["admin_rsa_public_key"])
            check_type(argname="argument admin_user_type", value=admin_user_type, expected_type=type_hints["admin_user_type"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_org_admin", value=is_org_admin, expected_type=type_hints["is_org_admin"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument must_change_password", value=must_change_password, expected_type=type_hints["must_change_password"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument region_group", value=region_group, expected_type=type_hints["region_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_name": admin_name,
            "edition": edition,
            "email": email,
            "grace_period_in_days": grace_period_in_days,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if admin_rsa_public_key is not None:
            self._values["admin_rsa_public_key"] = admin_rsa_public_key
        if admin_user_type is not None:
            self._values["admin_user_type"] = admin_user_type
        if comment is not None:
            self._values["comment"] = comment
        if first_name is not None:
            self._values["first_name"] = first_name
        if id is not None:
            self._values["id"] = id
        if is_org_admin is not None:
            self._values["is_org_admin"] = is_org_admin
        if last_name is not None:
            self._values["last_name"] = last_name
        if must_change_password is not None:
            self._values["must_change_password"] = must_change_password
        if region is not None:
            self._values["region"] = region
        if region_group is not None:
            self._values["region_group"] = region_group

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def admin_name(self) -> builtins.str:
        '''Login name of the initial administrative user of the account.

        A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_name Account#admin_name}
        '''
        result = self._values.get("admin_name")
        assert result is not None, "Required property 'admin_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition(self) -> builtins.str:
        '''Snowflake Edition of the account.

        See more about Snowflake Editions in the `official documentation <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Valid options are: ``STANDARD`` | ``ENTERPRISE`` | ``BUSINESS_CRITICAL``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#edition Account#edition}
        '''
        result = self._values.get("edition")
        assert result is not None, "Required property 'edition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the initial administrative user of the account.

        This email address is used to send any notifications about the account. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#email Account#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grace_period_in_days(self) -> jsii.Number:
        '''Specifies the number of days during which the account can be restored (“undropped”).

        The minimum is 3 days and the maximum is 90 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#grace_period_in_days Account#grace_period_in_days}
        '''
        result = self._values.get("grace_period_in_days")
        assert result is not None, "Required property 'grace_period_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier (i.e. name) for the account. It must be unique within an organization, regardless of which Snowflake Region the account is in and must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#name Account#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Password for the initial administrative user of the account.

        Either admin_password or admin_rsa_public_key has to be specified. This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_password Account#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Assigns a public key to the initial administrative user of the account.

        Either admin_password or admin_rsa_public_key has to be specified. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_rsa_public_key Account#admin_rsa_public_key}
        '''
        result = self._values.get("admin_rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_user_type(self) -> typing.Optional[builtins.str]:
        '''Used for setting the type of the first user that is assigned the ACCOUNTADMIN role during account creation.

        Valid options are: ``PERSON`` | ``SERVICE`` | ``LEGACY_SERVICE`` External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#admin_user_type Account#admin_user_type}
        '''
        result = self._values.get("admin_user_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#comment Account#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''First name of the initial administrative user of the account.

        This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#first_name Account#first_name}
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#id Account#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_org_admin(self) -> typing.Optional[builtins.str]:
        '''Sets an account property that determines whether the ORGADMIN role is enabled in the account.

        Only an organization administrator (i.e. user with the ORGADMIN role) can set the property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#is_org_admin Account#is_org_admin}
        '''
        result = self._values.get("is_org_admin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Last name of the initial administrative user of the account.

        This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#last_name Account#last_name}
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def must_change_password(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the new user created to administer the account is forced to change their password upon first login into the account.

        This field cannot be used whenever admin_user_type is set to SERVICE. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#must_change_password Account#must_change_password}
        '''
        result = self._values.get("must_change_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''`Snowflake Region ID <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-snowflake-region-ids>`_ of the region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region Account#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_group(self) -> typing.Optional[builtins.str]:
        '''ID of the region group where the account is created.

        To retrieve the region group ID for existing accounts in your organization, execute the `SHOW REGIONS <https://docs.snowflake.com/en/sql-reference/sql/show-regions>`_ command. For information about when you might need to specify region group, see `Region groups <https://docs.snowflake.com/en/user-guide/admin-account-identifier.html#label-region-groups>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account#region_group Account#region_group}
        '''
        result = self._values.get("region_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.account.AccountShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class AccountShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccountShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.account.AccountShowOutputList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc21166b86e2828495b5588cced4ab4475771a3d11f78e2e8794f6de075a6e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccountShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89db9e7f0014ead45b201b3eab4d053d37293a6bdc44cbb0e9865a0c211afd62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccountShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c652e1f312ea81300af574a19b6a73c3c8651a98eb2c64ff0c3bf6cd64dc5b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12cd67446fd66e709f1d9a57897355b0d35e303205f4581762e5ca7d61565cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667ad99e2c1c40c6840102f5e4c8e339c2dff1188bd959dbb6a1c08b65e4a6f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AccountShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.account.AccountShowOutputOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b984dfe760bbe7cd439ea5e1b477b231f7135870293218f849206fc6e1837791)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="accountLocator")
    def account_locator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountLocator"))

    @builtins.property
    @jsii.member(jsii_name="accountLocatorUrl")
    def account_locator_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountLocatorUrl"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @builtins.property
    @jsii.member(jsii_name="accountOldUrlLastUsed")
    def account_old_url_last_used(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountOldUrlLastUsed"))

    @builtins.property
    @jsii.member(jsii_name="accountOldUrlSavedOn")
    def account_old_url_saved_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountOldUrlSavedOn"))

    @builtins.property
    @jsii.member(jsii_name="accountUrl")
    def account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountUrl"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="consumptionBillingEntityName")
    def consumption_billing_entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumptionBillingEntityName"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="droppedOn")
    def dropped_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "droppedOn"))

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @builtins.property
    @jsii.member(jsii_name="isEventsAccount")
    def is_events_account(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isEventsAccount"))

    @builtins.property
    @jsii.member(jsii_name="isOrgAdmin")
    def is_org_admin(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isOrgAdmin"))

    @builtins.property
    @jsii.member(jsii_name="isOrganizationAccount")
    def is_organization_account(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isOrganizationAccount"))

    @builtins.property
    @jsii.member(jsii_name="managedAccounts")
    def managed_accounts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "managedAccounts"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceConsumerBillingEntityName")
    def marketplace_consumer_billing_entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceConsumerBillingEntityName"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceProviderBillingEntityName")
    def marketplace_provider_billing_entity_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "marketplaceProviderBillingEntityName"))

    @builtins.property
    @jsii.member(jsii_name="movedOn")
    def moved_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "movedOn"))

    @builtins.property
    @jsii.member(jsii_name="movedToOrganization")
    def moved_to_organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "movedToOrganization"))

    @builtins.property
    @jsii.member(jsii_name="oldAccountUrl")
    def old_account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oldAccountUrl"))

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationName"))

    @builtins.property
    @jsii.member(jsii_name="organizationOldUrl")
    def organization_old_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationOldUrl"))

    @builtins.property
    @jsii.member(jsii_name="organizationOldUrlLastUsed")
    def organization_old_url_last_used(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationOldUrlLastUsed"))

    @builtins.property
    @jsii.member(jsii_name="organizationOldUrlSavedOn")
    def organization_old_url_saved_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationOldUrlSavedOn"))

    @builtins.property
    @jsii.member(jsii_name="organizationUrlExpirationOn")
    def organization_url_expiration_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationUrlExpirationOn"))

    @builtins.property
    @jsii.member(jsii_name="regionGroup")
    def region_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionGroup"))

    @builtins.property
    @jsii.member(jsii_name="restoredOn")
    def restored_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restoredOn"))

    @builtins.property
    @jsii.member(jsii_name="scheduledDeletionTime")
    def scheduled_deletion_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheduledDeletionTime"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeRegion")
    def snowflake_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowflakeRegion"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccountShowOutput]:
        return typing.cast(typing.Optional[AccountShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AccountShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509e58dce6e65f2f624d4342982284e4a8fc7b42c7c39918bd65964248452454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Account",
    "AccountConfig",
    "AccountShowOutput",
    "AccountShowOutputList",
    "AccountShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__a29373c62148b7ac2a789ffbf18a14e4d195a99589893aeffac7dc5a22d115b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_name: builtins.str,
    edition: builtins.str,
    email: builtins.str,
    grace_period_in_days: jsii.Number,
    name: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    admin_rsa_public_key: typing.Optional[builtins.str] = None,
    admin_user_type: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_org_admin: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    must_change_password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    region_group: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbfe875f0c4c6ad93184fd38e96e502441e2d5000eae5428207a96cff2233bd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6163896dcab16fd16710ad2a40753a473079e78d9b67ce04bf4dbed3a726f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee2b0b668d131877584b9b9f9bd9da91a8ac0eca865697428e50b2b89506a12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11a9794d08aae08f0874f8bb161a0d04cb2000de018e83ae779ea9a9c22e016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c235b2cd2ffeba0f766c96be90a91a33ec790ea723f5c79d440f8f6f09614eff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a94eae3c2f6cd2ca32ce95ce2a6580cc790172582322a761973d10bdc00dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b9d86cbfe589f174d83611b9465f4e6f97436bd46332f4671738317c42e443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4846ef9e4d5a8ef166e502a46f05815a04fc0e6104db37c342759fa565ee3ee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd203ab91e49886cb22a6a9cf5ffd1227a7766264ff521c812715aeb5a4e66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e54f37f20e4b38306cea76770905f2d585ae3948c7bea582830210bb8276b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b05546c806723aa39bfad5745dceca46c711b42c16da6a1db578590683d3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b953fd7f7d5b8f16a99cb4b1b2c4fa0db7b346c6477223c513ed157d44373c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77031a3ec032fc044313626f58e6a8bd2d831b0009f7d0c082026edbbf1d3e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f8af34993e19c693a1b86d42507c5976d12738fdac85ef4a1db7b55cab0ca9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130b2230470ce387b43ae3af7d427b002bd349da116bdc4a39bb859343f7bb22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f04cdb119dfe3481568784effa2b7792d51e15551c3ab67e3ade1bac345caab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f239fabc136776fcbdb4e1b736f0f2f370000b96e28fb0e1c0d458365ad1c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b266165bc094077007b82aaae53c2057678021a29a5a57ee79781990bc91348(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_name: builtins.str,
    edition: builtins.str,
    email: builtins.str,
    grace_period_in_days: jsii.Number,
    name: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    admin_rsa_public_key: typing.Optional[builtins.str] = None,
    admin_user_type: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_org_admin: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    must_change_password: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    region_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc21166b86e2828495b5588cced4ab4475771a3d11f78e2e8794f6de075a6e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89db9e7f0014ead45b201b3eab4d053d37293a6bdc44cbb0e9865a0c211afd62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c652e1f312ea81300af574a19b6a73c3c8651a98eb2c64ff0c3bf6cd64dc5b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12cd67446fd66e709f1d9a57897355b0d35e303205f4581762e5ca7d61565cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667ad99e2c1c40c6840102f5e4c8e339c2dff1188bd959dbb6a1c08b65e4a6f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b984dfe760bbe7cd439ea5e1b477b231f7135870293218f849206fc6e1837791(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509e58dce6e65f2f624d4342982284e4a8fc7b42c7c39918bd65964248452454(
    value: typing.Optional[AccountShowOutput],
) -> None:
    """Type checking stubs"""
    pass

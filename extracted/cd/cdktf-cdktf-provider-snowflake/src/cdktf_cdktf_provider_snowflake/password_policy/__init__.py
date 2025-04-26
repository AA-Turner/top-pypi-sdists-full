r'''
# `snowflake_password_policy`

Refer to the Terraform Registry for docs: [`snowflake_password_policy`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy).
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


class PasswordPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.passwordPolicy.PasswordPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy snowflake_password_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        history: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lockout_time_mins: typing.Optional[jsii.Number] = None,
        max_age_days: typing.Optional[jsii.Number] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        min_age_days: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        min_lower_case_chars: typing.Optional[jsii.Number] = None,
        min_numeric_chars: typing.Optional[jsii.Number] = None,
        min_special_chars: typing.Optional[jsii.Number] = None,
        min_upper_case_chars: typing.Optional[jsii.Number] = None,
        or_replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy snowflake_password_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database this password policy belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#database PasswordPolicy#database}
        :param name: Identifier for the password policy; must be unique for your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#name PasswordPolicy#name}
        :param schema: The schema this password policy belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#schema PasswordPolicy#schema}
        :param comment: Adds a comment or overwrites an existing comment for the password policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#comment PasswordPolicy#comment}
        :param history: Specifies the number of the most recent passwords that Snowflake stores. These stored passwords cannot be repeated when a user updates their password value. The current password value does not count towards the history. When you increase the history value, Snowflake saves the previous values. When you decrease the value, Snowflake saves the stored values up to that value that is set. For example, if the history value is 8 and you change the history value to 3, Snowflake stores the most recent 3 passwords and deletes the 5 older password values from the history. Default: 0 Max: 24 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#history PasswordPolicy#history}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#id PasswordPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param if_not_exists: Prevent overwriting a previous password policy with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#if_not_exists PasswordPolicy#if_not_exists}
        :param lockout_time_mins: Specifies the number of minutes the user account will be locked after exhausting the designated number of password retries (i.e. PASSWORD_MAX_RETRIES). Supported range: 1 to 999, inclusive. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#lockout_time_mins PasswordPolicy#lockout_time_mins}
        :param max_age_days: Specifies the maximum number of days before the password must be changed. Supported range: 0 to 999, inclusive. A value of zero (i.e. 0) indicates that the password does not need to be changed. Snowflake does not recommend choosing this value for a default account-level password policy or for any user-level policy. Instead, choose a value that meets your internal security guidelines. Default: 90, which means the password must be changed every 90 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_age_days PasswordPolicy#max_age_days}
        :param max_length: Specifies the maximum number of characters the password must contain. This number must be greater than or equal to the sum of PASSWORD_MIN_LENGTH, PASSWORD_MIN_UPPER_CASE_CHARS, and PASSWORD_MIN_LOWER_CASE_CHARS. Supported range: 8 to 256, inclusive. Default: 256 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_length PasswordPolicy#max_length}
        :param max_retries: Specifies the maximum number of attempts to enter a password before being locked out. Supported range: 1 to 10, inclusive. Default: 5 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_retries PasswordPolicy#max_retries}
        :param min_age_days: Specifies the number of days the user must wait before a recently changed password can be changed again. Supported range: 0 to 999, inclusive. Default: 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_age_days PasswordPolicy#min_age_days}
        :param min_length: Specifies the minimum number of characters the password must contain. Supported range: 8 to 256, inclusive. Default: 8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_length PasswordPolicy#min_length}
        :param min_lower_case_chars: Specifies the minimum number of lowercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_lower_case_chars PasswordPolicy#min_lower_case_chars}
        :param min_numeric_chars: Specifies the minimum number of numeric characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_numeric_chars PasswordPolicy#min_numeric_chars}
        :param min_special_chars: Specifies the minimum number of special characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_special_chars PasswordPolicy#min_special_chars}
        :param min_upper_case_chars: Specifies the minimum number of uppercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_upper_case_chars PasswordPolicy#min_upper_case_chars}
        :param or_replace: Whether to override a previous password policy with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#or_replace PasswordPolicy#or_replace}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2acea2c57e41e2af49c5706f8fc97f7160a55d8ebff136551c47bd07f29367)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PasswordPolicyConfig(
            database=database,
            name=name,
            schema=schema,
            comment=comment,
            history=history,
            id=id,
            if_not_exists=if_not_exists,
            lockout_time_mins=lockout_time_mins,
            max_age_days=max_age_days,
            max_length=max_length,
            max_retries=max_retries,
            min_age_days=min_age_days,
            min_length=min_length,
            min_lower_case_chars=min_lower_case_chars,
            min_numeric_chars=min_numeric_chars,
            min_special_chars=min_special_chars,
            min_upper_case_chars=min_upper_case_chars,
            or_replace=or_replace,
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
        '''Generates CDKTF code for importing a PasswordPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PasswordPolicy to import.
        :param import_from_id: The id of the existing PasswordPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PasswordPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eead7a829821e1aea17762cdd477f193a17d9f48ef6679e3ace45a4fcbb888c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetHistory")
    def reset_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHistory", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIfNotExists")
    def reset_if_not_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIfNotExists", []))

    @jsii.member(jsii_name="resetLockoutTimeMins")
    def reset_lockout_time_mins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockoutTimeMins", []))

    @jsii.member(jsii_name="resetMaxAgeDays")
    def reset_max_age_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAgeDays", []))

    @jsii.member(jsii_name="resetMaxLength")
    def reset_max_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLength", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetMinAgeDays")
    def reset_min_age_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinAgeDays", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @jsii.member(jsii_name="resetMinLowerCaseChars")
    def reset_min_lower_case_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLowerCaseChars", []))

    @jsii.member(jsii_name="resetMinNumericChars")
    def reset_min_numeric_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumericChars", []))

    @jsii.member(jsii_name="resetMinSpecialChars")
    def reset_min_special_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinSpecialChars", []))

    @jsii.member(jsii_name="resetMinUpperCaseChars")
    def reset_min_upper_case_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinUpperCaseChars", []))

    @jsii.member(jsii_name="resetOrReplace")
    def reset_or_replace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrReplace", []))

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
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="historyInput")
    def history_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "historyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ifNotExistsInput")
    def if_not_exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ifNotExistsInput"))

    @builtins.property
    @jsii.member(jsii_name="lockoutTimeMinsInput")
    def lockout_time_mins_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockoutTimeMinsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeDaysInput")
    def max_age_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLengthInput")
    def max_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="minAgeDaysInput")
    def min_age_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minAgeDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="minLengthInput")
    def min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="minLowerCaseCharsInput")
    def min_lower_case_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLowerCaseCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumericCharsInput")
    def min_numeric_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumericCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="minSpecialCharsInput")
    def min_special_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minSpecialCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="minUpperCaseCharsInput")
    def min_upper_case_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minUpperCaseCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orReplaceInput")
    def or_replace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "orReplaceInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8785049a313ed30c92c438c455df0fbe551c3a7b8e48200b62c801b3f1e545fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123f8d18a4d8133099d56bea81876c5fbb44d7122ef0308496042ea04edb138a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="history")
    def history(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "history"))

    @history.setter
    def history(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a90ed7bd56bf958947fb02d357f344ba6928c8bf905ce0df6fbe6f84e9811a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "history", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269bd7835bfe9b81b4127af9420343378d450a19cd1af3f83dc37c7f49e8293e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ifNotExists")
    def if_not_exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ifNotExists"))

    @if_not_exists.setter
    def if_not_exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5b1b979b5249a51e8067f52d65665442825c72edfe92a6924647f785e772a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ifNotExists", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockoutTimeMins")
    def lockout_time_mins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockoutTimeMins"))

    @lockout_time_mins.setter
    def lockout_time_mins(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a17cf1ac165929ebb86bf1316be6de7a9259b16cad8029bdd8c9890656ce3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockoutTimeMins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeDays")
    def max_age_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeDays"))

    @max_age_days.setter
    def max_age_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cbed63c6bd1579cdfe25d091212bda172ce0f6c5ea2c0c37e71967f778d9702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxLength")
    def max_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLength"))

    @max_length.setter
    def max_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5238c10da19eace30fd3e73c7753cc001fec0da08996658606ed0b29f8fa5d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec61e0c8d6c7dc8c243916f7ac9dfd32090d72869f02b105a7de3f9cb35871f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minAgeDays")
    def min_age_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minAgeDays"))

    @min_age_days.setter
    def min_age_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621f8af2e4b7cadc257b9db71c232b524d99d41287cf3f2ff39b02c3151b32ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minAgeDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8f427dbaaa7900fc1ea9da980562da8c3df9cfa5cf396b6202425ab4214644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLowerCaseChars")
    def min_lower_case_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLowerCaseChars"))

    @min_lower_case_chars.setter
    def min_lower_case_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd88a385e4ea70ae0923cf58c598fc059b383781264c1007d9d1ebd6ca020213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLowerCaseChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumericChars")
    def min_numeric_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumericChars"))

    @min_numeric_chars.setter
    def min_numeric_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6722f0a2de7f6489a06726b030b64a9192db3da242df52a0aa9a53d563f403b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumericChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minSpecialChars")
    def min_special_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minSpecialChars"))

    @min_special_chars.setter
    def min_special_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eed8db94dadb821e6b5531d297894260b705e1ef2f0bf5bad5678443e616843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minSpecialChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minUpperCaseChars")
    def min_upper_case_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minUpperCaseChars"))

    @min_upper_case_chars.setter
    def min_upper_case_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5013b9b71e0f48bf1021bbcfa8b44a89ad95de50f8d865ac40d018cb630029ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minUpperCaseChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1583db6a4c8b474d4605bb3726b5dc1f18e9ecda415d54c96d0903a5c6727d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orReplace")
    def or_replace(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "orReplace"))

    @or_replace.setter
    def or_replace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1f0dda6d4385ef584227520b7ae9798c138a191206f0d51e79cbc1ddb175b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orReplace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ebfce20ed9c2d1513b25ec4cf7bcba95c84a3be306853e76be0351f0100cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.passwordPolicy.PasswordPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "comment": "comment",
        "history": "history",
        "id": "id",
        "if_not_exists": "ifNotExists",
        "lockout_time_mins": "lockoutTimeMins",
        "max_age_days": "maxAgeDays",
        "max_length": "maxLength",
        "max_retries": "maxRetries",
        "min_age_days": "minAgeDays",
        "min_length": "minLength",
        "min_lower_case_chars": "minLowerCaseChars",
        "min_numeric_chars": "minNumericChars",
        "min_special_chars": "minSpecialChars",
        "min_upper_case_chars": "minUpperCaseChars",
        "or_replace": "orReplace",
    },
)
class PasswordPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        history: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lockout_time_mins: typing.Optional[jsii.Number] = None,
        max_age_days: typing.Optional[jsii.Number] = None,
        max_length: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        min_age_days: typing.Optional[jsii.Number] = None,
        min_length: typing.Optional[jsii.Number] = None,
        min_lower_case_chars: typing.Optional[jsii.Number] = None,
        min_numeric_chars: typing.Optional[jsii.Number] = None,
        min_special_chars: typing.Optional[jsii.Number] = None,
        min_upper_case_chars: typing.Optional[jsii.Number] = None,
        or_replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database this password policy belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#database PasswordPolicy#database}
        :param name: Identifier for the password policy; must be unique for your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#name PasswordPolicy#name}
        :param schema: The schema this password policy belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#schema PasswordPolicy#schema}
        :param comment: Adds a comment or overwrites an existing comment for the password policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#comment PasswordPolicy#comment}
        :param history: Specifies the number of the most recent passwords that Snowflake stores. These stored passwords cannot be repeated when a user updates their password value. The current password value does not count towards the history. When you increase the history value, Snowflake saves the previous values. When you decrease the value, Snowflake saves the stored values up to that value that is set. For example, if the history value is 8 and you change the history value to 3, Snowflake stores the most recent 3 passwords and deletes the 5 older password values from the history. Default: 0 Max: 24 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#history PasswordPolicy#history}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#id PasswordPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param if_not_exists: Prevent overwriting a previous password policy with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#if_not_exists PasswordPolicy#if_not_exists}
        :param lockout_time_mins: Specifies the number of minutes the user account will be locked after exhausting the designated number of password retries (i.e. PASSWORD_MAX_RETRIES). Supported range: 1 to 999, inclusive. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#lockout_time_mins PasswordPolicy#lockout_time_mins}
        :param max_age_days: Specifies the maximum number of days before the password must be changed. Supported range: 0 to 999, inclusive. A value of zero (i.e. 0) indicates that the password does not need to be changed. Snowflake does not recommend choosing this value for a default account-level password policy or for any user-level policy. Instead, choose a value that meets your internal security guidelines. Default: 90, which means the password must be changed every 90 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_age_days PasswordPolicy#max_age_days}
        :param max_length: Specifies the maximum number of characters the password must contain. This number must be greater than or equal to the sum of PASSWORD_MIN_LENGTH, PASSWORD_MIN_UPPER_CASE_CHARS, and PASSWORD_MIN_LOWER_CASE_CHARS. Supported range: 8 to 256, inclusive. Default: 256 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_length PasswordPolicy#max_length}
        :param max_retries: Specifies the maximum number of attempts to enter a password before being locked out. Supported range: 1 to 10, inclusive. Default: 5 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_retries PasswordPolicy#max_retries}
        :param min_age_days: Specifies the number of days the user must wait before a recently changed password can be changed again. Supported range: 0 to 999, inclusive. Default: 0 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_age_days PasswordPolicy#min_age_days}
        :param min_length: Specifies the minimum number of characters the password must contain. Supported range: 8 to 256, inclusive. Default: 8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_length PasswordPolicy#min_length}
        :param min_lower_case_chars: Specifies the minimum number of lowercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_lower_case_chars PasswordPolicy#min_lower_case_chars}
        :param min_numeric_chars: Specifies the minimum number of numeric characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_numeric_chars PasswordPolicy#min_numeric_chars}
        :param min_special_chars: Specifies the minimum number of special characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_special_chars PasswordPolicy#min_special_chars}
        :param min_upper_case_chars: Specifies the minimum number of uppercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_upper_case_chars PasswordPolicy#min_upper_case_chars}
        :param or_replace: Whether to override a previous password policy with the same name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#or_replace PasswordPolicy#or_replace}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0a9ddde49617b17a0880a330ebeb7cad603bdaaee101aea08ac08d8025a6f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument history", value=history, expected_type=type_hints["history"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_not_exists", value=if_not_exists, expected_type=type_hints["if_not_exists"])
            check_type(argname="argument lockout_time_mins", value=lockout_time_mins, expected_type=type_hints["lockout_time_mins"])
            check_type(argname="argument max_age_days", value=max_age_days, expected_type=type_hints["max_age_days"])
            check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument min_age_days", value=min_age_days, expected_type=type_hints["min_age_days"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
            check_type(argname="argument min_lower_case_chars", value=min_lower_case_chars, expected_type=type_hints["min_lower_case_chars"])
            check_type(argname="argument min_numeric_chars", value=min_numeric_chars, expected_type=type_hints["min_numeric_chars"])
            check_type(argname="argument min_special_chars", value=min_special_chars, expected_type=type_hints["min_special_chars"])
            check_type(argname="argument min_upper_case_chars", value=min_upper_case_chars, expected_type=type_hints["min_upper_case_chars"])
            check_type(argname="argument or_replace", value=or_replace, expected_type=type_hints["or_replace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "schema": schema,
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
        if comment is not None:
            self._values["comment"] = comment
        if history is not None:
            self._values["history"] = history
        if id is not None:
            self._values["id"] = id
        if if_not_exists is not None:
            self._values["if_not_exists"] = if_not_exists
        if lockout_time_mins is not None:
            self._values["lockout_time_mins"] = lockout_time_mins
        if max_age_days is not None:
            self._values["max_age_days"] = max_age_days
        if max_length is not None:
            self._values["max_length"] = max_length
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if min_age_days is not None:
            self._values["min_age_days"] = min_age_days
        if min_length is not None:
            self._values["min_length"] = min_length
        if min_lower_case_chars is not None:
            self._values["min_lower_case_chars"] = min_lower_case_chars
        if min_numeric_chars is not None:
            self._values["min_numeric_chars"] = min_numeric_chars
        if min_special_chars is not None:
            self._values["min_special_chars"] = min_special_chars
        if min_upper_case_chars is not None:
            self._values["min_upper_case_chars"] = min_upper_case_chars
        if or_replace is not None:
            self._values["or_replace"] = or_replace

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
    def database(self) -> builtins.str:
        '''The database this password policy belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#database PasswordPolicy#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifier for the password policy; must be unique for your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#name PasswordPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema this password policy belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#schema PasswordPolicy#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Adds a comment or overwrites an existing comment for the password policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#comment PasswordPolicy#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def history(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of the most recent passwords that Snowflake stores.

        These stored passwords cannot be repeated when a user updates their password value. The current password value does not count towards the history. When you increase the history value, Snowflake saves the previous values. When you decrease the value, Snowflake saves the stored values up to that value that is set. For example, if the history value is 8 and you change the history value to 3, Snowflake stores the most recent 3 passwords and deletes the 5 older password values from the history. Default: 0 Max: 24

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#history PasswordPolicy#history}
        '''
        result = self._values.get("history")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#id PasswordPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_not_exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent overwriting a previous password policy with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#if_not_exists PasswordPolicy#if_not_exists}
        '''
        result = self._values.get("if_not_exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lockout_time_mins(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes the user account will be locked after exhausting the designated number of password retries (i.e. PASSWORD_MAX_RETRIES). Supported range: 1 to 999, inclusive. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#lockout_time_mins PasswordPolicy#lockout_time_mins}
        '''
        result = self._values.get("lockout_time_mins")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_age_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of days before the password must be changed.

        Supported range: 0 to 999, inclusive. A value of zero (i.e. 0) indicates that the password does not need to be changed. Snowflake does not recommend choosing this value for a default account-level password policy or for any user-level policy. Instead, choose a value that meets your internal security guidelines. Default: 90, which means the password must be changed every 90 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_age_days PasswordPolicy#max_age_days}
        '''
        result = self._values.get("max_age_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_length(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of characters the password must contain.

        This number must be greater than or equal to the sum of PASSWORD_MIN_LENGTH, PASSWORD_MIN_UPPER_CASE_CHARS, and PASSWORD_MIN_LOWER_CASE_CHARS. Supported range: 8 to 256, inclusive. Default: 256

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_length PasswordPolicy#max_length}
        '''
        result = self._values.get("max_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of attempts to enter a password before being locked out.

        Supported range: 1 to 10, inclusive. Default: 5

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#max_retries PasswordPolicy#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_age_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days the user must wait before a recently changed password can be changed again.

        Supported range: 0 to 999, inclusive. Default: 0

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_age_days PasswordPolicy#min_age_days}
        '''
        result = self._values.get("min_age_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of characters the password must contain. Supported range: 8 to 256, inclusive. Default: 8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_length PasswordPolicy#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_lower_case_chars(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of lowercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_lower_case_chars PasswordPolicy#min_lower_case_chars}
        '''
        result = self._values.get("min_lower_case_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_numeric_chars(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of numeric characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_numeric_chars PasswordPolicy#min_numeric_chars}
        '''
        result = self._values.get("min_numeric_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_special_chars(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of special characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_special_chars PasswordPolicy#min_special_chars}
        '''
        result = self._values.get("min_special_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_upper_case_chars(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of uppercase characters the password must contain. Supported range: 0 to 256, inclusive. Default: 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#min_upper_case_chars PasswordPolicy#min_upper_case_chars}
        '''
        result = self._values.get("min_upper_case_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def or_replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to override a previous password policy with the same name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/password_policy#or_replace PasswordPolicy#or_replace}
        '''
        result = self._values.get("or_replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PasswordPolicy",
    "PasswordPolicyConfig",
]

publication.publish()

def _typecheckingstub__0e2acea2c57e41e2af49c5706f8fc97f7160a55d8ebff136551c47bd07f29367(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    history: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lockout_time_mins: typing.Optional[jsii.Number] = None,
    max_age_days: typing.Optional[jsii.Number] = None,
    max_length: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    min_age_days: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    min_lower_case_chars: typing.Optional[jsii.Number] = None,
    min_numeric_chars: typing.Optional[jsii.Number] = None,
    min_special_chars: typing.Optional[jsii.Number] = None,
    min_upper_case_chars: typing.Optional[jsii.Number] = None,
    or_replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__eead7a829821e1aea17762cdd477f193a17d9f48ef6679e3ace45a4fcbb888c5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8785049a313ed30c92c438c455df0fbe551c3a7b8e48200b62c801b3f1e545fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123f8d18a4d8133099d56bea81876c5fbb44d7122ef0308496042ea04edb138a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a90ed7bd56bf958947fb02d357f344ba6928c8bf905ce0df6fbe6f84e9811a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269bd7835bfe9b81b4127af9420343378d450a19cd1af3f83dc37c7f49e8293e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5b1b979b5249a51e8067f52d65665442825c72edfe92a6924647f785e772a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a17cf1ac165929ebb86bf1316be6de7a9259b16cad8029bdd8c9890656ce3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cbed63c6bd1579cdfe25d091212bda172ce0f6c5ea2c0c37e71967f778d9702(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5238c10da19eace30fd3e73c7753cc001fec0da08996658606ed0b29f8fa5d3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec61e0c8d6c7dc8c243916f7ac9dfd32090d72869f02b105a7de3f9cb35871f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621f8af2e4b7cadc257b9db71c232b524d99d41287cf3f2ff39b02c3151b32ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8f427dbaaa7900fc1ea9da980562da8c3df9cfa5cf396b6202425ab4214644(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd88a385e4ea70ae0923cf58c598fc059b383781264c1007d9d1ebd6ca020213(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6722f0a2de7f6489a06726b030b64a9192db3da242df52a0aa9a53d563f403b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eed8db94dadb821e6b5531d297894260b705e1ef2f0bf5bad5678443e616843(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5013b9b71e0f48bf1021bbcfa8b44a89ad95de50f8d865ac40d018cb630029ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1583db6a4c8b474d4605bb3726b5dc1f18e9ecda415d54c96d0903a5c6727d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1f0dda6d4385ef584227520b7ae9798c138a191206f0d51e79cbc1ddb175b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ebfce20ed9c2d1513b25ec4cf7bcba95c84a3be306853e76be0351f0100cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0a9ddde49617b17a0880a330ebeb7cad603bdaaee101aea08ac08d8025a6f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    history: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    if_not_exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lockout_time_mins: typing.Optional[jsii.Number] = None,
    max_age_days: typing.Optional[jsii.Number] = None,
    max_length: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    min_age_days: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    min_lower_case_chars: typing.Optional[jsii.Number] = None,
    min_numeric_chars: typing.Optional[jsii.Number] = None,
    min_special_chars: typing.Optional[jsii.Number] = None,
    min_upper_case_chars: typing.Optional[jsii.Number] = None,
    or_replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

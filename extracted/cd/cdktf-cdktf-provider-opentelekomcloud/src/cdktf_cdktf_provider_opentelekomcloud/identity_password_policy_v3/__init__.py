r'''
# `opentelekomcloud_identity_password_policy_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_identity_password_policy_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3).
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


class IdentityPasswordPolicyV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.identityPasswordPolicyV3.IdentityPasswordPolicyV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3 opentelekomcloud_identity_password_policy_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        maximum_consecutive_identical_chars: typing.Optional[jsii.Number] = None,
        minimum_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        number_of_recent_passwords_disallowed: typing.Optional[jsii.Number] = None,
        password_char_combination: typing.Optional[jsii.Number] = None,
        password_not_username_or_invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_validity_period: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3 opentelekomcloud_identity_password_policy_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#id IdentityPasswordPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_consecutive_identical_chars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#maximum_consecutive_identical_chars IdentityPasswordPolicyV3#maximum_consecutive_identical_chars}.
        :param minimum_password_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_age IdentityPasswordPolicyV3#minimum_password_age}.
        :param minimum_password_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_length IdentityPasswordPolicyV3#minimum_password_length}.
        :param number_of_recent_passwords_disallowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#number_of_recent_passwords_disallowed IdentityPasswordPolicyV3#number_of_recent_passwords_disallowed}.
        :param password_char_combination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_char_combination IdentityPasswordPolicyV3#password_char_combination}.
        :param password_not_username_or_invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_not_username_or_invert IdentityPasswordPolicyV3#password_not_username_or_invert}.
        :param password_validity_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_validity_period IdentityPasswordPolicyV3#password_validity_period}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b206966f269fcaca13f739f551ebfeacefef272ea9474f4b98e94e9d3c46025)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IdentityPasswordPolicyV3Config(
            id=id,
            maximum_consecutive_identical_chars=maximum_consecutive_identical_chars,
            minimum_password_age=minimum_password_age,
            minimum_password_length=minimum_password_length,
            number_of_recent_passwords_disallowed=number_of_recent_passwords_disallowed,
            password_char_combination=password_char_combination,
            password_not_username_or_invert=password_not_username_or_invert,
            password_validity_period=password_validity_period,
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
        '''Generates CDKTF code for importing a IdentityPasswordPolicyV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IdentityPasswordPolicyV3 to import.
        :param import_from_id: The id of the existing IdentityPasswordPolicyV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IdentityPasswordPolicyV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d96ef17ca0158780dcac41ff671b8f8640f17d12ea8143e5dcf4906b53c7e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaximumConsecutiveIdenticalChars")
    def reset_maximum_consecutive_identical_chars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumConsecutiveIdenticalChars", []))

    @jsii.member(jsii_name="resetMinimumPasswordAge")
    def reset_minimum_password_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumPasswordAge", []))

    @jsii.member(jsii_name="resetMinimumPasswordLength")
    def reset_minimum_password_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumPasswordLength", []))

    @jsii.member(jsii_name="resetNumberOfRecentPasswordsDisallowed")
    def reset_number_of_recent_passwords_disallowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfRecentPasswordsDisallowed", []))

    @jsii.member(jsii_name="resetPasswordCharCombination")
    def reset_password_char_combination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordCharCombination", []))

    @jsii.member(jsii_name="resetPasswordNotUsernameOrInvert")
    def reset_password_not_username_or_invert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordNotUsernameOrInvert", []))

    @jsii.member(jsii_name="resetPasswordValidityPeriod")
    def reset_password_validity_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordValidityPeriod", []))

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
    @jsii.member(jsii_name="maximumPasswordLength")
    def maximum_password_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumPasswordLength"))

    @builtins.property
    @jsii.member(jsii_name="passwordRequirements")
    def password_requirements(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordRequirements"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumConsecutiveIdenticalCharsInput")
    def maximum_consecutive_identical_chars_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumConsecutiveIdenticalCharsInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumPasswordAgeInput")
    def minimum_password_age_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumPasswordAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumPasswordLengthInput")
    def minimum_password_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumPasswordLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfRecentPasswordsDisallowedInput")
    def number_of_recent_passwords_disallowed_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfRecentPasswordsDisallowedInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordCharCombinationInput")
    def password_char_combination_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordCharCombinationInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordNotUsernameOrInvertInput")
    def password_not_username_or_invert_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordNotUsernameOrInvertInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordValidityPeriodInput")
    def password_validity_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "passwordValidityPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb1f03cdded6059077ea1702dda26af71e34a96dfe0f15d7dedcc9a82ef4adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumConsecutiveIdenticalChars")
    def maximum_consecutive_identical_chars(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumConsecutiveIdenticalChars"))

    @maximum_consecutive_identical_chars.setter
    def maximum_consecutive_identical_chars(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab39f1453c3e1c5ca4a1848d6277c9f91f41ec2a4e853d03c3b0057bfa769d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumConsecutiveIdenticalChars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumPasswordAge")
    def minimum_password_age(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumPasswordAge"))

    @minimum_password_age.setter
    def minimum_password_age(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce221b4064b5c13406c05a623ccbbe343aff29a163be0e5e225315f2fddad0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumPasswordAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumPasswordLength")
    def minimum_password_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumPasswordLength"))

    @minimum_password_length.setter
    def minimum_password_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c7f46e92042bd991507130515dffdea4f929b3656b69e274e6056672f34937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumPasswordLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numberOfRecentPasswordsDisallowed")
    def number_of_recent_passwords_disallowed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfRecentPasswordsDisallowed"))

    @number_of_recent_passwords_disallowed.setter
    def number_of_recent_passwords_disallowed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e57807c92b6aa6ab5d8435dd4c6d0fc376225aa83f34a2b3d6fb8d36890514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfRecentPasswordsDisallowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordCharCombination")
    def password_char_combination(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordCharCombination"))

    @password_char_combination.setter
    def password_char_combination(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ad87aa7497fe32b594bc99efe0524f7e06b5d32f294b2c1db5afeeb902a210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordCharCombination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordNotUsernameOrInvert")
    def password_not_username_or_invert(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordNotUsernameOrInvert"))

    @password_not_username_or_invert.setter
    def password_not_username_or_invert(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f1e31b4da325c47c368edf9b0e44b9fba5470d4c3260b2d6994240a787cfdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordNotUsernameOrInvert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordValidityPeriod")
    def password_validity_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "passwordValidityPeriod"))

    @password_validity_period.setter
    def password_validity_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4dcdedb0a4e91f40fb2031683a2d495ecb60956889d73b4cd363cad0f518f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordValidityPeriod", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.identityPasswordPolicyV3.IdentityPasswordPolicyV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "maximum_consecutive_identical_chars": "maximumConsecutiveIdenticalChars",
        "minimum_password_age": "minimumPasswordAge",
        "minimum_password_length": "minimumPasswordLength",
        "number_of_recent_passwords_disallowed": "numberOfRecentPasswordsDisallowed",
        "password_char_combination": "passwordCharCombination",
        "password_not_username_or_invert": "passwordNotUsernameOrInvert",
        "password_validity_period": "passwordValidityPeriod",
    },
)
class IdentityPasswordPolicyV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        maximum_consecutive_identical_chars: typing.Optional[jsii.Number] = None,
        minimum_password_age: typing.Optional[jsii.Number] = None,
        minimum_password_length: typing.Optional[jsii.Number] = None,
        number_of_recent_passwords_disallowed: typing.Optional[jsii.Number] = None,
        password_char_combination: typing.Optional[jsii.Number] = None,
        password_not_username_or_invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_validity_period: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#id IdentityPasswordPolicyV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_consecutive_identical_chars: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#maximum_consecutive_identical_chars IdentityPasswordPolicyV3#maximum_consecutive_identical_chars}.
        :param minimum_password_age: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_age IdentityPasswordPolicyV3#minimum_password_age}.
        :param minimum_password_length: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_length IdentityPasswordPolicyV3#minimum_password_length}.
        :param number_of_recent_passwords_disallowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#number_of_recent_passwords_disallowed IdentityPasswordPolicyV3#number_of_recent_passwords_disallowed}.
        :param password_char_combination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_char_combination IdentityPasswordPolicyV3#password_char_combination}.
        :param password_not_username_or_invert: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_not_username_or_invert IdentityPasswordPolicyV3#password_not_username_or_invert}.
        :param password_validity_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_validity_period IdentityPasswordPolicyV3#password_validity_period}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f338213e857a5c17a78b93319597fc091adfcd582bd1020befe6cbe9ff796a2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maximum_consecutive_identical_chars", value=maximum_consecutive_identical_chars, expected_type=type_hints["maximum_consecutive_identical_chars"])
            check_type(argname="argument minimum_password_age", value=minimum_password_age, expected_type=type_hints["minimum_password_age"])
            check_type(argname="argument minimum_password_length", value=minimum_password_length, expected_type=type_hints["minimum_password_length"])
            check_type(argname="argument number_of_recent_passwords_disallowed", value=number_of_recent_passwords_disallowed, expected_type=type_hints["number_of_recent_passwords_disallowed"])
            check_type(argname="argument password_char_combination", value=password_char_combination, expected_type=type_hints["password_char_combination"])
            check_type(argname="argument password_not_username_or_invert", value=password_not_username_or_invert, expected_type=type_hints["password_not_username_or_invert"])
            check_type(argname="argument password_validity_period", value=password_validity_period, expected_type=type_hints["password_validity_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if id is not None:
            self._values["id"] = id
        if maximum_consecutive_identical_chars is not None:
            self._values["maximum_consecutive_identical_chars"] = maximum_consecutive_identical_chars
        if minimum_password_age is not None:
            self._values["minimum_password_age"] = minimum_password_age
        if minimum_password_length is not None:
            self._values["minimum_password_length"] = minimum_password_length
        if number_of_recent_passwords_disallowed is not None:
            self._values["number_of_recent_passwords_disallowed"] = number_of_recent_passwords_disallowed
        if password_char_combination is not None:
            self._values["password_char_combination"] = password_char_combination
        if password_not_username_or_invert is not None:
            self._values["password_not_username_or_invert"] = password_not_username_or_invert
        if password_validity_period is not None:
            self._values["password_validity_period"] = password_validity_period

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#id IdentityPasswordPolicyV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_consecutive_identical_chars(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#maximum_consecutive_identical_chars IdentityPasswordPolicyV3#maximum_consecutive_identical_chars}.'''
        result = self._values.get("maximum_consecutive_identical_chars")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_password_age(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_age IdentityPasswordPolicyV3#minimum_password_age}.'''
        result = self._values.get("minimum_password_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_password_length(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#minimum_password_length IdentityPasswordPolicyV3#minimum_password_length}.'''
        result = self._values.get("minimum_password_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_recent_passwords_disallowed(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#number_of_recent_passwords_disallowed IdentityPasswordPolicyV3#number_of_recent_passwords_disallowed}.'''
        result = self._values.get("number_of_recent_passwords_disallowed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_char_combination(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_char_combination IdentityPasswordPolicyV3#password_char_combination}.'''
        result = self._values.get("password_char_combination")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password_not_username_or_invert(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_not_username_or_invert IdentityPasswordPolicyV3#password_not_username_or_invert}.'''
        result = self._values.get("password_not_username_or_invert")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_validity_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/identity_password_policy_v3#password_validity_period IdentityPasswordPolicyV3#password_validity_period}.'''
        result = self._values.get("password_validity_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityPasswordPolicyV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdentityPasswordPolicyV3",
    "IdentityPasswordPolicyV3Config",
]

publication.publish()

def _typecheckingstub__5b206966f269fcaca13f739f551ebfeacefef272ea9474f4b98e94e9d3c46025(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    maximum_consecutive_identical_chars: typing.Optional[jsii.Number] = None,
    minimum_password_age: typing.Optional[jsii.Number] = None,
    minimum_password_length: typing.Optional[jsii.Number] = None,
    number_of_recent_passwords_disallowed: typing.Optional[jsii.Number] = None,
    password_char_combination: typing.Optional[jsii.Number] = None,
    password_not_username_or_invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_validity_period: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__65d96ef17ca0158780dcac41ff671b8f8640f17d12ea8143e5dcf4906b53c7e5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb1f03cdded6059077ea1702dda26af71e34a96dfe0f15d7dedcc9a82ef4adc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab39f1453c3e1c5ca4a1848d6277c9f91f41ec2a4e853d03c3b0057bfa769d44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce221b4064b5c13406c05a623ccbbe343aff29a163be0e5e225315f2fddad0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c7f46e92042bd991507130515dffdea4f929b3656b69e274e6056672f34937(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e57807c92b6aa6ab5d8435dd4c6d0fc376225aa83f34a2b3d6fb8d36890514(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ad87aa7497fe32b594bc99efe0524f7e06b5d32f294b2c1db5afeeb902a210(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f1e31b4da325c47c368edf9b0e44b9fba5470d4c3260b2d6994240a787cfdd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4dcdedb0a4e91f40fb2031683a2d495ecb60956889d73b4cd363cad0f518f1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f338213e857a5c17a78b93319597fc091adfcd582bd1020befe6cbe9ff796a2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_consecutive_identical_chars: typing.Optional[jsii.Number] = None,
    minimum_password_age: typing.Optional[jsii.Number] = None,
    minimum_password_length: typing.Optional[jsii.Number] = None,
    number_of_recent_passwords_disallowed: typing.Optional[jsii.Number] = None,
    password_char_combination: typing.Optional[jsii.Number] = None,
    password_not_username_or_invert: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_validity_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

r'''
# `random_password`

Refer to the Terraform Registry for docs: [`random_password`](https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password).
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


class Password(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-random.password.Password",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password random_password}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        length: jsii.Number,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lower: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_lower: typing.Optional[jsii.Number] = None,
        min_numeric: typing.Optional[jsii.Number] = None,
        min_special: typing.Optional[jsii.Number] = None,
        min_upper: typing.Optional[jsii.Number] = None,
        number: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        override_special: typing.Optional[builtins.str] = None,
        special: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password random_password} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param length: The length of the string desired. The minimum value for length is 1 and, length must also be >= (``min_upper`` + ``min_lower`` + ``min_numeric`` + ``min_special``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#length Password#length}
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. See `the main provider documentation <../index.html>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#keepers Password#keepers}
        :param lower: Include lowercase alphabet characters in the result. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#lower Password#lower}
        :param min_lower: Minimum number of lowercase alphabet characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_lower Password#min_lower}
        :param min_numeric: Minimum number of numeric characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_numeric Password#min_numeric}
        :param min_special: Minimum number of special characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_special Password#min_special}
        :param min_upper: Minimum number of uppercase alphabet characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_upper Password#min_upper}
        :param number: Include numeric characters in the result. Default value is ``true``. If ``number``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``. **NOTE**: This is deprecated, use ``numeric`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#number Password#number}
        :param numeric: Include numeric characters in the result. Default value is ``true``. If ``numeric``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#numeric Password#numeric}
        :param override_special: Supply your own list of special characters to use for string generation. This overrides the default character list in the special argument. The ``special`` argument must still be set to true for any overwritten characters to be used in generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#override_special Password#override_special}
        :param special: Include special characters in the result. These are ``!@#$%&*()-_=+[]{}<>:?``. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#special Password#special}
        :param upper: Include uppercase alphabet characters in the result. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#upper Password#upper}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e551c8c31386c14a4d9e880761e3ad6391b123483c2f43e664b9de076b25cb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PasswordConfig(
            length=length,
            keepers=keepers,
            lower=lower,
            min_lower=min_lower,
            min_numeric=min_numeric,
            min_special=min_special,
            min_upper=min_upper,
            number=number,
            numeric=numeric,
            override_special=override_special,
            special=special,
            upper=upper,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Password resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Password to import.
        :param import_from_id: The id of the existing Password that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Password to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a92fd9be03709d392a29bb40ceeac3de3c08c603f48b811a8baf72c05740c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetKeepers")
    def reset_keepers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepers", []))

    @jsii.member(jsii_name="resetLower")
    def reset_lower(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLower", []))

    @jsii.member(jsii_name="resetMinLower")
    def reset_min_lower(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLower", []))

    @jsii.member(jsii_name="resetMinNumeric")
    def reset_min_numeric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumeric", []))

    @jsii.member(jsii_name="resetMinSpecial")
    def reset_min_special(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinSpecial", []))

    @jsii.member(jsii_name="resetMinUpper")
    def reset_min_upper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinUpper", []))

    @jsii.member(jsii_name="resetNumber")
    def reset_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumber", []))

    @jsii.member(jsii_name="resetNumeric")
    def reset_numeric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumeric", []))

    @jsii.member(jsii_name="resetOverrideSpecial")
    def reset_override_special(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverrideSpecial", []))

    @jsii.member(jsii_name="resetSpecial")
    def reset_special(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecial", []))

    @jsii.member(jsii_name="resetUpper")
    def reset_upper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpper", []))

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
    @jsii.member(jsii_name="bcryptHash")
    def bcrypt_hash(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bcryptHash"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="result")
    def result(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "result"))

    @builtins.property
    @jsii.member(jsii_name="keepersInput")
    def keepers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "keepersInput"))

    @builtins.property
    @jsii.member(jsii_name="lengthInput")
    def length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lengthInput"))

    @builtins.property
    @jsii.member(jsii_name="lowerInput")
    def lower_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lowerInput"))

    @builtins.property
    @jsii.member(jsii_name="minLowerInput")
    def min_lower_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLowerInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumericInput")
    def min_numeric_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumericInput"))

    @builtins.property
    @jsii.member(jsii_name="minSpecialInput")
    def min_special_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minSpecialInput"))

    @builtins.property
    @jsii.member(jsii_name="minUpperInput")
    def min_upper_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minUpperInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInput")
    def number_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "numberInput"))

    @builtins.property
    @jsii.member(jsii_name="numericInput")
    def numeric_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "numericInput"))

    @builtins.property
    @jsii.member(jsii_name="overrideSpecialInput")
    def override_special_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overrideSpecialInput"))

    @builtins.property
    @jsii.member(jsii_name="specialInput")
    def special_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "specialInput"))

    @builtins.property
    @jsii.member(jsii_name="upperInput")
    def upper_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "upperInput"))

    @builtins.property
    @jsii.member(jsii_name="keepers")
    def keepers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "keepers"))

    @keepers.setter
    def keepers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8030d1618e10d401799eddf93ac4e4434bc0ad00a57bfade382cdb7d87cebfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @length.setter
    def length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4621074ba4c1eaf8ee06b367d4afbccf705db6f545b4195a2ea9f2537f41eb96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "length", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lower")
    def lower(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lower"))

    @lower.setter
    def lower(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b879eb3ddeb4d0229973f9d616db046a53dc600c8c542530341fd54b1272adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lower", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLower")
    def min_lower(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLower"))

    @min_lower.setter
    def min_lower(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f230333567ebd24638104b6a8bb1868f85324676358f26ea9138a507675909d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLower", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumeric")
    def min_numeric(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumeric"))

    @min_numeric.setter
    def min_numeric(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5027df8dfb402bd99ae92ee45efcc3c49e6b15044c65f4ee36f1800577c11815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumeric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minSpecial")
    def min_special(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minSpecial"))

    @min_special.setter
    def min_special(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__565115f707f1f7b60f3ccc621dbdf805c8a48f8c0de2c96e061e5238b980e372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minSpecial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minUpper")
    def min_upper(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minUpper"))

    @min_upper.setter
    def min_upper(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134cd35efad525f1e98cc34998f84ac703f49afcef66fe57319497383b09c34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minUpper", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="number")
    def number(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "number"))

    @number.setter
    def number(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762c6b25391ac398250b39a62ae8e33bce77ca1a1636467a01122f13899e5289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "number", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numeric")
    def numeric(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "numeric"))

    @numeric.setter
    def numeric(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42eafd550647443815aa0f3cf08f15d7018bc098fca1f3d05f2ed865869c34ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numeric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overrideSpecial")
    def override_special(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overrideSpecial"))

    @override_special.setter
    def override_special(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e2a5640362a1d62b3abec1609e026f34023a8a262025e90df4720f5ba5bd91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrideSpecial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="special")
    def special(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "special"))

    @special.setter
    def special(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8878ce09727fc38090c0b215a77611954f8baf20d16c65c97ee0d9afc2b49885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "special", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="upper")
    def upper(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "upper"))

    @upper.setter
    def upper(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4581220dfa128521ae6b11fcf58af39e0e0ed82d93bd87f2f0b559e2fb408df8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "upper", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-random.password.PasswordConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "length": "length",
        "keepers": "keepers",
        "lower": "lower",
        "min_lower": "minLower",
        "min_numeric": "minNumeric",
        "min_special": "minSpecial",
        "min_upper": "minUpper",
        "number": "number",
        "numeric": "numeric",
        "override_special": "overrideSpecial",
        "special": "special",
        "upper": "upper",
    },
)
class PasswordConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        length: jsii.Number,
        keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lower: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_lower: typing.Optional[jsii.Number] = None,
        min_numeric: typing.Optional[jsii.Number] = None,
        min_special: typing.Optional[jsii.Number] = None,
        min_upper: typing.Optional[jsii.Number] = None,
        number: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        override_special: typing.Optional[builtins.str] = None,
        special: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        upper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param length: The length of the string desired. The minimum value for length is 1 and, length must also be >= (``min_upper`` + ``min_lower`` + ``min_numeric`` + ``min_special``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#length Password#length}
        :param keepers: Arbitrary map of values that, when changed, will trigger recreation of resource. See `the main provider documentation <../index.html>`_ for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#keepers Password#keepers}
        :param lower: Include lowercase alphabet characters in the result. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#lower Password#lower}
        :param min_lower: Minimum number of lowercase alphabet characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_lower Password#min_lower}
        :param min_numeric: Minimum number of numeric characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_numeric Password#min_numeric}
        :param min_special: Minimum number of special characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_special Password#min_special}
        :param min_upper: Minimum number of uppercase alphabet characters in the result. Default value is ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_upper Password#min_upper}
        :param number: Include numeric characters in the result. Default value is ``true``. If ``number``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``. **NOTE**: This is deprecated, use ``numeric`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#number Password#number}
        :param numeric: Include numeric characters in the result. Default value is ``true``. If ``numeric``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#numeric Password#numeric}
        :param override_special: Supply your own list of special characters to use for string generation. This overrides the default character list in the special argument. The ``special`` argument must still be set to true for any overwritten characters to be used in generation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#override_special Password#override_special}
        :param special: Include special characters in the result. These are ``!@#$%&*()-_=+[]{}<>:?``. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#special Password#special}
        :param upper: Include uppercase alphabet characters in the result. Default value is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#upper Password#upper}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccfa84c3510bfa1c353c6a9e0e8bda72c3150582c6236e52d43e799da8e7e692)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
            check_type(argname="argument keepers", value=keepers, expected_type=type_hints["keepers"])
            check_type(argname="argument lower", value=lower, expected_type=type_hints["lower"])
            check_type(argname="argument min_lower", value=min_lower, expected_type=type_hints["min_lower"])
            check_type(argname="argument min_numeric", value=min_numeric, expected_type=type_hints["min_numeric"])
            check_type(argname="argument min_special", value=min_special, expected_type=type_hints["min_special"])
            check_type(argname="argument min_upper", value=min_upper, expected_type=type_hints["min_upper"])
            check_type(argname="argument number", value=number, expected_type=type_hints["number"])
            check_type(argname="argument numeric", value=numeric, expected_type=type_hints["numeric"])
            check_type(argname="argument override_special", value=override_special, expected_type=type_hints["override_special"])
            check_type(argname="argument special", value=special, expected_type=type_hints["special"])
            check_type(argname="argument upper", value=upper, expected_type=type_hints["upper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "length": length,
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
        if keepers is not None:
            self._values["keepers"] = keepers
        if lower is not None:
            self._values["lower"] = lower
        if min_lower is not None:
            self._values["min_lower"] = min_lower
        if min_numeric is not None:
            self._values["min_numeric"] = min_numeric
        if min_special is not None:
            self._values["min_special"] = min_special
        if min_upper is not None:
            self._values["min_upper"] = min_upper
        if number is not None:
            self._values["number"] = number
        if numeric is not None:
            self._values["numeric"] = numeric
        if override_special is not None:
            self._values["override_special"] = override_special
        if special is not None:
            self._values["special"] = special
        if upper is not None:
            self._values["upper"] = upper

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
    def length(self) -> jsii.Number:
        '''The length of the string desired.

        The minimum value for length is 1 and, length must also be >= (``min_upper`` + ``min_lower`` + ``min_numeric`` + ``min_special``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#length Password#length}
        '''
        result = self._values.get("length")
        assert result is not None, "Required property 'length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def keepers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Arbitrary map of values that, when changed, will trigger recreation of resource.

        See `the main provider documentation <../index.html>`_ for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#keepers Password#keepers}
        '''
        result = self._values.get("keepers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lower(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include lowercase alphabet characters in the result. Default value is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#lower Password#lower}
        '''
        result = self._values.get("lower")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_lower(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of lowercase alphabet characters in the result. Default value is ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_lower Password#min_lower}
        '''
        result = self._values.get("min_lower")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_numeric(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of numeric characters in the result. Default value is ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_numeric Password#min_numeric}
        '''
        result = self._values.get("min_numeric")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_special(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of special characters in the result. Default value is ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_special Password#min_special}
        '''
        result = self._values.get("min_special")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_upper(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of uppercase alphabet characters in the result. Default value is ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#min_upper Password#min_upper}
        '''
        result = self._values.get("min_upper")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include numeric characters in the result.

        Default value is ``true``. If ``number``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``. **NOTE**: This is deprecated, use ``numeric`` instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#number Password#number}
        '''
        result = self._values.get("number")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def numeric(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include numeric characters in the result.

        Default value is ``true``. If ``numeric``, ``upper``, ``lower``, and ``special`` are all configured, at least one of them must be set to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#numeric Password#numeric}
        '''
        result = self._values.get("numeric")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def override_special(self) -> typing.Optional[builtins.str]:
        '''Supply your own list of special characters to use for string generation.

        This overrides the default character list in the special argument.  The ``special`` argument must still be set to true for any overwritten characters to be used in generation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#override_special Password#override_special}
        '''
        result = self._values.get("override_special")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def special(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include special characters in the result. These are ``!@#$%&*()-_=+[]{}<>:?``. Default value is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#special Password#special}
        '''
        result = self._values.get("special")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def upper(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include uppercase alphabet characters in the result. Default value is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/random/3.7.2/docs/resources/password#upper Password#upper}
        '''
        result = self._values.get("upper")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PasswordConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Password",
    "PasswordConfig",
]

publication.publish()

def _typecheckingstub__4e551c8c31386c14a4d9e880761e3ad6391b123483c2f43e664b9de076b25cb0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    length: jsii.Number,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lower: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_lower: typing.Optional[jsii.Number] = None,
    min_numeric: typing.Optional[jsii.Number] = None,
    min_special: typing.Optional[jsii.Number] = None,
    min_upper: typing.Optional[jsii.Number] = None,
    number: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    override_special: typing.Optional[builtins.str] = None,
    special: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__30a92fd9be03709d392a29bb40ceeac3de3c08c603f48b811a8baf72c05740c0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8030d1618e10d401799eddf93ac4e4434bc0ad00a57bfade382cdb7d87cebfe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4621074ba4c1eaf8ee06b367d4afbccf705db6f545b4195a2ea9f2537f41eb96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b879eb3ddeb4d0229973f9d616db046a53dc600c8c542530341fd54b1272adb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f230333567ebd24638104b6a8bb1868f85324676358f26ea9138a507675909d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5027df8dfb402bd99ae92ee45efcc3c49e6b15044c65f4ee36f1800577c11815(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__565115f707f1f7b60f3ccc621dbdf805c8a48f8c0de2c96e061e5238b980e372(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134cd35efad525f1e98cc34998f84ac703f49afcef66fe57319497383b09c34e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762c6b25391ac398250b39a62ae8e33bce77ca1a1636467a01122f13899e5289(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42eafd550647443815aa0f3cf08f15d7018bc098fca1f3d05f2ed865869c34ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e2a5640362a1d62b3abec1609e026f34023a8a262025e90df4720f5ba5bd91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8878ce09727fc38090c0b215a77611954f8baf20d16c65c97ee0d9afc2b49885(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4581220dfa128521ae6b11fcf58af39e0e0ed82d93bd87f2f0b559e2fb408df8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfa84c3510bfa1c353c6a9e0e8bda72c3150582c6236e52d43e799da8e7e692(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    length: jsii.Number,
    keepers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lower: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_lower: typing.Optional[jsii.Number] = None,
    min_numeric: typing.Optional[jsii.Number] = None,
    min_special: typing.Optional[jsii.Number] = None,
    min_upper: typing.Optional[jsii.Number] = None,
    number: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    numeric: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    override_special: typing.Optional[builtins.str] = None,
    special: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    upper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

r'''
# `datadog_synthetics_global_variable`

Refer to the Terraform Registry for docs: [`datadog_synthetics_global_variable`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable).
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


class SyntheticsGlobalVariable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariable",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable datadog_synthetics_global_variable}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        is_fido: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_totp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_test_id: typing.Optional[builtins.str] = None,
        parse_test_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableParseTestOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        value: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable datadog_synthetics_global_variable} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Synthetics global variable name. Must be all uppercase with underscores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        :param description: Description of the global variable. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        :param is_fido: If set to true, the global variable is a FIDO variable. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_fido SyntheticsGlobalVariable#is_fido}
        :param is_totp: If set to true, the global variable is a TOTP variable. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_totp SyntheticsGlobalVariable#is_totp}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#options SyntheticsGlobalVariable#options}
        :param parse_test_id: Id of the Synthetics test to use for a variable from test. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        :param parse_test_options: parse_test_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        :param restricted_roles: A list of role identifiers to associate with the Synthetics global variable. **Deprecated.** This field is no longer supported by the Datadog API. Please use ``datadog_restriction_policy`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        :param secure: If set to true, the value of the global variable is hidden. This setting is automatically set to ``true`` if ``is_totp`` or ``is_fido`` is set to ``true``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        :param tags: A list of tags to associate with your synthetics global variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        :param value: The value of the global variable. Required unless ``is_fido`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8130ffd11a0e21ba65645d2942d6d24827dd309902720b48e6aa8bb09898234a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SyntheticsGlobalVariableConfig(
            name=name,
            description=description,
            is_fido=is_fido,
            is_totp=is_totp,
            options=options,
            parse_test_id=parse_test_id,
            parse_test_options=parse_test_options,
            restricted_roles=restricted_roles,
            secure=secure,
            tags=tags,
            value=value,
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
        '''Generates CDKTF code for importing a SyntheticsGlobalVariable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SyntheticsGlobalVariable to import.
        :param import_from_id: The id of the existing SyntheticsGlobalVariable that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SyntheticsGlobalVariable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36187fd5360e5ed4828e5ce73bbe0a81b0ac61df3e000fd6091b01322daf64ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9309d5506c1c99c479fc71c47525566a2845a98125d812bcb97489c0fd0e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="putParseTestOptions")
    def put_parse_test_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableParseTestOptions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2642918805c9f24132f34236a3d3ba4cf8e6a62e8abe9c8bbab0f6c3d81b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParseTestOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIsFido")
    def reset_is_fido(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsFido", []))

    @jsii.member(jsii_name="resetIsTotp")
    def reset_is_totp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsTotp", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetParseTestId")
    def reset_parse_test_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseTestId", []))

    @jsii.member(jsii_name="resetParseTestOptions")
    def reset_parse_test_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParseTestOptions", []))

    @jsii.member(jsii_name="resetRestrictedRoles")
    def reset_restricted_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedRoles", []))

    @jsii.member(jsii_name="resetSecure")
    def reset_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecure", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> "SyntheticsGlobalVariableOptionsList":
        return typing.cast("SyntheticsGlobalVariableOptionsList", jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="parseTestOptions")
    def parse_test_options(self) -> "SyntheticsGlobalVariableParseTestOptionsList":
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsList", jsii.get(self, "parseTestOptions"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="isFidoInput")
    def is_fido_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isFidoInput"))

    @builtins.property
    @jsii.member(jsii_name="isTotpInput")
    def is_totp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isTotpInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptions"]]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="parseTestIdInput")
    def parse_test_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parseTestIdInput"))

    @builtins.property
    @jsii.member(jsii_name="parseTestOptionsInput")
    def parse_test_options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptions"]]], jsii.get(self, "parseTestOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedRolesInput")
    def restricted_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="secureInput")
    def secure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5788193d85c608e53229844e5d474d6e97671a3940f445d70fab418f64b97f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isFido")
    def is_fido(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isFido"))

    @is_fido.setter
    def is_fido(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f5f597c8c4655cc89fdc4a26c9e439fcc5a7e16a8d02e59d45fb3d0fdda719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isFido", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTotp")
    def is_totp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isTotp"))

    @is_totp.setter
    def is_totp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614980a0570e90f4d200e173a9e8366737673eaff6bd16fbb147650d0c94fdff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTotp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8db3cbcbc12a692c9b8cab94ba6b62216d49b6ba4890ea3dec5bfa6930e5215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parseTestId")
    def parse_test_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parseTestId"))

    @parse_test_id.setter
    def parse_test_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a18607594b6da1ebaefc8ea8de385f4b5316de535be739bb45a0bc0a2e4e92a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parseTestId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedRoles")
    def restricted_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedRoles"))

    @restricted_roles.setter
    def restricted_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e791098824659489ff80e0e78f970432bc4199c9faa83ce76ec52776c7a803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secure")
    def secure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secure"))

    @secure.setter
    def secure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a40ce9bc785d30740d27aab35e01f9767684fb47d64e4741a0dba881efbfa36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a521fa7e1d9afa8e6d7062b6f1f25b1380ff83e25d6cab06040e1aaf3dc10b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4ab1a6261c0a0805944bb08aa51411a235c7968e7a04fa2e3bffb62ad10ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "description": "description",
        "is_fido": "isFido",
        "is_totp": "isTotp",
        "options": "options",
        "parse_test_id": "parseTestId",
        "parse_test_options": "parseTestOptions",
        "restricted_roles": "restrictedRoles",
        "secure": "secure",
        "tags": "tags",
        "value": "value",
    },
)
class SyntheticsGlobalVariableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        is_fido: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_totp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parse_test_id: typing.Optional[builtins.str] = None,
        parse_test_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableParseTestOptions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Synthetics global variable name. Must be all uppercase with underscores. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        :param description: Description of the global variable. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        :param is_fido: If set to true, the global variable is a FIDO variable. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_fido SyntheticsGlobalVariable#is_fido}
        :param is_totp: If set to true, the global variable is a TOTP variable. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_totp SyntheticsGlobalVariable#is_totp}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#options SyntheticsGlobalVariable#options}
        :param parse_test_id: Id of the Synthetics test to use for a variable from test. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        :param parse_test_options: parse_test_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        :param restricted_roles: A list of role identifiers to associate with the Synthetics global variable. **Deprecated.** This field is no longer supported by the Datadog API. Please use ``datadog_restriction_policy`` instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        :param secure: If set to true, the value of the global variable is hidden. This setting is automatically set to ``true`` if ``is_totp`` or ``is_fido`` is set to ``true``. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        :param tags: A list of tags to associate with your synthetics global variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        :param value: The value of the global variable. Required unless ``is_fido`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfac2b6f5d731f178d31b130a243e4236cc921180c897ee746b90bd6be142b0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument is_fido", value=is_fido, expected_type=type_hints["is_fido"])
            check_type(argname="argument is_totp", value=is_totp, expected_type=type_hints["is_totp"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument parse_test_id", value=parse_test_id, expected_type=type_hints["parse_test_id"])
            check_type(argname="argument parse_test_options", value=parse_test_options, expected_type=type_hints["parse_test_options"])
            check_type(argname="argument restricted_roles", value=restricted_roles, expected_type=type_hints["restricted_roles"])
            check_type(argname="argument secure", value=secure, expected_type=type_hints["secure"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if description is not None:
            self._values["description"] = description
        if is_fido is not None:
            self._values["is_fido"] = is_fido
        if is_totp is not None:
            self._values["is_totp"] = is_totp
        if options is not None:
            self._values["options"] = options
        if parse_test_id is not None:
            self._values["parse_test_id"] = parse_test_id
        if parse_test_options is not None:
            self._values["parse_test_options"] = parse_test_options
        if restricted_roles is not None:
            self._values["restricted_roles"] = restricted_roles
        if secure is not None:
            self._values["secure"] = secure
        if tags is not None:
            self._values["tags"] = tags
        if value is not None:
            self._values["value"] = value

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
    def name(self) -> builtins.str:
        '''Synthetics global variable name. Must be all uppercase with underscores.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#name SyntheticsGlobalVariable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the global variable. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#description SyntheticsGlobalVariable#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_fido(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the global variable is a FIDO variable. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_fido SyntheticsGlobalVariable#is_fido}
        '''
        result = self._values.get("is_fido")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_totp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the global variable is a TOTP variable. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#is_totp SyntheticsGlobalVariable#is_totp}
        '''
        result = self._values.get("is_totp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptions"]]]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#options SyntheticsGlobalVariable#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptions"]]], result)

    @builtins.property
    def parse_test_id(self) -> typing.Optional[builtins.str]:
        '''Id of the Synthetics test to use for a variable from test.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_id SyntheticsGlobalVariable#parse_test_id}
        '''
        result = self._values.get("parse_test_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parse_test_options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptions"]]]:
        '''parse_test_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parse_test_options SyntheticsGlobalVariable#parse_test_options}
        '''
        result = self._values.get("parse_test_options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptions"]]], result)

    @builtins.property
    def restricted_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of role identifiers to associate with the Synthetics global variable.

        **Deprecated.** This field is no longer supported by the Datadog API. Please use ``datadog_restriction_policy`` instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#restricted_roles SyntheticsGlobalVariable#restricted_roles}
        '''
        result = self._values.get("restricted_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the value of the global variable is hidden.

        This setting is automatically set to ``true`` if ``is_totp`` or ``is_fido`` is set to ``true``. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#secure SyntheticsGlobalVariable#secure}
        '''
        result = self._values.get("secure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tags to associate with your synthetics global variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#tags SyntheticsGlobalVariable#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value of the global variable. Required unless ``is_fido`` is set to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptions",
    jsii_struct_bases=[],
    name_mapping={"totp_parameters": "totpParameters"},
)
class SyntheticsGlobalVariableOptions:
    def __init__(
        self,
        *,
        totp_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableOptionsTotpParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param totp_parameters: totp_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#totp_parameters SyntheticsGlobalVariable#totp_parameters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6755b31a7df04a8db65d6898f0ef5aa4b064fe9b1caa7502bba98f1d772ccd3e)
            check_type(argname="argument totp_parameters", value=totp_parameters, expected_type=type_hints["totp_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if totp_parameters is not None:
            self._values["totp_parameters"] = totp_parameters

    @builtins.property
    def totp_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptionsTotpParameters"]]]:
        '''totp_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#totp_parameters SyntheticsGlobalVariable#totp_parameters}
        '''
        result = self._values.get("totp_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptionsTotpParameters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c0dfe6e74f4aeeff7651f86adef34759eaa54aa0e6121f8e3905cc8621f63fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsGlobalVariableOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef66822311558b7e5d9119a1a005d01a50082e267ba2aef583ca6c6acd6dd582)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsGlobalVariableOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee483cfaada655070198cd57f0a640cec68fe422feea4843f9287900093151e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84483fa40a54991d0df4ca8c6872b7ab0de360d27a07c71ba2900be6ad2ff732)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e49ee9594bcc089a2f9763b42601aef410952d0e46dc151a021240a0a509109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd67fa533ffa89c538ad208b30e443b49b6fd1392ad79592301f584379ee3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SyntheticsGlobalVariableOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4236d9479c386e2eef332cceb0ee0f32b95ace0923a50a1e03c096bfb13e6795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTotpParameters")
    def put_totp_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableOptionsTotpParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a379b3b3d60e97b6f80d31483ce849efed46520e17a12b9324137f9d69d142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTotpParameters", [value]))

    @jsii.member(jsii_name="resetTotpParameters")
    def reset_totp_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTotpParameters", []))

    @builtins.property
    @jsii.member(jsii_name="totpParameters")
    def totp_parameters(self) -> "SyntheticsGlobalVariableOptionsTotpParametersList":
        return typing.cast("SyntheticsGlobalVariableOptionsTotpParametersList", jsii.get(self, "totpParameters"))

    @builtins.property
    @jsii.member(jsii_name="totpParametersInput")
    def totp_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptionsTotpParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableOptionsTotpParameters"]]], jsii.get(self, "totpParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f71b18b5be7f000796399098d479c23e6f9879c4e4e17bcab3db6d1288926a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptionsTotpParameters",
    jsii_struct_bases=[],
    name_mapping={"digits": "digits", "refresh_interval": "refreshInterval"},
)
class SyntheticsGlobalVariableOptionsTotpParameters:
    def __init__(self, *, digits: jsii.Number, refresh_interval: jsii.Number) -> None:
        '''
        :param digits: Number of digits for the OTP. Value must be between 4 and 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#digits SyntheticsGlobalVariable#digits}
        :param refresh_interval: Interval for which to refresh the token (in seconds). Value must be between 0 and 999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#refresh_interval SyntheticsGlobalVariable#refresh_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aac5605417c7af6025d3f2a58df590a0db1e967ab31fb237ef913c2a3cb09927)
            check_type(argname="argument digits", value=digits, expected_type=type_hints["digits"])
            check_type(argname="argument refresh_interval", value=refresh_interval, expected_type=type_hints["refresh_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "digits": digits,
            "refresh_interval": refresh_interval,
        }

    @builtins.property
    def digits(self) -> jsii.Number:
        '''Number of digits for the OTP. Value must be between 4 and 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#digits SyntheticsGlobalVariable#digits}
        '''
        result = self._values.get("digits")
        assert result is not None, "Required property 'digits' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def refresh_interval(self) -> jsii.Number:
        '''Interval for which to refresh the token (in seconds). Value must be between 0 and 999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#refresh_interval SyntheticsGlobalVariable#refresh_interval}
        '''
        result = self._values.get("refresh_interval")
        assert result is not None, "Required property 'refresh_interval' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableOptionsTotpParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableOptionsTotpParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptionsTotpParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81510ab7c1714650b0eaa2ed034fb68b209c46e8d9e27cb363d14a78c3ab3da8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsGlobalVariableOptionsTotpParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aecd864899876143b1a0f583c5a1eddd64fa683cc1d1d73eba99cc5a5ed6282)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsGlobalVariableOptionsTotpParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6cbc8604df22587101e51f85ead7328e4bdb3395c127ac0f350e4346e288a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bfcd02b10ccaa42299a6521d3af7e950996491c414cbdf708c07e2aec6a3ea0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad825bfce56abb53d13e1f319dd2c685b9d971736aa272c98ecf0295a94a3cff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptionsTotpParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptionsTotpParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptionsTotpParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f1f1edc149efaa7789aed0da79675c99928e5a214b12f0a63e5aeafd78858e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SyntheticsGlobalVariableOptionsTotpParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableOptionsTotpParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__873ad96bb4a7598cd3a2d1b3e8fa06e4e04dfaccd63b659bd6a39b115dffa9ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="digitsInput")
    def digits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "digitsInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshIntervalInput")
    def refresh_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "refreshIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="digits")
    def digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "digits"))

    @digits.setter
    def digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520ecd25740c3ef1595356d749f2956a3e24b13de3dfed454626354ed8b9e730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="refreshInterval")
    def refresh_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "refreshInterval"))

    @refresh_interval.setter
    def refresh_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9081145c5196383ae47758ee1e7c766bb7bcc557509c734cbb73c7e9e4ffabbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "refreshInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptionsTotpParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptionsTotpParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptionsTotpParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b73ada8e458695c8325856ac2da256d136b513d917a8dbb274abb01c9bce6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptions",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "field": "field",
        "local_variable_name": "localVariableName",
        "parser": "parser",
    },
)
class SyntheticsGlobalVariableParseTestOptions:
    def __init__(
        self,
        *,
        type: builtins.str,
        field: typing.Optional[builtins.str] = None,
        local_variable_name: typing.Optional[builtins.str] = None,
        parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableParseTestOptionsParser", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Defines the source to use to extract the value. Valid values are ``http_body``, ``http_header``, ``http_status_code``, ``local_variable``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param field: Required when type = ``http_header``. Defines the header to use to extract the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#field SyntheticsGlobalVariable#field}
        :param local_variable_name: When type is ``local_variable``, name of the local variable to use to extract the value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#local_variable_name SyntheticsGlobalVariable#local_variable_name}
        :param parser: parser block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parser SyntheticsGlobalVariable#parser}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c891479c2ff58d4c7ee95c32ffb1c6e8113a005dc333ae5da8f69c0969c47b60)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument local_variable_name", value=local_variable_name, expected_type=type_hints["local_variable_name"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if field is not None:
            self._values["field"] = field
        if local_variable_name is not None:
            self._values["local_variable_name"] = local_variable_name
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def type(self) -> builtins.str:
        '''Defines the source to use to extract the value. Valid values are ``http_body``, ``http_header``, ``http_status_code``, ``local_variable``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field(self) -> typing.Optional[builtins.str]:
        '''Required when type = ``http_header``. Defines the header to use to extract the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#field SyntheticsGlobalVariable#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_variable_name(self) -> typing.Optional[builtins.str]:
        '''When type is ``local_variable``, name of the local variable to use to extract the value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#local_variable_name SyntheticsGlobalVariable#local_variable_name}
        '''
        result = self._values.get("local_variable_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parser(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptionsParser"]]]:
        '''parser block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#parser SyntheticsGlobalVariable#parser}
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptionsParser"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableParseTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableParseTestOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96a03d4bf58d0712f0dae4e750765ecc7bc6ff63f4197272caeffd50a7debd23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsGlobalVariableParseTestOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce56fc36bf947b41798fc7731cf622e99f1475d8874b0a103731838ac6ae9c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a7620420c890b00273ca159e95bf3c6755143616b0ef8148f33863f37416df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6b3cd47bad9a832ef34dd24dd4308731345eb14eb4a551ee2e1290750a27424)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f90b346c86e5521b0cb78a722f3cb76958d4878bd11aa7c35dafa7c31422d494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6792a123e63ab9107af5e8cabb7ea27cb026333578cfa1c6d4e5b2d6c4b92b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SyntheticsGlobalVariableParseTestOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e304cd61031eb012f85dc389d715dab5646e5be0fc1b52a4098852c058b886)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParser")
    def put_parser(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsGlobalVariableParseTestOptionsParser", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7509564b444de120bad1ab9e491c0ded8fd8f199a81d8bae14a54a99ae8c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParser", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @jsii.member(jsii_name="resetLocalVariableName")
    def reset_local_variable_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalVariableName", []))

    @jsii.member(jsii_name="resetParser")
    def reset_parser(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParser", []))

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> "SyntheticsGlobalVariableParseTestOptionsParserList":
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsParserList", jsii.get(self, "parser"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="localVariableNameInput")
    def local_variable_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localVariableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="parserInput")
    def parser_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptionsParser"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsGlobalVariableParseTestOptionsParser"]]], jsii.get(self, "parserInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "field"))

    @field.setter
    def field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d37da09cc9857df35cd0946bfa45b5e4e12683e5923f19a5e692d91b73f0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "field", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localVariableName")
    def local_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localVariableName"))

    @local_variable_name.setter
    def local_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7109537e74bdfd501f10f03c1f502ce6c18942c3b3073d9b7c317a6d88e592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localVariableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fcb33507c22dda355b535155a97c5fa71182c7976751e5da076d1ecbebc2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e81295eb53b8224ba71ccf8ee6615a25d6b64568e6f3ff0acffe34023964c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsParser",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class SyntheticsGlobalVariableParseTestOptionsParser:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Type of parser to extract the value. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        :param value: Value for the parser to use, required for type ``json_path`` or ``regex``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b61d4325df063e55e3376869c11f80e380138b0acca80b527a4305e8f7d8ecc)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of parser to extract the value. Valid values are ``raw``, ``json_path``, ``regex``, ``x_path``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#type SyntheticsGlobalVariable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value for the parser to use, required for type ``json_path`` or ``regex``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/synthetics_global_variable#value SyntheticsGlobalVariable#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsGlobalVariableParseTestOptionsParser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsGlobalVariableParseTestOptionsParserList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsParserList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c84409cec6bb02da7cbe6fdfe6af6670e5a2a3752a4b25052209adb9c4c299f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsGlobalVariableParseTestOptionsParserOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d52044e89d185a6825e2ad7969d2a123d9d77eb35ee59cb3d4ffff9a9b3570b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsGlobalVariableParseTestOptionsParserOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62bd68fa1427f717ae3c88ed1eef8abe9b8b1ab769a811ad47e3a7bf1f017dfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3445231022735cea907aad44fe743ce4dfc12df766fb390eca66d0749e0cf489)
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
            type_hints = typing.get_type_hints(_typecheckingstub__642b452f0b2a7fa663a96f48a9f5bde60d9542f66ffda5502c277a453f9b24ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptionsParser]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptionsParser]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptionsParser]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352339859ad04c809d5ef34eead4c2ccb816e852629d0cabb9c202dfa37c371a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SyntheticsGlobalVariableParseTestOptionsParserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.syntheticsGlobalVariable.SyntheticsGlobalVariableParseTestOptionsParserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96bcd2e362738eefe8344df96f9a9200c207516349d2dc84181f2a9e5eecf12d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a15579b79d6b9770670b36ff07ab0a7ce1b18e90c84eff2600a99f86213997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fdb27bdaf55f5734fb702d771a6426f0f5a5424d46bd6ae956b59a956e59f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptionsParser]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptionsParser]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptionsParser]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5003b27fa89627b796fe64d0eae72b4cf2af2013b8fcf4accede4a4ba31ac55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SyntheticsGlobalVariable",
    "SyntheticsGlobalVariableConfig",
    "SyntheticsGlobalVariableOptions",
    "SyntheticsGlobalVariableOptionsList",
    "SyntheticsGlobalVariableOptionsOutputReference",
    "SyntheticsGlobalVariableOptionsTotpParameters",
    "SyntheticsGlobalVariableOptionsTotpParametersList",
    "SyntheticsGlobalVariableOptionsTotpParametersOutputReference",
    "SyntheticsGlobalVariableParseTestOptions",
    "SyntheticsGlobalVariableParseTestOptionsList",
    "SyntheticsGlobalVariableParseTestOptionsOutputReference",
    "SyntheticsGlobalVariableParseTestOptionsParser",
    "SyntheticsGlobalVariableParseTestOptionsParserList",
    "SyntheticsGlobalVariableParseTestOptionsParserOutputReference",
]

publication.publish()

def _typecheckingstub__8130ffd11a0e21ba65645d2942d6d24827dd309902720b48e6aa8bb09898234a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    is_fido: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_totp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_test_id: typing.Optional[builtins.str] = None,
    parse_test_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableParseTestOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__36187fd5360e5ed4828e5ce73bbe0a81b0ac61df3e000fd6091b01322daf64ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9309d5506c1c99c479fc71c47525566a2845a98125d812bcb97489c0fd0e46(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2642918805c9f24132f34236a3d3ba4cf8e6a62e8abe9c8bbab0f6c3d81b52(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableParseTestOptions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5788193d85c608e53229844e5d474d6e97671a3940f445d70fab418f64b97f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f5f597c8c4655cc89fdc4a26c9e439fcc5a7e16a8d02e59d45fb3d0fdda719(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614980a0570e90f4d200e173a9e8366737673eaff6bd16fbb147650d0c94fdff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8db3cbcbc12a692c9b8cab94ba6b62216d49b6ba4890ea3dec5bfa6930e5215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a18607594b6da1ebaefc8ea8de385f4b5316de535be739bb45a0bc0a2e4e92a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e791098824659489ff80e0e78f970432bc4199c9faa83ce76ec52776c7a803(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a40ce9bc785d30740d27aab35e01f9767684fb47d64e4741a0dba881efbfa36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a521fa7e1d9afa8e6d7062b6f1f25b1380ff83e25d6cab06040e1aaf3dc10b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4ab1a6261c0a0805944bb08aa51411a235c7968e7a04fa2e3bffb62ad10ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfac2b6f5d731f178d31b130a243e4236cc921180c897ee746b90bd6be142b0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    is_fido: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_totp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parse_test_id: typing.Optional[builtins.str] = None,
    parse_test_options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableParseTestOptions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    restricted_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6755b31a7df04a8db65d6898f0ef5aa4b064fe9b1caa7502bba98f1d772ccd3e(
    *,
    totp_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableOptionsTotpParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0dfe6e74f4aeeff7651f86adef34759eaa54aa0e6121f8e3905cc8621f63fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef66822311558b7e5d9119a1a005d01a50082e267ba2aef583ca6c6acd6dd582(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee483cfaada655070198cd57f0a640cec68fe422feea4843f9287900093151e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84483fa40a54991d0df4ca8c6872b7ab0de360d27a07c71ba2900be6ad2ff732(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e49ee9594bcc089a2f9763b42601aef410952d0e46dc151a021240a0a509109(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd67fa533ffa89c538ad208b30e443b49b6fd1392ad79592301f584379ee3b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4236d9479c386e2eef332cceb0ee0f32b95ace0923a50a1e03c096bfb13e6795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a379b3b3d60e97b6f80d31483ce849efed46520e17a12b9324137f9d69d142(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableOptionsTotpParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f71b18b5be7f000796399098d479c23e6f9879c4e4e17bcab3db6d1288926a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac5605417c7af6025d3f2a58df590a0db1e967ab31fb237ef913c2a3cb09927(
    *,
    digits: jsii.Number,
    refresh_interval: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81510ab7c1714650b0eaa2ed034fb68b209c46e8d9e27cb363d14a78c3ab3da8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aecd864899876143b1a0f583c5a1eddd64fa683cc1d1d73eba99cc5a5ed6282(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6cbc8604df22587101e51f85ead7328e4bdb3395c127ac0f350e4346e288a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfcd02b10ccaa42299a6521d3af7e950996491c414cbdf708c07e2aec6a3ea0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad825bfce56abb53d13e1f319dd2c685b9d971736aa272c98ecf0295a94a3cff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f1f1edc149efaa7789aed0da79675c99928e5a214b12f0a63e5aeafd78858e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableOptionsTotpParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873ad96bb4a7598cd3a2d1b3e8fa06e4e04dfaccd63b659bd6a39b115dffa9ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520ecd25740c3ef1595356d749f2956a3e24b13de3dfed454626354ed8b9e730(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9081145c5196383ae47758ee1e7c766bb7bcc557509c734cbb73c7e9e4ffabbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b73ada8e458695c8325856ac2da256d136b513d917a8dbb274abb01c9bce6e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableOptionsTotpParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c891479c2ff58d4c7ee95c32ffb1c6e8113a005dc333ae5da8f69c0969c47b60(
    *,
    type: builtins.str,
    field: typing.Optional[builtins.str] = None,
    local_variable_name: typing.Optional[builtins.str] = None,
    parser: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableParseTestOptionsParser, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a03d4bf58d0712f0dae4e750765ecc7bc6ff63f4197272caeffd50a7debd23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce56fc36bf947b41798fc7731cf622e99f1475d8874b0a103731838ac6ae9c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a7620420c890b00273ca159e95bf3c6755143616b0ef8148f33863f37416df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b3cd47bad9a832ef34dd24dd4308731345eb14eb4a551ee2e1290750a27424(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90b346c86e5521b0cb78a722f3cb76958d4878bd11aa7c35dafa7c31422d494(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6792a123e63ab9107af5e8cabb7ea27cb026333578cfa1c6d4e5b2d6c4b92b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e304cd61031eb012f85dc389d715dab5646e5be0fc1b52a4098852c058b886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7509564b444de120bad1ab9e491c0ded8fd8f199a81d8bae14a54a99ae8c9e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsGlobalVariableParseTestOptionsParser, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d37da09cc9857df35cd0946bfa45b5e4e12683e5923f19a5e692d91b73f0c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7109537e74bdfd501f10f03c1f502ce6c18942c3b3073d9b7c317a6d88e592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fcb33507c22dda355b535155a97c5fa71182c7976751e5da076d1ecbebc2c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e81295eb53b8224ba71ccf8ee6615a25d6b64568e6f3ff0acffe34023964c88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b61d4325df063e55e3376869c11f80e380138b0acca80b527a4305e8f7d8ecc(
    *,
    type: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84409cec6bb02da7cbe6fdfe6af6670e5a2a3752a4b25052209adb9c4c299f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d52044e89d185a6825e2ad7969d2a123d9d77eb35ee59cb3d4ffff9a9b3570b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62bd68fa1427f717ae3c88ed1eef8abe9b8b1ab769a811ad47e3a7bf1f017dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3445231022735cea907aad44fe743ce4dfc12df766fb390eca66d0749e0cf489(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642b452f0b2a7fa663a96f48a9f5bde60d9542f66ffda5502c277a453f9b24ca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352339859ad04c809d5ef34eead4c2ccb816e852629d0cabb9c202dfa37c371a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsGlobalVariableParseTestOptionsParser]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bcd2e362738eefe8344df96f9a9200c207516349d2dc84181f2a9e5eecf12d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a15579b79d6b9770670b36ff07ab0a7ce1b18e90c84eff2600a99f86213997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fdb27bdaf55f5734fb702d771a6426f0f5a5424d46bd6ae956b59a956e59f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5003b27fa89627b796fe64d0eae72b4cf2af2013b8fcf4accede4a4ba31ac55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SyntheticsGlobalVariableParseTestOptionsParser]],
) -> None:
    """Type checking stubs"""
    pass

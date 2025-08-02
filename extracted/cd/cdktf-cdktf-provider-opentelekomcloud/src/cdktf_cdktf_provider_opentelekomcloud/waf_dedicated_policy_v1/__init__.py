r'''
# `opentelekomcloud_waf_dedicated_policy_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_policy_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1).
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


class WafDedicatedPolicyV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1 opentelekomcloud_waf_dedicated_policy_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        deep_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        level: typing.Optional[jsii.Number] = None,
        options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPolicyV1Options", typing.Dict[builtins.str, typing.Any]]]]] = None,
        protection_mode: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shiro_decryption_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1 opentelekomcloud_waf_dedicated_policy_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#name WafDedicatedPolicyV1#name}.
        :param deep_inspection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#deep_inspection WafDedicatedPolicyV1#deep_inspection}.
        :param full_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#full_detection WafDedicatedPolicyV1#full_detection}.
        :param header_inspection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#header_inspection WafDedicatedPolicyV1#header_inspection}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#id WafDedicatedPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#level WafDedicatedPolicyV1#level}.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#options WafDedicatedPolicyV1#options}
        :param protection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#protection_mode WafDedicatedPolicyV1#protection_mode}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#region WafDedicatedPolicyV1#region}.
        :param shiro_decryption_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#shiro_decryption_check WafDedicatedPolicyV1#shiro_decryption_check}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#timeouts WafDedicatedPolicyV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825a529ff47748e78ea405886efb1fd15d83d0066ea4b232b0409a30f064cbd7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedPolicyV1Config(
            name=name,
            deep_inspection=deep_inspection,
            full_detection=full_detection,
            header_inspection=header_inspection,
            id=id,
            level=level,
            options=options,
            protection_mode=protection_mode,
            region=region,
            shiro_decryption_check=shiro_decryption_check,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a WafDedicatedPolicyV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedPolicyV1 to import.
        :param import_from_id: The id of the existing WafDedicatedPolicyV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedPolicyV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284005803ffb6db4c5ed29fbdabe7aaad8c111beaf1404ae4b34e76be043035a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPolicyV1Options", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98709ec8f87b41d2af23d7eeda9b83ddedc7d59a215366625df5b00fdfb2de83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#create WafDedicatedPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#delete WafDedicatedPolicyV1#delete}.
        '''
        value = WafDedicatedPolicyV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeepInspection")
    def reset_deep_inspection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeepInspection", []))

    @jsii.member(jsii_name="resetFullDetection")
    def reset_full_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullDetection", []))

    @jsii.member(jsii_name="resetHeaderInspection")
    def reset_header_inspection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaderInspection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetProtectionMode")
    def reset_protection_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectionMode", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetShiroDecryptionCheck")
    def reset_shiro_decryption_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShiroDecryptionCheck", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> "WafDedicatedPolicyV1OptionsList":
        return typing.cast("WafDedicatedPolicyV1OptionsList", jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDedicatedPolicyV1TimeoutsOutputReference":
        return typing.cast("WafDedicatedPolicyV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deepInspectionInput")
    def deep_inspection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deepInspectionInput"))

    @builtins.property
    @jsii.member(jsii_name="fullDetectionInput")
    def full_detection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fullDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInspectionInput")
    def header_inspection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "headerInspectionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPolicyV1Options"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPolicyV1Options"]]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="protectionModeInput")
    def protection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="shiroDecryptionCheckInput")
    def shiro_decryption_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "shiroDecryptionCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedPolicyV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedPolicyV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deepInspection")
    def deep_inspection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deepInspection"))

    @deep_inspection.setter
    def deep_inspection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59661a1370ed9f27238d49b04cf639d42602360bd14c56cfacaf00ac187d5714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deepInspection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullDetection")
    def full_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fullDetection"))

    @full_detection.setter
    def full_detection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5f2c68b5bd03c6e8adbba718fb1e1acf7bcbd5ac34ef9a0b6580335b04d161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headerInspection")
    def header_inspection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "headerInspection"))

    @header_inspection.setter
    def header_inspection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f66a363f8ab8535b1e947bdff975b9ece10ff2ae49377e1ac73664fa2312d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headerInspection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfe415b674bd7c00ace4e81f016ada6c52f729679c55a1474a59cf9f03782b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "level"))

    @level.setter
    def level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a7bdf4ae4d2d1fac26233b912009d2a03f3ac40bc7e6834bccfe7d7cc6e59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fdca141db73b6c1a10914fec9f4cbae6ac1f0b596bbd1270ecbec2f4c82b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protectionMode")
    def protection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protectionMode"))

    @protection_mode.setter
    def protection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9964ed0140a8c8f2a3b482e501b16d0564874abaf2eb51e0eaab5a56983508f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cfc4ead3efb650d5ef5ef2785e55fd217dc453206d75bb00bbccef8c5cbbdad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shiroDecryptionCheck")
    def shiro_decryption_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "shiroDecryptionCheck"))

    @shiro_decryption_check.setter
    def shiro_decryption_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8da09237f219ddb971070ea341bf08ed37efd5e20ad16fe53baa89ef7907615c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shiroDecryptionCheck", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1Config",
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
        "deep_inspection": "deepInspection",
        "full_detection": "fullDetection",
        "header_inspection": "headerInspection",
        "id": "id",
        "level": "level",
        "options": "options",
        "protection_mode": "protectionMode",
        "region": "region",
        "shiro_decryption_check": "shiroDecryptionCheck",
        "timeouts": "timeouts",
    },
)
class WafDedicatedPolicyV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        deep_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        level: typing.Optional[jsii.Number] = None,
        options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPolicyV1Options", typing.Dict[builtins.str, typing.Any]]]]] = None,
        protection_mode: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        shiro_decryption_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedPolicyV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#name WafDedicatedPolicyV1#name}.
        :param deep_inspection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#deep_inspection WafDedicatedPolicyV1#deep_inspection}.
        :param full_detection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#full_detection WafDedicatedPolicyV1#full_detection}.
        :param header_inspection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#header_inspection WafDedicatedPolicyV1#header_inspection}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#id WafDedicatedPolicyV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#level WafDedicatedPolicyV1#level}.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#options WafDedicatedPolicyV1#options}
        :param protection_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#protection_mode WafDedicatedPolicyV1#protection_mode}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#region WafDedicatedPolicyV1#region}.
        :param shiro_decryption_check: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#shiro_decryption_check WafDedicatedPolicyV1#shiro_decryption_check}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#timeouts WafDedicatedPolicyV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafDedicatedPolicyV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b345ec378068c74113b5cd46447fe1037735cfd7a474f5ad62024087af63e2b5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument deep_inspection", value=deep_inspection, expected_type=type_hints["deep_inspection"])
            check_type(argname="argument full_detection", value=full_detection, expected_type=type_hints["full_detection"])
            check_type(argname="argument header_inspection", value=header_inspection, expected_type=type_hints["header_inspection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument protection_mode", value=protection_mode, expected_type=type_hints["protection_mode"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument shiro_decryption_check", value=shiro_decryption_check, expected_type=type_hints["shiro_decryption_check"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if deep_inspection is not None:
            self._values["deep_inspection"] = deep_inspection
        if full_detection is not None:
            self._values["full_detection"] = full_detection
        if header_inspection is not None:
            self._values["header_inspection"] = header_inspection
        if id is not None:
            self._values["id"] = id
        if level is not None:
            self._values["level"] = level
        if options is not None:
            self._values["options"] = options
        if protection_mode is not None:
            self._values["protection_mode"] = protection_mode
        if region is not None:
            self._values["region"] = region
        if shiro_decryption_check is not None:
            self._values["shiro_decryption_check"] = shiro_decryption_check
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#name WafDedicatedPolicyV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deep_inspection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#deep_inspection WafDedicatedPolicyV1#deep_inspection}.'''
        result = self._values.get("deep_inspection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def full_detection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#full_detection WafDedicatedPolicyV1#full_detection}.'''
        result = self._values.get("full_detection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header_inspection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#header_inspection WafDedicatedPolicyV1#header_inspection}.'''
        result = self._values.get("header_inspection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#id WafDedicatedPolicyV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#level WafDedicatedPolicyV1#level}.'''
        result = self._values.get("level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPolicyV1Options"]]]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#options WafDedicatedPolicyV1#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPolicyV1Options"]]], result)

    @builtins.property
    def protection_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#protection_mode WafDedicatedPolicyV1#protection_mode}.'''
        result = self._values.get("protection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#region WafDedicatedPolicyV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shiro_decryption_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#shiro_decryption_check WafDedicatedPolicyV1#shiro_decryption_check}.'''
        result = self._values.get("shiro_decryption_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDedicatedPolicyV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#timeouts WafDedicatedPolicyV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDedicatedPolicyV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPolicyV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1Options",
    jsii_struct_bases=[],
    name_mapping={
        "anti_crawler": "antiCrawler",
        "anti_leakage": "antiLeakage",
        "anti_tamper": "antiTamper",
        "blacklist": "blacklist",
        "cc": "cc",
        "common": "common",
        "crawler": "crawler",
        "crawler_engine": "crawlerEngine",
        "crawler_other": "crawlerOther",
        "crawler_scanner": "crawlerScanner",
        "crawler_script": "crawlerScript",
        "custom": "custom",
        "followed_action": "followedAction",
        "geolocation_access_control": "geolocationAccessControl",
        "ignore": "ignore",
        "privacy": "privacy",
        "web_attack": "webAttack",
        "web_shell": "webShell",
    },
)
class WafDedicatedPolicyV1Options:
    def __init__(
        self,
        *,
        anti_crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anti_leakage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anti_tamper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        blacklist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        common: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_other: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_scanner: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crawler_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        followed_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geolocation_access_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ignore: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_attack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_shell: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param anti_crawler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_crawler WafDedicatedPolicyV1#anti_crawler}.
        :param anti_leakage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_leakage WafDedicatedPolicyV1#anti_leakage}.
        :param anti_tamper: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_tamper WafDedicatedPolicyV1#anti_tamper}.
        :param blacklist: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#blacklist WafDedicatedPolicyV1#blacklist}.
        :param cc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#cc WafDedicatedPolicyV1#cc}.
        :param common: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#common WafDedicatedPolicyV1#common}.
        :param crawler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler WafDedicatedPolicyV1#crawler}.
        :param crawler_engine: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_engine WafDedicatedPolicyV1#crawler_engine}.
        :param crawler_other: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_other WafDedicatedPolicyV1#crawler_other}.
        :param crawler_scanner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_scanner WafDedicatedPolicyV1#crawler_scanner}.
        :param crawler_script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_script WafDedicatedPolicyV1#crawler_script}.
        :param custom: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#custom WafDedicatedPolicyV1#custom}.
        :param followed_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#followed_action WafDedicatedPolicyV1#followed_action}.
        :param geolocation_access_control: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#geolocation_access_control WafDedicatedPolicyV1#geolocation_access_control}.
        :param ignore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#ignore WafDedicatedPolicyV1#ignore}.
        :param privacy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#privacy WafDedicatedPolicyV1#privacy}.
        :param web_attack: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#web_attack WafDedicatedPolicyV1#web_attack}.
        :param web_shell: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#web_shell WafDedicatedPolicyV1#web_shell}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd7f8f876eac254ae5b7aceb056343777e7eb9fce2bbb9dddf0555b465c2058)
            check_type(argname="argument anti_crawler", value=anti_crawler, expected_type=type_hints["anti_crawler"])
            check_type(argname="argument anti_leakage", value=anti_leakage, expected_type=type_hints["anti_leakage"])
            check_type(argname="argument anti_tamper", value=anti_tamper, expected_type=type_hints["anti_tamper"])
            check_type(argname="argument blacklist", value=blacklist, expected_type=type_hints["blacklist"])
            check_type(argname="argument cc", value=cc, expected_type=type_hints["cc"])
            check_type(argname="argument common", value=common, expected_type=type_hints["common"])
            check_type(argname="argument crawler", value=crawler, expected_type=type_hints["crawler"])
            check_type(argname="argument crawler_engine", value=crawler_engine, expected_type=type_hints["crawler_engine"])
            check_type(argname="argument crawler_other", value=crawler_other, expected_type=type_hints["crawler_other"])
            check_type(argname="argument crawler_scanner", value=crawler_scanner, expected_type=type_hints["crawler_scanner"])
            check_type(argname="argument crawler_script", value=crawler_script, expected_type=type_hints["crawler_script"])
            check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
            check_type(argname="argument followed_action", value=followed_action, expected_type=type_hints["followed_action"])
            check_type(argname="argument geolocation_access_control", value=geolocation_access_control, expected_type=type_hints["geolocation_access_control"])
            check_type(argname="argument ignore", value=ignore, expected_type=type_hints["ignore"])
            check_type(argname="argument privacy", value=privacy, expected_type=type_hints["privacy"])
            check_type(argname="argument web_attack", value=web_attack, expected_type=type_hints["web_attack"])
            check_type(argname="argument web_shell", value=web_shell, expected_type=type_hints["web_shell"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if anti_crawler is not None:
            self._values["anti_crawler"] = anti_crawler
        if anti_leakage is not None:
            self._values["anti_leakage"] = anti_leakage
        if anti_tamper is not None:
            self._values["anti_tamper"] = anti_tamper
        if blacklist is not None:
            self._values["blacklist"] = blacklist
        if cc is not None:
            self._values["cc"] = cc
        if common is not None:
            self._values["common"] = common
        if crawler is not None:
            self._values["crawler"] = crawler
        if crawler_engine is not None:
            self._values["crawler_engine"] = crawler_engine
        if crawler_other is not None:
            self._values["crawler_other"] = crawler_other
        if crawler_scanner is not None:
            self._values["crawler_scanner"] = crawler_scanner
        if crawler_script is not None:
            self._values["crawler_script"] = crawler_script
        if custom is not None:
            self._values["custom"] = custom
        if followed_action is not None:
            self._values["followed_action"] = followed_action
        if geolocation_access_control is not None:
            self._values["geolocation_access_control"] = geolocation_access_control
        if ignore is not None:
            self._values["ignore"] = ignore
        if privacy is not None:
            self._values["privacy"] = privacy
        if web_attack is not None:
            self._values["web_attack"] = web_attack
        if web_shell is not None:
            self._values["web_shell"] = web_shell

    @builtins.property
    def anti_crawler(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_crawler WafDedicatedPolicyV1#anti_crawler}.'''
        result = self._values.get("anti_crawler")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def anti_leakage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_leakage WafDedicatedPolicyV1#anti_leakage}.'''
        result = self._values.get("anti_leakage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def anti_tamper(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#anti_tamper WafDedicatedPolicyV1#anti_tamper}.'''
        result = self._values.get("anti_tamper")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def blacklist(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#blacklist WafDedicatedPolicyV1#blacklist}.'''
        result = self._values.get("blacklist")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#cc WafDedicatedPolicyV1#cc}.'''
        result = self._values.get("cc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def common(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#common WafDedicatedPolicyV1#common}.'''
        result = self._values.get("common")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler WafDedicatedPolicyV1#crawler}.'''
        result = self._values.get("crawler")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_engine(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_engine WafDedicatedPolicyV1#crawler_engine}.'''
        result = self._values.get("crawler_engine")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_other(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_other WafDedicatedPolicyV1#crawler_other}.'''
        result = self._values.get("crawler_other")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_scanner(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_scanner WafDedicatedPolicyV1#crawler_scanner}.'''
        result = self._values.get("crawler_scanner")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crawler_script(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#crawler_script WafDedicatedPolicyV1#crawler_script}.'''
        result = self._values.get("crawler_script")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#custom WafDedicatedPolicyV1#custom}.'''
        result = self._values.get("custom")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def followed_action(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#followed_action WafDedicatedPolicyV1#followed_action}.'''
        result = self._values.get("followed_action")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def geolocation_access_control(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#geolocation_access_control WafDedicatedPolicyV1#geolocation_access_control}.'''
        result = self._values.get("geolocation_access_control")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ignore(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#ignore WafDedicatedPolicyV1#ignore}.'''
        result = self._values.get("ignore")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def privacy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#privacy WafDedicatedPolicyV1#privacy}.'''
        result = self._values.get("privacy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def web_attack(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#web_attack WafDedicatedPolicyV1#web_attack}.'''
        result = self._values.get("web_attack")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def web_shell(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#web_shell WafDedicatedPolicyV1#web_shell}.'''
        result = self._values.get("web_shell")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPolicyV1Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedPolicyV1OptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1OptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d7c4f2a1201018fbff27260564ab1b0311951e50dfddb2344c73997bcfeadb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WafDedicatedPolicyV1OptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a047dd0b63699d5c21bab6ac48cc5ce6082207792cb63e846066762e5cc714a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedPolicyV1OptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c980b3a784941c3d811d4ac9b5530b78e8471e9d5ac4eebd750708edfe5d49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__876fec1c21bceef542ca95e6c2f6b1a24d9dd4493468160577b768251cb9f524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83798f3538f2af337c6d9f1f93f8040127dbb951c0416e7f4f667e0ca414217a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPolicyV1Options]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPolicyV1Options]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPolicyV1Options]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecde3dad294ced76e4acbb1e1f279e5a4ed2ac7ae5433fa2638cde3b87a7ad6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedPolicyV1OptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1OptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87dc3239cd1cc9ac97680fbe70d3c826b4f169f2511d8299c97d4ec7e0a80743)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAntiCrawler")
    def reset_anti_crawler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntiCrawler", []))

    @jsii.member(jsii_name="resetAntiLeakage")
    def reset_anti_leakage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntiLeakage", []))

    @jsii.member(jsii_name="resetAntiTamper")
    def reset_anti_tamper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAntiTamper", []))

    @jsii.member(jsii_name="resetBlacklist")
    def reset_blacklist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlacklist", []))

    @jsii.member(jsii_name="resetCc")
    def reset_cc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCc", []))

    @jsii.member(jsii_name="resetCommon")
    def reset_common(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommon", []))

    @jsii.member(jsii_name="resetCrawler")
    def reset_crawler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawler", []))

    @jsii.member(jsii_name="resetCrawlerEngine")
    def reset_crawler_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerEngine", []))

    @jsii.member(jsii_name="resetCrawlerOther")
    def reset_crawler_other(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerOther", []))

    @jsii.member(jsii_name="resetCrawlerScanner")
    def reset_crawler_scanner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerScanner", []))

    @jsii.member(jsii_name="resetCrawlerScript")
    def reset_crawler_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerScript", []))

    @jsii.member(jsii_name="resetCustom")
    def reset_custom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustom", []))

    @jsii.member(jsii_name="resetFollowedAction")
    def reset_followed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowedAction", []))

    @jsii.member(jsii_name="resetGeolocationAccessControl")
    def reset_geolocation_access_control(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeolocationAccessControl", []))

    @jsii.member(jsii_name="resetIgnore")
    def reset_ignore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnore", []))

    @jsii.member(jsii_name="resetPrivacy")
    def reset_privacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivacy", []))

    @jsii.member(jsii_name="resetWebAttack")
    def reset_web_attack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebAttack", []))

    @jsii.member(jsii_name="resetWebShell")
    def reset_web_shell(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebShell", []))

    @builtins.property
    @jsii.member(jsii_name="botEnable")
    def bot_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "botEnable"))

    @builtins.property
    @jsii.member(jsii_name="precise")
    def precise(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "precise"))

    @builtins.property
    @jsii.member(jsii_name="antiCrawlerInput")
    def anti_crawler_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "antiCrawlerInput"))

    @builtins.property
    @jsii.member(jsii_name="antiLeakageInput")
    def anti_leakage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "antiLeakageInput"))

    @builtins.property
    @jsii.member(jsii_name="antiTamperInput")
    def anti_tamper_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "antiTamperInput"))

    @builtins.property
    @jsii.member(jsii_name="blacklistInput")
    def blacklist_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blacklistInput"))

    @builtins.property
    @jsii.member(jsii_name="ccInput")
    def cc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ccInput"))

    @builtins.property
    @jsii.member(jsii_name="commonInput")
    def common_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "commonInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerEngineInput")
    def crawler_engine_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerInput")
    def crawler_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerOtherInput")
    def crawler_other_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerOtherInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerScannerInput")
    def crawler_scanner_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerScannerInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerScriptInput")
    def crawler_script_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crawlerScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="customInput")
    def custom_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "customInput"))

    @builtins.property
    @jsii.member(jsii_name="followedActionInput")
    def followed_action_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "followedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="geolocationAccessControlInput")
    def geolocation_access_control_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "geolocationAccessControlInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreInput")
    def ignore_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreInput"))

    @builtins.property
    @jsii.member(jsii_name="privacyInput")
    def privacy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privacyInput"))

    @builtins.property
    @jsii.member(jsii_name="webAttackInput")
    def web_attack_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webAttackInput"))

    @builtins.property
    @jsii.member(jsii_name="webShellInput")
    def web_shell_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webShellInput"))

    @builtins.property
    @jsii.member(jsii_name="antiCrawler")
    def anti_crawler(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "antiCrawler"))

    @anti_crawler.setter
    def anti_crawler(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35c695f46df157e3c49af88ce0f89b21983dbe4fb0543cbf5edfada967e5ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "antiCrawler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="antiLeakage")
    def anti_leakage(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "antiLeakage"))

    @anti_leakage.setter
    def anti_leakage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1501fd491a70d6097061a148fcacdcea8f1608459873748883b62ce08112963c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "antiLeakage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="antiTamper")
    def anti_tamper(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "antiTamper"))

    @anti_tamper.setter
    def anti_tamper(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e48d34a480397fb72b4cfd278ed26b53df07de3e95f2447bfa2259c62ef8bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "antiTamper", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="blacklist")
    def blacklist(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blacklist"))

    @blacklist.setter
    def blacklist(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5ee5d8fa8441652318c12fac0c9076121222206fd0af165c7b6a6be15ff79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blacklist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cc")
    def cc(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cc"))

    @cc.setter
    def cc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddffeaef1d6f631f1f8d2c7e7475da772073946cb9f9f8a90ab42f8d6e6de18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="common")
    def common(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "common"))

    @common.setter
    def common(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9d63d3fffd1b1bed905389568c36360b62e151936346fc93f4aa5e70f06f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "common", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawler"))

    @crawler.setter
    def crawler(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3e63d31cc1b9fbb1ccefdaa615c7d11bddf2dade8fdf53e992ffd66638771d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerEngine")
    def crawler_engine(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerEngine"))

    @crawler_engine.setter
    def crawler_engine(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca26c639588f521e42099460fc59a547043d1dd206cb32ca609622e95d45942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerEngine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerOther")
    def crawler_other(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerOther"))

    @crawler_other.setter
    def crawler_other(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd294e4eb896dee0e0a89c8036c41c152421106668fcdb30967c6e9f4c7303af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerOther", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerScanner")
    def crawler_scanner(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerScanner"))

    @crawler_scanner.setter
    def crawler_scanner(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69423c5bc6354e456d4d234006d1aa43a65feed01b336160895587248f57d924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerScanner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crawlerScript")
    def crawler_script(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crawlerScript"))

    @crawler_script.setter
    def crawler_script(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777e70f402df7955ebf36f7385986d0755d423875cf10dc848240aa6067e7bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="custom")
    def custom(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "custom"))

    @custom.setter
    def custom(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ef1083783b85cecfb868e58154f42f2874459edaf339b23f0e83ddf01f0929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "custom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="followedAction")
    def followed_action(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "followedAction"))

    @followed_action.setter
    def followed_action(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53fd8a38f0a21718c6a8ef96182111b96953ae7b2922f93e28670f3ce2e093a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geolocationAccessControl")
    def geolocation_access_control(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "geolocationAccessControl"))

    @geolocation_access_control.setter
    def geolocation_access_control(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b7a113ae11c201045ec660b50125c35ddeee740aab6597fd7d2986621a34b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geolocationAccessControl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignore")
    def ignore(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignore"))

    @ignore.setter
    def ignore(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad235139b009d78ae38c61f93b2df2e3d3ad3c6838b6c3f409fd68bda424eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privacy")
    def privacy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privacy"))

    @privacy.setter
    def privacy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e224aa3c03d4a457840bae81c3889ec96c6448ef501863e430e775e5d7d28b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privacy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webAttack")
    def web_attack(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webAttack"))

    @web_attack.setter
    def web_attack(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ce40e755ba058cca34036045931169d0031f22478fe00b36d062631f43fe65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webAttack", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webShell")
    def web_shell(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webShell"))

    @web_shell.setter
    def web_shell(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48268ee57402bab5dd14f2ab578d4707853c10b13d1308c3d62512990ff3c354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webShell", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Options]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Options]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Options]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1b0196bcc08d956450604c210ef38e60335ce7831a876fc22657e5884facc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDedicatedPolicyV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#create WafDedicatedPolicyV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#delete WafDedicatedPolicyV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e63648aee18abf033a956824a8087472bfb745701e141f0c7122185ee107c1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#create WafDedicatedPolicyV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_policy_v1#delete WafDedicatedPolicyV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPolicyV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedPolicyV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPolicyV1.WafDedicatedPolicyV1TimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a86ec1760127d676f3d3e1d79b7b131ba8ec4c521aaf3e557a25d2bf8bfafbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d4ca32f147f6e91d334f3a75454e83b050f103f13c68e93480f925832a5ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f793e9f47b6c88f720335783de744b51191d75d94cce2e6f5b23a10b60c784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717c07b814bdebb2b139341f9ccbc62d3c53781c37f1b80d59eb7bec0d15b2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedPolicyV1",
    "WafDedicatedPolicyV1Config",
    "WafDedicatedPolicyV1Options",
    "WafDedicatedPolicyV1OptionsList",
    "WafDedicatedPolicyV1OptionsOutputReference",
    "WafDedicatedPolicyV1Timeouts",
    "WafDedicatedPolicyV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__825a529ff47748e78ea405886efb1fd15d83d0066ea4b232b0409a30f064cbd7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    deep_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[jsii.Number] = None,
    options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPolicyV1Options, typing.Dict[builtins.str, typing.Any]]]]] = None,
    protection_mode: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shiro_decryption_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__284005803ffb6db4c5ed29fbdabe7aaad8c111beaf1404ae4b34e76be043035a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98709ec8f87b41d2af23d7eeda9b83ddedc7d59a215366625df5b00fdfb2de83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPolicyV1Options, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59661a1370ed9f27238d49b04cf639d42602360bd14c56cfacaf00ac187d5714(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5f2c68b5bd03c6e8adbba718fb1e1acf7bcbd5ac34ef9a0b6580335b04d161(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f66a363f8ab8535b1e947bdff975b9ece10ff2ae49377e1ac73664fa2312d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfe415b674bd7c00ace4e81f016ada6c52f729679c55a1474a59cf9f03782b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a7bdf4ae4d2d1fac26233b912009d2a03f3ac40bc7e6834bccfe7d7cc6e59d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fdca141db73b6c1a10914fec9f4cbae6ac1f0b596bbd1270ecbec2f4c82b98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9964ed0140a8c8f2a3b482e501b16d0564874abaf2eb51e0eaab5a56983508f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cfc4ead3efb650d5ef5ef2785e55fd217dc453206d75bb00bbccef8c5cbbdad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da09237f219ddb971070ea341bf08ed37efd5e20ad16fe53baa89ef7907615c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b345ec378068c74113b5cd46447fe1037735cfd7a474f5ad62024087af63e2b5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    deep_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    full_detection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header_inspection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    level: typing.Optional[jsii.Number] = None,
    options: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPolicyV1Options, typing.Dict[builtins.str, typing.Any]]]]] = None,
    protection_mode: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    shiro_decryption_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedPolicyV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd7f8f876eac254ae5b7aceb056343777e7eb9fce2bbb9dddf0555b465c2058(
    *,
    anti_crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    anti_leakage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    anti_tamper: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    blacklist: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    common: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_engine: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_other: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_scanner: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crawler_script: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    followed_action: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    geolocation_access_control: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ignore: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    privacy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_attack: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_shell: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7c4f2a1201018fbff27260564ab1b0311951e50dfddb2344c73997bcfeadb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a047dd0b63699d5c21bab6ac48cc5ce6082207792cb63e846066762e5cc714a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c980b3a784941c3d811d4ac9b5530b78e8471e9d5ac4eebd750708edfe5d49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876fec1c21bceef542ca95e6c2f6b1a24d9dd4493468160577b768251cb9f524(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83798f3538f2af337c6d9f1f93f8040127dbb951c0416e7f4f667e0ca414217a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecde3dad294ced76e4acbb1e1f279e5a4ed2ac7ae5433fa2638cde3b87a7ad6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPolicyV1Options]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dc3239cd1cc9ac97680fbe70d3c826b4f169f2511d8299c97d4ec7e0a80743(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35c695f46df157e3c49af88ce0f89b21983dbe4fb0543cbf5edfada967e5ad9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1501fd491a70d6097061a148fcacdcea8f1608459873748883b62ce08112963c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e48d34a480397fb72b4cfd278ed26b53df07de3e95f2447bfa2259c62ef8bf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5ee5d8fa8441652318c12fac0c9076121222206fd0af165c7b6a6be15ff79d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddffeaef1d6f631f1f8d2c7e7475da772073946cb9f9f8a90ab42f8d6e6de18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9d63d3fffd1b1bed905389568c36360b62e151936346fc93f4aa5e70f06f44(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3e63d31cc1b9fbb1ccefdaa615c7d11bddf2dade8fdf53e992ffd66638771d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca26c639588f521e42099460fc59a547043d1dd206cb32ca609622e95d45942(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd294e4eb896dee0e0a89c8036c41c152421106668fcdb30967c6e9f4c7303af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69423c5bc6354e456d4d234006d1aa43a65feed01b336160895587248f57d924(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777e70f402df7955ebf36f7385986d0755d423875cf10dc848240aa6067e7bf7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ef1083783b85cecfb868e58154f42f2874459edaf339b23f0e83ddf01f0929(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53fd8a38f0a21718c6a8ef96182111b96953ae7b2922f93e28670f3ce2e093a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b7a113ae11c201045ec660b50125c35ddeee740aab6597fd7d2986621a34b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad235139b009d78ae38c61f93b2df2e3d3ad3c6838b6c3f409fd68bda424eef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e224aa3c03d4a457840bae81c3889ec96c6448ef501863e430e775e5d7d28b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ce40e755ba058cca34036045931169d0031f22478fe00b36d062631f43fe65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48268ee57402bab5dd14f2ab578d4707853c10b13d1308c3d62512990ff3c354(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1b0196bcc08d956450604c210ef38e60335ce7831a876fc22657e5884facc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Options]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e63648aee18abf033a956824a8087472bfb745701e141f0c7122185ee107c1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a86ec1760127d676f3d3e1d79b7b131ba8ec4c521aaf3e557a25d2bf8bfafbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d4ca32f147f6e91d334f3a75454e83b050f103f13c68e93480f925832a5ac5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f793e9f47b6c88f720335783de744b51191d75d94cce2e6f5b23a10b60c784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717c07b814bdebb2b139341f9ccbc62d3c53781c37f1b80d59eb7bec0d15b2fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPolicyV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

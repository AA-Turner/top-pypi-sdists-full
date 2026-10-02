r'''
# `google_model_armor_floorsetting`

Refer to the Terraform Registry for docs: [`google_model_armor_floorsetting`](https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting).
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


class GoogleModelArmorFloorsetting(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsetting",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting google_model_armor_floorsetting}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter_config: typing.Union["GoogleModelArmorFloorsettingFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        parent: builtins.str,
        ai_platform_floor_setting: typing.Optional[typing.Union["GoogleModelArmorFloorsettingAiPlatformFloorSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        floor_setting_metadata: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFloorSettingMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleModelArmorFloorsettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting google_model_armor_floorsetting} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_config GoogleModelArmorFloorsetting#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#location GoogleModelArmorFloorsetting#location}
        :param parent: Will be any one of these:. - 'projects/{project}' - 'folders/{folder}' - 'organizations/{organizationId}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#parent GoogleModelArmorFloorsetting#parent}
        :param ai_platform_floor_setting: ai_platform_floor_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#ai_platform_floor_setting GoogleModelArmorFloorsetting#ai_platform_floor_setting}
        :param enable_floor_setting_enforcement: Floor Settings enforcement status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_floor_setting_enforcement GoogleModelArmorFloorsetting#enable_floor_setting_enforcement}
        :param floor_setting_metadata: floor_setting_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#floor_setting_metadata GoogleModelArmorFloorsetting#floor_setting_metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#id GoogleModelArmorFloorsetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integrated_services: List of integrated services for which the floor setting is applicable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#integrated_services GoogleModelArmorFloorsetting#integrated_services}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#timeouts GoogleModelArmorFloorsetting#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd17d9c045c11aff8c514aed8922c7db048821f00c990e459f74744270d5131)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleModelArmorFloorsettingConfig(
            filter_config=filter_config,
            location=location,
            parent=parent,
            ai_platform_floor_setting=ai_platform_floor_setting,
            enable_floor_setting_enforcement=enable_floor_setting_enforcement,
            floor_setting_metadata=floor_setting_metadata,
            id=id,
            integrated_services=integrated_services,
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
        '''Generates CDKTF code for importing a GoogleModelArmorFloorsetting resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleModelArmorFloorsetting to import.
        :param import_from_id: The id of the existing GoogleModelArmorFloorsetting that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleModelArmorFloorsetting to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ba5722bac8c702a15e1416fb75420aa548356c69dabe593a8ef41b9c8ed819)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAiPlatformFloorSetting")
    def put_ai_platform_floor_setting(
        self,
        *,
        enable_cloud_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_and_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_cloud_logging: If true, log Model Armor filter results to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_cloud_logging GoogleModelArmorFloorsetting#enable_cloud_logging}
        :param inspect_and_block: If true, Model Armor filters will be run in inspect and block mode. Requests that trip Model Armor filters will be blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_and_block GoogleModelArmorFloorsetting#inspect_and_block}
        :param inspect_only: If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_only GoogleModelArmorFloorsetting#inspect_only}
        '''
        value = GoogleModelArmorFloorsettingAiPlatformFloorSetting(
            enable_cloud_logging=enable_cloud_logging,
            inspect_and_block=inspect_and_block,
            inspect_only=inspect_only,
        )

        return typing.cast(None, jsii.invoke(self, "putAiPlatformFloorSetting", [value]))

    @jsii.member(jsii_name="putFilterConfig")
    def put_filter_config(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#malicious_uri_filter_settings GoogleModelArmorFloorsetting#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#pi_and_jailbreak_filter_settings GoogleModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_settings GoogleModelArmorFloorsetting#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#sdp_settings GoogleModelArmorFloorsetting#sdp_settings}
        '''
        value = GoogleModelArmorFloorsettingFilterConfig(
            malicious_uri_filter_settings=malicious_uri_filter_settings,
            pi_and_jailbreak_filter_settings=pi_and_jailbreak_filter_settings,
            rai_settings=rai_settings,
            sdp_settings=sdp_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putFilterConfig", [value]))

    @jsii.member(jsii_name="putFloorSettingMetadata")
    def put_floor_setting_metadata(
        self,
        *,
        multi_language_detection: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#multi_language_detection GoogleModelArmorFloorsetting#multi_language_detection}
        '''
        value = GoogleModelArmorFloorsettingFloorSettingMetadata(
            multi_language_detection=multi_language_detection
        )

        return typing.cast(None, jsii.invoke(self, "putFloorSettingMetadata", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#create GoogleModelArmorFloorsetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#delete GoogleModelArmorFloorsetting#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#update GoogleModelArmorFloorsetting#update}.
        '''
        value = GoogleModelArmorFloorsettingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAiPlatformFloorSetting")
    def reset_ai_platform_floor_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiPlatformFloorSetting", []))

    @jsii.member(jsii_name="resetEnableFloorSettingEnforcement")
    def reset_enable_floor_setting_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableFloorSettingEnforcement", []))

    @jsii.member(jsii_name="resetFloorSettingMetadata")
    def reset_floor_setting_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloorSettingMetadata", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntegratedServices")
    def reset_integrated_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegratedServices", []))

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
    @jsii.member(jsii_name="aiPlatformFloorSetting")
    def ai_platform_floor_setting(
        self,
    ) -> "GoogleModelArmorFloorsettingAiPlatformFloorSettingOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingAiPlatformFloorSettingOutputReference", jsii.get(self, "aiPlatformFloorSetting"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="filterConfig")
    def filter_config(
        self,
    ) -> "GoogleModelArmorFloorsettingFilterConfigOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigOutputReference", jsii.get(self, "filterConfig"))

    @builtins.property
    @jsii.member(jsii_name="floorSettingMetadata")
    def floor_setting_metadata(
        self,
    ) -> "GoogleModelArmorFloorsettingFloorSettingMetadataOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingFloorSettingMetadataOutputReference", jsii.get(self, "floorSettingMetadata"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleModelArmorFloorsettingTimeoutsOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="aiPlatformFloorSettingInput")
    def ai_platform_floor_setting_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingAiPlatformFloorSetting"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingAiPlatformFloorSetting"], jsii.get(self, "aiPlatformFloorSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFloorSettingEnforcementInput")
    def enable_floor_setting_enforcement_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableFloorSettingEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="filterConfigInput")
    def filter_config_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfig"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfig"], jsii.get(self, "filterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="floorSettingMetadataInput")
    def floor_setting_metadata_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadata"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadata"], jsii.get(self, "floorSettingMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integratedServicesInput")
    def integrated_services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "integratedServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleModelArmorFloorsettingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleModelArmorFloorsettingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableFloorSettingEnforcement")
    def enable_floor_setting_enforcement(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableFloorSettingEnforcement"))

    @enable_floor_setting_enforcement.setter
    def enable_floor_setting_enforcement(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10539a690851845b0e58c1799929b7225b136ba231c8b1407dc3dbe5607f8ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFloorSettingEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d0faa007620c78630965835e6e4eb9a89d8b66818ac18252178ba47f991ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integratedServices")
    def integrated_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "integratedServices"))

    @integrated_services.setter
    def integrated_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9019f05e1bffa6a9538e05fced4a00606f338112cb3c370ff74bae0ac3d0e33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integratedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ab0b49cb063649d454d634e92ca493b20a945e23e6f33131818dd464414c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797a19b1d955aacd7cbdf0c6e92afaaf8d303538991b233da4049f7e548c11a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingAiPlatformFloorSetting",
    jsii_struct_bases=[],
    name_mapping={
        "enable_cloud_logging": "enableCloudLogging",
        "inspect_and_block": "inspectAndBlock",
        "inspect_only": "inspectOnly",
    },
)
class GoogleModelArmorFloorsettingAiPlatformFloorSetting:
    def __init__(
        self,
        *,
        enable_cloud_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_and_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_cloud_logging: If true, log Model Armor filter results to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_cloud_logging GoogleModelArmorFloorsetting#enable_cloud_logging}
        :param inspect_and_block: If true, Model Armor filters will be run in inspect and block mode. Requests that trip Model Armor filters will be blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_and_block GoogleModelArmorFloorsetting#inspect_and_block}
        :param inspect_only: If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_only GoogleModelArmorFloorsetting#inspect_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c80798f46bcf3b19261878b84d71d042d4fdedaf04205c04a32346c5b95477d)
            check_type(argname="argument enable_cloud_logging", value=enable_cloud_logging, expected_type=type_hints["enable_cloud_logging"])
            check_type(argname="argument inspect_and_block", value=inspect_and_block, expected_type=type_hints["inspect_and_block"])
            check_type(argname="argument inspect_only", value=inspect_only, expected_type=type_hints["inspect_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_cloud_logging is not None:
            self._values["enable_cloud_logging"] = enable_cloud_logging
        if inspect_and_block is not None:
            self._values["inspect_and_block"] = inspect_and_block
        if inspect_only is not None:
            self._values["inspect_only"] = inspect_only

    @builtins.property
    def enable_cloud_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, log Model Armor filter results to Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_cloud_logging GoogleModelArmorFloorsetting#enable_cloud_logging}
        '''
        result = self._values.get("enable_cloud_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inspect_and_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Model Armor filters will be run in inspect and block mode.

        Requests that trip Model Armor filters will be blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_and_block GoogleModelArmorFloorsetting#inspect_and_block}
        '''
        result = self._values.get("inspect_and_block")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inspect_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_only GoogleModelArmorFloorsetting#inspect_only}
        '''
        result = self._values.get("inspect_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingAiPlatformFloorSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingAiPlatformFloorSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingAiPlatformFloorSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5035074a65df93baeace7e3cf2f444aba0b31d2c098604c5626456b1750e62f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableCloudLogging")
    def reset_enable_cloud_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableCloudLogging", []))

    @jsii.member(jsii_name="resetInspectAndBlock")
    def reset_inspect_and_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectAndBlock", []))

    @jsii.member(jsii_name="resetInspectOnly")
    def reset_inspect_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectOnly", []))

    @builtins.property
    @jsii.member(jsii_name="enableCloudLoggingInput")
    def enable_cloud_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableCloudLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectAndBlockInput")
    def inspect_and_block_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inspectAndBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectOnlyInput")
    def inspect_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inspectOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableCloudLogging")
    def enable_cloud_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableCloudLogging"))

    @enable_cloud_logging.setter
    def enable_cloud_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadd1ce0e1b50a2189b8ed461895c7beafa92fc41cc62222f6927a68d8065782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCloudLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectAndBlock")
    def inspect_and_block(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inspectAndBlock"))

    @inspect_and_block.setter
    def inspect_and_block(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9e6f8721b0400c93a626a362063ab0dbceb0ae9677b639049641beda724b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectAndBlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectOnly")
    def inspect_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inspectOnly"))

    @inspect_only.setter
    def inspect_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c56a7614afade1b02e81bb3e16d3240d9f70c13894b40c0116bac993af473bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a4632a408d34080e21e829b2d6ecf22c74b25fb0514c399d3285a0192ac36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filter_config": "filterConfig",
        "location": "location",
        "parent": "parent",
        "ai_platform_floor_setting": "aiPlatformFloorSetting",
        "enable_floor_setting_enforcement": "enableFloorSettingEnforcement",
        "floor_setting_metadata": "floorSettingMetadata",
        "id": "id",
        "integrated_services": "integratedServices",
        "timeouts": "timeouts",
    },
)
class GoogleModelArmorFloorsettingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter_config: typing.Union["GoogleModelArmorFloorsettingFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        parent: builtins.str,
        ai_platform_floor_setting: typing.Optional[typing.Union[GoogleModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        floor_setting_metadata: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFloorSettingMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleModelArmorFloorsettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_config GoogleModelArmorFloorsetting#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#location GoogleModelArmorFloorsetting#location}
        :param parent: Will be any one of these:. - 'projects/{project}' - 'folders/{folder}' - 'organizations/{organizationId}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#parent GoogleModelArmorFloorsetting#parent}
        :param ai_platform_floor_setting: ai_platform_floor_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#ai_platform_floor_setting GoogleModelArmorFloorsetting#ai_platform_floor_setting}
        :param enable_floor_setting_enforcement: Floor Settings enforcement status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_floor_setting_enforcement GoogleModelArmorFloorsetting#enable_floor_setting_enforcement}
        :param floor_setting_metadata: floor_setting_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#floor_setting_metadata GoogleModelArmorFloorsetting#floor_setting_metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#id GoogleModelArmorFloorsetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integrated_services: List of integrated services for which the floor setting is applicable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#integrated_services GoogleModelArmorFloorsetting#integrated_services}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#timeouts GoogleModelArmorFloorsetting#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter_config, dict):
            filter_config = GoogleModelArmorFloorsettingFilterConfig(**filter_config)
        if isinstance(ai_platform_floor_setting, dict):
            ai_platform_floor_setting = GoogleModelArmorFloorsettingAiPlatformFloorSetting(**ai_platform_floor_setting)
        if isinstance(floor_setting_metadata, dict):
            floor_setting_metadata = GoogleModelArmorFloorsettingFloorSettingMetadata(**floor_setting_metadata)
        if isinstance(timeouts, dict):
            timeouts = GoogleModelArmorFloorsettingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbb679a033c400fd0d840c8779038d7297a37e22e52d7389cf51b8cb335a72f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filter_config", value=filter_config, expected_type=type_hints["filter_config"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument ai_platform_floor_setting", value=ai_platform_floor_setting, expected_type=type_hints["ai_platform_floor_setting"])
            check_type(argname="argument enable_floor_setting_enforcement", value=enable_floor_setting_enforcement, expected_type=type_hints["enable_floor_setting_enforcement"])
            check_type(argname="argument floor_setting_metadata", value=floor_setting_metadata, expected_type=type_hints["floor_setting_metadata"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument integrated_services", value=integrated_services, expected_type=type_hints["integrated_services"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_config": filter_config,
            "location": location,
            "parent": parent,
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
        if ai_platform_floor_setting is not None:
            self._values["ai_platform_floor_setting"] = ai_platform_floor_setting
        if enable_floor_setting_enforcement is not None:
            self._values["enable_floor_setting_enforcement"] = enable_floor_setting_enforcement
        if floor_setting_metadata is not None:
            self._values["floor_setting_metadata"] = floor_setting_metadata
        if id is not None:
            self._values["id"] = id
        if integrated_services is not None:
            self._values["integrated_services"] = integrated_services
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
    def filter_config(self) -> "GoogleModelArmorFloorsettingFilterConfig":
        '''filter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_config GoogleModelArmorFloorsetting#filter_config}
        '''
        result = self._values.get("filter_config")
        assert result is not None, "Required property 'filter_config' is missing"
        return typing.cast("GoogleModelArmorFloorsettingFilterConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#location GoogleModelArmorFloorsetting#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent(self) -> builtins.str:
        '''Will be any one of these:.

        - 'projects/{project}'
        - 'folders/{folder}'
        - 'organizations/{organizationId}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#parent GoogleModelArmorFloorsetting#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ai_platform_floor_setting(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting]:
        '''ai_platform_floor_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#ai_platform_floor_setting GoogleModelArmorFloorsetting#ai_platform_floor_setting}
        '''
        result = self._values.get("ai_platform_floor_setting")
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting], result)

    @builtins.property
    def enable_floor_setting_enforcement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Floor Settings enforcement status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_floor_setting_enforcement GoogleModelArmorFloorsetting#enable_floor_setting_enforcement}
        '''
        result = self._values.get("enable_floor_setting_enforcement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def floor_setting_metadata(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadata"]:
        '''floor_setting_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#floor_setting_metadata GoogleModelArmorFloorsetting#floor_setting_metadata}
        '''
        result = self._values.get("floor_setting_metadata")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadata"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#id GoogleModelArmorFloorsetting#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integrated_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of integrated services for which the floor setting is applicable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#integrated_services GoogleModelArmorFloorsetting#integrated_services}
        '''
        result = self._values.get("integrated_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleModelArmorFloorsettingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#timeouts GoogleModelArmorFloorsetting#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "malicious_uri_filter_settings": "maliciousUriFilterSettings",
        "pi_and_jailbreak_filter_settings": "piAndJailbreakFilterSettings",
        "rai_settings": "raiSettings",
        "sdp_settings": "sdpSettings",
    },
)
class GoogleModelArmorFloorsettingFilterConfig:
    def __init__(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#malicious_uri_filter_settings GoogleModelArmorFloorsetting#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#pi_and_jailbreak_filter_settings GoogleModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_settings GoogleModelArmorFloorsetting#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#sdp_settings GoogleModelArmorFloorsetting#sdp_settings}
        '''
        if isinstance(malicious_uri_filter_settings, dict):
            malicious_uri_filter_settings = GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(**malicious_uri_filter_settings)
        if isinstance(pi_and_jailbreak_filter_settings, dict):
            pi_and_jailbreak_filter_settings = GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(**pi_and_jailbreak_filter_settings)
        if isinstance(rai_settings, dict):
            rai_settings = GoogleModelArmorFloorsettingFilterConfigRaiSettings(**rai_settings)
        if isinstance(sdp_settings, dict):
            sdp_settings = GoogleModelArmorFloorsettingFilterConfigSdpSettings(**sdp_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324f12d4af77d363e38de0b40ba170fa1610c2249dfd06972b35d67de75150bf)
            check_type(argname="argument malicious_uri_filter_settings", value=malicious_uri_filter_settings, expected_type=type_hints["malicious_uri_filter_settings"])
            check_type(argname="argument pi_and_jailbreak_filter_settings", value=pi_and_jailbreak_filter_settings, expected_type=type_hints["pi_and_jailbreak_filter_settings"])
            check_type(argname="argument rai_settings", value=rai_settings, expected_type=type_hints["rai_settings"])
            check_type(argname="argument sdp_settings", value=sdp_settings, expected_type=type_hints["sdp_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if malicious_uri_filter_settings is not None:
            self._values["malicious_uri_filter_settings"] = malicious_uri_filter_settings
        if pi_and_jailbreak_filter_settings is not None:
            self._values["pi_and_jailbreak_filter_settings"] = pi_and_jailbreak_filter_settings
        if rai_settings is not None:
            self._values["rai_settings"] = rai_settings
        if sdp_settings is not None:
            self._values["sdp_settings"] = sdp_settings

    @builtins.property
    def malicious_uri_filter_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings"]:
        '''malicious_uri_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#malicious_uri_filter_settings GoogleModelArmorFloorsetting#malicious_uri_filter_settings}
        '''
        result = self._values.get("malicious_uri_filter_settings")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings"], result)

    @builtins.property
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"]:
        '''pi_and_jailbreak_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#pi_and_jailbreak_filter_settings GoogleModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        '''
        result = self._values.get("pi_and_jailbreak_filter_settings")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"], result)

    @builtins.property
    def rai_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigRaiSettings"]:
        '''rai_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_settings GoogleModelArmorFloorsetting#rai_settings}
        '''
        result = self._values.get("rai_settings")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigRaiSettings"], result)

    @builtins.property
    def sdp_settings(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettings"]:
        '''sdp_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#sdp_settings GoogleModelArmorFloorsetting#sdp_settings}
        '''
        result = self._values.get("sdp_settings")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bf1052ac98d26c3953e9a5b0d66163bb12a9ca367b060c0ed0feac184700b8)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__463077e2732bc8a08a0e9406e2929efdd2952cec978631822ca5faab3a38b936)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c943d0845d27adf5871172da42c695df0762ca536d4238443fda334a224e3645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230f5115e8f3b65e4e482dcf6f1760fc473cec18ff07934674cd9eb136a3abd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorFloorsettingFilterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcea9a0adcbe16c935271685486accafbd22992ddc89844025a30d4d03cab81d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaliciousUriFilterSettings")
    def put_malicious_uri_filter_settings(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(
            filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putMaliciousUriFilterSettings", [value]))

    @jsii.member(jsii_name="putPiAndJailbreakFilterSettings")
    def put_pi_and_jailbreak_filter_settings(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#confidence_level GoogleModelArmorFloorsetting#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(
            confidence_level=confidence_level, filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putPiAndJailbreakFilterSettings", [value]))

    @jsii.member(jsii_name="putRaiSettings")
    def put_rai_settings(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_filters GoogleModelArmorFloorsetting#rai_filters}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigRaiSettings(
            rai_filters=rai_filters
        )

        return typing.cast(None, jsii.invoke(self, "putRaiSettings", [value]))

    @jsii.member(jsii_name="putSdpSettings")
    def put_sdp_settings(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#advanced_config GoogleModelArmorFloorsetting#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#basic_config GoogleModelArmorFloorsetting#basic_config}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigSdpSettings(
            advanced_config=advanced_config, basic_config=basic_config
        )

        return typing.cast(None, jsii.invoke(self, "putSdpSettings", [value]))

    @jsii.member(jsii_name="resetMaliciousUriFilterSettings")
    def reset_malicious_uri_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaliciousUriFilterSettings", []))

    @jsii.member(jsii_name="resetPiAndJailbreakFilterSettings")
    def reset_pi_and_jailbreak_filter_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPiAndJailbreakFilterSettings", []))

    @jsii.member(jsii_name="resetRaiSettings")
    def reset_rai_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRaiSettings", []))

    @jsii.member(jsii_name="resetSdpSettings")
    def reset_sdp_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSdpSettings", []))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettings")
    def malicious_uri_filter_settings(
        self,
    ) -> GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference:
        return typing.cast(GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference, jsii.get(self, "maliciousUriFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettings")
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> "GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference", jsii.get(self, "piAndJailbreakFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="raiSettings")
    def rai_settings(
        self,
    ) -> "GoogleModelArmorFloorsettingFilterConfigRaiSettingsOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigRaiSettingsOutputReference", jsii.get(self, "raiSettings"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettings")
    def sdp_settings(
        self,
    ) -> "GoogleModelArmorFloorsettingFilterConfigSdpSettingsOutputReference":
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigSdpSettingsOutputReference", jsii.get(self, "sdpSettings"))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettingsInput")
    def malicious_uri_filter_settings_input(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings], jsii.get(self, "maliciousUriFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettingsInput")
    def pi_and_jailbreak_filter_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"], jsii.get(self, "piAndJailbreakFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="raiSettingsInput")
    def rai_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigRaiSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigRaiSettings"], jsii.get(self, "raiSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettingsInput")
    def sdp_settings_input(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettings"]:
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettings"], jsii.get(self, "sdpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a602c86155afe83dc3beb8b7d248c0840b1f062a3ec5f40b84721fce487ed29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_level": "confidenceLevel",
        "filter_enforcement": "filterEnforcement",
    },
)
class GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings:
    def __init__(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#confidence_level GoogleModelArmorFloorsetting#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf1a56f155bf3c2ac5b80bf54632474cd8bcf1e3bb782f66cd367bb54f881ab)
            check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidence_level is not None:
            self._values["confidence_level"] = confidence_level
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#confidence_level GoogleModelArmorFloorsetting#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a17324084d459a560ac957ebdee623b4fa94d24941d24d48e9e822181f3a609)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidenceLevel")
    def reset_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceLevel", []))

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevelInput")
    def confidence_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevel")
    def confidence_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidenceLevel"))

    @confidence_level.setter
    def confidence_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5b8ceb2f1efc38afde556124291161a5a9fdec9079fe33707594d1250b0d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f0de75c9c59dbd3575663a9996c27b64a37b3522ae1e471910d8572448f188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8166ea72ac2dbdb5d1333054b69055996a6c47110f8e66fe740d153e918dded5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigRaiSettings",
    jsii_struct_bases=[],
    name_mapping={"rai_filters": "raiFilters"},
)
class GoogleModelArmorFloorsettingFilterConfigRaiSettings:
    def __init__(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_filters GoogleModelArmorFloorsetting#rai_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f35a7207b08d6538166ea92ba6dee840721608ec53b98979d0f4079f334a7f)
            check_type(argname="argument rai_filters", value=rai_filters, expected_type=type_hints["rai_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rai_filters": rai_filters,
        }

    @builtins.property
    def rai_filters(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]:
        '''rai_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#rai_filters GoogleModelArmorFloorsetting#rai_filters}
        '''
        result = self._values.get("rai_filters")
        assert result is not None, "Required property 'rai_filters' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigRaiSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigRaiSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigRaiSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d1528a8acbac1b9404576b0418b2526cc7b182727b18228f4899e384b6a0bce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRaiFilters")
    def put_rai_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6246946252e0c4edd602dfc51b30d58ae2cdabf2dbcc712884bffbd2c03f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRaiFilters", [value]))

    @builtins.property
    @jsii.member(jsii_name="raiFilters")
    def rai_filters(
        self,
    ) -> "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList":
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList", jsii.get(self, "raiFilters"))

    @builtins.property
    @jsii.member(jsii_name="raiFiltersInput")
    def rai_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]], jsii.get(self, "raiFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigRaiSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigRaiSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigRaiSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cf796e24f152cbbb9f0df4de2bcd089848af25c6c02a3340c26b94a7aff49d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters",
    jsii_struct_bases=[],
    name_mapping={"filter_type": "filterType", "confidence_level": "confidenceLevel"},
)
class GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters:
    def __init__(
        self,
        *,
        filter_type: builtins.str,
        confidence_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_type: Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_type GoogleModelArmorFloorsetting#filter_type}
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#confidence_level GoogleModelArmorFloorsetting#confidence_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30b5178a5b97e85ceb4f73fa8dea6a1ea9f4b9279f828ce25cbfe3bda93e653)
            check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
            check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter_type": filter_type,
        }
        if confidence_level is not None:
            self._values["confidence_level"] = confidence_level

    @builtins.property
    def filter_type(self) -> builtins.str:
        '''Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_type GoogleModelArmorFloorsetting#filter_type}
        '''
        result = self._values.get("filter_type")
        assert result is not None, "Required property 'filter_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#confidence_level GoogleModelArmorFloorsetting#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d16450ca995f9d8e910582af0a60eef3fe4c5e95b0b8f5297ff5aa57e4241ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aeefc81d16053b254ee14416e759e84b184f98f18b969fb4f186b339dc5b85f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3f4314b26afb73c032e5f63d6682ab06a7cf963bb8ac9eae7d0ad1e6403263)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ffa06ca1f9070fc18ffe4966af51bdddfe0fca73416481b544810fe86ad08cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a4e9e4d626cb90208262d106afd3b487fd7dbc5676db54027300e838ea1a9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dfc1a1b0f0758fea3744b39070e3ec65a8067454741e5076f4f5d81dd8c03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f87e0721668bfae12be3a532e6c18b6319c11fcf76574fc758ef1253990ee96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfidenceLevel")
    def reset_confidence_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidenceLevel", []))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevelInput")
    def confidence_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidenceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="filterTypeInput")
    def filter_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="confidenceLevel")
    def confidence_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidenceLevel"))

    @confidence_level.setter
    def confidence_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1afca08afd34ce434badbf4ead29cef5784867456cbc9dfb753969bc20bd48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd54e8027ecea07b9a8227452f0c5fa3f6bda38e237b60df491056f145995b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618e26e7b502bb87428c4080722c014e5bc4514cffbc7018555a53e6354d96d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettings",
    jsii_struct_bases=[],
    name_mapping={"advanced_config": "advancedConfig", "basic_config": "basicConfig"},
)
class GoogleModelArmorFloorsettingFilterConfigSdpSettings:
    def __init__(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#advanced_config GoogleModelArmorFloorsetting#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#basic_config GoogleModelArmorFloorsetting#basic_config}
        '''
        if isinstance(advanced_config, dict):
            advanced_config = GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(**advanced_config)
        if isinstance(basic_config, dict):
            basic_config = GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(**basic_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ce8d2ac2a486bfefdd9811fc5b59d9c3291e267c76950e7f7860ac35de0e1c)
            check_type(argname="argument advanced_config", value=advanced_config, expected_type=type_hints["advanced_config"])
            check_type(argname="argument basic_config", value=basic_config, expected_type=type_hints["basic_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_config is not None:
            self._values["advanced_config"] = advanced_config
        if basic_config is not None:
            self._values["basic_config"] = basic_config

    @builtins.property
    def advanced_config(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig"]:
        '''advanced_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#advanced_config GoogleModelArmorFloorsetting#advanced_config}
        '''
        result = self._values.get("advanced_config")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig"], result)

    @builtins.property
    def basic_config(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig"]:
        '''basic_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#basic_config GoogleModelArmorFloorsetting#basic_config}
        '''
        result = self._values.get("basic_config")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigSdpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "inspect_template": "inspectTemplate",
    },
)
class GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#deidentify_template GoogleModelArmorFloorsetting#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name. If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_template GoogleModelArmorFloorsetting#inspect_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f59680385978677e6a9c0d82507fb6b73ecbc758effaddbbd9a949090f8bfc)
            check_type(argname="argument deidentify_template", value=deidentify_template, expected_type=type_hints["deidentify_template"])
            check_type(argname="argument inspect_template", value=inspect_template, expected_type=type_hints["inspect_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deidentify_template is not None:
            self._values["deidentify_template"] = deidentify_template
        if inspect_template is not None:
            self._values["inspect_template"] = inspect_template

    @builtins.property
    def deidentify_template(self) -> typing.Optional[builtins.str]:
        '''Optional Sensitive Data Protection Deidentify template resource name.

        If provided then DeidentifyContent action is performed during Sanitization
        using this template and inspect template. The De-identified data will
        be returned in SdpDeidentifyResult.
        Note that all info-types present in the deidentify template must be present
        in inspect template.

        e.g.
        'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#deidentify_template GoogleModelArmorFloorsetting#deidentify_template}
        '''
        result = self._values.get("deidentify_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inspect_template(self) -> typing.Optional[builtins.str]:
        '''Sensitive Data Protection inspect template resource name.

        If only inspect template is provided (de-identify template not provided),
        then Sensitive Data Protection InspectContent action is performed during
        Sanitization. All Sensitive Data Protection findings identified during
        inspection will be returned as SdpFinding in SdpInsepctionResult.

        e.g:-
        'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_template GoogleModelArmorFloorsetting#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e91d93b5dbdf66c8466e41ba0c65f0e9a06be6fa7f89ccbb3876fe11625032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeidentifyTemplate")
    def reset_deidentify_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeidentifyTemplate", []))

    @jsii.member(jsii_name="resetInspectTemplate")
    def reset_inspect_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInspectTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplateInput")
    def deidentify_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deidentifyTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="inspectTemplateInput")
    def inspect_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inspectTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="deidentifyTemplate")
    def deidentify_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deidentifyTemplate"))

    @deidentify_template.setter
    def deidentify_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6c0b4fc48f124d4fabb70c1ba154ee078ec18c1732e6f479fa9f7922e7cfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373bf405c3bd252b833d4de07cc90e2d0ca7300a49cb25091932b16672289b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088c90a91191128b049595b6f465e12b71d71d3b61c36717678230343e7d948e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41227a269a33363a5f0e9d0008f2a0b32a9950eb6653dcb922c3bfb990df766)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d79800c4e46338cf02d5a4e7fe79c12475cb758274a03cdaab2c625554f061aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFilterEnforcement")
    def reset_filter_enforcement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterEnforcement", []))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcementInput")
    def filter_enforcement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterEnforcementInput"))

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303b7f165027cf991eaec73265b6dc5cb6282fdc234719c566589c9b571f7f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7c92cc56213160494e42695493335767ae74100ad9e72b93898aeb45133958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorFloorsettingFilterConfigSdpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFilterConfigSdpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd6b21445e740794857a4c9a03016d9388432f7bafcdbbf6d1889fe0abfe6f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvancedConfig")
    def put_advanced_config(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#deidentify_template GoogleModelArmorFloorsetting#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name. If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#inspect_template GoogleModelArmorFloorsetting#inspect_template}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(
            deidentify_template=deidentify_template, inspect_template=inspect_template
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedConfig", [value]))

    @jsii.member(jsii_name="putBasicConfig")
    def put_basic_config(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#filter_enforcement GoogleModelArmorFloorsetting#filter_enforcement}
        '''
        value = GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(
            filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putBasicConfig", [value]))

    @jsii.member(jsii_name="resetAdvancedConfig")
    def reset_advanced_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedConfig", []))

    @jsii.member(jsii_name="resetBasicConfig")
    def reset_basic_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicConfig", []))

    @builtins.property
    @jsii.member(jsii_name="advancedConfig")
    def advanced_config(
        self,
    ) -> GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference:
        return typing.cast(GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference, jsii.get(self, "advancedConfig"))

    @builtins.property
    @jsii.member(jsii_name="basicConfig")
    def basic_config(
        self,
    ) -> GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference:
        return typing.cast(GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference, jsii.get(self, "basicConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfigInput")
    def advanced_config_input(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "advancedConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="basicConfigInput")
    def basic_config_input(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig], jsii.get(self, "basicConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettings]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede60e061c011819a89ed1e02764b02ab0a97d57b62f6ed83b65112104270a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFloorSettingMetadata",
    jsii_struct_bases=[],
    name_mapping={"multi_language_detection": "multiLanguageDetection"},
)
class GoogleModelArmorFloorsettingFloorSettingMetadata:
    def __init__(
        self,
        *,
        multi_language_detection: typing.Optional[typing.Union["GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#multi_language_detection GoogleModelArmorFloorsetting#multi_language_detection}
        '''
        if isinstance(multi_language_detection, dict):
            multi_language_detection = GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(**multi_language_detection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__122d3e14b58ec61a738e88bfc25ad8286f8d08841a444716099eb5fefe69672b)
            check_type(argname="argument multi_language_detection", value=multi_language_detection, expected_type=type_hints["multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if multi_language_detection is not None:
            self._values["multi_language_detection"] = multi_language_detection

    @builtins.property
    def multi_language_detection(
        self,
    ) -> typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection"]:
        '''multi_language_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#multi_language_detection GoogleModelArmorFloorsetting#multi_language_detection}
        '''
        result = self._values.get("multi_language_detection")
        return typing.cast(typing.Optional["GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFloorSettingMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection",
    jsii_struct_bases=[],
    name_mapping={"enable_multi_language_detection": "enableMultiLanguageDetection"},
)
class GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection:
    def __init__(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_multi_language_detection GoogleModelArmorFloorsetting#enable_multi_language_detection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6407a85ac57286aa471cd97740d372849296a47c3af7af9bca04d02f2da54a7)
            check_type(argname="argument enable_multi_language_detection", value=enable_multi_language_detection, expected_type=type_hints["enable_multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_multi_language_detection": enable_multi_language_detection,
        }

    @builtins.property
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, multi language detection will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_multi_language_detection GoogleModelArmorFloorsetting#enable_multi_language_detection}
        '''
        result = self._values.get("enable_multi_language_detection")
        assert result is not None, "Required property 'enable_multi_language_detection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4983e23544066b67066bbb4cc2be16e16dcf92d6603ecb4400c2a4a27f465de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enableMultiLanguageDetectionInput")
    def enable_multi_language_detection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableMultiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableMultiLanguageDetection")
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableMultiLanguageDetection"))

    @enable_multi_language_detection.setter
    def enable_multi_language_detection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4a4af63dc081cf806de94ba06533da64d11f96e595593ab1a334a5ed8e7d67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMultiLanguageDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a4126fc988d9e2ed71514ebf99e7b25cde9540516a45c358f6b523f95b7be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleModelArmorFloorsettingFloorSettingMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingFloorSettingMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69832828f3c30aaffae6ef113890496249f108687969f2cde4df1f05716acb0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMultiLanguageDetection")
    def put_multi_language_detection(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#enable_multi_language_detection GoogleModelArmorFloorsetting#enable_multi_language_detection}
        '''
        value = GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(
            enable_multi_language_detection=enable_multi_language_detection
        )

        return typing.cast(None, jsii.invoke(self, "putMultiLanguageDetection", [value]))

    @jsii.member(jsii_name="resetMultiLanguageDetection")
    def reset_multi_language_detection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiLanguageDetection", []))

    @builtins.property
    @jsii.member(jsii_name="multiLanguageDetection")
    def multi_language_detection(
        self,
    ) -> GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference:
        return typing.cast(GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference, jsii.get(self, "multiLanguageDetection"))

    @builtins.property
    @jsii.member(jsii_name="multiLanguageDetectionInput")
    def multi_language_detection_input(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection], jsii.get(self, "multiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadata]:
        return typing.cast(typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b495b570c6bd1fc015350a52d6c0549d73a86317d9500167c0a6d70bb83182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleModelArmorFloorsettingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#create GoogleModelArmorFloorsetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#delete GoogleModelArmorFloorsetting#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#update GoogleModelArmorFloorsetting#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a488dd34f5c554cd006e6522ec466d776d98abc899cd935bcda2cd2fb3c9eb8f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#create GoogleModelArmorFloorsetting#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#delete GoogleModelArmorFloorsetting#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.50.0/docs/resources/google_model_armor_floorsetting#update GoogleModelArmorFloorsetting#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleModelArmorFloorsettingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleModelArmorFloorsettingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleModelArmorFloorsetting.GoogleModelArmorFloorsettingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc598a9f82d572d4d3cefc83a67fe093c54cf73e9aae9e898f45bd375e79467a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c942417b425cf09510c106b2235d0fb700f92e9e827d0e85dfbf7656d1183e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d964a748128192e5cca5dffba5646aba4a35ce69dce65aff4d2f094ee0082d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7765f656143bd7844d5f9391be4bec43f973b60a84f5969c3036991735d59e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2214a4b00dab5554c86b69c0c5109a3d62251435bbb1604297c6ee57c56400f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleModelArmorFloorsetting",
    "GoogleModelArmorFloorsettingAiPlatformFloorSetting",
    "GoogleModelArmorFloorsettingAiPlatformFloorSettingOutputReference",
    "GoogleModelArmorFloorsettingConfig",
    "GoogleModelArmorFloorsettingFilterConfig",
    "GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings",
    "GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings",
    "GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigRaiSettings",
    "GoogleModelArmorFloorsettingFilterConfigRaiSettingsOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters",
    "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList",
    "GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettings",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference",
    "GoogleModelArmorFloorsettingFilterConfigSdpSettingsOutputReference",
    "GoogleModelArmorFloorsettingFloorSettingMetadata",
    "GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection",
    "GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference",
    "GoogleModelArmorFloorsettingFloorSettingMetadataOutputReference",
    "GoogleModelArmorFloorsettingTimeouts",
    "GoogleModelArmorFloorsettingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8cd17d9c045c11aff8c514aed8922c7db048821f00c990e459f74744270d5131(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter_config: typing.Union[GoogleModelArmorFloorsettingFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    parent: builtins.str,
    ai_platform_floor_setting: typing.Optional[typing.Union[GoogleModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    floor_setting_metadata: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFloorSettingMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleModelArmorFloorsettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__21ba5722bac8c702a15e1416fb75420aa548356c69dabe593a8ef41b9c8ed819(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10539a690851845b0e58c1799929b7225b136ba231c8b1407dc3dbe5607f8ffb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d0faa007620c78630965835e6e4eb9a89d8b66818ac18252178ba47f991ec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9019f05e1bffa6a9538e05fced4a00606f338112cb3c370ff74bae0ac3d0e33e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ab0b49cb063649d454d634e92ca493b20a945e23e6f33131818dd464414c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797a19b1d955aacd7cbdf0c6e92afaaf8d303538991b233da4049f7e548c11a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c80798f46bcf3b19261878b84d71d042d4fdedaf04205c04a32346c5b95477d(
    *,
    enable_cloud_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inspect_and_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inspect_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5035074a65df93baeace7e3cf2f444aba0b31d2c098604c5626456b1750e62f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadd1ce0e1b50a2189b8ed461895c7beafa92fc41cc62222f6927a68d8065782(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9e6f8721b0400c93a626a362063ab0dbceb0ae9677b639049641beda724b09(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c56a7614afade1b02e81bb3e16d3240d9f70c13894b40c0116bac993af473bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a4632a408d34080e21e829b2d6ecf22c74b25fb0514c399d3285a0192ac36f(
    value: typing.Optional[GoogleModelArmorFloorsettingAiPlatformFloorSetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbb679a033c400fd0d840c8779038d7297a37e22e52d7389cf51b8cb335a72f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter_config: typing.Union[GoogleModelArmorFloorsettingFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    parent: builtins.str,
    ai_platform_floor_setting: typing.Optional[typing.Union[GoogleModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    floor_setting_metadata: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFloorSettingMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleModelArmorFloorsettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324f12d4af77d363e38de0b40ba170fa1610c2249dfd06972b35d67de75150bf(
    *,
    malicious_uri_filter_settings: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    pi_and_jailbreak_filter_settings: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    rai_settings: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigRaiSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    sdp_settings: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigSdpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bf1052ac98d26c3953e9a5b0d66163bb12a9ca367b060c0ed0feac184700b8(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463077e2732bc8a08a0e9406e2929efdd2952cec978631822ca5faab3a38b936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c943d0845d27adf5871172da42c695df0762ca536d4238443fda334a224e3645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230f5115e8f3b65e4e482dcf6f1760fc473cec18ff07934674cd9eb136a3abd2(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcea9a0adcbe16c935271685486accafbd22992ddc89844025a30d4d03cab81d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a602c86155afe83dc3beb8b7d248c0840b1f062a3ec5f40b84721fce487ed29(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf1a56f155bf3c2ac5b80bf54632474cd8bcf1e3bb782f66cd367bb54f881ab(
    *,
    confidence_level: typing.Optional[builtins.str] = None,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a17324084d459a560ac957ebdee623b4fa94d24941d24d48e9e822181f3a609(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5b8ceb2f1efc38afde556124291161a5a9fdec9079fe33707594d1250b0d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f0de75c9c59dbd3575663a9996c27b64a37b3522ae1e471910d8572448f188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8166ea72ac2dbdb5d1333054b69055996a6c47110f8e66fe740d153e918dded5(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f35a7207b08d6538166ea92ba6dee840721608ec53b98979d0f4079f334a7f(
    *,
    rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1528a8acbac1b9404576b0418b2526cc7b182727b18228f4899e384b6a0bce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6246946252e0c4edd602dfc51b30d58ae2cdabf2dbcc712884bffbd2c03f7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cf796e24f152cbbb9f0df4de2bcd089848af25c6c02a3340c26b94a7aff49d(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigRaiSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30b5178a5b97e85ceb4f73fa8dea6a1ea9f4b9279f828ce25cbfe3bda93e653(
    *,
    filter_type: builtins.str,
    confidence_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d16450ca995f9d8e910582af0a60eef3fe4c5e95b0b8f5297ff5aa57e4241ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aeefc81d16053b254ee14416e759e84b184f98f18b969fb4f186b339dc5b85f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3f4314b26afb73c032e5f63d6682ab06a7cf963bb8ac9eae7d0ad1e6403263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffa06ca1f9070fc18ffe4966af51bdddfe0fca73416481b544810fe86ad08cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4e9e4d626cb90208262d106afd3b487fd7dbc5676db54027300e838ea1a9bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dfc1a1b0f0758fea3744b39070e3ec65a8067454741e5076f4f5d81dd8c03a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f87e0721668bfae12be3a532e6c18b6319c11fcf76574fc758ef1253990ee96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1afca08afd34ce434badbf4ead29cef5784867456cbc9dfb753969bc20bd48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd54e8027ecea07b9a8227452f0c5fa3f6bda38e237b60df491056f145995b9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618e26e7b502bb87428c4080722c014e5bc4514cffbc7018555a53e6354d96d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ce8d2ac2a486bfefdd9811fc5b59d9c3291e267c76950e7f7860ac35de0e1c(
    *,
    advanced_config: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_config: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f59680385978677e6a9c0d82507fb6b73ecbc758effaddbbd9a949090f8bfc(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    inspect_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e91d93b5dbdf66c8466e41ba0c65f0e9a06be6fa7f89ccbb3876fe11625032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6c0b4fc48f124d4fabb70c1ba154ee078ec18c1732e6f479fa9f7922e7cfd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373bf405c3bd252b833d4de07cc90e2d0ca7300a49cb25091932b16672289b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088c90a91191128b049595b6f465e12b71d71d3b61c36717678230343e7d948e(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41227a269a33363a5f0e9d0008f2a0b32a9950eb6653dcb922c3bfb990df766(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79800c4e46338cf02d5a4e7fe79c12475cb758274a03cdaab2c625554f061aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303b7f165027cf991eaec73265b6dc5cb6282fdc234719c566589c9b571f7f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7c92cc56213160494e42695493335767ae74100ad9e72b93898aeb45133958(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6b21445e740794857a4c9a03016d9388432f7bafcdbbf6d1889fe0abfe6f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede60e061c011819a89ed1e02764b02ab0a97d57b62f6ed83b65112104270a68(
    value: typing.Optional[GoogleModelArmorFloorsettingFilterConfigSdpSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__122d3e14b58ec61a738e88bfc25ad8286f8d08841a444716099eb5fefe69672b(
    *,
    multi_language_detection: typing.Optional[typing.Union[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6407a85ac57286aa471cd97740d372849296a47c3af7af9bca04d02f2da54a7(
    *,
    enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4983e23544066b67066bbb4cc2be16e16dcf92d6603ecb4400c2a4a27f465de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4a4af63dc081cf806de94ba06533da64d11f96e595593ab1a334a5ed8e7d67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a4126fc988d9e2ed71514ebf99e7b25cde9540516a45c358f6b523f95b7be0(
    value: typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69832828f3c30aaffae6ef113890496249f108687969f2cde4df1f05716acb0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b495b570c6bd1fc015350a52d6c0549d73a86317d9500167c0a6d70bb83182(
    value: typing.Optional[GoogleModelArmorFloorsettingFloorSettingMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a488dd34f5c554cd006e6522ec466d776d98abc899cd935bcda2cd2fb3c9eb8f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc598a9f82d572d4d3cefc83a67fe093c54cf73e9aae9e898f45bd375e79467a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c942417b425cf09510c106b2235d0fb700f92e9e827d0e85dfbf7656d1183e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d964a748128192e5cca5dffba5646aba4a35ce69dce65aff4d2f094ee0082d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7765f656143bd7844d5f9391be4bec43f973b60a84f5969c3036991735d59e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2214a4b00dab5554c86b69c0c5109a3d62251435bbb1604297c6ee57c56400f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleModelArmorFloorsettingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

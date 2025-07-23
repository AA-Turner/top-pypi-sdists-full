r'''
# `google_model_armor_floorsetting`

Refer to the Terraform Registry for docs: [`google_model_armor_floorsetting`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting).
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


class ModelArmorFloorsetting(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsetting",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting google_model_armor_floorsetting}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        filter_config: typing.Union["ModelArmorFloorsettingFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        parent: builtins.str,
        ai_platform_floor_setting: typing.Optional[typing.Union["ModelArmorFloorsettingAiPlatformFloorSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        floor_setting_metadata: typing.Optional[typing.Union["ModelArmorFloorsettingFloorSettingMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ModelArmorFloorsettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting google_model_armor_floorsetting} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_config ModelArmorFloorsetting#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#location ModelArmorFloorsetting#location}
        :param parent: Will be any one of these:. - 'projects/{project}' - 'folders/{folder}' - 'organizations/{organizationId}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#parent ModelArmorFloorsetting#parent}
        :param ai_platform_floor_setting: ai_platform_floor_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#ai_platform_floor_setting ModelArmorFloorsetting#ai_platform_floor_setting}
        :param enable_floor_setting_enforcement: Floor Settings enforcement status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_floor_setting_enforcement ModelArmorFloorsetting#enable_floor_setting_enforcement}
        :param floor_setting_metadata: floor_setting_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#floor_setting_metadata ModelArmorFloorsetting#floor_setting_metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#id ModelArmorFloorsetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integrated_services: List of integrated services for which the floor setting is applicable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#integrated_services ModelArmorFloorsetting#integrated_services}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#timeouts ModelArmorFloorsetting#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070cf6c0414f097fb1bf50eec7235c96f72d479c6a6613bce053bf232cd36eb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ModelArmorFloorsettingConfig(
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
        '''Generates CDKTF code for importing a ModelArmorFloorsetting resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ModelArmorFloorsetting to import.
        :param import_from_id: The id of the existing ModelArmorFloorsetting that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ModelArmorFloorsetting to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78fd88895e29897a6b8c8b0f6c99f540824c1c80ab74625c1b3741ee8b57c09)
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
        :param enable_cloud_logging: If true, log Model Armor filter results to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_cloud_logging ModelArmorFloorsetting#enable_cloud_logging}
        :param inspect_and_block: If true, Model Armor filters will be run in inspect and block mode. Requests that trip Model Armor filters will be blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_and_block ModelArmorFloorsetting#inspect_and_block}
        :param inspect_only: If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_only ModelArmorFloorsetting#inspect_only}
        '''
        value = ModelArmorFloorsettingAiPlatformFloorSetting(
            enable_cloud_logging=enable_cloud_logging,
            inspect_and_block=inspect_and_block,
            inspect_only=inspect_only,
        )

        return typing.cast(None, jsii.invoke(self, "putAiPlatformFloorSetting", [value]))

    @jsii.member(jsii_name="putFilterConfig")
    def put_filter_config(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#malicious_uri_filter_settings ModelArmorFloorsetting#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#pi_and_jailbreak_filter_settings ModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_settings ModelArmorFloorsetting#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#sdp_settings ModelArmorFloorsetting#sdp_settings}
        '''
        value = ModelArmorFloorsettingFilterConfig(
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
        multi_language_detection: typing.Optional[typing.Union["ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#multi_language_detection ModelArmorFloorsetting#multi_language_detection}
        '''
        value = ModelArmorFloorsettingFloorSettingMetadata(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#create ModelArmorFloorsetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#delete ModelArmorFloorsetting#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#update ModelArmorFloorsetting#update}.
        '''
        value = ModelArmorFloorsettingTimeouts(
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
    ) -> "ModelArmorFloorsettingAiPlatformFloorSettingOutputReference":
        return typing.cast("ModelArmorFloorsettingAiPlatformFloorSettingOutputReference", jsii.get(self, "aiPlatformFloorSetting"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="filterConfig")
    def filter_config(self) -> "ModelArmorFloorsettingFilterConfigOutputReference":
        return typing.cast("ModelArmorFloorsettingFilterConfigOutputReference", jsii.get(self, "filterConfig"))

    @builtins.property
    @jsii.member(jsii_name="floorSettingMetadata")
    def floor_setting_metadata(
        self,
    ) -> "ModelArmorFloorsettingFloorSettingMetadataOutputReference":
        return typing.cast("ModelArmorFloorsettingFloorSettingMetadataOutputReference", jsii.get(self, "floorSettingMetadata"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ModelArmorFloorsettingTimeoutsOutputReference":
        return typing.cast("ModelArmorFloorsettingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="aiPlatformFloorSettingInput")
    def ai_platform_floor_setting_input(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingAiPlatformFloorSetting"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingAiPlatformFloorSetting"], jsii.get(self, "aiPlatformFloorSettingInput"))

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
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfig"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfig"], jsii.get(self, "filterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="floorSettingMetadataInput")
    def floor_setting_metadata_input(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFloorSettingMetadata"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingFloorSettingMetadata"], jsii.get(self, "floorSettingMetadataInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ModelArmorFloorsettingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ModelArmorFloorsettingTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__36aa42da37d528a5307342f97ce83ece2d3536b66833b8e0fe6b56fe3254fe74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableFloorSettingEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e5fa357217dc935a63c2b8d4a928006cba7bb7ad23151b1c75f1cc952c4d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integratedServices")
    def integrated_services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "integratedServices"))

    @integrated_services.setter
    def integrated_services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6c885169957402a38bf3df34a32d00586d3d2a5f4f24dfb64f01935a2d689f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integratedServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829abb6f3512f8e55f35907242c1fb62296e6432f9a9db5c06c318b665f3c5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f271abe7853b6adc27d6c174f4ea8e52a08d3446d3876f7352ca2ad8f3cfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingAiPlatformFloorSetting",
    jsii_struct_bases=[],
    name_mapping={
        "enable_cloud_logging": "enableCloudLogging",
        "inspect_and_block": "inspectAndBlock",
        "inspect_only": "inspectOnly",
    },
)
class ModelArmorFloorsettingAiPlatformFloorSetting:
    def __init__(
        self,
        *,
        enable_cloud_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_and_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inspect_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_cloud_logging: If true, log Model Armor filter results to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_cloud_logging ModelArmorFloorsetting#enable_cloud_logging}
        :param inspect_and_block: If true, Model Armor filters will be run in inspect and block mode. Requests that trip Model Armor filters will be blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_and_block ModelArmorFloorsetting#inspect_and_block}
        :param inspect_only: If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_only ModelArmorFloorsetting#inspect_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553d9855ba1dc5b33ca80fe6c7c4663040b9069d254acaa3151d6b8baf0ffa3c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_cloud_logging ModelArmorFloorsetting#enable_cloud_logging}
        '''
        result = self._values.get("enable_cloud_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inspect_and_block(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Model Armor filters will be run in inspect and block mode.

        Requests that trip Model Armor filters will be blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_and_block ModelArmorFloorsetting#inspect_and_block}
        '''
        result = self._values.get("inspect_and_block")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inspect_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, Model Armor filters will be run in inspect only mode. No action will be taken on the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_only ModelArmorFloorsetting#inspect_only}
        '''
        result = self._values.get("inspect_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingAiPlatformFloorSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingAiPlatformFloorSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingAiPlatformFloorSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22e61bc7809435831b0fcf58a22e6d7b31ff98588ef4c99162697e7265b1e0dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10549da34375fc6b07b31dbd9887c87b90b2868813c3aeb25a05db8155f0c694)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50c51107895f71c728d0def619da7098eeb9efd5174657845228273486933bf7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ee107f7a2f446d5d339dfbc6c0be6efb234d6f81e779246a221845392336ab4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ca15bce2533ac5015192e868941d96d07eef6d438726f0c8b6a07f5de6f669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingConfig",
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
class ModelArmorFloorsettingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filter_config: typing.Union["ModelArmorFloorsettingFilterConfig", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        parent: builtins.str,
        ai_platform_floor_setting: typing.Optional[typing.Union[ModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        floor_setting_metadata: typing.Optional[typing.Union["ModelArmorFloorsettingFloorSettingMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ModelArmorFloorsettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filter_config: filter_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_config ModelArmorFloorsetting#filter_config}
        :param location: Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#location ModelArmorFloorsetting#location}
        :param parent: Will be any one of these:. - 'projects/{project}' - 'folders/{folder}' - 'organizations/{organizationId}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#parent ModelArmorFloorsetting#parent}
        :param ai_platform_floor_setting: ai_platform_floor_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#ai_platform_floor_setting ModelArmorFloorsetting#ai_platform_floor_setting}
        :param enable_floor_setting_enforcement: Floor Settings enforcement status. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_floor_setting_enforcement ModelArmorFloorsetting#enable_floor_setting_enforcement}
        :param floor_setting_metadata: floor_setting_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#floor_setting_metadata ModelArmorFloorsetting#floor_setting_metadata}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#id ModelArmorFloorsetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integrated_services: List of integrated services for which the floor setting is applicable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#integrated_services ModelArmorFloorsetting#integrated_services}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#timeouts ModelArmorFloorsetting#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter_config, dict):
            filter_config = ModelArmorFloorsettingFilterConfig(**filter_config)
        if isinstance(ai_platform_floor_setting, dict):
            ai_platform_floor_setting = ModelArmorFloorsettingAiPlatformFloorSetting(**ai_platform_floor_setting)
        if isinstance(floor_setting_metadata, dict):
            floor_setting_metadata = ModelArmorFloorsettingFloorSettingMetadata(**floor_setting_metadata)
        if isinstance(timeouts, dict):
            timeouts = ModelArmorFloorsettingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f49e5924678ecb9fe539921c6a1fb5fae76d15f23affc00807e30b6ed2be4b8)
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
    def filter_config(self) -> "ModelArmorFloorsettingFilterConfig":
        '''filter_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_config ModelArmorFloorsetting#filter_config}
        '''
        result = self._values.get("filter_config")
        assert result is not None, "Required property 'filter_config' is missing"
        return typing.cast("ModelArmorFloorsettingFilterConfig", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. It identifies the resource within its parent collection as described in https://google.aip.dev/122.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#location ModelArmorFloorsetting#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#parent ModelArmorFloorsetting#parent}
        '''
        result = self._values.get("parent")
        assert result is not None, "Required property 'parent' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ai_platform_floor_setting(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting]:
        '''ai_platform_floor_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#ai_platform_floor_setting ModelArmorFloorsetting#ai_platform_floor_setting}
        '''
        result = self._values.get("ai_platform_floor_setting")
        return typing.cast(typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting], result)

    @builtins.property
    def enable_floor_setting_enforcement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Floor Settings enforcement status.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_floor_setting_enforcement ModelArmorFloorsetting#enable_floor_setting_enforcement}
        '''
        result = self._values.get("enable_floor_setting_enforcement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def floor_setting_metadata(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFloorSettingMetadata"]:
        '''floor_setting_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#floor_setting_metadata ModelArmorFloorsetting#floor_setting_metadata}
        '''
        result = self._values.get("floor_setting_metadata")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFloorSettingMetadata"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#id ModelArmorFloorsetting#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integrated_services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of integrated services for which the floor setting is applicable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#integrated_services ModelArmorFloorsetting#integrated_services}
        '''
        result = self._values.get("integrated_services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ModelArmorFloorsettingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#timeouts ModelArmorFloorsetting#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ModelArmorFloorsettingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "malicious_uri_filter_settings": "maliciousUriFilterSettings",
        "pi_and_jailbreak_filter_settings": "piAndJailbreakFilterSettings",
        "rai_settings": "raiSettings",
        "sdp_settings": "sdpSettings",
    },
)
class ModelArmorFloorsettingFilterConfig:
    def __init__(
        self,
        *,
        malicious_uri_filter_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        pi_and_jailbreak_filter_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        rai_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigRaiSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        sdp_settings: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param malicious_uri_filter_settings: malicious_uri_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#malicious_uri_filter_settings ModelArmorFloorsetting#malicious_uri_filter_settings}
        :param pi_and_jailbreak_filter_settings: pi_and_jailbreak_filter_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#pi_and_jailbreak_filter_settings ModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        :param rai_settings: rai_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_settings ModelArmorFloorsetting#rai_settings}
        :param sdp_settings: sdp_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#sdp_settings ModelArmorFloorsetting#sdp_settings}
        '''
        if isinstance(malicious_uri_filter_settings, dict):
            malicious_uri_filter_settings = ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(**malicious_uri_filter_settings)
        if isinstance(pi_and_jailbreak_filter_settings, dict):
            pi_and_jailbreak_filter_settings = ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(**pi_and_jailbreak_filter_settings)
        if isinstance(rai_settings, dict):
            rai_settings = ModelArmorFloorsettingFilterConfigRaiSettings(**rai_settings)
        if isinstance(sdp_settings, dict):
            sdp_settings = ModelArmorFloorsettingFilterConfigSdpSettings(**sdp_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842568d849b7273ba8251507f426c13122ad63d9ee8123dbfb1924c5377ffd9b)
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
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings"]:
        '''malicious_uri_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#malicious_uri_filter_settings ModelArmorFloorsetting#malicious_uri_filter_settings}
        '''
        result = self._values.get("malicious_uri_filter_settings")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings"], result)

    @builtins.property
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"]:
        '''pi_and_jailbreak_filter_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#pi_and_jailbreak_filter_settings ModelArmorFloorsetting#pi_and_jailbreak_filter_settings}
        '''
        result = self._values.get("pi_and_jailbreak_filter_settings")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"], result)

    @builtins.property
    def rai_settings(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigRaiSettings"]:
        '''rai_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_settings ModelArmorFloorsetting#rai_settings}
        '''
        result = self._values.get("rai_settings")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigRaiSettings"], result)

    @builtins.property
    def sdp_settings(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettings"]:
        '''sdp_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#sdp_settings ModelArmorFloorsetting#sdp_settings}
        '''
        result = self._values.get("sdp_settings")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da98c8f0251677d6374d981a78632ea55a3279f69783729e5b93f2baf5e292af)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9164c6fce4086eab81650701755706d8b8be41d0948d897d3d110423c78231a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c74396c49883772a295f7bd93caaf925d9a2b02262fe23054a93adeb8e2605f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836c6968c12b5be56d412f86e6e7409d78924bc7599e930c5c06245cf09c348a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorFloorsettingFilterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c552bc768eaa0f4781bc33899ffdf94e708eafe8a3bf152e206cc7b862761806)
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
        :param filter_enforcement: Tells whether the Malicious URI filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        value = ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings(
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
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#confidence_level ModelArmorFloorsetting#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        value = ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(
            confidence_level=confidence_level, filter_enforcement=filter_enforcement
        )

        return typing.cast(None, jsii.invoke(self, "putPiAndJailbreakFilterSettings", [value]))

    @jsii.member(jsii_name="putRaiSettings")
    def put_rai_settings(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_filters ModelArmorFloorsetting#rai_filters}
        '''
        value = ModelArmorFloorsettingFilterConfigRaiSettings(rai_filters=rai_filters)

        return typing.cast(None, jsii.invoke(self, "putRaiSettings", [value]))

    @jsii.member(jsii_name="putSdpSettings")
    def put_sdp_settings(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#advanced_config ModelArmorFloorsetting#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#basic_config ModelArmorFloorsetting#basic_config}
        '''
        value = ModelArmorFloorsettingFilterConfigSdpSettings(
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
    ) -> ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference:
        return typing.cast(ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference, jsii.get(self, "maliciousUriFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettings")
    def pi_and_jailbreak_filter_settings(
        self,
    ) -> "ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference":
        return typing.cast("ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference", jsii.get(self, "piAndJailbreakFilterSettings"))

    @builtins.property
    @jsii.member(jsii_name="raiSettings")
    def rai_settings(
        self,
    ) -> "ModelArmorFloorsettingFilterConfigRaiSettingsOutputReference":
        return typing.cast("ModelArmorFloorsettingFilterConfigRaiSettingsOutputReference", jsii.get(self, "raiSettings"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettings")
    def sdp_settings(
        self,
    ) -> "ModelArmorFloorsettingFilterConfigSdpSettingsOutputReference":
        return typing.cast("ModelArmorFloorsettingFilterConfigSdpSettingsOutputReference", jsii.get(self, "sdpSettings"))

    @builtins.property
    @jsii.member(jsii_name="maliciousUriFilterSettingsInput")
    def malicious_uri_filter_settings_input(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings], jsii.get(self, "maliciousUriFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="piAndJailbreakFilterSettingsInput")
    def pi_and_jailbreak_filter_settings_input(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings"], jsii.get(self, "piAndJailbreakFilterSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="raiSettingsInput")
    def rai_settings_input(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigRaiSettings"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigRaiSettings"], jsii.get(self, "raiSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="sdpSettingsInput")
    def sdp_settings_input(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettings"]:
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettings"], jsii.get(self, "sdpSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ModelArmorFloorsettingFilterConfig]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e765ace3421485223c6bbe8c76802e07451446a62b68288fe9e3f5bd277c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_level": "confidenceLevel",
        "filter_enforcement": "filterEnforcement",
    },
)
class ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings:
    def __init__(
        self,
        *,
        confidence_level: typing.Optional[builtins.str] = None,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#confidence_level ModelArmorFloorsetting#confidence_level}
        :param filter_enforcement: Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1ec6c6d9ba2acf92c90ba8d954b2576b58ec2eef6b3edcfd3755f6fa48a28a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#confidence_level ModelArmorFloorsetting#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether Prompt injection and Jailbreak filter is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de79c3c86f11053791d652c91e29bbd6e8151724cb30aa31ea02c7015fbd90d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac9fd3f392e0adf2c9509d8c66d6936287f402cc5748e5cf73a1cb915febabb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterEnforcement")
    def filter_enforcement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterEnforcement"))

    @filter_enforcement.setter
    def filter_enforcement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1e711015eece29d8af1e30fdbf1387c4519f9bee0887f49d81c6ae6a2cada7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fe506ae1b29f8f5aa0c5f297bd79f5478ae2289e62f2917b42c41e6d170b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigRaiSettings",
    jsii_struct_bases=[],
    name_mapping={"rai_filters": "raiFilters"},
)
class ModelArmorFloorsettingFilterConfigRaiSettings:
    def __init__(
        self,
        *,
        rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rai_filters: rai_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_filters ModelArmorFloorsetting#rai_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cf3fba8255a72a2d27abaed41d91bb234dcca7d5ca0115134c2dde5cf4992f)
            check_type(argname="argument rai_filters", value=rai_filters, expected_type=type_hints["rai_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rai_filters": rai_filters,
        }

    @builtins.property
    def rai_filters(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]:
        '''rai_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#rai_filters ModelArmorFloorsetting#rai_filters}
        '''
        result = self._values.get("rai_filters")
        assert result is not None, "Required property 'rai_filters' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigRaiSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigRaiSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigRaiSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90d81f24f3e41694d917bc09115fa26a717f5c3331ba5092d6c73ebd59f18724)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRaiFilters")
    def put_rai_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86f9d97c17fde03d2af52b008d11e9be5244b910c666a67142f70c33824a1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRaiFilters", [value]))

    @builtins.property
    @jsii.member(jsii_name="raiFilters")
    def rai_filters(
        self,
    ) -> "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList":
        return typing.cast("ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList", jsii.get(self, "raiFilters"))

    @builtins.property
    @jsii.member(jsii_name="raiFiltersInput")
    def rai_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters"]]], jsii.get(self, "raiFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigRaiSettings]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigRaiSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigRaiSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3559287597068ec22ba533cdee8b6454e06b39431960543ff2623eaa25220d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters",
    jsii_struct_bases=[],
    name_mapping={"filter_type": "filterType", "confidence_level": "confidenceLevel"},
)
class ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters:
    def __init__(
        self,
        *,
        filter_type: builtins.str,
        confidence_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_type: Possible values: SEXUALLY_EXPLICIT HATE_SPEECH HARASSMENT DANGEROUS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_type ModelArmorFloorsetting#filter_type}
        :param confidence_level: Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#confidence_level ModelArmorFloorsetting#confidence_level}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ace306a6c082d31e2d433c5a1cf32114928bc0cf4165fb0fdfdc898a698f8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_type ModelArmorFloorsetting#filter_type}
        '''
        result = self._values.get("filter_type")
        assert result is not None, "Required property 'filter_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confidence_level(self) -> typing.Optional[builtins.str]:
        '''Possible values: LOW_AND_ABOVE MEDIUM_AND_ABOVE HIGH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#confidence_level ModelArmorFloorsetting#confidence_level}
        '''
        result = self._values.get("confidence_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ecc599f7f7af761d7e74aa4e55937d37a37dae9ebd5fd0a17374ce071dad29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba0b0a58a4bd330b5bd04b802657866783534d48f26e6a8a390f31d6e7980f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435e34938378db1bc8bd4764246654266d4d94af3acca0da4a1af0956157ce32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2edf993b2df7997e07dc5db2fb00c4ec438f930c84c14615c2e91c433bd2d94f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d8bdb8c15c61b614bc5450f82f18ce1f3910ceb2347968fd77f289564a4c3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7280140ce74c28b36bd96867bbac986d2dd15a44745937a3ff35ad8eb1aea21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e2fb1cc13a08970523a941c9fc0a92a755f114dac05711ef70fcdf440d05cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__311dfb1565070527b2e6a9e18ee4716bf34a5c55b7c8985199b6a168498c11eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidenceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filterType")
    def filter_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filterType"))

    @filter_type.setter
    def filter_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c268f826dcbb4dcc29ec68bce5badc4d677b2164d953b6fb2564a5596d600a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e28ece702c826224012032d71f79407de99666041bbc745b976be7a936698cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettings",
    jsii_struct_bases=[],
    name_mapping={"advanced_config": "advancedConfig", "basic_config": "basicConfig"},
)
class ModelArmorFloorsettingFilterConfigSdpSettings:
    def __init__(
        self,
        *,
        advanced_config: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        basic_config: typing.Optional[typing.Union["ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param advanced_config: advanced_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#advanced_config ModelArmorFloorsetting#advanced_config}
        :param basic_config: basic_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#basic_config ModelArmorFloorsetting#basic_config}
        '''
        if isinstance(advanced_config, dict):
            advanced_config = ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(**advanced_config)
        if isinstance(basic_config, dict):
            basic_config = ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(**basic_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0966479a18043179dbfd23d668d3c5d0c4e1b30404065fe74c5522849d569ba9)
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
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig"]:
        '''advanced_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#advanced_config ModelArmorFloorsetting#advanced_config}
        '''
        result = self._values.get("advanced_config")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig"], result)

    @builtins.property
    def basic_config(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig"]:
        '''basic_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#basic_config ModelArmorFloorsetting#basic_config}
        '''
        result = self._values.get("basic_config")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigSdpSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deidentify_template": "deidentifyTemplate",
        "inspect_template": "inspectTemplate",
    },
)
class ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig:
    def __init__(
        self,
        *,
        deidentify_template: typing.Optional[builtins.str] = None,
        inspect_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#deidentify_template ModelArmorFloorsetting#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name. If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_template ModelArmorFloorsetting#inspect_template}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc47c979194146e98bac101b6b64ba351785195f19e13d8a39527c261d24e67)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#deidentify_template ModelArmorFloorsetting#deidentify_template}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_template ModelArmorFloorsetting#inspect_template}
        '''
        result = self._values.get("inspect_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec974085abdb5bb24fa4c592a144c145d89a6fe6b3f96d0fafed16739441f7dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afdd81ff68834592e88a9b0525d54e8b9365695d2e11afef1c3a7265f49f3342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deidentifyTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inspectTemplate")
    def inspect_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inspectTemplate"))

    @inspect_template.setter
    def inspect_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cf79e3eca0cb6750eedf046372e218d6fb6bccf63f87c27b87a9e089ca30b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspectTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9680d3a654a0d40c2f000f2c8430da21b3d4097ef985d0924f92a1f82d7c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig",
    jsii_struct_bases=[],
    name_mapping={"filter_enforcement": "filterEnforcement"},
)
class ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig:
    def __init__(
        self,
        *,
        filter_enforcement: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f183051329be7bc9e1a696ce653d069caad6ed7af06424d129f40c6fecb1d7f3)
            check_type(argname="argument filter_enforcement", value=filter_enforcement, expected_type=type_hints["filter_enforcement"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_enforcement is not None:
            self._values["filter_enforcement"] = filter_enforcement

    @builtins.property
    def filter_enforcement(self) -> typing.Optional[builtins.str]:
        '''Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        result = self._values.get("filter_enforcement")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b69451cf2fee902b247392be91a60641ef3849c82536ce4ce0cf411759662e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08987b2b686cbea5cb710e729e2d4cc8987625574d912115cff8f4a6dca576ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterEnforcement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d224c5ea3215f4babf55c95f4bc494d977d9a9b66be3b6b79d3cb372cc6ae2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorFloorsettingFilterConfigSdpSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFilterConfigSdpSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6ed9e58b0f947ea2bc0af9151cd34dc831dbeac302201e1c6e0904700721be0)
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
        :param deidentify_template: Optional Sensitive Data Protection Deidentify template resource name. If provided then DeidentifyContent action is performed during Sanitization using this template and inspect template. The De-identified data will be returned in SdpDeidentifyResult. Note that all info-types present in the deidentify template must be present in inspect template. e.g. 'projects/{project}/locations/{location}/deidentifyTemplates/{deidentify_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#deidentify_template ModelArmorFloorsetting#deidentify_template}
        :param inspect_template: Sensitive Data Protection inspect template resource name. If only inspect template is provided (de-identify template not provided), then Sensitive Data Protection InspectContent action is performed during Sanitization. All Sensitive Data Protection findings identified during inspection will be returned as SdpFinding in SdpInsepctionResult. e.g:- 'projects/{project}/locations/{location}/inspectTemplates/{inspect_template}' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#inspect_template ModelArmorFloorsetting#inspect_template}
        '''
        value = ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig(
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
        :param filter_enforcement: Tells whether the Sensitive Data Protection basic config is enabled or disabled. Possible values: ENABLED DISABLED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#filter_enforcement ModelArmorFloorsetting#filter_enforcement}
        '''
        value = ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig(
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
    ) -> ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference:
        return typing.cast(ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference, jsii.get(self, "advancedConfig"))

    @builtins.property
    @jsii.member(jsii_name="basicConfig")
    def basic_config(
        self,
    ) -> ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference:
        return typing.cast(ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference, jsii.get(self, "basicConfig"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfigInput")
    def advanced_config_input(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig], jsii.get(self, "advancedConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="basicConfigInput")
    def basic_config_input(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig], jsii.get(self, "basicConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettings]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe9120e370902a05c1f43a0e40e8d48a58b110552dd599a9792e27f636fabcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFloorSettingMetadata",
    jsii_struct_bases=[],
    name_mapping={"multi_language_detection": "multiLanguageDetection"},
)
class ModelArmorFloorsettingFloorSettingMetadata:
    def __init__(
        self,
        *,
        multi_language_detection: typing.Optional[typing.Union["ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param multi_language_detection: multi_language_detection block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#multi_language_detection ModelArmorFloorsetting#multi_language_detection}
        '''
        if isinstance(multi_language_detection, dict):
            multi_language_detection = ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(**multi_language_detection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780b19bba2d02ca368d552e010a6ddd95357275546ac88b91aa5fcb507117174)
            check_type(argname="argument multi_language_detection", value=multi_language_detection, expected_type=type_hints["multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if multi_language_detection is not None:
            self._values["multi_language_detection"] = multi_language_detection

    @builtins.property
    def multi_language_detection(
        self,
    ) -> typing.Optional["ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection"]:
        '''multi_language_detection block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#multi_language_detection ModelArmorFloorsetting#multi_language_detection}
        '''
        result = self._values.get("multi_language_detection")
        return typing.cast(typing.Optional["ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFloorSettingMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection",
    jsii_struct_bases=[],
    name_mapping={"enable_multi_language_detection": "enableMultiLanguageDetection"},
)
class ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection:
    def __init__(
        self,
        *,
        enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_multi_language_detection ModelArmorFloorsetting#enable_multi_language_detection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe17355f4f17145924e41e6ec3936526a895edabb2df1a34c78f14085203d05)
            check_type(argname="argument enable_multi_language_detection", value=enable_multi_language_detection, expected_type=type_hints["enable_multi_language_detection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_multi_language_detection": enable_multi_language_detection,
        }

    @builtins.property
    def enable_multi_language_detection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''If true, multi language detection will be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_multi_language_detection ModelArmorFloorsetting#enable_multi_language_detection}
        '''
        result = self._values.get("enable_multi_language_detection")
        assert result is not None, "Required property 'enable_multi_language_detection' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__589d848e0933b6e832f841df307980fb2dcfce3156e3ae329af8d92878fd3f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9274400670f491ae8242db9fddeb814b9f1df03129985c542c2ad46a76ba28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableMultiLanguageDetection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cea1fb6be9dbe8570866f3d97eca5f9d897ac2e8da2cccd552a62d0775fc2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ModelArmorFloorsettingFloorSettingMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingFloorSettingMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f0b699d25c74cf5ff99e8fb93c705af2513601de904ddeeec37038eda3c7f08)
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
        :param enable_multi_language_detection: If true, multi language detection will be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#enable_multi_language_detection ModelArmorFloorsetting#enable_multi_language_detection}
        '''
        value = ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection(
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
    ) -> ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference:
        return typing.cast(ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference, jsii.get(self, "multiLanguageDetection"))

    @builtins.property
    @jsii.member(jsii_name="multiLanguageDetectionInput")
    def multi_language_detection_input(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection], jsii.get(self, "multiLanguageDetectionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ModelArmorFloorsettingFloorSettingMetadata]:
        return typing.cast(typing.Optional[ModelArmorFloorsettingFloorSettingMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ModelArmorFloorsettingFloorSettingMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4d0e12203a496664d9a43179ec4b620f1f919cc6fb69bf397baf0bf717abdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ModelArmorFloorsettingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#create ModelArmorFloorsetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#delete ModelArmorFloorsetting#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#update ModelArmorFloorsetting#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e5d223dfd4d77fbf4b46eab537ec5028078ccfe38979ef4357c4dd0997c1cc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#create ModelArmorFloorsetting#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#delete ModelArmorFloorsetting#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/model_armor_floorsetting#update ModelArmorFloorsetting#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelArmorFloorsettingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ModelArmorFloorsettingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.modelArmorFloorsetting.ModelArmorFloorsettingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b2ca8696d50c42ced092ff5694b77708b9abfe8643766f7cffa6cc928b5227f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5089905a4f3950622e92b8ef0a9c2991846bf06939c9162f030c7714478a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03105761e7b0d69ce19804b4ad6dcf3afce08323c9bb9c5a53c586b59d4d8645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5427dc93ef1009f4bfbde75f92e5649abf95473c58b1e6ab270ce076f1133182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a35d85526a12d5a2e4ce08d401f21915141e2ac0e4082b355fea8be778d0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ModelArmorFloorsetting",
    "ModelArmorFloorsettingAiPlatformFloorSetting",
    "ModelArmorFloorsettingAiPlatformFloorSettingOutputReference",
    "ModelArmorFloorsettingConfig",
    "ModelArmorFloorsettingFilterConfig",
    "ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings",
    "ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettingsOutputReference",
    "ModelArmorFloorsettingFilterConfigOutputReference",
    "ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings",
    "ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettingsOutputReference",
    "ModelArmorFloorsettingFilterConfigRaiSettings",
    "ModelArmorFloorsettingFilterConfigRaiSettingsOutputReference",
    "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters",
    "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersList",
    "ModelArmorFloorsettingFilterConfigRaiSettingsRaiFiltersOutputReference",
    "ModelArmorFloorsettingFilterConfigSdpSettings",
    "ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig",
    "ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfigOutputReference",
    "ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig",
    "ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfigOutputReference",
    "ModelArmorFloorsettingFilterConfigSdpSettingsOutputReference",
    "ModelArmorFloorsettingFloorSettingMetadata",
    "ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection",
    "ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetectionOutputReference",
    "ModelArmorFloorsettingFloorSettingMetadataOutputReference",
    "ModelArmorFloorsettingTimeouts",
    "ModelArmorFloorsettingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__070cf6c0414f097fb1bf50eec7235c96f72d479c6a6613bce053bf232cd36eb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    filter_config: typing.Union[ModelArmorFloorsettingFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    parent: builtins.str,
    ai_platform_floor_setting: typing.Optional[typing.Union[ModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    floor_setting_metadata: typing.Optional[typing.Union[ModelArmorFloorsettingFloorSettingMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ModelArmorFloorsettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e78fd88895e29897a6b8c8b0f6c99f540824c1c80ab74625c1b3741ee8b57c09(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36aa42da37d528a5307342f97ce83ece2d3536b66833b8e0fe6b56fe3254fe74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e5fa357217dc935a63c2b8d4a928006cba7bb7ad23151b1c75f1cc952c4d37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6c885169957402a38bf3df34a32d00586d3d2a5f4f24dfb64f01935a2d689f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829abb6f3512f8e55f35907242c1fb62296e6432f9a9db5c06c318b665f3c5ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f271abe7853b6adc27d6c174f4ea8e52a08d3446d3876f7352ca2ad8f3cfcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553d9855ba1dc5b33ca80fe6c7c4663040b9069d254acaa3151d6b8baf0ffa3c(
    *,
    enable_cloud_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inspect_and_block: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inspect_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e61bc7809435831b0fcf58a22e6d7b31ff98588ef4c99162697e7265b1e0dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10549da34375fc6b07b31dbd9887c87b90b2868813c3aeb25a05db8155f0c694(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c51107895f71c728d0def619da7098eeb9efd5174657845228273486933bf7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee107f7a2f446d5d339dfbc6c0be6efb234d6f81e779246a221845392336ab4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ca15bce2533ac5015192e868941d96d07eef6d438726f0c8b6a07f5de6f669(
    value: typing.Optional[ModelArmorFloorsettingAiPlatformFloorSetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f49e5924678ecb9fe539921c6a1fb5fae76d15f23affc00807e30b6ed2be4b8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filter_config: typing.Union[ModelArmorFloorsettingFilterConfig, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    parent: builtins.str,
    ai_platform_floor_setting: typing.Optional[typing.Union[ModelArmorFloorsettingAiPlatformFloorSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_floor_setting_enforcement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    floor_setting_metadata: typing.Optional[typing.Union[ModelArmorFloorsettingFloorSettingMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    integrated_services: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ModelArmorFloorsettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842568d849b7273ba8251507f426c13122ad63d9ee8123dbfb1924c5377ffd9b(
    *,
    malicious_uri_filter_settings: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    pi_and_jailbreak_filter_settings: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    rai_settings: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigRaiSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    sdp_settings: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigSdpSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da98c8f0251677d6374d981a78632ea55a3279f69783729e5b93f2baf5e292af(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9164c6fce4086eab81650701755706d8b8be41d0948d897d3d110423c78231a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c74396c49883772a295f7bd93caaf925d9a2b02262fe23054a93adeb8e2605f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c6968c12b5be56d412f86e6e7409d78924bc7599e930c5c06245cf09c348a(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigMaliciousUriFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c552bc768eaa0f4781bc33899ffdf94e708eafe8a3bf152e206cc7b862761806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e765ace3421485223c6bbe8c76802e07451446a62b68288fe9e3f5bd277c3f(
    value: typing.Optional[ModelArmorFloorsettingFilterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1ec6c6d9ba2acf92c90ba8d954b2576b58ec2eef6b3edcfd3755f6fa48a28a(
    *,
    confidence_level: typing.Optional[builtins.str] = None,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de79c3c86f11053791d652c91e29bbd6e8151724cb30aa31ea02c7015fbd90d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9fd3f392e0adf2c9509d8c66d6936287f402cc5748e5cf73a1cb915febabb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1e711015eece29d8af1e30fdbf1387c4519f9bee0887f49d81c6ae6a2cada7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fe506ae1b29f8f5aa0c5f297bd79f5478ae2289e62f2917b42c41e6d170b4e(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigPiAndJailbreakFilterSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cf3fba8255a72a2d27abaed41d91bb234dcca7d5ca0115134c2dde5cf4992f(
    *,
    rai_filters: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d81f24f3e41694d917bc09115fa26a717f5c3331ba5092d6c73ebd59f18724(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86f9d97c17fde03d2af52b008d11e9be5244b910c666a67142f70c33824a1bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3559287597068ec22ba533cdee8b6454e06b39431960543ff2623eaa25220d(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigRaiSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ace306a6c082d31e2d433c5a1cf32114928bc0cf4165fb0fdfdc898a698f8b(
    *,
    filter_type: builtins.str,
    confidence_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ecc599f7f7af761d7e74aa4e55937d37a37dae9ebd5fd0a17374ce071dad29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba0b0a58a4bd330b5bd04b802657866783534d48f26e6a8a390f31d6e7980f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435e34938378db1bc8bd4764246654266d4d94af3acca0da4a1af0956157ce32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edf993b2df7997e07dc5db2fb00c4ec438f930c84c14615c2e91c433bd2d94f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8bdb8c15c61b614bc5450f82f18ce1f3910ceb2347968fd77f289564a4c3b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7280140ce74c28b36bd96867bbac986d2dd15a44745937a3ff35ad8eb1aea21d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e2fb1cc13a08970523a941c9fc0a92a755f114dac05711ef70fcdf440d05cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311dfb1565070527b2e6a9e18ee4716bf34a5c55b7c8985199b6a168498c11eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c268f826dcbb4dcc29ec68bce5badc4d677b2164d953b6fb2564a5596d600a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e28ece702c826224012032d71f79407de99666041bbc745b976be7a936698cc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingFilterConfigRaiSettingsRaiFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0966479a18043179dbfd23d668d3c5d0c4e1b30404065fe74c5522849d569ba9(
    *,
    advanced_config: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    basic_config: typing.Optional[typing.Union[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc47c979194146e98bac101b6b64ba351785195f19e13d8a39527c261d24e67(
    *,
    deidentify_template: typing.Optional[builtins.str] = None,
    inspect_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec974085abdb5bb24fa4c592a144c145d89a6fe6b3f96d0fafed16739441f7dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdd81ff68834592e88a9b0525d54e8b9365695d2e11afef1c3a7265f49f3342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cf79e3eca0cb6750eedf046372e218d6fb6bccf63f87c27b87a9e089ca30b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9680d3a654a0d40c2f000f2c8430da21b3d4097ef985d0924f92a1f82d7c3c(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsAdvancedConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f183051329be7bc9e1a696ce653d069caad6ed7af06424d129f40c6fecb1d7f3(
    *,
    filter_enforcement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b69451cf2fee902b247392be91a60641ef3849c82536ce4ce0cf411759662e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08987b2b686cbea5cb710e729e2d4cc8987625574d912115cff8f4a6dca576ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d224c5ea3215f4babf55c95f4bc494d977d9a9b66be3b6b79d3cb372cc6ae2fd(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettingsBasicConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ed9e58b0f947ea2bc0af9151cd34dc831dbeac302201e1c6e0904700721be0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe9120e370902a05c1f43a0e40e8d48a58b110552dd599a9792e27f636fabcd(
    value: typing.Optional[ModelArmorFloorsettingFilterConfigSdpSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780b19bba2d02ca368d552e010a6ddd95357275546ac88b91aa5fcb507117174(
    *,
    multi_language_detection: typing.Optional[typing.Union[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe17355f4f17145924e41e6ec3936526a895edabb2df1a34c78f14085203d05(
    *,
    enable_multi_language_detection: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589d848e0933b6e832f841df307980fb2dcfce3156e3ae329af8d92878fd3f55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9274400670f491ae8242db9fddeb814b9f1df03129985c542c2ad46a76ba28(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cea1fb6be9dbe8570866f3d97eca5f9d897ac2e8da2cccd552a62d0775fc2a(
    value: typing.Optional[ModelArmorFloorsettingFloorSettingMetadataMultiLanguageDetection],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0b699d25c74cf5ff99e8fb93c705af2513601de904ddeeec37038eda3c7f08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4d0e12203a496664d9a43179ec4b620f1f919cc6fb69bf397baf0bf717abdd(
    value: typing.Optional[ModelArmorFloorsettingFloorSettingMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e5d223dfd4d77fbf4b46eab537ec5028078ccfe38979ef4357c4dd0997c1cc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2ca8696d50c42ced092ff5694b77708b9abfe8643766f7cffa6cc928b5227f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5089905a4f3950622e92b8ef0a9c2991846bf06939c9162f030c7714478a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03105761e7b0d69ce19804b4ad6dcf3afce08323c9bb9c5a53c586b59d4d8645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5427dc93ef1009f4bfbde75f92e5649abf95473c58b1e6ab270ce076f1133182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a35d85526a12d5a2e4ce08d401f21915141e2ac0e4082b355fea8be778d0f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ModelArmorFloorsettingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

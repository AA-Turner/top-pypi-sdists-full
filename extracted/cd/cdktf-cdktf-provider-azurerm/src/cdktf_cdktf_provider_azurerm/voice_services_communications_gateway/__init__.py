r'''
# `azurerm_voice_services_communications_gateway`

Refer to the Terraform Registry for docs: [`azurerm_voice_services_communications_gateway`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway).
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


class VoiceServicesCommunicationsGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway azurerm_voice_services_communications_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        codecs: builtins.str,
        connectivity: builtins.str,
        e911_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        resource_group_name: builtins.str,
        service_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VoiceServicesCommunicationsGatewayServiceLocation", typing.Dict[builtins.str, typing.Any]]]],
        api_bridge: typing.Optional[builtins.str] = None,
        auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
        emergency_dial_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        microsoft_teams_voicemail_pilot_number: typing.Optional[builtins.str] = None,
        on_prem_mcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VoiceServicesCommunicationsGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway azurerm_voice_services_communications_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param codecs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#codecs VoiceServicesCommunicationsGateway#codecs}.
        :param connectivity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#connectivity VoiceServicesCommunicationsGateway#connectivity}.
        :param e911_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#e911_type VoiceServicesCommunicationsGateway#e911_type}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#location VoiceServicesCommunicationsGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#name VoiceServicesCommunicationsGateway#name}.
        :param platforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#platforms VoiceServicesCommunicationsGateway#platforms}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#resource_group_name VoiceServicesCommunicationsGateway#resource_group_name}.
        :param service_location: service_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#service_location VoiceServicesCommunicationsGateway#service_location}
        :param api_bridge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#api_bridge VoiceServicesCommunicationsGateway#api_bridge}.
        :param auto_generated_domain_name_label_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#auto_generated_domain_name_label_scope VoiceServicesCommunicationsGateway#auto_generated_domain_name_label_scope}.
        :param emergency_dial_strings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#emergency_dial_strings VoiceServicesCommunicationsGateway#emergency_dial_strings}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#id VoiceServicesCommunicationsGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param microsoft_teams_voicemail_pilot_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#microsoft_teams_voicemail_pilot_number VoiceServicesCommunicationsGateway#microsoft_teams_voicemail_pilot_number}.
        :param on_prem_mcp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#on_prem_mcp_enabled VoiceServicesCommunicationsGateway#on_prem_mcp_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#tags VoiceServicesCommunicationsGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#timeouts VoiceServicesCommunicationsGateway#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cc1871bf4fffd270cbb3b45388026b872fbfdf2f881d411b3a95dc5fd4475e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VoiceServicesCommunicationsGatewayConfig(
            codecs=codecs,
            connectivity=connectivity,
            e911_type=e911_type,
            location=location,
            name=name,
            platforms=platforms,
            resource_group_name=resource_group_name,
            service_location=service_location,
            api_bridge=api_bridge,
            auto_generated_domain_name_label_scope=auto_generated_domain_name_label_scope,
            emergency_dial_strings=emergency_dial_strings,
            id=id,
            microsoft_teams_voicemail_pilot_number=microsoft_teams_voicemail_pilot_number,
            on_prem_mcp_enabled=on_prem_mcp_enabled,
            tags=tags,
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
        '''Generates CDKTF code for importing a VoiceServicesCommunicationsGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VoiceServicesCommunicationsGateway to import.
        :param import_from_id: The id of the existing VoiceServicesCommunicationsGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VoiceServicesCommunicationsGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62569204060a6df2d66a4f4d8abc43ca7924b0e368d1fceb321f470e571a542a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServiceLocation")
    def put_service_location(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VoiceServicesCommunicationsGatewayServiceLocation", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f149c9be5a82ca7c092d344739eb6ef6b1515fe61173354742c8fdb00a2551a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceLocation", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#create VoiceServicesCommunicationsGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#delete VoiceServicesCommunicationsGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#read VoiceServicesCommunicationsGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#update VoiceServicesCommunicationsGateway#update}.
        '''
        value = VoiceServicesCommunicationsGatewayTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiBridge")
    def reset_api_bridge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiBridge", []))

    @jsii.member(jsii_name="resetAutoGeneratedDomainNameLabelScope")
    def reset_auto_generated_domain_name_label_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGeneratedDomainNameLabelScope", []))

    @jsii.member(jsii_name="resetEmergencyDialStrings")
    def reset_emergency_dial_strings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmergencyDialStrings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMicrosoftTeamsVoicemailPilotNumber")
    def reset_microsoft_teams_voicemail_pilot_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftTeamsVoicemailPilotNumber", []))

    @jsii.member(jsii_name="resetOnPremMcpEnabled")
    def reset_on_prem_mcp_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnPremMcpEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="serviceLocation")
    def service_location(
        self,
    ) -> "VoiceServicesCommunicationsGatewayServiceLocationList":
        return typing.cast("VoiceServicesCommunicationsGatewayServiceLocationList", jsii.get(self, "serviceLocation"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VoiceServicesCommunicationsGatewayTimeoutsOutputReference":
        return typing.cast("VoiceServicesCommunicationsGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiBridgeInput")
    def api_bridge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiBridgeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGeneratedDomainNameLabelScopeInput")
    def auto_generated_domain_name_label_scope_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoGeneratedDomainNameLabelScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="codecsInput")
    def codecs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codecsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectivityInput")
    def connectivity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectivityInput"))

    @builtins.property
    @jsii.member(jsii_name="e911TypeInput")
    def e911_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "e911TypeInput"))

    @builtins.property
    @jsii.member(jsii_name="emergencyDialStringsInput")
    def emergency_dial_strings_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emergencyDialStringsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftTeamsVoicemailPilotNumberInput")
    def microsoft_teams_voicemail_pilot_number_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microsoftTeamsVoicemailPilotNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="onPremMcpEnabledInput")
    def on_prem_mcp_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onPremMcpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="platformsInput")
    def platforms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "platformsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLocationInput")
    def service_location_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VoiceServicesCommunicationsGatewayServiceLocation"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VoiceServicesCommunicationsGatewayServiceLocation"]]], jsii.get(self, "serviceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VoiceServicesCommunicationsGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VoiceServicesCommunicationsGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiBridge")
    def api_bridge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiBridge"))

    @api_bridge.setter
    def api_bridge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a7d3ba253dade42efb8ff45b1fae477d11cecb4c322c4c7e499b8e8475f270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiBridge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoGeneratedDomainNameLabelScope")
    def auto_generated_domain_name_label_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoGeneratedDomainNameLabelScope"))

    @auto_generated_domain_name_label_scope.setter
    def auto_generated_domain_name_label_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c30b91c989012b3de982ad568e8f9a9980e53daeaa8bdd724ac2a66eae31e78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGeneratedDomainNameLabelScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codecs")
    def codecs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codecs"))

    @codecs.setter
    def codecs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b38ae086588f0ab136e7e7afc0feacff3a9ae199addfc72974b69a0c36c717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectivity")
    def connectivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectivity"))

    @connectivity.setter
    def connectivity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ac6a5e76df744573c6f518af011689490e5be984fa22836ddc7f9149e5956e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="e911Type")
    def e911_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "e911Type"))

    @e911_type.setter
    def e911_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c6524044bd8133e749e6bdf35b474161ba9f8475da35742b62675546680b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "e911Type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emergencyDialStrings")
    def emergency_dial_strings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emergencyDialStrings"))

    @emergency_dial_strings.setter
    def emergency_dial_strings(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046ee6e2491893d8a47a134c8bde0568e24f4f8c4b79159f9d95a6dd1aac1ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emergencyDialStrings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ba49cfd242a11e6ea037050984d4070c4f12efdd7986209fa442f464105612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b795b9146b3a490c830e7cd668d933abcff7cc51cbc67ad5d200e7677cb9078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftTeamsVoicemailPilotNumber")
    def microsoft_teams_voicemail_pilot_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microsoftTeamsVoicemailPilotNumber"))

    @microsoft_teams_voicemail_pilot_number.setter
    def microsoft_teams_voicemail_pilot_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525869fa6e0622d592affcbc2d6859720eceed83cf70fc729c0520e6e5a4efee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftTeamsVoicemailPilotNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8280b2e0467ea1fa6a3287a789a0bce47e0048ac4ec8c85d99471ac9b6118b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onPremMcpEnabled")
    def on_prem_mcp_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onPremMcpEnabled"))

    @on_prem_mcp_enabled.setter
    def on_prem_mcp_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c854151dab2dfc4ea1b9532b5330a6a3fc2763863232d3fb0e28912436ae8e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremMcpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platforms")
    def platforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "platforms"))

    @platforms.setter
    def platforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaa5613d303c8a5ee47a3a17f314ee78e6e3fcdb7c10d30df0257cdedf05099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179f5e694041ae7857409532c7cd1797d10fce2cb802b18162853b021eb81cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff9aeb05bad48c1b7c2f38475ba033cbb04c36a53ea7ef18ec8c6d0c8cdb9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "codecs": "codecs",
        "connectivity": "connectivity",
        "e911_type": "e911Type",
        "location": "location",
        "name": "name",
        "platforms": "platforms",
        "resource_group_name": "resourceGroupName",
        "service_location": "serviceLocation",
        "api_bridge": "apiBridge",
        "auto_generated_domain_name_label_scope": "autoGeneratedDomainNameLabelScope",
        "emergency_dial_strings": "emergencyDialStrings",
        "id": "id",
        "microsoft_teams_voicemail_pilot_number": "microsoftTeamsVoicemailPilotNumber",
        "on_prem_mcp_enabled": "onPremMcpEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class VoiceServicesCommunicationsGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        codecs: builtins.str,
        connectivity: builtins.str,
        e911_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        resource_group_name: builtins.str,
        service_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VoiceServicesCommunicationsGatewayServiceLocation", typing.Dict[builtins.str, typing.Any]]]],
        api_bridge: typing.Optional[builtins.str] = None,
        auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
        emergency_dial_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        microsoft_teams_voicemail_pilot_number: typing.Optional[builtins.str] = None,
        on_prem_mcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VoiceServicesCommunicationsGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param codecs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#codecs VoiceServicesCommunicationsGateway#codecs}.
        :param connectivity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#connectivity VoiceServicesCommunicationsGateway#connectivity}.
        :param e911_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#e911_type VoiceServicesCommunicationsGateway#e911_type}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#location VoiceServicesCommunicationsGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#name VoiceServicesCommunicationsGateway#name}.
        :param platforms: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#platforms VoiceServicesCommunicationsGateway#platforms}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#resource_group_name VoiceServicesCommunicationsGateway#resource_group_name}.
        :param service_location: service_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#service_location VoiceServicesCommunicationsGateway#service_location}
        :param api_bridge: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#api_bridge VoiceServicesCommunicationsGateway#api_bridge}.
        :param auto_generated_domain_name_label_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#auto_generated_domain_name_label_scope VoiceServicesCommunicationsGateway#auto_generated_domain_name_label_scope}.
        :param emergency_dial_strings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#emergency_dial_strings VoiceServicesCommunicationsGateway#emergency_dial_strings}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#id VoiceServicesCommunicationsGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param microsoft_teams_voicemail_pilot_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#microsoft_teams_voicemail_pilot_number VoiceServicesCommunicationsGateway#microsoft_teams_voicemail_pilot_number}.
        :param on_prem_mcp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#on_prem_mcp_enabled VoiceServicesCommunicationsGateway#on_prem_mcp_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#tags VoiceServicesCommunicationsGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#timeouts VoiceServicesCommunicationsGateway#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VoiceServicesCommunicationsGatewayTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cea39d21f5c1cf69b7d987e981eef68f7f6b4ea42c01b2ed198133f024b581b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument codecs", value=codecs, expected_type=type_hints["codecs"])
            check_type(argname="argument connectivity", value=connectivity, expected_type=type_hints["connectivity"])
            check_type(argname="argument e911_type", value=e911_type, expected_type=type_hints["e911_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument service_location", value=service_location, expected_type=type_hints["service_location"])
            check_type(argname="argument api_bridge", value=api_bridge, expected_type=type_hints["api_bridge"])
            check_type(argname="argument auto_generated_domain_name_label_scope", value=auto_generated_domain_name_label_scope, expected_type=type_hints["auto_generated_domain_name_label_scope"])
            check_type(argname="argument emergency_dial_strings", value=emergency_dial_strings, expected_type=type_hints["emergency_dial_strings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument microsoft_teams_voicemail_pilot_number", value=microsoft_teams_voicemail_pilot_number, expected_type=type_hints["microsoft_teams_voicemail_pilot_number"])
            check_type(argname="argument on_prem_mcp_enabled", value=on_prem_mcp_enabled, expected_type=type_hints["on_prem_mcp_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "codecs": codecs,
            "connectivity": connectivity,
            "e911_type": e911_type,
            "location": location,
            "name": name,
            "platforms": platforms,
            "resource_group_name": resource_group_name,
            "service_location": service_location,
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
        if api_bridge is not None:
            self._values["api_bridge"] = api_bridge
        if auto_generated_domain_name_label_scope is not None:
            self._values["auto_generated_domain_name_label_scope"] = auto_generated_domain_name_label_scope
        if emergency_dial_strings is not None:
            self._values["emergency_dial_strings"] = emergency_dial_strings
        if id is not None:
            self._values["id"] = id
        if microsoft_teams_voicemail_pilot_number is not None:
            self._values["microsoft_teams_voicemail_pilot_number"] = microsoft_teams_voicemail_pilot_number
        if on_prem_mcp_enabled is not None:
            self._values["on_prem_mcp_enabled"] = on_prem_mcp_enabled
        if tags is not None:
            self._values["tags"] = tags
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
    def codecs(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#codecs VoiceServicesCommunicationsGateway#codecs}.'''
        result = self._values.get("codecs")
        assert result is not None, "Required property 'codecs' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connectivity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#connectivity VoiceServicesCommunicationsGateway#connectivity}.'''
        result = self._values.get("connectivity")
        assert result is not None, "Required property 'connectivity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def e911_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#e911_type VoiceServicesCommunicationsGateway#e911_type}.'''
        result = self._values.get("e911_type")
        assert result is not None, "Required property 'e911_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#location VoiceServicesCommunicationsGateway#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#name VoiceServicesCommunicationsGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platforms(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#platforms VoiceServicesCommunicationsGateway#platforms}.'''
        result = self._values.get("platforms")
        assert result is not None, "Required property 'platforms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#resource_group_name VoiceServicesCommunicationsGateway#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_location(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VoiceServicesCommunicationsGatewayServiceLocation"]]:
        '''service_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#service_location VoiceServicesCommunicationsGateway#service_location}
        '''
        result = self._values.get("service_location")
        assert result is not None, "Required property 'service_location' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VoiceServicesCommunicationsGatewayServiceLocation"]], result)

    @builtins.property
    def api_bridge(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#api_bridge VoiceServicesCommunicationsGateway#api_bridge}.'''
        result = self._values.get("api_bridge")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_generated_domain_name_label_scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#auto_generated_domain_name_label_scope VoiceServicesCommunicationsGateway#auto_generated_domain_name_label_scope}.'''
        result = self._values.get("auto_generated_domain_name_label_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emergency_dial_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#emergency_dial_strings VoiceServicesCommunicationsGateway#emergency_dial_strings}.'''
        result = self._values.get("emergency_dial_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#id VoiceServicesCommunicationsGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_teams_voicemail_pilot_number(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#microsoft_teams_voicemail_pilot_number VoiceServicesCommunicationsGateway#microsoft_teams_voicemail_pilot_number}.'''
        result = self._values.get("microsoft_teams_voicemail_pilot_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_prem_mcp_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#on_prem_mcp_enabled VoiceServicesCommunicationsGateway#on_prem_mcp_enabled}.'''
        result = self._values.get("on_prem_mcp_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#tags VoiceServicesCommunicationsGateway#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VoiceServicesCommunicationsGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#timeouts VoiceServicesCommunicationsGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VoiceServicesCommunicationsGatewayTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceServicesCommunicationsGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayServiceLocation",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "operator_addresses": "operatorAddresses",
        "allowed_media_source_address_prefixes": "allowedMediaSourceAddressPrefixes",
        "allowed_signaling_source_address_prefixes": "allowedSignalingSourceAddressPrefixes",
        "esrp_addresses": "esrpAddresses",
    },
)
class VoiceServicesCommunicationsGatewayServiceLocation:
    def __init__(
        self,
        *,
        location: builtins.str,
        operator_addresses: typing.Sequence[builtins.str],
        allowed_media_source_address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_signaling_source_address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        esrp_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#location VoiceServicesCommunicationsGateway#location}.
        :param operator_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#operator_addresses VoiceServicesCommunicationsGateway#operator_addresses}.
        :param allowed_media_source_address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#allowed_media_source_address_prefixes VoiceServicesCommunicationsGateway#allowed_media_source_address_prefixes}.
        :param allowed_signaling_source_address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#allowed_signaling_source_address_prefixes VoiceServicesCommunicationsGateway#allowed_signaling_source_address_prefixes}.
        :param esrp_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#esrp_addresses VoiceServicesCommunicationsGateway#esrp_addresses}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aeb7a98c8fa64e11cb61f6f0572e607c8e95cde83c5bd6d2c7c4521bb9f33b5)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument operator_addresses", value=operator_addresses, expected_type=type_hints["operator_addresses"])
            check_type(argname="argument allowed_media_source_address_prefixes", value=allowed_media_source_address_prefixes, expected_type=type_hints["allowed_media_source_address_prefixes"])
            check_type(argname="argument allowed_signaling_source_address_prefixes", value=allowed_signaling_source_address_prefixes, expected_type=type_hints["allowed_signaling_source_address_prefixes"])
            check_type(argname="argument esrp_addresses", value=esrp_addresses, expected_type=type_hints["esrp_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "operator_addresses": operator_addresses,
        }
        if allowed_media_source_address_prefixes is not None:
            self._values["allowed_media_source_address_prefixes"] = allowed_media_source_address_prefixes
        if allowed_signaling_source_address_prefixes is not None:
            self._values["allowed_signaling_source_address_prefixes"] = allowed_signaling_source_address_prefixes
        if esrp_addresses is not None:
            self._values["esrp_addresses"] = esrp_addresses

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#location VoiceServicesCommunicationsGateway#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator_addresses(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#operator_addresses VoiceServicesCommunicationsGateway#operator_addresses}.'''
        result = self._values.get("operator_addresses")
        assert result is not None, "Required property 'operator_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_media_source_address_prefixes(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#allowed_media_source_address_prefixes VoiceServicesCommunicationsGateway#allowed_media_source_address_prefixes}.'''
        result = self._values.get("allowed_media_source_address_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_signaling_source_address_prefixes(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#allowed_signaling_source_address_prefixes VoiceServicesCommunicationsGateway#allowed_signaling_source_address_prefixes}.'''
        result = self._values.get("allowed_signaling_source_address_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def esrp_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#esrp_addresses VoiceServicesCommunicationsGateway#esrp_addresses}.'''
        result = self._values.get("esrp_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceServicesCommunicationsGatewayServiceLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VoiceServicesCommunicationsGatewayServiceLocationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayServiceLocationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b851bb427a15cd8809ec225666a88b8b795f114aace7972a625fb389ae10f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VoiceServicesCommunicationsGatewayServiceLocationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4babc24d0d4c329beeb4de7e139d52aa34b38690ac8feadcfcf467a435ce7d69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VoiceServicesCommunicationsGatewayServiceLocationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c9e0cd59c7751e422373492c59bd1340841683c4af0fc1ed547206d6186bd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__151553e0de8128a3fb00fd47fb097ab4d90c2d2d608c92d9bb6726f9d631bb49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__913f8daeb9fcb0a4759b55c4a728de4982981a1ebf5bb1d68820aacd589f7281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VoiceServicesCommunicationsGatewayServiceLocation]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VoiceServicesCommunicationsGatewayServiceLocation]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VoiceServicesCommunicationsGatewayServiceLocation]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc41dacbd3897b5dad65976501e54603116fbbca73f4b101feec3ab8b7f27491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VoiceServicesCommunicationsGatewayServiceLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayServiceLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6262a671bff46aa439d5d61236883a4c8eb051ab010d587f270e361c8e33e18a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedMediaSourceAddressPrefixes")
    def reset_allowed_media_source_address_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedMediaSourceAddressPrefixes", []))

    @jsii.member(jsii_name="resetAllowedSignalingSourceAddressPrefixes")
    def reset_allowed_signaling_source_address_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedSignalingSourceAddressPrefixes", []))

    @jsii.member(jsii_name="resetEsrpAddresses")
    def reset_esrp_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEsrpAddresses", []))

    @builtins.property
    @jsii.member(jsii_name="allowedMediaSourceAddressPrefixesInput")
    def allowed_media_source_address_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMediaSourceAddressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedSignalingSourceAddressPrefixesInput")
    def allowed_signaling_source_address_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedSignalingSourceAddressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="esrpAddressesInput")
    def esrp_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "esrpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorAddressesInput")
    def operator_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "operatorAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMediaSourceAddressPrefixes")
    def allowed_media_source_address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMediaSourceAddressPrefixes"))

    @allowed_media_source_address_prefixes.setter
    def allowed_media_source_address_prefixes(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1eb3e7b7339f85d7ca94f24319665ecd8fd1bca739e43f0b97d88bbc4f3138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMediaSourceAddressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedSignalingSourceAddressPrefixes")
    def allowed_signaling_source_address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedSignalingSourceAddressPrefixes"))

    @allowed_signaling_source_address_prefixes.setter
    def allowed_signaling_source_address_prefixes(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a183f07877c2146e447bf566f617d33c117370ae5a2816ac927e459b335edee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedSignalingSourceAddressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="esrpAddresses")
    def esrp_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "esrpAddresses"))

    @esrp_addresses.setter
    def esrp_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31db033183ee2b520ab099140c222d5b503345b96f7e9b04fba413e1f0793757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "esrpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae002bacbbe72d92ab12092b93b233206335086aa79d4f5be2d8664a4f1951f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatorAddresses")
    def operator_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "operatorAddresses"))

    @operator_addresses.setter
    def operator_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784bbfcc9e578f94d467d4ee1dfd65562a5e2334d069e4a61e062075b757728e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatorAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayServiceLocation]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayServiceLocation]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayServiceLocation]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b6cb7aa67c2110795f70fd46cebd1841093d4bd9520f07af8fdcddcf18ab4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VoiceServicesCommunicationsGatewayTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#create VoiceServicesCommunicationsGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#delete VoiceServicesCommunicationsGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#read VoiceServicesCommunicationsGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#update VoiceServicesCommunicationsGateway#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bb1ebb5ab270cb8b9c1483d77b6bdd1a6cb851ae372926483deedce36bebca)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#create VoiceServicesCommunicationsGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#delete VoiceServicesCommunicationsGateway#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#read VoiceServicesCommunicationsGateway#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/voice_services_communications_gateway#update VoiceServicesCommunicationsGateway#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VoiceServicesCommunicationsGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VoiceServicesCommunicationsGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.voiceServicesCommunicationsGateway.VoiceServicesCommunicationsGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93ba9202e1663bc9f79d8c640d6508776c38264b065aedcc1836587d22b57782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2494c1155b723d7e876eee848ead7db63645c8b2efa328ea4bda8d210a9280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc032c0538b97ba06688c74e49dd29f2da20755d7bc2cfbbf8d48335e9ccbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f2035b721020905ef201d8fc8239bac34c3d6ca538ecef2220737e7541ddc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c647e1f637453eed0fada34ddbcacc4d28603bd6fbee54a582c17763633d892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99295add79e8e1b2109104ddb2417bca36fb95c9b2bfaff8277544992931d0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VoiceServicesCommunicationsGateway",
    "VoiceServicesCommunicationsGatewayConfig",
    "VoiceServicesCommunicationsGatewayServiceLocation",
    "VoiceServicesCommunicationsGatewayServiceLocationList",
    "VoiceServicesCommunicationsGatewayServiceLocationOutputReference",
    "VoiceServicesCommunicationsGatewayTimeouts",
    "VoiceServicesCommunicationsGatewayTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__11cc1871bf4fffd270cbb3b45388026b872fbfdf2f881d411b3a95dc5fd4475e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    codecs: builtins.str,
    connectivity: builtins.str,
    e911_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    resource_group_name: builtins.str,
    service_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VoiceServicesCommunicationsGatewayServiceLocation, typing.Dict[builtins.str, typing.Any]]]],
    api_bridge: typing.Optional[builtins.str] = None,
    auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
    emergency_dial_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    microsoft_teams_voicemail_pilot_number: typing.Optional[builtins.str] = None,
    on_prem_mcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VoiceServicesCommunicationsGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__62569204060a6df2d66a4f4d8abc43ca7924b0e368d1fceb321f470e571a542a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f149c9be5a82ca7c092d344739eb6ef6b1515fe61173354742c8fdb00a2551a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VoiceServicesCommunicationsGatewayServiceLocation, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a7d3ba253dade42efb8ff45b1fae477d11cecb4c322c4c7e499b8e8475f270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c30b91c989012b3de982ad568e8f9a9980e53daeaa8bdd724ac2a66eae31e78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b38ae086588f0ab136e7e7afc0feacff3a9ae199addfc72974b69a0c36c717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ac6a5e76df744573c6f518af011689490e5be984fa22836ddc7f9149e5956e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c6524044bd8133e749e6bdf35b474161ba9f8475da35742b62675546680b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046ee6e2491893d8a47a134c8bde0568e24f4f8c4b79159f9d95a6dd1aac1ebe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ba49cfd242a11e6ea037050984d4070c4f12efdd7986209fa442f464105612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b795b9146b3a490c830e7cd668d933abcff7cc51cbc67ad5d200e7677cb9078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525869fa6e0622d592affcbc2d6859720eceed83cf70fc729c0520e6e5a4efee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8280b2e0467ea1fa6a3287a789a0bce47e0048ac4ec8c85d99471ac9b6118b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c854151dab2dfc4ea1b9532b5330a6a3fc2763863232d3fb0e28912436ae8e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaa5613d303c8a5ee47a3a17f314ee78e6e3fcdb7c10d30df0257cdedf05099(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179f5e694041ae7857409532c7cd1797d10fce2cb802b18162853b021eb81cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff9aeb05bad48c1b7c2f38475ba033cbb04c36a53ea7ef18ec8c6d0c8cdb9e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cea39d21f5c1cf69b7d987e981eef68f7f6b4ea42c01b2ed198133f024b581b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    codecs: builtins.str,
    connectivity: builtins.str,
    e911_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    resource_group_name: builtins.str,
    service_location: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VoiceServicesCommunicationsGatewayServiceLocation, typing.Dict[builtins.str, typing.Any]]]],
    api_bridge: typing.Optional[builtins.str] = None,
    auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
    emergency_dial_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    microsoft_teams_voicemail_pilot_number: typing.Optional[builtins.str] = None,
    on_prem_mcp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VoiceServicesCommunicationsGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aeb7a98c8fa64e11cb61f6f0572e607c8e95cde83c5bd6d2c7c4521bb9f33b5(
    *,
    location: builtins.str,
    operator_addresses: typing.Sequence[builtins.str],
    allowed_media_source_address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_signaling_source_address_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    esrp_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b851bb427a15cd8809ec225666a88b8b795f114aace7972a625fb389ae10f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4babc24d0d4c329beeb4de7e139d52aa34b38690ac8feadcfcf467a435ce7d69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c9e0cd59c7751e422373492c59bd1340841683c4af0fc1ed547206d6186bd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151553e0de8128a3fb00fd47fb097ab4d90c2d2d608c92d9bb6726f9d631bb49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913f8daeb9fcb0a4759b55c4a728de4982981a1ebf5bb1d68820aacd589f7281(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc41dacbd3897b5dad65976501e54603116fbbca73f4b101feec3ab8b7f27491(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VoiceServicesCommunicationsGatewayServiceLocation]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6262a671bff46aa439d5d61236883a4c8eb051ab010d587f270e361c8e33e18a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1eb3e7b7339f85d7ca94f24319665ecd8fd1bca739e43f0b97d88bbc4f3138(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a183f07877c2146e447bf566f617d33c117370ae5a2816ac927e459b335edee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31db033183ee2b520ab099140c222d5b503345b96f7e9b04fba413e1f0793757(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae002bacbbe72d92ab12092b93b233206335086aa79d4f5be2d8664a4f1951f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784bbfcc9e578f94d467d4ee1dfd65562a5e2334d069e4a61e062075b757728e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b6cb7aa67c2110795f70fd46cebd1841093d4bd9520f07af8fdcddcf18ab4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayServiceLocation]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bb1ebb5ab270cb8b9c1483d77b6bdd1a6cb851ae372926483deedce36bebca(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ba9202e1663bc9f79d8c640d6508776c38264b065aedcc1836587d22b57782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2494c1155b723d7e876eee848ead7db63645c8b2efa328ea4bda8d210a9280(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc032c0538b97ba06688c74e49dd29f2da20755d7bc2cfbbf8d48335e9ccbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f2035b721020905ef201d8fc8239bac34c3d6ca538ecef2220737e7541ddc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c647e1f637453eed0fada34ddbcacc4d28603bd6fbee54a582c17763633d892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99295add79e8e1b2109104ddb2417bca36fb95c9b2bfaff8277544992931d0f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VoiceServicesCommunicationsGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

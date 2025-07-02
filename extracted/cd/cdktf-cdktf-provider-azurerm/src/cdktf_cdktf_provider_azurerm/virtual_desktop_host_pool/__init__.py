r'''
# `azurerm_virtual_desktop_host_pool`

Refer to the Terraform Registry for docs: [`azurerm_virtual_desktop_host_pool`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool).
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


class VirtualDesktopHostPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool azurerm_virtual_desktop_host_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        load_balancer_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        type: builtins.str,
        custom_rdp_properties: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_sessions_allowed: typing.Optional[jsii.Number] = None,
        personal_desktop_assignment_type: typing.Optional[builtins.str] = None,
        preferred_app_group_type: typing.Optional[builtins.str] = None,
        public_network_access: typing.Optional[builtins.str] = None,
        scheduled_agent_updates: typing.Optional[typing.Union["VirtualDesktopHostPoolScheduledAgentUpdates", typing.Dict[builtins.str, typing.Any]]] = None,
        start_vm_on_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualDesktopHostPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validate_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vm_template: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool azurerm_virtual_desktop_host_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param load_balancer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#load_balancer_type VirtualDesktopHostPool#load_balancer_type}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#location VirtualDesktopHostPool#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#name VirtualDesktopHostPool#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#resource_group_name VirtualDesktopHostPool#resource_group_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#type VirtualDesktopHostPool#type}.
        :param custom_rdp_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#custom_rdp_properties VirtualDesktopHostPool#custom_rdp_properties}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#description VirtualDesktopHostPool#description}.
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#friendly_name VirtualDesktopHostPool#friendly_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#id VirtualDesktopHostPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_sessions_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#maximum_sessions_allowed VirtualDesktopHostPool#maximum_sessions_allowed}.
        :param personal_desktop_assignment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#personal_desktop_assignment_type VirtualDesktopHostPool#personal_desktop_assignment_type}.
        :param preferred_app_group_type: Preferred App Group type to display. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#preferred_app_group_type VirtualDesktopHostPool#preferred_app_group_type}
        :param public_network_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#public_network_access VirtualDesktopHostPool#public_network_access}.
        :param scheduled_agent_updates: scheduled_agent_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#scheduled_agent_updates VirtualDesktopHostPool#scheduled_agent_updates}
        :param start_vm_on_connect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#start_vm_on_connect VirtualDesktopHostPool#start_vm_on_connect}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#tags VirtualDesktopHostPool#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timeouts VirtualDesktopHostPool#timeouts}
        :param validate_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#validate_environment VirtualDesktopHostPool#validate_environment}.
        :param vm_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#vm_template VirtualDesktopHostPool#vm_template}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fd1be0583c387ee8b443412efba0c339ebead809574f0d5c35b407028c7d6b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualDesktopHostPoolConfig(
            load_balancer_type=load_balancer_type,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            type=type,
            custom_rdp_properties=custom_rdp_properties,
            description=description,
            friendly_name=friendly_name,
            id=id,
            maximum_sessions_allowed=maximum_sessions_allowed,
            personal_desktop_assignment_type=personal_desktop_assignment_type,
            preferred_app_group_type=preferred_app_group_type,
            public_network_access=public_network_access,
            scheduled_agent_updates=scheduled_agent_updates,
            start_vm_on_connect=start_vm_on_connect,
            tags=tags,
            timeouts=timeouts,
            validate_environment=validate_environment,
            vm_template=vm_template,
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
        '''Generates CDKTF code for importing a VirtualDesktopHostPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualDesktopHostPool to import.
        :param import_from_id: The id of the existing VirtualDesktopHostPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualDesktopHostPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5f805290fa5aefca478502dbfdfec21a72b627817036394995826b8a85c0f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putScheduledAgentUpdates")
    def put_scheduled_agent_updates(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        use_session_host_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#enabled VirtualDesktopHostPool#enabled}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#schedule VirtualDesktopHostPool#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timezone VirtualDesktopHostPool#timezone}.
        :param use_session_host_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#use_session_host_timezone VirtualDesktopHostPool#use_session_host_timezone}.
        '''
        value = VirtualDesktopHostPoolScheduledAgentUpdates(
            enabled=enabled,
            schedule=schedule,
            timezone=timezone,
            use_session_host_timezone=use_session_host_timezone,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduledAgentUpdates", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#create VirtualDesktopHostPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#delete VirtualDesktopHostPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#read VirtualDesktopHostPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#update VirtualDesktopHostPool#update}.
        '''
        value = VirtualDesktopHostPoolTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomRdpProperties")
    def reset_custom_rdp_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRdpProperties", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaximumSessionsAllowed")
    def reset_maximum_sessions_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumSessionsAllowed", []))

    @jsii.member(jsii_name="resetPersonalDesktopAssignmentType")
    def reset_personal_desktop_assignment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonalDesktopAssignmentType", []))

    @jsii.member(jsii_name="resetPreferredAppGroupType")
    def reset_preferred_app_group_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreferredAppGroupType", []))

    @jsii.member(jsii_name="resetPublicNetworkAccess")
    def reset_public_network_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccess", []))

    @jsii.member(jsii_name="resetScheduledAgentUpdates")
    def reset_scheduled_agent_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledAgentUpdates", []))

    @jsii.member(jsii_name="resetStartVmOnConnect")
    def reset_start_vm_on_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartVmOnConnect", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValidateEnvironment")
    def reset_validate_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateEnvironment", []))

    @jsii.member(jsii_name="resetVmTemplate")
    def reset_vm_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmTemplate", []))

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
    @jsii.member(jsii_name="scheduledAgentUpdates")
    def scheduled_agent_updates(
        self,
    ) -> "VirtualDesktopHostPoolScheduledAgentUpdatesOutputReference":
        return typing.cast("VirtualDesktopHostPoolScheduledAgentUpdatesOutputReference", jsii.get(self, "scheduledAgentUpdates"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualDesktopHostPoolTimeoutsOutputReference":
        return typing.cast("VirtualDesktopHostPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="customRdpPropertiesInput")
    def custom_rdp_properties_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customRdpPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerTypeInput")
    def load_balancer_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumSessionsAllowedInput")
    def maximum_sessions_allowed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumSessionsAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="personalDesktopAssignmentTypeInput")
    def personal_desktop_assignment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "personalDesktopAssignmentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="preferredAppGroupTypeInput")
    def preferred_app_group_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredAppGroupTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessInput")
    def public_network_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicNetworkAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledAgentUpdatesInput")
    def scheduled_agent_updates_input(
        self,
    ) -> typing.Optional["VirtualDesktopHostPoolScheduledAgentUpdates"]:
        return typing.cast(typing.Optional["VirtualDesktopHostPoolScheduledAgentUpdates"], jsii.get(self, "scheduledAgentUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="startVmOnConnectInput")
    def start_vm_on_connect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startVmOnConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualDesktopHostPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualDesktopHostPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="validateEnvironmentInput")
    def validate_environment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="vmTemplateInput")
    def vm_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="customRdpProperties")
    def custom_rdp_properties(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customRdpProperties"))

    @custom_rdp_properties.setter
    def custom_rdp_properties(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1f182258be39ea18aaaf2158bed953e012a94356110f52ded8db840aa55085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRdpProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d3fdf500b60cc6d6c4cdba3eb2e1614335c250f7bee0ccae2f67ac8c320570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf029b62aa3ebad2c4d29e272621b34b97c76a688c6f7ff2ab79079a14c155b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1eb427158d50fbb7621358fbabd6398f6225e6d2a2781a895258c4b341bf24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerType")
    def load_balancer_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerType"))

    @load_balancer_type.setter
    def load_balancer_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21e43f93a50eaf3bc419697e09fa76bb42beff4470aceec553612a6f03ad698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__132cdd99c65e1761222e5c656fc790bf0bacf156ff6549f74d4540fec09ffcb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumSessionsAllowed")
    def maximum_sessions_allowed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumSessionsAllowed"))

    @maximum_sessions_allowed.setter
    def maximum_sessions_allowed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47e690914baaf8a86b3431650f100e7f926de5b116bfb73dbef00727254417c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumSessionsAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e2407472cf69a6357cc3b17f744720af0acdc1dcef0048b2c998d87b084772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="personalDesktopAssignmentType")
    def personal_desktop_assignment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "personalDesktopAssignmentType"))

    @personal_desktop_assignment_type.setter
    def personal_desktop_assignment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd3274d2a5d34199afb0dd0cc8eb90158c5e4286edf78e20792169c1627571c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "personalDesktopAssignmentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preferredAppGroupType")
    def preferred_app_group_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredAppGroupType"))

    @preferred_app_group_type.setter
    def preferred_app_group_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcf018fc51324e5e6e60344e59c681042aeccbbbdf69d564b0b4bd91fa0481e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredAppGroupType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccess")
    def public_network_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicNetworkAccess"))

    @public_network_access.setter
    def public_network_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027c6bba39daf645566a704e361ffc54a59968b80d0ad493dff877e3732e2755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d6a8ae84c49ed5fb22e6607d62873d360f7f3c5f27b11d47305106ed6e1852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startVmOnConnect")
    def start_vm_on_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startVmOnConnect"))

    @start_vm_on_connect.setter
    def start_vm_on_connect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed63ac55ba4d09f8655510f620b26f923b359b2ccacd3bdd44a0f6e91769f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startVmOnConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9031d1e052be4028c363b38435de5cde4de459210f4ddbe0aa84db99d0e966d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad8aad5cb8f68aaa1a3976174495533532f0fd886d4ab4d295816fc748f26f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateEnvironment")
    def validate_environment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateEnvironment"))

    @validate_environment.setter
    def validate_environment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a688559c6f8f24b7b8f960465cbb4c9533787346f01db1a0800dc4ac1888d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmTemplate")
    def vm_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmTemplate"))

    @vm_template.setter
    def vm_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a19b221c63044398db43fede890bf7f4a7badffaa560f4d05c080ad5596ff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmTemplate", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "load_balancer_type": "loadBalancerType",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "type": "type",
        "custom_rdp_properties": "customRdpProperties",
        "description": "description",
        "friendly_name": "friendlyName",
        "id": "id",
        "maximum_sessions_allowed": "maximumSessionsAllowed",
        "personal_desktop_assignment_type": "personalDesktopAssignmentType",
        "preferred_app_group_type": "preferredAppGroupType",
        "public_network_access": "publicNetworkAccess",
        "scheduled_agent_updates": "scheduledAgentUpdates",
        "start_vm_on_connect": "startVmOnConnect",
        "tags": "tags",
        "timeouts": "timeouts",
        "validate_environment": "validateEnvironment",
        "vm_template": "vmTemplate",
    },
)
class VirtualDesktopHostPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        load_balancer_type: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        type: builtins.str,
        custom_rdp_properties: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        maximum_sessions_allowed: typing.Optional[jsii.Number] = None,
        personal_desktop_assignment_type: typing.Optional[builtins.str] = None,
        preferred_app_group_type: typing.Optional[builtins.str] = None,
        public_network_access: typing.Optional[builtins.str] = None,
        scheduled_agent_updates: typing.Optional[typing.Union["VirtualDesktopHostPoolScheduledAgentUpdates", typing.Dict[builtins.str, typing.Any]]] = None,
        start_vm_on_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualDesktopHostPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        validate_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vm_template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param load_balancer_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#load_balancer_type VirtualDesktopHostPool#load_balancer_type}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#location VirtualDesktopHostPool#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#name VirtualDesktopHostPool#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#resource_group_name VirtualDesktopHostPool#resource_group_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#type VirtualDesktopHostPool#type}.
        :param custom_rdp_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#custom_rdp_properties VirtualDesktopHostPool#custom_rdp_properties}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#description VirtualDesktopHostPool#description}.
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#friendly_name VirtualDesktopHostPool#friendly_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#id VirtualDesktopHostPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maximum_sessions_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#maximum_sessions_allowed VirtualDesktopHostPool#maximum_sessions_allowed}.
        :param personal_desktop_assignment_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#personal_desktop_assignment_type VirtualDesktopHostPool#personal_desktop_assignment_type}.
        :param preferred_app_group_type: Preferred App Group type to display. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#preferred_app_group_type VirtualDesktopHostPool#preferred_app_group_type}
        :param public_network_access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#public_network_access VirtualDesktopHostPool#public_network_access}.
        :param scheduled_agent_updates: scheduled_agent_updates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#scheduled_agent_updates VirtualDesktopHostPool#scheduled_agent_updates}
        :param start_vm_on_connect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#start_vm_on_connect VirtualDesktopHostPool#start_vm_on_connect}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#tags VirtualDesktopHostPool#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timeouts VirtualDesktopHostPool#timeouts}
        :param validate_environment: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#validate_environment VirtualDesktopHostPool#validate_environment}.
        :param vm_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#vm_template VirtualDesktopHostPool#vm_template}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(scheduled_agent_updates, dict):
            scheduled_agent_updates = VirtualDesktopHostPoolScheduledAgentUpdates(**scheduled_agent_updates)
        if isinstance(timeouts, dict):
            timeouts = VirtualDesktopHostPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60151b0af9b06d14f30b7a4d45f6c7d60692d3c6566609cdf32ad2eec12d610)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument custom_rdp_properties", value=custom_rdp_properties, expected_type=type_hints["custom_rdp_properties"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maximum_sessions_allowed", value=maximum_sessions_allowed, expected_type=type_hints["maximum_sessions_allowed"])
            check_type(argname="argument personal_desktop_assignment_type", value=personal_desktop_assignment_type, expected_type=type_hints["personal_desktop_assignment_type"])
            check_type(argname="argument preferred_app_group_type", value=preferred_app_group_type, expected_type=type_hints["preferred_app_group_type"])
            check_type(argname="argument public_network_access", value=public_network_access, expected_type=type_hints["public_network_access"])
            check_type(argname="argument scheduled_agent_updates", value=scheduled_agent_updates, expected_type=type_hints["scheduled_agent_updates"])
            check_type(argname="argument start_vm_on_connect", value=start_vm_on_connect, expected_type=type_hints["start_vm_on_connect"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument validate_environment", value=validate_environment, expected_type=type_hints["validate_environment"])
            check_type(argname="argument vm_template", value=vm_template, expected_type=type_hints["vm_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "type": type,
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
        if custom_rdp_properties is not None:
            self._values["custom_rdp_properties"] = custom_rdp_properties
        if description is not None:
            self._values["description"] = description
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if maximum_sessions_allowed is not None:
            self._values["maximum_sessions_allowed"] = maximum_sessions_allowed
        if personal_desktop_assignment_type is not None:
            self._values["personal_desktop_assignment_type"] = personal_desktop_assignment_type
        if preferred_app_group_type is not None:
            self._values["preferred_app_group_type"] = preferred_app_group_type
        if public_network_access is not None:
            self._values["public_network_access"] = public_network_access
        if scheduled_agent_updates is not None:
            self._values["scheduled_agent_updates"] = scheduled_agent_updates
        if start_vm_on_connect is not None:
            self._values["start_vm_on_connect"] = start_vm_on_connect
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if validate_environment is not None:
            self._values["validate_environment"] = validate_environment
        if vm_template is not None:
            self._values["vm_template"] = vm_template

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
    def load_balancer_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#load_balancer_type VirtualDesktopHostPool#load_balancer_type}.'''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#location VirtualDesktopHostPool#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#name VirtualDesktopHostPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#resource_group_name VirtualDesktopHostPool#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#type VirtualDesktopHostPool#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_rdp_properties(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#custom_rdp_properties VirtualDesktopHostPool#custom_rdp_properties}.'''
        result = self._values.get("custom_rdp_properties")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#description VirtualDesktopHostPool#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#friendly_name VirtualDesktopHostPool#friendly_name}.'''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#id VirtualDesktopHostPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_sessions_allowed(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#maximum_sessions_allowed VirtualDesktopHostPool#maximum_sessions_allowed}.'''
        result = self._values.get("maximum_sessions_allowed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def personal_desktop_assignment_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#personal_desktop_assignment_type VirtualDesktopHostPool#personal_desktop_assignment_type}.'''
        result = self._values.get("personal_desktop_assignment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_app_group_type(self) -> typing.Optional[builtins.str]:
        '''Preferred App Group type to display.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#preferred_app_group_type VirtualDesktopHostPool#preferred_app_group_type}
        '''
        result = self._values.get("preferred_app_group_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#public_network_access VirtualDesktopHostPool#public_network_access}.'''
        result = self._values.get("public_network_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_agent_updates(
        self,
    ) -> typing.Optional["VirtualDesktopHostPoolScheduledAgentUpdates"]:
        '''scheduled_agent_updates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#scheduled_agent_updates VirtualDesktopHostPool#scheduled_agent_updates}
        '''
        result = self._values.get("scheduled_agent_updates")
        return typing.cast(typing.Optional["VirtualDesktopHostPoolScheduledAgentUpdates"], result)

    @builtins.property
    def start_vm_on_connect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#start_vm_on_connect VirtualDesktopHostPool#start_vm_on_connect}.'''
        result = self._values.get("start_vm_on_connect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#tags VirtualDesktopHostPool#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualDesktopHostPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timeouts VirtualDesktopHostPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualDesktopHostPoolTimeouts"], result)

    @builtins.property
    def validate_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#validate_environment VirtualDesktopHostPool#validate_environment}.'''
        result = self._values.get("validate_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vm_template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#vm_template VirtualDesktopHostPool#vm_template}.'''
        result = self._values.get("vm_template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopHostPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolScheduledAgentUpdates",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "schedule": "schedule",
        "timezone": "timezone",
        "use_session_host_timezone": "useSessionHostTimezone",
    },
)
class VirtualDesktopHostPoolScheduledAgentUpdates:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timezone: typing.Optional[builtins.str] = None,
        use_session_host_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#enabled VirtualDesktopHostPool#enabled}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#schedule VirtualDesktopHostPool#schedule}
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timezone VirtualDesktopHostPool#timezone}.
        :param use_session_host_timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#use_session_host_timezone VirtualDesktopHostPool#use_session_host_timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a7a54f9c51b074ebb0f8524be4aa28e029fb404322e5bb7e2cb76600a0dfcf)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument use_session_host_timezone", value=use_session_host_timezone, expected_type=type_hints["use_session_host_timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if schedule is not None:
            self._values["schedule"] = schedule
        if timezone is not None:
            self._values["timezone"] = timezone
        if use_session_host_timezone is not None:
            self._values["use_session_host_timezone"] = use_session_host_timezone

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#enabled VirtualDesktopHostPool#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule"]]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#schedule VirtualDesktopHostPool#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule"]]], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#timezone VirtualDesktopHostPool#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_session_host_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#use_session_host_timezone VirtualDesktopHostPool#use_session_host_timezone}.'''
        result = self._values.get("use_session_host_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopHostPoolScheduledAgentUpdates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopHostPoolScheduledAgentUpdatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolScheduledAgentUpdatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f61f45d2923fc89afa3e15cc3f82694c0f9a3146b07a9d8ae91e4ba4586259)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b598cdc1d611e3d29f4cd0cf1212505bf85dc6917b05512f92b2eeeca046179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetUseSessionHostTimezone")
    def reset_use_session_host_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseSessionHostTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "VirtualDesktopHostPoolScheduledAgentUpdatesScheduleList":
        return typing.cast("VirtualDesktopHostPoolScheduledAgentUpdatesScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopHostPoolScheduledAgentUpdatesSchedule"]]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="useSessionHostTimezoneInput")
    def use_session_host_timezone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useSessionHostTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604eae249dabcc4db33aa3b55bd48e13d3024f08f5b32e6710944f3ed7fd9462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5350284fa0677fbbd4ba63bc77a1119ca937de222efb736a48dc7a3d9cb00001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSessionHostTimezone")
    def use_session_host_timezone(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useSessionHostTimezone"))

    @use_session_host_timezone.setter
    def use_session_host_timezone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41228942b9a38254b162503f4214d8724184ebc300217ea71705f2f5e2b2a193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSessionHostTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualDesktopHostPoolScheduledAgentUpdates]:
        return typing.cast(typing.Optional[VirtualDesktopHostPoolScheduledAgentUpdates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualDesktopHostPoolScheduledAgentUpdates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481888eb0d0a68ad831ce22e7749bc65cca86a3f77931ba927d4ed5c640d0dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolScheduledAgentUpdatesSchedule",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "hour_of_day": "hourOfDay"},
)
class VirtualDesktopHostPoolScheduledAgentUpdatesSchedule:
    def __init__(self, *, day_of_week: builtins.str, hour_of_day: jsii.Number) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#day_of_week VirtualDesktopHostPool#day_of_week}.
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#hour_of_day VirtualDesktopHostPool#hour_of_day}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cae61fe22cd08fa18da6f96e44d4b535c5b8dcd07c0bd17d21e24a5c25c8e2)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "hour_of_day": hour_of_day,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#day_of_week VirtualDesktopHostPool#day_of_week}.'''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour_of_day(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#hour_of_day VirtualDesktopHostPool#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        assert result is not None, "Required property 'hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopHostPoolScheduledAgentUpdatesSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopHostPoolScheduledAgentUpdatesScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolScheduledAgentUpdatesScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0b69d790296f407be98334e7442e81700c1c47ca87eef975ea023098647773)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualDesktopHostPoolScheduledAgentUpdatesScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f2a4db7d855cdacb7deb5e2613fac37bbb5853b99a1d21e0da32a49e40f1b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualDesktopHostPoolScheduledAgentUpdatesScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15e7061cfb70b509f708f3f6b1c75483be230b0edea82134fafd09c78e7de77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c051128a889474dcf52a37acec5b93d7eeb1d099c2c917516c651670a69a4c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d261ee9bcf22f66d74f2f94cd67ccde3bdd53c3b57bb6ad39418b9064effe415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7487d236dfc091162a2fa6b6d55e310f46ff010ea26cd9c4a59d0316893afbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualDesktopHostPoolScheduledAgentUpdatesScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolScheduledAgentUpdatesScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__883672fc0834edae5d30de9d32f26d38690f0f863ff642396cccb973e70bc395)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da85f8d8f77a571b327f729072a1e33e276fb288759174e7617ef0c0c1534373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014704fffc5a8b900e5738c98185d42cb78ab0b3512dd097d31847be3645cd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c336f9590521c019ebd9b242c719f05a20f36d72f000c0a9d53a3734d0d5e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VirtualDesktopHostPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#create VirtualDesktopHostPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#delete VirtualDesktopHostPool#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#read VirtualDesktopHostPool#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#update VirtualDesktopHostPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2019474fccbd84b58eeec101bb2ae011f59eb269d00e136f92a99fe1a00aee)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#create VirtualDesktopHostPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#delete VirtualDesktopHostPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#read VirtualDesktopHostPool#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_host_pool#update VirtualDesktopHostPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopHostPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopHostPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopHostPool.VirtualDesktopHostPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8998ac98605dff5ec417beb64555395e269b1d32b3076f004651219362f1b3b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65148cc03f11afa004d02e3c11e3728f7efff859e66f4d3b9a10f97b6eccfd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5713e0ff031c13242f452b8f445e3f1a438cea0fe9ef750c896386527266d7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f664b18a2f1ac0cbe9c3b7e5330a0b93999c5f6815d334eaa1d52a126bd752d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0209846af54984b5efdd2fa6b1f406d5c2df29c4d07b6d32f31fc73372c0b24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f640d28feb5467c3a2356c75ca0aac07223100eb4ba5ea88ce85399cef369f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualDesktopHostPool",
    "VirtualDesktopHostPoolConfig",
    "VirtualDesktopHostPoolScheduledAgentUpdates",
    "VirtualDesktopHostPoolScheduledAgentUpdatesOutputReference",
    "VirtualDesktopHostPoolScheduledAgentUpdatesSchedule",
    "VirtualDesktopHostPoolScheduledAgentUpdatesScheduleList",
    "VirtualDesktopHostPoolScheduledAgentUpdatesScheduleOutputReference",
    "VirtualDesktopHostPoolTimeouts",
    "VirtualDesktopHostPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__38fd1be0583c387ee8b443412efba0c339ebead809574f0d5c35b407028c7d6b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    load_balancer_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    type: builtins.str,
    custom_rdp_properties: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_sessions_allowed: typing.Optional[jsii.Number] = None,
    personal_desktop_assignment_type: typing.Optional[builtins.str] = None,
    preferred_app_group_type: typing.Optional[builtins.str] = None,
    public_network_access: typing.Optional[builtins.str] = None,
    scheduled_agent_updates: typing.Optional[typing.Union[VirtualDesktopHostPoolScheduledAgentUpdates, typing.Dict[builtins.str, typing.Any]]] = None,
    start_vm_on_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualDesktopHostPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validate_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vm_template: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9c5f805290fa5aefca478502dbfdfec21a72b627817036394995826b8a85c0f6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1f182258be39ea18aaaf2158bed953e012a94356110f52ded8db840aa55085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d3fdf500b60cc6d6c4cdba3eb2e1614335c250f7bee0ccae2f67ac8c320570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf029b62aa3ebad2c4d29e272621b34b97c76a688c6f7ff2ab79079a14c155b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1eb427158d50fbb7621358fbabd6398f6225e6d2a2781a895258c4b341bf24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21e43f93a50eaf3bc419697e09fa76bb42beff4470aceec553612a6f03ad698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132cdd99c65e1761222e5c656fc790bf0bacf156ff6549f74d4540fec09ffcb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47e690914baaf8a86b3431650f100e7f926de5b116bfb73dbef00727254417c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e2407472cf69a6357cc3b17f744720af0acdc1dcef0048b2c998d87b084772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd3274d2a5d34199afb0dd0cc8eb90158c5e4286edf78e20792169c1627571c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcf018fc51324e5e6e60344e59c681042aeccbbbdf69d564b0b4bd91fa0481e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027c6bba39daf645566a704e361ffc54a59968b80d0ad493dff877e3732e2755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d6a8ae84c49ed5fb22e6607d62873d360f7f3c5f27b11d47305106ed6e1852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed63ac55ba4d09f8655510f620b26f923b359b2ccacd3bdd44a0f6e91769f2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9031d1e052be4028c363b38435de5cde4de459210f4ddbe0aa84db99d0e966d2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad8aad5cb8f68aaa1a3976174495533532f0fd886d4ab4d295816fc748f26f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a688559c6f8f24b7b8f960465cbb4c9533787346f01db1a0800dc4ac1888d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a19b221c63044398db43fede890bf7f4a7badffaa560f4d05c080ad5596ff7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60151b0af9b06d14f30b7a4d45f6c7d60692d3c6566609cdf32ad2eec12d610(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    load_balancer_type: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    type: builtins.str,
    custom_rdp_properties: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    maximum_sessions_allowed: typing.Optional[jsii.Number] = None,
    personal_desktop_assignment_type: typing.Optional[builtins.str] = None,
    preferred_app_group_type: typing.Optional[builtins.str] = None,
    public_network_access: typing.Optional[builtins.str] = None,
    scheduled_agent_updates: typing.Optional[typing.Union[VirtualDesktopHostPoolScheduledAgentUpdates, typing.Dict[builtins.str, typing.Any]]] = None,
    start_vm_on_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualDesktopHostPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    validate_environment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vm_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a7a54f9c51b074ebb0f8524be4aa28e029fb404322e5bb7e2cb76600a0dfcf(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    schedule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timezone: typing.Optional[builtins.str] = None,
    use_session_host_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f61f45d2923fc89afa3e15cc3f82694c0f9a3146b07a9d8ae91e4ba4586259(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b598cdc1d611e3d29f4cd0cf1212505bf85dc6917b05512f92b2eeeca046179(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604eae249dabcc4db33aa3b55bd48e13d3024f08f5b32e6710944f3ed7fd9462(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5350284fa0677fbbd4ba63bc77a1119ca937de222efb736a48dc7a3d9cb00001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41228942b9a38254b162503f4214d8724184ebc300217ea71705f2f5e2b2a193(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481888eb0d0a68ad831ce22e7749bc65cca86a3f77931ba927d4ed5c640d0dc4(
    value: typing.Optional[VirtualDesktopHostPoolScheduledAgentUpdates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cae61fe22cd08fa18da6f96e44d4b535c5b8dcd07c0bd17d21e24a5c25c8e2(
    *,
    day_of_week: builtins.str,
    hour_of_day: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0b69d790296f407be98334e7442e81700c1c47ca87eef975ea023098647773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f2a4db7d855cdacb7deb5e2613fac37bbb5853b99a1d21e0da32a49e40f1b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15e7061cfb70b509f708f3f6b1c75483be230b0edea82134fafd09c78e7de77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c051128a889474dcf52a37acec5b93d7eeb1d099c2c917516c651670a69a4c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d261ee9bcf22f66d74f2f94cd67ccde3bdd53c3b57bb6ad39418b9064effe415(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7487d236dfc091162a2fa6b6d55e310f46ff010ea26cd9c4a59d0316893afbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883672fc0834edae5d30de9d32f26d38690f0f863ff642396cccb973e70bc395(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da85f8d8f77a571b327f729072a1e33e276fb288759174e7617ef0c0c1534373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014704fffc5a8b900e5738c98185d42cb78ab0b3512dd097d31847be3645cd90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c336f9590521c019ebd9b242c719f05a20f36d72f000c0a9d53a3734d0d5e38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolScheduledAgentUpdatesSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2019474fccbd84b58eeec101bb2ae011f59eb269d00e136f92a99fe1a00aee(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8998ac98605dff5ec417beb64555395e269b1d32b3076f004651219362f1b3b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65148cc03f11afa004d02e3c11e3728f7efff859e66f4d3b9a10f97b6eccfd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5713e0ff031c13242f452b8f445e3f1a438cea0fe9ef750c896386527266d7dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f664b18a2f1ac0cbe9c3b7e5330a0b93999c5f6815d334eaa1d52a126bd752d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0209846af54984b5efdd2fa6b1f406d5c2df29c4d07b6d32f31fc73372c0b24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f640d28feb5467c3a2356c75ca0aac07223100eb4ba5ea88ce85399cef369f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopHostPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

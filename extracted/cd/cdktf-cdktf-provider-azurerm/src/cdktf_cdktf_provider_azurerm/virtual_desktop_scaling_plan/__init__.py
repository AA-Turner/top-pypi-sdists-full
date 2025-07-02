r'''
# `azurerm_virtual_desktop_scaling_plan`

Refer to the Terraform Registry for docs: [`azurerm_virtual_desktop_scaling_plan`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan).
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


class VirtualDesktopScalingPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan azurerm_virtual_desktop_scaling_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanSchedule", typing.Dict[builtins.str, typing.Any]]]],
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        exclusion_tag: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        host_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanHostPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualDesktopScalingPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan azurerm_virtual_desktop_scaling_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#location VirtualDesktopScalingPlan#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#name VirtualDesktopScalingPlan#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#resource_group_name VirtualDesktopScalingPlan#resource_group_name}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#schedule VirtualDesktopScalingPlan#schedule}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#time_zone VirtualDesktopScalingPlan#time_zone}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#description VirtualDesktopScalingPlan#description}.
        :param exclusion_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#exclusion_tag VirtualDesktopScalingPlan#exclusion_tag}.
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#friendly_name VirtualDesktopScalingPlan#friendly_name}.
        :param host_pool: host_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#host_pool VirtualDesktopScalingPlan#host_pool}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#id VirtualDesktopScalingPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#tags VirtualDesktopScalingPlan#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#timeouts VirtualDesktopScalingPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d5351a7e463d7a28c75d7fe570115c620fa8194d59ac8ffec54ad3545a06a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualDesktopScalingPlanConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            schedule=schedule,
            time_zone=time_zone,
            description=description,
            exclusion_tag=exclusion_tag,
            friendly_name=friendly_name,
            host_pool=host_pool,
            id=id,
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
        '''Generates CDKTF code for importing a VirtualDesktopScalingPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VirtualDesktopScalingPlan to import.
        :param import_from_id: The id of the existing VirtualDesktopScalingPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VirtualDesktopScalingPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1d3812ecb2f445f47e28800fd111bd4cbed23e149b366a9b5c926eb2e8a961)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHostPool")
    def put_host_pool(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanHostPool", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e67b01800fb1808da7ce9f1b5ff7016c0615cb1decd58ae1e5b5e3393fb9f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHostPool", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanSchedule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9785381023afe7e57afc77d758ec97d1308ac42d954fdb9655b6df7d9b04be44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#create VirtualDesktopScalingPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#delete VirtualDesktopScalingPlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#read VirtualDesktopScalingPlan#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#update VirtualDesktopScalingPlan#update}.
        '''
        value = VirtualDesktopScalingPlanTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExclusionTag")
    def reset_exclusion_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionTag", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetHostPool")
    def reset_host_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostPool", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="hostPool")
    def host_pool(self) -> "VirtualDesktopScalingPlanHostPoolList":
        return typing.cast("VirtualDesktopScalingPlanHostPoolList", jsii.get(self, "hostPool"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "VirtualDesktopScalingPlanScheduleList":
        return typing.cast("VirtualDesktopScalingPlanScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualDesktopScalingPlanTimeoutsOutputReference":
        return typing.cast("VirtualDesktopScalingPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionTagInput")
    def exclusion_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exclusionTagInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostPoolInput")
    def host_pool_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanHostPool"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanHostPool"]]], jsii.get(self, "hostPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanSchedule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanSchedule"]]], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualDesktopScalingPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VirtualDesktopScalingPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b5f7e9e6023aa2d0a93d78b119f2e6da6f15257d27b9c73573e457d6376b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusionTag")
    def exclusion_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exclusionTag"))

    @exclusion_tag.setter
    def exclusion_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d47db7880ef7c82a9eb5e38647b964ef02434accbba293f24a701d39f1e2971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce26f1b0096fbb37d9c508ae7b27f3e920f78434a541cb135c594f970a543868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0868354369ead2599de3e54a89e2cb410d1973d41d73657255e02cd07ec134a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01edf0c8ed984da2413f48f6104d677abb0b33980a88aa1c436621590dcefccb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ecf99e36fe92605eabe34e5970dea50e0dc3ddb2a6a3873166f0c52f510b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1465ea5f900db3597c9f21ba9fe08386ac3daa04322462db349600419c5320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41af813b87fdd0a834fb02ac46af2bb9743b0df51a174aa4c7aa56ea455fa19b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03b2a5958b819b9a1711de07128f1c3731bc2392a9028fa60a6a6947b859a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "schedule": "schedule",
        "time_zone": "timeZone",
        "description": "description",
        "exclusion_tag": "exclusionTag",
        "friendly_name": "friendlyName",
        "host_pool": "hostPool",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class VirtualDesktopScalingPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanSchedule", typing.Dict[builtins.str, typing.Any]]]],
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        exclusion_tag: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        host_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualDesktopScalingPlanHostPool", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VirtualDesktopScalingPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#location VirtualDesktopScalingPlan#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#name VirtualDesktopScalingPlan#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#resource_group_name VirtualDesktopScalingPlan#resource_group_name}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#schedule VirtualDesktopScalingPlan#schedule}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#time_zone VirtualDesktopScalingPlan#time_zone}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#description VirtualDesktopScalingPlan#description}.
        :param exclusion_tag: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#exclusion_tag VirtualDesktopScalingPlan#exclusion_tag}.
        :param friendly_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#friendly_name VirtualDesktopScalingPlan#friendly_name}.
        :param host_pool: host_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#host_pool VirtualDesktopScalingPlan#host_pool}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#id VirtualDesktopScalingPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#tags VirtualDesktopScalingPlan#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#timeouts VirtualDesktopScalingPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = VirtualDesktopScalingPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9560d40fb4ff9fbd2c9231c74be649dd05bee52711a88547e857d47e0a7755)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclusion_tag", value=exclusion_tag, expected_type=type_hints["exclusion_tag"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument host_pool", value=host_pool, expected_type=type_hints["host_pool"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "schedule": schedule,
            "time_zone": time_zone,
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
        if exclusion_tag is not None:
            self._values["exclusion_tag"] = exclusion_tag
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if host_pool is not None:
            self._values["host_pool"] = host_pool
        if id is not None:
            self._values["id"] = id
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#location VirtualDesktopScalingPlan#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#name VirtualDesktopScalingPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#resource_group_name VirtualDesktopScalingPlan#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanSchedule"]]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#schedule VirtualDesktopScalingPlan#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanSchedule"]], result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#time_zone VirtualDesktopScalingPlan#time_zone}.'''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#description VirtualDesktopScalingPlan#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusion_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#exclusion_tag VirtualDesktopScalingPlan#exclusion_tag}.'''
        result = self._values.get("exclusion_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#friendly_name VirtualDesktopScalingPlan#friendly_name}.'''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_pool(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanHostPool"]]]:
        '''host_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#host_pool VirtualDesktopScalingPlan#host_pool}
        '''
        result = self._values.get("host_pool")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualDesktopScalingPlanHostPool"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#id VirtualDesktopScalingPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#tags VirtualDesktopScalingPlan#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VirtualDesktopScalingPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#timeouts VirtualDesktopScalingPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VirtualDesktopScalingPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopScalingPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanHostPool",
    jsii_struct_bases=[],
    name_mapping={
        "hostpool_id": "hostpoolId",
        "scaling_plan_enabled": "scalingPlanEnabled",
    },
)
class VirtualDesktopScalingPlanHostPool:
    def __init__(
        self,
        *,
        hostpool_id: builtins.str,
        scaling_plan_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param hostpool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#hostpool_id VirtualDesktopScalingPlan#hostpool_id}.
        :param scaling_plan_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#scaling_plan_enabled VirtualDesktopScalingPlan#scaling_plan_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b357c42ede400a109362ed9a77ee18b8620fdcce7a9a74c5b4c0b6ad128eedf6)
            check_type(argname="argument hostpool_id", value=hostpool_id, expected_type=type_hints["hostpool_id"])
            check_type(argname="argument scaling_plan_enabled", value=scaling_plan_enabled, expected_type=type_hints["scaling_plan_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostpool_id": hostpool_id,
            "scaling_plan_enabled": scaling_plan_enabled,
        }

    @builtins.property
    def hostpool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#hostpool_id VirtualDesktopScalingPlan#hostpool_id}.'''
        result = self._values.get("hostpool_id")
        assert result is not None, "Required property 'hostpool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scaling_plan_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#scaling_plan_enabled VirtualDesktopScalingPlan#scaling_plan_enabled}.'''
        result = self._values.get("scaling_plan_enabled")
        assert result is not None, "Required property 'scaling_plan_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopScalingPlanHostPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopScalingPlanHostPoolList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanHostPoolList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__737a29b73f98c49534f871ac13a51fda736728e449fa9236bc28304ab2caa9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualDesktopScalingPlanHostPoolOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5794e74453455d28b288fa084734d8b92abbd14ff3887cff85647131889a1587)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualDesktopScalingPlanHostPoolOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ad7e41e8ce83cc80a3797396d9e709e93f303c2ab8377fe28278ff30d7ed8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80094b8975c0597105a56049512c3159235cdf59d0e3a24c0256b00958b59669)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76c541e2174573d6958d0ee3d39aa17b0f0518449c07d8ce29d2f85379c523b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanHostPool]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanHostPool]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanHostPool]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f0a6c860c54974b12ed22e824656577d221e3f277059be6ab916ae775eaed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualDesktopScalingPlanHostPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanHostPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3da9b19ff0ec33eca8212df15b8a53eb35326daa2b7a60ad63693fd5fe261518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hostpoolIdInput")
    def hostpool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostpoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingPlanEnabledInput")
    def scaling_plan_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scalingPlanEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostpoolId")
    def hostpool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostpoolId"))

    @hostpool_id.setter
    def hostpool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d514603d6aee05dda7a1460afda93e288f552d878ce2f9cf6ff46aaf2f8c7e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostpoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingPlanEnabled")
    def scaling_plan_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scalingPlanEnabled"))

    @scaling_plan_enabled.setter
    def scaling_plan_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e9e28519df5c00b84ee57cbaa55a9291588438b4309399cf905a19311210e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingPlanEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanHostPool]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanHostPool]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanHostPool]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0891627c569f5ce2dc5fa53db829b91942a87fb2f1629cecb0478955f5d5fc14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "name": "name",
        "off_peak_load_balancing_algorithm": "offPeakLoadBalancingAlgorithm",
        "off_peak_start_time": "offPeakStartTime",
        "peak_load_balancing_algorithm": "peakLoadBalancingAlgorithm",
        "peak_start_time": "peakStartTime",
        "ramp_down_capacity_threshold_percent": "rampDownCapacityThresholdPercent",
        "ramp_down_force_logoff_users": "rampDownForceLogoffUsers",
        "ramp_down_load_balancing_algorithm": "rampDownLoadBalancingAlgorithm",
        "ramp_down_minimum_hosts_percent": "rampDownMinimumHostsPercent",
        "ramp_down_notification_message": "rampDownNotificationMessage",
        "ramp_down_start_time": "rampDownStartTime",
        "ramp_down_stop_hosts_when": "rampDownStopHostsWhen",
        "ramp_down_wait_time_minutes": "rampDownWaitTimeMinutes",
        "ramp_up_load_balancing_algorithm": "rampUpLoadBalancingAlgorithm",
        "ramp_up_start_time": "rampUpStartTime",
        "ramp_up_capacity_threshold_percent": "rampUpCapacityThresholdPercent",
        "ramp_up_minimum_hosts_percent": "rampUpMinimumHostsPercent",
    },
)
class VirtualDesktopScalingPlanSchedule:
    def __init__(
        self,
        *,
        days_of_week: typing.Sequence[builtins.str],
        name: builtins.str,
        off_peak_load_balancing_algorithm: builtins.str,
        off_peak_start_time: builtins.str,
        peak_load_balancing_algorithm: builtins.str,
        peak_start_time: builtins.str,
        ramp_down_capacity_threshold_percent: jsii.Number,
        ramp_down_force_logoff_users: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        ramp_down_load_balancing_algorithm: builtins.str,
        ramp_down_minimum_hosts_percent: jsii.Number,
        ramp_down_notification_message: builtins.str,
        ramp_down_start_time: builtins.str,
        ramp_down_stop_hosts_when: builtins.str,
        ramp_down_wait_time_minutes: jsii.Number,
        ramp_up_load_balancing_algorithm: builtins.str,
        ramp_up_start_time: builtins.str,
        ramp_up_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
        ramp_up_minimum_hosts_percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#days_of_week VirtualDesktopScalingPlan#days_of_week}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#name VirtualDesktopScalingPlan#name}.
        :param off_peak_load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#off_peak_load_balancing_algorithm VirtualDesktopScalingPlan#off_peak_load_balancing_algorithm}.
        :param off_peak_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#off_peak_start_time VirtualDesktopScalingPlan#off_peak_start_time}.
        :param peak_load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#peak_load_balancing_algorithm VirtualDesktopScalingPlan#peak_load_balancing_algorithm}.
        :param peak_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#peak_start_time VirtualDesktopScalingPlan#peak_start_time}.
        :param ramp_down_capacity_threshold_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_capacity_threshold_percent VirtualDesktopScalingPlan#ramp_down_capacity_threshold_percent}.
        :param ramp_down_force_logoff_users: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_force_logoff_users VirtualDesktopScalingPlan#ramp_down_force_logoff_users}.
        :param ramp_down_load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_load_balancing_algorithm VirtualDesktopScalingPlan#ramp_down_load_balancing_algorithm}.
        :param ramp_down_minimum_hosts_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_minimum_hosts_percent VirtualDesktopScalingPlan#ramp_down_minimum_hosts_percent}.
        :param ramp_down_notification_message: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_notification_message VirtualDesktopScalingPlan#ramp_down_notification_message}.
        :param ramp_down_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_start_time VirtualDesktopScalingPlan#ramp_down_start_time}.
        :param ramp_down_stop_hosts_when: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_stop_hosts_when VirtualDesktopScalingPlan#ramp_down_stop_hosts_when}.
        :param ramp_down_wait_time_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_wait_time_minutes VirtualDesktopScalingPlan#ramp_down_wait_time_minutes}.
        :param ramp_up_load_balancing_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_load_balancing_algorithm VirtualDesktopScalingPlan#ramp_up_load_balancing_algorithm}.
        :param ramp_up_start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_start_time VirtualDesktopScalingPlan#ramp_up_start_time}.
        :param ramp_up_capacity_threshold_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_capacity_threshold_percent VirtualDesktopScalingPlan#ramp_up_capacity_threshold_percent}.
        :param ramp_up_minimum_hosts_percent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_minimum_hosts_percent VirtualDesktopScalingPlan#ramp_up_minimum_hosts_percent}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ce758f604a989e16f5b18f7663d84d811bb4808a832ec73cf0768aff463f6c)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument off_peak_load_balancing_algorithm", value=off_peak_load_balancing_algorithm, expected_type=type_hints["off_peak_load_balancing_algorithm"])
            check_type(argname="argument off_peak_start_time", value=off_peak_start_time, expected_type=type_hints["off_peak_start_time"])
            check_type(argname="argument peak_load_balancing_algorithm", value=peak_load_balancing_algorithm, expected_type=type_hints["peak_load_balancing_algorithm"])
            check_type(argname="argument peak_start_time", value=peak_start_time, expected_type=type_hints["peak_start_time"])
            check_type(argname="argument ramp_down_capacity_threshold_percent", value=ramp_down_capacity_threshold_percent, expected_type=type_hints["ramp_down_capacity_threshold_percent"])
            check_type(argname="argument ramp_down_force_logoff_users", value=ramp_down_force_logoff_users, expected_type=type_hints["ramp_down_force_logoff_users"])
            check_type(argname="argument ramp_down_load_balancing_algorithm", value=ramp_down_load_balancing_algorithm, expected_type=type_hints["ramp_down_load_balancing_algorithm"])
            check_type(argname="argument ramp_down_minimum_hosts_percent", value=ramp_down_minimum_hosts_percent, expected_type=type_hints["ramp_down_minimum_hosts_percent"])
            check_type(argname="argument ramp_down_notification_message", value=ramp_down_notification_message, expected_type=type_hints["ramp_down_notification_message"])
            check_type(argname="argument ramp_down_start_time", value=ramp_down_start_time, expected_type=type_hints["ramp_down_start_time"])
            check_type(argname="argument ramp_down_stop_hosts_when", value=ramp_down_stop_hosts_when, expected_type=type_hints["ramp_down_stop_hosts_when"])
            check_type(argname="argument ramp_down_wait_time_minutes", value=ramp_down_wait_time_minutes, expected_type=type_hints["ramp_down_wait_time_minutes"])
            check_type(argname="argument ramp_up_load_balancing_algorithm", value=ramp_up_load_balancing_algorithm, expected_type=type_hints["ramp_up_load_balancing_algorithm"])
            check_type(argname="argument ramp_up_start_time", value=ramp_up_start_time, expected_type=type_hints["ramp_up_start_time"])
            check_type(argname="argument ramp_up_capacity_threshold_percent", value=ramp_up_capacity_threshold_percent, expected_type=type_hints["ramp_up_capacity_threshold_percent"])
            check_type(argname="argument ramp_up_minimum_hosts_percent", value=ramp_up_minimum_hosts_percent, expected_type=type_hints["ramp_up_minimum_hosts_percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_of_week": days_of_week,
            "name": name,
            "off_peak_load_balancing_algorithm": off_peak_load_balancing_algorithm,
            "off_peak_start_time": off_peak_start_time,
            "peak_load_balancing_algorithm": peak_load_balancing_algorithm,
            "peak_start_time": peak_start_time,
            "ramp_down_capacity_threshold_percent": ramp_down_capacity_threshold_percent,
            "ramp_down_force_logoff_users": ramp_down_force_logoff_users,
            "ramp_down_load_balancing_algorithm": ramp_down_load_balancing_algorithm,
            "ramp_down_minimum_hosts_percent": ramp_down_minimum_hosts_percent,
            "ramp_down_notification_message": ramp_down_notification_message,
            "ramp_down_start_time": ramp_down_start_time,
            "ramp_down_stop_hosts_when": ramp_down_stop_hosts_when,
            "ramp_down_wait_time_minutes": ramp_down_wait_time_minutes,
            "ramp_up_load_balancing_algorithm": ramp_up_load_balancing_algorithm,
            "ramp_up_start_time": ramp_up_start_time,
        }
        if ramp_up_capacity_threshold_percent is not None:
            self._values["ramp_up_capacity_threshold_percent"] = ramp_up_capacity_threshold_percent
        if ramp_up_minimum_hosts_percent is not None:
            self._values["ramp_up_minimum_hosts_percent"] = ramp_up_minimum_hosts_percent

    @builtins.property
    def days_of_week(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#days_of_week VirtualDesktopScalingPlan#days_of_week}.'''
        result = self._values.get("days_of_week")
        assert result is not None, "Required property 'days_of_week' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#name VirtualDesktopScalingPlan#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def off_peak_load_balancing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#off_peak_load_balancing_algorithm VirtualDesktopScalingPlan#off_peak_load_balancing_algorithm}.'''
        result = self._values.get("off_peak_load_balancing_algorithm")
        assert result is not None, "Required property 'off_peak_load_balancing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def off_peak_start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#off_peak_start_time VirtualDesktopScalingPlan#off_peak_start_time}.'''
        result = self._values.get("off_peak_start_time")
        assert result is not None, "Required property 'off_peak_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peak_load_balancing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#peak_load_balancing_algorithm VirtualDesktopScalingPlan#peak_load_balancing_algorithm}.'''
        result = self._values.get("peak_load_balancing_algorithm")
        assert result is not None, "Required property 'peak_load_balancing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peak_start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#peak_start_time VirtualDesktopScalingPlan#peak_start_time}.'''
        result = self._values.get("peak_start_time")
        assert result is not None, "Required property 'peak_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_down_capacity_threshold_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_capacity_threshold_percent VirtualDesktopScalingPlan#ramp_down_capacity_threshold_percent}.'''
        result = self._values.get("ramp_down_capacity_threshold_percent")
        assert result is not None, "Required property 'ramp_down_capacity_threshold_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ramp_down_force_logoff_users(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_force_logoff_users VirtualDesktopScalingPlan#ramp_down_force_logoff_users}.'''
        result = self._values.get("ramp_down_force_logoff_users")
        assert result is not None, "Required property 'ramp_down_force_logoff_users' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def ramp_down_load_balancing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_load_balancing_algorithm VirtualDesktopScalingPlan#ramp_down_load_balancing_algorithm}.'''
        result = self._values.get("ramp_down_load_balancing_algorithm")
        assert result is not None, "Required property 'ramp_down_load_balancing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_down_minimum_hosts_percent(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_minimum_hosts_percent VirtualDesktopScalingPlan#ramp_down_minimum_hosts_percent}.'''
        result = self._values.get("ramp_down_minimum_hosts_percent")
        assert result is not None, "Required property 'ramp_down_minimum_hosts_percent' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ramp_down_notification_message(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_notification_message VirtualDesktopScalingPlan#ramp_down_notification_message}.'''
        result = self._values.get("ramp_down_notification_message")
        assert result is not None, "Required property 'ramp_down_notification_message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_down_start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_start_time VirtualDesktopScalingPlan#ramp_down_start_time}.'''
        result = self._values.get("ramp_down_start_time")
        assert result is not None, "Required property 'ramp_down_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_down_stop_hosts_when(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_stop_hosts_when VirtualDesktopScalingPlan#ramp_down_stop_hosts_when}.'''
        result = self._values.get("ramp_down_stop_hosts_when")
        assert result is not None, "Required property 'ramp_down_stop_hosts_when' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_down_wait_time_minutes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_down_wait_time_minutes VirtualDesktopScalingPlan#ramp_down_wait_time_minutes}.'''
        result = self._values.get("ramp_down_wait_time_minutes")
        assert result is not None, "Required property 'ramp_down_wait_time_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ramp_up_load_balancing_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_load_balancing_algorithm VirtualDesktopScalingPlan#ramp_up_load_balancing_algorithm}.'''
        result = self._values.get("ramp_up_load_balancing_algorithm")
        assert result is not None, "Required property 'ramp_up_load_balancing_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_up_start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_start_time VirtualDesktopScalingPlan#ramp_up_start_time}.'''
        result = self._values.get("ramp_up_start_time")
        assert result is not None, "Required property 'ramp_up_start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ramp_up_capacity_threshold_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_capacity_threshold_percent VirtualDesktopScalingPlan#ramp_up_capacity_threshold_percent}.'''
        result = self._values.get("ramp_up_capacity_threshold_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ramp_up_minimum_hosts_percent(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#ramp_up_minimum_hosts_percent VirtualDesktopScalingPlan#ramp_up_minimum_hosts_percent}.'''
        result = self._values.get("ramp_up_minimum_hosts_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopScalingPlanSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopScalingPlanScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ae6f3e774073eea68098b5b6c68754255c3fa92786ff32d9900b487d096cfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualDesktopScalingPlanScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d766b63d7a45fc130e5f07a5ace1936f1c2d79d953c5487ace87872fd372847b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualDesktopScalingPlanScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a422fe74ef9092192a1c7cca8cfc3f4770eb754bfaff281f4296070576c567)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d816e43ad71d48640be555a52af9405c03fdd0fcd61ea8120a014bbcbac4c89f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e6c65fecb6e4cf660f7b187e320e92993d85a5e7748eaf751a713c595820f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanSchedule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanSchedule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanSchedule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63f2cf68dffacd068b9b013fffea617f31f513feda8d1acfb21b36fd0e3e7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VirtualDesktopScalingPlanScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2d84a5e5c06164f33c02ad5fed07f649fd47e5ff53c2ea255bf69716c1314b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRampUpCapacityThresholdPercent")
    def reset_ramp_up_capacity_threshold_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRampUpCapacityThresholdPercent", []))

    @jsii.member(jsii_name="resetRampUpMinimumHostsPercent")
    def reset_ramp_up_minimum_hosts_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRampUpMinimumHostsPercent", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="offPeakLoadBalancingAlgorithmInput")
    def off_peak_load_balancing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offPeakLoadBalancingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="offPeakStartTimeInput")
    def off_peak_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offPeakStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="peakLoadBalancingAlgorithmInput")
    def peak_load_balancing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peakLoadBalancingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="peakStartTimeInput")
    def peak_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peakStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownCapacityThresholdPercentInput")
    def ramp_down_capacity_threshold_percent_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rampDownCapacityThresholdPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownForceLogoffUsersInput")
    def ramp_down_force_logoff_users_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rampDownForceLogoffUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownLoadBalancingAlgorithmInput")
    def ramp_down_load_balancing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampDownLoadBalancingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownMinimumHostsPercentInput")
    def ramp_down_minimum_hosts_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rampDownMinimumHostsPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownNotificationMessageInput")
    def ramp_down_notification_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampDownNotificationMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownStartTimeInput")
    def ramp_down_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampDownStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownStopHostsWhenInput")
    def ramp_down_stop_hosts_when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampDownStopHostsWhenInput"))

    @builtins.property
    @jsii.member(jsii_name="rampDownWaitTimeMinutesInput")
    def ramp_down_wait_time_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rampDownWaitTimeMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="rampUpCapacityThresholdPercentInput")
    def ramp_up_capacity_threshold_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rampUpCapacityThresholdPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="rampUpLoadBalancingAlgorithmInput")
    def ramp_up_load_balancing_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampUpLoadBalancingAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="rampUpMinimumHostsPercentInput")
    def ramp_up_minimum_hosts_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rampUpMinimumHostsPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="rampUpStartTimeInput")
    def ramp_up_start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rampUpStartTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd02c2ab602e80b7a4be705c9173cfd32301709476593d2e2bf44ef3a34a6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b0ebeadf39d7fb60897dacaa10cd659b823c517d31e8a42e8e6dafe8a469a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offPeakLoadBalancingAlgorithm")
    def off_peak_load_balancing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offPeakLoadBalancingAlgorithm"))

    @off_peak_load_balancing_algorithm.setter
    def off_peak_load_balancing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51ab24e3287dcfc78e0c3fce9f6e1e00b19572f51a58865ca60391cff550441d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offPeakLoadBalancingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offPeakStartTime")
    def off_peak_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offPeakStartTime"))

    @off_peak_start_time.setter
    def off_peak_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1c066cabb1dc857194700592b4c50713d6d420d1597ec841aba7aa10ecd4cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offPeakStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peakLoadBalancingAlgorithm")
    def peak_load_balancing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peakLoadBalancingAlgorithm"))

    @peak_load_balancing_algorithm.setter
    def peak_load_balancing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117c3210db80e2a2c514667c2abb30e104ed047d19214318df65b632e6805657)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peakLoadBalancingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peakStartTime")
    def peak_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peakStartTime"))

    @peak_start_time.setter
    def peak_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b3907bc4034e97a08889c838ffa0c9b53e5a5216f8cf59d67b548f00297936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peakStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownCapacityThresholdPercent")
    def ramp_down_capacity_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rampDownCapacityThresholdPercent"))

    @ramp_down_capacity_threshold_percent.setter
    def ramp_down_capacity_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d4489d9bf13d6bd21db15e9e05c22fbee04ddb1aae6df7f43342504f5d49f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownCapacityThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownForceLogoffUsers")
    def ramp_down_force_logoff_users(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rampDownForceLogoffUsers"))

    @ramp_down_force_logoff_users.setter
    def ramp_down_force_logoff_users(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8857f3d93aeaf90c582afd4e7f4b4a62ab60c80d530147e2b8dc0ddaf1e0a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownForceLogoffUsers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownLoadBalancingAlgorithm")
    def ramp_down_load_balancing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampDownLoadBalancingAlgorithm"))

    @ramp_down_load_balancing_algorithm.setter
    def ramp_down_load_balancing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667d28a747a51c5490146308998b6ec10c958b4300ff24e3fcbc4aa2ac9d503a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownLoadBalancingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownMinimumHostsPercent")
    def ramp_down_minimum_hosts_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rampDownMinimumHostsPercent"))

    @ramp_down_minimum_hosts_percent.setter
    def ramp_down_minimum_hosts_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6d1c9c6824004eface55d86a21e705624bf0b8a9d99f2cc841a2cc07de2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownMinimumHostsPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownNotificationMessage")
    def ramp_down_notification_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampDownNotificationMessage"))

    @ramp_down_notification_message.setter
    def ramp_down_notification_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889dd04225cb39d1092fbb1cd22605d07d274931bb5f5f312539bc79ed6ddafb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownNotificationMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownStartTime")
    def ramp_down_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampDownStartTime"))

    @ramp_down_start_time.setter
    def ramp_down_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ad61b501acf786a5314a84af911ffac65045e12e42363aa2417c6cba4c0b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownStopHostsWhen")
    def ramp_down_stop_hosts_when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampDownStopHostsWhen"))

    @ramp_down_stop_hosts_when.setter
    def ramp_down_stop_hosts_when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeae0e058f2668356db7d007495b6f3c9a1a0119f7c7bdec987897d9d352f685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownStopHostsWhen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampDownWaitTimeMinutes")
    def ramp_down_wait_time_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rampDownWaitTimeMinutes"))

    @ramp_down_wait_time_minutes.setter
    def ramp_down_wait_time_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19d1db181735c8c050754a25fa14d209f83fecddc6f74c878249b968ad3cad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampDownWaitTimeMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampUpCapacityThresholdPercent")
    def ramp_up_capacity_threshold_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rampUpCapacityThresholdPercent"))

    @ramp_up_capacity_threshold_percent.setter
    def ramp_up_capacity_threshold_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055d815b8fb65a61bf805808f11c19f8a450e03567d179dbcae9363ed89e1b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampUpCapacityThresholdPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampUpLoadBalancingAlgorithm")
    def ramp_up_load_balancing_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampUpLoadBalancingAlgorithm"))

    @ramp_up_load_balancing_algorithm.setter
    def ramp_up_load_balancing_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6508dc18afa5339c58b72ec35f987497968a1c44ff12a8907cf20f3f70700f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampUpLoadBalancingAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampUpMinimumHostsPercent")
    def ramp_up_minimum_hosts_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rampUpMinimumHostsPercent"))

    @ramp_up_minimum_hosts_percent.setter
    def ramp_up_minimum_hosts_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e855d2063ad79f4db58ce7c55a26355b05522cd7445827b8a8938aadbee1fb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampUpMinimumHostsPercent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rampUpStartTime")
    def ramp_up_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rampUpStartTime"))

    @ramp_up_start_time.setter
    def ramp_up_start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351a3034ec6e68aa241f2eb466cd4684ca1e16abeebf60607e7cc2afc300d987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rampUpStartTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanSchedule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanSchedule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanSchedule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb08d1b1462164af46b98bfbe008da300923ec0f6a4fdc7a7ed0d204bf109615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VirtualDesktopScalingPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#create VirtualDesktopScalingPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#delete VirtualDesktopScalingPlan#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#read VirtualDesktopScalingPlan#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#update VirtualDesktopScalingPlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d19cc6027c254ca7f0973bdd9ef628ccb4acd5a03865d7d1b8003e6c41527c4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#create VirtualDesktopScalingPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#delete VirtualDesktopScalingPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#read VirtualDesktopScalingPlan#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/virtual_desktop_scaling_plan#update VirtualDesktopScalingPlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualDesktopScalingPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualDesktopScalingPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.virtualDesktopScalingPlan.VirtualDesktopScalingPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c3ce0a70c9cd90b0eba983ed675e3f59a56a6c13cf6d83418368ac7e13fff71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__239d5624a2b3905217f824f3b357eeeb115231d1aa5b270c554b2b0d64a190ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3dafcfb6c16bc83bd1bc75bc17af8b23a05c03459f08055bf35824b681f208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eb537d08c6828e64fd24e93ea511bd7da45475a03f3e156d12952bed89b761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ba020cf21a129564a66e46eecb2b088beacca74f0bee1cc97cbc89182ff288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba3cf7610c2a253aa163ff6ac9665d133ea465e534811dea8d8523bf523accf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VirtualDesktopScalingPlan",
    "VirtualDesktopScalingPlanConfig",
    "VirtualDesktopScalingPlanHostPool",
    "VirtualDesktopScalingPlanHostPoolList",
    "VirtualDesktopScalingPlanHostPoolOutputReference",
    "VirtualDesktopScalingPlanSchedule",
    "VirtualDesktopScalingPlanScheduleList",
    "VirtualDesktopScalingPlanScheduleOutputReference",
    "VirtualDesktopScalingPlanTimeouts",
    "VirtualDesktopScalingPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f0d5351a7e463d7a28c75d7fe570115c620fa8194d59ac8ffec54ad3545a06a9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanSchedule, typing.Dict[builtins.str, typing.Any]]]],
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    exclusion_tag: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    host_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanHostPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualDesktopScalingPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7b1d3812ecb2f445f47e28800fd111bd4cbed23e149b366a9b5c926eb2e8a961(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e67b01800fb1808da7ce9f1b5ff7016c0615cb1decd58ae1e5b5e3393fb9f2c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanHostPool, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9785381023afe7e57afc77d758ec97d1308ac42d954fdb9655b6df7d9b04be44(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanSchedule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b5f7e9e6023aa2d0a93d78b119f2e6da6f15257d27b9c73573e457d6376b9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d47db7880ef7c82a9eb5e38647b964ef02434accbba293f24a701d39f1e2971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce26f1b0096fbb37d9c508ae7b27f3e920f78434a541cb135c594f970a543868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0868354369ead2599de3e54a89e2cb410d1973d41d73657255e02cd07ec134a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01edf0c8ed984da2413f48f6104d677abb0b33980a88aa1c436621590dcefccb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ecf99e36fe92605eabe34e5970dea50e0dc3ddb2a6a3873166f0c52f510b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1465ea5f900db3597c9f21ba9fe08386ac3daa04322462db349600419c5320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41af813b87fdd0a834fb02ac46af2bb9743b0df51a174aa4c7aa56ea455fa19b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03b2a5958b819b9a1711de07128f1c3731bc2392a9028fa60a6a6947b859a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9560d40fb4ff9fbd2c9231c74be649dd05bee52711a88547e857d47e0a7755(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    schedule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanSchedule, typing.Dict[builtins.str, typing.Any]]]],
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    exclusion_tag: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    host_pool: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualDesktopScalingPlanHostPool, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VirtualDesktopScalingPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b357c42ede400a109362ed9a77ee18b8620fdcce7a9a74c5b4c0b6ad128eedf6(
    *,
    hostpool_id: builtins.str,
    scaling_plan_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737a29b73f98c49534f871ac13a51fda736728e449fa9236bc28304ab2caa9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5794e74453455d28b288fa084734d8b92abbd14ff3887cff85647131889a1587(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ad7e41e8ce83cc80a3797396d9e709e93f303c2ab8377fe28278ff30d7ed8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80094b8975c0597105a56049512c3159235cdf59d0e3a24c0256b00958b59669(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c541e2174573d6958d0ee3d39aa17b0f0518449c07d8ce29d2f85379c523b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f0a6c860c54974b12ed22e824656577d221e3f277059be6ab916ae775eaed8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanHostPool]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da9b19ff0ec33eca8212df15b8a53eb35326daa2b7a60ad63693fd5fe261518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d514603d6aee05dda7a1460afda93e288f552d878ce2f9cf6ff46aaf2f8c7e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e9e28519df5c00b84ee57cbaa55a9291588438b4309399cf905a19311210e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0891627c569f5ce2dc5fa53db829b91942a87fb2f1629cecb0478955f5d5fc14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanHostPool]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ce758f604a989e16f5b18f7663d84d811bb4808a832ec73cf0768aff463f6c(
    *,
    days_of_week: typing.Sequence[builtins.str],
    name: builtins.str,
    off_peak_load_balancing_algorithm: builtins.str,
    off_peak_start_time: builtins.str,
    peak_load_balancing_algorithm: builtins.str,
    peak_start_time: builtins.str,
    ramp_down_capacity_threshold_percent: jsii.Number,
    ramp_down_force_logoff_users: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ramp_down_load_balancing_algorithm: builtins.str,
    ramp_down_minimum_hosts_percent: jsii.Number,
    ramp_down_notification_message: builtins.str,
    ramp_down_start_time: builtins.str,
    ramp_down_stop_hosts_when: builtins.str,
    ramp_down_wait_time_minutes: jsii.Number,
    ramp_up_load_balancing_algorithm: builtins.str,
    ramp_up_start_time: builtins.str,
    ramp_up_capacity_threshold_percent: typing.Optional[jsii.Number] = None,
    ramp_up_minimum_hosts_percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ae6f3e774073eea68098b5b6c68754255c3fa92786ff32d9900b487d096cfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d766b63d7a45fc130e5f07a5ace1936f1c2d79d953c5487ace87872fd372847b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a422fe74ef9092192a1c7cca8cfc3f4770eb754bfaff281f4296070576c567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d816e43ad71d48640be555a52af9405c03fdd0fcd61ea8120a014bbcbac4c89f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e6c65fecb6e4cf660f7b187e320e92993d85a5e7748eaf751a713c595820f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63f2cf68dffacd068b9b013fffea617f31f513feda8d1acfb21b36fd0e3e7e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualDesktopScalingPlanSchedule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d84a5e5c06164f33c02ad5fed07f649fd47e5ff53c2ea255bf69716c1314b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd02c2ab602e80b7a4be705c9173cfd32301709476593d2e2bf44ef3a34a6b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b0ebeadf39d7fb60897dacaa10cd659b823c517d31e8a42e8e6dafe8a469a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51ab24e3287dcfc78e0c3fce9f6e1e00b19572f51a58865ca60391cff550441d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1c066cabb1dc857194700592b4c50713d6d420d1597ec841aba7aa10ecd4cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117c3210db80e2a2c514667c2abb30e104ed047d19214318df65b632e6805657(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b3907bc4034e97a08889c838ffa0c9b53e5a5216f8cf59d67b548f00297936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d4489d9bf13d6bd21db15e9e05c22fbee04ddb1aae6df7f43342504f5d49f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8857f3d93aeaf90c582afd4e7f4b4a62ab60c80d530147e2b8dc0ddaf1e0a2c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667d28a747a51c5490146308998b6ec10c958b4300ff24e3fcbc4aa2ac9d503a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6d1c9c6824004eface55d86a21e705624bf0b8a9d99f2cc841a2cc07de2e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889dd04225cb39d1092fbb1cd22605d07d274931bb5f5f312539bc79ed6ddafb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ad61b501acf786a5314a84af911ffac65045e12e42363aa2417c6cba4c0b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeae0e058f2668356db7d007495b6f3c9a1a0119f7c7bdec987897d9d352f685(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19d1db181735c8c050754a25fa14d209f83fecddc6f74c878249b968ad3cad4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055d815b8fb65a61bf805808f11c19f8a450e03567d179dbcae9363ed89e1b43(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6508dc18afa5339c58b72ec35f987497968a1c44ff12a8907cf20f3f70700f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e855d2063ad79f4db58ce7c55a26355b05522cd7445827b8a8938aadbee1fb9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351a3034ec6e68aa241f2eb466cd4684ca1e16abeebf60607e7cc2afc300d987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb08d1b1462164af46b98bfbe008da300923ec0f6a4fdc7a7ed0d204bf109615(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanSchedule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d19cc6027c254ca7f0973bdd9ef628ccb4acd5a03865d7d1b8003e6c41527c4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3ce0a70c9cd90b0eba983ed675e3f59a56a6c13cf6d83418368ac7e13fff71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__239d5624a2b3905217f824f3b357eeeb115231d1aa5b270c554b2b0d64a190ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3dafcfb6c16bc83bd1bc75bc17af8b23a05c03459f08055bf35824b681f208(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eb537d08c6828e64fd24e93ea511bd7da45475a03f3e156d12952bed89b761(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ba020cf21a129564a66e46eecb2b088beacca74f0bee1cc97cbc89182ff288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba3cf7610c2a253aa163ff6ac9665d133ea465e534811dea8d8523bf523accf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VirtualDesktopScalingPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

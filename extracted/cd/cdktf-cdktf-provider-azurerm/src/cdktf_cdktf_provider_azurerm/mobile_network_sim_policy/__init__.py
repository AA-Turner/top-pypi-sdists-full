r'''
# `azurerm_mobile_network_sim_policy`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_sim_policy`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy).
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


class MobileNetworkSimPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy azurerm_mobile_network_sim_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_slice_id: builtins.str,
        location: builtins.str,
        mobile_network_id: builtins.str,
        name: builtins.str,
        slice: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimPolicySlice", typing.Dict[builtins.str, typing.Any]]]],
        user_equipment_aggregate_maximum_bit_rate: typing.Union["MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        rat_frequency_selection_priority_index: typing.Optional[jsii.Number] = None,
        registration_timer_in_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkSimPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy azurerm_mobile_network_sim_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_slice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_slice_id MobileNetworkSimPolicy#default_slice_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#location MobileNetworkSimPolicy#location}.
        :param mobile_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#mobile_network_id MobileNetworkSimPolicy#mobile_network_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#name MobileNetworkSimPolicy#name}.
        :param slice: slice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#slice MobileNetworkSimPolicy#slice}
        :param user_equipment_aggregate_maximum_bit_rate: user_equipment_aggregate_maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#user_equipment_aggregate_maximum_bit_rate MobileNetworkSimPolicy#user_equipment_aggregate_maximum_bit_rate}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#id MobileNetworkSimPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rat_frequency_selection_priority_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#rat_frequency_selection_priority_index MobileNetworkSimPolicy#rat_frequency_selection_priority_index}.
        :param registration_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#registration_timer_in_seconds MobileNetworkSimPolicy#registration_timer_in_seconds}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#tags MobileNetworkSimPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#timeouts MobileNetworkSimPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047249f7269eaf267257b903bf8a7e018b8bdc9cb38c3ea3d0edad929d0aadc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkSimPolicyConfig(
            default_slice_id=default_slice_id,
            location=location,
            mobile_network_id=mobile_network_id,
            name=name,
            slice=slice,
            user_equipment_aggregate_maximum_bit_rate=user_equipment_aggregate_maximum_bit_rate,
            id=id,
            rat_frequency_selection_priority_index=rat_frequency_selection_priority_index,
            registration_timer_in_seconds=registration_timer_in_seconds,
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
        '''Generates CDKTF code for importing a MobileNetworkSimPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkSimPolicy to import.
        :param import_from_id: The id of the existing MobileNetworkSimPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkSimPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03df60266ef6e2c219f0d429d210112f457bde37713251b4f1e27dc9af5949a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSlice")
    def put_slice(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimPolicySlice", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f6b1252bcc9a69bd02aa9aa84ac830f311290baab9357f584fd6ccd75ed8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSlice", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#create MobileNetworkSimPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#delete MobileNetworkSimPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#read MobileNetworkSimPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#update MobileNetworkSimPolicy#update}.
        '''
        value = MobileNetworkSimPolicyTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserEquipmentAggregateMaximumBitRate")
    def put_user_equipment_aggregate_maximum_bit_rate(
        self,
        *,
        downlink: builtins.str,
        uplink: builtins.str,
    ) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.
        '''
        value = MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate(
            downlink=downlink, uplink=uplink
        )

        return typing.cast(None, jsii.invoke(self, "putUserEquipmentAggregateMaximumBitRate", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRatFrequencySelectionPriorityIndex")
    def reset_rat_frequency_selection_priority_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRatFrequencySelectionPriorityIndex", []))

    @jsii.member(jsii_name="resetRegistrationTimerInSeconds")
    def reset_registration_timer_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistrationTimerInSeconds", []))

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
    @jsii.member(jsii_name="slice")
    def slice(self) -> "MobileNetworkSimPolicySliceList":
        return typing.cast("MobileNetworkSimPolicySliceList", jsii.get(self, "slice"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MobileNetworkSimPolicyTimeoutsOutputReference":
        return typing.cast("MobileNetworkSimPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentAggregateMaximumBitRate")
    def user_equipment_aggregate_maximum_bit_rate(
        self,
    ) -> "MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRateOutputReference":
        return typing.cast("MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRateOutputReference", jsii.get(self, "userEquipmentAggregateMaximumBitRate"))

    @builtins.property
    @jsii.member(jsii_name="defaultSliceIdInput")
    def default_slice_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSliceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkIdInput")
    def mobile_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ratFrequencySelectionPriorityIndexInput")
    def rat_frequency_selection_priority_index_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ratFrequencySelectionPriorityIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="registrationTimerInSecondsInput")
    def registration_timer_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "registrationTimerInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="sliceInput")
    def slice_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySlice"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySlice"]]], jsii.get(self, "sliceInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkSimPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkSimPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userEquipmentAggregateMaximumBitRateInput")
    def user_equipment_aggregate_maximum_bit_rate_input(
        self,
    ) -> typing.Optional["MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate"]:
        return typing.cast(typing.Optional["MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate"], jsii.get(self, "userEquipmentAggregateMaximumBitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSliceId")
    def default_slice_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSliceId"))

    @default_slice_id.setter
    def default_slice_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7567f308bff1ab0a4ea70a23b4aabd874ef13997e608193bd8cb07a421975f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSliceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f337845c2d92052e130ea3477a33c2789ff07dda3c5d50c8a8fee404c16074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8718348f7a8e6a4713d7f1babe92180ab5ff8298e7480212b58c80f5e86f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkId")
    def mobile_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkId"))

    @mobile_network_id.setter
    def mobile_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc254605b384c2f4b8cff0ef292641a3447a0907153bbba63e6e58ed85635193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d64c923dc193fe537689ad389ecc25196a6fca806faafe5c721337cd165951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ratFrequencySelectionPriorityIndex")
    def rat_frequency_selection_priority_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ratFrequencySelectionPriorityIndex"))

    @rat_frequency_selection_priority_index.setter
    def rat_frequency_selection_priority_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173cc727c9149a94dfb91e57383e68ad1f63724f95e25d887eb26d8d0963a3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ratFrequencySelectionPriorityIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registrationTimerInSeconds")
    def registration_timer_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "registrationTimerInSeconds"))

    @registration_timer_in_seconds.setter
    def registration_timer_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ece9f758292c8879913c4a5f97c703dee0c82e3c8462864c11cf569cc8c8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registrationTimerInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b246bf664a1317120e1c411b81310886d24b0633dc61e5d650acad037c65e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_slice_id": "defaultSliceId",
        "location": "location",
        "mobile_network_id": "mobileNetworkId",
        "name": "name",
        "slice": "slice",
        "user_equipment_aggregate_maximum_bit_rate": "userEquipmentAggregateMaximumBitRate",
        "id": "id",
        "rat_frequency_selection_priority_index": "ratFrequencySelectionPriorityIndex",
        "registration_timer_in_seconds": "registrationTimerInSeconds",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MobileNetworkSimPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        default_slice_id: builtins.str,
        location: builtins.str,
        mobile_network_id: builtins.str,
        name: builtins.str,
        slice: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimPolicySlice", typing.Dict[builtins.str, typing.Any]]]],
        user_equipment_aggregate_maximum_bit_rate: typing.Union["MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        rat_frequency_selection_priority_index: typing.Optional[jsii.Number] = None,
        registration_timer_in_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkSimPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_slice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_slice_id MobileNetworkSimPolicy#default_slice_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#location MobileNetworkSimPolicy#location}.
        :param mobile_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#mobile_network_id MobileNetworkSimPolicy#mobile_network_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#name MobileNetworkSimPolicy#name}.
        :param slice: slice block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#slice MobileNetworkSimPolicy#slice}
        :param user_equipment_aggregate_maximum_bit_rate: user_equipment_aggregate_maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#user_equipment_aggregate_maximum_bit_rate MobileNetworkSimPolicy#user_equipment_aggregate_maximum_bit_rate}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#id MobileNetworkSimPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rat_frequency_selection_priority_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#rat_frequency_selection_priority_index MobileNetworkSimPolicy#rat_frequency_selection_priority_index}.
        :param registration_timer_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#registration_timer_in_seconds MobileNetworkSimPolicy#registration_timer_in_seconds}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#tags MobileNetworkSimPolicy#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#timeouts MobileNetworkSimPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(user_equipment_aggregate_maximum_bit_rate, dict):
            user_equipment_aggregate_maximum_bit_rate = MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate(**user_equipment_aggregate_maximum_bit_rate)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkSimPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f6d1e04a3ca5021de4b8db056821d16c4c6ee2edc3d622465417dffbfb492f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_slice_id", value=default_slice_id, expected_type=type_hints["default_slice_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mobile_network_id", value=mobile_network_id, expected_type=type_hints["mobile_network_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument slice", value=slice, expected_type=type_hints["slice"])
            check_type(argname="argument user_equipment_aggregate_maximum_bit_rate", value=user_equipment_aggregate_maximum_bit_rate, expected_type=type_hints["user_equipment_aggregate_maximum_bit_rate"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rat_frequency_selection_priority_index", value=rat_frequency_selection_priority_index, expected_type=type_hints["rat_frequency_selection_priority_index"])
            check_type(argname="argument registration_timer_in_seconds", value=registration_timer_in_seconds, expected_type=type_hints["registration_timer_in_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_slice_id": default_slice_id,
            "location": location,
            "mobile_network_id": mobile_network_id,
            "name": name,
            "slice": slice,
            "user_equipment_aggregate_maximum_bit_rate": user_equipment_aggregate_maximum_bit_rate,
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
        if id is not None:
            self._values["id"] = id
        if rat_frequency_selection_priority_index is not None:
            self._values["rat_frequency_selection_priority_index"] = rat_frequency_selection_priority_index
        if registration_timer_in_seconds is not None:
            self._values["registration_timer_in_seconds"] = registration_timer_in_seconds
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
    def default_slice_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_slice_id MobileNetworkSimPolicy#default_slice_id}.'''
        result = self._values.get("default_slice_id")
        assert result is not None, "Required property 'default_slice_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#location MobileNetworkSimPolicy#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#mobile_network_id MobileNetworkSimPolicy#mobile_network_id}.'''
        result = self._values.get("mobile_network_id")
        assert result is not None, "Required property 'mobile_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#name MobileNetworkSimPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slice(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySlice"]]:
        '''slice block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#slice MobileNetworkSimPolicy#slice}
        '''
        result = self._values.get("slice")
        assert result is not None, "Required property 'slice' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySlice"]], result)

    @builtins.property
    def user_equipment_aggregate_maximum_bit_rate(
        self,
    ) -> "MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate":
        '''user_equipment_aggregate_maximum_bit_rate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#user_equipment_aggregate_maximum_bit_rate MobileNetworkSimPolicy#user_equipment_aggregate_maximum_bit_rate}
        '''
        result = self._values.get("user_equipment_aggregate_maximum_bit_rate")
        assert result is not None, "Required property 'user_equipment_aggregate_maximum_bit_rate' is missing"
        return typing.cast("MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#id MobileNetworkSimPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rat_frequency_selection_priority_index(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#rat_frequency_selection_priority_index MobileNetworkSimPolicy#rat_frequency_selection_priority_index}.'''
        result = self._values.get("rat_frequency_selection_priority_index")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def registration_timer_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#registration_timer_in_seconds MobileNetworkSimPolicy#registration_timer_in_seconds}.'''
        result = self._values.get("registration_timer_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#tags MobileNetworkSimPolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MobileNetworkSimPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#timeouts MobileNetworkSimPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkSimPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySlice",
    jsii_struct_bases=[],
    name_mapping={
        "data_network": "dataNetwork",
        "default_data_network_id": "defaultDataNetworkId",
        "slice_id": "sliceId",
    },
)
class MobileNetworkSimPolicySlice:
    def __init__(
        self,
        *,
        data_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkSimPolicySliceDataNetwork", typing.Dict[builtins.str, typing.Any]]]],
        default_data_network_id: builtins.str,
        slice_id: builtins.str,
    ) -> None:
        '''
        :param data_network: data_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#data_network MobileNetworkSimPolicy#data_network}
        :param default_data_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_data_network_id MobileNetworkSimPolicy#default_data_network_id}.
        :param slice_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#slice_id MobileNetworkSimPolicy#slice_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75815374457a924e44130f2ece6d665da5861b5be68614d69eeac6ad69e32b79)
            check_type(argname="argument data_network", value=data_network, expected_type=type_hints["data_network"])
            check_type(argname="argument default_data_network_id", value=default_data_network_id, expected_type=type_hints["default_data_network_id"])
            check_type(argname="argument slice_id", value=slice_id, expected_type=type_hints["slice_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_network": data_network,
            "default_data_network_id": default_data_network_id,
            "slice_id": slice_id,
        }

    @builtins.property
    def data_network(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySliceDataNetwork"]]:
        '''data_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#data_network MobileNetworkSimPolicy#data_network}
        '''
        result = self._values.get("data_network")
        assert result is not None, "Required property 'data_network' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkSimPolicySliceDataNetwork"]], result)

    @builtins.property
    def default_data_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_data_network_id MobileNetworkSimPolicy#default_data_network_id}.'''
        result = self._values.get("default_data_network_id")
        assert result is not None, "Required property 'default_data_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slice_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#slice_id MobileNetworkSimPolicy#slice_id}.'''
        result = self._values.get("slice_id")
        assert result is not None, "Required property 'slice_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicySlice(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceDataNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_services_ids": "allowedServicesIds",
        "data_network_id": "dataNetworkId",
        "qos_indicator": "qosIndicator",
        "session_aggregate_maximum_bit_rate": "sessionAggregateMaximumBitRate",
        "additional_allowed_session_types": "additionalAllowedSessionTypes",
        "allocation_and_retention_priority_level": "allocationAndRetentionPriorityLevel",
        "default_session_type": "defaultSessionType",
        "max_buffered_packets": "maxBufferedPackets",
        "preemption_capability": "preemptionCapability",
        "preemption_vulnerability": "preemptionVulnerability",
    },
)
class MobileNetworkSimPolicySliceDataNetwork:
    def __init__(
        self,
        *,
        allowed_services_ids: typing.Sequence[builtins.str],
        data_network_id: builtins.str,
        qos_indicator: jsii.Number,
        session_aggregate_maximum_bit_rate: typing.Union["MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        additional_allowed_session_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
        default_session_type: typing.Optional[builtins.str] = None,
        max_buffered_packets: typing.Optional[jsii.Number] = None,
        preemption_capability: typing.Optional[builtins.str] = None,
        preemption_vulnerability: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allowed_services_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#allowed_services_ids MobileNetworkSimPolicy#allowed_services_ids}.
        :param data_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#data_network_id MobileNetworkSimPolicy#data_network_id}.
        :param qos_indicator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#qos_indicator MobileNetworkSimPolicy#qos_indicator}.
        :param session_aggregate_maximum_bit_rate: session_aggregate_maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#session_aggregate_maximum_bit_rate MobileNetworkSimPolicy#session_aggregate_maximum_bit_rate}
        :param additional_allowed_session_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#additional_allowed_session_types MobileNetworkSimPolicy#additional_allowed_session_types}.
        :param allocation_and_retention_priority_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#allocation_and_retention_priority_level MobileNetworkSimPolicy#allocation_and_retention_priority_level}.
        :param default_session_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_session_type MobileNetworkSimPolicy#default_session_type}.
        :param max_buffered_packets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#max_buffered_packets MobileNetworkSimPolicy#max_buffered_packets}.
        :param preemption_capability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#preemption_capability MobileNetworkSimPolicy#preemption_capability}.
        :param preemption_vulnerability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#preemption_vulnerability MobileNetworkSimPolicy#preemption_vulnerability}.
        '''
        if isinstance(session_aggregate_maximum_bit_rate, dict):
            session_aggregate_maximum_bit_rate = MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate(**session_aggregate_maximum_bit_rate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c30b14f49d4d325c254f8ce1753c02407b8aa36fe7ee2490aa2d6f8ce20716e)
            check_type(argname="argument allowed_services_ids", value=allowed_services_ids, expected_type=type_hints["allowed_services_ids"])
            check_type(argname="argument data_network_id", value=data_network_id, expected_type=type_hints["data_network_id"])
            check_type(argname="argument qos_indicator", value=qos_indicator, expected_type=type_hints["qos_indicator"])
            check_type(argname="argument session_aggregate_maximum_bit_rate", value=session_aggregate_maximum_bit_rate, expected_type=type_hints["session_aggregate_maximum_bit_rate"])
            check_type(argname="argument additional_allowed_session_types", value=additional_allowed_session_types, expected_type=type_hints["additional_allowed_session_types"])
            check_type(argname="argument allocation_and_retention_priority_level", value=allocation_and_retention_priority_level, expected_type=type_hints["allocation_and_retention_priority_level"])
            check_type(argname="argument default_session_type", value=default_session_type, expected_type=type_hints["default_session_type"])
            check_type(argname="argument max_buffered_packets", value=max_buffered_packets, expected_type=type_hints["max_buffered_packets"])
            check_type(argname="argument preemption_capability", value=preemption_capability, expected_type=type_hints["preemption_capability"])
            check_type(argname="argument preemption_vulnerability", value=preemption_vulnerability, expected_type=type_hints["preemption_vulnerability"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_services_ids": allowed_services_ids,
            "data_network_id": data_network_id,
            "qos_indicator": qos_indicator,
            "session_aggregate_maximum_bit_rate": session_aggregate_maximum_bit_rate,
        }
        if additional_allowed_session_types is not None:
            self._values["additional_allowed_session_types"] = additional_allowed_session_types
        if allocation_and_retention_priority_level is not None:
            self._values["allocation_and_retention_priority_level"] = allocation_and_retention_priority_level
        if default_session_type is not None:
            self._values["default_session_type"] = default_session_type
        if max_buffered_packets is not None:
            self._values["max_buffered_packets"] = max_buffered_packets
        if preemption_capability is not None:
            self._values["preemption_capability"] = preemption_capability
        if preemption_vulnerability is not None:
            self._values["preemption_vulnerability"] = preemption_vulnerability

    @builtins.property
    def allowed_services_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#allowed_services_ids MobileNetworkSimPolicy#allowed_services_ids}.'''
        result = self._values.get("allowed_services_ids")
        assert result is not None, "Required property 'allowed_services_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def data_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#data_network_id MobileNetworkSimPolicy#data_network_id}.'''
        result = self._values.get("data_network_id")
        assert result is not None, "Required property 'data_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qos_indicator(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#qos_indicator MobileNetworkSimPolicy#qos_indicator}.'''
        result = self._values.get("qos_indicator")
        assert result is not None, "Required property 'qos_indicator' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def session_aggregate_maximum_bit_rate(
        self,
    ) -> "MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate":
        '''session_aggregate_maximum_bit_rate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#session_aggregate_maximum_bit_rate MobileNetworkSimPolicy#session_aggregate_maximum_bit_rate}
        '''
        result = self._values.get("session_aggregate_maximum_bit_rate")
        assert result is not None, "Required property 'session_aggregate_maximum_bit_rate' is missing"
        return typing.cast("MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate", result)

    @builtins.property
    def additional_allowed_session_types(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#additional_allowed_session_types MobileNetworkSimPolicy#additional_allowed_session_types}.'''
        result = self._values.get("additional_allowed_session_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allocation_and_retention_priority_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#allocation_and_retention_priority_level MobileNetworkSimPolicy#allocation_and_retention_priority_level}.'''
        result = self._values.get("allocation_and_retention_priority_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_session_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#default_session_type MobileNetworkSimPolicy#default_session_type}.'''
        result = self._values.get("default_session_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_buffered_packets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#max_buffered_packets MobileNetworkSimPolicy#max_buffered_packets}.'''
        result = self._values.get("max_buffered_packets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemption_capability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#preemption_capability MobileNetworkSimPolicy#preemption_capability}.'''
        result = self._values.get("preemption_capability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemption_vulnerability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#preemption_vulnerability MobileNetworkSimPolicy#preemption_vulnerability}.'''
        result = self._values.get("preemption_vulnerability")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicySliceDataNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimPolicySliceDataNetworkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceDataNetworkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdb18fa123f0e2f889e01b49edd48b142aa838f35ec76c0af13fe6e076dc220d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MobileNetworkSimPolicySliceDataNetworkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137f48aa52631bb904224042d6ed433349613813a3924a3282c421c89c23957a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MobileNetworkSimPolicySliceDataNetworkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c3f306a3df0be8095d06287a53cebeff7644e2e4b680ff1ac37801f363a240)
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
            type_hints = typing.get_type_hints(_typecheckingstub__748f27ab12866d2cf1050ef44ca7e66af2a1464d3ed5d87509ad83203c5f47f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a4fd3093748043efe08a9972e8616f370c99a3780d851e1d796e1cf1da341d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3ee6421e6865b1f5af2dded6fff9f309ff5a95e6fa0ffeaeb0782887c1a17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkSimPolicySliceDataNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceDataNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d3ba48bda5d00f3baa546096f0430a03ef78aa1fb1163fb3cb5e0c85db5cbd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSessionAggregateMaximumBitRate")
    def put_session_aggregate_maximum_bit_rate(
        self,
        *,
        downlink: builtins.str,
        uplink: builtins.str,
    ) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.
        '''
        value = MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate(
            downlink=downlink, uplink=uplink
        )

        return typing.cast(None, jsii.invoke(self, "putSessionAggregateMaximumBitRate", [value]))

    @jsii.member(jsii_name="resetAdditionalAllowedSessionTypes")
    def reset_additional_allowed_session_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalAllowedSessionTypes", []))

    @jsii.member(jsii_name="resetAllocationAndRetentionPriorityLevel")
    def reset_allocation_and_retention_priority_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationAndRetentionPriorityLevel", []))

    @jsii.member(jsii_name="resetDefaultSessionType")
    def reset_default_session_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSessionType", []))

    @jsii.member(jsii_name="resetMaxBufferedPackets")
    def reset_max_buffered_packets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBufferedPackets", []))

    @jsii.member(jsii_name="resetPreemptionCapability")
    def reset_preemption_capability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionCapability", []))

    @jsii.member(jsii_name="resetPreemptionVulnerability")
    def reset_preemption_vulnerability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionVulnerability", []))

    @builtins.property
    @jsii.member(jsii_name="sessionAggregateMaximumBitRate")
    def session_aggregate_maximum_bit_rate(
        self,
    ) -> "MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRateOutputReference":
        return typing.cast("MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRateOutputReference", jsii.get(self, "sessionAggregateMaximumBitRate"))

    @builtins.property
    @jsii.member(jsii_name="additionalAllowedSessionTypesInput")
    def additional_allowed_session_types_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalAllowedSessionTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevelInput")
    def allocation_and_retention_priority_level_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocationAndRetentionPriorityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedServicesIdsInput")
    def allowed_services_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedServicesIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataNetworkIdInput")
    def data_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSessionTypeInput")
    def default_session_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSessionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBufferedPacketsInput")
    def max_buffered_packets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBufferedPacketsInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionCapabilityInput")
    def preemption_capability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionCapabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerabilityInput")
    def preemption_vulnerability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionVulnerabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="qosIndicatorInput")
    def qos_indicator_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosIndicatorInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAggregateMaximumBitRateInput")
    def session_aggregate_maximum_bit_rate_input(
        self,
    ) -> typing.Optional["MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate"]:
        return typing.cast(typing.Optional["MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate"], jsii.get(self, "sessionAggregateMaximumBitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalAllowedSessionTypes")
    def additional_allowed_session_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalAllowedSessionTypes"))

    @additional_allowed_session_types.setter
    def additional_allowed_session_types(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195835ed7bb0ec0394d1ee71bb9f8328c61d48a493e6e5412e2920d59df2c699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalAllowedSessionTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevel")
    def allocation_and_retention_priority_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocationAndRetentionPriorityLevel"))

    @allocation_and_retention_priority_level.setter
    def allocation_and_retention_priority_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7846e54c8b4bb69f7761cc3ad0a473e7124f518b2079f0378c68cd5b57bed29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationAndRetentionPriorityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedServicesIds")
    def allowed_services_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedServicesIds"))

    @allowed_services_ids.setter
    def allowed_services_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa41b78a6e2e6c3fcc1bcbdb2ed4cf3b9656ba6cc2f4ea3f986c172dca481c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedServicesIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataNetworkId")
    def data_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataNetworkId"))

    @data_network_id.setter
    def data_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9712f9564c3b28051dceb3d3cdeee28446db85ede4b8510fc455a19b1127e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSessionType")
    def default_session_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSessionType"))

    @default_session_type.setter
    def default_session_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361ccaf2e7f0bb084716132a6e02f7cf273a59fb4f1d0a0e24cc665a2ae2f977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSessionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBufferedPackets")
    def max_buffered_packets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBufferedPackets"))

    @max_buffered_packets.setter
    def max_buffered_packets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e64d76cecc32eccd41da11f2d76057610b46a9217fa8c1b0f1624aa43728f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBufferedPackets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionCapability")
    def preemption_capability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionCapability"))

    @preemption_capability.setter
    def preemption_capability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cbeffc77a60b5cca7c4c0d586e9457452627853619e6cc4ae77c6d9bc7378e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionCapability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerability")
    def preemption_vulnerability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionVulnerability"))

    @preemption_vulnerability.setter
    def preemption_vulnerability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc399d20be3876838aebedc08b69fc580009965384e1d4679db2c204fcc8848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionVulnerability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosIndicator")
    def qos_indicator(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qosIndicator"))

    @qos_indicator.setter
    def qos_indicator(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d219f0544467319af1578d3788958e1be2678f86dd9322e772999c09117523c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosIndicator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySliceDataNetwork]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySliceDataNetwork]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySliceDataNetwork]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87ca6c00f9c8514028bfaa3b219c12c9aa61296d41992e82896ac3a868776e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate",
    jsii_struct_bases=[],
    name_mapping={"downlink": "downlink", "uplink": "uplink"},
)
class MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate:
    def __init__(self, *, downlink: builtins.str, uplink: builtins.str) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d8ecf4f199993bbfe31053386923a8c172edd16ee7524c3b9ecb259463b23b)
            check_type(argname="argument downlink", value=downlink, expected_type=type_hints["downlink"])
            check_type(argname="argument uplink", value=uplink, expected_type=type_hints["uplink"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downlink": downlink,
            "uplink": uplink,
        }

    @builtins.property
    def downlink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.'''
        result = self._values.get("downlink")
        assert result is not None, "Required property 'downlink' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uplink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.'''
        result = self._values.get("uplink")
        assert result is not None, "Required property 'uplink' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8fb9eb86d0883abaf6b65b0e17926457cb322d858b1ed9333baeb6cc6ce08e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="downlinkInput")
    def downlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="uplinkInput")
    def uplink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uplinkInput"))

    @builtins.property
    @jsii.member(jsii_name="downlink")
    def downlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downlink"))

    @downlink.setter
    def downlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2105f4a70c7ce10f93a8a5fe50820547538bede76b86e0b78dc7c0efe9899214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uplink")
    def uplink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uplink"))

    @uplink.setter
    def uplink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1576c9a5afe8bd05197deaa8316181d755c49e3be080b8bf9d253316a182d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uplink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead22d38ed65409cd871820a610067a1fcd4b518ffd992091363f289c3e87f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkSimPolicySliceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__462a55185904371ee0f6d6737a4a8a83c8df48fa5f1b6fdc4956b082f2db47b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MobileNetworkSimPolicySliceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc61c07f6422e16f8bd4275cb29c77dab1252f8e30322761017431e603dd173)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MobileNetworkSimPolicySliceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7d459e381db3513b8a123da348ed8de87a74a793eb290c157b0793685b1897)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e409fbe4966082465414342a1c41f93ca7df5dd4fb12f010eb2b9d623701af5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae713d438d4f93ba03079753d951a4f28e2707e4af9980ad85e5074ebe9b6563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySlice]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySlice]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySlice]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eecae2b49b257b9971b7c9effbb3f97c07d3a420c44f77dc6075a5131c06df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkSimPolicySliceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicySliceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f449952707c70e10079f26efccae663d9d19b7f12d3c601e554220393448dd3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataNetwork")
    def put_data_network(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySliceDataNetwork, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87098dfe59d35b6007d913b49e34e29d885bcb622bf37b2e808b6e4c774a33c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataNetwork", [value]))

    @builtins.property
    @jsii.member(jsii_name="dataNetwork")
    def data_network(self) -> MobileNetworkSimPolicySliceDataNetworkList:
        return typing.cast(MobileNetworkSimPolicySliceDataNetworkList, jsii.get(self, "dataNetwork"))

    @builtins.property
    @jsii.member(jsii_name="dataNetworkInput")
    def data_network_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]], jsii.get(self, "dataNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDataNetworkIdInput")
    def default_data_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDataNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sliceIdInput")
    def slice_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sliceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDataNetworkId")
    def default_data_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDataNetworkId"))

    @default_data_network_id.setter
    def default_data_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa52216f98d0cd7636d32d380060511d1fe06526d5d5e077ee2f1ce41d1e9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDataNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sliceId")
    def slice_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sliceId"))

    @slice_id.setter
    def slice_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444241f8ca6591ac9a78d3a9176b8f85b761d1b7026442bc5595b370289ac1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sliceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySlice]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySlice]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySlice]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c42ab0d6dbd483f98a2235302298a89dd963ccb98c30d39544b88a78090cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkSimPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#create MobileNetworkSimPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#delete MobileNetworkSimPolicy#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#read MobileNetworkSimPolicy#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#update MobileNetworkSimPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16fa8bd751762a5dd2e32fc3ec8533e9122bc80657d6ba0e6409adda3513636)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#create MobileNetworkSimPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#delete MobileNetworkSimPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#read MobileNetworkSimPolicy#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#update MobileNetworkSimPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e131718485bb63930006664b7613b758133106ef040a7e0777182a2c603bb9f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caf7d61a977f3e0f39c7fb6dddc4d90de998b98b3f4bcf579b088853507e3e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__addde6cd74d9c9ee2f4219178537adfe23cd2e3e3efdbab14dda6f661ef7cdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c888f035cc2625fc5f0f2ce26fac75fc44a57eb66953aff096ee9e0c811ce1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa3ce201b257077ebabb0b317a950448675fd61f0cabfc08ae4ce57471e55ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ce87a9505a6ca3796f2ebb9ee3125724e0857f3bf12237eed85c0c220eee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate",
    jsii_struct_bases=[],
    name_mapping={"downlink": "downlink", "uplink": "uplink"},
)
class MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate:
    def __init__(self, *, downlink: builtins.str, uplink: builtins.str) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e495d5dc6c8973ff8aef6f83933366a349c5cfa41dc71ed8565b4a5a264f73ac)
            check_type(argname="argument downlink", value=downlink, expected_type=type_hints["downlink"])
            check_type(argname="argument uplink", value=uplink, expected_type=type_hints["uplink"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downlink": downlink,
            "uplink": uplink,
        }

    @builtins.property
    def downlink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#downlink MobileNetworkSimPolicy#downlink}.'''
        result = self._values.get("downlink")
        assert result is not None, "Required property 'downlink' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uplink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_sim_policy#uplink MobileNetworkSimPolicy#uplink}.'''
        result = self._values.get("uplink")
        assert result is not None, "Required property 'uplink' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkSimPolicy.MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__487410dc3f7d817697d49b240ae16b7cbe8ea5ca2a32c92cd9889087ab239935)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="downlinkInput")
    def downlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="uplinkInput")
    def uplink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uplinkInput"))

    @builtins.property
    @jsii.member(jsii_name="downlink")
    def downlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downlink"))

    @downlink.setter
    def downlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7011e03e841a715a7f4366134ad1f95b199ac8f373fd3ca8e72052da099fa808)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uplink")
    def uplink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uplink"))

    @uplink.setter
    def uplink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ffcc7034694820f72620e7968b129d220f7f46393780a9882deaa9ae45728d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uplink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c47995fe99ecf3aaa43ae165982ed7a879dfa3fa0a1ce2de77b9a5f0d1dfdefd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkSimPolicy",
    "MobileNetworkSimPolicyConfig",
    "MobileNetworkSimPolicySlice",
    "MobileNetworkSimPolicySliceDataNetwork",
    "MobileNetworkSimPolicySliceDataNetworkList",
    "MobileNetworkSimPolicySliceDataNetworkOutputReference",
    "MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate",
    "MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRateOutputReference",
    "MobileNetworkSimPolicySliceList",
    "MobileNetworkSimPolicySliceOutputReference",
    "MobileNetworkSimPolicyTimeouts",
    "MobileNetworkSimPolicyTimeoutsOutputReference",
    "MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate",
    "MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRateOutputReference",
]

publication.publish()

def _typecheckingstub__047249f7269eaf267257b903bf8a7e018b8bdc9cb38c3ea3d0edad929d0aadc6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_slice_id: builtins.str,
    location: builtins.str,
    mobile_network_id: builtins.str,
    name: builtins.str,
    slice: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySlice, typing.Dict[builtins.str, typing.Any]]]],
    user_equipment_aggregate_maximum_bit_rate: typing.Union[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    rat_frequency_selection_priority_index: typing.Optional[jsii.Number] = None,
    registration_timer_in_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkSimPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__03df60266ef6e2c219f0d429d210112f457bde37713251b4f1e27dc9af5949a8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f6b1252bcc9a69bd02aa9aa84ac830f311290baab9357f584fd6ccd75ed8b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySlice, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7567f308bff1ab0a4ea70a23b4aabd874ef13997e608193bd8cb07a421975f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f337845c2d92052e130ea3477a33c2789ff07dda3c5d50c8a8fee404c16074(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8718348f7a8e6a4713d7f1babe92180ab5ff8298e7480212b58c80f5e86f2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc254605b384c2f4b8cff0ef292641a3447a0907153bbba63e6e58ed85635193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d64c923dc193fe537689ad389ecc25196a6fca806faafe5c721337cd165951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173cc727c9149a94dfb91e57383e68ad1f63724f95e25d887eb26d8d0963a3b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ece9f758292c8879913c4a5f97c703dee0c82e3c8462864c11cf569cc8c8cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b246bf664a1317120e1c411b81310886d24b0633dc61e5d650acad037c65e64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f6d1e04a3ca5021de4b8db056821d16c4c6ee2edc3d622465417dffbfb492f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_slice_id: builtins.str,
    location: builtins.str,
    mobile_network_id: builtins.str,
    name: builtins.str,
    slice: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySlice, typing.Dict[builtins.str, typing.Any]]]],
    user_equipment_aggregate_maximum_bit_rate: typing.Union[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    rat_frequency_selection_priority_index: typing.Optional[jsii.Number] = None,
    registration_timer_in_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkSimPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75815374457a924e44130f2ece6d665da5861b5be68614d69eeac6ad69e32b79(
    *,
    data_network: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySliceDataNetwork, typing.Dict[builtins.str, typing.Any]]]],
    default_data_network_id: builtins.str,
    slice_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c30b14f49d4d325c254f8ce1753c02407b8aa36fe7ee2490aa2d6f8ce20716e(
    *,
    allowed_services_ids: typing.Sequence[builtins.str],
    data_network_id: builtins.str,
    qos_indicator: jsii.Number,
    session_aggregate_maximum_bit_rate: typing.Union[MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate, typing.Dict[builtins.str, typing.Any]],
    additional_allowed_session_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
    default_session_type: typing.Optional[builtins.str] = None,
    max_buffered_packets: typing.Optional[jsii.Number] = None,
    preemption_capability: typing.Optional[builtins.str] = None,
    preemption_vulnerability: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb18fa123f0e2f889e01b49edd48b142aa838f35ec76c0af13fe6e076dc220d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137f48aa52631bb904224042d6ed433349613813a3924a3282c421c89c23957a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c3f306a3df0be8095d06287a53cebeff7644e2e4b680ff1ac37801f363a240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748f27ab12866d2cf1050ef44ca7e66af2a1464d3ed5d87509ad83203c5f47f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4fd3093748043efe08a9972e8616f370c99a3780d851e1d796e1cf1da341d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3ee6421e6865b1f5af2dded6fff9f309ff5a95e6fa0ffeaeb0782887c1a17a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySliceDataNetwork]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3ba48bda5d00f3baa546096f0430a03ef78aa1fb1163fb3cb5e0c85db5cbd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195835ed7bb0ec0394d1ee71bb9f8328c61d48a493e6e5412e2920d59df2c699(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7846e54c8b4bb69f7761cc3ad0a473e7124f518b2079f0378c68cd5b57bed29(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa41b78a6e2e6c3fcc1bcbdb2ed4cf3b9656ba6cc2f4ea3f986c172dca481c7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9712f9564c3b28051dceb3d3cdeee28446db85ede4b8510fc455a19b1127e18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361ccaf2e7f0bb084716132a6e02f7cf273a59fb4f1d0a0e24cc665a2ae2f977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e64d76cecc32eccd41da11f2d76057610b46a9217fa8c1b0f1624aa43728f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cbeffc77a60b5cca7c4c0d586e9457452627853619e6cc4ae77c6d9bc7378e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc399d20be3876838aebedc08b69fc580009965384e1d4679db2c204fcc8848(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d219f0544467319af1578d3788958e1be2678f86dd9322e772999c09117523c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87ca6c00f9c8514028bfaa3b219c12c9aa61296d41992e82896ac3a868776e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySliceDataNetwork]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d8ecf4f199993bbfe31053386923a8c172edd16ee7524c3b9ecb259463b23b(
    *,
    downlink: builtins.str,
    uplink: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fb9eb86d0883abaf6b65b0e17926457cb322d858b1ed9333baeb6cc6ce08e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2105f4a70c7ce10f93a8a5fe50820547538bede76b86e0b78dc7c0efe9899214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1576c9a5afe8bd05197deaa8316181d755c49e3be080b8bf9d253316a182d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead22d38ed65409cd871820a610067a1fcd4b518ffd992091363f289c3e87f04(
    value: typing.Optional[MobileNetworkSimPolicySliceDataNetworkSessionAggregateMaximumBitRate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462a55185904371ee0f6d6737a4a8a83c8df48fa5f1b6fdc4956b082f2db47b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc61c07f6422e16f8bd4275cb29c77dab1252f8e30322761017431e603dd173(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7d459e381db3513b8a123da348ed8de87a74a793eb290c157b0793685b1897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e409fbe4966082465414342a1c41f93ca7df5dd4fb12f010eb2b9d623701af5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae713d438d4f93ba03079753d951a4f28e2707e4af9980ad85e5074ebe9b6563(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eecae2b49b257b9971b7c9effbb3f97c07d3a420c44f77dc6075a5131c06df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkSimPolicySlice]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f449952707c70e10079f26efccae663d9d19b7f12d3c601e554220393448dd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87098dfe59d35b6007d913b49e34e29d885bcb622bf37b2e808b6e4c774a33c7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkSimPolicySliceDataNetwork, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa52216f98d0cd7636d32d380060511d1fe06526d5d5e077ee2f1ce41d1e9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444241f8ca6591ac9a78d3a9176b8f85b761d1b7026442bc5595b370289ac1e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c42ab0d6dbd483f98a2235302298a89dd963ccb98c30d39544b88a78090cfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicySlice]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16fa8bd751762a5dd2e32fc3ec8533e9122bc80657d6ba0e6409adda3513636(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e131718485bb63930006664b7613b758133106ef040a7e0777182a2c603bb9f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf7d61a977f3e0f39c7fb6dddc4d90de998b98b3f4bcf579b088853507e3e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__addde6cd74d9c9ee2f4219178537adfe23cd2e3e3efdbab14dda6f661ef7cdc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c888f035cc2625fc5f0f2ce26fac75fc44a57eb66953aff096ee9e0c811ce1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa3ce201b257077ebabb0b317a950448675fd61f0cabfc08ae4ce57471e55ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ce87a9505a6ca3796f2ebb9ee3125724e0857f3bf12237eed85c0c220eee20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkSimPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e495d5dc6c8973ff8aef6f83933366a349c5cfa41dc71ed8565b4a5a264f73ac(
    *,
    downlink: builtins.str,
    uplink: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487410dc3f7d817697d49b240ae16b7cbe8ea5ca2a32c92cd9889087ab239935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7011e03e841a715a7f4366134ad1f95b199ac8f373fd3ca8e72052da099fa808(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ffcc7034694820f72620e7968b129d220f7f46393780a9882deaa9ae45728d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47995fe99ecf3aaa43ae165982ed7a879dfa3fa0a1ce2de77b9a5f0d1dfdefd(
    value: typing.Optional[MobileNetworkSimPolicyUserEquipmentAggregateMaximumBitRate],
) -> None:
    """Type checking stubs"""
    pass

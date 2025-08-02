r'''
# `opentelekomcloud_deh_host_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_deh_host_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1).
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


class DehHostV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1 opentelekomcloud_deh_host_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        host_type: builtins.str,
        name: builtins.str,
        auto_placement: typing.Optional[builtins.str] = None,
        available_instance_capacities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DehHostV1AvailableInstanceCapacities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        available_memory: typing.Optional[jsii.Number] = None,
        available_vcpus: typing.Optional[jsii.Number] = None,
        cores: typing.Optional[jsii.Number] = None,
        host_type_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_total: typing.Optional[jsii.Number] = None,
        instance_uuids: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        sockets: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DehHostV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcpus: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1 opentelekomcloud_deh_host_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#availability_zone DehHostV1#availability_zone}.
        :param host_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type DehHostV1#host_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#name DehHostV1#name}.
        :param auto_placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#auto_placement DehHostV1#auto_placement}.
        :param available_instance_capacities: available_instance_capacities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_instance_capacities DehHostV1#available_instance_capacities}
        :param available_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_memory DehHostV1#available_memory}.
        :param available_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_vcpus DehHostV1#available_vcpus}.
        :param cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#cores DehHostV1#cores}.
        :param host_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type_name DehHostV1#host_type_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#id DehHostV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_total: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_total DehHostV1#instance_total}.
        :param instance_uuids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_uuids DehHostV1#instance_uuids}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#memory DehHostV1#memory}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#region DehHostV1#region}.
        :param sockets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#sockets DehHostV1#sockets}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#status DehHostV1#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#tags DehHostV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#timeouts DehHostV1#timeouts}
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#vcpus DehHostV1#vcpus}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc4a509142d9d7f3e81c2f21ce48e4c4478805d3fc8968de78d5de1b4d7ff15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DehHostV1Config(
            availability_zone=availability_zone,
            host_type=host_type,
            name=name,
            auto_placement=auto_placement,
            available_instance_capacities=available_instance_capacities,
            available_memory=available_memory,
            available_vcpus=available_vcpus,
            cores=cores,
            host_type_name=host_type_name,
            id=id,
            instance_total=instance_total,
            instance_uuids=instance_uuids,
            memory=memory,
            region=region,
            sockets=sockets,
            status=status,
            tags=tags,
            timeouts=timeouts,
            vcpus=vcpus,
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
        '''Generates CDKTF code for importing a DehHostV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DehHostV1 to import.
        :param import_from_id: The id of the existing DehHostV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DehHostV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e48731d5285a2e59940d8bcf8ebfd73f8cd45a484deb6a4909455f808fdbcf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAvailableInstanceCapacities")
    def put_available_instance_capacities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DehHostV1AvailableInstanceCapacities", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee1d3b461bd52ea973339f4ad9a1b90cefdc0d9f00f6a97cca2df181c78682e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAvailableInstanceCapacities", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#create DehHostV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#delete DehHostV1#delete}.
        '''
        value = DehHostV1Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoPlacement")
    def reset_auto_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPlacement", []))

    @jsii.member(jsii_name="resetAvailableInstanceCapacities")
    def reset_available_instance_capacities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableInstanceCapacities", []))

    @jsii.member(jsii_name="resetAvailableMemory")
    def reset_available_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableMemory", []))

    @jsii.member(jsii_name="resetAvailableVcpus")
    def reset_available_vcpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailableVcpus", []))

    @jsii.member(jsii_name="resetCores")
    def reset_cores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCores", []))

    @jsii.member(jsii_name="resetHostTypeName")
    def reset_host_type_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostTypeName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceTotal")
    def reset_instance_total(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTotal", []))

    @jsii.member(jsii_name="resetInstanceUuids")
    def reset_instance_uuids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceUuids", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSockets")
    def reset_sockets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSockets", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVcpus")
    def reset_vcpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcpus", []))

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
    @jsii.member(jsii_name="availableInstanceCapacities")
    def available_instance_capacities(
        self,
    ) -> "DehHostV1AvailableInstanceCapacitiesList":
        return typing.cast("DehHostV1AvailableInstanceCapacitiesList", jsii.get(self, "availableInstanceCapacities"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DehHostV1TimeoutsOutputReference":
        return typing.cast("DehHostV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoPlacementInput")
    def auto_placement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="availableInstanceCapacitiesInput")
    def available_instance_capacities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DehHostV1AvailableInstanceCapacities"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DehHostV1AvailableInstanceCapacities"]]], jsii.get(self, "availableInstanceCapacitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="availableMemoryInput")
    def available_memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availableMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="availableVcpusInput")
    def available_vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availableVcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="coresInput")
    def cores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coresInput"))

    @builtins.property
    @jsii.member(jsii_name="hostTypeInput")
    def host_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="hostTypeNameInput")
    def host_type_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostTypeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTotalInput")
    def instance_total_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceTotalInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceUuidsInput")
    def instance_uuids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceUuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="socketsInput")
    def sockets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "socketsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DehHostV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DehHostV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vcpusInput")
    def vcpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vcpusInput"))

    @builtins.property
    @jsii.member(jsii_name="autoPlacement")
    def auto_placement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoPlacement"))

    @auto_placement.setter
    def auto_placement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e062397546a6403c31b2727065513af00456d5d80c55579a203fce50a8e5158)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPlacement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609b19c2ac976fca922afe83ef6fd77e5424cc7a73d60670700976823f1f0b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableMemory")
    def available_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableMemory"))

    @available_memory.setter
    def available_memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07b4b488b07d893ebdd38d28fb0f4929a6070bf275688310c9cbf426bf04c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableMemory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availableVcpus")
    def available_vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableVcpus"))

    @available_vcpus.setter
    def available_vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc5941234e31c9af92dca52949ae188c956888cef28e8bc013a99f0180baa11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availableVcpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cores")
    def cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cores"))

    @cores.setter
    def cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ea69db3cdc7354388342980d409d150e89f33abb2af0d0f6e7dce35d7afb2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cores", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostType")
    def host_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostType"))

    @host_type.setter
    def host_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148370e44725cdb6929c05b5485a9c0a46e2d8f9c9cfb4ecf5ab601a67c3745a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostTypeName")
    def host_type_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostTypeName"))

    @host_type_name.setter
    def host_type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5275b1adcef7c308ec034ee07e4d2f0f29c7b6335497439ead1ead4d223778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostTypeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401ed5b5c95a655114a52ae3567a3673344b6994903cb6d69be5fb669919e6ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTotal")
    def instance_total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceTotal"))

    @instance_total.setter
    def instance_total(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c182d6b5d5944f158afd5bd3705fc4ef7e0ceeb8dd18334eaf189a1f3694cadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTotal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceUuids")
    def instance_uuids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceUuids"))

    @instance_uuids.setter
    def instance_uuids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba00d31fac40713f437b1852a12817154bae404a220fb5ea56194a65afd878c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceUuids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49a963229a12acbbd551e1deb57cebea6e65c5be6f3d1172ea66fdbfa98682f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d63d66763c24672b53a792784819cfea9957a7869bd472d7d608bebe7b60d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235729e129dfca43c5dad7f53090c7a245a23a1c080caadd84181b3ab07f5893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sockets")
    def sockets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sockets"))

    @sockets.setter
    def sockets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b000d61c060650fa9e794f2df93bc6f990f9e8f695440dc6f7bf33a7db2d5b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sockets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb22db2b2cd26179bf3a7b388751732ed7e5ca27f79c28d0d19043e7ac6b5d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c6fc2ae2b2b1b0ca3fd3d2c093286b5c3d01fcc7c254558fef331c138e8c69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vcpus")
    def vcpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vcpus"))

    @vcpus.setter
    def vcpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ceca934faa0559f72c83ee581cfd261e33b961badeab33e70e850428a8c121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vcpus", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1AvailableInstanceCapacities",
    jsii_struct_bases=[],
    name_mapping={},
)
class DehHostV1AvailableInstanceCapacities:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DehHostV1AvailableInstanceCapacities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DehHostV1AvailableInstanceCapacitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1AvailableInstanceCapacitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49dff6f90018f760eb43f63ddda34602c79d0356ea1330ecd4737311e12d9a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DehHostV1AvailableInstanceCapacitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c984fc14b389d840d7e254218b74b4fd4ea914b12cf6a71fa6bc8f31aa42808)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DehHostV1AvailableInstanceCapacitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0e7040449f531fd9b85cfea0403ab6a87d2f4cadd2e5ce74dee63d861b73a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a73596ee8f8a841d08adb990e5ffbf71f4603ad8ee5c1856c4d9deb1cf01c8f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3103e3ad5c92c09776dc349d9036344be3c6777e0ffb68ea0dc2b329c9a5fcb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c608c767bed81540fbecdfcb98da61313c63d269b04dfb5cee8658607803b1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DehHostV1AvailableInstanceCapacitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1AvailableInstanceCapacitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4714095e6dc85143b036b7caabf868bf0359c1d44630647f9927f37337bd77fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavor"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1AvailableInstanceCapacities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1AvailableInstanceCapacities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1AvailableInstanceCapacities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa1d3a6939ede6b5c48dbd422a408bd453f6bca4bc9d14f9e2db036c32b8cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "host_type": "hostType",
        "name": "name",
        "auto_placement": "autoPlacement",
        "available_instance_capacities": "availableInstanceCapacities",
        "available_memory": "availableMemory",
        "available_vcpus": "availableVcpus",
        "cores": "cores",
        "host_type_name": "hostTypeName",
        "id": "id",
        "instance_total": "instanceTotal",
        "instance_uuids": "instanceUuids",
        "memory": "memory",
        "region": "region",
        "sockets": "sockets",
        "status": "status",
        "tags": "tags",
        "timeouts": "timeouts",
        "vcpus": "vcpus",
    },
)
class DehHostV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        host_type: builtins.str,
        name: builtins.str,
        auto_placement: typing.Optional[builtins.str] = None,
        available_instance_capacities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DehHostV1AvailableInstanceCapacities, typing.Dict[builtins.str, typing.Any]]]]] = None,
        available_memory: typing.Optional[jsii.Number] = None,
        available_vcpus: typing.Optional[jsii.Number] = None,
        cores: typing.Optional[jsii.Number] = None,
        host_type_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_total: typing.Optional[jsii.Number] = None,
        instance_uuids: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        sockets: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DehHostV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vcpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#availability_zone DehHostV1#availability_zone}.
        :param host_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type DehHostV1#host_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#name DehHostV1#name}.
        :param auto_placement: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#auto_placement DehHostV1#auto_placement}.
        :param available_instance_capacities: available_instance_capacities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_instance_capacities DehHostV1#available_instance_capacities}
        :param available_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_memory DehHostV1#available_memory}.
        :param available_vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_vcpus DehHostV1#available_vcpus}.
        :param cores: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#cores DehHostV1#cores}.
        :param host_type_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type_name DehHostV1#host_type_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#id DehHostV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_total: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_total DehHostV1#instance_total}.
        :param instance_uuids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_uuids DehHostV1#instance_uuids}.
        :param memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#memory DehHostV1#memory}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#region DehHostV1#region}.
        :param sockets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#sockets DehHostV1#sockets}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#status DehHostV1#status}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#tags DehHostV1#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#timeouts DehHostV1#timeouts}
        :param vcpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#vcpus DehHostV1#vcpus}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DehHostV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf301bacdbc72b8f2d1e047f6d56a342fe570dfc348e88e1e3925b175decc35)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument host_type", value=host_type, expected_type=type_hints["host_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_placement", value=auto_placement, expected_type=type_hints["auto_placement"])
            check_type(argname="argument available_instance_capacities", value=available_instance_capacities, expected_type=type_hints["available_instance_capacities"])
            check_type(argname="argument available_memory", value=available_memory, expected_type=type_hints["available_memory"])
            check_type(argname="argument available_vcpus", value=available_vcpus, expected_type=type_hints["available_vcpus"])
            check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
            check_type(argname="argument host_type_name", value=host_type_name, expected_type=type_hints["host_type_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_total", value=instance_total, expected_type=type_hints["instance_total"])
            check_type(argname="argument instance_uuids", value=instance_uuids, expected_type=type_hints["instance_uuids"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument sockets", value=sockets, expected_type=type_hints["sockets"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "host_type": host_type,
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
        if auto_placement is not None:
            self._values["auto_placement"] = auto_placement
        if available_instance_capacities is not None:
            self._values["available_instance_capacities"] = available_instance_capacities
        if available_memory is not None:
            self._values["available_memory"] = available_memory
        if available_vcpus is not None:
            self._values["available_vcpus"] = available_vcpus
        if cores is not None:
            self._values["cores"] = cores
        if host_type_name is not None:
            self._values["host_type_name"] = host_type_name
        if id is not None:
            self._values["id"] = id
        if instance_total is not None:
            self._values["instance_total"] = instance_total
        if instance_uuids is not None:
            self._values["instance_uuids"] = instance_uuids
        if memory is not None:
            self._values["memory"] = memory
        if region is not None:
            self._values["region"] = region
        if sockets is not None:
            self._values["sockets"] = sockets
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vcpus is not None:
            self._values["vcpus"] = vcpus

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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#availability_zone DehHostV1#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type DehHostV1#host_type}.'''
        result = self._values.get("host_type")
        assert result is not None, "Required property 'host_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#name DehHostV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_placement(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#auto_placement DehHostV1#auto_placement}.'''
        result = self._values.get("auto_placement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def available_instance_capacities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]]:
        '''available_instance_capacities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_instance_capacities DehHostV1#available_instance_capacities}
        '''
        result = self._values.get("available_instance_capacities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]], result)

    @builtins.property
    def available_memory(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_memory DehHostV1#available_memory}.'''
        result = self._values.get("available_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def available_vcpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#available_vcpus DehHostV1#available_vcpus}.'''
        result = self._values.get("available_vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cores(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#cores DehHostV1#cores}.'''
        result = self._values.get("cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host_type_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#host_type_name DehHostV1#host_type_name}.'''
        result = self._values.get("host_type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#id DehHostV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_total(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_total DehHostV1#instance_total}.'''
        result = self._values.get("instance_total")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_uuids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#instance_uuids DehHostV1#instance_uuids}.'''
        result = self._values.get("instance_uuids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#memory DehHostV1#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#region DehHostV1#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sockets(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#sockets DehHostV1#sockets}.'''
        result = self._values.get("sockets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#status DehHostV1#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#tags DehHostV1#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DehHostV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#timeouts DehHostV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DehHostV1Timeouts"], result)

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#vcpus DehHostV1#vcpus}.'''
        result = self._values.get("vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DehHostV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DehHostV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#create DehHostV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#delete DehHostV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4ba5ffdbb418f41d22be00c2b9eb197087594ced9415ee45271f8dc9ca31ed)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#create DehHostV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/deh_host_v1#delete DehHostV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DehHostV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DehHostV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dehHostV1.DehHostV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44021296489ceadaae80dc25c224111aed296b9986eb6ef0e4b74fbf0c7adbc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2177571a32e30dbe1492c6fbced4f16c866bd7e0279a1552821e884a1743b72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3355af4451b8d3d4c4cb7fea127d4740218f352e510763e655cbfd144d1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4d7fd3b24daf3a999ee3c4c303732769ebbfb2c855c4d0f13258d46b4833b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DehHostV1",
    "DehHostV1AvailableInstanceCapacities",
    "DehHostV1AvailableInstanceCapacitiesList",
    "DehHostV1AvailableInstanceCapacitiesOutputReference",
    "DehHostV1Config",
    "DehHostV1Timeouts",
    "DehHostV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ecc4a509142d9d7f3e81c2f21ce48e4c4478805d3fc8968de78d5de1b4d7ff15(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    host_type: builtins.str,
    name: builtins.str,
    auto_placement: typing.Optional[builtins.str] = None,
    available_instance_capacities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DehHostV1AvailableInstanceCapacities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_memory: typing.Optional[jsii.Number] = None,
    available_vcpus: typing.Optional[jsii.Number] = None,
    cores: typing.Optional[jsii.Number] = None,
    host_type_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_total: typing.Optional[jsii.Number] = None,
    instance_uuids: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    sockets: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DehHostV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcpus: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__d8e48731d5285a2e59940d8bcf8ebfd73f8cd45a484deb6a4909455f808fdbcf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee1d3b461bd52ea973339f4ad9a1b90cefdc0d9f00f6a97cca2df181c78682e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DehHostV1AvailableInstanceCapacities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e062397546a6403c31b2727065513af00456d5d80c55579a203fce50a8e5158(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609b19c2ac976fca922afe83ef6fd77e5424cc7a73d60670700976823f1f0b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07b4b488b07d893ebdd38d28fb0f4929a6070bf275688310c9cbf426bf04c83(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc5941234e31c9af92dca52949ae188c956888cef28e8bc013a99f0180baa11(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ea69db3cdc7354388342980d409d150e89f33abb2af0d0f6e7dce35d7afb2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148370e44725cdb6929c05b5485a9c0a46e2d8f9c9cfb4ecf5ab601a67c3745a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5275b1adcef7c308ec034ee07e4d2f0f29c7b6335497439ead1ead4d223778(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401ed5b5c95a655114a52ae3567a3673344b6994903cb6d69be5fb669919e6ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c182d6b5d5944f158afd5bd3705fc4ef7e0ceeb8dd18334eaf189a1f3694cadc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba00d31fac40713f437b1852a12817154bae404a220fb5ea56194a65afd878c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49a963229a12acbbd551e1deb57cebea6e65c5be6f3d1172ea66fdbfa98682f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d63d66763c24672b53a792784819cfea9957a7869bd472d7d608bebe7b60d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235729e129dfca43c5dad7f53090c7a245a23a1c080caadd84181b3ab07f5893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b000d61c060650fa9e794f2df93bc6f990f9e8f695440dc6f7bf33a7db2d5b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb22db2b2cd26179bf3a7b388751732ed7e5ca27f79c28d0d19043e7ac6b5d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c6fc2ae2b2b1b0ca3fd3d2c093286b5c3d01fcc7c254558fef331c138e8c69(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ceca934faa0559f72c83ee581cfd261e33b961badeab33e70e850428a8c121(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49dff6f90018f760eb43f63ddda34602c79d0356ea1330ecd4737311e12d9a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c984fc14b389d840d7e254218b74b4fd4ea914b12cf6a71fa6bc8f31aa42808(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0e7040449f531fd9b85cfea0403ab6a87d2f4cadd2e5ce74dee63d861b73a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73596ee8f8a841d08adb990e5ffbf71f4603ad8ee5c1856c4d9deb1cf01c8f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3103e3ad5c92c09776dc349d9036344be3c6777e0ffb68ea0dc2b329c9a5fcb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c608c767bed81540fbecdfcb98da61313c63d269b04dfb5cee8658607803b1a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DehHostV1AvailableInstanceCapacities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4714095e6dc85143b036b7caabf868bf0359c1d44630647f9927f37337bd77fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa1d3a6939ede6b5c48dbd422a408bd453f6bca4bc9d14f9e2db036c32b8cae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1AvailableInstanceCapacities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf301bacdbc72b8f2d1e047f6d56a342fe570dfc348e88e1e3925b175decc35(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    host_type: builtins.str,
    name: builtins.str,
    auto_placement: typing.Optional[builtins.str] = None,
    available_instance_capacities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DehHostV1AvailableInstanceCapacities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    available_memory: typing.Optional[jsii.Number] = None,
    available_vcpus: typing.Optional[jsii.Number] = None,
    cores: typing.Optional[jsii.Number] = None,
    host_type_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_total: typing.Optional[jsii.Number] = None,
    instance_uuids: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    sockets: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DehHostV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vcpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4ba5ffdbb418f41d22be00c2b9eb197087594ced9415ee45271f8dc9ca31ed(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44021296489ceadaae80dc25c224111aed296b9986eb6ef0e4b74fbf0c7adbc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2177571a32e30dbe1492c6fbced4f16c866bd7e0279a1552821e884a1743b72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3355af4451b8d3d4c4cb7fea127d4740218f352e510763e655cbfd144d1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4d7fd3b24daf3a999ee3c4c303732769ebbfb2c855c4d0f13258d46b4833b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DehHostV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

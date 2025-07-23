r'''
# `google_compute_resource_policy`

Refer to the Terraform Registry for docs: [`google_compute_resource_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy).
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


class ComputeResourcePolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy google_compute_resource_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disk_consistency_group_policy: typing.Optional[typing.Union["ComputeResourcePolicyDiskConsistencyGroupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        group_placement_policy: typing.Optional[typing.Union["ComputeResourcePolicyGroupPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_policy: typing.Optional[typing.Union["ComputeResourcePolicyWorkloadPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy google_compute_resource_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#name ComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#description ComputeResourcePolicy#description}
        :param disk_consistency_group_policy: disk_consistency_group_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#disk_consistency_group_policy ComputeResourcePolicy#disk_consistency_group_policy}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#id ComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#project ComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#region ComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
        :param workload_policy: workload_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#workload_policy ComputeResourcePolicy#workload_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3e16d2beae709200f3ea76b570bf0081c8efd00f7c347d2c6bc6389c8a0ebc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeResourcePolicyConfig(
            name=name,
            description=description,
            disk_consistency_group_policy=disk_consistency_group_policy,
            group_placement_policy=group_placement_policy,
            id=id,
            instance_schedule_policy=instance_schedule_policy,
            project=project,
            region=region,
            snapshot_schedule_policy=snapshot_schedule_policy,
            timeouts=timeouts,
            workload_policy=workload_policy,
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
        '''Generates CDKTF code for importing a ComputeResourcePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeResourcePolicy to import.
        :param import_from_id: The id of the existing ComputeResourcePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeResourcePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20acd42c7311578905ade1ec69242135b4cd24622a826a5c3212ec561b12c1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDiskConsistencyGroupPolicy")
    def put_disk_consistency_group_policy(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable disk consistency on the resource policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#enabled ComputeResourcePolicy#enabled}
        '''
        value = ComputeResourcePolicyDiskConsistencyGroupPolicy(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putDiskConsistencyGroupPolicy", [value]))

    @jsii.member(jsii_name="putGroupPlacementPolicy")
    def put_group_placement_policy(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        gpu_topology: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        :param gpu_topology: Specifies the shape of the GPU slice, in slice based GPU families eg. A4X. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#gpu_topology ComputeResourcePolicy#gpu_topology}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        value = ComputeResourcePolicyGroupPlacementPolicy(
            availability_domain_count=availability_domain_count,
            collocation=collocation,
            gpu_topology=gpu_topology,
            vm_count=vm_count,
        )

        return typing.cast(None, jsii.invoke(self, "putGroupPlacementPolicy", [value]))

    @jsii.member(jsii_name="putInstanceSchedulePolicy")
    def put_instance_schedule_policy(
        self,
        *,
        time_zone: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        vm_start_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicy(
            time_zone=time_zone,
            expiration_time=expiration_time,
            start_time=start_time,
            vm_start_schedule=vm_start_schedule,
            vm_stop_schedule=vm_stop_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceSchedulePolicy", [value]))

    @jsii.member(jsii_name="putSnapshotSchedulePolicy")
    def put_snapshot_schedule_policy(
        self,
        *,
        schedule: typing.Union["ComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[builtins.str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicy(
            schedule=schedule,
            retention_policy=retention_policy,
            snapshot_properties=snapshot_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotSchedulePolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#create ComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#delete ComputeResourcePolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#update ComputeResourcePolicy#update}.
        '''
        value = ComputeResourcePolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkloadPolicy")
    def put_workload_policy(
        self,
        *,
        type: builtins.str,
        accelerator_topology: typing.Optional[builtins.str] = None,
        max_topology_distance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of workload policy. Possible values: ["HIGH_AVAILABILITY", "HIGH_THROUGHPUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#type ComputeResourcePolicy#type}
        :param accelerator_topology: The accelerator topology. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if max topology distance is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#accelerator_topology ComputeResourcePolicy#accelerator_topology}
        :param max_topology_distance: The maximum topology distance. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_topology_distance ComputeResourcePolicy#max_topology_distance}
        '''
        value = ComputeResourcePolicyWorkloadPolicy(
            type=type,
            accelerator_topology=accelerator_topology,
            max_topology_distance=max_topology_distance,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkloadPolicy", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskConsistencyGroupPolicy")
    def reset_disk_consistency_group_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskConsistencyGroupPolicy", []))

    @jsii.member(jsii_name="resetGroupPlacementPolicy")
    def reset_group_placement_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupPlacementPolicy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceSchedulePolicy")
    def reset_instance_schedule_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSchedulePolicy", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSnapshotSchedulePolicy")
    def reset_snapshot_schedule_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotSchedulePolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkloadPolicy")
    def reset_workload_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadPolicy", []))

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
    @jsii.member(jsii_name="diskConsistencyGroupPolicy")
    def disk_consistency_group_policy(
        self,
    ) -> "ComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference":
        return typing.cast("ComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference", jsii.get(self, "diskConsistencyGroupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="groupPlacementPolicy")
    def group_placement_policy(
        self,
    ) -> "ComputeResourcePolicyGroupPlacementPolicyOutputReference":
        return typing.cast("ComputeResourcePolicyGroupPlacementPolicyOutputReference", jsii.get(self, "groupPlacementPolicy"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicy")
    def instance_schedule_policy(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyOutputReference", jsii.get(self, "instanceSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="snapshotSchedulePolicy")
    def snapshot_schedule_policy(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyOutputReference", jsii.get(self, "snapshotSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeResourcePolicyTimeoutsOutputReference":
        return typing.cast("ComputeResourcePolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicy")
    def workload_policy(self) -> "ComputeResourcePolicyWorkloadPolicyOutputReference":
        return typing.cast("ComputeResourcePolicyWorkloadPolicyOutputReference", jsii.get(self, "workloadPolicy"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConsistencyGroupPolicyInput")
    def disk_consistency_group_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyDiskConsistencyGroupPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyDiskConsistencyGroupPolicy"], jsii.get(self, "diskConsistencyGroupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="groupPlacementPolicyInput")
    def group_placement_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"], jsii.get(self, "groupPlacementPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicyInput")
    def instance_schedule_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"], jsii.get(self, "instanceSchedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotSchedulePolicyInput")
    def snapshot_schedule_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"], jsii.get(self, "snapshotSchedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeResourcePolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeResourcePolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicyInput")
    def workload_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyWorkloadPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyWorkloadPolicy"], jsii.get(self, "workloadPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97245cfcd67b37f9c0b5216cb4254218fad0aa032f9d2a93857427a2a15ccd59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581fbe793c8b68c2f368f90f9144274bf253cb7315fea5d4e11bd067d4aa722d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9ca9842406ef22e868fb94c1465e31c3428a6d4c272a5aaec47626d05820ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958882512a4819ba899893980834c2cfb25f3ea6f9ef5950ffac21e6c0e99b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30673a24f12c32b7dcaa11a5980884a22f3fb272167e77ad02cba9aeb6d6a32f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyConfig",
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
        "disk_consistency_group_policy": "diskConsistencyGroupPolicy",
        "group_placement_policy": "groupPlacementPolicy",
        "id": "id",
        "instance_schedule_policy": "instanceSchedulePolicy",
        "project": "project",
        "region": "region",
        "snapshot_schedule_policy": "snapshotSchedulePolicy",
        "timeouts": "timeouts",
        "workload_policy": "workloadPolicy",
    },
)
class ComputeResourcePolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk_consistency_group_policy: typing.Optional[typing.Union["ComputeResourcePolicyDiskConsistencyGroupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        group_placement_policy: typing.Optional[typing.Union["ComputeResourcePolicyGroupPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeResourcePolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_policy: typing.Optional[typing.Union["ComputeResourcePolicyWorkloadPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#name ComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#description ComputeResourcePolicy#description}
        :param disk_consistency_group_policy: disk_consistency_group_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#disk_consistency_group_policy ComputeResourcePolicy#disk_consistency_group_policy}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#id ComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#project ComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#region ComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
        :param workload_policy: workload_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#workload_policy ComputeResourcePolicy#workload_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(disk_consistency_group_policy, dict):
            disk_consistency_group_policy = ComputeResourcePolicyDiskConsistencyGroupPolicy(**disk_consistency_group_policy)
        if isinstance(group_placement_policy, dict):
            group_placement_policy = ComputeResourcePolicyGroupPlacementPolicy(**group_placement_policy)
        if isinstance(instance_schedule_policy, dict):
            instance_schedule_policy = ComputeResourcePolicyInstanceSchedulePolicy(**instance_schedule_policy)
        if isinstance(snapshot_schedule_policy, dict):
            snapshot_schedule_policy = ComputeResourcePolicySnapshotSchedulePolicy(**snapshot_schedule_policy)
        if isinstance(timeouts, dict):
            timeouts = ComputeResourcePolicyTimeouts(**timeouts)
        if isinstance(workload_policy, dict):
            workload_policy = ComputeResourcePolicyWorkloadPolicy(**workload_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b282e2fd7c767e525396cbbea1527593883fd1b55f2b698451dea0f1fa872c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_consistency_group_policy", value=disk_consistency_group_policy, expected_type=type_hints["disk_consistency_group_policy"])
            check_type(argname="argument group_placement_policy", value=group_placement_policy, expected_type=type_hints["group_placement_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_schedule_policy", value=instance_schedule_policy, expected_type=type_hints["instance_schedule_policy"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument snapshot_schedule_policy", value=snapshot_schedule_policy, expected_type=type_hints["snapshot_schedule_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workload_policy", value=workload_policy, expected_type=type_hints["workload_policy"])
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
        if disk_consistency_group_policy is not None:
            self._values["disk_consistency_group_policy"] = disk_consistency_group_policy
        if group_placement_policy is not None:
            self._values["group_placement_policy"] = group_placement_policy
        if id is not None:
            self._values["id"] = id
        if instance_schedule_policy is not None:
            self._values["instance_schedule_policy"] = instance_schedule_policy
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if snapshot_schedule_policy is not None:
            self._values["snapshot_schedule_policy"] = snapshot_schedule_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workload_policy is not None:
            self._values["workload_policy"] = workload_policy

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
        '''The name of the resource, provided by the client when initially creating the resource.

        The resource name must be 1-63 characters long, and comply
        with RFC1035. Specifically, the name must be 1-63 characters long and
        match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the
        first character must be a lowercase letter, and all following characters
        must be a dash, lowercase letter, or digit, except the last character,
        which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#name ComputeResourcePolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#description ComputeResourcePolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_consistency_group_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicyDiskConsistencyGroupPolicy"]:
        '''disk_consistency_group_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#disk_consistency_group_policy ComputeResourcePolicy#disk_consistency_group_policy}
        '''
        result = self._values.get("disk_consistency_group_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyDiskConsistencyGroupPolicy"], result)

    @builtins.property
    def group_placement_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"]:
        '''group_placement_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#group_placement_policy ComputeResourcePolicy#group_placement_policy}
        '''
        result = self._values.get("group_placement_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyGroupPlacementPolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#id ComputeResourcePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_schedule_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"]:
        '''instance_schedule_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#instance_schedule_policy ComputeResourcePolicy#instance_schedule_policy}
        '''
        result = self._values.get("instance_schedule_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#project ComputeResourcePolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where resource policy resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#region ComputeResourcePolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_schedule_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"]:
        '''snapshot_schedule_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_schedule_policy ComputeResourcePolicy#snapshot_schedule_policy}
        '''
        result = self._values.get("snapshot_schedule_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeResourcePolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#timeouts ComputeResourcePolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeResourcePolicyTimeouts"], result)

    @builtins.property
    def workload_policy(self) -> typing.Optional["ComputeResourcePolicyWorkloadPolicy"]:
        '''workload_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#workload_policy ComputeResourcePolicy#workload_policy}
        '''
        result = self._values.get("workload_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicyWorkloadPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyDiskConsistencyGroupPolicy",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class ComputeResourcePolicyDiskConsistencyGroupPolicy:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable disk consistency on the resource policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#enabled ComputeResourcePolicy#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd051806b9d0fec1e28ddf027128f8ad6a06a5cc7db68f4db3ae42d9d17d2d6b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable disk consistency on the resource policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#enabled ComputeResourcePolicy#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyDiskConsistencyGroupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76a5b067193b218f6d26e2213865c6f7f6f355727261f301591396c0e1383510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__33c5c9dff9e3db47941329a9f9bf06fbaf43a8cdbeb010bde658ca94cb41c363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyDiskConsistencyGroupPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyDiskConsistencyGroupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyDiskConsistencyGroupPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77884fd8eb5144a8ef974b5a2315cb2059ba68a46068bf10079535104123a130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyGroupPlacementPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "availability_domain_count": "availabilityDomainCount",
        "collocation": "collocation",
        "gpu_topology": "gpuTopology",
        "vm_count": "vmCount",
    },
)
class ComputeResourcePolicyGroupPlacementPolicy:
    def __init__(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        gpu_topology: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        :param gpu_topology: Specifies the shape of the GPU slice, in slice based GPU families eg. A4X. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#gpu_topology ComputeResourcePolicy#gpu_topology}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5a29e15f41254bcdb9f0497c4044bfa9e0e24ee89e2007012dc472c4239ae5)
            check_type(argname="argument availability_domain_count", value=availability_domain_count, expected_type=type_hints["availability_domain_count"])
            check_type(argname="argument collocation", value=collocation, expected_type=type_hints["collocation"])
            check_type(argname="argument gpu_topology", value=gpu_topology, expected_type=type_hints["gpu_topology"])
            check_type(argname="argument vm_count", value=vm_count, expected_type=type_hints["vm_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_domain_count is not None:
            self._values["availability_domain_count"] = availability_domain_count
        if collocation is not None:
            self._values["collocation"] = collocation
        if gpu_topology is not None:
            self._values["gpu_topology"] = gpu_topology
        if vm_count is not None:
            self._values["vm_count"] = vm_count

    @builtins.property
    def availability_domain_count(self) -> typing.Optional[jsii.Number]:
        '''The number of availability domains instances will be spread across.

        If two instances are in different
        availability domain, they will not be put in the same low latency network

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#availability_domain_count ComputeResourcePolicy#availability_domain_count}
        '''
        result = self._values.get("availability_domain_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def collocation(self) -> typing.Optional[builtins.str]:
        '''Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network.

        Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created
        with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy
        attached. Possible values: ["COLLOCATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#collocation ComputeResourcePolicy#collocation}
        '''
        result = self._values.get("collocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_topology(self) -> typing.Optional[builtins.str]:
        '''Specifies the shape of the GPU slice, in slice based GPU families eg. A4X.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#gpu_topology ComputeResourcePolicy#gpu_topology}
        '''
        result = self._values.get("gpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_count(self) -> typing.Optional[jsii.Number]:
        '''Number of VMs in this placement group.

        Google does not recommend that you use this field
        unless you use a compact policy and you want your policy to work only if it contains this
        exact number of VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_count ComputeResourcePolicy#vm_count}
        '''
        result = self._values.get("vm_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyGroupPlacementPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyGroupPlacementPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyGroupPlacementPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24046ba29738ceac5961334d8c63846b110c6137b99d7116e68a40f6ad2c4c6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAvailabilityDomainCount")
    def reset_availability_domain_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityDomainCount", []))

    @jsii.member(jsii_name="resetCollocation")
    def reset_collocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollocation", []))

    @jsii.member(jsii_name="resetGpuTopology")
    def reset_gpu_topology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuTopology", []))

    @jsii.member(jsii_name="resetVmCount")
    def reset_vm_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmCount", []))

    @builtins.property
    @jsii.member(jsii_name="availabilityDomainCountInput")
    def availability_domain_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availabilityDomainCountInput"))

    @builtins.property
    @jsii.member(jsii_name="collocationInput")
    def collocation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collocationInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuTopologyInput")
    def gpu_topology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpuTopologyInput"))

    @builtins.property
    @jsii.member(jsii_name="vmCountInput")
    def vm_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vmCountInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityDomainCount")
    def availability_domain_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomainCount"))

    @availability_domain_count.setter
    def availability_domain_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba503a631b83483fd41083a59cdcb7a4948b02c2cd2a0b0e4b984c7164f3aaaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomainCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collocation")
    def collocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collocation"))

    @collocation.setter
    def collocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf1c8c7e7eea3195af04baf6b52087d8d9b6c9503707171937a1ffcb6d9edb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuTopology")
    def gpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuTopology"))

    @gpu_topology.setter
    def gpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28e095d1bd9a45664f3325082d0f6165c57d8283b6c675e90e921eec6598b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmCount")
    def vm_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmCount"))

    @vm_count.setter
    def vm_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb90130c07e5cf7f03c058ffc2143ad45ab5d958489a2e9ea1e8cacd3ec04bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyGroupPlacementPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyGroupPlacementPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyGroupPlacementPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76db459b641ec2c0b872cb038910a9a7e82347e46d22674c44613a3c559ce31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "expiration_time": "expirationTime",
        "start_time": "startTime",
        "vm_start_schedule": "vmStartSchedule",
        "vm_stop_schedule": "vmStopSchedule",
    },
)
class ComputeResourcePolicyInstanceSchedulePolicy:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        vm_start_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        if isinstance(vm_start_schedule, dict):
            vm_start_schedule = ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(**vm_start_schedule)
        if isinstance(vm_stop_schedule, dict):
            vm_stop_schedule = ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(**vm_stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac86bbef13f0d022eabb62537d55720f33ae3b399bb389c989e96f85a6edafcc)
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument vm_start_schedule", value=vm_start_schedule, expected_type=type_hints["vm_start_schedule"])
            check_type(argname="argument vm_stop_schedule", value=vm_stop_schedule, expected_type=type_hints["vm_stop_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_zone": time_zone,
        }
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if start_time is not None:
            self._values["start_time"] = start_time
        if vm_start_schedule is not None:
            self._values["vm_start_schedule"] = vm_start_schedule
        if vm_stop_schedule is not None:
            self._values["vm_stop_schedule"] = vm_stop_schedule

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''Specifies the time zone to be used in interpreting the schedule.

        The value of this field must be a time zone name
        from the tz database: http://en.wikipedia.org/wiki/Tz_database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#time_zone ComputeResourcePolicy#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''The expiration time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#expiration_time ComputeResourcePolicy#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_start_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        '''vm_start_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_start_schedule ComputeResourcePolicy#vm_start_schedule}
        '''
        result = self._values.get("vm_start_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], result)

    @builtins.property
    def vm_stop_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        '''vm_stop_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#vm_stop_schedule ComputeResourcePolicy#vm_stop_schedule}
        '''
        result = self._values.get("vm_stop_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdc80ad88c4745c6e9a1156bef739cb0fc1d636d4ef5549a7e2fec4952e356d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVmStartSchedule")
    def put_vm_start_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(
            schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putVmStartSchedule", [value]))

    @jsii.member(jsii_name="putVmStopSchedule")
    def put_vm_stop_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        value = ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(
            schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putVmStopSchedule", [value]))

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetVmStartSchedule")
    def reset_vm_start_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmStartSchedule", []))

    @jsii.member(jsii_name="resetVmStopSchedule")
    def reset_vm_stop_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmStopSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="vmStartSchedule")
    def vm_start_schedule(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference", jsii.get(self, "vmStartSchedule"))

    @builtins.property
    @jsii.member(jsii_name="vmStopSchedule")
    def vm_stop_schedule(
        self,
    ) -> "ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference":
        return typing.cast("ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference", jsii.get(self, "vmStopSchedule"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="vmStartScheduleInput")
    def vm_start_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], jsii.get(self, "vmStartScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="vmStopScheduleInput")
    def vm_stop_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], jsii.get(self, "vmStopScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0f82f39f5a14a2d4d9f6b96cdd21800a468918888f8e312c3c2a3fb9a7603f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9060f92a2949b424357a970ec43176dac652802ab6836f13ce40418d1c0baee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067ea3430b6acc76a200138db1299db0062e86eb4bc7b339e3b97f9933afa052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6040b3585d5c37e4950704ad27ba2da53f375ea29b06fde14b57753c59e7e705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db52cd2c4cb8f1fcf84b44e9d6b37989eee059f4e9022c46ca4a7938795b04be)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f3b9e920d74b449b4e55668049c6823dbf126b28b03187e1c7223305d79ea1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37caebb32236dd1f12dfb1d337ba96a7c748f3da491eecca4ed31056cab4db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180500bef5ce79ea75a36d255cb9f9cab18680e34f34033ecb0d424d3eace168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc19f7555adeb4c3049cbe1382d46551b1a8c7cbe96f386abf0add52a853f19)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76a719bb93b7f751b2f228a7bf3047150a23f99f24bf71298e1c10b721e157a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7b9cc07533a54851425dc583042174fa26940b1ac80fdeafb3348a4ddf3990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8836a854f9e2fd153cc623014fb918174173aea140215af7dc19ebd144c3be19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "retention_policy": "retentionPolicy",
        "snapshot_properties": "snapshotProperties",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicy:
    def __init__(
        self,
        *,
        schedule: typing.Union["ComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[builtins.str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        if isinstance(schedule, dict):
            schedule = ComputeResourcePolicySnapshotSchedulePolicySchedule(**schedule)
        if isinstance(retention_policy, dict):
            retention_policy = ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(**retention_policy)
        if isinstance(snapshot_properties, dict):
            snapshot_properties = ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(**snapshot_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607efe77891cb51555d5a0201e0546837cad3ac7a3200916fc857e64050c6bb0)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument snapshot_properties", value=snapshot_properties, expected_type=type_hints["snapshot_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if snapshot_properties is not None:
            self._values["snapshot_properties"] = snapshot_properties

    @builtins.property
    def schedule(self) -> "ComputeResourcePolicySnapshotSchedulePolicySchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#schedule ComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicySchedule", result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#retention_policy ComputeResourcePolicy#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], result)

    @builtins.property
    def snapshot_properties(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        '''snapshot_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#snapshot_properties ComputeResourcePolicy#snapshot_properties}
        '''
        result = self._values.get("snapshot_properties")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a96a8832b016496638d2a76ec08067b9c5198d7d96af822a6b1bd39eaccea174)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        max_retention_days: jsii.Number,
        on_source_disk_delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(
            max_retention_days=max_retention_days,
            on_source_disk_delete=on_source_disk_delete,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicySchedule(
            daily_schedule=daily_schedule,
            hourly_schedule=hourly_schedule,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="putSnapshotProperties")
    def put_snapshot_properties(
        self,
        *,
        chain_name: typing.Optional[builtins.str] = None,
        guest_flush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#labels ComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(
            chain_name=chain_name,
            guest_flush=guest_flush,
            labels=labels,
            storage_locations=storage_locations,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotProperties", [value]))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSnapshotProperties")
    def reset_snapshot_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotProperties", []))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="snapshotProperties")
    def snapshot_properties(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference", jsii.get(self, "snapshotProperties"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPropertiesInput")
    def snapshot_properties_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], jsii.get(self, "snapshotPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181cb24bd018eb2b496b36ec3c308c49ec755823da8234c4f6bcf07e8938df1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retention_days": "maxRetentionDays",
        "on_source_disk_delete": "onSourceDiskDelete",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy:
    def __init__(
        self,
        *,
        max_retention_days: jsii.Number,
        on_source_disk_delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c995b729de2f04a99ff6647534552bbd2986116c7568f0e515b5f1d871059e)
            check_type(argname="argument max_retention_days", value=max_retention_days, expected_type=type_hints["max_retention_days"])
            check_type(argname="argument on_source_disk_delete", value=on_source_disk_delete, expected_type=type_hints["on_source_disk_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_retention_days": max_retention_days,
        }
        if on_source_disk_delete is not None:
            self._values["on_source_disk_delete"] = on_source_disk_delete

    @builtins.property
    def max_retention_days(self) -> jsii.Number:
        '''Maximum age of the snapshot that is allowed to be kept.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_retention_days ComputeResourcePolicy#max_retention_days}
        '''
        result = self._values.get("max_retention_days")
        assert result is not None, "Required property 'max_retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def on_source_disk_delete(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior to apply to scheduled snapshots when the source disk is deleted.

        Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#on_source_disk_delete ComputeResourcePolicy#on_source_disk_delete}
        '''
        result = self._values.get("on_source_disk_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea736c5f0a08baf4eed8eed9c97ec10f6982afffe4f8430f64b2a37e1ed80e4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOnSourceDiskDelete")
    def reset_on_source_disk_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnSourceDiskDelete", []))

    @builtins.property
    @jsii.member(jsii_name="maxRetentionDaysInput")
    def max_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="onSourceDiskDeleteInput")
    def on_source_disk_delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onSourceDiskDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetentionDays")
    def max_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetentionDays"))

    @max_retention_days.setter
    def max_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef7d33a6cc906ed0d3fa442de868c0973d5d81271be9efb575501c1849d9403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onSourceDiskDelete")
    def on_source_disk_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onSourceDiskDelete"))

    @on_source_disk_delete.setter
    def on_source_disk_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd577d8b6a00352d96f52edc8fb41afa03ae76aff990943b4f6e480ae52ef76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onSourceDiskDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e3c8a162f2a37bf374959ae9181f6db6ca32cc47350a3b45c7febb497c0165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "hourly_schedule": "hourlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicySchedule:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(**hourly_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b083af9e99ebe6f9d2e850004ff4a4b8dcfa9932d6100d149c30a37c01151e5)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument hourly_schedule", value=hourly_schedule, expected_type=type_hints["hourly_schedule"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if hourly_schedule is not None:
            self._values["hourly_schedule"] = hourly_schedule
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#daily_schedule ComputeResourcePolicy#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"], result)

    @builtins.property
    def hourly_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hourly_schedule ComputeResourcePolicy#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#weekly_schedule ComputeResourcePolicy#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    jsii_struct_bases=[],
    name_mapping={"days_in_cycle": "daysInCycle", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule:
    def __init__(self, *, days_in_cycle: jsii.Number, start_time: builtins.str) -> None:
        '''
        :param days_in_cycle: Defines a schedule with units measured in days. The value determines how many days pass between the start of each cycle. Days in cycle for snapshot schedule policy must be 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b6c613b3f6412c4218f3f3b064e876a70572d4476afaf14c0c76308dcd302f)
            check_type(argname="argument days_in_cycle", value=days_in_cycle, expected_type=type_hints["days_in_cycle"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_in_cycle": days_in_cycle,
            "start_time": start_time,
        }

    @builtins.property
    def days_in_cycle(self) -> jsii.Number:
        '''Defines a schedule with units measured in days.

        The value determines how many days pass between the start of each cycle. Days in cycle for snapshot schedule policy must be 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        '''
        result = self._values.get("days_in_cycle")
        assert result is not None, "Required property 'days_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00.

        For example,
        both 13:00-5 and 08:00 are valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aa9f0856bb2b17393d07afc5cc7aa0a3d10ca0db7edba6918a7a7fa0696d1d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="daysInCycleInput")
    def days_in_cycle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysInCycle")
    def days_in_cycle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysInCycle"))

    @days_in_cycle.setter
    def days_in_cycle(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f84dc3ee0dc3f9f20961054a703ff13a40081e0423be5d71147deedce803213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysInCycle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed06d7c6d7296c33958f2ac073fd89bfaf10a41533ebc759db8ab4e32cd4e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b28627ced7f845990b7da86e8d54537696f4cc8256d69f9bbca006f1c06e22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"hours_in_cycle": "hoursInCycle", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule:
    def __init__(
        self,
        *,
        hours_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9a6e49437c634a0ab8bac23c31b37336ff551885f97d4a8b7b169dc28b1f0f)
            check_type(argname="argument hours_in_cycle", value=hours_in_cycle, expected_type=type_hints["hours_in_cycle"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours_in_cycle": hours_in_cycle,
            "start_time": start_time,
        }

    @builtins.property
    def hours_in_cycle(self) -> jsii.Number:
        '''The number of hours between snapshots.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        '''
        result = self._values.get("hours_in_cycle")
        assert result is not None, "Required property 'hours_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in an hourly format "HH:MM",
        where HH : [00-23] and MM : [00] GMT. eg: 21:00

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5082b775bc3fee3408c5ed275688bb1ae771110c5deb74c42808be9d0f55a0a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hoursInCycleInput")
    def hours_in_cycle_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInCycleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="hoursInCycle")
    def hours_in_cycle(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hoursInCycle"))

    @hours_in_cycle.setter
    def hours_in_cycle(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1803328449d0967fe72f6491d87f3f6e0e4516ca544151015bf6734fab62d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hoursInCycle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006d33d997dbd5de61d320ef3d279506f541ecce2e74d1fb648e3d3573c1b0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99656fc0058d3d7b54ed75385aeda9f7f7e5f65298f0a10e0e7c46d869db3d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcb1dbef1a9b2a268dc55e3d2ec16e232b06a1d0c36409db5e9e4e8eb0e43ad9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDailySchedule")
    def put_daily_schedule(
        self,
        *,
        days_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param days_in_cycle: Defines a schedule with units measured in days. The value determines how many days pass between the start of each cycle. Days in cycle for snapshot schedule policy must be 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#days_in_cycle ComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(
            days_in_cycle=days_in_cycle, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putDailySchedule", [value]))

    @jsii.member(jsii_name="putHourlySchedule")
    def put_hourly_schedule(
        self,
        *,
        hours_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#hours_in_cycle ComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(
            hours_in_cycle=hours_in_cycle, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putHourlySchedule", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        value = ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(
            day_of_weeks=day_of_weeks
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetHourlySchedule")
    def reset_hourly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlySchedule", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference, jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference":
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyScheduleInput")
    def hourly_schedule_input(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        return typing.cast(typing.Optional["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ad4aa352c89168ecc54f5dacad48dd2eeb3298243e8f08f21c355373115fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={"day_of_weeks": "dayOfWeeks"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule:
    def __init__(
        self,
        *,
        day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153999083f30eeef88ab0f316c6257595ccf419f7356b06c6c3eb82eaf577c51)
            check_type(argname="argument day_of_weeks", value=day_of_weeks, expected_type=type_hints["day_of_weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_weeks": day_of_weeks,
        }

    @builtins.property
    def day_of_weeks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]]:
        '''day_of_weeks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#day_of_weeks ComputeResourcePolicy#day_of_weeks}
        '''
        result = self._values.get("day_of_weeks")
        assert result is not None, "Required property 'day_of_weeks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks:
    def __init__(self, *, day: builtins.str, start_time: builtins.str) -> None:
        '''
        :param day: The day of the week to create the snapshot. e.g. MONDAY Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#day ComputeResourcePolicy#day}
        :param start_time: Time within the window to start the operations. It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5324d2c340ba8f3b3b42a5b968610fd0e31638ec14ee56f0b70c9d7b585eff4)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''The day of the week to create the snapshot.

        e.g. MONDAY Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#day ComputeResourcePolicy#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#start_time ComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0681f63b7b95c754a38f6002c6b215c6cd4bf0cf44e9e044d4d7e3d5828ff939)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90f2b0b4b28be3e45f6b269ebbc5517da7873e01069f5f8a5f4aa6bb7ca4531)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694f266c8a16b1bec06279053cdfe0409404407295860f96724bb2994a0d202c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce143c6694d3db0ec2916f94d0c39c4bd8e3e1bc19041ed65a7913b3af2ffe63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b31c488d5cef800a363130419ded56a13d0608f9bd184021c8b8026d9cabe82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91da33fa5756f19de53c40d52a6e07e7d61ffb2874639534b5cfb7a98c08e045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a19d9ff541cf6591b8799f1ed5ae858b006137f65e6ce00d7f8eaaf0d6bc3ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4546dc6d6987d0a30791b8a24f4caa4687839ae3bba3a4b2c373cfab0c666885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a934616ce3fe0e84d2319446de62d5c13e1cf2af860031ec9f9e0018d44f1d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338568f22215b9fdd4e5714ef4ed75181e13032905e1948ff7d18c4c7649493f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ec733e348c6c398af5adf4ab9e568f96a83f8fd69f24e2a0631e69149a7416)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDayOfWeeks")
    def put_day_of_weeks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a2a412d5d8dc0202720e931299f635bb1a148edc44fdfef4a8927a6f01d5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDayOfWeeks", [value]))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeks")
    def day_of_weeks(
        self,
    ) -> ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList:
        return typing.cast(ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList, jsii.get(self, "dayOfWeeks"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeksInput")
    def day_of_weeks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "dayOfWeeksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbbbe67149d5e4192951d88cbe7d90b27386e2d8661021180597c5f7b618daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    jsii_struct_bases=[],
    name_mapping={
        "chain_name": "chainName",
        "guest_flush": "guestFlush",
        "labels": "labels",
        "storage_locations": "storageLocations",
    },
)
class ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties:
    def __init__(
        self,
        *,
        chain_name: typing.Optional[builtins.str] = None,
        guest_flush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#labels ComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8fa87dbaebde00a58184bcb235144c55e0ea42d40782ba5188033a07dac8dc3)
            check_type(argname="argument chain_name", value=chain_name, expected_type=type_hints["chain_name"])
            check_type(argname="argument guest_flush", value=guest_flush, expected_type=type_hints["guest_flush"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument storage_locations", value=storage_locations, expected_type=type_hints["storage_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chain_name is not None:
            self._values["chain_name"] = chain_name
        if guest_flush is not None:
            self._values["guest_flush"] = guest_flush
        if labels is not None:
            self._values["labels"] = labels
        if storage_locations is not None:
            self._values["storage_locations"] = storage_locations

    @builtins.property
    def chain_name(self) -> typing.Optional[builtins.str]:
        '''Creates the new snapshot in the snapshot chain labeled with the specified name.

        The chain name must be 1-63 characters long and comply
        with RFC1035.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#chain_name ComputeResourcePolicy#chain_name}
        '''
        result = self._values.get("chain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_flush(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to perform a 'guest aware' snapshot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#guest_flush ComputeResourcePolicy#guest_flush}
        '''
        result = self._values.get("guest_flush")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key-value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#labels ComputeResourcePolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def storage_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage bucket location to store the auto snapshot (regional or multi-regional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#storage_locations ComputeResourcePolicy#storage_locations}
        '''
        result = self._values.get("storage_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0857d7a02c0bae99070de036a3d69d656fa1cab00b6f5b26cdf0587804ebf1f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChainName")
    def reset_chain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChainName", []))

    @jsii.member(jsii_name="resetGuestFlush")
    def reset_guest_flush(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestFlush", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetStorageLocations")
    def reset_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageLocations", []))

    @builtins.property
    @jsii.member(jsii_name="chainNameInput")
    def chain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="guestFlushInput")
    def guest_flush_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "guestFlushInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationsInput")
    def storage_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="chainName")
    def chain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chainName"))

    @chain_name.setter
    def chain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb120a0fc67128e814c17f41873b81fbc33c179f5124c0203c22f4b058dc020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestFlush")
    def guest_flush(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "guestFlush"))

    @guest_flush.setter
    def guest_flush(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f529948c123fc8a636c9b7c57f08f3d2c49c7eaebc6518ad733daf530ce98125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFlush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf713565eea776b9e0c2b69a6acfa31e085258e504ca9a220372f0f289833304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageLocations")
    def storage_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageLocations"))

    @storage_locations.setter
    def storage_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e183f01e938a8a283da5462fc4e8f85e8fcd3c672c96158c06792d374c9808f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties]:
        return typing.cast(typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9563dd84b45aa2488f077e127fd59f902d88305efde74ed264649c3444db1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeResourcePolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#create ComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#delete ComputeResourcePolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#update ComputeResourcePolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf47e29da7b3c9ed6169e4141297ed1c09997ca9a09615d70948c188de7acf0e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#create ComputeResourcePolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#delete ComputeResourcePolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#update ComputeResourcePolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea603289a872042375efe959d4b41b7b24c48b7cda66c2479a1d8a70a9c9b18d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f147578c5dc90dfad21297128f627bceac05fad31f5311c97361ef499b204d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc459f000a010422f74f024481e68de063c4e699647eb96bf3d8738d49d69645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55cb05e3db8c4399c11ff6032ba5d23ef39f943d2e5a8ef930d58842ed9f3aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a0f8b395e0d69296af137200e3f9a855dc553e4251b3b6637119a0ffa27b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyWorkloadPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "accelerator_topology": "acceleratorTopology",
        "max_topology_distance": "maxTopologyDistance",
    },
)
class ComputeResourcePolicyWorkloadPolicy:
    def __init__(
        self,
        *,
        type: builtins.str,
        accelerator_topology: typing.Optional[builtins.str] = None,
        max_topology_distance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of workload policy. Possible values: ["HIGH_AVAILABILITY", "HIGH_THROUGHPUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#type ComputeResourcePolicy#type}
        :param accelerator_topology: The accelerator topology. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if max topology distance is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#accelerator_topology ComputeResourcePolicy#accelerator_topology}
        :param max_topology_distance: The maximum topology distance. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_topology_distance ComputeResourcePolicy#max_topology_distance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__401a6c7353daf5cdddb45331b42b450d1f250fc7aba3149a5d852e08969029f0)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument accelerator_topology", value=accelerator_topology, expected_type=type_hints["accelerator_topology"])
            check_type(argname="argument max_topology_distance", value=max_topology_distance, expected_type=type_hints["max_topology_distance"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if accelerator_topology is not None:
            self._values["accelerator_topology"] = accelerator_topology
        if max_topology_distance is not None:
            self._values["max_topology_distance"] = max_topology_distance

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of workload policy. Possible values: ["HIGH_AVAILABILITY", "HIGH_THROUGHPUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#type ComputeResourcePolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_topology(self) -> typing.Optional[builtins.str]:
        '''The accelerator topology.

        This field can be set only when the workload policy type is HIGH_THROUGHPUT
        and cannot be set if max topology distance is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#accelerator_topology ComputeResourcePolicy#accelerator_topology}
        '''
        result = self._values.get("accelerator_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_topology_distance(self) -> typing.Optional[builtins.str]:
        '''The maximum topology distance.

        This field can be set only when the workload policy type is HIGH_THROUGHPUT
        and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_resource_policy#max_topology_distance ComputeResourcePolicy#max_topology_distance}
        '''
        result = self._values.get("max_topology_distance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResourcePolicyWorkloadPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeResourcePolicyWorkloadPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeResourcePolicy.ComputeResourcePolicyWorkloadPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed73b4346a4c7a8c3dd1c555e2849855f37914f0a3c3874c2579404e9c7be9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcceleratorTopology")
    def reset_accelerator_topology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorTopology", []))

    @jsii.member(jsii_name="resetMaxTopologyDistance")
    def reset_max_topology_distance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxTopologyDistance", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTopologyInput")
    def accelerator_topology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTopologyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTopologyDistanceInput")
    def max_topology_distance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxTopologyDistanceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTopology")
    def accelerator_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorTopology"))

    @accelerator_topology.setter
    def accelerator_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee13ad9147c96867fedd31c686a7887eaecf678397673ee685540da3d45d814c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTopologyDistance")
    def max_topology_distance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTopologyDistance"))

    @max_topology_distance.setter
    def max_topology_distance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e57efcac7bdfd1d20da42b13bb91c880d595a68c9abe304616b211f44e5f15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTopologyDistance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65eb3b7d5d5f2f01321998d01dd7ecda8f1463c698ac40df63abe5efab4b0e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeResourcePolicyWorkloadPolicy]:
        return typing.cast(typing.Optional[ComputeResourcePolicyWorkloadPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeResourcePolicyWorkloadPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a530c6edc1ee60d31f6bc2d3c611b50c415e196e0022866a5c18f16b8b7569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeResourcePolicy",
    "ComputeResourcePolicyConfig",
    "ComputeResourcePolicyDiskConsistencyGroupPolicy",
    "ComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference",
    "ComputeResourcePolicyGroupPlacementPolicy",
    "ComputeResourcePolicyGroupPlacementPolicyOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicy",
    "ComputeResourcePolicyInstanceSchedulePolicyOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    "ComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicy",
    "ComputeResourcePolicySnapshotSchedulePolicyOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    "ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
    "ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    "ComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
    "ComputeResourcePolicyTimeouts",
    "ComputeResourcePolicyTimeoutsOutputReference",
    "ComputeResourcePolicyWorkloadPolicy",
    "ComputeResourcePolicyWorkloadPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__ce3e16d2beae709200f3ea76b570bf0081c8efd00f7c347d2c6bc6389c8a0ebc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disk_consistency_group_policy: typing.Optional[typing.Union[ComputeResourcePolicyDiskConsistencyGroupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    group_placement_policy: typing.Optional[typing.Union[ComputeResourcePolicyGroupPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_policy: typing.Optional[typing.Union[ComputeResourcePolicyWorkloadPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f20acd42c7311578905ade1ec69242135b4cd24622a826a5c3212ec561b12c1f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97245cfcd67b37f9c0b5216cb4254218fad0aa032f9d2a93857427a2a15ccd59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581fbe793c8b68c2f368f90f9144274bf253cb7315fea5d4e11bd067d4aa722d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9ca9842406ef22e868fb94c1465e31c3428a6d4c272a5aaec47626d05820ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958882512a4819ba899893980834c2cfb25f3ea6f9ef5950ffac21e6c0e99b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30673a24f12c32b7dcaa11a5980884a22f3fb272167e77ad02cba9aeb6d6a32f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b282e2fd7c767e525396cbbea1527593883fd1b55f2b698451dea0f1fa872c(
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
    disk_consistency_group_policy: typing.Optional[typing.Union[ComputeResourcePolicyDiskConsistencyGroupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    group_placement_policy: typing.Optional[typing.Union[ComputeResourcePolicyGroupPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_schedule_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeResourcePolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_policy: typing.Optional[typing.Union[ComputeResourcePolicyWorkloadPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd051806b9d0fec1e28ddf027128f8ad6a06a5cc7db68f4db3ae42d9d17d2d6b(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a5b067193b218f6d26e2213865c6f7f6f355727261f301591396c0e1383510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c5c9dff9e3db47941329a9f9bf06fbaf43a8cdbeb010bde658ca94cb41c363(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77884fd8eb5144a8ef974b5a2315cb2059ba68a46068bf10079535104123a130(
    value: typing.Optional[ComputeResourcePolicyDiskConsistencyGroupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5a29e15f41254bcdb9f0497c4044bfa9e0e24ee89e2007012dc472c4239ae5(
    *,
    availability_domain_count: typing.Optional[jsii.Number] = None,
    collocation: typing.Optional[builtins.str] = None,
    gpu_topology: typing.Optional[builtins.str] = None,
    vm_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24046ba29738ceac5961334d8c63846b110c6137b99d7116e68a40f6ad2c4c6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba503a631b83483fd41083a59cdcb7a4948b02c2cd2a0b0e4b984c7164f3aaaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf1c8c7e7eea3195af04baf6b52087d8d9b6c9503707171937a1ffcb6d9edb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28e095d1bd9a45664f3325082d0f6165c57d8283b6c675e90e921eec6598b4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb90130c07e5cf7f03c058ffc2143ad45ab5d958489a2e9ea1e8cacd3ec04bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76db459b641ec2c0b872cb038910a9a7e82347e46d22674c44613a3c559ce31(
    value: typing.Optional[ComputeResourcePolicyGroupPlacementPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac86bbef13f0d022eabb62537d55720f33ae3b399bb389c989e96f85a6edafcc(
    *,
    time_zone: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    vm_start_schedule: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_stop_schedule: typing.Optional[typing.Union[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc80ad88c4745c6e9a1156bef739cb0fc1d636d4ef5549a7e2fec4952e356d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0f82f39f5a14a2d4d9f6b96cdd21800a468918888f8e312c3c2a3fb9a7603f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9060f92a2949b424357a970ec43176dac652802ab6836f13ce40418d1c0baee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067ea3430b6acc76a200138db1299db0062e86eb4bc7b339e3b97f9933afa052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6040b3585d5c37e4950704ad27ba2da53f375ea29b06fde14b57753c59e7e705(
    value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db52cd2c4cb8f1fcf84b44e9d6b37989eee059f4e9022c46ca4a7938795b04be(
    *,
    schedule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f3b9e920d74b449b4e55668049c6823dbf126b28b03187e1c7223305d79ea1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37caebb32236dd1f12dfb1d337ba96a7c748f3da491eecca4ed31056cab4db2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180500bef5ce79ea75a36d255cb9f9cab18680e34f34033ecb0d424d3eace168(
    value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc19f7555adeb4c3049cbe1382d46551b1a8c7cbe96f386abf0add52a853f19(
    *,
    schedule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a719bb93b7f751b2f228a7bf3047150a23f99f24bf71298e1c10b721e157a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7b9cc07533a54851425dc583042174fa26940b1ac80fdeafb3348a4ddf3990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8836a854f9e2fd153cc623014fb918174173aea140215af7dc19ebd144c3be19(
    value: typing.Optional[ComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607efe77891cb51555d5a0201e0546837cad3ac7a3200916fc857e64050c6bb0(
    *,
    schedule: typing.Union[ComputeResourcePolicySnapshotSchedulePolicySchedule, typing.Dict[builtins.str, typing.Any]],
    retention_policy: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_properties: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a96a8832b016496638d2a76ec08067b9c5198d7d96af822a6b1bd39eaccea174(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181cb24bd018eb2b496b36ec3c308c49ec755823da8234c4f6bcf07e8938df1a(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c995b729de2f04a99ff6647534552bbd2986116c7568f0e515b5f1d871059e(
    *,
    max_retention_days: jsii.Number,
    on_source_disk_delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea736c5f0a08baf4eed8eed9c97ec10f6982afffe4f8430f64b2a37e1ed80e4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef7d33a6cc906ed0d3fa442de868c0973d5d81271be9efb575501c1849d9403(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd577d8b6a00352d96f52edc8fb41afa03ae76aff990943b4f6e480ae52ef76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e3c8a162f2a37bf374959ae9181f6db6ca32cc47350a3b45c7febb497c0165(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b083af9e99ebe6f9d2e850004ff4a4b8dcfa9932d6100d149c30a37c01151e5(
    *,
    daily_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b6c613b3f6412c4218f3f3b064e876a70572d4476afaf14c0c76308dcd302f(
    *,
    days_in_cycle: jsii.Number,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa9f0856bb2b17393d07afc5cc7aa0a3d10ca0db7edba6918a7a7fa0696d1d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f84dc3ee0dc3f9f20961054a703ff13a40081e0423be5d71147deedce803213(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed06d7c6d7296c33958f2ac073fd89bfaf10a41533ebc759db8ab4e32cd4e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b28627ced7f845990b7da86e8d54537696f4cc8256d69f9bbca006f1c06e22b(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9a6e49437c634a0ab8bac23c31b37336ff551885f97d4a8b7b169dc28b1f0f(
    *,
    hours_in_cycle: jsii.Number,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5082b775bc3fee3408c5ed275688bb1ae771110c5deb74c42808be9d0f55a0a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1803328449d0967fe72f6491d87f3f6e0e4516ca544151015bf6734fab62d4f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006d33d997dbd5de61d320ef3d279506f541ecce2e74d1fb648e3d3573c1b0f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99656fc0058d3d7b54ed75385aeda9f7f7e5f65298f0a10e0e7c46d869db3d69(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb1dbef1a9b2a268dc55e3d2ec16e232b06a1d0c36409db5e9e4e8eb0e43ad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ad4aa352c89168ecc54f5dacad48dd2eeb3298243e8f08f21c355373115fc8(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153999083f30eeef88ab0f316c6257595ccf419f7356b06c6c3eb82eaf577c51(
    *,
    day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5324d2c340ba8f3b3b42a5b968610fd0e31638ec14ee56f0b70c9d7b585eff4(
    *,
    day: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0681f63b7b95c754a38f6002c6b215c6cd4bf0cf44e9e044d4d7e3d5828ff939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90f2b0b4b28be3e45f6b269ebbc5517da7873e01069f5f8a5f4aa6bb7ca4531(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694f266c8a16b1bec06279053cdfe0409404407295860f96724bb2994a0d202c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce143c6694d3db0ec2916f94d0c39c4bd8e3e1bc19041ed65a7913b3af2ffe63(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b31c488d5cef800a363130419ded56a13d0608f9bd184021c8b8026d9cabe82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91da33fa5756f19de53c40d52a6e07e7d61ffb2874639534b5cfb7a98c08e045(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a19d9ff541cf6591b8799f1ed5ae858b006137f65e6ce00d7f8eaaf0d6bc3ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4546dc6d6987d0a30791b8a24f4caa4687839ae3bba3a4b2c373cfab0c666885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a934616ce3fe0e84d2319446de62d5c13e1cf2af860031ec9f9e0018d44f1d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338568f22215b9fdd4e5714ef4ed75181e13032905e1948ff7d18c4c7649493f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ec733e348c6c398af5adf4ab9e568f96a83f8fd69f24e2a0631e69149a7416(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a2a412d5d8dc0202720e931299f635bb1a148edc44fdfef4a8927a6f01d5c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbbbe67149d5e4192951d88cbe7d90b27386e2d8661021180597c5f7b618daa(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fa87dbaebde00a58184bcb235144c55e0ea42d40782ba5188033a07dac8dc3(
    *,
    chain_name: typing.Optional[builtins.str] = None,
    guest_flush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0857d7a02c0bae99070de036a3d69d656fa1cab00b6f5b26cdf0587804ebf1f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb120a0fc67128e814c17f41873b81fbc33c179f5124c0203c22f4b058dc020(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f529948c123fc8a636c9b7c57f08f3d2c49c7eaebc6518ad733daf530ce98125(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf713565eea776b9e0c2b69a6acfa31e085258e504ca9a220372f0f289833304(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e183f01e938a8a283da5462fc4e8f85e8fcd3c672c96158c06792d374c9808f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9563dd84b45aa2488f077e127fd59f902d88305efde74ed264649c3444db1f(
    value: typing.Optional[ComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf47e29da7b3c9ed6169e4141297ed1c09997ca9a09615d70948c188de7acf0e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea603289a872042375efe959d4b41b7b24c48b7cda66c2479a1d8a70a9c9b18d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f147578c5dc90dfad21297128f627bceac05fad31f5311c97361ef499b204d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc459f000a010422f74f024481e68de063c4e699647eb96bf3d8738d49d69645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cb05e3db8c4399c11ff6032ba5d23ef39f943d2e5a8ef930d58842ed9f3aa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a0f8b395e0d69296af137200e3f9a855dc553e4251b3b6637119a0ffa27b88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeResourcePolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__401a6c7353daf5cdddb45331b42b450d1f250fc7aba3149a5d852e08969029f0(
    *,
    type: builtins.str,
    accelerator_topology: typing.Optional[builtins.str] = None,
    max_topology_distance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed73b4346a4c7a8c3dd1c555e2849855f37914f0a3c3874c2579404e9c7be9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee13ad9147c96867fedd31c686a7887eaecf678397673ee685540da3d45d814c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e57efcac7bdfd1d20da42b13bb91c880d595a68c9abe304616b211f44e5f15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65eb3b7d5d5f2f01321998d01dd7ecda8f1463c698ac40df63abe5efab4b0e85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a530c6edc1ee60d31f6bc2d3c611b50c415e196e0022866a5c18f16b8b7569(
    value: typing.Optional[ComputeResourcePolicyWorkloadPolicy],
) -> None:
    """Type checking stubs"""
    pass

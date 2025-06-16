r'''
# `google_compute_resource_policy`

Refer to the Terraform Registry for docs: [`google_compute_resource_policy`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy).
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


class GoogleComputeResourcePolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy google_compute_resource_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disk_consistency_group_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        group_placement_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyGroupPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeResourcePolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyWorkloadPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy google_compute_resource_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#name GoogleComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#description GoogleComputeResourcePolicy#description}
        :param disk_consistency_group_policy: disk_consistency_group_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#disk_consistency_group_policy GoogleComputeResourcePolicy#disk_consistency_group_policy}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#group_placement_policy GoogleComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#id GoogleComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#instance_schedule_policy GoogleComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#project GoogleComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#region GoogleComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_schedule_policy GoogleComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#timeouts GoogleComputeResourcePolicy#timeouts}
        :param workload_policy: workload_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#workload_policy GoogleComputeResourcePolicy#workload_policy}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405aac0afc3e649d3b182a2862299dd14d648f8cb8442c2754efca139199006e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeResourcePolicyConfig(
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
        '''Generates CDKTF code for importing a GoogleComputeResourcePolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleComputeResourcePolicy to import.
        :param import_from_id: The id of the existing GoogleComputeResourcePolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleComputeResourcePolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062996597ecebbcd0cf48aafb05ddc36a8b3214d4bf26420e285a28f27262ad3)
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
        :param enabled: Enable disk consistency on the resource policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#enabled GoogleComputeResourcePolicy#enabled}
        '''
        value = GoogleComputeResourcePolicyDiskConsistencyGroupPolicy(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putDiskConsistencyGroupPolicy", [value]))

    @jsii.member(jsii_name="putGroupPlacementPolicy")
    def put_group_placement_policy(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        gpu_topology: typing.Optional[builtins.str] = None,
        max_distance: typing.Optional[jsii.Number] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#availability_domain_count GoogleComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#collocation GoogleComputeResourcePolicy#collocation}
        :param gpu_topology: Specifies the shape of the GPU slice, in slice based GPU families eg. A4X. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#gpu_topology GoogleComputeResourcePolicy#gpu_topology}
        :param max_distance: Specifies the number of max logical switches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_distance GoogleComputeResourcePolicy#max_distance}
        :param tpu_topology: Specifies the shape of the TPU slice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#tpu_topology GoogleComputeResourcePolicy#tpu_topology}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_count GoogleComputeResourcePolicy#vm_count}
        '''
        value = GoogleComputeResourcePolicyGroupPlacementPolicy(
            availability_domain_count=availability_domain_count,
            collocation=collocation,
            gpu_topology=gpu_topology,
            max_distance=max_distance,
            tpu_topology=tpu_topology,
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
        vm_start_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#time_zone GoogleComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#expiration_time GoogleComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_start_schedule GoogleComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_stop_schedule GoogleComputeResourcePolicy#vm_stop_schedule}
        '''
        value = GoogleComputeResourcePolicyInstanceSchedulePolicy(
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
        schedule: typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[builtins.str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#retention_policy GoogleComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_properties GoogleComputeResourcePolicy#snapshot_properties}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#create GoogleComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#delete GoogleComputeResourcePolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#update GoogleComputeResourcePolicy#update}.
        '''
        value = GoogleComputeResourcePolicyTimeouts(
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
        :param type: The type of workload policy. Possible values: ["HIGH_AVAILABILITY", "HIGH_THROUGHPUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#type GoogleComputeResourcePolicy#type}
        :param accelerator_topology: The accelerator topology. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if max topology distance is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#accelerator_topology GoogleComputeResourcePolicy#accelerator_topology}
        :param max_topology_distance: The maximum topology distance. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_topology_distance GoogleComputeResourcePolicy#max_topology_distance}
        '''
        value = GoogleComputeResourcePolicyWorkloadPolicy(
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
    ) -> "GoogleComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference", jsii.get(self, "diskConsistencyGroupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="groupPlacementPolicy")
    def group_placement_policy(
        self,
    ) -> "GoogleComputeResourcePolicyGroupPlacementPolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicyGroupPlacementPolicyOutputReference", jsii.get(self, "groupPlacementPolicy"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicy")
    def instance_schedule_policy(
        self,
    ) -> "GoogleComputeResourcePolicyInstanceSchedulePolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicyInstanceSchedulePolicyOutputReference", jsii.get(self, "instanceSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="snapshotSchedulePolicy")
    def snapshot_schedule_policy(
        self,
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicyOutputReference", jsii.get(self, "snapshotSchedulePolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeResourcePolicyTimeoutsOutputReference":
        return typing.cast("GoogleComputeResourcePolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicy")
    def workload_policy(
        self,
    ) -> "GoogleComputeResourcePolicyWorkloadPolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicyWorkloadPolicyOutputReference", jsii.get(self, "workloadPolicy"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskConsistencyGroupPolicyInput")
    def disk_consistency_group_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy"], jsii.get(self, "diskConsistencyGroupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="groupPlacementPolicyInput")
    def group_placement_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyGroupPlacementPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyGroupPlacementPolicy"], jsii.get(self, "groupPlacementPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSchedulePolicyInput")
    def instance_schedule_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicy"], jsii.get(self, "instanceSchedulePolicyInput"))

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
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicy"], jsii.get(self, "snapshotSchedulePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeResourcePolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeResourcePolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadPolicyInput")
    def workload_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyWorkloadPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyWorkloadPolicy"], jsii.get(self, "workloadPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941b15e635d55e978c170de06b4d295bb7f97c8a2f846ea5d96d357657265e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf55deb133860b2fc8ae0f21a0691ff66d760f5c4e32aecca0aa4c9f089539cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec4d5c0ead4fbb9c6760410f7fd4ae6c2ccdf9d415989ad153b70756c77194a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31c3a57b364833f75d87fcda509082e8aff9beeb773b0de685b1420462a8aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecc6150b5ed4b55d21efe8873b27e63ba4a5ea715f19db15d6f2565b079210f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyConfig",
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
class GoogleComputeResourcePolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk_consistency_group_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        group_placement_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyGroupPlacementPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_schedule_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        snapshot_schedule_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeResourcePolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicyWorkloadPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_'? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#name GoogleComputeResourcePolicy#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#description GoogleComputeResourcePolicy#description}
        :param disk_consistency_group_policy: disk_consistency_group_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#disk_consistency_group_policy GoogleComputeResourcePolicy#disk_consistency_group_policy}
        :param group_placement_policy: group_placement_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#group_placement_policy GoogleComputeResourcePolicy#group_placement_policy}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#id GoogleComputeResourcePolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_schedule_policy: instance_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#instance_schedule_policy GoogleComputeResourcePolicy#instance_schedule_policy}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#project GoogleComputeResourcePolicy#project}.
        :param region: Region where resource policy resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#region GoogleComputeResourcePolicy#region}
        :param snapshot_schedule_policy: snapshot_schedule_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_schedule_policy GoogleComputeResourcePolicy#snapshot_schedule_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#timeouts GoogleComputeResourcePolicy#timeouts}
        :param workload_policy: workload_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#workload_policy GoogleComputeResourcePolicy#workload_policy}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(disk_consistency_group_policy, dict):
            disk_consistency_group_policy = GoogleComputeResourcePolicyDiskConsistencyGroupPolicy(**disk_consistency_group_policy)
        if isinstance(group_placement_policy, dict):
            group_placement_policy = GoogleComputeResourcePolicyGroupPlacementPolicy(**group_placement_policy)
        if isinstance(instance_schedule_policy, dict):
            instance_schedule_policy = GoogleComputeResourcePolicyInstanceSchedulePolicy(**instance_schedule_policy)
        if isinstance(snapshot_schedule_policy, dict):
            snapshot_schedule_policy = GoogleComputeResourcePolicySnapshotSchedulePolicy(**snapshot_schedule_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeResourcePolicyTimeouts(**timeouts)
        if isinstance(workload_policy, dict):
            workload_policy = GoogleComputeResourcePolicyWorkloadPolicy(**workload_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843f8d6a2bbce0a06666e7745389d26a85264b2b841c7c5309eb706f3c6ad97a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#name GoogleComputeResourcePolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#description GoogleComputeResourcePolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_consistency_group_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy"]:
        '''disk_consistency_group_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#disk_consistency_group_policy GoogleComputeResourcePolicy#disk_consistency_group_policy}
        '''
        result = self._values.get("disk_consistency_group_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyDiskConsistencyGroupPolicy"], result)

    @builtins.property
    def group_placement_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyGroupPlacementPolicy"]:
        '''group_placement_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#group_placement_policy GoogleComputeResourcePolicy#group_placement_policy}
        '''
        result = self._values.get("group_placement_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyGroupPlacementPolicy"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#id GoogleComputeResourcePolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_schedule_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicy"]:
        '''instance_schedule_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#instance_schedule_policy GoogleComputeResourcePolicy#instance_schedule_policy}
        '''
        result = self._values.get("instance_schedule_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicy"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#project GoogleComputeResourcePolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where resource policy resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#region GoogleComputeResourcePolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_schedule_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicy"]:
        '''snapshot_schedule_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_schedule_policy GoogleComputeResourcePolicy#snapshot_schedule_policy}
        '''
        result = self._values.get("snapshot_schedule_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeResourcePolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#timeouts GoogleComputeResourcePolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyTimeouts"], result)

    @builtins.property
    def workload_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyWorkloadPolicy"]:
        '''workload_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#workload_policy GoogleComputeResourcePolicy#workload_policy}
        '''
        result = self._values.get("workload_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyWorkloadPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyDiskConsistencyGroupPolicy",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleComputeResourcePolicyDiskConsistencyGroupPolicy:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable disk consistency on the resource policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#enabled GoogleComputeResourcePolicy#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a65697076cc8b527c37ac671dcff7bdd055fc9860bfcc2b51c1bdde26625679)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable disk consistency on the resource policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#enabled GoogleComputeResourcePolicy#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyDiskConsistencyGroupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56f0f34a4ff098957a649e8e060bea12b192be97c6aae51764651ca5b5e39f3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de2555964ca9fb1d198ea4de6f884dff052c0fef133c5c09f9ab1d6d55a05ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f42a45739373865834610c6c3622a4a856339ca491713fc9ebd087f68cc934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyGroupPlacementPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "availability_domain_count": "availabilityDomainCount",
        "collocation": "collocation",
        "gpu_topology": "gpuTopology",
        "max_distance": "maxDistance",
        "tpu_topology": "tpuTopology",
        "vm_count": "vmCount",
    },
)
class GoogleComputeResourcePolicyGroupPlacementPolicy:
    def __init__(
        self,
        *,
        availability_domain_count: typing.Optional[jsii.Number] = None,
        collocation: typing.Optional[builtins.str] = None,
        gpu_topology: typing.Optional[builtins.str] = None,
        max_distance: typing.Optional[jsii.Number] = None,
        tpu_topology: typing.Optional[builtins.str] = None,
        vm_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_domain_count: The number of availability domains instances will be spread across. If two instances are in different availability domain, they will not be put in the same low latency network Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#availability_domain_count GoogleComputeResourcePolicy#availability_domain_count}
        :param collocation: Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network. Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy attached. Possible values: ["COLLOCATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#collocation GoogleComputeResourcePolicy#collocation}
        :param gpu_topology: Specifies the shape of the GPU slice, in slice based GPU families eg. A4X. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#gpu_topology GoogleComputeResourcePolicy#gpu_topology}
        :param max_distance: Specifies the number of max logical switches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_distance GoogleComputeResourcePolicy#max_distance}
        :param tpu_topology: Specifies the shape of the TPU slice. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#tpu_topology GoogleComputeResourcePolicy#tpu_topology}
        :param vm_count: Number of VMs in this placement group. Google does not recommend that you use this field unless you use a compact policy and you want your policy to work only if it contains this exact number of VMs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_count GoogleComputeResourcePolicy#vm_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db4d8cce4484aedfc9b69823c9b1658b16aef170aa4779d79ce656ffabba8c8)
            check_type(argname="argument availability_domain_count", value=availability_domain_count, expected_type=type_hints["availability_domain_count"])
            check_type(argname="argument collocation", value=collocation, expected_type=type_hints["collocation"])
            check_type(argname="argument gpu_topology", value=gpu_topology, expected_type=type_hints["gpu_topology"])
            check_type(argname="argument max_distance", value=max_distance, expected_type=type_hints["max_distance"])
            check_type(argname="argument tpu_topology", value=tpu_topology, expected_type=type_hints["tpu_topology"])
            check_type(argname="argument vm_count", value=vm_count, expected_type=type_hints["vm_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_domain_count is not None:
            self._values["availability_domain_count"] = availability_domain_count
        if collocation is not None:
            self._values["collocation"] = collocation
        if gpu_topology is not None:
            self._values["gpu_topology"] = gpu_topology
        if max_distance is not None:
            self._values["max_distance"] = max_distance
        if tpu_topology is not None:
            self._values["tpu_topology"] = tpu_topology
        if vm_count is not None:
            self._values["vm_count"] = vm_count

    @builtins.property
    def availability_domain_count(self) -> typing.Optional[jsii.Number]:
        '''The number of availability domains instances will be spread across.

        If two instances are in different
        availability domain, they will not be put in the same low latency network

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#availability_domain_count GoogleComputeResourcePolicy#availability_domain_count}
        '''
        result = self._values.get("availability_domain_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def collocation(self) -> typing.Optional[builtins.str]:
        '''Collocation specifies whether to place VMs inside the same availability domain on the same low-latency network.

        Specify 'COLLOCATED' to enable collocation. Can only be specified with 'vm_count'. If compute instances are created
        with a COLLOCATED policy, then exactly 'vm_count' instances must be created at the same time with the resource policy
        attached. Possible values: ["COLLOCATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#collocation GoogleComputeResourcePolicy#collocation}
        '''
        result = self._values.get("collocation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_topology(self) -> typing.Optional[builtins.str]:
        '''Specifies the shape of the GPU slice, in slice based GPU families eg. A4X.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#gpu_topology GoogleComputeResourcePolicy#gpu_topology}
        '''
        result = self._values.get("gpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_distance(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of max logical switches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_distance GoogleComputeResourcePolicy#max_distance}
        '''
        result = self._values.get("max_distance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tpu_topology(self) -> typing.Optional[builtins.str]:
        '''Specifies the shape of the TPU slice.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#tpu_topology GoogleComputeResourcePolicy#tpu_topology}
        '''
        result = self._values.get("tpu_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_count(self) -> typing.Optional[jsii.Number]:
        '''Number of VMs in this placement group.

        Google does not recommend that you use this field
        unless you use a compact policy and you want your policy to work only if it contains this
        exact number of VMs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_count GoogleComputeResourcePolicy#vm_count}
        '''
        result = self._values.get("vm_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyGroupPlacementPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyGroupPlacementPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyGroupPlacementPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ec969bd7e647076410dd72153f57127c97603a7b093b74ef76bd5ec6b07be5)
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

    @jsii.member(jsii_name="resetMaxDistance")
    def reset_max_distance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDistance", []))

    @jsii.member(jsii_name="resetTpuTopology")
    def reset_tpu_topology(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpuTopology", []))

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
    @jsii.member(jsii_name="maxDistanceInput")
    def max_distance_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDistanceInput"))

    @builtins.property
    @jsii.member(jsii_name="tpuTopologyInput")
    def tpu_topology_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpuTopologyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b30014f8824776f264b0f6a70014076ac29b695c7c63033c9ae8a2ae933ff458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomainCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collocation")
    def collocation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collocation"))

    @collocation.setter
    def collocation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7826747346de304bc3ae42099214a5921d6c2b18eae248254c83d8b36382724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuTopology")
    def gpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuTopology"))

    @gpu_topology.setter
    def gpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eab7bd964597596766042a76ef5084266007bd8834a2c71b79b0e5ec89ff064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDistance")
    def max_distance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDistance"))

    @max_distance.setter
    def max_distance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb63379ec54941ef9e215a84eabd0207de482b69b7beb904dd3688cb03ef5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDistance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tpuTopology")
    def tpu_topology(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpuTopology"))

    @tpu_topology.setter
    def tpu_topology(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e46438a243f294fea33573a0ac428f12a59bb87a7d317f25de6c27306357151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpuTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmCount")
    def vm_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vmCount"))

    @vm_count.setter
    def vm_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351bc2512f8df46368583d8a5b5e54d18508ca8b0a8df8135ae60988a3f042da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyGroupPlacementPolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyGroupPlacementPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyGroupPlacementPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c32b08ab44340187757d332a0058fc30f91b0e9201ee229dc0a63992c3ef50f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "expiration_time": "expirationTime",
        "start_time": "startTime",
        "vm_start_schedule": "vmStartSchedule",
        "vm_stop_schedule": "vmStopSchedule",
    },
)
class GoogleComputeResourcePolicyInstanceSchedulePolicy:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        vm_start_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        vm_stop_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_zone: Specifies the time zone to be used in interpreting the schedule. The value of this field must be a time zone name from the tz database: http://en.wikipedia.org/wiki/Tz_database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#time_zone GoogleComputeResourcePolicy#time_zone}
        :param expiration_time: The expiration time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#expiration_time GoogleComputeResourcePolicy#expiration_time}
        :param start_time: The start time of the schedule. The timestamp is an RFC3339 string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        :param vm_start_schedule: vm_start_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_start_schedule GoogleComputeResourcePolicy#vm_start_schedule}
        :param vm_stop_schedule: vm_stop_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_stop_schedule GoogleComputeResourcePolicy#vm_stop_schedule}
        '''
        if isinstance(vm_start_schedule, dict):
            vm_start_schedule = GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(**vm_start_schedule)
        if isinstance(vm_stop_schedule, dict):
            vm_stop_schedule = GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(**vm_stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57ab56e53516ada146be5d75c7ad154774bdff301f61a58d480dd364f185b653)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#time_zone GoogleComputeResourcePolicy#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''The expiration time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#expiration_time GoogleComputeResourcePolicy#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time of the schedule. The timestamp is an RFC3339 string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_start_schedule(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        '''vm_start_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_start_schedule GoogleComputeResourcePolicy#vm_start_schedule}
        '''
        result = self._values.get("vm_start_schedule")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], result)

    @builtins.property
    def vm_stop_schedule(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        '''vm_stop_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#vm_stop_schedule GoogleComputeResourcePolicy#vm_stop_schedule}
        '''
        result = self._values.get("vm_stop_schedule")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyInstanceSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyInstanceSchedulePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da2ee775b1bd8c2ef23264a7aeeb4abb23105397c47716bd9a369fed59a9e887)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putVmStartSchedule")
    def put_vm_start_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        value = GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(
            schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putVmStartSchedule", [value]))

    @jsii.member(jsii_name="putVmStopSchedule")
    def put_vm_stop_schedule(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        value = GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(
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
    ) -> "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference":
        return typing.cast("GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference", jsii.get(self, "vmStartSchedule"))

    @builtins.property
    @jsii.member(jsii_name="vmStopSchedule")
    def vm_stop_schedule(
        self,
    ) -> "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference":
        return typing.cast("GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference", jsii.get(self, "vmStopSchedule"))

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
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule"], jsii.get(self, "vmStartScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="vmStopScheduleInput")
    def vm_stop_schedule_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule"], jsii.get(self, "vmStopScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5d3beed73daddb51ce0c4cf661a6a5dabad1755e97c3e7bd467c942326d702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3386a15b9909ca4bd7072b09fcf05396e7e5bf5318bd28d24b8e64f2aaa437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bde2d214b86c2d19b30dbde38d10b1b1fb5ee3e20b5cdc355dafd8972d38fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce56849faff5c365db0224d6d85c88355a5257456ebadc5fbc91c14c725b56d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2175abf81687158bad1e61026208b9534b2aaaaaa7fff185301c479f40bb37c9)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d469528d4dd63e56294b90accc4b5829058241eb73d863f744e0379284f19a16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__267efee1e097c437adf7311e7abecfedb70f808db71086e36b7f96131b238c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b57893c6f59422e4494f071b5b97c5d4c1b098c69c0b29a179ba89b2f097dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule:
    def __init__(self, *, schedule: builtins.str) -> None:
        '''
        :param schedule: Specifies the frequency for the operation, using the unix-cron format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801a401e35f986818c01eaae6e307b58274dbd7e93258a2ec7f86ecdc53c1ca6)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }

    @builtins.property
    def schedule(self) -> builtins.str:
        '''Specifies the frequency for the operation, using the unix-cron format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d0d56e7c250376e14e3cf14ae6df6961f1fac91dc17d7d128a0e96130285c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4029f7b010dfec6dfc24f7a1826f75a5a63ed72f9d59385408574d57347819fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83a50c52afaaad35c7421b09b26a483749b7472c11aaaa1ba44084e9216ef1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "retention_policy": "retentionPolicy",
        "snapshot_properties": "snapshotProperties",
    },
)
class GoogleComputeResourcePolicySnapshotSchedulePolicy:
    def __init__(
        self,
        *,
        schedule: typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicySchedule", typing.Dict[builtins.str, typing.Any]],
        retention_policy: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        snapshot_properties: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#retention_policy GoogleComputeResourcePolicy#retention_policy}
        :param snapshot_properties: snapshot_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_properties GoogleComputeResourcePolicy#snapshot_properties}
        '''
        if isinstance(schedule, dict):
            schedule = GoogleComputeResourcePolicySnapshotSchedulePolicySchedule(**schedule)
        if isinstance(retention_policy, dict):
            retention_policy = GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(**retention_policy)
        if isinstance(snapshot_properties, dict):
            snapshot_properties = GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(**snapshot_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe71fd20748caac7ba04e26502340eb3b69733c70e6d951dd72805193634af8)
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
    def schedule(self) -> "GoogleComputeResourcePolicySnapshotSchedulePolicySchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#schedule GoogleComputeResourcePolicy#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicySchedule", result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#retention_policy GoogleComputeResourcePolicy#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], result)

    @builtins.property
    def snapshot_properties(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        '''snapshot_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#snapshot_properties GoogleComputeResourcePolicy#snapshot_properties}
        '''
        result = self._values.get("snapshot_properties")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33dc0abda49d92a5cf5cf2ba1aac33fb4fae2a85ea1b3c0aea9a9b93eb756695)
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
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_retention_days GoogleComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#on_source_disk_delete GoogleComputeResourcePolicy#on_source_disk_delete}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(
            max_retention_days=max_retention_days,
            on_source_disk_delete=on_source_disk_delete,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#daily_schedule GoogleComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hourly_schedule GoogleComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#weekly_schedule GoogleComputeResourcePolicy#weekly_schedule}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicySchedule(
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
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#chain_name GoogleComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#guest_flush GoogleComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#labels GoogleComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#storage_locations GoogleComputeResourcePolicy#storage_locations}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(
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
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference":
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference":
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="snapshotProperties")
    def snapshot_properties(
        self,
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference":
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference", jsii.get(self, "snapshotProperties"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySchedule"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPropertiesInput")
    def snapshot_properties_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties"], jsii.get(self, "snapshotPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39397c4432e092f0f1dd96a2fb0cb28c502386a86e33e7ec1d703295806488f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_retention_days": "maxRetentionDays",
        "on_source_disk_delete": "onSourceDiskDelete",
    },
)
class GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy:
    def __init__(
        self,
        *,
        max_retention_days: jsii.Number,
        on_source_disk_delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param max_retention_days: Maximum age of the snapshot that is allowed to be kept. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_retention_days GoogleComputeResourcePolicy#max_retention_days}
        :param on_source_disk_delete: Specifies the behavior to apply to scheduled snapshots when the source disk is deleted. Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#on_source_disk_delete GoogleComputeResourcePolicy#on_source_disk_delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a036fa3ffc0db402dd8dff1ba97d01a8f6fb887313da9c0cbbdbd1744a2fcddb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_retention_days GoogleComputeResourcePolicy#max_retention_days}
        '''
        result = self._values.get("max_retention_days")
        assert result is not None, "Required property 'max_retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def on_source_disk_delete(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior to apply to scheduled snapshots when the source disk is deleted.

        Default value: "KEEP_AUTO_SNAPSHOTS" Possible values: ["KEEP_AUTO_SNAPSHOTS", "APPLY_RETENTION_POLICY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#on_source_disk_delete GoogleComputeResourcePolicy#on_source_disk_delete}
        '''
        result = self._values.get("on_source_disk_delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63eb75707d0b8a95cc3de3e29e04916187b2ce2b1b929e6ee8f6446866efe555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df61642271587c8eab4f3a6166fa9f6ed363eea84e96c49489d3a85d6f2d7b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onSourceDiskDelete")
    def on_source_disk_delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onSourceDiskDelete"))

    @on_source_disk_delete.setter
    def on_source_disk_delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1582623857ff964d6af38ef5871b983ec4d1200fee3135d2e0dc8f2c5a8ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onSourceDiskDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e839e0023332f574570ccfe298fd3080e5a151a16ed89ef64eeb4871001b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "hourly_schedule": "hourlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class GoogleComputeResourcePolicySnapshotSchedulePolicySchedule:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        hourly_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#daily_schedule GoogleComputeResourcePolicy#daily_schedule}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hourly_schedule GoogleComputeResourcePolicy#hourly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#weekly_schedule GoogleComputeResourcePolicy#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(**hourly_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07361f893c01435aca4ab2ebd70e7d676efbc7d1f843e8177811cbdfd130660e)
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
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#daily_schedule GoogleComputeResourcePolicy#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule"], result)

    @builtins.property
    def hourly_schedule(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hourly_schedule GoogleComputeResourcePolicy#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#weekly_schedule GoogleComputeResourcePolicy#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    jsii_struct_bases=[],
    name_mapping={"days_in_cycle": "daysInCycle", "start_time": "startTime"},
)
class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule:
    def __init__(self, *, days_in_cycle: jsii.Number, start_time: builtins.str) -> None:
        '''
        :param days_in_cycle: Defines a schedule with units measured in days. The value determines how many days pass between the start of each cycle. Days in cycle for snapshot schedule policy must be 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#days_in_cycle GoogleComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d8ccf1de1af88cdcd56e7eaab88dc5e19cf82e2884965590fbb84fd7f09a86)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#days_in_cycle GoogleComputeResourcePolicy#days_in_cycle}
        '''
        result = self._values.get("days_in_cycle")
        assert result is not None, "Required property 'days_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00.

        For example,
        both 13:00-5 and 08:00 are valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__760089ff30699346acdbdb94fd850d6d780cf266ed71f07408b5867f119e1ee5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9ac641f58a04edd4df572ebd2a0ece73da14510615f43e16f245cd8c204521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysInCycle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9006599c2a6fd6f7132edcf99046fb260f239d3a2cc2425a3dc6ac678bcccce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b130897f5e6f4dca325f0bf07f78bfc6fdf4b1eae80e8dda082701d66e0ed36e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"hours_in_cycle": "hoursInCycle", "start_time": "startTime"},
)
class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule:
    def __init__(
        self,
        *,
        hours_in_cycle: jsii.Number,
        start_time: builtins.str,
    ) -> None:
        '''
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hours_in_cycle GoogleComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec953b9961a7545f4b814387a958d206f70f4cbc842e5cb4afb44dfb4355bc9a)
            check_type(argname="argument hours_in_cycle", value=hours_in_cycle, expected_type=type_hints["hours_in_cycle"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours_in_cycle": hours_in_cycle,
            "start_time": start_time,
        }

    @builtins.property
    def hours_in_cycle(self) -> jsii.Number:
        '''The number of hours between snapshots.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hours_in_cycle GoogleComputeResourcePolicy#hours_in_cycle}
        '''
        result = self._values.get("hours_in_cycle")
        assert result is not None, "Required property 'hours_in_cycle' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in an hourly format "HH:MM",
        where HH : [00-23] and MM : [00] GMT. eg: 21:00

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ed6d84ce28c99649a82fb7837e297f571e7f79102cdb10c581dbc98af5cdff3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ec04ca78318de08f822c2462701b0a1f9db9476402cb2f2e04ab3dec59887f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hoursInCycle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab47d213009037d5bec2f4eb5922c96ccab1e7e546335565b70840614371970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a96b92ea8354095f4d2c0a84e4b09f75d050e495336db5fba0c534aa0b8a346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__961940afb5297764836768000c7953488a097700b0165f609eaf772cc260e120)
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
        :param days_in_cycle: Defines a schedule with units measured in days. The value determines how many days pass between the start of each cycle. Days in cycle for snapshot schedule policy must be 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#days_in_cycle GoogleComputeResourcePolicy#days_in_cycle}
        :param start_time: This must be in UTC format that resolves to one of 00:00, 04:00, 08:00, 12:00, 16:00, or 20:00. For example, both 13:00-5 and 08:00 are valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule(
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
        :param hours_in_cycle: The number of hours between snapshots. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#hours_in_cycle GoogleComputeResourcePolicy#hours_in_cycle}
        :param start_time: Time within the window to start the operations. It must be in an hourly format "HH:MM", where HH : [00-23] and MM : [00] GMT. eg: 21:00 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule(
            hours_in_cycle=hours_in_cycle, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putHourlySchedule", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#day_of_weeks GoogleComputeResourcePolicy#day_of_weeks}
        '''
        value = GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(
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
    ) -> GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference:
        return typing.cast(GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(
        self,
    ) -> GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference:
        return typing.cast(GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference, jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference":
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyScheduleInput")
    def hourly_schedule_input(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"]:
        return typing.cast(typing.Optional["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd5ba24f30b73aaffa249cb1e166e38ed0b4e09403b3641ab922404458123d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={"day_of_weeks": "dayOfWeeks"},
)
class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule:
    def __init__(
        self,
        *,
        day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param day_of_weeks: day_of_weeks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#day_of_weeks GoogleComputeResourcePolicy#day_of_weeks}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d043619940693724a8c6d40863df70ddac029d6ea244d66f07949f5da37eaa)
            check_type(argname="argument day_of_weeks", value=day_of_weeks, expected_type=type_hints["day_of_weeks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_weeks": day_of_weeks,
        }

    @builtins.property
    def day_of_weeks(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]]:
        '''day_of_weeks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#day_of_weeks GoogleComputeResourcePolicy#day_of_weeks}
        '''
        result = self._values.get("day_of_weeks")
        assert result is not None, "Required property 'day_of_weeks' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks:
    def __init__(self, *, day: builtins.str, start_time: builtins.str) -> None:
        '''
        :param day: The day of the week to create the snapshot. e.g. MONDAY Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#day GoogleComputeResourcePolicy#day}
        :param start_time: Time within the window to start the operations. It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1beef23655fd5bbb8eed8b15abecb57a5d11a7a200cdce0f78f45a197db3c987)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#day GoogleComputeResourcePolicy#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Time within the window to start the operations.

        It must be in format "HH:MM", where HH : [00-23] and MM : [00-00] GMT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#start_time GoogleComputeResourcePolicy#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7330895ed4738754f37a097dcf3b67faa410b0009b771658858ca433f8924db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5463436b46768b77e85835a045aad764bf5c686306005bd430e207ed9d173d85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767b8b6e995291d8da4aeaf4d712e73dc35f7147bcbdcb3f6eecba1bb3385124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b668795617282eb89e1b45d1edd61734ab4f71adf512b6bc95f556b5f482d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e84fe6e16ae43bb0b9af44f84e5440496c5c5dff6e1eb3105f44f55d288e5279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363b684cfe54acc69a152d08c149bb7c316c8def8712cdb38dc6ccc1ef4314f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef354fe68a878ae9f96b5139795ac4ff3e16fc8b7ff2836fe500a2df417d192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d639a23c3e15fc972579e8e5f239b44e4b2a6fef862c5ca9b1cada29b4cc01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27486c5a4dc186a64271a42035e11b56c6cbaedaeb6ec1143a33052c64d96f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4313f52883506ff15997bdb8c221848188d46733bc94f464e25840c6077f847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faa1d6f5ae4ad11798f82f749af36a14494ce7f894fd966b841d1c93d1f7e53d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDayOfWeeks")
    def put_day_of_weeks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bb4181fa9324061d133f4b0471f2c1eda40c9a91f3c3f0757ee75d16dc9b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDayOfWeeks", [value]))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeks")
    def day_of_weeks(
        self,
    ) -> GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList:
        return typing.cast(GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList, jsii.get(self, "dayOfWeeks"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeeksInput")
    def day_of_weeks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]], jsii.get(self, "dayOfWeeksInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12adcbdd6f2147838e8ed87d84cc01243e9f242987f8f790ffeead1c87ad3fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    jsii_struct_bases=[],
    name_mapping={
        "chain_name": "chainName",
        "guest_flush": "guestFlush",
        "labels": "labels",
        "storage_locations": "storageLocations",
    },
)
class GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties:
    def __init__(
        self,
        *,
        chain_name: typing.Optional[builtins.str] = None,
        guest_flush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param chain_name: Creates the new snapshot in the snapshot chain labeled with the specified name. The chain name must be 1-63 characters long and comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#chain_name GoogleComputeResourcePolicy#chain_name}
        :param guest_flush: Whether to perform a 'guest aware' snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#guest_flush GoogleComputeResourcePolicy#guest_flush}
        :param labels: A set of key-value pairs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#labels GoogleComputeResourcePolicy#labels}
        :param storage_locations: Cloud Storage bucket location to store the auto snapshot (regional or multi-regional). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#storage_locations GoogleComputeResourcePolicy#storage_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a51e60fada8d896a526bcc79eab3504bd5622b116ed471a779894f5bf2fc7f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#chain_name GoogleComputeResourcePolicy#chain_name}
        '''
        result = self._values.get("chain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_flush(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to perform a 'guest aware' snapshot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#guest_flush GoogleComputeResourcePolicy#guest_flush}
        '''
        result = self._values.get("guest_flush")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key-value pairs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#labels GoogleComputeResourcePolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def storage_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage bucket location to store the auto snapshot (regional or multi-regional).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#storage_locations GoogleComputeResourcePolicy#storage_locations}
        '''
        result = self._values.get("storage_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__482e5fdbe1378b8386806e92d1f8b26e4ec71eaf3a2f15cb56013377dc8a5df0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ea3ec9ca4c385f0ae2a394b738b5902360cd1dcc4dfb49174e63d1525c920a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dca2b838dfbe315f885c752b9557fc8acc2af41787684ba1a3c53419f2321c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestFlush", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a1ffbf69c484a029e9f791d2699bf9fd3821fddc514af0c560eb53e53633d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageLocations")
    def storage_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageLocations"))

    @storage_locations.setter
    def storage_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42e09eba184c93c108a26db788ae0e6ac857afc1c46da58d509141a6f280fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82d787815b14295271902f59d98348b6cf11d7a5c02a68d29a8aeaddd9ce084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeResourcePolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#create GoogleComputeResourcePolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#delete GoogleComputeResourcePolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#update GoogleComputeResourcePolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc52d7d2fe0ff385af7e3a90b2a976cf111f870587a7a3a709a78cd08b4a63e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#create GoogleComputeResourcePolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#delete GoogleComputeResourcePolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#update GoogleComputeResourcePolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__273b2e3f8949a70dfbb26a008363a604253034e985bd0ed55710d8f33d7bb76b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31376eb67415ea8b758c40af140b9fe9c73b680aca369981dffe8695521dd5a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ba8b7fdc6435629cbc0cb7c5e1e42aa5abc972a17455cf0d65471243af5870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b67b1c7d3d67577cb377e75c7d5abf1ddfe97f6ed33c829a1a0011a03d998b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950bfc98d5d45955328bdf0b1f4f2cfb33f076cbd79a714fdddc23ad04c66c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyWorkloadPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "accelerator_topology": "acceleratorTopology",
        "max_topology_distance": "maxTopologyDistance",
    },
)
class GoogleComputeResourcePolicyWorkloadPolicy:
    def __init__(
        self,
        *,
        type: builtins.str,
        accelerator_topology: typing.Optional[builtins.str] = None,
        max_topology_distance: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: The type of workload policy. Possible values: ["HIGH_AVAILABILITY", "HIGH_THROUGHPUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#type GoogleComputeResourcePolicy#type}
        :param accelerator_topology: The accelerator topology. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if max topology distance is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#accelerator_topology GoogleComputeResourcePolicy#accelerator_topology}
        :param max_topology_distance: The maximum topology distance. This field can be set only when the workload policy type is HIGH_THROUGHPUT and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_topology_distance GoogleComputeResourcePolicy#max_topology_distance}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41b119b41850e59796879b871fba2b761099070c635544de095f5ca09bc5bea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#type GoogleComputeResourcePolicy#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_topology(self) -> typing.Optional[builtins.str]:
        '''The accelerator topology.

        This field can be set only when the workload policy type is HIGH_THROUGHPUT
        and cannot be set if max topology distance is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#accelerator_topology GoogleComputeResourcePolicy#accelerator_topology}
        '''
        result = self._values.get("accelerator_topology")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_topology_distance(self) -> typing.Optional[builtins.str]:
        '''The maximum topology distance.

        This field can be set only when the workload policy type is HIGH_THROUGHPUT
        and cannot be set if accelerator topology is set. Possible values: ["BLOCK", "CLUSTER", "SUBBLOCK"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_compute_resource_policy#max_topology_distance GoogleComputeResourcePolicy#max_topology_distance}
        '''
        result = self._values.get("max_topology_distance")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeResourcePolicyWorkloadPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeResourcePolicyWorkloadPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeResourcePolicy.GoogleComputeResourcePolicyWorkloadPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44c9c3e78a97a04cdc98c51b3c95fac152a7a3113255f83ec3c2f0fbeabc991c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60debe3e054fb6bb687f74e565d7910d12207f5bbc3c12209662e0c3f65b96c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorTopology", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxTopologyDistance")
    def max_topology_distance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxTopologyDistance"))

    @max_topology_distance.setter
    def max_topology_distance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc523ceee23a560645edd5030bdd494d78ae2bc56ff819bf12ec1228897db03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTopologyDistance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e3bc2841c6cef6e05a360e0869dfd8bd75f569f36222d4b068c2e5515e3f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleComputeResourcePolicyWorkloadPolicy]:
        return typing.cast(typing.Optional[GoogleComputeResourcePolicyWorkloadPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeResourcePolicyWorkloadPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830b448bddcf20df4ded7093b11d1bb033020a50a7cca51c9783e26e3fe6f567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleComputeResourcePolicy",
    "GoogleComputeResourcePolicyConfig",
    "GoogleComputeResourcePolicyDiskConsistencyGroupPolicy",
    "GoogleComputeResourcePolicyDiskConsistencyGroupPolicyOutputReference",
    "GoogleComputeResourcePolicyGroupPlacementPolicy",
    "GoogleComputeResourcePolicyGroupPlacementPolicyOutputReference",
    "GoogleComputeResourcePolicyInstanceSchedulePolicy",
    "GoogleComputeResourcePolicyInstanceSchedulePolicyOutputReference",
    "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule",
    "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartScheduleOutputReference",
    "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule",
    "GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopScheduleOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicy",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicyOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicySchedule",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailyScheduleOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlyScheduleOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksList",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeksOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleOutputReference",
    "GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties",
    "GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotPropertiesOutputReference",
    "GoogleComputeResourcePolicyTimeouts",
    "GoogleComputeResourcePolicyTimeoutsOutputReference",
    "GoogleComputeResourcePolicyWorkloadPolicy",
    "GoogleComputeResourcePolicyWorkloadPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__405aac0afc3e649d3b182a2862299dd14d648f8cb8442c2754efca139199006e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disk_consistency_group_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    group_placement_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyGroupPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_schedule_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_schedule_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeResourcePolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyWorkloadPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__062996597ecebbcd0cf48aafb05ddc36a8b3214d4bf26420e285a28f27262ad3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941b15e635d55e978c170de06b4d295bb7f97c8a2f846ea5d96d357657265e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf55deb133860b2fc8ae0f21a0691ff66d760f5c4e32aecca0aa4c9f089539cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec4d5c0ead4fbb9c6760410f7fd4ae6c2ccdf9d415989ad153b70756c77194a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31c3a57b364833f75d87fcda509082e8aff9beeb773b0de685b1420462a8aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecc6150b5ed4b55d21efe8873b27e63ba4a5ea715f19db15d6f2565b079210f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843f8d6a2bbce0a06666e7745389d26a85264b2b841c7c5309eb706f3c6ad97a(
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
    disk_consistency_group_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    group_placement_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyGroupPlacementPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_schedule_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyInstanceSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    snapshot_schedule_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeResourcePolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicyWorkloadPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a65697076cc8b527c37ac671dcff7bdd055fc9860bfcc2b51c1bdde26625679(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56f0f34a4ff098957a649e8e060bea12b192be97c6aae51764651ca5b5e39f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de2555964ca9fb1d198ea4de6f884dff052c0fef133c5c09f9ab1d6d55a05ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f42a45739373865834610c6c3622a4a856339ca491713fc9ebd087f68cc934(
    value: typing.Optional[GoogleComputeResourcePolicyDiskConsistencyGroupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db4d8cce4484aedfc9b69823c9b1658b16aef170aa4779d79ce656ffabba8c8(
    *,
    availability_domain_count: typing.Optional[jsii.Number] = None,
    collocation: typing.Optional[builtins.str] = None,
    gpu_topology: typing.Optional[builtins.str] = None,
    max_distance: typing.Optional[jsii.Number] = None,
    tpu_topology: typing.Optional[builtins.str] = None,
    vm_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ec969bd7e647076410dd72153f57127c97603a7b093b74ef76bd5ec6b07be5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30014f8824776f264b0f6a70014076ac29b695c7c63033c9ae8a2ae933ff458(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7826747346de304bc3ae42099214a5921d6c2b18eae248254c83d8b36382724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eab7bd964597596766042a76ef5084266007bd8834a2c71b79b0e5ec89ff064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb63379ec54941ef9e215a84eabd0207de482b69b7beb904dd3688cb03ef5ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e46438a243f294fea33573a0ac428f12a59bb87a7d317f25de6c27306357151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351bc2512f8df46368583d8a5b5e54d18508ca8b0a8df8135ae60988a3f042da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32b08ab44340187757d332a0058fc30f91b0e9201ee229dc0a63992c3ef50f2(
    value: typing.Optional[GoogleComputeResourcePolicyGroupPlacementPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ab56e53516ada146be5d75c7ad154774bdff301f61a58d480dd364f185b653(
    *,
    time_zone: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    vm_start_schedule: typing.Optional[typing.Union[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    vm_stop_schedule: typing.Optional[typing.Union[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2ee775b1bd8c2ef23264a7aeeb4abb23105397c47716bd9a369fed59a9e887(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5d3beed73daddb51ce0c4cf661a6a5dabad1755e97c3e7bd467c942326d702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3386a15b9909ca4bd7072b09fcf05396e7e5bf5318bd28d24b8e64f2aaa437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bde2d214b86c2d19b30dbde38d10b1b1fb5ee3e20b5cdc355dafd8972d38fb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce56849faff5c365db0224d6d85c88355a5257456ebadc5fbc91c14c725b56d(
    value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2175abf81687158bad1e61026208b9534b2aaaaaa7fff185301c479f40bb37c9(
    *,
    schedule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d469528d4dd63e56294b90accc4b5829058241eb73d863f744e0379284f19a16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267efee1e097c437adf7311e7abecfedb70f808db71086e36b7f96131b238c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b57893c6f59422e4494f071b5b97c5d4c1b098c69c0b29a179ba89b2f097dd6(
    value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStartSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801a401e35f986818c01eaae6e307b58274dbd7e93258a2ec7f86ecdc53c1ca6(
    *,
    schedule: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d0d56e7c250376e14e3cf14ae6df6961f1fac91dc17d7d128a0e96130285c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4029f7b010dfec6dfc24f7a1826f75a5a63ed72f9d59385408574d57347819fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83a50c52afaaad35c7421b09b26a483749b7472c11aaaa1ba44084e9216ef1e(
    value: typing.Optional[GoogleComputeResourcePolicyInstanceSchedulePolicyVmStopSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe71fd20748caac7ba04e26502340eb3b69733c70e6d951dd72805193634af8(
    *,
    schedule: typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicySchedule, typing.Dict[builtins.str, typing.Any]],
    retention_policy: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    snapshot_properties: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dc0abda49d92a5cf5cf2ba1aac33fb4fae2a85ea1b3c0aea9a9b93eb756695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39397c4432e092f0f1dd96a2fb0cb28c502386a86e33e7ec1d703295806488f6(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a036fa3ffc0db402dd8dff1ba97d01a8f6fb887313da9c0cbbdbd1744a2fcddb(
    *,
    max_retention_days: jsii.Number,
    on_source_disk_delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63eb75707d0b8a95cc3de3e29e04916187b2ce2b1b929e6ee8f6446866efe555(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df61642271587c8eab4f3a6166fa9f6ed363eea84e96c49489d3a85d6f2d7b16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1582623857ff964d6af38ef5871b983ec4d1200fee3135d2e0dc8f2c5a8ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e839e0023332f574570ccfe298fd3080e5a151a16ed89ef64eeb4871001b07(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07361f893c01435aca4ab2ebd70e7d676efbc7d1f843e8177811cbdfd130660e(
    *,
    daily_schedule: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    hourly_schedule: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d8ccf1de1af88cdcd56e7eaab88dc5e19cf82e2884965590fbb84fd7f09a86(
    *,
    days_in_cycle: jsii.Number,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760089ff30699346acdbdb94fd850d6d780cf266ed71f07408b5867f119e1ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9ac641f58a04edd4df572ebd2a0ece73da14510615f43e16f245cd8c204521(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9006599c2a6fd6f7132edcf99046fb260f239d3a2cc2425a3dc6ac678bcccce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b130897f5e6f4dca325f0bf07f78bfc6fdf4b1eae80e8dda082701d66e0ed36e(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec953b9961a7545f4b814387a958d206f70f4cbc842e5cb4afb44dfb4355bc9a(
    *,
    hours_in_cycle: jsii.Number,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed6d84ce28c99649a82fb7837e297f571e7f79102cdb10c581dbc98af5cdff3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ec04ca78318de08f822c2462701b0a1f9db9476402cb2f2e04ab3dec59887f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab47d213009037d5bec2f4eb5922c96ccab1e7e546335565b70840614371970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a96b92ea8354095f4d2c0a84e4b09f75d050e495336db5fba0c534aa0b8a346(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleHourlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961940afb5297764836768000c7953488a097700b0165f609eaf772cc260e120(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd5ba24f30b73aaffa249cb1e166e38ed0b4e09403b3641ab922404458123d3(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d043619940693724a8c6d40863df70ddac029d6ea244d66f07949f5da37eaa(
    *,
    day_of_weeks: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1beef23655fd5bbb8eed8b15abecb57a5d11a7a200cdce0f78f45a197db3c987(
    *,
    day: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7330895ed4738754f37a097dcf3b67faa410b0009b771658858ca433f8924db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5463436b46768b77e85835a045aad764bf5c686306005bd430e207ed9d173d85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767b8b6e995291d8da4aeaf4d712e73dc35f7147bcbdcb3f6eecba1bb3385124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b668795617282eb89e1b45d1edd61734ab4f71adf512b6bc95f556b5f482d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84fe6e16ae43bb0b9af44f84e5440496c5c5dff6e1eb3105f44f55d288e5279(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b684cfe54acc69a152d08c149bb7c316c8def8712cdb38dc6ccc1ef4314f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef354fe68a878ae9f96b5139795ac4ff3e16fc8b7ff2836fe500a2df417d192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d639a23c3e15fc972579e8e5f239b44e4b2a6fef862c5ca9b1cada29b4cc01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27486c5a4dc186a64271a42035e11b56c6cbaedaeb6ec1143a33052c64d96f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4313f52883506ff15997bdb8c221848188d46733bc94f464e25840c6077f847(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa1d6f5ae4ad11798f82f749af36a14494ce7f894fd966b841d1c93d1f7e53d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bb4181fa9324061d133f4b0471f2c1eda40c9a91f3c3f0757ee75d16dc9b8d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklyScheduleDayOfWeeks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12adcbdd6f2147838e8ed87d84cc01243e9f242987f8f790ffeead1c87ad3fc9(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicyScheduleWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a51e60fada8d896a526bcc79eab3504bd5622b116ed471a779894f5bf2fc7f(
    *,
    chain_name: typing.Optional[builtins.str] = None,
    guest_flush: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482e5fdbe1378b8386806e92d1f8b26e4ec71eaf3a2f15cb56013377dc8a5df0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ea3ec9ca4c385f0ae2a394b738b5902360cd1dcc4dfb49174e63d1525c920a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca2b838dfbe315f885c752b9557fc8acc2af41787684ba1a3c53419f2321c5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a1ffbf69c484a029e9f791d2699bf9fd3821fddc514af0c560eb53e53633d2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42e09eba184c93c108a26db788ae0e6ac857afc1c46da58d509141a6f280fca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82d787815b14295271902f59d98348b6cf11d7a5c02a68d29a8aeaddd9ce084(
    value: typing.Optional[GoogleComputeResourcePolicySnapshotSchedulePolicySnapshotProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc52d7d2fe0ff385af7e3a90b2a976cf111f870587a7a3a709a78cd08b4a63e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273b2e3f8949a70dfbb26a008363a604253034e985bd0ed55710d8f33d7bb76b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31376eb67415ea8b758c40af140b9fe9c73b680aca369981dffe8695521dd5a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ba8b7fdc6435629cbc0cb7c5e1e42aa5abc972a17455cf0d65471243af5870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b67b1c7d3d67577cb377e75c7d5abf1ddfe97f6ed33c829a1a0011a03d998b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950bfc98d5d45955328bdf0b1f4f2cfb33f076cbd79a714fdddc23ad04c66c29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeResourcePolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41b119b41850e59796879b871fba2b761099070c635544de095f5ca09bc5bea(
    *,
    type: builtins.str,
    accelerator_topology: typing.Optional[builtins.str] = None,
    max_topology_distance: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c9c3e78a97a04cdc98c51b3c95fac152a7a3113255f83ec3c2f0fbeabc991c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60debe3e054fb6bb687f74e565d7910d12207f5bbc3c12209662e0c3f65b96c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc523ceee23a560645edd5030bdd494d78ae2bc56ff819bf12ec1228897db03b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e3bc2841c6cef6e05a360e0869dfd8bd75f569f36222d4b068c2e5515e3f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830b448bddcf20df4ded7093b11d1bb033020a50a7cca51c9783e26e3fe6f567(
    value: typing.Optional[GoogleComputeResourcePolicyWorkloadPolicy],
) -> None:
    """Type checking stubs"""
    pass

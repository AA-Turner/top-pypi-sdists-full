r'''
# `google_compute_region_instance_template`

Refer to the Terraform Registry for docs: [`google_compute_region_instance_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template).
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


class ComputeRegionInstanceTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template google_compute_region_instance_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
        machine_type: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union["ComputeRegionInstanceTemplateAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union["ComputeRegionInstanceTemplateConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_description: typing.Optional[builtins.str] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeRegionInstanceTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeRegionInstanceTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeRegionInstanceTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[typing.Union["ComputeRegionInstanceTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeRegionInstanceTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionInstanceTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template google_compute_region_instance_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk ComputeRegionInstanceTemplate#disk}
        :param machine_type: The machine type to create. To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#machine_type ComputeRegionInstanceTemplate#machine_type}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#advanced_machine_features ComputeRegionInstanceTemplate#advanced_machine_features}
        :param can_ip_forward: Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#can_ip_forward ComputeRegionInstanceTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_config ComputeRegionInstanceTemplate#confidential_instance_config}
        :param description: A brief description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#description ComputeRegionInstanceTemplate#description}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#guest_accelerator ComputeRegionInstanceTemplate#guest_accelerator}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#id ComputeRegionInstanceTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_description ComputeRegionInstanceTemplate#instance_description}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key_revocation_action_type ComputeRegionInstanceTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs to assign to instances created from this template,. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#labels ComputeRegionInstanceTemplate#labels}
        :param metadata: Metadata key/value pairs to make available from within instances created from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata ComputeRegionInstanceTemplate#metadata}
        :param metadata_startup_script: An alternative to using the startup-script metadata key, mostly to match the compute_instance resource. This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata_startup_script ComputeRegionInstanceTemplate#metadata_startup_script}
        :param min_cpu_platform: Specifies a minimum CPU platform. Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_cpu_platform ComputeRegionInstanceTemplate#min_cpu_platform}
        :param name: The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name ComputeRegionInstanceTemplate#name}
        :param name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name_prefix ComputeRegionInstanceTemplate#name_prefix}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_interface ComputeRegionInstanceTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_performance_config ComputeRegionInstanceTemplate#network_performance_config}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#project ComputeRegionInstanceTemplate#project}
        :param region: The region in which the instance template is located. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#region ComputeRegionInstanceTemplate#region}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#reservation_affinity ComputeRegionInstanceTemplate#reservation_affinity}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_manager_tags ComputeRegionInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_policies ComputeRegionInstanceTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scheduling ComputeRegionInstanceTemplate#scheduling}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#service_account ComputeRegionInstanceTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#shielded_instance_config ComputeRegionInstanceTemplate#shielded_instance_config}
        :param tags: Tags to attach to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#tags ComputeRegionInstanceTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#timeouts ComputeRegionInstanceTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7206550734101103d8e516e6465ed5ebe178aca992c3a28580a63b6980299c94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionInstanceTemplateConfig(
            disk=disk,
            machine_type=machine_type,
            advanced_machine_features=advanced_machine_features,
            can_ip_forward=can_ip_forward,
            confidential_instance_config=confidential_instance_config,
            description=description,
            guest_accelerator=guest_accelerator,
            id=id,
            instance_description=instance_description,
            key_revocation_action_type=key_revocation_action_type,
            labels=labels,
            metadata=metadata,
            metadata_startup_script=metadata_startup_script,
            min_cpu_platform=min_cpu_platform,
            name=name,
            name_prefix=name_prefix,
            network_interface=network_interface,
            network_performance_config=network_performance_config,
            project=project,
            region=region,
            reservation_affinity=reservation_affinity,
            resource_manager_tags=resource_manager_tags,
            resource_policies=resource_policies,
            scheduling=scheduling,
            service_account=service_account,
            shielded_instance_config=shielded_instance_config,
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
        '''Generates CDKTF code for importing a ComputeRegionInstanceTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionInstanceTemplate to import.
        :param import_from_id: The id of the existing ComputeRegionInstanceTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionInstanceTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab28cfbfdc89b04e594a2d3a44048a8e8db1deb9da74d07eca219ed46bc69fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedMachineFeatures")
    def put_advanced_machine_features(
        self,
        *,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_uefi_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_monitoring_unit: typing.Optional[builtins.str] = None,
        threads_per_core: typing.Optional[jsii.Number] = None,
        turbo_mode: typing.Optional[builtins.str] = None,
        visible_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_nested_virtualization ComputeRegionInstanceTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_uefi_networking ComputeRegionInstanceTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#performance_monitoring_unit ComputeRegionInstanceTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#threads_per_core ComputeRegionInstanceTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#turbo_mode ComputeRegionInstanceTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#visible_core_count ComputeRegionInstanceTemplate#visible_core_count}
        '''
        value = ComputeRegionInstanceTemplateAdvancedMachineFeatures(
            enable_nested_virtualization=enable_nested_virtualization,
            enable_uefi_networking=enable_uefi_networking,
            performance_monitoring_unit=performance_monitoring_unit,
            threads_per_core=threads_per_core,
            turbo_mode=turbo_mode,
            visible_core_count=visible_core_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putConfidentialInstanceConfig")
    def put_confidential_instance_config(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_type ComputeRegionInstanceTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_confidential_compute ComputeRegionInstanceTemplate#enable_confidential_compute}
        '''
        value = ComputeRegionInstanceTemplateConfidentialInstanceConfig(
            confidential_instance_type=confidential_instance_type,
            enable_confidential_compute=enable_confidential_compute,
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0a2e36c89107545c9064bcaa79e5dff93a7a613e2eed7a26c8395afeac9d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7292fee0a8bff6381def2143ae2e1647ff59905015fb41d209ab148e91c2baf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerator", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cda5125c9d96b2fb655dcd9c958171a2b68c6ba81eb90abe9e4b388fde80e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#total_egress_bandwidth_tier ComputeRegionInstanceTemplate#total_egress_bandwidth_tier}
        '''
        value = ComputeRegionInstanceTemplateNetworkPerformanceConfig(
            total_egress_bandwidth_tier=total_egress_bandwidth_tier
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkPerformanceConfig", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#specific_reservation ComputeRegionInstanceTemplate#specific_reservation}
        '''
        value = ComputeRegionInstanceTemplateReservationAffinity(
            type=type, specific_reservation=specific_reservation
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putScheduling")
    def put_scheduling(
        self,
        *,
        automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_domain: typing.Optional[jsii.Number] = None,
        instance_termination_action: typing.Optional[builtins.str] = None,
        local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeRegionInstanceTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user). This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#automatic_restart ComputeRegionInstanceTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#availability_domain ComputeRegionInstanceTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_termination_action ComputeRegionInstanceTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#local_ssd_recovery_timeout ComputeRegionInstanceTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#max_run_duration ComputeRegionInstanceTemplate#max_run_duration}
        :param min_node_cpus: Minimum number of cpus for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_node_cpus ComputeRegionInstanceTemplate#min_node_cpus}
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#node_affinities ComputeRegionInstanceTemplate#node_affinities}
        :param on_host_maintenance: Defines the maintenance behavior for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_host_maintenance ComputeRegionInstanceTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_instance_stop_action ComputeRegionInstanceTemplate#on_instance_stop_action}
        :param preemptible: Allows instance to be preempted. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#preemptible ComputeRegionInstanceTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioning_model ComputeRegionInstanceTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#termination_time ComputeRegionInstanceTemplate#termination_time}
        '''
        value = ComputeRegionInstanceTemplateScheduling(
            automatic_restart=automatic_restart,
            availability_domain=availability_domain,
            instance_termination_action=instance_termination_action,
            local_ssd_recovery_timeout=local_ssd_recovery_timeout,
            max_run_duration=max_run_duration,
            min_node_cpus=min_node_cpus,
            node_affinities=node_affinities,
            on_host_maintenance=on_host_maintenance,
            on_instance_stop_action=on_instance_stop_action,
            preemptible=preemptible,
            provisioning_model=provisioning_model,
            termination_time=termination_time,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduling", [value]))

    @jsii.member(jsii_name="putServiceAccount")
    def put_service_account(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported. To allow full access to all Cloud APIs, use the cloud-platform scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scopes ComputeRegionInstanceTemplate#scopes}
        :param email: The service account e-mail address. If not given, the default Google Compute Engine service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#email ComputeRegionInstanceTemplate#email}
        '''
        value = ComputeRegionInstanceTemplateServiceAccount(scopes=scopes, email=email)

        return typing.cast(None, jsii.invoke(self, "putServiceAccount", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results depending on whether they match or not. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_integrity_monitoring ComputeRegionInstanceTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Verify the digital signature of all boot components, and halt the boot process if signature verification fails. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_secure_boot ComputeRegionInstanceTemplate#enable_secure_boot}
        :param enable_vtpm: Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_vtpm ComputeRegionInstanceTemplate#enable_vtpm}
        '''
        value = ComputeRegionInstanceTemplateShieldedInstanceConfig(
            enable_integrity_monitoring=enable_integrity_monitoring,
            enable_secure_boot=enable_secure_boot,
            enable_vtpm=enable_vtpm,
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#create ComputeRegionInstanceTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#delete ComputeRegionInstanceTemplate#delete}.
        '''
        value = ComputeRegionInstanceTemplateTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedMachineFeatures")
    def reset_advanced_machine_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedMachineFeatures", []))

    @jsii.member(jsii_name="resetCanIpForward")
    def reset_can_ip_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanIpForward", []))

    @jsii.member(jsii_name="resetConfidentialInstanceConfig")
    def reset_confidential_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGuestAccelerator")
    def reset_guest_accelerator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestAccelerator", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceDescription")
    def reset_instance_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceDescription", []))

    @jsii.member(jsii_name="resetKeyRevocationActionType")
    def reset_key_revocation_action_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRevocationActionType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataStartupScript")
    def reset_metadata_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataStartupScript", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNamePrefix")
    def reset_name_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamePrefix", []))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetNetworkPerformanceConfig")
    def reset_network_performance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPerformanceConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @jsii.member(jsii_name="resetResourcePolicies")
    def reset_resource_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePolicies", []))

    @jsii.member(jsii_name="resetScheduling")
    def reset_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduling", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

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
    @jsii.member(jsii_name="advancedMachineFeatures")
    def advanced_machine_features(
        self,
    ) -> "ComputeRegionInstanceTemplateAdvancedMachineFeaturesOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateAdvancedMachineFeaturesOutputReference", jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> "ComputeRegionInstanceTemplateConfidentialInstanceConfigOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateConfidentialInstanceConfigOutputReference", jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> "ComputeRegionInstanceTemplateDiskList":
        return typing.cast("ComputeRegionInstanceTemplateDiskList", jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerator")
    def guest_accelerator(self) -> "ComputeRegionInstanceTemplateGuestAcceleratorList":
        return typing.cast("ComputeRegionInstanceTemplateGuestAcceleratorList", jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="metadataFingerprint")
    def metadata_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> "ComputeRegionInstanceTemplateNetworkInterfaceList":
        return typing.cast("ComputeRegionInstanceTemplateNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> "ComputeRegionInstanceTemplateNetworkPerformanceConfigOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateNetworkPerformanceConfigOutputReference", jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="numericId")
    def numeric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "numericId"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "ComputeRegionInstanceTemplateReservationAffinityOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "ComputeRegionInstanceTemplateSchedulingOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(
        self,
    ) -> "ComputeRegionInstanceTemplateServiceAccountOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "ComputeRegionInstanceTemplateShieldedInstanceConfigOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="tagsFingerprint")
    def tags_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagsFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionInstanceTemplateTimeoutsOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateAdvancedMachineFeatures"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateAdvancedMachineFeatures"], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="canIpForwardInput")
    def can_ip_forward_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canIpForwardInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfigInput")
    def confidential_instance_config_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateConfidentialInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateConfidentialInstanceConfig"], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateDisk"]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorInput")
    def guest_accelerator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateGuestAccelerator"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateGuestAccelerator"]]], jsii.get(self, "guestAcceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceDescriptionInput")
    def instance_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRevocationActionTypeInput")
    def key_revocation_action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRevocationActionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataStartupScriptInput")
    def metadata_startup_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataStartupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatformInput")
    def min_cpu_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minCpuPlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namePrefixInput")
    def name_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfigInput")
    def network_performance_config_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateNetworkPerformanceConfig"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateNetworkPerformanceConfig"], jsii.get(self, "networkPerformanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateReservationAffinity"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoliciesInput")
    def resource_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcePoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateScheduling"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateServiceAccount"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateServiceAccount"], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionInstanceTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionInstanceTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="canIpForward")
    def can_ip_forward(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canIpForward"))

    @can_ip_forward.setter
    def can_ip_forward(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c025e05e24fd7f3f5c11d3c66985cfa7058b2b062288ba016197452d26b9c4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canIpForward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274c8c78d9581ef50a8cc43016cbd8078dd8973ae153c137d71dccdc6c505751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a20458b7908ce626f63fe02690b4471c68a40795acf1f5dc81ea2a9cefb954f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceDescription")
    def instance_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceDescription"))

    @instance_description.setter
    def instance_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0402d723ac239114af8c6b3fcfd39969c3473784fe1f27765e954a638ada02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyRevocationActionType")
    def key_revocation_action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRevocationActionType"))

    @key_revocation_action_type.setter
    def key_revocation_action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2e8087c21750e47b83e79ea5a95df67ada5d2bcdf544d6a9564f481b40f87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRevocationActionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8955ba13134c46beb2f3674c7669e8d6fa665e76e5db4745562639b1e4d4cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef91bcfc176e0375b3243949a37a956941cc010dcd73e55102d7ee26df169f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9b6102f274dde904da779bf583204cf4ab9d7b6b0fa67b989a1079e5f5f655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataStartupScript")
    def metadata_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataStartupScript"))

    @metadata_startup_script.setter
    def metadata_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a921830f7f1846fd1ead92b0f4b2372bf432e10084ecb1648a8bd7e26ecb91ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282a3ad51303ee003b4e8a4cec5733478473d4f8a05a165a80fe5fd3df020042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4032ece98a12856b57c7a74349bd4683b8a05311752d0551cd718b483174e64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e82ab46021708a0f04dcd99d314a478b7ce4eba8c5db880fbdd267151de9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc37859b2cce5078cdf0ac44ed67e590468b0392514ffc8198caa6aa5bdb0406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6051616b57d625e3dfe8cbafba35df0c4e2bfd2f8d6a3ad891ae21330812727e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5226c52212a903c22d3e7b5ede21c4de91f8a4ae34fc7e30f1bf92a941f68c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9f76c32e9253fedf8b8e6ce43fd710e4192780ab854205c108aa0ad661eded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e8554908e7cfe1506febb4e8ce457c93bbdfdabd96c4d7f6fbe973338d0105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateAdvancedMachineFeatures",
    jsii_struct_bases=[],
    name_mapping={
        "enable_nested_virtualization": "enableNestedVirtualization",
        "enable_uefi_networking": "enableUefiNetworking",
        "performance_monitoring_unit": "performanceMonitoringUnit",
        "threads_per_core": "threadsPerCore",
        "turbo_mode": "turboMode",
        "visible_core_count": "visibleCoreCount",
    },
)
class ComputeRegionInstanceTemplateAdvancedMachineFeatures:
    def __init__(
        self,
        *,
        enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_uefi_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_monitoring_unit: typing.Optional[builtins.str] = None,
        threads_per_core: typing.Optional[jsii.Number] = None,
        turbo_mode: typing.Optional[builtins.str] = None,
        visible_core_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_nested_virtualization ComputeRegionInstanceTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_uefi_networking ComputeRegionInstanceTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#performance_monitoring_unit ComputeRegionInstanceTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#threads_per_core ComputeRegionInstanceTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#turbo_mode ComputeRegionInstanceTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#visible_core_count ComputeRegionInstanceTemplate#visible_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205721e59d09ac1746ec1c8a9bd6ec504440f423adf843657a73de87f22374b0)
            check_type(argname="argument enable_nested_virtualization", value=enable_nested_virtualization, expected_type=type_hints["enable_nested_virtualization"])
            check_type(argname="argument enable_uefi_networking", value=enable_uefi_networking, expected_type=type_hints["enable_uefi_networking"])
            check_type(argname="argument performance_monitoring_unit", value=performance_monitoring_unit, expected_type=type_hints["performance_monitoring_unit"])
            check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
            check_type(argname="argument turbo_mode", value=turbo_mode, expected_type=type_hints["turbo_mode"])
            check_type(argname="argument visible_core_count", value=visible_core_count, expected_type=type_hints["visible_core_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_nested_virtualization is not None:
            self._values["enable_nested_virtualization"] = enable_nested_virtualization
        if enable_uefi_networking is not None:
            self._values["enable_uefi_networking"] = enable_uefi_networking
        if performance_monitoring_unit is not None:
            self._values["performance_monitoring_unit"] = performance_monitoring_unit
        if threads_per_core is not None:
            self._values["threads_per_core"] = threads_per_core
        if turbo_mode is not None:
            self._values["turbo_mode"] = turbo_mode
        if visible_core_count is not None:
            self._values["visible_core_count"] = visible_core_count

    @builtins.property
    def enable_nested_virtualization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable nested virtualization or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_nested_virtualization ComputeRegionInstanceTemplate#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_uefi_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable UEFI networking or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_uefi_networking ComputeRegionInstanceTemplate#enable_uefi_networking}
        '''
        result = self._values.get("enable_uefi_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_monitoring_unit(self) -> typing.Optional[builtins.str]:
        '''The PMU is a hardware component within the CPU core that monitors how the processor runs code.

        Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#performance_monitoring_unit ComputeRegionInstanceTemplate#performance_monitoring_unit}
        '''
        result = self._values.get("performance_monitoring_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#threads_per_core ComputeRegionInstanceTemplate#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def turbo_mode(self) -> typing.Optional[builtins.str]:
        '''Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#turbo_mode ComputeRegionInstanceTemplate#turbo_mode}
        '''
        result = self._values.get("turbo_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visible_core_count(self) -> typing.Optional[jsii.Number]:
        '''The number of physical cores to expose to an instance.

        Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#visible_core_count ComputeRegionInstanceTemplate#visible_core_count}
        '''
        result = self._values.get("visible_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80bb71951439a863305f9414f02ce3fc921976d35034271dfde3bf57e655401b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableNestedVirtualization")
    def reset_enable_nested_virtualization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNestedVirtualization", []))

    @jsii.member(jsii_name="resetEnableUefiNetworking")
    def reset_enable_uefi_networking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUefiNetworking", []))

    @jsii.member(jsii_name="resetPerformanceMonitoringUnit")
    def reset_performance_monitoring_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceMonitoringUnit", []))

    @jsii.member(jsii_name="resetThreadsPerCore")
    def reset_threads_per_core(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreadsPerCore", []))

    @jsii.member(jsii_name="resetTurboMode")
    def reset_turbo_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTurboMode", []))

    @jsii.member(jsii_name="resetVisibleCoreCount")
    def reset_visible_core_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibleCoreCount", []))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualizationInput")
    def enable_nested_virtualization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNestedVirtualizationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUefiNetworkingInput")
    def enable_uefi_networking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUefiNetworkingInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnitInput")
    def performance_monitoring_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceMonitoringUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="threadsPerCoreInput")
    def threads_per_core_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "threadsPerCoreInput"))

    @builtins.property
    @jsii.member(jsii_name="turboModeInput")
    def turbo_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "turboModeInput"))

    @builtins.property
    @jsii.member(jsii_name="visibleCoreCountInput")
    def visible_core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "visibleCoreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNestedVirtualization")
    def enable_nested_virtualization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNestedVirtualization"))

    @enable_nested_virtualization.setter
    def enable_nested_virtualization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32b7c8dcc3dcd8a33b16e9049ade50af6ab092aeb56134ab8d1ad4ddf18d421e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNestedVirtualization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUefiNetworking")
    def enable_uefi_networking(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUefiNetworking"))

    @enable_uefi_networking.setter
    def enable_uefi_networking(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a719b9bff3f93c925fba3b6da80553a72059bbb62dc0a3762b7ef08b19d744a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUefiNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnit")
    def performance_monitoring_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceMonitoringUnit"))

    @performance_monitoring_unit.setter
    def performance_monitoring_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43663047cae15fca86ea3a404cc60dc97c2bf1c9a82c33d9d8249c424f1e07b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMonitoringUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dfb9ff2b98ed34f1941ff322b2800ac31a9d52e628225d1f69cbf7ed328f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="turboMode")
    def turbo_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "turboMode"))

    @turbo_mode.setter
    def turbo_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58bde152e7f8c015fd88f473b2abd34db891dad6044a71bb64b4eadb2104114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "turboMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibleCoreCount")
    def visible_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "visibleCoreCount"))

    @visible_core_count.setter
    def visible_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3404983d8d08e3e7116e393a6ff907fad43d2a6a106de4b687ceb49ab64bd60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibleCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242e38580e88205402d93d9bd9bcda9659d870f71259181701daaa265fac992a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidential_instance_type": "confidentialInstanceType",
        "enable_confidential_compute": "enableConfidentialCompute",
    },
)
class ComputeRegionInstanceTemplateConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_type ComputeRegionInstanceTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_confidential_compute ComputeRegionInstanceTemplate#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504f8a052222427e535978b529aadbfc7db7f3ae8b0d83f271651dd1ff481acc)
            check_type(argname="argument confidential_instance_type", value=confidential_instance_type, expected_type=type_hints["confidential_instance_type"])
            check_type(argname="argument enable_confidential_compute", value=enable_confidential_compute, expected_type=type_hints["enable_confidential_compute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confidential_instance_type is not None:
            self._values["confidential_instance_type"] = confidential_instance_type
        if enable_confidential_compute is not None:
            self._values["enable_confidential_compute"] = enable_confidential_compute

    @builtins.property
    def confidential_instance_type(self) -> typing.Optional[builtins.str]:
        '''The confidential computing technology the instance uses.

        SEV is an AMD feature. TDX is an Intel feature. One of the following
        values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform =
        "AMD Milan" is currently required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_type ComputeRegionInstanceTemplate#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_confidential_compute ComputeRegionInstanceTemplate#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc1c4517771a5e3c86d1d07e5f4a6bb515c173af06a5b924f0c81d0e12566e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConfidentialInstanceType")
    def reset_confidential_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceType", []))

    @jsii.member(jsii_name="resetEnableConfidentialCompute")
    def reset_enable_confidential_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialCompute", []))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceTypeInput")
    def confidential_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "confidentialInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialComputeInput")
    def enable_confidential_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceType")
    def confidential_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "confidentialInstanceType"))

    @confidential_instance_type.setter
    def confidential_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430c809a27cf6f1de21c378ad10de053da29f11664f159af93ae84a357fb8b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confidentialInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialCompute")
    def enable_confidential_compute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConfidentialCompute"))

    @enable_confidential_compute.setter
    def enable_confidential_compute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e9133a02b3bdc262cc5f70ef7e197ba6e51af475a7f5e80337cc9d7a0f9810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a0f4e976eb2406dcb33956abf6c120bf9bc77512b926c493a542e92c3f6639)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "disk": "disk",
        "machine_type": "machineType",
        "advanced_machine_features": "advancedMachineFeatures",
        "can_ip_forward": "canIpForward",
        "confidential_instance_config": "confidentialInstanceConfig",
        "description": "description",
        "guest_accelerator": "guestAccelerator",
        "id": "id",
        "instance_description": "instanceDescription",
        "key_revocation_action_type": "keyRevocationActionType",
        "labels": "labels",
        "metadata": "metadata",
        "metadata_startup_script": "metadataStartupScript",
        "min_cpu_platform": "minCpuPlatform",
        "name": "name",
        "name_prefix": "namePrefix",
        "network_interface": "networkInterface",
        "network_performance_config": "networkPerformanceConfig",
        "project": "project",
        "region": "region",
        "reservation_affinity": "reservationAffinity",
        "resource_manager_tags": "resourceManagerTags",
        "resource_policies": "resourcePolicies",
        "scheduling": "scheduling",
        "service_account": "serviceAccount",
        "shielded_instance_config": "shieldedInstanceConfig",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class ComputeRegionInstanceTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
        machine_type: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union[ComputeRegionInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_description: typing.Optional[builtins.str] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeRegionInstanceTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeRegionInstanceTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeRegionInstanceTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[typing.Union["ComputeRegionInstanceTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeRegionInstanceTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionInstanceTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk ComputeRegionInstanceTemplate#disk}
        :param machine_type: The machine type to create. To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#machine_type ComputeRegionInstanceTemplate#machine_type}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#advanced_machine_features ComputeRegionInstanceTemplate#advanced_machine_features}
        :param can_ip_forward: Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#can_ip_forward ComputeRegionInstanceTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_config ComputeRegionInstanceTemplate#confidential_instance_config}
        :param description: A brief description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#description ComputeRegionInstanceTemplate#description}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#guest_accelerator ComputeRegionInstanceTemplate#guest_accelerator}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#id ComputeRegionInstanceTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_description ComputeRegionInstanceTemplate#instance_description}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key_revocation_action_type ComputeRegionInstanceTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs to assign to instances created from this template,. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#labels ComputeRegionInstanceTemplate#labels}
        :param metadata: Metadata key/value pairs to make available from within instances created from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata ComputeRegionInstanceTemplate#metadata}
        :param metadata_startup_script: An alternative to using the startup-script metadata key, mostly to match the compute_instance resource. This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata_startup_script ComputeRegionInstanceTemplate#metadata_startup_script}
        :param min_cpu_platform: Specifies a minimum CPU platform. Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_cpu_platform ComputeRegionInstanceTemplate#min_cpu_platform}
        :param name: The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name ComputeRegionInstanceTemplate#name}
        :param name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name_prefix ComputeRegionInstanceTemplate#name_prefix}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_interface ComputeRegionInstanceTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_performance_config ComputeRegionInstanceTemplate#network_performance_config}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#project ComputeRegionInstanceTemplate#project}
        :param region: The region in which the instance template is located. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#region ComputeRegionInstanceTemplate#region}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#reservation_affinity ComputeRegionInstanceTemplate#reservation_affinity}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_manager_tags ComputeRegionInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_policies ComputeRegionInstanceTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scheduling ComputeRegionInstanceTemplate#scheduling}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#service_account ComputeRegionInstanceTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#shielded_instance_config ComputeRegionInstanceTemplate#shielded_instance_config}
        :param tags: Tags to attach to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#tags ComputeRegionInstanceTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#timeouts ComputeRegionInstanceTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = ComputeRegionInstanceTemplateAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = ComputeRegionInstanceTemplateConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(network_performance_config, dict):
            network_performance_config = ComputeRegionInstanceTemplateNetworkPerformanceConfig(**network_performance_config)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = ComputeRegionInstanceTemplateReservationAffinity(**reservation_affinity)
        if isinstance(scheduling, dict):
            scheduling = ComputeRegionInstanceTemplateScheduling(**scheduling)
        if isinstance(service_account, dict):
            service_account = ComputeRegionInstanceTemplateServiceAccount(**service_account)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = ComputeRegionInstanceTemplateShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionInstanceTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c14404ed8faaaae7cd844af0b3cd5e863c74fd64a3830b43b202235f35a32b6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument can_ip_forward", value=can_ip_forward, expected_type=type_hints["can_ip_forward"])
            check_type(argname="argument confidential_instance_config", value=confidential_instance_config, expected_type=type_hints["confidential_instance_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument guest_accelerator", value=guest_accelerator, expected_type=type_hints["guest_accelerator"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_description", value=instance_description, expected_type=type_hints["instance_description"])
            check_type(argname="argument key_revocation_action_type", value=key_revocation_action_type, expected_type=type_hints["key_revocation_action_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_startup_script", value=metadata_startup_script, expected_type=type_hints["metadata_startup_script"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument network_performance_config", value=network_performance_config, expected_type=type_hints["network_performance_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
            check_type(argname="argument resource_policies", value=resource_policies, expected_type=type_hints["resource_policies"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk": disk,
            "machine_type": machine_type,
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
        if advanced_machine_features is not None:
            self._values["advanced_machine_features"] = advanced_machine_features
        if can_ip_forward is not None:
            self._values["can_ip_forward"] = can_ip_forward
        if confidential_instance_config is not None:
            self._values["confidential_instance_config"] = confidential_instance_config
        if description is not None:
            self._values["description"] = description
        if guest_accelerator is not None:
            self._values["guest_accelerator"] = guest_accelerator
        if id is not None:
            self._values["id"] = id
        if instance_description is not None:
            self._values["instance_description"] = instance_description
        if key_revocation_action_type is not None:
            self._values["key_revocation_action_type"] = key_revocation_action_type
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_startup_script is not None:
            self._values["metadata_startup_script"] = metadata_startup_script
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if name is not None:
            self._values["name"] = name
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if network_performance_config is not None:
            self._values["network_performance_config"] = network_performance_config
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags
        if resource_policies is not None:
            self._values["resource_policies"] = resource_policies
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if service_account is not None:
            self._values["service_account"] = service_account
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
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
    def disk(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateDisk"]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk ComputeRegionInstanceTemplate#disk}
        '''
        result = self._values.get("disk")
        assert result is not None, "Required property 'disk' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateDisk"]], result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The machine type to create.

        To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#machine_type ComputeRegionInstanceTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#advanced_machine_features ComputeRegionInstanceTemplate#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures], result)

    @builtins.property
    def can_ip_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#can_ip_forward ComputeRegionInstanceTemplate#can_ip_forward}
        '''
        result = self._values.get("can_ip_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#confidential_instance_config ComputeRegionInstanceTemplate#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#description ComputeRegionInstanceTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#guest_accelerator ComputeRegionInstanceTemplate#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateGuestAccelerator"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#id ComputeRegionInstanceTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_description(self) -> typing.Optional[builtins.str]:
        '''A description of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_description ComputeRegionInstanceTemplate#instance_description}
        '''
        result = self._values.get("instance_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_revocation_action_type(self) -> typing.Optional[builtins.str]:
        '''Action to be taken when a customer's encryption key is revoked.

        Supports "STOP" and "NONE", with "NONE" being the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key_revocation_action_type ComputeRegionInstanceTemplate#key_revocation_action_type}
        '''
        result = self._values.get("key_revocation_action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to instances created from this template,.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#labels ComputeRegionInstanceTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata key/value pairs to make available from within instances created from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata ComputeRegionInstanceTemplate#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_startup_script(self) -> typing.Optional[builtins.str]:
        '''An alternative to using the startup-script metadata key, mostly to match the compute_instance resource.

        This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#metadata_startup_script ComputeRegionInstanceTemplate#metadata_startup_script}
        '''
        result = self._values.get("metadata_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Specifies a minimum CPU platform.

        Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_cpu_platform ComputeRegionInstanceTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name ComputeRegionInstanceTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Creates a unique name beginning with the specified prefix. Conflicts with name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#name_prefix ComputeRegionInstanceTemplate#name_prefix}
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_interface ComputeRegionInstanceTemplate#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterface"]]], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_performance_config ComputeRegionInstanceTemplate#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateNetworkPerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#project ComputeRegionInstanceTemplate#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region in which the instance template is located. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#region ComputeRegionInstanceTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#reservation_affinity ComputeRegionInstanceTemplate#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateReservationAffinity"], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_manager_tags ComputeRegionInstanceTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_policies ComputeRegionInstanceTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["ComputeRegionInstanceTemplateScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scheduling ComputeRegionInstanceTemplate#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateScheduling"], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#service_account ComputeRegionInstanceTemplate#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateServiceAccount"], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#shielded_instance_config ComputeRegionInstanceTemplate#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to attach to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#tags ComputeRegionInstanceTemplate#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionInstanceTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#timeouts ComputeRegionInstanceTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDisk",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "auto_delete": "autoDelete",
        "boot": "boot",
        "device_name": "deviceName",
        "disk_encryption_key": "diskEncryptionKey",
        "disk_name": "diskName",
        "disk_size_gb": "diskSizeGb",
        "disk_type": "diskType",
        "guest_os_features": "guestOsFeatures",
        "interface": "interface",
        "labels": "labels",
        "mode": "mode",
        "provisioned_iops": "provisionedIops",
        "provisioned_throughput": "provisionedThroughput",
        "resource_manager_tags": "resourceManagerTags",
        "resource_policies": "resourcePolicies",
        "source": "source",
        "source_image": "sourceImage",
        "source_image_encryption_key": "sourceImageEncryptionKey",
        "source_snapshot": "sourceSnapshot",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "type": "type",
    },
)
class ComputeRegionInstanceTemplateDisk:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_name: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeRegionInstanceTemplateDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_name: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        disk_type: typing.Optional[builtins.str] = None,
        guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        interface: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        mode: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        source_image: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the image. Allowed values are ARM64 or X86_64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#architecture ComputeRegionInstanceTemplate#architecture}
        :param auto_delete: Whether or not the disk should be auto-deleted. This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#auto_delete ComputeRegionInstanceTemplate#auto_delete}
        :param boot: Indicates that this is a boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#boot ComputeRegionInstanceTemplate#boot}
        :param device_name: A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance. If not specified, the server chooses a default device name to apply to this disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#device_name ComputeRegionInstanceTemplate#device_name}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_encryption_key ComputeRegionInstanceTemplate#disk_encryption_key}
        :param disk_name: Name of the disk. When not provided, this defaults to the name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_name ComputeRegionInstanceTemplate#disk_name}
        :param disk_size_gb: The size of the image in gigabytes. If not specified, it will inherit the size of its base image. For SCRATCH disks, the size must be one of 375 or 3000 GB, with a default of 375 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_size_gb ComputeRegionInstanceTemplate#disk_size_gb}
        :param disk_type: The Google Compute Engine disk type. Such as "pd-ssd", "local-ssd", "pd-balanced" or "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_type ComputeRegionInstanceTemplate#disk_type}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#guest_os_features ComputeRegionInstanceTemplate#guest_os_features}
        :param interface: Specifies the disk interface to use for attaching this disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#interface ComputeRegionInstanceTemplate#interface}
        :param labels: A set of key/value label pairs to assign to disks,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#labels ComputeRegionInstanceTemplate#labels}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If you are attaching or creating a boot disk, this must read-write mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#mode ComputeRegionInstanceTemplate#mode}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. For more details, see the `Extreme persistent disk documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_ or the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_ depending on the selected disk_type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioned_iops ComputeRegionInstanceTemplate#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk, in MB/s. This sets the amount of data that can be read or written from the disk per second. Values must greater than or equal to 1. For more details, see the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioned_throughput ComputeRegionInstanceTemplate#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_manager_tags ComputeRegionInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list (short name or id) of resource policies to attach to this disk. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_policies ComputeRegionInstanceTemplate#resource_policies}
        :param source: The name (not self_link) of the disk (such as those managed by google_compute_disk) to attach. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source ComputeRegionInstanceTemplate#source}
        :param source_image: The image from which to initialize this disk. This can be one of: the image's self_link, projects/{project}/global/images/{image}, projects/{project}/global/images/family/{family}, global/images/{image}, global/images/family/{family}, family/{family}, {project}/{family}, {project}/{image}, {family}, or {image}. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_image ComputeRegionInstanceTemplate#source_image}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_image_encryption_key ComputeRegionInstanceTemplate#source_image_encryption_key}
        :param source_snapshot: The source snapshot to create this disk. When creating a new instance, one of initializeParams.sourceSnapshot, initializeParams.sourceImage, or disks.source is required except for local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_snapshot ComputeRegionInstanceTemplate#source_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_snapshot_encryption_key ComputeRegionInstanceTemplate#source_snapshot_encryption_key}
        :param type: The type of Google Compute Engine disk, can be either "SCRATCH" or "PERSISTENT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        '''
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ComputeRegionInstanceTemplateDiskDiskEncryptionKey(**disk_encryption_key)
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df580be0920b4c6eaa713627e5c2b5ace2d0a9b2e71672df03f1be10fed9aecd)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_delete", value=auto_delete, expected_type=type_hints["auto_delete"])
            check_type(argname="argument boot", value=boot, expected_type=type_hints["boot"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument guest_os_features", value=guest_os_features, expected_type=type_hints["guest_os_features"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument provisioned_iops", value=provisioned_iops, expected_type=type_hints["provisioned_iops"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
            check_type(argname="argument resource_policies", value=resource_policies, expected_type=type_hints["resource_policies"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_image", value=source_image, expected_type=type_hints["source_image"])
            check_type(argname="argument source_image_encryption_key", value=source_image_encryption_key, expected_type=type_hints["source_image_encryption_key"])
            check_type(argname="argument source_snapshot", value=source_snapshot, expected_type=type_hints["source_snapshot"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_delete is not None:
            self._values["auto_delete"] = auto_delete
        if boot is not None:
            self._values["boot"] = boot
        if device_name is not None:
            self._values["device_name"] = device_name
        if disk_encryption_key is not None:
            self._values["disk_encryption_key"] = disk_encryption_key
        if disk_name is not None:
            self._values["disk_name"] = disk_name
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if disk_type is not None:
            self._values["disk_type"] = disk_type
        if guest_os_features is not None:
            self._values["guest_os_features"] = guest_os_features
        if interface is not None:
            self._values["interface"] = interface
        if labels is not None:
            self._values["labels"] = labels
        if mode is not None:
            self._values["mode"] = mode
        if provisioned_iops is not None:
            self._values["provisioned_iops"] = provisioned_iops
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags
        if resource_policies is not None:
            self._values["resource_policies"] = resource_policies
        if source is not None:
            self._values["source"] = source
        if source_image is not None:
            self._values["source_image"] = source_image
        if source_image_encryption_key is not None:
            self._values["source_image_encryption_key"] = source_image_encryption_key
        if source_snapshot is not None:
            self._values["source_snapshot"] = source_snapshot
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The architecture of the image. Allowed values are ARM64 or X86_64.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#architecture ComputeRegionInstanceTemplate#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the disk should be auto-deleted. This defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#auto_delete ComputeRegionInstanceTemplate#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that this is a boot disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#boot ComputeRegionInstanceTemplate#boot}
        '''
        result = self._values.get("boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance.

        If not specified, the server chooses a default device name to apply to this disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#device_name ComputeRegionInstanceTemplate#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateDiskDiskEncryptionKey"]:
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_encryption_key ComputeRegionInstanceTemplate#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateDiskDiskEncryptionKey"], result)

    @builtins.property
    def disk_name(self) -> typing.Optional[builtins.str]:
        '''Name of the disk. When not provided, this defaults to the name of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_name ComputeRegionInstanceTemplate#disk_name}
        '''
        result = self._values.get("disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the image in gigabytes.

        If not specified, it will inherit the size of its base image. For SCRATCH disks, the size must be one of 375 or 3000 GB, with a default of 375 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_size_gb ComputeRegionInstanceTemplate#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The Google Compute Engine disk type. Such as "pd-ssd", "local-ssd", "pd-balanced" or "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#disk_type ComputeRegionInstanceTemplate#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_os_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of features to enable on the guest operating system. Applicable only for bootable images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#guest_os_features ComputeRegionInstanceTemplate#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''Specifies the disk interface to use for attaching this disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#interface ComputeRegionInstanceTemplate#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to disks,.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#labels ComputeRegionInstanceTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode in which to attach this disk, either READ_WRITE or READ_ONLY.

        If you are attaching or creating a boot disk, this must read-write mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#mode ComputeRegionInstanceTemplate#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS to provision for the disk.

        This sets the number of I/O operations per second that the disk can handle. For more details, see the `Extreme persistent disk documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_ or the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_ depending on the selected disk_type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioned_iops ComputeRegionInstanceTemplate#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much throughput to provision for the disk, in MB/s.

        This sets the amount of data that can be read or written from the disk per second. Values must greater than or equal to 1. For more details, see the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioned_throughput ComputeRegionInstanceTemplate#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_manager_tags ComputeRegionInstanceTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list (short name or id) of resource policies to attach to this disk.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#resource_policies ComputeRegionInstanceTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The name (not self_link) of the disk (such as those managed by google_compute_disk) to attach.

        ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source ComputeRegionInstanceTemplate#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image(self) -> typing.Optional[builtins.str]:
        '''The image from which to initialize this disk.

        This can be one of: the image's self_link, projects/{project}/global/images/{image}, projects/{project}/global/images/family/{family}, global/images/{image}, global/images/family/{family}, family/{family}, {project}/{family}, {project}/{image}, {family}, or {image}. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_image ComputeRegionInstanceTemplate#source_image}
        '''
        result = self._values.get("source_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_image_encryption_key ComputeRegionInstanceTemplate#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''The source snapshot to create this disk.

        When creating
        a new instance, one of initializeParams.sourceSnapshot,
        initializeParams.sourceImage, or disks.source is
        required except for local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_snapshot ComputeRegionInstanceTemplate#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#source_snapshot_encryption_key ComputeRegionInstanceTemplate#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of Google Compute Engine disk, can be either "SCRATCH" or "PERSISTENT".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
    },
)
class ComputeRegionInstanceTemplateDiskDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2eb76572b04906d75153a3d00a1ddd60a668c5e780d461da92ee9e82a0d292)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key that is stored in Google Cloud KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateDiskDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateDiskDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41f52281d18bf86fde32cd3405e12eda1f4e60f443923860246bcdc8a045bedf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a633adfb380fc4f832f724d79a8aed12692b4f96f8b795d3c99722ee145c08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367229d3cdc18f7e0a58ac4c73c76c228764b85b561cd94bb87f8ec3b569062c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbd2d737419e43ce667448c609e55f606e0e58e01ba2c916817774ee51ebef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7482e04853e2d596be8fe37305bdc6f2b38571006a94dd945106f4ab3d33941)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf2997cf4adba035354e27363f720a7a720498f500cccc5d1119fe1e16613fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b88f47401ea2402c2208601414aef5ee467d5d91bc4950e89092cd746c22fb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb35e261be95cfbc804b2629da94ef6ad1c7975fad040cb1d70a618cfccc0c03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee072bf4de9367934e8b3f8b86195b15c746ddaf38ddad10c6635a1faccee524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3eeef0971834583203d7b35537a50be97e3e0d12db75810af686eb0d1220c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db500087e726ec69bf705ccc6798dc4bf4461d0395e0fcf69b4ff37992aba192)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        '''
        value = ComputeRegionInstanceTemplateDiskDiskEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putSourceImageEncryptionKey")
    def put_source_image_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        value = ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceImageEncryptionKey", [value]))

    @jsii.member(jsii_name="putSourceSnapshotEncryptionKey")
    def put_source_snapshot_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        value = ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceSnapshotEncryptionKey", [value]))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetAutoDelete")
    def reset_auto_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDelete", []))

    @jsii.member(jsii_name="resetBoot")
    def reset_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBoot", []))

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetDiskEncryptionKey")
    def reset_disk_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKey", []))

    @jsii.member(jsii_name="resetDiskName")
    def reset_disk_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskName", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetDiskType")
    def reset_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskType", []))

    @jsii.member(jsii_name="resetGuestOsFeatures")
    def reset_guest_os_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestOsFeatures", []))

    @jsii.member(jsii_name="resetInterface")
    def reset_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterface", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetProvisionedIops")
    def reset_provisioned_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedIops", []))

    @jsii.member(jsii_name="resetProvisionedThroughput")
    def reset_provisioned_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedThroughput", []))

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @jsii.member(jsii_name="resetResourcePolicies")
    def reset_resource_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePolicies", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSourceImage")
    def reset_source_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImage", []))

    @jsii.member(jsii_name="resetSourceImageEncryptionKey")
    def reset_source_image_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageEncryptionKey", []))

    @jsii.member(jsii_name="resetSourceSnapshot")
    def reset_source_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshot", []))

    @jsii.member(jsii_name="resetSourceSnapshotEncryptionKey")
    def reset_source_snapshot_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshotEncryptionKey", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(
        self,
    ) -> ComputeRegionInstanceTemplateDiskDiskEncryptionKeyOutputReference:
        return typing.cast(ComputeRegionInstanceTemplateDiskDiskEncryptionKeyOutputReference, jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeRegionInstanceTemplateDiskSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateDiskSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteInput")
    def auto_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="bootInput")
    def boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyInput")
    def disk_encryption_key_input(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="diskNameInput")
    def disk_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeaturesInput")
    def guest_os_features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "guestOsFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedIopsInput")
    def provisioned_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughputInput")
    def provisioned_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoliciesInput")
    def resource_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcePoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKeyInput")
    def source_image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageInput")
    def source_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceImageInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotInput")
    def source_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4ad49165b62fc445658bfa41fffbe180cb3245307b7791afd3664687231822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoDelete")
    def auto_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDelete"))

    @auto_delete.setter
    def auto_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7f4a089b2b8aadbd49efed6e11bc0b72be02203604d5b2e4018277dc7cb257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="boot")
    def boot(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "boot"))

    @boot.setter
    def boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b979d1f14854ec5086085a9ec95794d207ba2c9366b572f51ae5589c2f5e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "boot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2218002caa20ac21913d5e01cdf41d7c8d9cc5f08980a4c35f5c9b09fbb0cf4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskName")
    def disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskName"))

    @disk_name.setter
    def disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b316c7bf04d7a8256628a3446be186c215336afbd67ee25a714961bc9a7c272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f775c055275c43be2f612c5fce8df6e2496f4078f7ab4ae1d9e7b397aa7540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7927280627567a944e844164cd444e266e38c319100e87d78e2f71ec2c1313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "guestOsFeatures"))

    @guest_os_features.setter
    def guest_os_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d6b7ab966745f52de0c921489d2969d776066d4a09529f6a260a5b2ed2d129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestOsFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486ce274b703cd1d9df543c89376dd6eb1bb3e185c12cc3ed7aae3db6ab76d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea5530206af349503bc256274882ec0ef5b576282c93feca2ad188b2355b7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09186475935a5b595757b42a7c3f8bae65acc20d8cd75868348218ea817595d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6a9931c96d4b653a3b3aea77b6a532f5f4b5bc85e61d265e772d421036aaa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f8ef167c116c1f40607a46ee5edcec875b686da7f0aed734cb88a51567b210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTags")
    def resource_manager_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceManagerTags"))

    @resource_manager_tags.setter
    def resource_manager_tags(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d86a35d47d58ab3fba229bb333ea0cd84621007ee39dde2507717b34ea26b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d7ee4fc5bbc5b279e3e450445180f758e06ed8cd65600a4fee3e2bf57b2a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c4059a2c6eb0f733ed0dcec480d0f0297274be0ddbea0d30e22744e205f391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceImage")
    def source_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImage"))

    @source_image.setter
    def source_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0b95700b61af275c0dab302c55b6ba0882c5381772405dc175c1ee357a7c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5df98d6a1c6623699ba1c4500f360578a2be9bc624790347de1793363b50965d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e94a79afb9e1567be43bae44ad06325f29f62550adb866d2f29bb0fc4687d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cb2c30395ca65b2a423551bf043a9355857a71f6c93104f8bd3be344220fc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56afd9f8b9375e0999ff9c51bacc07ac6071e10b4da504b04b314c578bc4bf2b)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
            check_type(argname="argument rsa_encrypted_key", value=rsa_encrypted_key, expected_type=type_hints["rsa_encrypted_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key
        if rsa_encrypted_key is not None:
            self._values["rsa_encrypted_key"] = rsa_encrypted_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key that is stored in Google Cloud KMS.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute
        Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateDiskSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f6656d1b1e9c908d815a94490c70c790092da43db64d95f5aedc31bf75fc098)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @jsii.member(jsii_name="resetRsaEncryptedKey")
    def reset_rsa_encrypted_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaEncryptedKey", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKeyInput")
    def rsa_encrypted_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaEncryptedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b6c3e4b4397dfc91406f720b048c5616413e08f304710074081ba82b26c7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8888b3b110d449df7991661c764adc06853ea9c930bae69187ccfc4bb523d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04035a233ab7f7fc9248b78552aaba396a866b93dbbc9455b18c14dcc770242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcbb4ca3191e374ab69cf8f0df1d914a535c9f1f6528ea40bce5d0615740a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34426a9d0f39ff096dd6a4d6e648e6b2665bd7e7871b5726abf0cf43ff213aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8648925bb34f0dd2631ff1446f13786e9181738bc35b250555714bc1e53acf69)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
            check_type(argname="argument rsa_encrypted_key", value=rsa_encrypted_key, expected_type=type_hints["rsa_encrypted_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key
        if rsa_encrypted_key is not None:
            self._values["rsa_encrypted_key"] = rsa_encrypted_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key that is stored in Google Cloud KMS.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_self_link ComputeRegionInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute
        Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#kms_key_service_account ComputeRegionInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#raw_key ComputeRegionInstanceTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#rsa_encrypted_key ComputeRegionInstanceTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc2ef27221280a2a10bbe0d670367da90b563329f3aa9f6f16b4da7cff20d491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetKmsKeyServiceAccount")
    def reset_kms_key_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyServiceAccount", []))

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @jsii.member(jsii_name="resetRsaEncryptedKey")
    def reset_rsa_encrypted_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaEncryptedKey", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccountInput")
    def kms_key_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKeyInput")
    def rsa_encrypted_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaEncryptedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48af2ff54bb54dac0f4bd27033df5c24bc89e62da49582e681972a27a8b9006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9945ccf055b53cca22be59f8da74eb2fd4da7e6ad68be3d97bf321d19f630233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c35da9688952ee9bcad988133e028f1d8434ad33c7455a3f7db6d5a4a5b4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcdfa327c8de4d4222634f3c6ebe2a8b086564fcf2dac96d629a5c260681ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f14f88e6d0e6652fe41a48864788c379aa8656b8a718b755144c4ea9c2a266a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class ComputeRegionInstanceTemplateGuestAccelerator:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#count ComputeRegionInstanceTemplate#count}
        :param type: The accelerator type resource to expose to this instance. E.g. nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b40538bc453fee6fb2298262d78b19f03d524cc038151a80ac177109106265)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#count ComputeRegionInstanceTemplate#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource to expose to this instance. E.g. nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateGuestAcceleratorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f745e9f3edc3bee4fe5a2842db6545e40e33c6501a3a7fb0b26a4b803a94ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60728f9476bffce0ffc57454af997340c7c8bf68248250bc884702eee363e62f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654675290658ad13f8c11c292e634826b29ef0a1f372077a9f81dcb1492747e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b248f4cc2ec16c23af5637240af986919be33ea062c18334ff3dead57527248)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44bcd63d0ddc387409dddc0273a6b182ecc7afd08728c6168503a90ab70c9fbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46755f45568f0615d83600e885c27a5265559ccf2bd193cf9a9adf916395bdf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateGuestAcceleratorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2fd7f2a0cb1d56595be81566d81ec9d2b7bd2fb458bddb06d8519a26ccde788)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823a60917e7ce8387b89aed7f45d5bea2a46bb800daabae2f60d016927e8aca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0215aa04bd1102644cdecb33b5664d626cd50ee8eaf09ced33bc4c40e81fbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3a38a24c7fb3d5542ab93a27b1fc5106cf130b4eb6a52a6b87ff8fcd4b6886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "alias_ip_range": "aliasIpRange",
        "internal_ipv6_prefix_length": "internalIpv6PrefixLength",
        "ipv6_access_config": "ipv6AccessConfig",
        "ipv6_address": "ipv6Address",
        "network": "network",
        "network_ip": "networkIp",
        "nic_type": "nicType",
        "queue_count": "queueCount",
        "stack_type": "stackType",
        "subnetwork": "subnetwork",
        "subnetwork_project": "subnetworkProject",
    },
)
class ComputeRegionInstanceTemplateNetworkInterface:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
        ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ipv6_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_ip: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        queue_count: typing.Optional[jsii.Number] = None,
        stack_type: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        subnetwork_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#access_config ComputeRegionInstanceTemplate#access_config}
        :param alias_ip_range: alias_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#alias_ip_range ComputeRegionInstanceTemplate#alias_ip_range}
        :param internal_ipv6_prefix_length: The prefix length of the primary internal IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#internal_ipv6_prefix_length ComputeRegionInstanceTemplate#internal_ipv6_prefix_length}
        :param ipv6_access_config: ipv6_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ipv6_access_config ComputeRegionInstanceTemplate#ipv6_access_config}
        :param ipv6_address: An IPv6 internal network address for this network interface. If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ipv6_address ComputeRegionInstanceTemplate#ipv6_address}
        :param network: The name or self_link of the network to attach this interface to. Use network attribute for Legacy or Auto subnetted networks and subnetwork for custom subnetted networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network ComputeRegionInstanceTemplate#network}
        :param network_ip: The private IP address to assign to the instance. If empty, the address will be automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_ip ComputeRegionInstanceTemplate#network_ip}
        :param nic_type: The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, MRDMA, and IRDMA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nic_type ComputeRegionInstanceTemplate#nic_type}
        :param queue_count: The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It will be empty if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#queue_count ComputeRegionInstanceTemplate#queue_count}
        :param stack_type: The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#stack_type ComputeRegionInstanceTemplate#stack_type}
        :param subnetwork: The name of the subnetwork to attach this interface to. The subnetwork must exist in the same region this instance will be created in. Either network or subnetwork must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork ComputeRegionInstanceTemplate#subnetwork}
        :param subnetwork_project: The ID of the project in which the subnetwork belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork_project ComputeRegionInstanceTemplate#subnetwork_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20acf50197e08084b1fcdf6345c7ffd17bcc2ab246f950b5e98e8208c92ed17)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument alias_ip_range", value=alias_ip_range, expected_type=type_hints["alias_ip_range"])
            check_type(argname="argument internal_ipv6_prefix_length", value=internal_ipv6_prefix_length, expected_type=type_hints["internal_ipv6_prefix_length"])
            check_type(argname="argument ipv6_access_config", value=ipv6_access_config, expected_type=type_hints["ipv6_access_config"])
            check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_ip", value=network_ip, expected_type=type_hints["network_ip"])
            check_type(argname="argument nic_type", value=nic_type, expected_type=type_hints["nic_type"])
            check_type(argname="argument queue_count", value=queue_count, expected_type=type_hints["queue_count"])
            check_type(argname="argument stack_type", value=stack_type, expected_type=type_hints["stack_type"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument subnetwork_project", value=subnetwork_project, expected_type=type_hints["subnetwork_project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if alias_ip_range is not None:
            self._values["alias_ip_range"] = alias_ip_range
        if internal_ipv6_prefix_length is not None:
            self._values["internal_ipv6_prefix_length"] = internal_ipv6_prefix_length
        if ipv6_access_config is not None:
            self._values["ipv6_access_config"] = ipv6_access_config
        if ipv6_address is not None:
            self._values["ipv6_address"] = ipv6_address
        if network is not None:
            self._values["network"] = network
        if network_ip is not None:
            self._values["network_ip"] = network_ip
        if nic_type is not None:
            self._values["nic_type"] = nic_type
        if queue_count is not None:
            self._values["queue_count"] = queue_count
        if stack_type is not None:
            self._values["stack_type"] = stack_type
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if subnetwork_project is not None:
            self._values["subnetwork_project"] = subnetwork_project

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#access_config ComputeRegionInstanceTemplate#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig"]]], result)

    @builtins.property
    def alias_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange"]]]:
        '''alias_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#alias_ip_range ComputeRegionInstanceTemplate#alias_ip_range}
        '''
        result = self._values.get("alias_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange"]]], result)

    @builtins.property
    def internal_ipv6_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''The prefix length of the primary internal IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#internal_ipv6_prefix_length ComputeRegionInstanceTemplate#internal_ipv6_prefix_length}
        '''
        result = self._values.get("internal_ipv6_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ipv6_access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig"]]]:
        '''ipv6_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ipv6_access_config ComputeRegionInstanceTemplate#ipv6_access_config}
        '''
        result = self._values.get("ipv6_access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig"]]], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''An IPv6 internal network address for this network interface.

        If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ipv6_address ComputeRegionInstanceTemplate#ipv6_address}
        '''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the network to attach this interface to.

        Use network attribute for Legacy or Auto subnetted networks and subnetwork for custom subnetted networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network ComputeRegionInstanceTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_ip(self) -> typing.Optional[builtins.str]:
        '''The private IP address to assign to the instance. If empty, the address will be automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_ip ComputeRegionInstanceTemplate#network_ip}
        '''
        result = self._values.get("network_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, MRDMA, and IRDMA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nic_type ComputeRegionInstanceTemplate#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_count(self) -> typing.Optional[jsii.Number]:
        '''The networking queue count that's specified by users for the network interface.

        Both Rx and Tx queues will be set to this number. It will be empty if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#queue_count ComputeRegionInstanceTemplate#queue_count}
        '''
        result = self._values.get("queue_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this network interface to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#stack_type ComputeRegionInstanceTemplate#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name of the subnetwork to attach this interface to.

        The subnetwork must exist in the same region this instance will be created in. Either network or subnetwork must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork ComputeRegionInstanceTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the subnetwork belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork_project ComputeRegionInstanceTemplate#subnetwork_project}
        '''
        result = self._values.get("subnetwork_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"nat_ip": "natIp", "network_tier": "networkTier"},
)
class ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig:
    def __init__(
        self,
        *,
        nat_ip: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nat_ip: The IP address that will be 1:1 mapped to the instance's network ip. If not given, one will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nat_ip ComputeRegionInstanceTemplate#nat_ip}
        :param network_tier: The networking tier used for configuring this instance template. This field can take the following values: PREMIUM, STANDARD, FIXED_STANDARD. If this field is not specified, it is assumed to be PREMIUM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_tier ComputeRegionInstanceTemplate#network_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6389f44f4cfd43ab07ea747aba3503adbefbd4fd2affd468fa4bfe9509653e4a)
            check_type(argname="argument nat_ip", value=nat_ip, expected_type=type_hints["nat_ip"])
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if nat_ip is not None:
            self._values["nat_ip"] = nat_ip
        if network_tier is not None:
            self._values["network_tier"] = network_tier

    @builtins.property
    def nat_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address that will be 1:1 mapped to the instance's network ip.

        If not given, one will be generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nat_ip ComputeRegionInstanceTemplate#nat_ip}
        '''
        result = self._values.get("nat_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tier(self) -> typing.Optional[builtins.str]:
        '''The networking tier used for configuring this instance template.

        This field can take the following values: PREMIUM, STANDARD, FIXED_STANDARD. If this field is not specified, it is assumed to be PREMIUM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_tier ComputeRegionInstanceTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a14bd58d293154583879338805f6968bb7c5c44e0ab8f2a7d9c8e6945072be34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1144a35b0f627a485f733f4b77cefc5ea8d82adb41dd8775f60383deef1855)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b7222d08cb52bb249641de82b17c30dc63598991c1b7f476db62ac57a401e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab586a81d2ee7217142acc1fe60f10d609738b52d1f92f6a4eb947291bcf435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5415d38fd92b0341e367fe945d0138b4fac25d9f2de6ef26fcf227495c9f6417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca17b5b27acdc2fbeee345fb10f25267700a48e4371104a2a014f2cc5d9cde9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b082a18f4167594d878a007e2b645046e893c9d0d487e979ae6f402bd36605f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNatIp")
    def reset_nat_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNatIp", []))

    @jsii.member(jsii_name="resetNetworkTier")
    def reset_network_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTier", []))

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="natIpInput")
    def nat_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natIpInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTierInput")
    def network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="natIp")
    def nat_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natIp"))

    @nat_ip.setter
    def nat_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180e73368e3ae2a5be499bffa5bdcdace1153946fba628adcbf2228d1e1fe102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cae29a8fa783f085737915decf5b457a5508afec68407e3e2cbecfe16cb916f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dbddf07aba916aa879bbcd94b4c519928479d5126c2dca3fd2aee7b108cb536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "ip_cidr_range": "ipCidrRange",
        "subnetwork_range_name": "subnetworkRangeName",
    },
)
class ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange:
    def __init__(
        self,
        *,
        ip_cidr_range: builtins.str,
        subnetwork_range_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_cidr_range: The IP CIDR range represented by this alias IP range. This IP CIDR range must belong to the specified subnetwork and cannot contain IP addresses reserved by system or used by other network interfaces. At the time of writing only a netmask (e.g. /24) may be supplied, with a CIDR format resulting in an API error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ip_cidr_range ComputeRegionInstanceTemplate#ip_cidr_range}
        :param subnetwork_range_name: The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range. If left unspecified, the primary range of the subnetwork will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork_range_name ComputeRegionInstanceTemplate#subnetwork_range_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a70f7af2a994fd21216f8f2e7a265c9d578651b8779b3389eff81b4dd23bc6)
            check_type(argname="argument ip_cidr_range", value=ip_cidr_range, expected_type=type_hints["ip_cidr_range"])
            check_type(argname="argument subnetwork_range_name", value=subnetwork_range_name, expected_type=type_hints["subnetwork_range_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_cidr_range": ip_cidr_range,
        }
        if subnetwork_range_name is not None:
            self._values["subnetwork_range_name"] = subnetwork_range_name

    @builtins.property
    def ip_cidr_range(self) -> builtins.str:
        '''The IP CIDR range represented by this alias IP range.

        This IP CIDR range must belong to the specified subnetwork and cannot contain IP addresses reserved by system or used by other network interfaces. At the time of writing only a netmask (e.g. /24) may be supplied, with a CIDR format resulting in an API error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#ip_cidr_range ComputeRegionInstanceTemplate#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        assert result is not None, "Required property 'ip_cidr_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnetwork_range_name(self) -> typing.Optional[builtins.str]:
        '''The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range.

        If left unspecified, the primary range of the subnetwork will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#subnetwork_range_name ComputeRegionInstanceTemplate#subnetwork_range_name}
        '''
        result = self._values.get("subnetwork_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a95470d3d85d827a5cb332f41151f2a211c0b6e291cd7eec191484754c1c216b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1070b5270b30e4a04731b3993a103b340e6e98d4e517b2682324daec86568987)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d67d692fc9189ec6cf68bb832b2ef2e081da58cd9f3748b4b6730033d8f5741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68e24f1fed1aa617a54cf630afc82410c38f390eef7875cb8ac866be394e12e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ca39752a445cb12fb5cf2ad943ad8cfb886b4d099efbaf71216cb5f546c3afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50197a193a3bc25cfab5cd0b1df330c82dc1c6eb18410047b80a8ec5e9b74a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5b7c4689649b3ec9ba417e3f88e6f2efac3763db2a10962c75f26c25f974284)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubnetworkRangeName")
    def reset_subnetwork_range_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetworkRangeName", []))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRangeInput")
    def ip_cidr_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipCidrRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkRangeNameInput")
    def subnetwork_range_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkRangeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipCidrRange")
    def ip_cidr_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipCidrRange"))

    @ip_cidr_range.setter
    def ip_cidr_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a4a5e97a2db120ff1a19bd36c6e167c3bd8dd4c0f98df0bf7fae6cdecbb44f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkRangeName")
    def subnetwork_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkRangeName"))

    @subnetwork_range_name.setter
    def subnetwork_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd740958ec4583f02e1f913e14a0e4fd8058e990032ba2f9d4139185b16bca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cc4512b1367e619467daf06c39cac8b97de05d141962f4bedccb0e91383250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig",
    jsii_struct_bases=[],
    name_mapping={"network_tier": "networkTier"},
)
class ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig:
    def __init__(self, *, network_tier: builtins.str) -> None:
        '''
        :param network_tier: The service-level to be provided for IPv6 traffic when the subnet has an external subnet. Only PREMIUM tier is valid for IPv6 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_tier ComputeRegionInstanceTemplate#network_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c69c80ccbd00b2a85e0aa0348f9ba804df23cc4f93d9d9dd608dd486615ac74)
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_tier": network_tier,
        }

    @builtins.property
    def network_tier(self) -> builtins.str:
        '''The service-level to be provided for IPv6 traffic when the subnet has an external subnet.

        Only PREMIUM tier is valid for IPv6

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#network_tier ComputeRegionInstanceTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        assert result is not None, "Required property 'network_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b409a85850bee4c9bc4ecada9829cae14c1915172c445abf31d8b16ad1629ac6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85ea6809a74aba9a11d1422f163c7672c20864a22e82b17c9a8a689eed010c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ab93c0f54308778f4ab639af315222733d1b2091e72efb87d9537a6c9f7639)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b378681e7c5810bcb45725043877cb287fa705b26c1c4d8f6205b8e8c1a601)
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
            type_hints = typing.get_type_hints(_typecheckingstub__161cbff1e5b872dbee5394dd81acc16f05e06739d841fad2f3abbddea3bb226b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43af3ff292f0d4f90b4c33d91d3aa986a22fb30644519f64d1a703d0305013e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db3971b83be6341580ac02a98f6d51d43b295d18c820517e81896616d87b8f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="externalIpv6")
    def external_ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6"))

    @builtins.property
    @jsii.member(jsii_name="externalIpv6PrefixLength")
    def external_ipv6_prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6PrefixLength"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="networkTierInput")
    def network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466fa2d1c3761c86e1ab634ebc1b34a2f0d437b2533bddb75018f9d86150e8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7296c0a6e5ce52d79228cedf0b5c652b5bdf1cde8f41707ea6e755b06d82465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cf3c811ed6363a1f9769a3f92c021c175cde97ace5d96500c2ee2fa09ff7288)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6211c2823dd379327a5bb8a47e5effdf2e76f60e32e713cac888a8751c98fe78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c7c5fc731cd42ec9ca510a13bf0dfddf8bb5b932a94dfd4a9d159064a1a90f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f74dc830f2fde63c49b539c6b9b9d5209c87d9d731019c19b12108f8bff70a39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62df8b6f5d9f6766bb71b0cbf1c8d3bc7b0c6d32f532c77d0230938f9b567982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65c23337d503f9a52bc3f3682f53eda6093db23bbaf2e269b8dc02a34bc48fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__418f36cee811072c38c28a73daefebd334daa5e634cb9a6fdc3f5684c52d2c6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a998049bb8ec88e9e9bb61e0ff426557455e910d1ae95da4fb80f4431598c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putAliasIpRange")
    def put_alias_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6406192a33f7135fcdd2a28103e7c091dcae5cbd7dfa2e8ed23b0ba5fcb48d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAliasIpRange", [value]))

    @jsii.member(jsii_name="putIpv6AccessConfig")
    def put_ipv6_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe5caadc4cf3b539835ba07112d82eeabac803c7a6de6929ad93460d9e4b2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpv6AccessConfig", [value]))

    @jsii.member(jsii_name="resetAccessConfig")
    def reset_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessConfig", []))

    @jsii.member(jsii_name="resetAliasIpRange")
    def reset_alias_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliasIpRange", []))

    @jsii.member(jsii_name="resetInternalIpv6PrefixLength")
    def reset_internal_ipv6_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalIpv6PrefixLength", []))

    @jsii.member(jsii_name="resetIpv6AccessConfig")
    def reset_ipv6_access_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6AccessConfig", []))

    @jsii.member(jsii_name="resetIpv6Address")
    def reset_ipv6_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Address", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkIp")
    def reset_network_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkIp", []))

    @jsii.member(jsii_name="resetNicType")
    def reset_nic_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicType", []))

    @jsii.member(jsii_name="resetQueueCount")
    def reset_queue_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueCount", []))

    @jsii.member(jsii_name="resetStackType")
    def reset_stack_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStackType", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetSubnetworkProject")
    def reset_subnetwork_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetworkProject", []))

    @builtins.property
    @jsii.member(jsii_name="accessConfig")
    def access_config(
        self,
    ) -> ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigList:
        return typing.cast(ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRange")
    def alias_ip_range(
        self,
    ) -> ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeList:
        return typing.cast(ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeList, jsii.get(self, "aliasIpRange"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfig")
    def ipv6_access_config(
        self,
    ) -> ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigList:
        return typing.cast(ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigList, jsii.get(self, "ipv6AccessConfig"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessType")
    def ipv6_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6AccessType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRangeInput")
    def alias_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "aliasIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6PrefixLengthInput")
    def internal_ipv6_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalIpv6PrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfigInput")
    def ipv6_access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "ipv6AccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressInput")
    def ipv6_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIpInput")
    def network_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIpInput"))

    @builtins.property
    @jsii.member(jsii_name="nicTypeInput")
    def nic_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nicTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="queueCountInput")
    def queue_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queueCountInput"))

    @builtins.property
    @jsii.member(jsii_name="stackTypeInput")
    def stack_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkProjectInput")
    def subnetwork_project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkProjectInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6PrefixLength")
    def internal_ipv6_prefix_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "internalIpv6PrefixLength"))

    @internal_ipv6_prefix_length.setter
    def internal_ipv6_prefix_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3d8bad98a709edfd1a336d28b18ecb0a751c736a2c0b70719c287c163cb2c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4340407b3c5347d173c63506a2a04c851d4af05250e5850b2108ee77984181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2f4381bfec74eadc0a7c0737206fde7ff8097e1e628da135bd6cc57110d72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkIp")
    def network_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkIp"))

    @network_ip.setter
    def network_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484d29a4b9025d8260e64e511772d1a4f740e903f8c33aa492e99a0b90313d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccf5af6d942043bedc8bc3f5946f156388ee814576c5835620e479a1ad65cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueCount")
    def queue_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueCount"))

    @queue_count.setter
    def queue_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a9fe541868b603cedfaf4bf90688b144deb51ff9222aa79633a95e6785c9b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f3f9efe1dc5d079071e57a77b4e283479d15e9e5ece20e33b5a84dcf96a01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaa30a5b47863ce1a9ab2efcb9fb6ce41b1b11805160f79791aeef9042c08da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkProject")
    def subnetwork_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkProject"))

    @subnetwork_project.setter
    def subnetwork_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c5d670d863c80d8d45f84e935bdda7992a1bbf2505897e96face900201e4ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8941e9d6026f7fe48c3c77657695267677d1298b1f17fa2ebf02f50d4fe1ae15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class ComputeRegionInstanceTemplateNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#total_egress_bandwidth_tier ComputeRegionInstanceTemplate#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23726e485ebf34581683bbabd8aae17a71967c2989e3b72d463e4b43a734593)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#total_egress_bandwidth_tier ComputeRegionInstanceTemplate#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateNetworkPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62685a3a28b0d3cb7c82bfd4f4d8ceefff0b3df140f0a3e8867b577c2b1d14a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="totalEgressBandwidthTierInput")
    def total_egress_bandwidth_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "totalEgressBandwidthTierInput"))

    @builtins.property
    @jsii.member(jsii_name="totalEgressBandwidthTier")
    def total_egress_bandwidth_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "totalEgressBandwidthTier"))

    @total_egress_bandwidth_tier.setter
    def total_egress_bandwidth_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75043a4de6d256aace2b64680fad351e2c9887fb539a0484894f931cf14dcaa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93715f928a54992e4fa9d4c933efd051966731606dfa0938987fafbf523a30f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "specific_reservation": "specificReservation"},
)
class ComputeRegionInstanceTemplateReservationAffinity:
    def __init__(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#specific_reservation ComputeRegionInstanceTemplate#specific_reservation}
        '''
        if isinstance(specific_reservation, dict):
            specific_reservation = ComputeRegionInstanceTemplateReservationAffinitySpecificReservation(**specific_reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3562df6c1482d43c12f771e68fe9f49a8441b692d6f309aac36f2d17b6e479)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument specific_reservation", value=specific_reservation, expected_type=type_hints["specific_reservation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if specific_reservation is not None:
            self._values["specific_reservation"] = specific_reservation

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of reservation from which this instance can consume resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#type ComputeRegionInstanceTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def specific_reservation(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation"]:
        '''specific_reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#specific_reservation ComputeRegionInstanceTemplate#specific_reservation}
        '''
        result = self._values.get("specific_reservation")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a242e607ec677305593f4d58079a27e6091233d7a17873eedd1980f16862ac21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSpecificReservation")
    def put_specific_reservation(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key ComputeRegionInstanceTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#values ComputeRegionInstanceTemplate#values}
        '''
        value = ComputeRegionInstanceTemplateReservationAffinitySpecificReservation(
            key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSpecificReservation", [value]))

    @jsii.member(jsii_name="resetSpecificReservation")
    def reset_specific_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpecificReservation", []))

    @builtins.property
    @jsii.member(jsii_name="specificReservation")
    def specific_reservation(
        self,
    ) -> "ComputeRegionInstanceTemplateReservationAffinitySpecificReservationOutputReference":
        return typing.cast("ComputeRegionInstanceTemplateReservationAffinitySpecificReservationOutputReference", jsii.get(self, "specificReservation"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationInput")
    def specific_reservation_input(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation"]:
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateReservationAffinitySpecificReservation"], jsii.get(self, "specificReservationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a71d03c8fd37f15c75fb63bfd18c4038b9a487df52d79fd74989d16cf63362c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateReservationAffinity]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2767c27ab211ab0a2f6e19e482afbe169f2814472a0c53216d0988f1f42b55b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateReservationAffinitySpecificReservation",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class ComputeRegionInstanceTemplateReservationAffinitySpecificReservation:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key ComputeRegionInstanceTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#values ComputeRegionInstanceTemplate#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2664c9ebbefe56fd20c6b04f2f12f03176aaa282689edd2fbb4eb7d11ccf7f94)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Corresponds to the label key of a reservation resource.

        To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key ComputeRegionInstanceTemplate#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Corresponds to the label values of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#values ComputeRegionInstanceTemplate#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateReservationAffinitySpecificReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateReservationAffinitySpecificReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateReservationAffinitySpecificReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__323ed799fd45ed4ceb0b69a9f74d7c77aa49b86f64d90567280aab2d5854cc3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035f5954cf43ee926c4138214713ff44254cef625a7bcd419c3e629696236846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5690a8d625460b3db5cb15d5432f96406e7122cd0706563b17b78efda15b815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateReservationAffinitySpecificReservation]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateReservationAffinitySpecificReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateReservationAffinitySpecificReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a66ff57543392a7f32b44cb34868be5d411a54f6fd770c7f1fec00a7ea6237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateScheduling",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_restart": "automaticRestart",
        "availability_domain": "availabilityDomain",
        "instance_termination_action": "instanceTerminationAction",
        "local_ssd_recovery_timeout": "localSsdRecoveryTimeout",
        "max_run_duration": "maxRunDuration",
        "min_node_cpus": "minNodeCpus",
        "node_affinities": "nodeAffinities",
        "on_host_maintenance": "onHostMaintenance",
        "on_instance_stop_action": "onInstanceStopAction",
        "preemptible": "preemptible",
        "provisioning_model": "provisioningModel",
        "termination_time": "terminationTime",
    },
)
class ComputeRegionInstanceTemplateScheduling:
    def __init__(
        self,
        *,
        automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_domain: typing.Optional[jsii.Number] = None,
        instance_termination_action: typing.Optional[builtins.str] = None,
        local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeRegionInstanceTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionInstanceTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user). This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#automatic_restart ComputeRegionInstanceTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#availability_domain ComputeRegionInstanceTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_termination_action ComputeRegionInstanceTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#local_ssd_recovery_timeout ComputeRegionInstanceTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#max_run_duration ComputeRegionInstanceTemplate#max_run_duration}
        :param min_node_cpus: Minimum number of cpus for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_node_cpus ComputeRegionInstanceTemplate#min_node_cpus}
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#node_affinities ComputeRegionInstanceTemplate#node_affinities}
        :param on_host_maintenance: Defines the maintenance behavior for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_host_maintenance ComputeRegionInstanceTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_instance_stop_action ComputeRegionInstanceTemplate#on_instance_stop_action}
        :param preemptible: Allows instance to be preempted. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#preemptible ComputeRegionInstanceTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioning_model ComputeRegionInstanceTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#termination_time ComputeRegionInstanceTemplate#termination_time}
        '''
        if isinstance(max_run_duration, dict):
            max_run_duration = ComputeRegionInstanceTemplateSchedulingMaxRunDuration(**max_run_duration)
        if isinstance(on_instance_stop_action, dict):
            on_instance_stop_action = ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction(**on_instance_stop_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6968cd1a47d00d9f58148373c53d808f94f90b2b9a9426fd1040405b81e724fd)
            check_type(argname="argument automatic_restart", value=automatic_restart, expected_type=type_hints["automatic_restart"])
            check_type(argname="argument availability_domain", value=availability_domain, expected_type=type_hints["availability_domain"])
            check_type(argname="argument instance_termination_action", value=instance_termination_action, expected_type=type_hints["instance_termination_action"])
            check_type(argname="argument local_ssd_recovery_timeout", value=local_ssd_recovery_timeout, expected_type=type_hints["local_ssd_recovery_timeout"])
            check_type(argname="argument max_run_duration", value=max_run_duration, expected_type=type_hints["max_run_duration"])
            check_type(argname="argument min_node_cpus", value=min_node_cpus, expected_type=type_hints["min_node_cpus"])
            check_type(argname="argument node_affinities", value=node_affinities, expected_type=type_hints["node_affinities"])
            check_type(argname="argument on_host_maintenance", value=on_host_maintenance, expected_type=type_hints["on_host_maintenance"])
            check_type(argname="argument on_instance_stop_action", value=on_instance_stop_action, expected_type=type_hints["on_instance_stop_action"])
            check_type(argname="argument preemptible", value=preemptible, expected_type=type_hints["preemptible"])
            check_type(argname="argument provisioning_model", value=provisioning_model, expected_type=type_hints["provisioning_model"])
            check_type(argname="argument termination_time", value=termination_time, expected_type=type_hints["termination_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_restart is not None:
            self._values["automatic_restart"] = automatic_restart
        if availability_domain is not None:
            self._values["availability_domain"] = availability_domain
        if instance_termination_action is not None:
            self._values["instance_termination_action"] = instance_termination_action
        if local_ssd_recovery_timeout is not None:
            self._values["local_ssd_recovery_timeout"] = local_ssd_recovery_timeout
        if max_run_duration is not None:
            self._values["max_run_duration"] = max_run_duration
        if min_node_cpus is not None:
            self._values["min_node_cpus"] = min_node_cpus
        if node_affinities is not None:
            self._values["node_affinities"] = node_affinities
        if on_host_maintenance is not None:
            self._values["on_host_maintenance"] = on_host_maintenance
        if on_instance_stop_action is not None:
            self._values["on_instance_stop_action"] = on_instance_stop_action
        if preemptible is not None:
            self._values["preemptible"] = preemptible
        if provisioning_model is not None:
            self._values["provisioning_model"] = provisioning_model
        if termination_time is not None:
            self._values["termination_time"] = termination_time

    @builtins.property
    def automatic_restart(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user).

        This defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#automatic_restart ComputeRegionInstanceTemplate#automatic_restart}
        '''
        result = self._values.get("automatic_restart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_domain(self) -> typing.Optional[jsii.Number]:
        '''Specifies the availability domain, which this instance should be scheduled on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#availability_domain ComputeRegionInstanceTemplate#availability_domain}
        '''
        result = self._values.get("availability_domain")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_termination_action(self) -> typing.Optional[builtins.str]:
        '''Specifies the action GCE should take when SPOT VM is preempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#instance_termination_action ComputeRegionInstanceTemplate#instance_termination_action}
        '''
        result = self._values.get("instance_termination_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_recovery_timeout(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout"]]]:
        '''local_ssd_recovery_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#local_ssd_recovery_timeout ComputeRegionInstanceTemplate#local_ssd_recovery_timeout}
        '''
        result = self._values.get("local_ssd_recovery_timeout")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout"]]], result)

    @builtins.property
    def max_run_duration(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateSchedulingMaxRunDuration"]:
        '''max_run_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#max_run_duration ComputeRegionInstanceTemplate#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateSchedulingMaxRunDuration"], result)

    @builtins.property
    def min_node_cpus(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of cpus for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#min_node_cpus ComputeRegionInstanceTemplate#min_node_cpus}
        '''
        result = self._values.get("min_node_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_affinities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateSchedulingNodeAffinities"]]]:
        '''node_affinities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#node_affinities ComputeRegionInstanceTemplate#node_affinities}
        '''
        result = self._values.get("node_affinities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionInstanceTemplateSchedulingNodeAffinities"]]], result)

    @builtins.property
    def on_host_maintenance(self) -> typing.Optional[builtins.str]:
        '''Defines the maintenance behavior for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_host_maintenance ComputeRegionInstanceTemplate#on_host_maintenance}
        '''
        result = self._values.get("on_host_maintenance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_instance_stop_action(
        self,
    ) -> typing.Optional["ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction"]:
        '''on_instance_stop_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#on_instance_stop_action ComputeRegionInstanceTemplate#on_instance_stop_action}
        '''
        result = self._values.get("on_instance_stop_action")
        return typing.cast(typing.Optional["ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction"], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows instance to be preempted. This defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#preemptible ComputeRegionInstanceTemplate#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_model(self) -> typing.Optional[builtins.str]:
        '''Whether the instance is spot. If this is set as SPOT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#provisioning_model ComputeRegionInstanceTemplate#provisioning_model}
        '''
        result = self._values.get("provisioning_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the timestamp, when the instance will be terminated, in RFC3339 text format.

        If specified, the instance termination action
        will be performed at the termination time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#termination_time ComputeRegionInstanceTemplate#termination_time}
        '''
        result = self._values.get("termination_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#seconds ComputeRegionInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nanos ComputeRegionInstanceTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8092087c0a309b93051bef974d571f1cf1a86aab6860acb67848787e2f1ed3a)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#seconds ComputeRegionInstanceTemplate#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented
        with a 0 seconds field and a positive nanos field. Must
        be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nanos ComputeRegionInstanceTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__885f5956cb5d85a7d7f77fdfd9881260d9ff8f3a8277bddfb8169cb55d0e1492)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8adbb88679c778ef219d8bad535eab1ac7df3f2ff744a13fa6935f55f5cb1790)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc95a8b9bc82de12e24c963d0250e71d106a6195f600c43e96e32c61fa26cdfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d35053acc9fd70a5cb0b17efc4dbdf6dc79b2d7630fe149a2e50717b924c17c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__266ddb11cd875bd2b3af4381106c21c13ceee72ab91c61754f0cc316e5565677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6788cd1bcac85c40bc39906ca12f94239310fef7cd4008b17242453e9fe8cd0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19028d3e85fa0c0ffc088517543568cef7f0837c0c68a90ffdf5fb54c9713fa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e0172db219b906ff53a45899739ec7cca38dcb18aa309c059006ad56a5fe36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd9252e3854dad4e8aec2cb7f46590566ed42cbc17c36c85b395427bbe84e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5c62645d95372f2dc891b595345f8c64c426fcedc587569a4f49e2caf010be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingMaxRunDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeRegionInstanceTemplateSchedulingMaxRunDuration:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#seconds ComputeRegionInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nanos ComputeRegionInstanceTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b342c7a6019c6bcf5599d634cf7f3dc54b14ff48187485044dfd0bb243f0bd)
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seconds": seconds,
        }
        if nanos is not None:
            self._values["nanos"] = nanos

    @builtins.property
    def seconds(self) -> jsii.Number:
        '''Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#seconds ComputeRegionInstanceTemplate#seconds}
        '''
        result = self._values.get("seconds")
        assert result is not None, "Required property 'seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Span of time that's a fraction of a second at nanosecond resolution.

        Durations less than one second are represented
        with a 0 seconds field and a positive nanos field. Must
        be from 0 to 999,999,999 inclusive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nanos ComputeRegionInstanceTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateSchedulingMaxRunDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateSchedulingMaxRunDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingMaxRunDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27f6d51ced65fdf53776745b27c86d0e8626a908e71c4f537f5d90f40915b77d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bebbd640e21628d8238900398c9a7f4cb261c8da9a94213b09193337d79a1a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c44ae4bb2dd60bb4d996e88e4bda6141946e5926fc090ad8aae276ca3258ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae22b1f4c1108ac3a786dafd63c444709ac662761c3810a4eb387f63063b004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingNodeAffinities",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ComputeRegionInstanceTemplateSchedulingNodeAffinities:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key ComputeRegionInstanceTemplate#key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#operator ComputeRegionInstanceTemplate#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#values ComputeRegionInstanceTemplate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f61063cdc08d0de04d8c96dad9712624850a8c904801a8ab4181258316bedb5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#key ComputeRegionInstanceTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#operator ComputeRegionInstanceTemplate#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#values ComputeRegionInstanceTemplate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateSchedulingNodeAffinities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateSchedulingNodeAffinitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingNodeAffinitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bef5d291bbad800fe3bc36042ea91557a1310cbf6eb75f4b7b1e8e6346fa37b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionInstanceTemplateSchedulingNodeAffinitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91936eac7f89a4661a23c4c3f3b16086212b79a713733255cf55b75090f33b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionInstanceTemplateSchedulingNodeAffinitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949dd40e63f2645cc667e2d401fa20bac7d98e52243f47327c99fd6dc5944ac5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24021a2bce07063743ca924b0f41fa7a32e4e603da26b3d2fca03777f1642b0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bcf5fbe5a8acba3129c1f84878195adb37c9dcc384046c98ec196b319b29686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315a2e675a1dcbb6974a980ddb6dc82e1bac6bc7e744c66ccbac1e349bc38b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateSchedulingNodeAffinitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingNodeAffinitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8217602aba3380278729f680e1ad23bf40f11f5e68718f550aa326e02ad812cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dac1f64cbe07a510b9951d76a7ad09dcbd79f62a3fdaf684bad84cc9a1b660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd7ba449beeb98eeeed378bdce5f824dd10df48a143623a4d100ab20d0ced61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56de3a1efb88b00930ddc02eb63b264d22745015ac271f6a1413f1ef89bc1db5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingNodeAffinities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingNodeAffinities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingNodeAffinities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1867c3690e60e216417fe3670acee2585486157e147992ce3291b13bfe8244d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction",
    jsii_struct_bases=[],
    name_mapping={"discard_local_ssd": "discardLocalSsd"},
)
class ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction:
    def __init__(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#discard_local_ssd ComputeRegionInstanceTemplate#discard_local_ssd}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad2a8d7b906c9ab22961e1dacbe2c54e644704075adcc5eac15dc0179ddc825)
            check_type(argname="argument discard_local_ssd", value=discard_local_ssd, expected_type=type_hints["discard_local_ssd"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discard_local_ssd is not None:
            self._values["discard_local_ssd"] = discard_local_ssd

    @builtins.property
    def discard_local_ssd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the contents of any attached Local SSD disks will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#discard_local_ssd ComputeRegionInstanceTemplate#discard_local_ssd}
        '''
        result = self._values.get("discard_local_ssd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateSchedulingOnInstanceStopActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingOnInstanceStopActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60ad8588e2308f0967cc23a3c62af3fed8400336540957cfeddd1ace68bc1b98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiscardLocalSsd")
    def reset_discard_local_ssd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscardLocalSsd", []))

    @builtins.property
    @jsii.member(jsii_name="discardLocalSsdInput")
    def discard_local_ssd_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "discardLocalSsdInput"))

    @builtins.property
    @jsii.member(jsii_name="discardLocalSsd")
    def discard_local_ssd(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "discardLocalSsd"))

    @discard_local_ssd.setter
    def discard_local_ssd(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e41f50fc0be198df26c3620c55980f59f53071ca2adc350e0cf3ca858ccaa77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discardLocalSsd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79a0b833deefb579f795b66551e5d4411b01620259b7a8ce4830ba05607a016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionInstanceTemplateSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cca6092733539a78e1d59ff3f3017f46ab7e38de83880b468dbcd9ac208fddb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalSsdRecoveryTimeout")
    def put_local_ssd_recovery_timeout(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4b8af6afd85b8c3a48a26004d429ecf7c9d4a15bb3976235195d9b058e63d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLocalSsdRecoveryTimeout", [value]))

    @jsii.member(jsii_name="putMaxRunDuration")
    def put_max_run_duration(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#seconds ComputeRegionInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#nanos ComputeRegionInstanceTemplate#nanos}
        '''
        value = ComputeRegionInstanceTemplateSchedulingMaxRunDuration(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putMaxRunDuration", [value]))

    @jsii.member(jsii_name="putNodeAffinities")
    def put_node_affinities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4f168f14ff79c180a3a6c2b35489879803822d83fe508c44c8352db2429918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinities", [value]))

    @jsii.member(jsii_name="putOnInstanceStopAction")
    def put_on_instance_stop_action(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#discard_local_ssd ComputeRegionInstanceTemplate#discard_local_ssd}
        '''
        value = ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction(
            discard_local_ssd=discard_local_ssd
        )

        return typing.cast(None, jsii.invoke(self, "putOnInstanceStopAction", [value]))

    @jsii.member(jsii_name="resetAutomaticRestart")
    def reset_automatic_restart(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticRestart", []))

    @jsii.member(jsii_name="resetAvailabilityDomain")
    def reset_availability_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityDomain", []))

    @jsii.member(jsii_name="resetInstanceTerminationAction")
    def reset_instance_termination_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceTerminationAction", []))

    @jsii.member(jsii_name="resetLocalSsdRecoveryTimeout")
    def reset_local_ssd_recovery_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalSsdRecoveryTimeout", []))

    @jsii.member(jsii_name="resetMaxRunDuration")
    def reset_max_run_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRunDuration", []))

    @jsii.member(jsii_name="resetMinNodeCpus")
    def reset_min_node_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNodeCpus", []))

    @jsii.member(jsii_name="resetNodeAffinities")
    def reset_node_affinities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAffinities", []))

    @jsii.member(jsii_name="resetOnHostMaintenance")
    def reset_on_host_maintenance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnHostMaintenance", []))

    @jsii.member(jsii_name="resetOnInstanceStopAction")
    def reset_on_instance_stop_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnInstanceStopAction", []))

    @jsii.member(jsii_name="resetPreemptible")
    def reset_preemptible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptible", []))

    @jsii.member(jsii_name="resetProvisioningModel")
    def reset_provisioning_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisioningModel", []))

    @jsii.member(jsii_name="resetTerminationTime")
    def reset_termination_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationTime", []))

    @builtins.property
    @jsii.member(jsii_name="localSsdRecoveryTimeout")
    def local_ssd_recovery_timeout(
        self,
    ) -> ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList:
        return typing.cast(ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList, jsii.get(self, "localSsdRecoveryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(
        self,
    ) -> ComputeRegionInstanceTemplateSchedulingMaxRunDurationOutputReference:
        return typing.cast(ComputeRegionInstanceTemplateSchedulingMaxRunDurationOutputReference, jsii.get(self, "maxRunDuration"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinities")
    def node_affinities(
        self,
    ) -> ComputeRegionInstanceTemplateSchedulingNodeAffinitiesList:
        return typing.cast(ComputeRegionInstanceTemplateSchedulingNodeAffinitiesList, jsii.get(self, "nodeAffinities"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopAction")
    def on_instance_stop_action(
        self,
    ) -> ComputeRegionInstanceTemplateSchedulingOnInstanceStopActionOutputReference:
        return typing.cast(ComputeRegionInstanceTemplateSchedulingOnInstanceStopActionOutputReference, jsii.get(self, "onInstanceStopAction"))

    @builtins.property
    @jsii.member(jsii_name="automaticRestartInput")
    def automatic_restart_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticRestartInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityDomainInput")
    def availability_domain_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "availabilityDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTerminationActionInput")
    def instance_termination_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTerminationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="localSsdRecoveryTimeoutInput")
    def local_ssd_recovery_timeout_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]], jsii.get(self, "localSsdRecoveryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDurationInput")
    def max_run_duration_input(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration], jsii.get(self, "maxRunDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCpusInput")
    def min_node_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinitiesInput")
    def node_affinities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]], jsii.get(self, "nodeAffinitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenanceInput")
    def on_host_maintenance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onHostMaintenanceInput"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopActionInput")
    def on_instance_stop_action_input(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction], jsii.get(self, "onInstanceStopActionInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptibleInput")
    def preemptible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preemptibleInput"))

    @builtins.property
    @jsii.member(jsii_name="provisioningModelInput")
    def provisioning_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provisioningModelInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationTimeInput")
    def termination_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terminationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticRestart")
    def automatic_restart(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticRestart"))

    @automatic_restart.setter
    def automatic_restart(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752939b87e267cd1103100b1a9217a02c2c886c6b0c5eb9defd2267af178b493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticRestart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityDomain")
    def availability_domain(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomain"))

    @availability_domain.setter
    def availability_domain(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436cc1099eeee5497c2150e3a7da1be3e00cad3927764e06a6b2bc47e8e4a20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTerminationAction")
    def instance_termination_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminationAction"))

    @instance_termination_action.setter
    def instance_termination_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef080eec92ac3d39657b5adf1ca3c89846fb10a61adce5a5a79f1dd7626164a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCpus")
    def min_node_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCpus"))

    @min_node_cpus.setter
    def min_node_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77d498b6b03296d4df8fa92e382ff1880ad554bd42324f53c3ed9d08e1c6a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenance")
    def on_host_maintenance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onHostMaintenance"))

    @on_host_maintenance.setter
    def on_host_maintenance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6a63862a17be87989d22eb4dae4fe807b980767f58c4b99c7675d51f3c8243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onHostMaintenance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptible")
    def preemptible(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preemptible"))

    @preemptible.setter
    def preemptible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a79a475f1f18353f40eb26cb547bec3d2b23a6d473dc179166d96abfe07984d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningModel")
    def provisioning_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningModel"))

    @provisioning_model.setter
    def provisioning_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19436c1ad985c617eeac8279145e696a0e79cc08d60b08edbe564cda0d1b7ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationTime")
    def termination_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminationTime"))

    @termination_time.setter
    def termination_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f1bea2a72e902fa64d4594ca254d62c271cf215949bebfc313525af03117c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateScheduling]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateScheduling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f322283c9fde8630b7b11de7af446e08889a276986ed70f45e9798fca0a8350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"scopes": "scopes", "email": "email"},
)
class ComputeRegionInstanceTemplateServiceAccount:
    def __init__(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported. To allow full access to all Cloud APIs, use the cloud-platform scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scopes ComputeRegionInstanceTemplate#scopes}
        :param email: The service account e-mail address. If not given, the default Google Compute Engine service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#email ComputeRegionInstanceTemplate#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c73719ec5cd641d64ad8325c68881a2e7b0838afdb24b41e872c45fb98257a0)
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scopes": scopes,
        }
        if email is not None:
            self._values["email"] = email

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''A list of service scopes.

        Both OAuth2 URLs and gcloud short names are supported. To allow full access to all Cloud APIs, use the cloud-platform scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#scopes ComputeRegionInstanceTemplate#scopes}
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The service account e-mail address. If not given, the default Google Compute Engine service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#email ComputeRegionInstanceTemplate#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1ac51423c4d4d54a2c0b8fd62fbe9a94744418083ddb1496d101d5ecf88f83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df485fa5f296d277dbdb6fd973f2edaf6d2b116b3295e4188fc5365dde61da26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511f193be1b962734bdc5f0a99e8ca878cdfcacb9d0cbbe2d98d9908d272861a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateServiceAccount]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3adff3f6813f8e188f31e59c9c49137883f97e34b4c0096427d695ad2ed6bd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class ComputeRegionInstanceTemplateShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results depending on whether they match or not. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_integrity_monitoring ComputeRegionInstanceTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Verify the digital signature of all boot components, and halt the boot process if signature verification fails. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_secure_boot ComputeRegionInstanceTemplate#enable_secure_boot}
        :param enable_vtpm: Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_vtpm ComputeRegionInstanceTemplate#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f9c1a533ab60ce9334a1f153c221617ae7b142ed1c82a55564981b7faa0bc5)
            check_type(argname="argument enable_integrity_monitoring", value=enable_integrity_monitoring, expected_type=type_hints["enable_integrity_monitoring"])
            check_type(argname="argument enable_secure_boot", value=enable_secure_boot, expected_type=type_hints["enable_secure_boot"])
            check_type(argname="argument enable_vtpm", value=enable_vtpm, expected_type=type_hints["enable_vtpm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_integrity_monitoring is not None:
            self._values["enable_integrity_monitoring"] = enable_integrity_monitoring
        if enable_secure_boot is not None:
            self._values["enable_secure_boot"] = enable_secure_boot
        if enable_vtpm is not None:
            self._values["enable_vtpm"] = enable_vtpm

    @builtins.property
    def enable_integrity_monitoring(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results depending on whether they match or not.

        Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_integrity_monitoring ComputeRegionInstanceTemplate#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verify the digital signature of all boot components, and halt the boot process if signature verification fails.

        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_secure_boot ComputeRegionInstanceTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates.

        Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#enable_vtpm ComputeRegionInstanceTemplate#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__602d49a23a8aeee029dec18e3ceaa7e832ada3d2c0b0bad0de490021604eea34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableIntegrityMonitoring")
    def reset_enable_integrity_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIntegrityMonitoring", []))

    @jsii.member(jsii_name="resetEnableSecureBoot")
    def reset_enable_secure_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecureBoot", []))

    @jsii.member(jsii_name="resetEnableVtpm")
    def reset_enable_vtpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableVtpm", []))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoringInput")
    def enable_integrity_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIntegrityMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecureBootInput")
    def enable_secure_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecureBootInput"))

    @builtins.property
    @jsii.member(jsii_name="enableVtpmInput")
    def enable_vtpm_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableVtpmInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIntegrityMonitoring")
    def enable_integrity_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIntegrityMonitoring"))

    @enable_integrity_monitoring.setter
    def enable_integrity_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976451937bfddcf78f924d19eec8322beb8282361627e0e5edf3c9d259fb2964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIntegrityMonitoring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecureBoot")
    def enable_secure_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecureBoot"))

    @enable_secure_boot.setter
    def enable_secure_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d085715b6a3eece5b1d3ab72d08804ea9517c4d494289f60eec553464ff1f2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecureBoot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableVtpm")
    def enable_vtpm(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableVtpm"))

    @enable_vtpm.setter
    def enable_vtpm(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2ca9d8b824b269fc1804598e6035bd22d2a36386acfa358beb7c65f1c6ec6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionInstanceTemplateShieldedInstanceConfig]:
        return typing.cast(typing.Optional[ComputeRegionInstanceTemplateShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionInstanceTemplateShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d1cf0f55361547edbc1b838ed9a9a073722893cf9ca590048e17075885ad27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeRegionInstanceTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#create ComputeRegionInstanceTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#delete ComputeRegionInstanceTemplate#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ea3618f9e1d311b43a42b04a6227aa1b09d8796ecff682795b2dee29ad7cd3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#create ComputeRegionInstanceTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_instance_template#delete ComputeRegionInstanceTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionInstanceTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionInstanceTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionInstanceTemplate.ComputeRegionInstanceTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d19e8cfceac1a586d3d881566e26cf01b975494baeadae25bb76845d65c8df9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f470cb5cca1d76b92da5dbab337515929786ee64c3a3c3665bc4dc38db15a8be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa39111c246a381639e1ca78e8b3749a13948f33145655040f2be317bab34ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f667ec5257dc6eadad06d55d6521622c6fb8966c89d59e9679f878bc2e8663e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionInstanceTemplate",
    "ComputeRegionInstanceTemplateAdvancedMachineFeatures",
    "ComputeRegionInstanceTemplateAdvancedMachineFeaturesOutputReference",
    "ComputeRegionInstanceTemplateConfidentialInstanceConfig",
    "ComputeRegionInstanceTemplateConfidentialInstanceConfigOutputReference",
    "ComputeRegionInstanceTemplateConfig",
    "ComputeRegionInstanceTemplateDisk",
    "ComputeRegionInstanceTemplateDiskDiskEncryptionKey",
    "ComputeRegionInstanceTemplateDiskDiskEncryptionKeyOutputReference",
    "ComputeRegionInstanceTemplateDiskList",
    "ComputeRegionInstanceTemplateDiskOutputReference",
    "ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey",
    "ComputeRegionInstanceTemplateDiskSourceImageEncryptionKeyOutputReference",
    "ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey",
    "ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference",
    "ComputeRegionInstanceTemplateGuestAccelerator",
    "ComputeRegionInstanceTemplateGuestAcceleratorList",
    "ComputeRegionInstanceTemplateGuestAcceleratorOutputReference",
    "ComputeRegionInstanceTemplateNetworkInterface",
    "ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig",
    "ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigList",
    "ComputeRegionInstanceTemplateNetworkInterfaceAccessConfigOutputReference",
    "ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange",
    "ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeList",
    "ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference",
    "ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig",
    "ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigList",
    "ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
    "ComputeRegionInstanceTemplateNetworkInterfaceList",
    "ComputeRegionInstanceTemplateNetworkInterfaceOutputReference",
    "ComputeRegionInstanceTemplateNetworkPerformanceConfig",
    "ComputeRegionInstanceTemplateNetworkPerformanceConfigOutputReference",
    "ComputeRegionInstanceTemplateReservationAffinity",
    "ComputeRegionInstanceTemplateReservationAffinityOutputReference",
    "ComputeRegionInstanceTemplateReservationAffinitySpecificReservation",
    "ComputeRegionInstanceTemplateReservationAffinitySpecificReservationOutputReference",
    "ComputeRegionInstanceTemplateScheduling",
    "ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout",
    "ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList",
    "ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
    "ComputeRegionInstanceTemplateSchedulingMaxRunDuration",
    "ComputeRegionInstanceTemplateSchedulingMaxRunDurationOutputReference",
    "ComputeRegionInstanceTemplateSchedulingNodeAffinities",
    "ComputeRegionInstanceTemplateSchedulingNodeAffinitiesList",
    "ComputeRegionInstanceTemplateSchedulingNodeAffinitiesOutputReference",
    "ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction",
    "ComputeRegionInstanceTemplateSchedulingOnInstanceStopActionOutputReference",
    "ComputeRegionInstanceTemplateSchedulingOutputReference",
    "ComputeRegionInstanceTemplateServiceAccount",
    "ComputeRegionInstanceTemplateServiceAccountOutputReference",
    "ComputeRegionInstanceTemplateShieldedInstanceConfig",
    "ComputeRegionInstanceTemplateShieldedInstanceConfigOutputReference",
    "ComputeRegionInstanceTemplateTimeouts",
    "ComputeRegionInstanceTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7206550734101103d8e516e6465ed5ebe178aca992c3a28580a63b6980299c94(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
    machine_type: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeRegionInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_description: typing.Optional[builtins.str] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeRegionInstanceTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeRegionInstanceTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[typing.Union[ComputeRegionInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionInstanceTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2ab28cfbfdc89b04e594a2d3a44048a8e8db1deb9da74d07eca219ed46bc69fd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0a2e36c89107545c9064bcaa79e5dff93a7a613e2eed7a26c8395afeac9d3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7292fee0a8bff6381def2143ae2e1647ff59905015fb41d209ab148e91c2baf6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cda5125c9d96b2fb655dcd9c958171a2b68c6ba81eb90abe9e4b388fde80e75(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c025e05e24fd7f3f5c11d3c66985cfa7058b2b062288ba016197452d26b9c4db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274c8c78d9581ef50a8cc43016cbd8078dd8973ae153c137d71dccdc6c505751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a20458b7908ce626f63fe02690b4471c68a40795acf1f5dc81ea2a9cefb954f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0402d723ac239114af8c6b3fcfd39969c3473784fe1f27765e954a638ada02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2e8087c21750e47b83e79ea5a95df67ada5d2bcdf544d6a9564f481b40f87c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8955ba13134c46beb2f3674c7669e8d6fa665e76e5db4745562639b1e4d4cc7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef91bcfc176e0375b3243949a37a956941cc010dcd73e55102d7ee26df169f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9b6102f274dde904da779bf583204cf4ab9d7b6b0fa67b989a1079e5f5f655(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a921830f7f1846fd1ead92b0f4b2372bf432e10084ecb1648a8bd7e26ecb91ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282a3ad51303ee003b4e8a4cec5733478473d4f8a05a165a80fe5fd3df020042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4032ece98a12856b57c7a74349bd4683b8a05311752d0551cd718b483174e64b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e82ab46021708a0f04dcd99d314a478b7ce4eba8c5db880fbdd267151de9e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc37859b2cce5078cdf0ac44ed67e590468b0392514ffc8198caa6aa5bdb0406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6051616b57d625e3dfe8cbafba35df0c4e2bfd2f8d6a3ad891ae21330812727e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5226c52212a903c22d3e7b5ede21c4de91f8a4ae34fc7e30f1bf92a941f68c93(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9f76c32e9253fedf8b8e6ce43fd710e4192780ab854205c108aa0ad661eded(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e8554908e7cfe1506febb4e8ce457c93bbdfdabd96c4d7f6fbe973338d0105(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205721e59d09ac1746ec1c8a9bd6ec504440f423adf843657a73de87f22374b0(
    *,
    enable_nested_virtualization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_uefi_networking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    performance_monitoring_unit: typing.Optional[builtins.str] = None,
    threads_per_core: typing.Optional[jsii.Number] = None,
    turbo_mode: typing.Optional[builtins.str] = None,
    visible_core_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bb71951439a863305f9414f02ce3fc921976d35034271dfde3bf57e655401b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32b7c8dcc3dcd8a33b16e9049ade50af6ab092aeb56134ab8d1ad4ddf18d421e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a719b9bff3f93c925fba3b6da80553a72059bbb62dc0a3762b7ef08b19d744a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43663047cae15fca86ea3a404cc60dc97c2bf1c9a82c33d9d8249c424f1e07b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dfb9ff2b98ed34f1941ff322b2800ac31a9d52e628225d1f69cbf7ed328f0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58bde152e7f8c015fd88f473b2abd34db891dad6044a71bb64b4eadb2104114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3404983d8d08e3e7116e393a6ff907fad43d2a6a106de4b687ceb49ab64bd60d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242e38580e88205402d93d9bd9bcda9659d870f71259181701daaa265fac992a(
    value: typing.Optional[ComputeRegionInstanceTemplateAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504f8a052222427e535978b529aadbfc7db7f3ae8b0d83f271651dd1ff481acc(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc1c4517771a5e3c86d1d07e5f4a6bb515c173af06a5b924f0c81d0e12566e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430c809a27cf6f1de21c378ad10de053da29f11664f159af93ae84a357fb8b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e9133a02b3bdc262cc5f70ef7e197ba6e51af475a7f5e80337cc9d7a0f9810(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a0f4e976eb2406dcb33956abf6c120bf9bc77512b926c493a542e92c3f6639(
    value: typing.Optional[ComputeRegionInstanceTemplateConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c14404ed8faaaae7cd844af0b3cd5e863c74fd64a3830b43b202235f35a32b6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
    machine_type: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeRegionInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_description: typing.Optional[builtins.str] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeRegionInstanceTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeRegionInstanceTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[typing.Union[ComputeRegionInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeRegionInstanceTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionInstanceTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df580be0920b4c6eaa713627e5c2b5ace2d0a9b2e71672df03f1be10fed9aecd(
    *,
    architecture: typing.Optional[builtins.str] = None,
    auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_name: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeRegionInstanceTemplateDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_name: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    disk_type: typing.Optional[builtins.str] = None,
    guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    interface: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    mode: typing.Optional[builtins.str] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    source_image: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2eb76572b04906d75153a3d00a1ddd60a668c5e780d461da92ee9e82a0d292(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f52281d18bf86fde32cd3405e12eda1f4e60f443923860246bcdc8a045bedf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a633adfb380fc4f832f724d79a8aed12692b4f96f8b795d3c99722ee145c08c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367229d3cdc18f7e0a58ac4c73c76c228764b85b561cd94bb87f8ec3b569062c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbd2d737419e43ce667448c609e55f606e0e58e01ba2c916817774ee51ebef5(
    value: typing.Optional[ComputeRegionInstanceTemplateDiskDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7482e04853e2d596be8fe37305bdc6f2b38571006a94dd945106f4ab3d33941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf2997cf4adba035354e27363f720a7a720498f500cccc5d1119fe1e16613fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b88f47401ea2402c2208601414aef5ee467d5d91bc4950e89092cd746c22fb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb35e261be95cfbc804b2629da94ef6ad1c7975fad040cb1d70a618cfccc0c03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee072bf4de9367934e8b3f8b86195b15c746ddaf38ddad10c6635a1faccee524(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3eeef0971834583203d7b35537a50be97e3e0d12db75810af686eb0d1220c38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db500087e726ec69bf705ccc6798dc4bf4461d0395e0fcf69b4ff37992aba192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4ad49165b62fc445658bfa41fffbe180cb3245307b7791afd3664687231822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7f4a089b2b8aadbd49efed6e11bc0b72be02203604d5b2e4018277dc7cb257(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b979d1f14854ec5086085a9ec95794d207ba2c9366b572f51ae5589c2f5e41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2218002caa20ac21913d5e01cdf41d7c8d9cc5f08980a4c35f5c9b09fbb0cf4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b316c7bf04d7a8256628a3446be186c215336afbd67ee25a714961bc9a7c272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f775c055275c43be2f612c5fce8df6e2496f4078f7ab4ae1d9e7b397aa7540(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7927280627567a944e844164cd444e266e38c319100e87d78e2f71ec2c1313(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d6b7ab966745f52de0c921489d2969d776066d4a09529f6a260a5b2ed2d129(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486ce274b703cd1d9df543c89376dd6eb1bb3e185c12cc3ed7aae3db6ab76d34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea5530206af349503bc256274882ec0ef5b576282c93feca2ad188b2355b7eb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09186475935a5b595757b42a7c3f8bae65acc20d8cd75868348218ea817595d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6a9931c96d4b653a3b3aea77b6a532f5f4b5bc85e61d265e772d421036aaa9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f8ef167c116c1f40607a46ee5edcec875b686da7f0aed734cb88a51567b210(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d86a35d47d58ab3fba229bb333ea0cd84621007ee39dde2507717b34ea26b7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d7ee4fc5bbc5b279e3e450445180f758e06ed8cd65600a4fee3e2bf57b2a6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c4059a2c6eb0f733ed0dcec480d0f0297274be0ddbea0d30e22744e205f391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0b95700b61af275c0dab302c55b6ba0882c5381772405dc175c1ee357a7c06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df98d6a1c6623699ba1c4500f360578a2be9bc624790347de1793363b50965d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e94a79afb9e1567be43bae44ad06325f29f62550adb866d2f29bb0fc4687d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cb2c30395ca65b2a423551bf043a9355857a71f6c93104f8bd3be344220fc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56afd9f8b9375e0999ff9c51bacc07ac6071e10b4da504b04b314c578bc4bf2b(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6656d1b1e9c908d815a94490c70c790092da43db64d95f5aedc31bf75fc098(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b6c3e4b4397dfc91406f720b048c5616413e08f304710074081ba82b26c7bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8888b3b110d449df7991661c764adc06853ea9c930bae69187ccfc4bb523d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04035a233ab7f7fc9248b78552aaba396a866b93dbbc9455b18c14dcc770242(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcbb4ca3191e374ab69cf8f0df1d914a535c9f1f6528ea40bce5d0615740a8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34426a9d0f39ff096dd6a4d6e648e6b2665bd7e7871b5726abf0cf43ff213aa(
    value: typing.Optional[ComputeRegionInstanceTemplateDiskSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8648925bb34f0dd2631ff1446f13786e9181738bc35b250555714bc1e53acf69(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2ef27221280a2a10bbe0d670367da90b563329f3aa9f6f16b4da7cff20d491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48af2ff54bb54dac0f4bd27033df5c24bc89e62da49582e681972a27a8b9006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9945ccf055b53cca22be59f8da74eb2fd4da7e6ad68be3d97bf321d19f630233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c35da9688952ee9bcad988133e028f1d8434ad33c7455a3f7db6d5a4a5b4bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcdfa327c8de4d4222634f3c6ebe2a8b086564fcf2dac96d629a5c260681ab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f14f88e6d0e6652fe41a48864788c379aa8656b8a718b755144c4ea9c2a266a(
    value: typing.Optional[ComputeRegionInstanceTemplateDiskSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b40538bc453fee6fb2298262d78b19f03d524cc038151a80ac177109106265(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f745e9f3edc3bee4fe5a2842db6545e40e33c6501a3a7fb0b26a4b803a94ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60728f9476bffce0ffc57454af997340c7c8bf68248250bc884702eee363e62f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654675290658ad13f8c11c292e634826b29ef0a1f372077a9f81dcb1492747e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b248f4cc2ec16c23af5637240af986919be33ea062c18334ff3dead57527248(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bcd63d0ddc387409dddc0273a6b182ecc7afd08728c6168503a90ab70c9fbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46755f45568f0615d83600e885c27a5265559ccf2bd193cf9a9adf916395bdf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fd7f2a0cb1d56595be81566d81ec9d2b7bd2fb458bddb06d8519a26ccde788(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823a60917e7ce8387b89aed7f45d5bea2a46bb800daabae2f60d016927e8aca4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0215aa04bd1102644cdecb33b5664d626cd50ee8eaf09ced33bc4c40e81fbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3a38a24c7fb3d5542ab93a27b1fc5106cf130b4eb6a52a6b87ff8fcd4b6886(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20acf50197e08084b1fcdf6345c7ffd17bcc2ab246f950b5e98e8208c92ed17(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
    ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ipv6_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_ip: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    queue_count: typing.Optional[jsii.Number] = None,
    stack_type: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    subnetwork_project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6389f44f4cfd43ab07ea747aba3503adbefbd4fd2affd468fa4bfe9509653e4a(
    *,
    nat_ip: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14bd58d293154583879338805f6968bb7c5c44e0ab8f2a7d9c8e6945072be34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1144a35b0f627a485f733f4b77cefc5ea8d82adb41dd8775f60383deef1855(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b7222d08cb52bb249641de82b17c30dc63598991c1b7f476db62ac57a401e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab586a81d2ee7217142acc1fe60f10d609738b52d1f92f6a4eb947291bcf435(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5415d38fd92b0341e367fe945d0138b4fac25d9f2de6ef26fcf227495c9f6417(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca17b5b27acdc2fbeee345fb10f25267700a48e4371104a2a014f2cc5d9cde9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b082a18f4167594d878a007e2b645046e893c9d0d487e979ae6f402bd36605f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180e73368e3ae2a5be499bffa5bdcdace1153946fba628adcbf2228d1e1fe102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cae29a8fa783f085737915decf5b457a5508afec68407e3e2cbecfe16cb916f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dbddf07aba916aa879bbcd94b4c519928479d5126c2dca3fd2aee7b108cb536(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a70f7af2a994fd21216f8f2e7a265c9d578651b8779b3389eff81b4dd23bc6(
    *,
    ip_cidr_range: builtins.str,
    subnetwork_range_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95470d3d85d827a5cb332f41151f2a211c0b6e291cd7eec191484754c1c216b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1070b5270b30e4a04731b3993a103b340e6e98d4e517b2682324daec86568987(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d67d692fc9189ec6cf68bb832b2ef2e081da58cd9f3748b4b6730033d8f5741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e24f1fed1aa617a54cf630afc82410c38f390eef7875cb8ac866be394e12e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca39752a445cb12fb5cf2ad943ad8cfb886b4d099efbaf71216cb5f546c3afb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50197a193a3bc25cfab5cd0b1df330c82dc1c6eb18410047b80a8ec5e9b74a5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b7c4689649b3ec9ba417e3f88e6f2efac3763db2a10962c75f26c25f974284(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a4a5e97a2db120ff1a19bd36c6e167c3bd8dd4c0f98df0bf7fae6cdecbb44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd740958ec4583f02e1f913e14a0e4fd8058e990032ba2f9d4139185b16bca4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cc4512b1367e619467daf06c39cac8b97de05d141962f4bedccb0e91383250(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c69c80ccbd00b2a85e0aa0348f9ba804df23cc4f93d9d9dd608dd486615ac74(
    *,
    network_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b409a85850bee4c9bc4ecada9829cae14c1915172c445abf31d8b16ad1629ac6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85ea6809a74aba9a11d1422f163c7672c20864a22e82b17c9a8a689eed010c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ab93c0f54308778f4ab639af315222733d1b2091e72efb87d9537a6c9f7639(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b378681e7c5810bcb45725043877cb287fa705b26c1c4d8f6205b8e8c1a601(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161cbff1e5b872dbee5394dd81acc16f05e06739d841fad2f3abbddea3bb226b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43af3ff292f0d4f90b4c33d91d3aa986a22fb30644519f64d1a703d0305013e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db3971b83be6341580ac02a98f6d51d43b295d18c820517e81896616d87b8f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466fa2d1c3761c86e1ab634ebc1b34a2f0d437b2533bddb75018f9d86150e8da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7296c0a6e5ce52d79228cedf0b5c652b5bdf1cde8f41707ea6e755b06d82465(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf3c811ed6363a1f9769a3f92c021c175cde97ace5d96500c2ee2fa09ff7288(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6211c2823dd379327a5bb8a47e5effdf2e76f60e32e713cac888a8751c98fe78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c7c5fc731cd42ec9ca510a13bf0dfddf8bb5b932a94dfd4a9d159064a1a90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74dc830f2fde63c49b539c6b9b9d5209c87d9d731019c19b12108f8bff70a39(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62df8b6f5d9f6766bb71b0cbf1c8d3bc7b0c6d32f532c77d0230938f9b567982(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65c23337d503f9a52bc3f3682f53eda6093db23bbaf2e269b8dc02a34bc48fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418f36cee811072c38c28a73daefebd334daa5e634cb9a6fdc3f5684c52d2c6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a998049bb8ec88e9e9bb61e0ff426557455e910d1ae95da4fb80f4431598c44(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6406192a33f7135fcdd2a28103e7c091dcae5cbd7dfa2e8ed23b0ba5fcb48d3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe5caadc4cf3b539835ba07112d82eeabac803c7a6de6929ad93460d9e4b2b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3d8bad98a709edfd1a336d28b18ecb0a751c736a2c0b70719c287c163cb2c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4340407b3c5347d173c63506a2a04c851d4af05250e5850b2108ee77984181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2f4381bfec74eadc0a7c0737206fde7ff8097e1e628da135bd6cc57110d72e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484d29a4b9025d8260e64e511772d1a4f740e903f8c33aa492e99a0b90313d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccf5af6d942043bedc8bc3f5946f156388ee814576c5835620e479a1ad65cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a9fe541868b603cedfaf4bf90688b144deb51ff9222aa79633a95e6785c9b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f3f9efe1dc5d079071e57a77b4e283479d15e9e5ece20e33b5a84dcf96a01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaa30a5b47863ce1a9ab2efcb9fb6ce41b1b11805160f79791aeef9042c08da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c5d670d863c80d8d45f84e935bdda7992a1bbf2505897e96face900201e4ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8941e9d6026f7fe48c3c77657695267677d1298b1f17fa2ebf02f50d4fe1ae15(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23726e485ebf34581683bbabd8aae17a71967c2989e3b72d463e4b43a734593(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62685a3a28b0d3cb7c82bfd4f4d8ceefff0b3df140f0a3e8867b577c2b1d14a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75043a4de6d256aace2b64680fad351e2c9887fb539a0484894f931cf14dcaa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93715f928a54992e4fa9d4c933efd051966731606dfa0938987fafbf523a30f9(
    value: typing.Optional[ComputeRegionInstanceTemplateNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3562df6c1482d43c12f771e68fe9f49a8441b692d6f309aac36f2d17b6e479(
    *,
    type: builtins.str,
    specific_reservation: typing.Optional[typing.Union[ComputeRegionInstanceTemplateReservationAffinitySpecificReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a242e607ec677305593f4d58079a27e6091233d7a17873eedd1980f16862ac21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a71d03c8fd37f15c75fb63bfd18c4038b9a487df52d79fd74989d16cf63362c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2767c27ab211ab0a2f6e19e482afbe169f2814472a0c53216d0988f1f42b55b3(
    value: typing.Optional[ComputeRegionInstanceTemplateReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2664c9ebbefe56fd20c6b04f2f12f03176aaa282689edd2fbb4eb7d11ccf7f94(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323ed799fd45ed4ceb0b69a9f74d7c77aa49b86f64d90567280aab2d5854cc3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035f5954cf43ee926c4138214713ff44254cef625a7bcd419c3e629696236846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5690a8d625460b3db5cb15d5432f96406e7122cd0706563b17b78efda15b815(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a66ff57543392a7f32b44cb34868be5d411a54f6fd770c7f1fec00a7ea6237(
    value: typing.Optional[ComputeRegionInstanceTemplateReservationAffinitySpecificReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6968cd1a47d00d9f58148373c53d808f94f90b2b9a9426fd1040405b81e724fd(
    *,
    automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_domain: typing.Optional[jsii.Number] = None,
    instance_termination_action: typing.Optional[builtins.str] = None,
    local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_run_duration: typing.Optional[typing.Union[ComputeRegionInstanceTemplateSchedulingMaxRunDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_node_cpus: typing.Optional[jsii.Number] = None,
    node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on_host_maintenance: typing.Optional[builtins.str] = None,
    on_instance_stop_action: typing.Optional[typing.Union[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_model: typing.Optional[builtins.str] = None,
    termination_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8092087c0a309b93051bef974d571f1cf1a86aab6860acb67848787e2f1ed3a(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885f5956cb5d85a7d7f77fdfd9881260d9ff8f3a8277bddfb8169cb55d0e1492(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8adbb88679c778ef219d8bad535eab1ac7df3f2ff744a13fa6935f55f5cb1790(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc95a8b9bc82de12e24c963d0250e71d106a6195f600c43e96e32c61fa26cdfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d35053acc9fd70a5cb0b17efc4dbdf6dc79b2d7630fe149a2e50717b924c17c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266ddb11cd875bd2b3af4381106c21c13ceee72ab91c61754f0cc316e5565677(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6788cd1bcac85c40bc39906ca12f94239310fef7cd4008b17242453e9fe8cd0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19028d3e85fa0c0ffc088517543568cef7f0837c0c68a90ffdf5fb54c9713fa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e0172db219b906ff53a45899739ec7cca38dcb18aa309c059006ad56a5fe36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd9252e3854dad4e8aec2cb7f46590566ed42cbc17c36c85b395427bbe84e45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5c62645d95372f2dc891b595345f8c64c426fcedc587569a4f49e2caf010be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b342c7a6019c6bcf5599d634cf7f3dc54b14ff48187485044dfd0bb243f0bd(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f6d51ced65fdf53776745b27c86d0e8626a908e71c4f537f5d90f40915b77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebbd640e21628d8238900398c9a7f4cb261c8da9a94213b09193337d79a1a54(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c44ae4bb2dd60bb4d996e88e4bda6141946e5926fc090ad8aae276ca3258ac8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae22b1f4c1108ac3a786dafd63c444709ac662761c3810a4eb387f63063b004(
    value: typing.Optional[ComputeRegionInstanceTemplateSchedulingMaxRunDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f61063cdc08d0de04d8c96dad9712624850a8c904801a8ab4181258316bedb5(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bef5d291bbad800fe3bc36042ea91557a1310cbf6eb75f4b7b1e8e6346fa37b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91936eac7f89a4661a23c4c3f3b16086212b79a713733255cf55b75090f33b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949dd40e63f2645cc667e2d401fa20bac7d98e52243f47327c99fd6dc5944ac5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24021a2bce07063743ca924b0f41fa7a32e4e603da26b3d2fca03777f1642b0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcf5fbe5a8acba3129c1f84878195adb37c9dcc384046c98ec196b319b29686(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315a2e675a1dcbb6974a980ddb6dc82e1bac6bc7e744c66ccbac1e349bc38b35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionInstanceTemplateSchedulingNodeAffinities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8217602aba3380278729f680e1ad23bf40f11f5e68718f550aa326e02ad812cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dac1f64cbe07a510b9951d76a7ad09dcbd79f62a3fdaf684bad84cc9a1b660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd7ba449beeb98eeeed378bdce5f824dd10df48a143623a4d100ab20d0ced61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56de3a1efb88b00930ddc02eb63b264d22745015ac271f6a1413f1ef89bc1db5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1867c3690e60e216417fe3670acee2585486157e147992ce3291b13bfe8244d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateSchedulingNodeAffinities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad2a8d7b906c9ab22961e1dacbe2c54e644704075adcc5eac15dc0179ddc825(
    *,
    discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ad8588e2308f0967cc23a3c62af3fed8400336540957cfeddd1ace68bc1b98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e41f50fc0be198df26c3620c55980f59f53071ca2adc350e0cf3ca858ccaa77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79a0b833deefb579f795b66551e5d4411b01620259b7a8ce4830ba05607a016(
    value: typing.Optional[ComputeRegionInstanceTemplateSchedulingOnInstanceStopAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cca6092733539a78e1d59ff3f3017f46ab7e38de83880b468dbcd9ac208fddb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4b8af6afd85b8c3a48a26004d429ecf7c9d4a15bb3976235195d9b058e63d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4f168f14ff79c180a3a6c2b35489879803822d83fe508c44c8352db2429918(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752939b87e267cd1103100b1a9217a02c2c886c6b0c5eb9defd2267af178b493(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436cc1099eeee5497c2150e3a7da1be3e00cad3927764e06a6b2bc47e8e4a20e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef080eec92ac3d39657b5adf1ca3c89846fb10a61adce5a5a79f1dd7626164a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77d498b6b03296d4df8fa92e382ff1880ad554bd42324f53c3ed9d08e1c6a9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6a63862a17be87989d22eb4dae4fe807b980767f58c4b99c7675d51f3c8243(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a79a475f1f18353f40eb26cb547bec3d2b23a6d473dc179166d96abfe07984d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19436c1ad985c617eeac8279145e696a0e79cc08d60b08edbe564cda0d1b7ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f1bea2a72e902fa64d4594ca254d62c271cf215949bebfc313525af03117c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f322283c9fde8630b7b11de7af446e08889a276986ed70f45e9798fca0a8350(
    value: typing.Optional[ComputeRegionInstanceTemplateScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c73719ec5cd641d64ad8325c68881a2e7b0838afdb24b41e872c45fb98257a0(
    *,
    scopes: typing.Sequence[builtins.str],
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1ac51423c4d4d54a2c0b8fd62fbe9a94744418083ddb1496d101d5ecf88f83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df485fa5f296d277dbdb6fd973f2edaf6d2b116b3295e4188fc5365dde61da26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511f193be1b962734bdc5f0a99e8ca878cdfcacb9d0cbbe2d98d9908d272861a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3adff3f6813f8e188f31e59c9c49137883f97e34b4c0096427d695ad2ed6bd0d(
    value: typing.Optional[ComputeRegionInstanceTemplateServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f9c1a533ab60ce9334a1f153c221617ae7b142ed1c82a55564981b7faa0bc5(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602d49a23a8aeee029dec18e3ceaa7e832ada3d2c0b0bad0de490021604eea34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976451937bfddcf78f924d19eec8322beb8282361627e0e5edf3c9d259fb2964(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d085715b6a3eece5b1d3ab72d08804ea9517c4d494289f60eec553464ff1f2ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2ca9d8b824b269fc1804598e6035bd22d2a36386acfa358beb7c65f1c6ec6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d1cf0f55361547edbc1b838ed9a9a073722893cf9ca590048e17075885ad27(
    value: typing.Optional[ComputeRegionInstanceTemplateShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ea3618f9e1d311b43a42b04a6227aa1b09d8796ecff682795b2dee29ad7cd3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19e8cfceac1a586d3d881566e26cf01b975494baeadae25bb76845d65c8df9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f470cb5cca1d76b92da5dbab337515929786ee64c3a3c3665bc4dc38db15a8be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa39111c246a381639e1ca78e8b3749a13948f33145655040f2be317bab34ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f667ec5257dc6eadad06d55d6521622c6fb8966c89d59e9679f878bc2e8663e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionInstanceTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

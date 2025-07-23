r'''
# `google_compute_instance_template`

Refer to the Terraform Registry for docs: [`google_compute_instance_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template).
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


class ComputeInstanceTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template google_compute_instance_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
        machine_type: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union["ComputeInstanceTemplateAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union["ComputeInstanceTemplateConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_description: typing.Optional[builtins.str] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template google_compute_instance_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk ComputeInstanceTemplate#disk}
        :param machine_type: The machine type to create. To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#machine_type ComputeInstanceTemplate#machine_type}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#advanced_machine_features ComputeInstanceTemplate#advanced_machine_features}
        :param can_ip_forward: Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#can_ip_forward ComputeInstanceTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_config ComputeInstanceTemplate#confidential_instance_config}
        :param description: A brief description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#description ComputeInstanceTemplate#description}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#guest_accelerator ComputeInstanceTemplate#guest_accelerator}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#id ComputeInstanceTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_description ComputeInstanceTemplate#instance_description}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key_revocation_action_type ComputeInstanceTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs to assign to instances created from this template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#labels ComputeInstanceTemplate#labels}
        :param metadata: Metadata key/value pairs to make available from within instances created from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata ComputeInstanceTemplate#metadata}
        :param metadata_startup_script: An alternative to using the startup-script metadata key, mostly to match the compute_instance resource. This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata_startup_script ComputeInstanceTemplate#metadata_startup_script}
        :param min_cpu_platform: Specifies a minimum CPU platform. Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_cpu_platform ComputeInstanceTemplate#min_cpu_platform}
        :param name: The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name ComputeInstanceTemplate#name}
        :param name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with name. Max length is 54 characters. Prefixes with lengths longer than 37 characters will use a shortened UUID that will be more prone to collisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name_prefix ComputeInstanceTemplate#name_prefix}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_interface ComputeInstanceTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_performance_config ComputeInstanceTemplate#network_performance_config}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#project ComputeInstanceTemplate#project}
        :param region: An instance template is a global resource that is not bound to a zone or a region. However, you can still specify some regional resources in an instance template, which restricts the template to the region where that resource resides. For example, a custom subnetwork resource is tied to a specific region. Defaults to the region of the Provider if no value is given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#region ComputeInstanceTemplate#region}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#reservation_affinity ComputeInstanceTemplate#reservation_affinity}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_manager_tags ComputeInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_policies ComputeInstanceTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scheduling ComputeInstanceTemplate#scheduling}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#service_account ComputeInstanceTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#shielded_instance_config ComputeInstanceTemplate#shielded_instance_config}
        :param tags: Tags to attach to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#tags ComputeInstanceTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#timeouts ComputeInstanceTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cf633252edc7ab3fae9af894664c0fd70d486a116066e8bba425f96aff04be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceTemplateConfig(
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
        '''Generates CDKTF code for importing a ComputeInstanceTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstanceTemplate to import.
        :param import_from_id: The id of the existing ComputeInstanceTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstanceTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b43db1c01a848636d281e00ca0b2cfe2d336c5cfd386fde9962b264f5b179ca)
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_nested_virtualization ComputeInstanceTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_uefi_networking ComputeInstanceTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#performance_monitoring_unit ComputeInstanceTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#threads_per_core ComputeInstanceTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#turbo_mode ComputeInstanceTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#visible_core_count ComputeInstanceTemplate#visible_core_count}
        '''
        value = ComputeInstanceTemplateAdvancedMachineFeatures(
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
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_type ComputeInstanceTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_confidential_compute ComputeInstanceTemplate#enable_confidential_compute}
        '''
        value = ComputeInstanceTemplateConfidentialInstanceConfig(
            confidential_instance_type=confidential_instance_type,
            enable_confidential_compute=enable_confidential_compute,
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putDisk")
    def put_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072ccc7f51ea680b80000af4a904ee236ada08af74f74c867a1ac28fbb40d817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisk", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b8d701ebbe44d7097463c9d19ed05749355ec02a26fb218483bb676e57134f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerator", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5c0d938e93386aaa24d5daf04844f9b1925d24a5836a2b81bab801ed3646ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#total_egress_bandwidth_tier ComputeInstanceTemplate#total_egress_bandwidth_tier}
        '''
        value = ComputeInstanceTemplateNetworkPerformanceConfig(
            total_egress_bandwidth_tier=total_egress_bandwidth_tier
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkPerformanceConfig", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#specific_reservation ComputeInstanceTemplate#specific_reservation}
        '''
        value = ComputeInstanceTemplateReservationAffinity(
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
        local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user). This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#automatic_restart ComputeInstanceTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#availability_domain ComputeInstanceTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_termination_action ComputeInstanceTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#local_ssd_recovery_timeout ComputeInstanceTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#max_run_duration ComputeInstanceTemplate#max_run_duration}
        :param min_node_cpus: Minimum number of cpus for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_node_cpus ComputeInstanceTemplate#min_node_cpus}
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#node_affinities ComputeInstanceTemplate#node_affinities}
        :param on_host_maintenance: Defines the maintenance behavior for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_host_maintenance ComputeInstanceTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_instance_stop_action ComputeInstanceTemplate#on_instance_stop_action}
        :param preemptible: Allows instance to be preempted. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#preemptible ComputeInstanceTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioning_model ComputeInstanceTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#termination_time ComputeInstanceTemplate#termination_time}
        '''
        value = ComputeInstanceTemplateScheduling(
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
        :param scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported. To allow full access to all Cloud APIs, use the cloud-platform scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scopes ComputeInstanceTemplate#scopes}
        :param email: The service account e-mail address. If not given, the default Google Compute Engine service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#email ComputeInstanceTemplate#email}
        '''
        value = ComputeInstanceTemplateServiceAccount(scopes=scopes, email=email)

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
        :param enable_integrity_monitoring: Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results depending on whether they match or not. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_integrity_monitoring ComputeInstanceTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Verify the digital signature of all boot components, and halt the boot process if signature verification fails. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_secure_boot ComputeInstanceTemplate#enable_secure_boot}
        :param enable_vtpm: Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_vtpm ComputeInstanceTemplate#enable_vtpm}
        '''
        value = ComputeInstanceTemplateShieldedInstanceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#create ComputeInstanceTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#delete ComputeInstanceTemplate#delete}.
        '''
        value = ComputeInstanceTemplateTimeouts(create=create, delete=delete)

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
    ) -> "ComputeInstanceTemplateAdvancedMachineFeaturesOutputReference":
        return typing.cast("ComputeInstanceTemplateAdvancedMachineFeaturesOutputReference", jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> "ComputeInstanceTemplateConfidentialInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceTemplateConfidentialInstanceConfigOutputReference", jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> "ComputeInstanceTemplateDiskList":
        return typing.cast("ComputeInstanceTemplateDiskList", jsii.get(self, "disk"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerator")
    def guest_accelerator(self) -> "ComputeInstanceTemplateGuestAcceleratorList":
        return typing.cast("ComputeInstanceTemplateGuestAcceleratorList", jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="metadataFingerprint")
    def metadata_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> "ComputeInstanceTemplateNetworkInterfaceList":
        return typing.cast("ComputeInstanceTemplateNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> "ComputeInstanceTemplateNetworkPerformanceConfigOutputReference":
        return typing.cast("ComputeInstanceTemplateNetworkPerformanceConfigOutputReference", jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="numericId")
    def numeric_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "numericId"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "ComputeInstanceTemplateReservationAffinityOutputReference":
        return typing.cast("ComputeInstanceTemplateReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "ComputeInstanceTemplateSchedulingOutputReference":
        return typing.cast("ComputeInstanceTemplateSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="selfLinkUnique")
    def self_link_unique(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLinkUnique"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> "ComputeInstanceTemplateServiceAccountOutputReference":
        return typing.cast("ComputeInstanceTemplateServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "ComputeInstanceTemplateShieldedInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceTemplateShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

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
    def timeouts(self) -> "ComputeInstanceTemplateTimeoutsOutputReference":
        return typing.cast("ComputeInstanceTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateAdvancedMachineFeatures"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateAdvancedMachineFeatures"], jsii.get(self, "advancedMachineFeaturesInput"))

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
    ) -> typing.Optional["ComputeInstanceTemplateConfidentialInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateConfidentialInstanceConfig"], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateDisk"]]], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorInput")
    def guest_accelerator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateGuestAccelerator"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateGuestAccelerator"]]], jsii.get(self, "guestAcceleratorInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfigInput")
    def network_performance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateNetworkPerformanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateNetworkPerformanceConfig"], jsii.get(self, "networkPerformanceConfigInput"))

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
    ) -> typing.Optional["ComputeInstanceTemplateReservationAffinity"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

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
    def scheduling_input(self) -> typing.Optional["ComputeInstanceTemplateScheduling"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateServiceAccount"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateServiceAccount"], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc151ebb13a9710ffbe557fa3834d3e628af9a1c280622fb2aba68c1bfc4b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canIpForward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef697f7fa599dfe803803a2f5f7f96548b6897d526b06045c8412f663c83dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650883a47d58ed99034082e149ad96fec228cdf1b56cfc2779129db57441a8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceDescription")
    def instance_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceDescription"))

    @instance_description.setter
    def instance_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b5853b2bbaec3502f30d952fe8bd15709e965a0575122a9cd5dde65fbc4fbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyRevocationActionType")
    def key_revocation_action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRevocationActionType"))

    @key_revocation_action_type.setter
    def key_revocation_action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e13fe2bda6c3c62ea83c5907488808032a0aa40014c04d82c80c92206093c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRevocationActionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc65f23d3670987771a364d017f9a653426039ef6cf158f4b1f13ad48f3150f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a3cc7d28b6ddda49ca61fd4ebd2c58093cb5e2b611abdf39155b31393be287)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b747b4ca3ca13dfaa1dfa8d13090e89e41bcaa9f68f15774c29b4caea88918d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataStartupScript")
    def metadata_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataStartupScript"))

    @metadata_startup_script.setter
    def metadata_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53c39d4f6e5a5d5f81135cb72bcf6c395ffe826c63ed8e3eb7164ac9803c22b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2ecf62c236c56a85e0c0c3312595650f14f5bf376e4c34a31d4b2d9df18be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631e9549ef7a7f31dae01c915569f2af60c3ff1ec0ea095c30b769313d970363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namePrefix")
    def name_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namePrefix"))

    @name_prefix.setter
    def name_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4389759d4597dc65be58cea810c3a64427fa0461c6a8dd7b521267f43779dcd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c18dd43ea9007f5684b63efbc2e3008a6f91460a86d92d420b0354018645d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3013e8768686cfd3341c46b8f2f15639caa1b20ecef4ae6f05196fd9b07b9465)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60f39a407507bb48f3803dd708e15205b7e9c515b5d47df1ab5bb45838cac24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2aad022a15a6cd4105bba551a120da15c8c9445c67a887e6e5aa8207780f59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28d8ada072df6af5f06c02361e3ae60221533f0c7946e9cab44d2d9dd53f173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateAdvancedMachineFeatures",
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
class ComputeInstanceTemplateAdvancedMachineFeatures:
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_nested_virtualization ComputeInstanceTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_uefi_networking ComputeInstanceTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#performance_monitoring_unit ComputeInstanceTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#threads_per_core ComputeInstanceTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#turbo_mode ComputeInstanceTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#visible_core_count ComputeInstanceTemplate#visible_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca98a0ca4fff4536f5554418144a6b0a4b38084e9a15a11dce3220826eab6b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_nested_virtualization ComputeInstanceTemplate#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_uefi_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable UEFI networking or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_uefi_networking ComputeInstanceTemplate#enable_uefi_networking}
        '''
        result = self._values.get("enable_uefi_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_monitoring_unit(self) -> typing.Optional[builtins.str]:
        '''The PMU is a hardware component within the CPU core that monitors how the processor runs code.

        Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#performance_monitoring_unit ComputeInstanceTemplate#performance_monitoring_unit}
        '''
        result = self._values.get("performance_monitoring_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#threads_per_core ComputeInstanceTemplate#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def turbo_mode(self) -> typing.Optional[builtins.str]:
        '''Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#turbo_mode ComputeInstanceTemplate#turbo_mode}
        '''
        result = self._values.get("turbo_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visible_core_count(self) -> typing.Optional[jsii.Number]:
        '''The number of physical cores to expose to an instance.

        Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#visible_core_count ComputeInstanceTemplate#visible_core_count}
        '''
        result = self._values.get("visible_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eabf1d9ec90083b9fb6dd8a5e27bf1c48285a76125182d46015f39b72e7b1e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83c4c8073883f547652290099f8c67e96486f9f67aad7e31f785eac5391d92b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0aabdadd0acb3f541cb80689167d30d30c9acf1ffd78f4b824824012fc28027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUefiNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnit")
    def performance_monitoring_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceMonitoringUnit"))

    @performance_monitoring_unit.setter
    def performance_monitoring_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86db4332e0425f156ac49ec7a29e5078470c803a9fd351d20d28713aeae979eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMonitoringUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9b89cb5d5bc46a696d67a67df327a5a74a69b631907c636920f35ab310cada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="turboMode")
    def turbo_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "turboMode"))

    @turbo_mode.setter
    def turbo_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48f63c46e64599df23de50c9efef680c42e7f70da7c6a34a96ac8deb14d812a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "turboMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibleCoreCount")
    def visible_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "visibleCoreCount"))

    @visible_core_count.setter
    def visible_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e251b385367725e2116cf6538f673dd3b9a23ae9f977609c5c1e102080f6706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibleCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8feb9893299e8fb072a42f3fdc2a697d325eb809857d3f1ccada9d8b8dd1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidential_instance_type": "confidentialInstanceType",
        "enable_confidential_compute": "enableConfidentialCompute",
    },
)
class ComputeInstanceTemplateConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_type ComputeInstanceTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_confidential_compute ComputeInstanceTemplate#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7778be93b7c3dbee70b52de1e5289f3b904b74a9123ebe179733405b07a776)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_type ComputeInstanceTemplate#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_confidential_compute ComputeInstanceTemplate#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe5c4ff2b8ddf89f851b4b3db394751703432e1290f3a24302a8fb3496b283c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a691293018c11f29d4c3db575013ad4aa33a4fe416b38d86af389a398391e42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f20a1f38d631fd92495d462226a70379a24de65a8757d4d875cfc7590aeebd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9f750c17166303a8b70808b6e1894d62bd3838e33ec9ccdaf56fd086a9dec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateConfig",
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
class ComputeInstanceTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateDisk", typing.Dict[builtins.str, typing.Any]]]],
        machine_type: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_description: typing.Optional[builtins.str] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        name_prefix: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param disk: disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk ComputeInstanceTemplate#disk}
        :param machine_type: The machine type to create. To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#machine_type ComputeInstanceTemplate#machine_type}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#advanced_machine_features ComputeInstanceTemplate#advanced_machine_features}
        :param can_ip_forward: Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#can_ip_forward ComputeInstanceTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_config ComputeInstanceTemplate#confidential_instance_config}
        :param description: A brief description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#description ComputeInstanceTemplate#description}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#guest_accelerator ComputeInstanceTemplate#guest_accelerator}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#id ComputeInstanceTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_description: A description of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_description ComputeInstanceTemplate#instance_description}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key_revocation_action_type ComputeInstanceTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs to assign to instances created from this template. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#labels ComputeInstanceTemplate#labels}
        :param metadata: Metadata key/value pairs to make available from within instances created from this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata ComputeInstanceTemplate#metadata}
        :param metadata_startup_script: An alternative to using the startup-script metadata key, mostly to match the compute_instance resource. This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata_startup_script ComputeInstanceTemplate#metadata_startup_script}
        :param min_cpu_platform: Specifies a minimum CPU platform. Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_cpu_platform ComputeInstanceTemplate#min_cpu_platform}
        :param name: The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name ComputeInstanceTemplate#name}
        :param name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with name. Max length is 54 characters. Prefixes with lengths longer than 37 characters will use a shortened UUID that will be more prone to collisions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name_prefix ComputeInstanceTemplate#name_prefix}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_interface ComputeInstanceTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_performance_config ComputeInstanceTemplate#network_performance_config}
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#project ComputeInstanceTemplate#project}
        :param region: An instance template is a global resource that is not bound to a zone or a region. However, you can still specify some regional resources in an instance template, which restricts the template to the region where that resource resides. For example, a custom subnetwork resource is tied to a specific region. Defaults to the region of the Provider if no value is given. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#region ComputeInstanceTemplate#region}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#reservation_affinity ComputeInstanceTemplate#reservation_affinity}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_manager_tags ComputeInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_policies ComputeInstanceTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scheduling ComputeInstanceTemplate#scheduling}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#service_account ComputeInstanceTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#shielded_instance_config ComputeInstanceTemplate#shielded_instance_config}
        :param tags: Tags to attach to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#tags ComputeInstanceTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#timeouts ComputeInstanceTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = ComputeInstanceTemplateAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = ComputeInstanceTemplateConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(network_performance_config, dict):
            network_performance_config = ComputeInstanceTemplateNetworkPerformanceConfig(**network_performance_config)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = ComputeInstanceTemplateReservationAffinity(**reservation_affinity)
        if isinstance(scheduling, dict):
            scheduling = ComputeInstanceTemplateScheduling(**scheduling)
        if isinstance(service_account, dict):
            service_account = ComputeInstanceTemplateServiceAccount(**service_account)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = ComputeInstanceTemplateShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f8c16465e742ce9d6f9212c6a33be8ad2802b87720a8475413f7225f5cd41a)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateDisk"]]:
        '''disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk ComputeInstanceTemplate#disk}
        '''
        result = self._values.get("disk")
        assert result is not None, "Required property 'disk' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateDisk"]], result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The machine type to create.

        To create a machine with a custom type (such as extended memory), format the value like custom-VCPUS-MEM_IN_MB like custom-6-20480 for 6 vCPU and 20GB of RAM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#machine_type ComputeInstanceTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#advanced_machine_features ComputeInstanceTemplate#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures], result)

    @builtins.property
    def can_ip_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow sending and receiving of packets with non-matching source or destination IPs. This defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#can_ip_forward ComputeInstanceTemplate#can_ip_forward}
        '''
        result = self._values.get("can_ip_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#confidential_instance_config ComputeInstanceTemplate#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#description ComputeInstanceTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#guest_accelerator ComputeInstanceTemplate#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateGuestAccelerator"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#id ComputeInstanceTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_description(self) -> typing.Optional[builtins.str]:
        '''A description of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_description ComputeInstanceTemplate#instance_description}
        '''
        result = self._values.get("instance_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_revocation_action_type(self) -> typing.Optional[builtins.str]:
        '''Action to be taken when a customer's encryption key is revoked.

        Supports "STOP" and "NONE", with "NONE" being the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key_revocation_action_type ComputeInstanceTemplate#key_revocation_action_type}
        '''
        result = self._values.get("key_revocation_action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to instances created from this template.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#labels ComputeInstanceTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata key/value pairs to make available from within instances created from this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata ComputeInstanceTemplate#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_startup_script(self) -> typing.Optional[builtins.str]:
        '''An alternative to using the startup-script metadata key, mostly to match the compute_instance resource.

        This replaces the startup-script metadata key on the created instance and thus the two mechanisms are not allowed to be used simultaneously.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#metadata_startup_script ComputeInstanceTemplate#metadata_startup_script}
        '''
        result = self._values.get("metadata_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''Specifies a minimum CPU platform.

        Applicable values are the friendly names of CPU platforms, such as Intel Haswell or Intel Skylake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_cpu_platform ComputeInstanceTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance template. If you leave this blank, Terraform will auto-generate a unique name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name ComputeInstanceTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name_prefix(self) -> typing.Optional[builtins.str]:
        '''Creates a unique name beginning with the specified prefix.

        Conflicts with name. Max length is 54 characters. Prefixes with lengths longer than 37 characters will use a shortened UUID that will be more prone to collisions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#name_prefix ComputeInstanceTemplate#name_prefix}
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_interface ComputeInstanceTemplate#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterface"]]], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_performance_config ComputeInstanceTemplate#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["ComputeInstanceTemplateNetworkPerformanceConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#project ComputeInstanceTemplate#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''An instance template is a global resource that is not bound to a zone or a region.

        However, you can still specify some regional resources in an instance template, which restricts the template to the region where that resource resides. For example, a custom subnetwork resource is tied to a specific region. Defaults to the region of the Provider if no value is given.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#region ComputeInstanceTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#reservation_affinity ComputeInstanceTemplate#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["ComputeInstanceTemplateReservationAffinity"], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags.
        Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456.
        The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_manager_tags ComputeInstanceTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_policies ComputeInstanceTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["ComputeInstanceTemplateScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scheduling ComputeInstanceTemplate#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["ComputeInstanceTemplateScheduling"], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#service_account ComputeInstanceTemplate#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["ComputeInstanceTemplateServiceAccount"], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#shielded_instance_config ComputeInstanceTemplate#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["ComputeInstanceTemplateShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags to attach to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#tags ComputeInstanceTemplate#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#timeouts ComputeInstanceTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDisk",
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
class ComputeInstanceTemplateDisk:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_name: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeInstanceTemplateDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
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
        source_image_encryption_key: typing.Optional[typing.Union["ComputeInstanceTemplateDiskSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the image. Allowed values are ARM64 or X86_64. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#architecture ComputeInstanceTemplate#architecture}
        :param auto_delete: Whether or not the disk should be auto-deleted. This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#auto_delete ComputeInstanceTemplate#auto_delete}
        :param boot: Indicates that this is a boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#boot ComputeInstanceTemplate#boot}
        :param device_name: A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance. If not specified, the server chooses a default device name to apply to this disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#device_name ComputeInstanceTemplate#device_name}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_encryption_key ComputeInstanceTemplate#disk_encryption_key}
        :param disk_name: Name of the disk. When not provided, this defaults to the name of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_name ComputeInstanceTemplate#disk_name}
        :param disk_size_gb: The size of the image in gigabytes. If not specified, it will inherit the size of its base image. For SCRATCH disks, the size must be one of 375 or 3000 GB, with a default of 375 GB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_size_gb ComputeInstanceTemplate#disk_size_gb}
        :param disk_type: The Google Compute Engine disk type. Such as "pd-ssd", "local-ssd", "pd-balanced" or "pd-standard". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_type ComputeInstanceTemplate#disk_type}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#guest_os_features ComputeInstanceTemplate#guest_os_features}
        :param interface: Specifies the disk interface to use for attaching this disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#interface ComputeInstanceTemplate#interface}
        :param labels: A set of key/value label pairs to assign to disks,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#labels ComputeInstanceTemplate#labels}
        :param mode: The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If you are attaching or creating a boot disk, this must read-write mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#mode ComputeInstanceTemplate#mode}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. For more details, see the `Extreme persistent disk documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_ or the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_ depending on the selected disk_type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioned_iops ComputeInstanceTemplate#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk, in MB/s. This sets the amount of data that can be read or written from the disk per second. Values must greater than or equal to 1. For more details, see the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioned_throughput ComputeInstanceTemplate#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_manager_tags ComputeInstanceTemplate#resource_manager_tags}
        :param resource_policies: A list (short name or id) of resource policies to attach to this disk. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_policies ComputeInstanceTemplate#resource_policies}
        :param source: The name (not self_link) of the disk (such as those managed by google_compute_disk) to attach. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source ComputeInstanceTemplate#source}
        :param source_image: The image from which to initialize this disk. This can be one of: the image's self_link, projects/{project}/global/images/{image}, projects/{project}/global/images/family/{family}, global/images/{image}, global/images/family/{family}, family/{family}, {project}/{family}, {project}/{image}, {family}, or {image}. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_image ComputeInstanceTemplate#source_image}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_image_encryption_key ComputeInstanceTemplate#source_image_encryption_key}
        :param source_snapshot: The source snapshot to create this disk. When creating a new instance, one of initializeParams.sourceSnapshot, initializeParams.sourceImage, or disks.source is required except for local SSD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_snapshot ComputeInstanceTemplate#source_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_snapshot_encryption_key ComputeInstanceTemplate#source_snapshot_encryption_key}
        :param type: The type of Google Compute Engine disk, can be either "SCRATCH" or "PERSISTENT". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        '''
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ComputeInstanceTemplateDiskDiskEncryptionKey(**disk_encryption_key)
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeInstanceTemplateDiskSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc210ccfcf958f3d1c6119757749c914e0792adc0ef812f66e910f716ebf7e7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#architecture ComputeInstanceTemplate#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the disk should be auto-deleted. This defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#auto_delete ComputeInstanceTemplate#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates that this is a boot disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#boot ComputeInstanceTemplate#boot}
        '''
        result = self._values.get("boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''A unique device name that is reflected into the /dev/ tree of a Linux operating system running within the instance.

        If not specified, the server chooses a default device name to apply to this disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#device_name ComputeInstanceTemplate#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateDiskDiskEncryptionKey"]:
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_encryption_key ComputeInstanceTemplate#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceTemplateDiskDiskEncryptionKey"], result)

    @builtins.property
    def disk_name(self) -> typing.Optional[builtins.str]:
        '''Name of the disk. When not provided, this defaults to the name of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_name ComputeInstanceTemplate#disk_name}
        '''
        result = self._values.get("disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the image in gigabytes.

        If not specified, it will inherit the size of its base image. For SCRATCH disks, the size must be one of 375 or 3000 GB, with a default of 375 GB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_size_gb ComputeInstanceTemplate#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disk_type(self) -> typing.Optional[builtins.str]:
        '''The Google Compute Engine disk type. Such as "pd-ssd", "local-ssd", "pd-balanced" or "pd-standard".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#disk_type ComputeInstanceTemplate#disk_type}
        '''
        result = self._values.get("disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_os_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of features to enable on the guest operating system. Applicable only for bootable images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#guest_os_features ComputeInstanceTemplate#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''Specifies the disk interface to use for attaching this disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#interface ComputeInstanceTemplate#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to disks,.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#labels ComputeInstanceTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode in which to attach this disk, either READ_WRITE or READ_ONLY.

        If you are attaching or creating a boot disk, this must read-write mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#mode ComputeInstanceTemplate#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS to provision for the disk.

        This sets the number of I/O operations per second that the disk can handle. For more details, see the `Extreme persistent disk documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_ or the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_ depending on the selected disk_type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioned_iops ComputeInstanceTemplate#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much throughput to provision for the disk, in MB/s.

        This sets the amount of data that can be read or written from the disk per second. Values must greater than or equal to 1. For more details, see the `Hyperdisk documentation <https://cloud.google.com/compute/docs/disks/hyperdisks>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioned_throughput ComputeInstanceTemplate#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_manager_tags ComputeInstanceTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list (short name or id) of resource policies to attach to this disk.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#resource_policies ComputeInstanceTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The name (not self_link) of the disk (such as those managed by google_compute_disk) to attach.

        ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source ComputeInstanceTemplate#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image(self) -> typing.Optional[builtins.str]:
        '''The image from which to initialize this disk.

        This can be one of: the image's self_link, projects/{project}/global/images/{image}, projects/{project}/global/images/family/{family}, global/images/{image}, global/images/family/{family}, family/{family}, {project}/{family}, {project}/{image}, {family}, or {image}. ~> Note: Either source or source_image is required when creating a new instance except for when creating a local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_image ComputeInstanceTemplate#source_image}
        '''
        result = self._values.get("source_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateDiskSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_image_encryption_key ComputeInstanceTemplate#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceTemplateDiskSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''The source snapshot to create this disk.

        When creating
        a new instance, one of initializeParams.sourceSnapshot,
        initializeParams.sourceImage, or disks.source is
        required except for local SSD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_snapshot ComputeInstanceTemplate#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#source_snapshot_encryption_key ComputeInstanceTemplate#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of Google Compute Engine disk, can be either "SCRATCH" or "PERSISTENT".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
    },
)
class ComputeInstanceTemplateDiskDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8960ebec6f3240b387b1a9f7c718ae36152b0d59479eb537823ceb9515dabf0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateDiskDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateDiskDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d809df671857ae8da357b8d744b85dd95bbb82e5fd241f111329be69ed8ed7ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da538e0166dd5926c5a18a612f808aaf2af10e756d74073535225d19c1f45cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5174c38f399480a3072d40e8f0b084f9ca5368907b855f0e32ec857bb4fe05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134a0a933873ff7527db3a755b922303c6e444e44e8e8f1eaa44d0c94792bf6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2498f2d4d383f90083bcf1f2799b7e6744639391519dc65803bd5c620a542c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceTemplateDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9091cdaeb4215567d6a7819287f3af8f0ecd0cb5d8a347f929f7bfbc52f9050a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417cf5417f06bbcf9348b2eddff2e5f08ef63db8d944bc7dfd7aef152feb56e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8e07e90c390dd27c552ada72ce625caee01adfdebb5e3ca0836c7b2e528f61f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ed5b2905e9bc5c6913c37ff687359516774a35f2cf3082bfb5edcbf8dc04f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbea10873a7aa08bc32162a25703bb55aa2c454bfc6d49018147287dc7ab0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4575b676db9e1aef9f6004d6e47e683672c846eb4db97b0815a36d20c7047755)
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        '''
        value = ComputeInstanceTemplateDiskDiskEncryptionKey(
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        value = ComputeInstanceTemplateDiskSourceImageEncryptionKey(
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        value = ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey(
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
    ) -> ComputeInstanceTemplateDiskDiskEncryptionKeyOutputReference:
        return typing.cast(ComputeInstanceTemplateDiskDiskEncryptionKeyOutputReference, jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeInstanceTemplateDiskSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceTemplateDiskSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

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
    ) -> typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey], jsii.get(self, "diskEncryptionKeyInput"))

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
    ) -> typing.Optional["ComputeInstanceTemplateDiskSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateDiskSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

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
    ) -> typing.Optional["ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6a8ed6791e3d0b2782f7fd8905523cc8df2a9ec3ce61718197a79f6ebb11be60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46dd666ed506d61e10fe596191d53c4e8744eda989d572ef5659a1035e1697ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a15572741430acc5e39c6c7bfaaebe1a7bb1dd9b7fba78c8f3ffbf49f759768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "boot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619c624ea0a4da070243b8d914139e431f34fa946869c304dc238e6373f8c71b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskName")
    def disk_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskName"))

    @disk_name.setter
    def disk_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e763beb7e52f0653634e4c92b523c157933e0d93b2af2c663da950e4d37fd2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9081e1b5c1c18c8bfa02aefaebc1f96f73506b0fb1f5a0624bccdcfa6d27f7c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374d85e2682787b297e9f7cf6d6abf4f4a6922dc0d975fb6a08385de4821751d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "guestOsFeatures"))

    @guest_os_features.setter
    def guest_os_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd40838e9f1ab1ac7385645b74de936804fea2f6ec6aa0d5e123575936e222d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestOsFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c218d53ec2805bc9cace1188a007c6dc5c490d02d7e1ba427d732e505088b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1338bf37a7aabc30ff5e2f46bc2f2a94a7e9cc30efffc8c6e8bdb4ffbe161b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d7314426965abbab25cf5b7ac4beeab663e1bdf4bbe21052efec8b5a9774d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04619a534bd9d351993d74671a5129e3c07109be1efef4ee8c675a04c8f8966a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9840576bf7d6595782967164b67e0e69af8aaf0f27d788bdedb5a84eea3c99e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aad5171f8ebe73566c4e83889f7f4bc02362fd13ba4b56df9584de9d7ccd36c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09b57624d99db117c013f02d39f1a8dcdf719af3b236a8ea91a3a43c03633b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4813e5bd8f8db56d30e4423c61a931d3ca55620c7e37fb3827cc83c3a9cae827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceImage")
    def source_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImage"))

    @source_image.setter
    def source_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98736561114f187be46f41d82acfa3ecc9c32fe07847858459d9143b0cf3c23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4d4c9034248447b51d76ecfe46d6a7cc49b5d530ce5f7aa3c9dcfbeb1791f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd81f208fe5b5dadf7c2ffd6a081cdb3e85ecb6035b3f0d205d2ffad1d299be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566ff7480914e40c8eba428e6fe7f132cb51df99fc942d44b43cf1cc63063a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceTemplateDiskSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944fd6a7af5c5fe18138af1d9c5c5659601590e866cb711552b15bf0a044e4ee)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute
        Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateDiskSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateDiskSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e2107d2008dfa2d9800293aa2ac6aacfca2bfca0a890af4110ec1c7ca9edeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42da513c720cd4e0481d9d204c652ff7dc4ea5584dd8aef09090ac1a817bb69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbaa553045254977f69ddb56c9a3a247d442a1998d3e4bb0c4e835aab1ca104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f001c59631b5fe74648d9581fc2856eb4615419b60d37852b7b2ca15be1122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3085d31ec36caf33a6ae0454bc3ca36781728faf850e439135f4fe275ed19dd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateDiskSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateDiskSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateDiskSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c061c0390aaae4c6794de90f2ea8573bd3250326e3f31f8d055bfe0d2e6ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c99b535cbe5c31efc754d7a2f1a47fd92a01d76395231d15911d81d5c72e0e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_self_link ComputeInstanceTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute
        Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#kms_key_service_account ComputeInstanceTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#raw_key ComputeInstanceTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#rsa_encrypted_key ComputeInstanceTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecb8ba60e7b08263bdee26dae20b503dbd14877f84414ff66975e24ab2c22cf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d9b5fbc0e79fa894e54980fd136301c401a90cbed85eaf6e83a4f770f0507aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c2ffecf377010d53e0519c3db5297200622c000b0eee9a1116a401d8df412c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02eb918f6e84745ccd43b8c141fa20df7e83133b17b7f90747f3b84286f5ecbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c0dbb41aefc63e58b27e25db3adc6c8cdc58187c477087853af1ab3ed51030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de54eae70810a85c977e304df66613acc0a4cd42fbdad023dc92bf7d4896dbca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class ComputeInstanceTemplateGuestAccelerator:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#count ComputeInstanceTemplate#count}
        :param type: The accelerator type resource to expose to this instance. E.g. nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55700645a43c29f2ad7aba29146b960c24ee2030ce577e6e076f537099bde6f)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#count ComputeInstanceTemplate#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource to expose to this instance. E.g. nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateGuestAcceleratorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__698477f3f63e1b79005c02ab440edf5131257c46c3032098750ccb2267d2e724)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095e8697afee015083fb9966e2478d78b12ad0ec2ff31084b4cc5cc2a9f273fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2e2ff9394a7457791af4928761cbc29a286932bf7a776c52830ce3921388a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f98f2cc267e599d9145223bf8b284316e4d3b0b8cd328fc520f6d6f7e292fca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f63dafa708b5619af9d92f5bf8c31a75babedeca787f7ecb6169ec43afd2596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08f4144916c5a89ddee23ce36101010092dcf6e7dfd08dc8d64f42db4c0cd99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateGuestAcceleratorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37c6c90ba9d752fa20c1177b38bae74089efc3b9905efc48c241ce58902d4699)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8cb9ce9438e8d534c013364a17dc39f71d0dbc43e297bbfef694f75bc6341e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a6d0b7cd4eb7ff8d62ca662136d049c652dbc3323d7b980cac04479af02ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3e80d58e4b986e1180844dc95ca87294f2880ad8f6125df29ec361aa8660b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterface",
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
class ComputeInstanceTemplateNetworkInterface:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterfaceAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterfaceAliasIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
        ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#access_config ComputeInstanceTemplate#access_config}
        :param alias_ip_range: alias_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#alias_ip_range ComputeInstanceTemplate#alias_ip_range}
        :param internal_ipv6_prefix_length: The prefix length of the primary internal IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#internal_ipv6_prefix_length ComputeInstanceTemplate#internal_ipv6_prefix_length}
        :param ipv6_access_config: ipv6_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ipv6_access_config ComputeInstanceTemplate#ipv6_access_config}
        :param ipv6_address: An IPv6 internal network address for this network interface. If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ipv6_address ComputeInstanceTemplate#ipv6_address}
        :param network: The name or self_link of the network to attach this interface to. Use network attribute for Legacy or Auto subnetted networks and subnetwork for custom subnetted networks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network ComputeInstanceTemplate#network}
        :param network_ip: The private IP address to assign to the instance. If empty, the address will be automatically assigned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_ip ComputeInstanceTemplate#network_ip}
        :param nic_type: The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, MRDMA, and IRDMA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nic_type ComputeInstanceTemplate#nic_type}
        :param queue_count: The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It will be empty if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#queue_count ComputeInstanceTemplate#queue_count}
        :param stack_type: The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#stack_type ComputeInstanceTemplate#stack_type}
        :param subnetwork: The name of the subnetwork to attach this interface to. The subnetwork must exist in the same region this instance will be created in. Either network or subnetwork must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork ComputeInstanceTemplate#subnetwork}
        :param subnetwork_project: The ID of the project in which the subnetwork belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork_project ComputeInstanceTemplate#subnetwork_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f976593061de9c39f50b0cda4f30fcd71370c545d2f1c80e95bf0389b86694f1)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#access_config ComputeInstanceTemplate#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceAccessConfig"]]], result)

    @builtins.property
    def alias_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceAliasIpRange"]]]:
        '''alias_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#alias_ip_range ComputeInstanceTemplate#alias_ip_range}
        '''
        result = self._values.get("alias_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceAliasIpRange"]]], result)

    @builtins.property
    def internal_ipv6_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''The prefix length of the primary internal IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#internal_ipv6_prefix_length ComputeInstanceTemplate#internal_ipv6_prefix_length}
        '''
        result = self._values.get("internal_ipv6_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ipv6_access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig"]]]:
        '''ipv6_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ipv6_access_config ComputeInstanceTemplate#ipv6_access_config}
        '''
        result = self._values.get("ipv6_access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig"]]], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''An IPv6 internal network address for this network interface.

        If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ipv6_address ComputeInstanceTemplate#ipv6_address}
        '''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the network to attach this interface to.

        Use network attribute for Legacy or Auto subnetted networks and subnetwork for custom subnetted networks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network ComputeInstanceTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_ip(self) -> typing.Optional[builtins.str]:
        '''The private IP address to assign to the instance. If empty, the address will be automatically assigned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_ip ComputeInstanceTemplate#network_ip}
        '''
        result = self._values.get("network_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, MRDMA, and IRDMA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nic_type ComputeInstanceTemplate#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_count(self) -> typing.Optional[jsii.Number]:
        '''The networking queue count that's specified by users for the network interface.

        Both Rx and Tx queues will be set to this number. It will be empty if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#queue_count ComputeInstanceTemplate#queue_count}
        '''
        result = self._values.get("queue_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this network interface to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#stack_type ComputeInstanceTemplate#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name of the subnetwork to attach this interface to.

        The subnetwork must exist in the same region this instance will be created in. Either network or subnetwork must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork ComputeInstanceTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the subnetwork belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork_project ComputeInstanceTemplate#subnetwork_project}
        '''
        result = self._values.get("subnetwork_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAccessConfig",
    jsii_struct_bases=[],
    name_mapping={"nat_ip": "natIp", "network_tier": "networkTier"},
)
class ComputeInstanceTemplateNetworkInterfaceAccessConfig:
    def __init__(
        self,
        *,
        nat_ip: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nat_ip: The IP address that will be 1:1 mapped to the instance's network ip. If not given, one will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nat_ip ComputeInstanceTemplate#nat_ip}
        :param network_tier: The networking tier used for configuring this instance template. This field can take the following values: PREMIUM, STANDARD, FIXED_STANDARD. If this field is not specified, it is assumed to be PREMIUM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_tier ComputeInstanceTemplate#network_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467589b7d4ce982ca48e030297c121cc04b7455013e72f13f6736dcfeea98718)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nat_ip ComputeInstanceTemplate#nat_ip}
        '''
        result = self._values.get("nat_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tier(self) -> typing.Optional[builtins.str]:
        '''The networking tier used for configuring this instance template.

        This field can take the following values: PREMIUM, STANDARD, FIXED_STANDARD. If this field is not specified, it is assumed to be PREMIUM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_tier ComputeInstanceTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateNetworkInterfaceAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateNetworkInterfaceAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c675f76edfb51b540df4f5f0c4eb8ff86c188c98e9f80f8c9a7cf67102ffae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateNetworkInterfaceAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67bcb7db15cd12be51c19f9519f25d2929c6c69525b0d91175ebbf8cf9b97ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateNetworkInterfaceAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a007051b83c45a0e73a9aeebe18ba318fc1ec6ab4227e17a12bbf8e0d299dede)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f117828a1934d8d9c86a93fc33d8fca01f8ba9b5ed62ca0780556b858c63f2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddfc952a3ea6482e85513b8735b4676d2e365ff9359abad1b3d340a4e5d48a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996172fe7858504e14be8fed3c2c983d620bd18ca22734da842d34b619c1b15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateNetworkInterfaceAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db40c207dbebe30326d89aed87c8d776d08bdc2797a753258b2007398ce93cd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d932dff86db2f38e06d67242a816ba89f907d11a7601d5dc493bb859cd4ba221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a34b3dc81b9e1f223f0bf3134a269aefaaf644f3959145540c87b8f80d9efa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25fa3da75022df0e2a7cd4187bddc831bdd5eb1903e6db6ab4ee7519771deae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAliasIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "ip_cidr_range": "ipCidrRange",
        "subnetwork_range_name": "subnetworkRangeName",
    },
)
class ComputeInstanceTemplateNetworkInterfaceAliasIpRange:
    def __init__(
        self,
        *,
        ip_cidr_range: builtins.str,
        subnetwork_range_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_cidr_range: The IP CIDR range represented by this alias IP range. This IP CIDR range must belong to the specified subnetwork and cannot contain IP addresses reserved by system or used by other network interfaces. At the time of writing only a netmask (e.g. /24) may be supplied, with a CIDR format resulting in an API error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ip_cidr_range ComputeInstanceTemplate#ip_cidr_range}
        :param subnetwork_range_name: The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range. If left unspecified, the primary range of the subnetwork will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork_range_name ComputeInstanceTemplate#subnetwork_range_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6063397cac382bb7fc71fcecaaebd334c72a21431722642750a39e4a2abdd6a2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#ip_cidr_range ComputeInstanceTemplate#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        assert result is not None, "Required property 'ip_cidr_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnetwork_range_name(self) -> typing.Optional[builtins.str]:
        '''The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range.

        If left unspecified, the primary range of the subnetwork will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#subnetwork_range_name ComputeInstanceTemplate#subnetwork_range_name}
        '''
        result = self._values.get("subnetwork_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateNetworkInterfaceAliasIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateNetworkInterfaceAliasIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAliasIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e68b4f5295973570de7802112e0cabe4106264a08efbf36b6135ca22fc867afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28134e7fce29e0dec6ad24632a8059ed82da6fa132f9304b1519afff105029dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9438d8dab93c89b6eae163e549d533c47e3a69868bc1243ceb1f249d2111e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3e62651afa0ec48e5f66d138caf77d0c1fb00c9ad552f2a3c387c3a60bff0c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e97215f9da99b4f299943ec348fe623b614156152b941c716f22a5f8b020817d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9632d59c01e6096ef9e7a45b748bacd7c4c1a771a7bf1560dbd74d94be5c7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59a2976ed677a64c7cf6a3f3d38d4a7445f2ff7283f76b1f49b2ba06de3887c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2af6d19d75a4c567669153368a0e095474be9de13130c32dd6c234084d6c0f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkRangeName")
    def subnetwork_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkRangeName"))

    @subnetwork_range_name.setter
    def subnetwork_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bef6a15f8ba3e4f55f4ff464cf7e445dbc9c56413e37e77c0e02416109b4825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAliasIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAliasIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9283bfb39c36b5a021494034264b285af3843840ac8475363724baae1681a7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig",
    jsii_struct_bases=[],
    name_mapping={"network_tier": "networkTier"},
)
class ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig:
    def __init__(self, *, network_tier: builtins.str) -> None:
        '''
        :param network_tier: The service-level to be provided for IPv6 traffic when the subnet has an external subnet. Only PREMIUM tier is valid for IPv6 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_tier ComputeInstanceTemplate#network_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bec06c9fc4d0977bf9505114b85ea999ff14de9de453ba4a7e0e080b776dbca)
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_tier": network_tier,
        }

    @builtins.property
    def network_tier(self) -> builtins.str:
        '''The service-level to be provided for IPv6 traffic when the subnet has an external subnet.

        Only PREMIUM tier is valid for IPv6

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#network_tier ComputeInstanceTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        assert result is not None, "Required property 'network_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1750054be2d0fd8f1c0ed1b9a75e025022e533f95ce6ede864c7a46ed1d2835c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afbe84b21bf4ca5ed6d231cd20148aa6f3ad61984097748a293bdf37e28c992)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910dd13fe90038fa713a41ef382f5468452e3fea273eb2d376ea180859f939a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59c66205893f00620e5b2d6854bda35ca9d35b106fa694ade568758148d24476)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfc55313740d4915f170b38fe297fcb52d3d1f19bbe16c2a2e8a48004cf2b508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc43544137042de7d33bb2adbd2b4a86b7c3d89b562c2bc55785f67411d4427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb39ac4bac86a2f08c8bc2f618ae83a825f7dd54e283f721c93f2ac503f26dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e6431aae8fe066c024682da5bb9785271fa86900c5882cda978ce0be35335ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e0b985ff8e676d6fc5c4f65d9906038d320dbd6d6a5a8ee313187393cd8878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afdcde4e0deccec6bf43eac0d0e2c90e7588f04b23cf9c873e3a7d72fecba41c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068a808aef1d82694155ad7d7edfd25b9cce0646c8d9d08ca13ed09cae32aba6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a61e150e06b193540f4737679df1bb4eda8fa21ca902c5b272369ea7739bd0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e003e428cd8f3b4688112afda1814abc0d17a4979cf6c9ce00f9694feb5f1f9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a13f5c93083e5545b471ed15638157a81561e6fcb7a7493ebf645119df803af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d978a05f706cc56cf22d9f416ff03bd10aac71c44922b3d905d6bd5a25247ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6956ace3ada2a6b734ea40e103f915c53c585cfbc12f96a6d16ccbd5f048a4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9bc71bf979e64fde3f37f9cd4b27441218e5fe5fa40e43d27008228c56ecc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putAliasIpRange")
    def put_alias_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1018c3cb6f1be2031d055a3287aac370e326ea50612f0038e6eb3141b4fdb1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAliasIpRange", [value]))

    @jsii.member(jsii_name="putIpv6AccessConfig")
    def put_ipv6_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42c4596d84435164a68f2a9141e989a3c03c343edfeec5c4a74ccfb8eb429ea)
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
    def access_config(self) -> ComputeInstanceTemplateNetworkInterfaceAccessConfigList:
        return typing.cast(ComputeInstanceTemplateNetworkInterfaceAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRange")
    def alias_ip_range(self) -> ComputeInstanceTemplateNetworkInterfaceAliasIpRangeList:
        return typing.cast(ComputeInstanceTemplateNetworkInterfaceAliasIpRangeList, jsii.get(self, "aliasIpRange"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfig")
    def ipv6_access_config(
        self,
    ) -> ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigList:
        return typing.cast(ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigList, jsii.get(self, "ipv6AccessConfig"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRangeInput")
    def alias_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "aliasIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6PrefixLengthInput")
    def internal_ipv6_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalIpv6PrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfigInput")
    def ipv6_access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "ipv6AccessConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6812e3e24462ee5d61c4cb0bcbbd216125d87f58116177528e438a5e840cd346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4b5daa2ce69ee472a1e542a9ad180a8b7f03bccb70a2ed25f652b0cfd1f43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12fafe23980e353e8b042ddb11ed3fa26799baa6bf348781563ed76e50f27228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkIp")
    def network_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkIp"))

    @network_ip.setter
    def network_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915b35356310ebc1bb6684cb7f321a5059b6d05b50a5d50e49111c2cdafa614f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75fc33a800d177f396cba42bf210bd1897219e11acc5c68edf520a7c20d8e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueCount")
    def queue_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueCount"))

    @queue_count.setter
    def queue_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b06364883a79c17c6d44d6b192c7a16065539c7822eea044c7b151f8280f820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac57572ed5fa8f27cdd98dc4e925fd9d348aea24873fa9fa708aec3138fe1b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e17567efd15ecc48c7508a635d7901f8630625301f9fff4ef1ca7bccb3bb076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkProject")
    def subnetwork_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkProject"))

    @subnetwork_project.setter
    def subnetwork_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c411c31d51721d091e64e2e6bc04b54ed1bdbfd00fdbda01e8525df1dd63b638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce974ce286b1199b00c5ea98d7e041948f5b5a30fadb7b5fd0aa76dfdc191557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class ComputeInstanceTemplateNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#total_egress_bandwidth_tier ComputeInstanceTemplate#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9656bcd743c28434ecf8d644a8c73a50854f782829c4999afc78bcd5254e5cf3)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#total_egress_bandwidth_tier ComputeInstanceTemplate#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateNetworkPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb1369bed3022b9f71e63c3a9e2a2ef1033b342905bfd9dcc3251c5791a627da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8292a56c8098c970a32e7c89fd7070ad0599914075a35dc0f551aabd5a3a3ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355ae59c48e9e19585ae8d9bcea27f3e222a44d2ea22229cb28cafdcc377e40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "specific_reservation": "specificReservation"},
)
class ComputeInstanceTemplateReservationAffinity:
    def __init__(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#specific_reservation ComputeInstanceTemplate#specific_reservation}
        '''
        if isinstance(specific_reservation, dict):
            specific_reservation = ComputeInstanceTemplateReservationAffinitySpecificReservation(**specific_reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4249ae14e04d756faf0b6e174ade5f28ca6253ce1b212f9bb330466894999577)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#type ComputeInstanceTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def specific_reservation(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateReservationAffinitySpecificReservation"]:
        '''specific_reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#specific_reservation ComputeInstanceTemplate#specific_reservation}
        '''
        result = self._values.get("specific_reservation")
        return typing.cast(typing.Optional["ComputeInstanceTemplateReservationAffinitySpecificReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d228a775f5946fab6a19d59b6a7b34685dab1c71954b1fe676c228f0ac909b8a)
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
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key ComputeInstanceTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#values ComputeInstanceTemplate#values}
        '''
        value = ComputeInstanceTemplateReservationAffinitySpecificReservation(
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
    ) -> "ComputeInstanceTemplateReservationAffinitySpecificReservationOutputReference":
        return typing.cast("ComputeInstanceTemplateReservationAffinitySpecificReservationOutputReference", jsii.get(self, "specificReservation"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationInput")
    def specific_reservation_input(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateReservationAffinitySpecificReservation"]:
        return typing.cast(typing.Optional["ComputeInstanceTemplateReservationAffinitySpecificReservation"], jsii.get(self, "specificReservationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__84bafd8f9c92d150a8a0b128b441a1855a62fbaa001082e5c41a6c5c322f067e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateReservationAffinity]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3832847c2bcb43dd79ebef6ece8c28b0fbd5c2769938d2d9a19db8a377794e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateReservationAffinitySpecificReservation",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class ComputeInstanceTemplateReservationAffinitySpecificReservation:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key ComputeInstanceTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#values ComputeInstanceTemplate#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd5d8f0f96b7d96b99613faf2dd10bb5de588b08f0d186ea2002defa71adaee3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key ComputeInstanceTemplate#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Corresponds to the label values of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#values ComputeInstanceTemplate#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateReservationAffinitySpecificReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateReservationAffinitySpecificReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateReservationAffinitySpecificReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91026d3f7628ebafd1a2f3441e01cdab701d2e1bd1af6c7eb6f65ffe0482786c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e532e8279dc4e5d9cce07fbbc5f6c6d07e715ad9986886f3b8f75f9610b66b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f81ac123e503fd4510e6240ead29b7891f329f29337a91c95f39dc75d912eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateReservationAffinitySpecificReservation]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateReservationAffinitySpecificReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateReservationAffinitySpecificReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011e7b61c9a4dce04dfd32e5492350282dbb9fbf5a60b767884f7725c930f281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateScheduling",
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
class ComputeInstanceTemplateScheduling:
    def __init__(
        self,
        *,
        automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_domain: typing.Optional[jsii.Number] = None,
        instance_termination_action: typing.Optional[builtins.str] = None,
        local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies whether the instance should be automatically restarted if it is terminated by Compute Engine (not terminated by a user). This defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#automatic_restart ComputeInstanceTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#availability_domain ComputeInstanceTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_termination_action ComputeInstanceTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#local_ssd_recovery_timeout ComputeInstanceTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#max_run_duration ComputeInstanceTemplate#max_run_duration}
        :param min_node_cpus: Minimum number of cpus for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_node_cpus ComputeInstanceTemplate#min_node_cpus}
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#node_affinities ComputeInstanceTemplate#node_affinities}
        :param on_host_maintenance: Defines the maintenance behavior for this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_host_maintenance ComputeInstanceTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_instance_stop_action ComputeInstanceTemplate#on_instance_stop_action}
        :param preemptible: Allows instance to be preempted. This defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#preemptible ComputeInstanceTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioning_model ComputeInstanceTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#termination_time ComputeInstanceTemplate#termination_time}
        '''
        if isinstance(max_run_duration, dict):
            max_run_duration = ComputeInstanceTemplateSchedulingMaxRunDuration(**max_run_duration)
        if isinstance(on_instance_stop_action, dict):
            on_instance_stop_action = ComputeInstanceTemplateSchedulingOnInstanceStopAction(**on_instance_stop_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c710d29be029be478563af8f6e0ae3560f118cf10f91438bc0b7d176cccd66a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#automatic_restart ComputeInstanceTemplate#automatic_restart}
        '''
        result = self._values.get("automatic_restart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_domain(self) -> typing.Optional[jsii.Number]:
        '''Specifies the availability domain, which this instance should be scheduled on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#availability_domain ComputeInstanceTemplate#availability_domain}
        '''
        result = self._values.get("availability_domain")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_termination_action(self) -> typing.Optional[builtins.str]:
        '''Specifies the action GCE should take when SPOT VM is preempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#instance_termination_action ComputeInstanceTemplate#instance_termination_action}
        '''
        result = self._values.get("instance_termination_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_recovery_timeout(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout"]]]:
        '''local_ssd_recovery_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#local_ssd_recovery_timeout ComputeInstanceTemplate#local_ssd_recovery_timeout}
        '''
        result = self._values.get("local_ssd_recovery_timeout")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout"]]], result)

    @builtins.property
    def max_run_duration(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateSchedulingMaxRunDuration"]:
        '''max_run_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#max_run_duration ComputeInstanceTemplate#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional["ComputeInstanceTemplateSchedulingMaxRunDuration"], result)

    @builtins.property
    def min_node_cpus(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of cpus for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#min_node_cpus ComputeInstanceTemplate#min_node_cpus}
        '''
        result = self._values.get("min_node_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_affinities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateSchedulingNodeAffinities"]]]:
        '''node_affinities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#node_affinities ComputeInstanceTemplate#node_affinities}
        '''
        result = self._values.get("node_affinities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceTemplateSchedulingNodeAffinities"]]], result)

    @builtins.property
    def on_host_maintenance(self) -> typing.Optional[builtins.str]:
        '''Defines the maintenance behavior for this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_host_maintenance ComputeInstanceTemplate#on_host_maintenance}
        '''
        result = self._values.get("on_host_maintenance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_instance_stop_action(
        self,
    ) -> typing.Optional["ComputeInstanceTemplateSchedulingOnInstanceStopAction"]:
        '''on_instance_stop_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#on_instance_stop_action ComputeInstanceTemplate#on_instance_stop_action}
        '''
        result = self._values.get("on_instance_stop_action")
        return typing.cast(typing.Optional["ComputeInstanceTemplateSchedulingOnInstanceStopAction"], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows instance to be preempted. This defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#preemptible ComputeInstanceTemplate#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_model(self) -> typing.Optional[builtins.str]:
        '''Whether the instance is spot. If this is set as SPOT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#provisioning_model ComputeInstanceTemplate#provisioning_model}
        '''
        result = self._values.get("provisioning_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the timestamp, when the instance will be terminated, in RFC3339 text format.

        If specified, the instance termination action
        will be performed at the termination time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#termination_time ComputeInstanceTemplate#termination_time}
        '''
        result = self._values.get("termination_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#seconds ComputeInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nanos ComputeInstanceTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96f30fb0b2b1af8062d12046616edabd716e6ea148e197ff0467dac6f2bdba6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#seconds ComputeInstanceTemplate#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nanos ComputeInstanceTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__576e07d91192b82a1e050ab664a5e0869a593b7c5b6a431cda15b8e4ba7bfcff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb0dc751a8841c91764bb0ea2531b5cba7d4885ac3671e86fae7482ccaedb98)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907d7bb33c1531c6d71d9eabf1accd2e0aabb65b16dd009f66bed10e3b26cb88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d760a56813d72692e95c2f6933980dfa00e9ba091cc3d8d2abbe7ba5de1f2b18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a53f0ad37f26b13633da4967f8b385f7dcba597fb25b99bc2903429fd56d6b05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d43d32f75f5e53a3a4545095fbfaed300b12b0edc25206bdbdb0140fd42a7b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b4b906f7c85db20debb56e4dbe500cf9e2106d358875fdda27733e8eeb6e145)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e81ba4ba8f8c3247869ca0aa69a1d5906ffb6ad8382c89c4afea4ce2fb505be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f776541c9ca8bf33b73c3d8f7772c972abf6a57e3b2393ff1cdf0a3383deb6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e2aaf1172ff8b8e100ad65899d97c5935863bb6a766febf4f3a2a943549b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingMaxRunDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceTemplateSchedulingMaxRunDuration:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#seconds ComputeInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nanos ComputeInstanceTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c0577aedac68e6a1665f6514ee8743a2a5b60a7e2db338b3e591ef3f2f9aaf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#seconds ComputeInstanceTemplate#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nanos ComputeInstanceTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateSchedulingMaxRunDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateSchedulingMaxRunDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingMaxRunDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f82f074398e0623df0cfd140e69b311bacf74bc8cebd572dcb83a202f0c0704)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14cbc8cb973803ef8ae134986210befcfe4450c952316a80f193d59a81c912de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e5ff31f9e4a897a662ae0dcca3f6f4896d590e91b0481a5b52253388921301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09774054c20292af109b1ca44f843d6dca4e7595e3554ca785e9e220e19fd3c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingNodeAffinities",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ComputeInstanceTemplateSchedulingNodeAffinities:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key ComputeInstanceTemplate#key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#operator ComputeInstanceTemplate#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#values ComputeInstanceTemplate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fcb64907fc56173f55892fa11168b256f575fb9d8b6b6274ce20f58704c2c0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#key ComputeInstanceTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#operator ComputeInstanceTemplate#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#values ComputeInstanceTemplate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateSchedulingNodeAffinities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateSchedulingNodeAffinitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingNodeAffinitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b885f71c5f8ed94d7043737bfb62975e4850d50f09536510b6c52ca5ea6c0b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceTemplateSchedulingNodeAffinitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1acf86ec0fe4fef61e158363f6a23b879a3ece67df68cab4b16a5d60bd08175)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceTemplateSchedulingNodeAffinitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c22fe4b2bcf81819dca883956988ed32dd5ae347dc580966293572bb16acec9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c10716a0a04f092a382f78e9b61472b949b93311d8774df03e3bb70dfa0b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61dc552d00444eb085256edcbc0b20d6fdb3f9ea0922924d6747b7cc8a14a58d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67bf184265a28361bce6dbc57dc16d55181ec98d016507c6da6f2229a76b251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateSchedulingNodeAffinitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingNodeAffinitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81693563b543aa9785c134d3421024dae5992fc98db800fa4006929aeb94a370)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d6b7da1eebddf6c1caed9dfef3703db7891b3a4b337b42537592a23cd01d7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afda7bfcf227439007a8a1c59fd401354b0a798189adc05ba325d878e8f4876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688ec241d91ab931b5d0f2b37b64db41c7f7286c67bb1884fa8c6127c9002acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingNodeAffinities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingNodeAffinities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingNodeAffinities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ddf0bdf7e486623704e4c118cc24510a6b823d23ce5741d3a66d6e116012a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingOnInstanceStopAction",
    jsii_struct_bases=[],
    name_mapping={"discard_local_ssd": "discardLocalSsd"},
)
class ComputeInstanceTemplateSchedulingOnInstanceStopAction:
    def __init__(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#discard_local_ssd ComputeInstanceTemplate#discard_local_ssd}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9af56bcdd8cdc8d3297b8d031b7e762141883d81896b16a70458087271ab66)
            check_type(argname="argument discard_local_ssd", value=discard_local_ssd, expected_type=type_hints["discard_local_ssd"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discard_local_ssd is not None:
            self._values["discard_local_ssd"] = discard_local_ssd

    @builtins.property
    def discard_local_ssd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the contents of any attached Local SSD disks will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#discard_local_ssd ComputeInstanceTemplate#discard_local_ssd}
        '''
        result = self._values.get("discard_local_ssd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateSchedulingOnInstanceStopAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateSchedulingOnInstanceStopActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingOnInstanceStopActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c5ebf92d39fd4beae61aaa3efe406345b15e56d8442cfa8df7d330d2cb56aa1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5660a60b7f2328db44fa3700894e3c4fc18b54897dcecb295ba2d63e93b2935b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discardLocalSsd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674fb264da95befdf0523487be07c2c584e1e71aa4e8fce5a27a1b2de9223cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceTemplateSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb37a6f8659c2654f89f40b0032529c47249bc09dc50beeca707f6d14729764)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalSsdRecoveryTimeout")
    def put_local_ssd_recovery_timeout(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8da9ce29c31f29258b95f46a0760820bea6a77550a2b00294d8a66370662dbe)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#seconds ComputeInstanceTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#nanos ComputeInstanceTemplate#nanos}
        '''
        value = ComputeInstanceTemplateSchedulingMaxRunDuration(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putMaxRunDuration", [value]))

    @jsii.member(jsii_name="putNodeAffinities")
    def put_node_affinities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db41273fdd21df3ba15d5005bc164444a4ae54f02ba9207b77d68ce82778cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinities", [value]))

    @jsii.member(jsii_name="putOnInstanceStopAction")
    def put_on_instance_stop_action(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#discard_local_ssd ComputeInstanceTemplate#discard_local_ssd}
        '''
        value = ComputeInstanceTemplateSchedulingOnInstanceStopAction(
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
    ) -> ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList:
        return typing.cast(ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList, jsii.get(self, "localSsdRecoveryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(
        self,
    ) -> ComputeInstanceTemplateSchedulingMaxRunDurationOutputReference:
        return typing.cast(ComputeInstanceTemplateSchedulingMaxRunDurationOutputReference, jsii.get(self, "maxRunDuration"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinities")
    def node_affinities(self) -> ComputeInstanceTemplateSchedulingNodeAffinitiesList:
        return typing.cast(ComputeInstanceTemplateSchedulingNodeAffinitiesList, jsii.get(self, "nodeAffinities"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopAction")
    def on_instance_stop_action(
        self,
    ) -> ComputeInstanceTemplateSchedulingOnInstanceStopActionOutputReference:
        return typing.cast(ComputeInstanceTemplateSchedulingOnInstanceStopActionOutputReference, jsii.get(self, "onInstanceStopAction"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]], jsii.get(self, "localSsdRecoveryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDurationInput")
    def max_run_duration_input(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration], jsii.get(self, "maxRunDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCpusInput")
    def min_node_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinitiesInput")
    def node_affinities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]], jsii.get(self, "nodeAffinitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenanceInput")
    def on_host_maintenance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onHostMaintenanceInput"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopActionInput")
    def on_instance_stop_action_input(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction], jsii.get(self, "onInstanceStopActionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__844cecf7d938e4715d63c62212fc71486cc8e316f2386ac5959a3ca9b568db83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticRestart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityDomain")
    def availability_domain(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomain"))

    @availability_domain.setter
    def availability_domain(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cd6bfd5d46a62527e496674566296a56897e88beb02f91235fed7f2ab1e707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTerminationAction")
    def instance_termination_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminationAction"))

    @instance_termination_action.setter
    def instance_termination_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34ad21e1ce5bd784700eba46499854477835a600628f82b48c55895e3fbe03a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCpus")
    def min_node_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCpus"))

    @min_node_cpus.setter
    def min_node_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694b01045e95aae13ddcd31bd0205a0b2c3541a1cb6c5bc50ece8a0ff43fa27b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenance")
    def on_host_maintenance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onHostMaintenance"))

    @on_host_maintenance.setter
    def on_host_maintenance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02431b62a38897f3055c85eeb066c78ebf8d3ef99150c97036d8b930b03f5fbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__354b828df03a678019977ffb652c65cfe6db8357f35d5aba00f101f3e66be4e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningModel")
    def provisioning_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningModel"))

    @provisioning_model.setter
    def provisioning_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d975086e39cea4690456c61dc2e444623ffe3552ce29a027908dade2b5c6dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationTime")
    def termination_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminationTime"))

    @termination_time.setter
    def termination_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c70840dc52f609e0efb601bd8d65ff0b44dd0451fa79e9968f78f264ffb9e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceTemplateScheduling]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateScheduling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85a977b4d60208ec426156d9a158570af5b7e72ce86a13638feeb82b8ee6ed7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"scopes": "scopes", "email": "email"},
)
class ComputeInstanceTemplateServiceAccount:
    def __init__(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Both OAuth2 URLs and gcloud short names are supported. To allow full access to all Cloud APIs, use the cloud-platform scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scopes ComputeInstanceTemplate#scopes}
        :param email: The service account e-mail address. If not given, the default Google Compute Engine service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#email ComputeInstanceTemplate#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d731a2766caa10b8dc2894eb25379340c310538e1bcff26662dbbe00f98a483b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#scopes ComputeInstanceTemplate#scopes}
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The service account e-mail address. If not given, the default Google Compute Engine service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#email ComputeInstanceTemplate#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b7b02cfeaf94fe0a36d3c3ebfb9346991dec386745ec1663eb4e2d892cee58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c5123df32c00f97a2415c6b3cc931fbdd9729c95d2cab39e945ef8a2f7aa713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2267f5a7d13d596a26e524991b8db6dbe69ff0a01f3e6405234f7b84f9fcf265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceTemplateServiceAccount]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fdc103979725af73e405cac1cb4438e288a58f19ad38c3e9bb98d5354d60fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class ComputeInstanceTemplateShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Compare the most recent boot measurements to the integrity policy baseline and return a pair of pass/fail results depending on whether they match or not. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_integrity_monitoring ComputeInstanceTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Verify the digital signature of all boot components, and halt the boot process if signature verification fails. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_secure_boot ComputeInstanceTemplate#enable_secure_boot}
        :param enable_vtpm: Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_vtpm ComputeInstanceTemplate#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1977d38bc7a3631396728cb20d0d722e52fa25cfbdf938567f0fe120289154)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_integrity_monitoring ComputeInstanceTemplate#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verify the digital signature of all boot components, and halt the boot process if signature verification fails.

        Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_secure_boot ComputeInstanceTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use a virtualized trusted platform module, which is a specialized computer chip you can use to encrypt objects like keys and certificates.

        Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#enable_vtpm ComputeInstanceTemplate#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d7834e78cd5064300d5c017ec2c9e4f98d310ef8883173057b9b1e243fd6cb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c88374fb275d99cdeb2165425fb435349e5f3fadf84a7cbb9ba73d23cc4e9cc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18baf6109c12f18f539a169a5a457681b2de4537f85d622812b4cf2deb3b5ea7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1faa1f71111a41ad8f5b442a2b259f06866c73497820dc26e0206747f6ea8afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceTemplateShieldedInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceTemplateShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceTemplateShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497f022f85e1f90ccd6236e65ae4f8e00d804b7c22d39602b195a41c58c413df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ComputeInstanceTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#create ComputeInstanceTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#delete ComputeInstanceTemplate#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180be508cf1faf093f608cd18363ee8514a4765d81b129fa9e067c8a69429a01)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#create ComputeInstanceTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_template#delete ComputeInstanceTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceTemplate.ComputeInstanceTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3211dfc732eff8a3e11bc4ce1d5464f57f6574de1ce4f71e04d47eba500d5ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc9880bdd088e85c33ba0ee2e0d61155a5979100b021a2797791b682f81afd9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6921856998187423c1e09dab7928d3849517f64d2aad7eb32b378b8b46dda7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48b2e0a5249cdd3291c1185b0d33c34cd91dda8100a5d6fac5dbc1a8b237181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstanceTemplate",
    "ComputeInstanceTemplateAdvancedMachineFeatures",
    "ComputeInstanceTemplateAdvancedMachineFeaturesOutputReference",
    "ComputeInstanceTemplateConfidentialInstanceConfig",
    "ComputeInstanceTemplateConfidentialInstanceConfigOutputReference",
    "ComputeInstanceTemplateConfig",
    "ComputeInstanceTemplateDisk",
    "ComputeInstanceTemplateDiskDiskEncryptionKey",
    "ComputeInstanceTemplateDiskDiskEncryptionKeyOutputReference",
    "ComputeInstanceTemplateDiskList",
    "ComputeInstanceTemplateDiskOutputReference",
    "ComputeInstanceTemplateDiskSourceImageEncryptionKey",
    "ComputeInstanceTemplateDiskSourceImageEncryptionKeyOutputReference",
    "ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey",
    "ComputeInstanceTemplateDiskSourceSnapshotEncryptionKeyOutputReference",
    "ComputeInstanceTemplateGuestAccelerator",
    "ComputeInstanceTemplateGuestAcceleratorList",
    "ComputeInstanceTemplateGuestAcceleratorOutputReference",
    "ComputeInstanceTemplateNetworkInterface",
    "ComputeInstanceTemplateNetworkInterfaceAccessConfig",
    "ComputeInstanceTemplateNetworkInterfaceAccessConfigList",
    "ComputeInstanceTemplateNetworkInterfaceAccessConfigOutputReference",
    "ComputeInstanceTemplateNetworkInterfaceAliasIpRange",
    "ComputeInstanceTemplateNetworkInterfaceAliasIpRangeList",
    "ComputeInstanceTemplateNetworkInterfaceAliasIpRangeOutputReference",
    "ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig",
    "ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigList",
    "ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
    "ComputeInstanceTemplateNetworkInterfaceList",
    "ComputeInstanceTemplateNetworkInterfaceOutputReference",
    "ComputeInstanceTemplateNetworkPerformanceConfig",
    "ComputeInstanceTemplateNetworkPerformanceConfigOutputReference",
    "ComputeInstanceTemplateReservationAffinity",
    "ComputeInstanceTemplateReservationAffinityOutputReference",
    "ComputeInstanceTemplateReservationAffinitySpecificReservation",
    "ComputeInstanceTemplateReservationAffinitySpecificReservationOutputReference",
    "ComputeInstanceTemplateScheduling",
    "ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout",
    "ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutList",
    "ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
    "ComputeInstanceTemplateSchedulingMaxRunDuration",
    "ComputeInstanceTemplateSchedulingMaxRunDurationOutputReference",
    "ComputeInstanceTemplateSchedulingNodeAffinities",
    "ComputeInstanceTemplateSchedulingNodeAffinitiesList",
    "ComputeInstanceTemplateSchedulingNodeAffinitiesOutputReference",
    "ComputeInstanceTemplateSchedulingOnInstanceStopAction",
    "ComputeInstanceTemplateSchedulingOnInstanceStopActionOutputReference",
    "ComputeInstanceTemplateSchedulingOutputReference",
    "ComputeInstanceTemplateServiceAccount",
    "ComputeInstanceTemplateServiceAccountOutputReference",
    "ComputeInstanceTemplateShieldedInstanceConfig",
    "ComputeInstanceTemplateShieldedInstanceConfigOutputReference",
    "ComputeInstanceTemplateTimeouts",
    "ComputeInstanceTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__49cf633252edc7ab3fae9af894664c0fd70d486a116066e8bba425f96aff04be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
    machine_type: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_description: typing.Optional[builtins.str] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6b43db1c01a848636d281e00ca0b2cfe2d336c5cfd386fde9962b264f5b179ca(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072ccc7f51ea680b80000af4a904ee236ada08af74f74c867a1ac28fbb40d817(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b8d701ebbe44d7097463c9d19ed05749355ec02a26fb218483bb676e57134f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5c0d938e93386aaa24d5daf04844f9b1925d24a5836a2b81bab801ed3646ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc151ebb13a9710ffbe557fa3834d3e628af9a1c280622fb2aba68c1bfc4b8f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef697f7fa599dfe803803a2f5f7f96548b6897d526b06045c8412f663c83dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650883a47d58ed99034082e149ad96fec228cdf1b56cfc2779129db57441a8f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b5853b2bbaec3502f30d952fe8bd15709e965a0575122a9cd5dde65fbc4fbfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e13fe2bda6c3c62ea83c5907488808032a0aa40014c04d82c80c92206093c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc65f23d3670987771a364d017f9a653426039ef6cf158f4b1f13ad48f3150f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a3cc7d28b6ddda49ca61fd4ebd2c58093cb5e2b611abdf39155b31393be287(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b747b4ca3ca13dfaa1dfa8d13090e89e41bcaa9f68f15774c29b4caea88918d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53c39d4f6e5a5d5f81135cb72bcf6c395ffe826c63ed8e3eb7164ac9803c22b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2ecf62c236c56a85e0c0c3312595650f14f5bf376e4c34a31d4b2d9df18be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631e9549ef7a7f31dae01c915569f2af60c3ff1ec0ea095c30b769313d970363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4389759d4597dc65be58cea810c3a64427fa0461c6a8dd7b521267f43779dcd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c18dd43ea9007f5684b63efbc2e3008a6f91460a86d92d420b0354018645d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3013e8768686cfd3341c46b8f2f15639caa1b20ecef4ae6f05196fd9b07b9465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60f39a407507bb48f3803dd708e15205b7e9c515b5d47df1ab5bb45838cac24(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2aad022a15a6cd4105bba551a120da15c8c9445c67a887e6e5aa8207780f59d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28d8ada072df6af5f06c02361e3ae60221533f0c7946e9cab44d2d9dd53f173(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca98a0ca4fff4536f5554418144a6b0a4b38084e9a15a11dce3220826eab6b1(
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

def _typecheckingstub__3eabf1d9ec90083b9fb6dd8a5e27bf1c48285a76125182d46015f39b72e7b1e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83c4c8073883f547652290099f8c67e96486f9f67aad7e31f785eac5391d92b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0aabdadd0acb3f541cb80689167d30d30c9acf1ffd78f4b824824012fc28027(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86db4332e0425f156ac49ec7a29e5078470c803a9fd351d20d28713aeae979eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9b89cb5d5bc46a696d67a67df327a5a74a69b631907c636920f35ab310cada(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48f63c46e64599df23de50c9efef680c42e7f70da7c6a34a96ac8deb14d812a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e251b385367725e2116cf6538f673dd3b9a23ae9f977609c5c1e102080f6706(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8feb9893299e8fb072a42f3fdc2a697d325eb809857d3f1ccada9d8b8dd1eb(
    value: typing.Optional[ComputeInstanceTemplateAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7778be93b7c3dbee70b52de1e5289f3b904b74a9123ebe179733405b07a776(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5c4ff2b8ddf89f851b4b3db394751703432e1290f3a24302a8fb3496b283c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a691293018c11f29d4c3db575013ad4aa33a4fe416b38d86af389a398391e42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f20a1f38d631fd92495d462226a70379a24de65a8757d4d875cfc7590aeebd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9f750c17166303a8b70808b6e1894d62bd3838e33ec9ccdaf56fd086a9dec6(
    value: typing.Optional[ComputeInstanceTemplateConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f8c16465e742ce9d6f9212c6a33be8ad2802b87720a8475413f7225f5cd41a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disk: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateDisk, typing.Dict[builtins.str, typing.Any]]]],
    machine_type: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_description: typing.Optional[builtins.str] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    name_prefix: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc210ccfcf958f3d1c6119757749c914e0792adc0ef812f66e910f716ebf7e7(
    *,
    architecture: typing.Optional[builtins.str] = None,
    auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_name: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeInstanceTemplateDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
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
    source_image_encryption_key: typing.Optional[typing.Union[ComputeInstanceTemplateDiskSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8960ebec6f3240b387b1a9f7c718ae36152b0d59479eb537823ceb9515dabf0(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d809df671857ae8da357b8d744b85dd95bbb82e5fd241f111329be69ed8ed7ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da538e0166dd5926c5a18a612f808aaf2af10e756d74073535225d19c1f45cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5174c38f399480a3072d40e8f0b084f9ca5368907b855f0e32ec857bb4fe05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134a0a933873ff7527db3a755b922303c6e444e44e8e8f1eaa44d0c94792bf6c(
    value: typing.Optional[ComputeInstanceTemplateDiskDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2498f2d4d383f90083bcf1f2799b7e6744639391519dc65803bd5c620a542c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9091cdaeb4215567d6a7819287f3af8f0ecd0cb5d8a347f929f7bfbc52f9050a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417cf5417f06bbcf9348b2eddff2e5f08ef63db8d944bc7dfd7aef152feb56e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e07e90c390dd27c552ada72ce625caee01adfdebb5e3ca0836c7b2e528f61f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ed5b2905e9bc5c6913c37ff687359516774a35f2cf3082bfb5edcbf8dc04f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbea10873a7aa08bc32162a25703bb55aa2c454bfc6d49018147287dc7ab0b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4575b676db9e1aef9f6004d6e47e683672c846eb4db97b0815a36d20c7047755(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8ed6791e3d0b2782f7fd8905523cc8df2a9ec3ce61718197a79f6ebb11be60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dd666ed506d61e10fe596191d53c4e8744eda989d572ef5659a1035e1697ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a15572741430acc5e39c6c7bfaaebe1a7bb1dd9b7fba78c8f3ffbf49f759768(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619c624ea0a4da070243b8d914139e431f34fa946869c304dc238e6373f8c71b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e763beb7e52f0653634e4c92b523c157933e0d93b2af2c663da950e4d37fd2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9081e1b5c1c18c8bfa02aefaebc1f96f73506b0fb1f5a0624bccdcfa6d27f7c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374d85e2682787b297e9f7cf6d6abf4f4a6922dc0d975fb6a08385de4821751d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd40838e9f1ab1ac7385645b74de936804fea2f6ec6aa0d5e123575936e222d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c218d53ec2805bc9cace1188a007c6dc5c490d02d7e1ba427d732e505088b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1338bf37a7aabc30ff5e2f46bc2f2a94a7e9cc30efffc8c6e8bdb4ffbe161b28(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d7314426965abbab25cf5b7ac4beeab663e1bdf4bbe21052efec8b5a9774d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04619a534bd9d351993d74671a5129e3c07109be1efef4ee8c675a04c8f8966a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9840576bf7d6595782967164b67e0e69af8aaf0f27d788bdedb5a84eea3c99e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad5171f8ebe73566c4e83889f7f4bc02362fd13ba4b56df9584de9d7ccd36c7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09b57624d99db117c013f02d39f1a8dcdf719af3b236a8ea91a3a43c03633b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4813e5bd8f8db56d30e4423c61a931d3ca55620c7e37fb3827cc83c3a9cae827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98736561114f187be46f41d82acfa3ecc9c32fe07847858459d9143b0cf3c23e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4d4c9034248447b51d76ecfe46d6a7cc49b5d530ce5f7aa3c9dcfbeb1791f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd81f208fe5b5dadf7c2ffd6a081cdb3e85ecb6035b3f0d205d2ffad1d299be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566ff7480914e40c8eba428e6fe7f132cb51df99fc942d44b43cf1cc63063a3e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944fd6a7af5c5fe18138af1d9c5c5659601590e866cb711552b15bf0a044e4ee(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e2107d2008dfa2d9800293aa2ac6aacfca2bfca0a890af4110ec1c7ca9edeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42da513c720cd4e0481d9d204c652ff7dc4ea5584dd8aef09090ac1a817bb69e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbaa553045254977f69ddb56c9a3a247d442a1998d3e4bb0c4e835aab1ca104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f001c59631b5fe74648d9581fc2856eb4615419b60d37852b7b2ca15be1122(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3085d31ec36caf33a6ae0454bc3ca36781728faf850e439135f4fe275ed19dd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c061c0390aaae4c6794de90f2ea8573bd3250326e3f31f8d055bfe0d2e6ea9(
    value: typing.Optional[ComputeInstanceTemplateDiskSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c99b535cbe5c31efc754d7a2f1a47fd92a01d76395231d15911d81d5c72e0e(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb8ba60e7b08263bdee26dae20b503dbd14877f84414ff66975e24ab2c22cf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9b5fbc0e79fa894e54980fd136301c401a90cbed85eaf6e83a4f770f0507aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c2ffecf377010d53e0519c3db5297200622c000b0eee9a1116a401d8df412c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eb918f6e84745ccd43b8c141fa20df7e83133b17b7f90747f3b84286f5ecbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c0dbb41aefc63e58b27e25db3adc6c8cdc58187c477087853af1ab3ed51030(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de54eae70810a85c977e304df66613acc0a4cd42fbdad023dc92bf7d4896dbca(
    value: typing.Optional[ComputeInstanceTemplateDiskSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55700645a43c29f2ad7aba29146b960c24ee2030ce577e6e076f537099bde6f(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698477f3f63e1b79005c02ab440edf5131257c46c3032098750ccb2267d2e724(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095e8697afee015083fb9966e2478d78b12ad0ec2ff31084b4cc5cc2a9f273fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2e2ff9394a7457791af4928761cbc29a286932bf7a776c52830ce3921388a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f98f2cc267e599d9145223bf8b284316e4d3b0b8cd328fc520f6d6f7e292fca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f63dafa708b5619af9d92f5bf8c31a75babedeca787f7ecb6169ec43afd2596(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08f4144916c5a89ddee23ce36101010092dcf6e7dfd08dc8d64f42db4c0cd99(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c6c90ba9d752fa20c1177b38bae74089efc3b9905efc48c241ce58902d4699(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8cb9ce9438e8d534c013364a17dc39f71d0dbc43e297bbfef694f75bc6341e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a6d0b7cd4eb7ff8d62ca662136d049c652dbc3323d7b980cac04479af02ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3e80d58e4b986e1180844dc95ca87294f2880ad8f6125df29ec361aa8660b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f976593061de9c39f50b0cda4f30fcd71370c545d2f1c80e95bf0389b86694f1(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
    ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__467589b7d4ce982ca48e030297c121cc04b7455013e72f13f6736dcfeea98718(
    *,
    nat_ip: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c675f76edfb51b540df4f5f0c4eb8ff86c188c98e9f80f8c9a7cf67102ffae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67bcb7db15cd12be51c19f9519f25d2929c6c69525b0d91175ebbf8cf9b97ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a007051b83c45a0e73a9aeebe18ba318fc1ec6ab4227e17a12bbf8e0d299dede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f117828a1934d8d9c86a93fc33d8fca01f8ba9b5ed62ca0780556b858c63f2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfc952a3ea6482e85513b8735b4676d2e365ff9359abad1b3d340a4e5d48a3a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996172fe7858504e14be8fed3c2c983d620bd18ca22734da842d34b619c1b15c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db40c207dbebe30326d89aed87c8d776d08bdc2797a753258b2007398ce93cd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d932dff86db2f38e06d67242a816ba89f907d11a7601d5dc493bb859cd4ba221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a34b3dc81b9e1f223f0bf3134a269aefaaf644f3959145540c87b8f80d9efa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25fa3da75022df0e2a7cd4187bddc831bdd5eb1903e6db6ab4ee7519771deae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6063397cac382bb7fc71fcecaaebd334c72a21431722642750a39e4a2abdd6a2(
    *,
    ip_cidr_range: builtins.str,
    subnetwork_range_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68b4f5295973570de7802112e0cabe4106264a08efbf36b6135ca22fc867afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28134e7fce29e0dec6ad24632a8059ed82da6fa132f9304b1519afff105029dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9438d8dab93c89b6eae163e549d533c47e3a69868bc1243ceb1f249d2111e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e62651afa0ec48e5f66d138caf77d0c1fb00c9ad552f2a3c387c3a60bff0c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97215f9da99b4f299943ec348fe623b614156152b941c716f22a5f8b020817d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9632d59c01e6096ef9e7a45b748bacd7c4c1a771a7bf1560dbd74d94be5c7ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceAliasIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a2976ed677a64c7cf6a3f3d38d4a7445f2ff7283f76b1f49b2ba06de3887c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2af6d19d75a4c567669153368a0e095474be9de13130c32dd6c234084d6c0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bef6a15f8ba3e4f55f4ff464cf7e445dbc9c56413e37e77c0e02416109b4825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9283bfb39c36b5a021494034264b285af3843840ac8475363724baae1681a7b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceAliasIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bec06c9fc4d0977bf9505114b85ea999ff14de9de453ba4a7e0e080b776dbca(
    *,
    network_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1750054be2d0fd8f1c0ed1b9a75e025022e533f95ce6ede864c7a46ed1d2835c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afbe84b21bf4ca5ed6d231cd20148aa6f3ad61984097748a293bdf37e28c992(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910dd13fe90038fa713a41ef382f5468452e3fea273eb2d376ea180859f939a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c66205893f00620e5b2d6854bda35ca9d35b106fa694ade568758148d24476(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc55313740d4915f170b38fe297fcb52d3d1f19bbe16c2a2e8a48004cf2b508(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc43544137042de7d33bb2adbd2b4a86b7c3d89b562c2bc55785f67411d4427(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb39ac4bac86a2f08c8bc2f618ae83a825f7dd54e283f721c93f2ac503f26dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6431aae8fe066c024682da5bb9785271fa86900c5882cda978ce0be35335ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e0b985ff8e676d6fc5c4f65d9906038d320dbd6d6a5a8ee313187393cd8878(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdcde4e0deccec6bf43eac0d0e2c90e7588f04b23cf9c873e3a7d72fecba41c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068a808aef1d82694155ad7d7edfd25b9cce0646c8d9d08ca13ed09cae32aba6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a61e150e06b193540f4737679df1bb4eda8fa21ca902c5b272369ea7739bd0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e003e428cd8f3b4688112afda1814abc0d17a4979cf6c9ce00f9694feb5f1f9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a13f5c93083e5545b471ed15638157a81561e6fcb7a7493ebf645119df803af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d978a05f706cc56cf22d9f416ff03bd10aac71c44922b3d905d6bd5a25247ec6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6956ace3ada2a6b734ea40e103f915c53c585cfbc12f96a6d16ccbd5f048a4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9bc71bf979e64fde3f37f9cd4b27441218e5fe5fa40e43d27008228c56ecc1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1018c3cb6f1be2031d055a3287aac370e326ea50612f0038e6eb3141b4fdb1c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42c4596d84435164a68f2a9141e989a3c03c343edfeec5c4a74ccfb8eb429ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6812e3e24462ee5d61c4cb0bcbbd216125d87f58116177528e438a5e840cd346(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4b5daa2ce69ee472a1e542a9ad180a8b7f03bccb70a2ed25f652b0cfd1f43f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fafe23980e353e8b042ddb11ed3fa26799baa6bf348781563ed76e50f27228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915b35356310ebc1bb6684cb7f321a5059b6d05b50a5d50e49111c2cdafa614f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75fc33a800d177f396cba42bf210bd1897219e11acc5c68edf520a7c20d8e4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b06364883a79c17c6d44d6b192c7a16065539c7822eea044c7b151f8280f820(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac57572ed5fa8f27cdd98dc4e925fd9d348aea24873fa9fa708aec3138fe1b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e17567efd15ecc48c7508a635d7901f8630625301f9fff4ef1ca7bccb3bb076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c411c31d51721d091e64e2e6bc04b54ed1bdbfd00fdbda01e8525df1dd63b638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce974ce286b1199b00c5ea98d7e041948f5b5a30fadb7b5fd0aa76dfdc191557(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9656bcd743c28434ecf8d644a8c73a50854f782829c4999afc78bcd5254e5cf3(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1369bed3022b9f71e63c3a9e2a2ef1033b342905bfd9dcc3251c5791a627da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8292a56c8098c970a32e7c89fd7070ad0599914075a35dc0f551aabd5a3a3ad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355ae59c48e9e19585ae8d9bcea27f3e222a44d2ea22229cb28cafdcc377e40e(
    value: typing.Optional[ComputeInstanceTemplateNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4249ae14e04d756faf0b6e174ade5f28ca6253ce1b212f9bb330466894999577(
    *,
    type: builtins.str,
    specific_reservation: typing.Optional[typing.Union[ComputeInstanceTemplateReservationAffinitySpecificReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d228a775f5946fab6a19d59b6a7b34685dab1c71954b1fe676c228f0ac909b8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bafd8f9c92d150a8a0b128b441a1855a62fbaa001082e5c41a6c5c322f067e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3832847c2bcb43dd79ebef6ece8c28b0fbd5c2769938d2d9a19db8a377794e3e(
    value: typing.Optional[ComputeInstanceTemplateReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd5d8f0f96b7d96b99613faf2dd10bb5de588b08f0d186ea2002defa71adaee3(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91026d3f7628ebafd1a2f3441e01cdab701d2e1bd1af6c7eb6f65ffe0482786c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e532e8279dc4e5d9cce07fbbc5f6c6d07e715ad9986886f3b8f75f9610b66b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f81ac123e503fd4510e6240ead29b7891f329f29337a91c95f39dc75d912eab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011e7b61c9a4dce04dfd32e5492350282dbb9fbf5a60b767884f7725c930f281(
    value: typing.Optional[ComputeInstanceTemplateReservationAffinitySpecificReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c710d29be029be478563af8f6e0ae3560f118cf10f91438bc0b7d176cccd66a(
    *,
    automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_domain: typing.Optional[jsii.Number] = None,
    instance_termination_action: typing.Optional[builtins.str] = None,
    local_ssd_recovery_timeout: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_run_duration: typing.Optional[typing.Union[ComputeInstanceTemplateSchedulingMaxRunDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_node_cpus: typing.Optional[jsii.Number] = None,
    node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on_host_maintenance: typing.Optional[builtins.str] = None,
    on_instance_stop_action: typing.Optional[typing.Union[ComputeInstanceTemplateSchedulingOnInstanceStopAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_model: typing.Optional[builtins.str] = None,
    termination_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96f30fb0b2b1af8062d12046616edabd716e6ea148e197ff0467dac6f2bdba6(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576e07d91192b82a1e050ab664a5e0869a593b7c5b6a431cda15b8e4ba7bfcff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb0dc751a8841c91764bb0ea2531b5cba7d4885ac3671e86fae7482ccaedb98(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907d7bb33c1531c6d71d9eabf1accd2e0aabb65b16dd009f66bed10e3b26cb88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d760a56813d72692e95c2f6933980dfa00e9ba091cc3d8d2abbe7ba5de1f2b18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53f0ad37f26b13633da4967f8b385f7dcba597fb25b99bc2903429fd56d6b05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d43d32f75f5e53a3a4545095fbfaed300b12b0edc25206bdbdb0140fd42a7b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4b906f7c85db20debb56e4dbe500cf9e2106d358875fdda27733e8eeb6e145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e81ba4ba8f8c3247869ca0aa69a1d5906ffb6ad8382c89c4afea4ce2fb505be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f776541c9ca8bf33b73c3d8f7772c972abf6a57e3b2393ff1cdf0a3383deb6ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e2aaf1172ff8b8e100ad65899d97c5935863bb6a766febf4f3a2a943549b5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c0577aedac68e6a1665f6514ee8743a2a5b60a7e2db338b3e591ef3f2f9aaf(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f82f074398e0623df0cfd140e69b311bacf74bc8cebd572dcb83a202f0c0704(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cbc8cb973803ef8ae134986210befcfe4450c952316a80f193d59a81c912de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e5ff31f9e4a897a662ae0dcca3f6f4896d590e91b0481a5b52253388921301(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09774054c20292af109b1ca44f843d6dca4e7595e3554ca785e9e220e19fd3c4(
    value: typing.Optional[ComputeInstanceTemplateSchedulingMaxRunDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fcb64907fc56173f55892fa11168b256f575fb9d8b6b6274ce20f58704c2c0(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b885f71c5f8ed94d7043737bfb62975e4850d50f09536510b6c52ca5ea6c0b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1acf86ec0fe4fef61e158363f6a23b879a3ece67df68cab4b16a5d60bd08175(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c22fe4b2bcf81819dca883956988ed32dd5ae347dc580966293572bb16acec9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c10716a0a04f092a382f78e9b61472b949b93311d8774df03e3bb70dfa0b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61dc552d00444eb085256edcbc0b20d6fdb3f9ea0922924d6747b7cc8a14a58d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67bf184265a28361bce6dbc57dc16d55181ec98d016507c6da6f2229a76b251(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceTemplateSchedulingNodeAffinities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81693563b543aa9785c134d3421024dae5992fc98db800fa4006929aeb94a370(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6b7da1eebddf6c1caed9dfef3703db7891b3a4b337b42537592a23cd01d7f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afda7bfcf227439007a8a1c59fd401354b0a798189adc05ba325d878e8f4876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688ec241d91ab931b5d0f2b37b64db41c7f7286c67bb1884fa8c6127c9002acc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddf0bdf7e486623704e4c118cc24510a6b823d23ce5741d3a66d6e116012a03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateSchedulingNodeAffinities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9af56bcdd8cdc8d3297b8d031b7e762141883d81896b16a70458087271ab66(
    *,
    discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5ebf92d39fd4beae61aaa3efe406345b15e56d8442cfa8df7d330d2cb56aa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5660a60b7f2328db44fa3700894e3c4fc18b54897dcecb295ba2d63e93b2935b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674fb264da95befdf0523487be07c2c584e1e71aa4e8fce5a27a1b2de9223cc5(
    value: typing.Optional[ComputeInstanceTemplateSchedulingOnInstanceStopAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb37a6f8659c2654f89f40b0032529c47249bc09dc50beeca707f6d14729764(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8da9ce29c31f29258b95f46a0760820bea6a77550a2b00294d8a66370662dbe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db41273fdd21df3ba15d5005bc164444a4ae54f02ba9207b77d68ce82778cf1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844cecf7d938e4715d63c62212fc71486cc8e316f2386ac5959a3ca9b568db83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cd6bfd5d46a62527e496674566296a56897e88beb02f91235fed7f2ab1e707(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34ad21e1ce5bd784700eba46499854477835a600628f82b48c55895e3fbe03a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694b01045e95aae13ddcd31bd0205a0b2c3541a1cb6c5bc50ece8a0ff43fa27b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02431b62a38897f3055c85eeb066c78ebf8d3ef99150c97036d8b930b03f5fbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354b828df03a678019977ffb652c65cfe6db8357f35d5aba00f101f3e66be4e2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d975086e39cea4690456c61dc2e444623ffe3552ce29a027908dade2b5c6dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c70840dc52f609e0efb601bd8d65ff0b44dd0451fa79e9968f78f264ffb9e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85a977b4d60208ec426156d9a158570af5b7e72ce86a13638feeb82b8ee6ed7(
    value: typing.Optional[ComputeInstanceTemplateScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d731a2766caa10b8dc2894eb25379340c310538e1bcff26662dbbe00f98a483b(
    *,
    scopes: typing.Sequence[builtins.str],
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b7b02cfeaf94fe0a36d3c3ebfb9346991dec386745ec1663eb4e2d892cee58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5123df32c00f97a2415c6b3cc931fbdd9729c95d2cab39e945ef8a2f7aa713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2267f5a7d13d596a26e524991b8db6dbe69ff0a01f3e6405234f7b84f9fcf265(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fdc103979725af73e405cac1cb4438e288a58f19ad38c3e9bb98d5354d60fe(
    value: typing.Optional[ComputeInstanceTemplateServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1977d38bc7a3631396728cb20d0d722e52fa25cfbdf938567f0fe120289154(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7834e78cd5064300d5c017ec2c9e4f98d310ef8883173057b9b1e243fd6cb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88374fb275d99cdeb2165425fb435349e5f3fadf84a7cbb9ba73d23cc4e9cc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18baf6109c12f18f539a169a5a457681b2de4537f85d622812b4cf2deb3b5ea7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1faa1f71111a41ad8f5b442a2b259f06866c73497820dc26e0206747f6ea8afa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497f022f85e1f90ccd6236e65ae4f8e00d804b7c22d39602b195a41c58c413df(
    value: typing.Optional[ComputeInstanceTemplateShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180be508cf1faf093f608cd18363ee8514a4765d81b129fa9e067c8a69429a01(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3211dfc732eff8a3e11bc4ce1d5464f57f6574de1ce4f71e04d47eba500d5ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9880bdd088e85c33ba0ee2e0d61155a5979100b021a2797791b682f81afd9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6921856998187423c1e09dab7928d3849517f64d2aad7eb32b378b8b46dda7f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48b2e0a5249cdd3291c1185b0d33c34cd91dda8100a5d6fac5dbc1a8b237181(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

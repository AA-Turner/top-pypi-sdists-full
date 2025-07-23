r'''
# `google_compute_instance_from_template`

Refer to the Terraform Registry for docs: [`google_compute_instance_from_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template).
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


class ComputeInstanceFromTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template google_compute_instance_from_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        source_instance_template: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union["ComputeInstanceFromTemplateAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateAttachedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union["ComputeInstanceFromTemplateBootDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union["ComputeInstanceFromTemplateConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_status: typing.Optional[builtins.str] = None,
        enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_encryption_key: typing.Optional[typing.Union["ComputeInstanceFromTemplateInstanceEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceFromTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeInstanceFromTemplateParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceFromTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceFromTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateScratchDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceFromTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceFromTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceFromTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template google_compute_instance_from_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the instance. One of name or self_link must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#name ComputeInstanceFromTemplate#name}
        :param source_instance_template: Name or self link of an instance template to create the instance based on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_instance_template ComputeInstanceFromTemplate#source_instance_template}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#advanced_machine_features ComputeInstanceFromTemplate#advanced_machine_features}
        :param allow_stopping_for_update: If true, allows Terraform to stop the instance to update its properties. If you try to update a property that requires stopping the instance without setting this field, the update will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#allow_stopping_for_update ComputeInstanceFromTemplate#allow_stopping_for_update}
        :param attached_disk: attached_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#attached_disk ComputeInstanceFromTemplate#attached_disk}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#boot_disk ComputeInstanceFromTemplate#boot_disk}
        :param can_ip_forward: Whether sending and receiving of packets with non-matching source or destination IPs is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#can_ip_forward ComputeInstanceFromTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_config ComputeInstanceFromTemplate#confidential_instance_config}
        :param deletion_protection: Whether deletion protection is enabled on this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#deletion_protection ComputeInstanceFromTemplate#deletion_protection}
        :param description: A brief description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#description ComputeInstanceFromTemplate#description}
        :param desired_status: Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#desired_status ComputeInstanceFromTemplate#desired_status}
        :param enable_display: Whether the instance has virtual displays enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_display ComputeInstanceFromTemplate#enable_display}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_accelerator ComputeInstanceFromTemplate#guest_accelerator}
        :param hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#hostname ComputeInstanceFromTemplate#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#id ComputeInstanceFromTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_encryption_key: instance_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_encryption_key ComputeInstanceFromTemplate#instance_encryption_key}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key_revocation_action_type ComputeInstanceFromTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs assigned to the instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        :param machine_type: The machine type to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#machine_type ComputeInstanceFromTemplate#machine_type}
        :param metadata: Metadata key/value pairs made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata ComputeInstanceFromTemplate#metadata}
        :param metadata_startup_script: Metadata startup scripts made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata_startup_script ComputeInstanceFromTemplate#metadata_startup_script}
        :param min_cpu_platform: The minimum CPU platform specified for the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_cpu_platform ComputeInstanceFromTemplate#min_cpu_platform}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_interface ComputeInstanceFromTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_performance_config ComputeInstanceFromTemplate#network_performance_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#params ComputeInstanceFromTemplate#params}
        :param project: The ID of the project in which the resource belongs. If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#project ComputeInstanceFromTemplate#project}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#reservation_affinity ComputeInstanceFromTemplate#reservation_affinity}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scheduling ComputeInstanceFromTemplate#scheduling}
        :param scratch_disk: scratch_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scratch_disk ComputeInstanceFromTemplate#scratch_disk}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#service_account ComputeInstanceFromTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#shielded_instance_config ComputeInstanceFromTemplate#shielded_instance_config}
        :param tags: The list of tags attached to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#tags ComputeInstanceFromTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#timeouts ComputeInstanceFromTemplate#timeouts}
        :param zone: The zone of the instance. If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#zone ComputeInstanceFromTemplate#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9124d7c3f082b1298466630389ce5b835ab60613b6b9b2156faa779358c47722)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceFromTemplateConfig(
            name=name,
            source_instance_template=source_instance_template,
            advanced_machine_features=advanced_machine_features,
            allow_stopping_for_update=allow_stopping_for_update,
            attached_disk=attached_disk,
            boot_disk=boot_disk,
            can_ip_forward=can_ip_forward,
            confidential_instance_config=confidential_instance_config,
            deletion_protection=deletion_protection,
            description=description,
            desired_status=desired_status,
            enable_display=enable_display,
            guest_accelerator=guest_accelerator,
            hostname=hostname,
            id=id,
            instance_encryption_key=instance_encryption_key,
            key_revocation_action_type=key_revocation_action_type,
            labels=labels,
            machine_type=machine_type,
            metadata=metadata,
            metadata_startup_script=metadata_startup_script,
            min_cpu_platform=min_cpu_platform,
            network_interface=network_interface,
            network_performance_config=network_performance_config,
            params=params,
            project=project,
            reservation_affinity=reservation_affinity,
            resource_policies=resource_policies,
            scheduling=scheduling,
            scratch_disk=scratch_disk,
            service_account=service_account,
            shielded_instance_config=shielded_instance_config,
            tags=tags,
            timeouts=timeouts,
            zone=zone,
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
        '''Generates CDKTF code for importing a ComputeInstanceFromTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstanceFromTemplate to import.
        :param import_from_id: The id of the existing ComputeInstanceFromTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstanceFromTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a0d1fafa28757ccf886bd38038315b61c49d3626b41233acb7066d5fd3c16e)
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_nested_virtualization ComputeInstanceFromTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_uefi_networking ComputeInstanceFromTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#performance_monitoring_unit ComputeInstanceFromTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#threads_per_core ComputeInstanceFromTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#turbo_mode ComputeInstanceFromTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#visible_core_count ComputeInstanceFromTemplate#visible_core_count}
        '''
        value = ComputeInstanceFromTemplateAdvancedMachineFeatures(
            enable_nested_virtualization=enable_nested_virtualization,
            enable_uefi_networking=enable_uefi_networking,
            performance_monitoring_unit=performance_monitoring_unit,
            threads_per_core=threads_per_core,
            turbo_mode=turbo_mode,
            visible_core_count=visible_core_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedMachineFeatures", [value]))

    @jsii.member(jsii_name="putAttachedDisk")
    def put_attached_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateAttachedDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd86eff08c8a375305ce0b338f991d67a91e8bc75a9aa949291057d38559b92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAttachedDisk", [value]))

    @jsii.member(jsii_name="putBootDisk")
    def put_boot_disk(
        self,
        *,
        auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_name: typing.Optional[builtins.str] = None,
        disk_encryption_key_raw: typing.Optional[builtins.str] = None,
        disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
        disk_encryption_service_account: typing.Optional[builtins.str] = None,
        force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        initialize_params: typing.Optional[typing.Union["ComputeInstanceFromTemplateBootDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete: Whether the disk will be auto-deleted when the instance is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#auto_delete ComputeInstanceFromTemplate#auto_delete}
        :param device_name: Name with which attached disk will be accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_raw ComputeInstanceFromTemplate#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_rsa ComputeInstanceFromTemplate#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_service_account ComputeInstanceFromTemplate#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#force_attach ComputeInstanceFromTemplate#force_attach}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_os_features ComputeInstanceFromTemplate#guest_os_features}
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#initialize_params ComputeInstanceFromTemplate#initialize_params}
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#interface ComputeInstanceFromTemplate#interface}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#mode ComputeInstanceFromTemplate#mode}
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source ComputeInstanceFromTemplate#source}
        '''
        value = ComputeInstanceFromTemplateBootDisk(
            auto_delete=auto_delete,
            device_name=device_name,
            disk_encryption_key_raw=disk_encryption_key_raw,
            disk_encryption_key_rsa=disk_encryption_key_rsa,
            disk_encryption_service_account=disk_encryption_service_account,
            force_attach=force_attach,
            guest_os_features=guest_os_features,
            initialize_params=initialize_params,
            interface=interface,
            kms_key_self_link=kms_key_self_link,
            mode=mode,
            source=source,
        )

        return typing.cast(None, jsii.invoke(self, "putBootDisk", [value]))

    @jsii.member(jsii_name="putConfidentialInstanceConfig")
    def put_confidential_instance_config(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_type ComputeInstanceFromTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        '''
        value = ComputeInstanceFromTemplateConfidentialInstanceConfig(
            confidential_instance_type=confidential_instance_type,
            enable_confidential_compute=enable_confidential_compute,
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4956625220e67b80c385a70b49445baa5839754d7cb033889e050c7628f164a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestAccelerator", [value]))

    @jsii.member(jsii_name="putInstanceEncryptionKey")
    def put_instance_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        '''
        value = ComputeInstanceFromTemplateInstanceEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceEncryptionKey", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fcf30e2cb3b7c0ab85919287e3f427f6e8a6a83718807067d8f7283da21b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#total_egress_bandwidth_tier ComputeInstanceFromTemplate#total_egress_bandwidth_tier}
        '''
        value = ComputeInstanceFromTemplateNetworkPerformanceConfig(
            total_egress_bandwidth_tier=total_egress_bandwidth_tier
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkPerformanceConfig", [value]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        '''
        value = ComputeInstanceFromTemplateParams(
            resource_manager_tags=resource_manager_tags
        )

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceFromTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#specific_reservation ComputeInstanceFromTemplate#specific_reservation}
        '''
        value = ComputeInstanceFromTemplateReservationAffinity(
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
        local_ssd_recovery_timeout: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#automatic_restart ComputeInstanceFromTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#availability_domain ComputeInstanceFromTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_termination_action ComputeInstanceFromTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#local_ssd_recovery_timeout ComputeInstanceFromTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#max_run_duration ComputeInstanceFromTemplate#max_run_duration}
        :param min_node_cpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_node_cpus ComputeInstanceFromTemplate#min_node_cpus}.
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#node_affinities ComputeInstanceFromTemplate#node_affinities}
        :param on_host_maintenance: Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_host_maintenance ComputeInstanceFromTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_instance_stop_action ComputeInstanceFromTemplate#on_instance_stop_action}
        :param preemptible: Whether the instance is preemptible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#preemptible ComputeInstanceFromTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioning_model ComputeInstanceFromTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#termination_time ComputeInstanceFromTemplate#termination_time}
        '''
        value = ComputeInstanceFromTemplateScheduling(
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

    @jsii.member(jsii_name="putScratchDisk")
    def put_scratch_disk(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateScratchDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee94dba9b0419cd693edd6b591babb695bf32d6ee6bb7010916fec605db92b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScratchDisk", [value]))

    @jsii.member(jsii_name="putServiceAccount")
    def put_service_account(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scopes ComputeInstanceFromTemplate#scopes}
        :param email: The service account e-mail address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#email ComputeInstanceFromTemplate#email}
        '''
        value = ComputeInstanceFromTemplateServiceAccount(scopes=scopes, email=email)

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
        :param enable_integrity_monitoring: Whether integrity monitoring is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_integrity_monitoring ComputeInstanceFromTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Whether secure boot is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_secure_boot ComputeInstanceFromTemplate#enable_secure_boot}
        :param enable_vtpm: Whether the instance uses vTPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_vtpm ComputeInstanceFromTemplate#enable_vtpm}
        '''
        value = ComputeInstanceFromTemplateShieldedInstanceConfig(
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
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#create ComputeInstanceFromTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#delete ComputeInstanceFromTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#update ComputeInstanceFromTemplate#update}.
        '''
        value = ComputeInstanceFromTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedMachineFeatures")
    def reset_advanced_machine_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedMachineFeatures", []))

    @jsii.member(jsii_name="resetAllowStoppingForUpdate")
    def reset_allow_stopping_for_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowStoppingForUpdate", []))

    @jsii.member(jsii_name="resetAttachedDisk")
    def reset_attached_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAttachedDisk", []))

    @jsii.member(jsii_name="resetBootDisk")
    def reset_boot_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDisk", []))

    @jsii.member(jsii_name="resetCanIpForward")
    def reset_can_ip_forward(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanIpForward", []))

    @jsii.member(jsii_name="resetConfidentialInstanceConfig")
    def reset_confidential_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfidentialInstanceConfig", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDesiredStatus")
    def reset_desired_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredStatus", []))

    @jsii.member(jsii_name="resetEnableDisplay")
    def reset_enable_display(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDisplay", []))

    @jsii.member(jsii_name="resetGuestAccelerator")
    def reset_guest_accelerator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestAccelerator", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceEncryptionKey")
    def reset_instance_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceEncryptionKey", []))

    @jsii.member(jsii_name="resetKeyRevocationActionType")
    def reset_key_revocation_action_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRevocationActionType", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataStartupScript")
    def reset_metadata_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataStartupScript", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

    @jsii.member(jsii_name="resetNetworkInterface")
    def reset_network_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterface", []))

    @jsii.member(jsii_name="resetNetworkPerformanceConfig")
    def reset_network_performance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPerformanceConfig", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetResourcePolicies")
    def reset_resource_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePolicies", []))

    @jsii.member(jsii_name="resetScheduling")
    def reset_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduling", []))

    @jsii.member(jsii_name="resetScratchDisk")
    def reset_scratch_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScratchDisk", []))

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

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    ) -> "ComputeInstanceFromTemplateAdvancedMachineFeaturesOutputReference":
        return typing.cast("ComputeInstanceFromTemplateAdvancedMachineFeaturesOutputReference", jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="attachedDisk")
    def attached_disk(self) -> "ComputeInstanceFromTemplateAttachedDiskList":
        return typing.cast("ComputeInstanceFromTemplateAttachedDiskList", jsii.get(self, "attachedDisk"))

    @builtins.property
    @jsii.member(jsii_name="bootDisk")
    def boot_disk(self) -> "ComputeInstanceFromTemplateBootDiskOutputReference":
        return typing.cast("ComputeInstanceFromTemplateBootDiskOutputReference", jsii.get(self, "bootDisk"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> "ComputeInstanceFromTemplateConfidentialInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceFromTemplateConfidentialInstanceConfigOutputReference", jsii.get(self, "confidentialInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="cpuPlatform")
    def cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuPlatform"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="currentStatus")
    def current_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentStatus"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="guestAccelerator")
    def guest_accelerator(self) -> "ComputeInstanceFromTemplateGuestAcceleratorList":
        return typing.cast("ComputeInstanceFromTemplateGuestAcceleratorList", jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="instanceEncryptionKey")
    def instance_encryption_key(
        self,
    ) -> "ComputeInstanceFromTemplateInstanceEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceFromTemplateInstanceEncryptionKeyOutputReference", jsii.get(self, "instanceEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="metadataFingerprint")
    def metadata_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="networkInterface")
    def network_interface(self) -> "ComputeInstanceFromTemplateNetworkInterfaceList":
        return typing.cast("ComputeInstanceFromTemplateNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> "ComputeInstanceFromTemplateNetworkPerformanceConfigOutputReference":
        return typing.cast("ComputeInstanceFromTemplateNetworkPerformanceConfigOutputReference", jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeInstanceFromTemplateParamsOutputReference":
        return typing.cast("ComputeInstanceFromTemplateParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "ComputeInstanceFromTemplateReservationAffinityOutputReference":
        return typing.cast("ComputeInstanceFromTemplateReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "ComputeInstanceFromTemplateSchedulingOutputReference":
        return typing.cast("ComputeInstanceFromTemplateSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="scratchDisk")
    def scratch_disk(self) -> "ComputeInstanceFromTemplateScratchDiskList":
        return typing.cast("ComputeInstanceFromTemplateScratchDiskList", jsii.get(self, "scratchDisk"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(
        self,
    ) -> "ComputeInstanceFromTemplateServiceAccountOutputReference":
        return typing.cast("ComputeInstanceFromTemplateServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "ComputeInstanceFromTemplateShieldedInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceFromTemplateShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

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
    def timeouts(self) -> "ComputeInstanceFromTemplateTimeoutsOutputReference":
        return typing.cast("ComputeInstanceFromTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateAdvancedMachineFeatures"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateAdvancedMachineFeatures"], jsii.get(self, "advancedMachineFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowStoppingForUpdateInput")
    def allow_stopping_for_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowStoppingForUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="attachedDiskInput")
    def attached_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateAttachedDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateAttachedDisk"]]], jsii.get(self, "attachedDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskInput")
    def boot_disk_input(self) -> typing.Optional["ComputeInstanceFromTemplateBootDisk"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDisk"], jsii.get(self, "bootDiskInput"))

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
    ) -> typing.Optional["ComputeInstanceFromTemplateConfidentialInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateConfidentialInstanceConfig"], jsii.get(self, "confidentialInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStatusInput")
    def desired_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDisplayInput")
    def enable_display_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDisplayInput"))

    @builtins.property
    @jsii.member(jsii_name="guestAcceleratorInput")
    def guest_accelerator_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateGuestAccelerator"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateGuestAccelerator"]]], jsii.get(self, "guestAcceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceEncryptionKeyInput")
    def instance_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateInstanceEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateInstanceEncryptionKey"], jsii.get(self, "instanceEncryptionKeyInput"))

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
    @jsii.member(jsii_name="networkInterfaceInput")
    def network_interface_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfigInput")
    def network_performance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateNetworkPerformanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateNetworkPerformanceConfig"], jsii.get(self, "networkPerformanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeInstanceFromTemplateParams"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateReservationAffinity"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoliciesInput")
    def resource_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcePoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateScheduling"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="scratchDiskInput")
    def scratch_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateScratchDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateScratchDisk"]]], jsii.get(self, "scratchDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateServiceAccount"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateServiceAccount"], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplateInput")
    def source_instance_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstanceTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceFromTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceFromTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="allowStoppingForUpdate")
    def allow_stopping_for_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowStoppingForUpdate"))

    @allow_stopping_for_update.setter
    def allow_stopping_for_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07e9705b5f013901ff56c8841bf8548dd8cf737b56eb576e3f0f9afcf07bc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowStoppingForUpdate", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__90a8f24ba5e384de867395dadd3d61ebf37b640b06822cd6a6020b8a4235ceac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canIpForward", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862490ea015e40356bb0f0631681a158b0be717408abe19834c070f5731ed66b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc3853607653bad7fad357c5bf50410fd28ebb1f9b935ae61e274546f32ecec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredStatus")
    def desired_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredStatus"))

    @desired_status.setter
    def desired_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a1cf26738e8f5e12422ce037d5884beb30385cdf4d8765b801394249d84950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDisplay")
    def enable_display(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDisplay"))

    @enable_display.setter
    def enable_display(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6f1c08bc1e5a895eb75450bc72c62c3978e9a50823e04fa39f85cf51e980bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDisplay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86690719363fbe0722cc19638ed108c0e58bf3de135e37d6feb89a2d74e97e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a8d523c0ef29a48e41153bb12c136cb6cd65ae179fc396233c83f891578897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyRevocationActionType")
    def key_revocation_action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRevocationActionType"))

    @key_revocation_action_type.setter
    def key_revocation_action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba413f81113eb78c5a0311cc459c01a6aa4c1193714fdef010d315757b7106f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRevocationActionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d180637448a48a3d002438a1e16da3e0febd5cc6a14a0c0064ef073c48a14d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9377fd6fa32f761cba9fdf8e8c04397751a36f78f1c2a8b4d753b54674c1b145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdd646c9d03fa3b0aa2f97865c5c4e8b14c756d8c38a103ada18b26ac21632f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataStartupScript")
    def metadata_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataStartupScript"))

    @metadata_startup_script.setter
    def metadata_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e270053afbd5695d0f10fa209b9fe7511b1e0469aa7fa4591a9654dadd3913b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc31b59384ebcbbfd7ae0ae74ca1b1e0bc66aa34807b4ce32204c49ec0ae1a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b911f4a91f6ea031e663ccdaa2f0d3aa6c3133f321ed583b0451622729edc025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7d6d8cfdffd3e824023624ccd71e2ffe8dbdcd84ff3dc9874c2911c8012b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bd05fc4c124fcace57ffdc8f50d757fd983832dff59c06309e0d5b1665f0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstanceTemplate")
    def source_instance_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstanceTemplate"))

    @source_instance_template.setter
    def source_instance_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869732f927acbd4478ddf44be4bfa6419eb61306e47d60f930cb64e0abde7c13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstanceTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f50cb5795a6043b996800d00d36c5e141fda50b7f285b150c925cb4149316c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2661c1484b6e13c44536e6f5c1ab371e33daab81f3fb76e4a6d8644f86c10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateAdvancedMachineFeatures",
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
class ComputeInstanceFromTemplateAdvancedMachineFeatures:
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_nested_virtualization ComputeInstanceFromTemplate#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_uefi_networking ComputeInstanceFromTemplate#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#performance_monitoring_unit ComputeInstanceFromTemplate#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#threads_per_core ComputeInstanceFromTemplate#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#turbo_mode ComputeInstanceFromTemplate#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#visible_core_count ComputeInstanceFromTemplate#visible_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11be50a7e28ab76bbf149f69ca128c858934fca2cb97b8fb26f071101d1ced57)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_nested_virtualization ComputeInstanceFromTemplate#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_uefi_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable UEFI networking for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_uefi_networking ComputeInstanceFromTemplate#enable_uefi_networking}
        '''
        result = self._values.get("enable_uefi_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_monitoring_unit(self) -> typing.Optional[builtins.str]:
        '''The PMU is a hardware component within the CPU core that monitors how the processor runs code.

        Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#performance_monitoring_unit ComputeInstanceFromTemplate#performance_monitoring_unit}
        '''
        result = self._values.get("performance_monitoring_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#threads_per_core ComputeInstanceFromTemplate#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def turbo_mode(self) -> typing.Optional[builtins.str]:
        '''Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#turbo_mode ComputeInstanceFromTemplate#turbo_mode}
        '''
        result = self._values.get("turbo_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visible_core_count(self) -> typing.Optional[jsii.Number]:
        '''The number of physical cores to expose to an instance.

        Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#visible_core_count ComputeInstanceFromTemplate#visible_core_count}
        '''
        result = self._values.get("visible_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a5550afd9eee196b103e8e68edf23ed3e07f0d203df6af68db83fac5402d19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__267023582d07f2a570f6f1de102834eef9a8a509c6177b1528faaa6f912a9b68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1708101c3ebb635e7cd12ab92989a0b8863269ea7eb0cdd646720f89b89e4f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUefiNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnit")
    def performance_monitoring_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceMonitoringUnit"))

    @performance_monitoring_unit.setter
    def performance_monitoring_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06413ee307512439e3da2283cb5d6488d29bbe25aff1f18dc64d89eeb2eb1c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMonitoringUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1da2327c6d658bde3d3c26b563e9d088c29058d0c227b668397260f8735af16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="turboMode")
    def turbo_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "turboMode"))

    @turbo_mode.setter
    def turbo_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade8a0859bc6210dfc2c757737b2f37f0355b49df9e4d4f465f9d9b04ccd526e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "turboMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibleCoreCount")
    def visible_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "visibleCoreCount"))

    @visible_core_count.setter
    def visible_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__435a8715913b8af94187f56fcbcf5e24ebc97712e01f535f4f624b1a02d1e6b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibleCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb4960269b6663edd643dff7cb4449e61eb70a10fae241c5c252b055777264e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateAttachedDisk",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "device_name": "deviceName",
        "disk_encryption_key_raw": "diskEncryptionKeyRaw",
        "disk_encryption_key_rsa": "diskEncryptionKeyRsa",
        "disk_encryption_service_account": "diskEncryptionServiceAccount",
        "force_attach": "forceAttach",
        "kms_key_self_link": "kmsKeySelfLink",
        "mode": "mode",
    },
)
class ComputeInstanceFromTemplateAttachedDisk:
    def __init__(
        self,
        *,
        source: builtins.str,
        device_name: typing.Optional[builtins.str] = None,
        disk_encryption_key_raw: typing.Optional[builtins.str] = None,
        disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
        disk_encryption_service_account: typing.Optional[builtins.str] = None,
        force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source ComputeInstanceFromTemplate#source}
        :param device_name: Name with which the attached disk is accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_raw ComputeInstanceFromTemplate#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_rsa ComputeInstanceFromTemplate#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_service_account ComputeInstanceFromTemplate#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#force_attach ComputeInstanceFromTemplate#force_attach}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#mode ComputeInstanceFromTemplate#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0472425de7657cd3c80ddc34a8a5fc3a621e4f26183b45d1ca4779a3645e55)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument disk_encryption_key_raw", value=disk_encryption_key_raw, expected_type=type_hints["disk_encryption_key_raw"])
            check_type(argname="argument disk_encryption_key_rsa", value=disk_encryption_key_rsa, expected_type=type_hints["disk_encryption_key_rsa"])
            check_type(argname="argument disk_encryption_service_account", value=disk_encryption_service_account, expected_type=type_hints["disk_encryption_service_account"])
            check_type(argname="argument force_attach", value=force_attach, expected_type=type_hints["force_attach"])
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if device_name is not None:
            self._values["device_name"] = device_name
        if disk_encryption_key_raw is not None:
            self._values["disk_encryption_key_raw"] = disk_encryption_key_raw
        if disk_encryption_key_rsa is not None:
            self._values["disk_encryption_key_rsa"] = disk_encryption_key_rsa
        if disk_encryption_service_account is not None:
            self._values["disk_encryption_service_account"] = disk_encryption_service_account
        if force_attach is not None:
            self._values["force_attach"] = force_attach
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def source(self) -> builtins.str:
        '''The name or self_link of the disk attached to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source ComputeInstanceFromTemplate#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which the attached disk is accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_raw(self) -> typing.Optional[builtins.str]:
        '''A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_raw ComputeInstanceFromTemplate#disk_encryption_key_raw}
        '''
        result = self._values.get("disk_encryption_key_raw")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_rsa(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_rsa ComputeInstanceFromTemplate#disk_encryption_key_rsa}
        '''
        result = self._values.get("disk_encryption_key_rsa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_service_account ComputeInstanceFromTemplate#disk_encryption_service_account}
        '''
        result = self._values.get("disk_encryption_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_attach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force attach the regional disk even if it's currently attached to another instance.

        If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#force_attach ComputeInstanceFromTemplate#force_attach}
        '''
        result = self._values.get("force_attach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#mode ComputeInstanceFromTemplate#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateAttachedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateAttachedDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateAttachedDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da5a31a6ca2c27fa487368ce257b53a410682b9feb213f75499d87d6f7179e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateAttachedDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e923a9b549a36780325831b242f4aa3454a64aae6f5a115cf3eb7c50bb0cbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateAttachedDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e89552f8844b7b9c25947ce2b81ef72259bba601265a01c0f54e55a62db9fae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a5b9dce11081e7c4a57275972033f7ad05d8caf61b4db84d85c7dbee88cacf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cd3473cd263d69d66bdfa95c2be5ea4df0555107439abb53ff54fe3f622c30d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e13314481467aaa9891120e827b193d3807382ad7616564f83327d436a23d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateAttachedDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateAttachedDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c47f8c89e8d2b8d42aef1f4f970ed7a75566f0e94609bed990f78340f92b7070)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetDiskEncryptionKeyRaw")
    def reset_disk_encryption_key_raw(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKeyRaw", []))

    @jsii.member(jsii_name="resetDiskEncryptionKeyRsa")
    def reset_disk_encryption_key_rsa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKeyRsa", []))

    @jsii.member(jsii_name="resetDiskEncryptionServiceAccount")
    def reset_disk_encryption_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionServiceAccount", []))

    @jsii.member(jsii_name="resetForceAttach")
    def reset_force_attach(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceAttach", []))

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeySha256")
    def disk_encryption_key_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeySha256"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRawInput")
    def disk_encryption_key_raw_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionKeyRawInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsaInput")
    def disk_encryption_key_rsa_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionKeyRsaInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccountInput")
    def disk_encryption_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="forceAttachInput")
    def force_attach_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceAttachInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87de0285ba3f0d9b337ad42253fee454b8a8605f3f17eb46e69edbfc080b4057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRaw")
    def disk_encryption_key_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRaw"))

    @disk_encryption_key_raw.setter
    def disk_encryption_key_raw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1465b85f013704a14cac2300f2ec6b9b92fa7d2b27f569fc37f264c568cb3dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsa")
    def disk_encryption_key_rsa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRsa"))

    @disk_encryption_key_rsa.setter
    def disk_encryption_key_rsa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea009c57c6aee2b2dea4639c2033f0b271d6af912735dbfff2b8a45cf2ef2367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRsa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccount")
    def disk_encryption_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionServiceAccount"))

    @disk_encryption_service_account.setter
    def disk_encryption_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e1415744ffb9fd99d8364d3e8a68bddba52008943769a8f386cbaf18143db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceAttach")
    def force_attach(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceAttach"))

    @force_attach.setter
    def force_attach(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2de14fe8713c1d078345a043d01166c62f8fb8c914a18e38d80a3a3cc23d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceAttach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f18efbe87c1c1f2538c0ce32012ec6b8b4eed99b2642ee7661d8cd4ba9e40d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c05f016a3dbe0c5bca6a705b4f6304a991fbef08b0ce30dc561ff96e415d8c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5befff7eb15e2001db5e86e93525aff1bb4c0453b175765efab4a8680985b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateAttachedDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateAttachedDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateAttachedDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467285fa4d811d3ceb6521a6ba59231d455c553d726cae9c206ddab481d6a147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDisk",
    jsii_struct_bases=[],
    name_mapping={
        "auto_delete": "autoDelete",
        "device_name": "deviceName",
        "disk_encryption_key_raw": "diskEncryptionKeyRaw",
        "disk_encryption_key_rsa": "diskEncryptionKeyRsa",
        "disk_encryption_service_account": "diskEncryptionServiceAccount",
        "force_attach": "forceAttach",
        "guest_os_features": "guestOsFeatures",
        "initialize_params": "initializeParams",
        "interface": "interface",
        "kms_key_self_link": "kmsKeySelfLink",
        "mode": "mode",
        "source": "source",
    },
)
class ComputeInstanceFromTemplateBootDisk:
    def __init__(
        self,
        *,
        auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        device_name: typing.Optional[builtins.str] = None,
        disk_encryption_key_raw: typing.Optional[builtins.str] = None,
        disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
        disk_encryption_service_account: typing.Optional[builtins.str] = None,
        force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
        initialize_params: typing.Optional[typing.Union["ComputeInstanceFromTemplateBootDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete: Whether the disk will be auto-deleted when the instance is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#auto_delete ComputeInstanceFromTemplate#auto_delete}
        :param device_name: Name with which attached disk will be accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_raw ComputeInstanceFromTemplate#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_rsa ComputeInstanceFromTemplate#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_service_account ComputeInstanceFromTemplate#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#force_attach ComputeInstanceFromTemplate#force_attach}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_os_features ComputeInstanceFromTemplate#guest_os_features}
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#initialize_params ComputeInstanceFromTemplate#initialize_params}
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#interface ComputeInstanceFromTemplate#interface}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#mode ComputeInstanceFromTemplate#mode}
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source ComputeInstanceFromTemplate#source}
        '''
        if isinstance(initialize_params, dict):
            initialize_params = ComputeInstanceFromTemplateBootDiskInitializeParams(**initialize_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9daaccb37d7f482f186a649a6b98f91648e2f4fc825f2e9ab7a632441f110d)
            check_type(argname="argument auto_delete", value=auto_delete, expected_type=type_hints["auto_delete"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument disk_encryption_key_raw", value=disk_encryption_key_raw, expected_type=type_hints["disk_encryption_key_raw"])
            check_type(argname="argument disk_encryption_key_rsa", value=disk_encryption_key_rsa, expected_type=type_hints["disk_encryption_key_rsa"])
            check_type(argname="argument disk_encryption_service_account", value=disk_encryption_service_account, expected_type=type_hints["disk_encryption_service_account"])
            check_type(argname="argument force_attach", value=force_attach, expected_type=type_hints["force_attach"])
            check_type(argname="argument guest_os_features", value=guest_os_features, expected_type=type_hints["guest_os_features"])
            check_type(argname="argument initialize_params", value=initialize_params, expected_type=type_hints["initialize_params"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_delete is not None:
            self._values["auto_delete"] = auto_delete
        if device_name is not None:
            self._values["device_name"] = device_name
        if disk_encryption_key_raw is not None:
            self._values["disk_encryption_key_raw"] = disk_encryption_key_raw
        if disk_encryption_key_rsa is not None:
            self._values["disk_encryption_key_rsa"] = disk_encryption_key_rsa
        if disk_encryption_service_account is not None:
            self._values["disk_encryption_service_account"] = disk_encryption_service_account
        if force_attach is not None:
            self._values["force_attach"] = force_attach
        if guest_os_features is not None:
            self._values["guest_os_features"] = guest_os_features
        if initialize_params is not None:
            self._values["initialize_params"] = initialize_params
        if interface is not None:
            self._values["interface"] = interface
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if mode is not None:
            self._values["mode"] = mode
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def auto_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the disk will be auto-deleted when the instance is deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#auto_delete ComputeInstanceFromTemplate#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which attached disk will be accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_raw(self) -> typing.Optional[builtins.str]:
        '''A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_raw ComputeInstanceFromTemplate#disk_encryption_key_raw}
        '''
        result = self._values.get("disk_encryption_key_raw")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_rsa(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_key_rsa ComputeInstanceFromTemplate#disk_encryption_key_rsa}
        '''
        result = self._values.get("disk_encryption_key_rsa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#disk_encryption_service_account ComputeInstanceFromTemplate#disk_encryption_service_account}
        '''
        result = self._values.get("disk_encryption_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_attach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force attach the regional disk even if it's currently attached to another instance.

        If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#force_attach ComputeInstanceFromTemplate#force_attach}
        '''
        result = self._values.get("force_attach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_os_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of features to enable on the guest operating system. Applicable only for bootable images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_os_features ComputeInstanceFromTemplate#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def initialize_params(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParams"]:
        '''initialize_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#initialize_params ComputeInstanceFromTemplate#initialize_params}
        '''
        result = self._values.get("initialize_params")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParams"], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''The disk interface used for attaching this disk.

        One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#interface ComputeInstanceFromTemplate#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#mode ComputeInstanceFromTemplate#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the disk attached to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source ComputeInstanceFromTemplate#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateBootDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParams",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "enable_confidential_compute": "enableConfidentialCompute",
        "image": "image",
        "labels": "labels",
        "provisioned_iops": "provisionedIops",
        "provisioned_throughput": "provisionedThroughput",
        "resource_manager_tags": "resourceManagerTags",
        "resource_policies": "resourcePolicies",
        "size": "size",
        "snapshot": "snapshot",
        "source_image_encryption_key": "sourceImageEncryptionKey",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "storage_pool": "storagePool",
        "type": "type",
    },
)
class ComputeInstanceFromTemplateBootDiskInitializeParams:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the disk. One of "X86_64" or "ARM64". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#architecture ComputeInstanceFromTemplate#architecture}
        :param enable_confidential_compute: A flag to enable confidential compute mode on boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        :param image: The image from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#image ComputeInstanceFromTemplate#image}
        :param labels: A set of key/value label pairs assigned to the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_iops ComputeInstanceFromTemplate#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_throughput ComputeInstanceFromTemplate#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance's boot disk. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        :param size: The size of the image in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#size ComputeInstanceFromTemplate#size}
        :param snapshot: The snapshot from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#snapshot ComputeInstanceFromTemplate#snapshot}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_image_encryption_key ComputeInstanceFromTemplate#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_snapshot_encryption_key ComputeInstanceFromTemplate#source_snapshot_encryption_key}
        :param storage_pool: The URL of the storage pool in which the new disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#storage_pool ComputeInstanceFromTemplate#storage_pool}
        :param type: The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c43290875167e467d184f760e883b7d7bac501946d12ad7bcebf6119b99edf6c)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument enable_confidential_compute", value=enable_confidential_compute, expected_type=type_hints["enable_confidential_compute"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument provisioned_iops", value=provisioned_iops, expected_type=type_hints["provisioned_iops"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
            check_type(argname="argument resource_policies", value=resource_policies, expected_type=type_hints["resource_policies"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument source_image_encryption_key", value=source_image_encryption_key, expected_type=type_hints["source_image_encryption_key"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument storage_pool", value=storage_pool, expected_type=type_hints["storage_pool"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if enable_confidential_compute is not None:
            self._values["enable_confidential_compute"] = enable_confidential_compute
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if provisioned_iops is not None:
            self._values["provisioned_iops"] = provisioned_iops
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags
        if resource_policies is not None:
            self._values["resource_policies"] = resource_policies
        if size is not None:
            self._values["size"] = size
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if source_image_encryption_key is not None:
            self._values["source_image_encryption_key"] = source_image_encryption_key
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if storage_pool is not None:
            self._values["storage_pool"] = storage_pool
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The architecture of the disk. One of "X86_64" or "ARM64".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#architecture ComputeInstanceFromTemplate#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag to enable confidential compute mode on boot disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''The image from which this disk was initialised.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#image ComputeInstanceFromTemplate#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs assigned to the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS to provision for the disk.

        This sets the number of I/O operations per second that the disk can handle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_iops ComputeInstanceFromTemplate#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much throughput to provision for the disk.

        This sets the number of throughput mb per second that the disk can handle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_throughput ComputeInstanceFromTemplate#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance's boot disk.

        Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the image in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#size ComputeInstanceFromTemplate#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot(self) -> typing.Optional[builtins.str]:
        '''The snapshot from which this disk was initialised.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#snapshot ComputeInstanceFromTemplate#snapshot}
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_image_encryption_key ComputeInstanceFromTemplate#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_snapshot_encryption_key ComputeInstanceFromTemplate#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def storage_pool(self) -> typing.Optional[builtins.str]:
        '''The URL of the storage pool in which the new disk is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#storage_pool ComputeInstanceFromTemplate#storage_pool}
        '''
        result = self._values.get("storage_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateBootDiskInitializeParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateBootDiskInitializeParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a2848a2300de7685ef88373c9b81165a8174c1a3a2801e3aca5b74e86fc6d55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        value = ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey(
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        value = ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceSnapshotEncryptionKey", [value]))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetEnableConfidentialCompute")
    def reset_enable_confidential_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialCompute", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

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

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetSourceImageEncryptionKey")
    def reset_source_image_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageEncryptionKey", []))

    @jsii.member(jsii_name="resetSourceSnapshotEncryptionKey")
    def reset_source_snapshot_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshotEncryptionKey", []))

    @jsii.member(jsii_name="resetStoragePool")
    def reset_storage_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoragePool", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialComputeInput")
    def enable_confidential_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

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
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotInput")
    def snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKeyInput")
    def source_image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolInput")
    def storage_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a74dd879d10cf8f3d85663b42392e55bd6c7607f445cb08b327f75ca5a36bd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__37e202f6731e00a728b5b33e17459b62cd35752b87dc5918c905d8638e6d7e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacdc3db458fe91622c27e3e9a5361dfb4fd331ffe8e591c201e490c74967407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ea74d843629481ed6254cb5328ce82e2ce4d1dd43f312b1a48919d792d73e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a54c8d1aa8a3be970ffa3b031f3716ba9210c6bdc74406234a46fd60b9ac1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b345c8e18c974c18869564927e1800cdb2299888aaf99b66500c6842795a74a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f78198546dc63e59a8536c5c269e9ff246139ac08708bf1e3c6f8039fa35b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92eb080a097b9a15bde7157787dad633d7d3f6b186b38b992e6f037c22e21fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe5f467dce7a811b1150b1815bc6fb8cf17e6a52bd1fe1fb02a2cc11b151922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @snapshot.setter
    def snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fdcd371dd6f2c180ccfd5ca16e2941990e559f89dc9547969e6be2f590d0a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbeffbe2e790d7331b8682ea84ace0f64176615c735bae9a1be7848710e59b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee963abf7008e105d6a19af9405e9f74b0d6d12e91d68aece9967826711125f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84865fa8e6495b7faaad67417306f56c69742a3492841152a6d7d260ef980bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4ee3a30a110932668bbba67ad7a31afd4a66bc4a31cf76ebd54f265da39bf3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da1fc821f2723fe995e7654ffd398401f5288a72e058c233910cdfaa065a3101)
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
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a1d508b26461be832498af079e198aeb830696b4c7fe0b0208e7e037996c8e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28966121dca933f46bcf0018116eda10db4064f37aa79a4e03009c23eed18b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267c020da86af75062ac4ecd8a5b55abe72b4b928c5a54de9ba3336925279b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428bd8910d97c660920743ead7660d51a946b9b0ae031e1b4d375931883cf953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ffd62291c405a357da596158576f930ccb6c14dc03e4ef5ca7fc663e78cd6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245f28686355d583457fd9f86d093e91eac0abc5f1330fce691cc1576c2674bd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#raw_key ComputeInstanceFromTemplate#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#rsa_encrypted_key ComputeInstanceFromTemplate#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d9f2f4ea9f387f6ee555cf913882e2a9c0cfc215ef71b41e46282e395c7a5d)
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
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a4c2b15212cef2b14e8d26a48e2754d6a55926a2f5ad0c0635e99bb18730d0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69db9db38a438da344ec89fb550377043c8a37f110f484325d3b71863ffc8430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02273a808f61db70a41f8d1c0a3c38a34e671c772f1d6b79f8ddba5c035d018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e861b85747371be64af5abca3a851362743c4447fd1ad14e38d3779f9086947d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca0035fbff8d89b3adbb266bb768f3a55beea5a1c81d660f01929c2e57d7b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateBootDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateBootDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18246e52fc616b22e8d5ce252bbb8b11d56af565996bc42c2231c8daaddb3c07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInitializeParams")
    def put_initialize_params(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the disk. One of "X86_64" or "ARM64". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#architecture ComputeInstanceFromTemplate#architecture}
        :param enable_confidential_compute: A flag to enable confidential compute mode on boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        :param image: The image from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#image ComputeInstanceFromTemplate#image}
        :param labels: A set of key/value label pairs assigned to the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_iops ComputeInstanceFromTemplate#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioned_throughput ComputeInstanceFromTemplate#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance's boot disk. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        :param size: The size of the image in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#size ComputeInstanceFromTemplate#size}
        :param snapshot: The snapshot from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#snapshot ComputeInstanceFromTemplate#snapshot}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_image_encryption_key ComputeInstanceFromTemplate#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_snapshot_encryption_key ComputeInstanceFromTemplate#source_snapshot_encryption_key}
        :param storage_pool: The URL of the storage pool in which the new disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#storage_pool ComputeInstanceFromTemplate#storage_pool}
        :param type: The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        value = ComputeInstanceFromTemplateBootDiskInitializeParams(
            architecture=architecture,
            enable_confidential_compute=enable_confidential_compute,
            image=image,
            labels=labels,
            provisioned_iops=provisioned_iops,
            provisioned_throughput=provisioned_throughput,
            resource_manager_tags=resource_manager_tags,
            resource_policies=resource_policies,
            size=size,
            snapshot=snapshot,
            source_image_encryption_key=source_image_encryption_key,
            source_snapshot_encryption_key=source_snapshot_encryption_key,
            storage_pool=storage_pool,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putInitializeParams", [value]))

    @jsii.member(jsii_name="resetAutoDelete")
    def reset_auto_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDelete", []))

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetDiskEncryptionKeyRaw")
    def reset_disk_encryption_key_raw(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKeyRaw", []))

    @jsii.member(jsii_name="resetDiskEncryptionKeyRsa")
    def reset_disk_encryption_key_rsa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKeyRsa", []))

    @jsii.member(jsii_name="resetDiskEncryptionServiceAccount")
    def reset_disk_encryption_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionServiceAccount", []))

    @jsii.member(jsii_name="resetForceAttach")
    def reset_force_attach(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceAttach", []))

    @jsii.member(jsii_name="resetGuestOsFeatures")
    def reset_guest_os_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestOsFeatures", []))

    @jsii.member(jsii_name="resetInitializeParams")
    def reset_initialize_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializeParams", []))

    @jsii.member(jsii_name="resetInterface")
    def reset_interface(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterface", []))

    @jsii.member(jsii_name="resetKmsKeySelfLink")
    def reset_kms_key_self_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeySelfLink", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeySha256")
    def disk_encryption_key_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeySha256"))

    @builtins.property
    @jsii.member(jsii_name="initializeParams")
    def initialize_params(
        self,
    ) -> ComputeInstanceFromTemplateBootDiskInitializeParamsOutputReference:
        return typing.cast(ComputeInstanceFromTemplateBootDiskInitializeParamsOutputReference, jsii.get(self, "initializeParams"))

    @builtins.property
    @jsii.member(jsii_name="autoDeleteInput")
    def auto_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRawInput")
    def disk_encryption_key_raw_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionKeyRawInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsaInput")
    def disk_encryption_key_rsa_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionKeyRsaInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccountInput")
    def disk_encryption_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="forceAttachInput")
    def force_attach_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceAttachInput"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeaturesInput")
    def guest_os_features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "guestOsFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="initializeParamsInput")
    def initialize_params_input(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams], jsii.get(self, "initializeParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLinkInput")
    def kms_key_self_link_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeySelfLinkInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3f144bb37c858742fcb642ea4b3f668615c2635ef7d9e6014269a67401e47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291e7ba58b52b4b28a042d61fef7a4db34047a213f978a29bfbc0a0609279ee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRaw")
    def disk_encryption_key_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRaw"))

    @disk_encryption_key_raw.setter
    def disk_encryption_key_raw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ac7cadd8aa090eb3d1207c78a0c99b5e73b0a4f8ff0839f98eef484d87b31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsa")
    def disk_encryption_key_rsa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRsa"))

    @disk_encryption_key_rsa.setter
    def disk_encryption_key_rsa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a66405c849acc5574261fe4094a6bea4b9db1cbe722df4a2941d00dd4dd31d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRsa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccount")
    def disk_encryption_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionServiceAccount"))

    @disk_encryption_service_account.setter
    def disk_encryption_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae445a43371e8a72f95475c0598d01c1d847143aecac79576924eccf530d0fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceAttach")
    def force_attach(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceAttach"))

    @force_attach.setter
    def force_attach(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c49209f79de058e0b7575594f7d83b04a552464d27904262954884e9c4a605a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceAttach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "guestOsFeatures"))

    @guest_os_features.setter
    def guest_os_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfec923a9d1bc148be10f812d89ec28117b218a42829effd7eb4d8424cdee229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestOsFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5e52e0df903939fbab4ba403e0e0aa5d0ace6a57d13806e1b192453947b732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1047b0368a4a068686e698c1405a818f950ddd7bf56dfcdddde552cbfb3f9246)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8f7a961c5ecb083cef8ecaf29c3945ed408998f13f2eefab2a2b89cc771405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0131e011b1d92dcbe99501802d1b6e39f20da029ff48f3b88ca3a1fe628d2572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceFromTemplateBootDisk]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateBootDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5f694ebf278fba382dcb460452ff77473471283ea8ebb5f280a6b622469b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidential_instance_type": "confidentialInstanceType",
        "enable_confidential_compute": "enableConfidentialCompute",
    },
)
class ComputeInstanceFromTemplateConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_type ComputeInstanceFromTemplate#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eca2f5d5aafa2dc5ccbf8cc7fa64669eb1bac438f9db7f173d8e3cd782e6ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_type ComputeInstanceFromTemplate#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_confidential_compute ComputeInstanceFromTemplate#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__752e17e1df75abc370399c5391314e6fe89ad7f688cebd6292cc50f5ee8179e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25da22463144e82d16b643b9661fd57b8de5caf206bff936a68cc39bbee691cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4d1242438d9c6d80eea4ed206752c0f4d17058087d68b204aecf4fe293cbc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df391f44098e98d49697686cbf98a7c19e3f4c4c0827eb2a597035d2a8ec53de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateConfig",
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
        "source_instance_template": "sourceInstanceTemplate",
        "advanced_machine_features": "advancedMachineFeatures",
        "allow_stopping_for_update": "allowStoppingForUpdate",
        "attached_disk": "attachedDisk",
        "boot_disk": "bootDisk",
        "can_ip_forward": "canIpForward",
        "confidential_instance_config": "confidentialInstanceConfig",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "desired_status": "desiredStatus",
        "enable_display": "enableDisplay",
        "guest_accelerator": "guestAccelerator",
        "hostname": "hostname",
        "id": "id",
        "instance_encryption_key": "instanceEncryptionKey",
        "key_revocation_action_type": "keyRevocationActionType",
        "labels": "labels",
        "machine_type": "machineType",
        "metadata": "metadata",
        "metadata_startup_script": "metadataStartupScript",
        "min_cpu_platform": "minCpuPlatform",
        "network_interface": "networkInterface",
        "network_performance_config": "networkPerformanceConfig",
        "params": "params",
        "project": "project",
        "reservation_affinity": "reservationAffinity",
        "resource_policies": "resourcePolicies",
        "scheduling": "scheduling",
        "scratch_disk": "scratchDisk",
        "service_account": "serviceAccount",
        "shielded_instance_config": "shieldedInstanceConfig",
        "tags": "tags",
        "timeouts": "timeouts",
        "zone": "zone",
    },
)
class ComputeInstanceFromTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        source_instance_template: builtins.str,
        advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceFromTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
        boot_disk: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_status: typing.Optional[builtins.str] = None,
        enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_encryption_key: typing.Optional[typing.Union["ComputeInstanceFromTemplateInstanceEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_type: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterface", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceFromTemplateNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeInstanceFromTemplateParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceFromTemplateReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceFromTemplateScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateScratchDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceFromTemplateServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceFromTemplateShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceFromTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the instance. One of name or self_link must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#name ComputeInstanceFromTemplate#name}
        :param source_instance_template: Name or self link of an instance template to create the instance based on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_instance_template ComputeInstanceFromTemplate#source_instance_template}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#advanced_machine_features ComputeInstanceFromTemplate#advanced_machine_features}
        :param allow_stopping_for_update: If true, allows Terraform to stop the instance to update its properties. If you try to update a property that requires stopping the instance without setting this field, the update will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#allow_stopping_for_update ComputeInstanceFromTemplate#allow_stopping_for_update}
        :param attached_disk: attached_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#attached_disk ComputeInstanceFromTemplate#attached_disk}
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#boot_disk ComputeInstanceFromTemplate#boot_disk}
        :param can_ip_forward: Whether sending and receiving of packets with non-matching source or destination IPs is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#can_ip_forward ComputeInstanceFromTemplate#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_config ComputeInstanceFromTemplate#confidential_instance_config}
        :param deletion_protection: Whether deletion protection is enabled on this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#deletion_protection ComputeInstanceFromTemplate#deletion_protection}
        :param description: A brief description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#description ComputeInstanceFromTemplate#description}
        :param desired_status: Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#desired_status ComputeInstanceFromTemplate#desired_status}
        :param enable_display: Whether the instance has virtual displays enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_display ComputeInstanceFromTemplate#enable_display}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_accelerator ComputeInstanceFromTemplate#guest_accelerator}
        :param hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#hostname ComputeInstanceFromTemplate#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#id ComputeInstanceFromTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_encryption_key: instance_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_encryption_key ComputeInstanceFromTemplate#instance_encryption_key}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key_revocation_action_type ComputeInstanceFromTemplate#key_revocation_action_type}
        :param labels: A set of key/value label pairs assigned to the instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        :param machine_type: The machine type to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#machine_type ComputeInstanceFromTemplate#machine_type}
        :param metadata: Metadata key/value pairs made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata ComputeInstanceFromTemplate#metadata}
        :param metadata_startup_script: Metadata startup scripts made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata_startup_script ComputeInstanceFromTemplate#metadata_startup_script}
        :param min_cpu_platform: The minimum CPU platform specified for the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_cpu_platform ComputeInstanceFromTemplate#min_cpu_platform}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_interface ComputeInstanceFromTemplate#network_interface}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_performance_config ComputeInstanceFromTemplate#network_performance_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#params ComputeInstanceFromTemplate#params}
        :param project: The ID of the project in which the resource belongs. If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#project ComputeInstanceFromTemplate#project}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#reservation_affinity ComputeInstanceFromTemplate#reservation_affinity}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scheduling ComputeInstanceFromTemplate#scheduling}
        :param scratch_disk: scratch_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scratch_disk ComputeInstanceFromTemplate#scratch_disk}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#service_account ComputeInstanceFromTemplate#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#shielded_instance_config ComputeInstanceFromTemplate#shielded_instance_config}
        :param tags: The list of tags attached to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#tags ComputeInstanceFromTemplate#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#timeouts ComputeInstanceFromTemplate#timeouts}
        :param zone: The zone of the instance. If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#zone ComputeInstanceFromTemplate#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = ComputeInstanceFromTemplateAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(boot_disk, dict):
            boot_disk = ComputeInstanceFromTemplateBootDisk(**boot_disk)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = ComputeInstanceFromTemplateConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(instance_encryption_key, dict):
            instance_encryption_key = ComputeInstanceFromTemplateInstanceEncryptionKey(**instance_encryption_key)
        if isinstance(network_performance_config, dict):
            network_performance_config = ComputeInstanceFromTemplateNetworkPerformanceConfig(**network_performance_config)
        if isinstance(params, dict):
            params = ComputeInstanceFromTemplateParams(**params)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = ComputeInstanceFromTemplateReservationAffinity(**reservation_affinity)
        if isinstance(scheduling, dict):
            scheduling = ComputeInstanceFromTemplateScheduling(**scheduling)
        if isinstance(service_account, dict):
            service_account = ComputeInstanceFromTemplateServiceAccount(**service_account)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = ComputeInstanceFromTemplateShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceFromTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed7912504b0e71b044d42bf8efadad4d400bb2eac9a7ffca5a7f1ae085368a1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_instance_template", value=source_instance_template, expected_type=type_hints["source_instance_template"])
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument allow_stopping_for_update", value=allow_stopping_for_update, expected_type=type_hints["allow_stopping_for_update"])
            check_type(argname="argument attached_disk", value=attached_disk, expected_type=type_hints["attached_disk"])
            check_type(argname="argument boot_disk", value=boot_disk, expected_type=type_hints["boot_disk"])
            check_type(argname="argument can_ip_forward", value=can_ip_forward, expected_type=type_hints["can_ip_forward"])
            check_type(argname="argument confidential_instance_config", value=confidential_instance_config, expected_type=type_hints["confidential_instance_config"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_status", value=desired_status, expected_type=type_hints["desired_status"])
            check_type(argname="argument enable_display", value=enable_display, expected_type=type_hints["enable_display"])
            check_type(argname="argument guest_accelerator", value=guest_accelerator, expected_type=type_hints["guest_accelerator"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_encryption_key", value=instance_encryption_key, expected_type=type_hints["instance_encryption_key"])
            check_type(argname="argument key_revocation_action_type", value=key_revocation_action_type, expected_type=type_hints["key_revocation_action_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_startup_script", value=metadata_startup_script, expected_type=type_hints["metadata_startup_script"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument network_performance_config", value=network_performance_config, expected_type=type_hints["network_performance_config"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument resource_policies", value=resource_policies, expected_type=type_hints["resource_policies"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument scratch_disk", value=scratch_disk, expected_type=type_hints["scratch_disk"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source_instance_template": source_instance_template,
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
        if allow_stopping_for_update is not None:
            self._values["allow_stopping_for_update"] = allow_stopping_for_update
        if attached_disk is not None:
            self._values["attached_disk"] = attached_disk
        if boot_disk is not None:
            self._values["boot_disk"] = boot_disk
        if can_ip_forward is not None:
            self._values["can_ip_forward"] = can_ip_forward
        if confidential_instance_config is not None:
            self._values["confidential_instance_config"] = confidential_instance_config
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if desired_status is not None:
            self._values["desired_status"] = desired_status
        if enable_display is not None:
            self._values["enable_display"] = enable_display
        if guest_accelerator is not None:
            self._values["guest_accelerator"] = guest_accelerator
        if hostname is not None:
            self._values["hostname"] = hostname
        if id is not None:
            self._values["id"] = id
        if instance_encryption_key is not None:
            self._values["instance_encryption_key"] = instance_encryption_key
        if key_revocation_action_type is not None:
            self._values["key_revocation_action_type"] = key_revocation_action_type
        if labels is not None:
            self._values["labels"] = labels
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_startup_script is not None:
            self._values["metadata_startup_script"] = metadata_startup_script
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
        if network_interface is not None:
            self._values["network_interface"] = network_interface
        if network_performance_config is not None:
            self._values["network_performance_config"] = network_performance_config
        if params is not None:
            self._values["params"] = params
        if project is not None:
            self._values["project"] = project
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if resource_policies is not None:
            self._values["resource_policies"] = resource_policies
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if scratch_disk is not None:
            self._values["scratch_disk"] = scratch_disk
        if service_account is not None:
            self._values["service_account"] = service_account
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone is not None:
            self._values["zone"] = zone

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
        '''The name of the instance. One of name or self_link must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#name ComputeInstanceFromTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_instance_template(self) -> builtins.str:
        '''Name or self link of an instance template to create the instance based on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#source_instance_template ComputeInstanceFromTemplate#source_instance_template}
        '''
        result = self._values.get("source_instance_template")
        assert result is not None, "Required property 'source_instance_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#advanced_machine_features ComputeInstanceFromTemplate#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures], result)

    @builtins.property
    def allow_stopping_for_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, allows Terraform to stop the instance to update its properties.

        If you try to update a property that requires stopping the instance without setting this field, the update will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#allow_stopping_for_update ComputeInstanceFromTemplate#allow_stopping_for_update}
        '''
        result = self._values.get("allow_stopping_for_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def attached_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]]:
        '''attached_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#attached_disk ComputeInstanceFromTemplate#attached_disk}
        '''
        result = self._values.get("attached_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]], result)

    @builtins.property
    def boot_disk(self) -> typing.Optional[ComputeInstanceFromTemplateBootDisk]:
        '''boot_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#boot_disk ComputeInstanceFromTemplate#boot_disk}
        '''
        result = self._values.get("boot_disk")
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateBootDisk], result)

    @builtins.property
    def can_ip_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether sending and receiving of packets with non-matching source or destination IPs is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#can_ip_forward ComputeInstanceFromTemplate#can_ip_forward}
        '''
        result = self._values.get("can_ip_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#confidential_instance_config ComputeInstanceFromTemplate#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether deletion protection is enabled on this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#deletion_protection ComputeInstanceFromTemplate#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#description ComputeInstanceFromTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_status(self) -> typing.Optional[builtins.str]:
        '''Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#desired_status ComputeInstanceFromTemplate#desired_status}
        '''
        result = self._values.get("desired_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_display(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has virtual displays enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_display ComputeInstanceFromTemplate#enable_display}
        '''
        result = self._values.get("enable_display")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#guest_accelerator ComputeInstanceFromTemplate#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateGuestAccelerator"]]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''A custom hostname for the instance.

        Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#hostname ComputeInstanceFromTemplate#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#id ComputeInstanceFromTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateInstanceEncryptionKey"]:
        '''instance_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_encryption_key ComputeInstanceFromTemplate#instance_encryption_key}
        '''
        result = self._values.get("instance_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateInstanceEncryptionKey"], result)

    @builtins.property
    def key_revocation_action_type(self) -> typing.Optional[builtins.str]:
        '''Action to be taken when a customer's encryption key is revoked.

        Supports "STOP" and "NONE", with "NONE" being the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key_revocation_action_type ComputeInstanceFromTemplate#key_revocation_action_type}
        '''
        result = self._values.get("key_revocation_action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs assigned to the instance.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#labels ComputeInstanceFromTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#machine_type ComputeInstanceFromTemplate#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata key/value pairs made available within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata ComputeInstanceFromTemplate#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_startup_script(self) -> typing.Optional[builtins.str]:
        '''Metadata startup scripts made available within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#metadata_startup_script ComputeInstanceFromTemplate#metadata_startup_script}
        '''
        result = self._values.get("metadata_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The minimum CPU platform specified for the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_cpu_platform ComputeInstanceFromTemplate#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterface"]]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_interface ComputeInstanceFromTemplate#network_interface}
        '''
        result = self._values.get("network_interface")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterface"]]], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_performance_config ComputeInstanceFromTemplate#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateNetworkPerformanceConfig"], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeInstanceFromTemplateParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#params ComputeInstanceFromTemplate#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateParams"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#project ComputeInstanceFromTemplate#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#reservation_affinity ComputeInstanceFromTemplate#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateReservationAffinity"], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_policies ComputeInstanceFromTemplate#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["ComputeInstanceFromTemplateScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scheduling ComputeInstanceFromTemplate#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateScheduling"], result)

    @builtins.property
    def scratch_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateScratchDisk"]]]:
        '''scratch_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scratch_disk ComputeInstanceFromTemplate#scratch_disk}
        '''
        result = self._values.get("scratch_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateScratchDisk"]]], result)

    @builtins.property
    def service_account(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#service_account ComputeInstanceFromTemplate#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateServiceAccount"], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#shielded_instance_config ComputeInstanceFromTemplate#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of tags attached to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#tags ComputeInstanceFromTemplate#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceFromTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#timeouts ComputeInstanceFromTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The zone of the instance.

        If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#zone ComputeInstanceFromTemplate#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class ComputeInstanceFromTemplateGuestAccelerator:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#count ComputeInstanceFromTemplate#count}
        :param type: The accelerator type resource exposed to this instance. E.g. nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d411b16899a41ff78cad092ee225fa75666ed0466e7119f8a3ea9c59d9ea52)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#count ComputeInstanceFromTemplate#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource exposed to this instance. E.g. nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateGuestAcceleratorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__946bbfcb1f2b0efbf79aff92a87ccc8f93613b5767a6c2a117cc55dbff7a466e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74193ac4315adf7d86bc2e0dcb9ced301521f044a77b8c76240c25c1ced62b09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e47e17fafe5459ef3fd6be042853718caf0cb22d8a70546dd4d2513dea59467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7f31101c39e06206f4f1605bce1bdb8cacb0b9922cdcb3eb9cc1186ea7b31b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8fc1bd326a810523b336513095836fe309772063c42a174f91426566c2e6232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83be6e0b63000c5baf2fe9b4d72a13449e49f4b115526ddffa2769d26e021ff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateGuestAcceleratorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76583d8e6a66b6f435f4403a9164d4b03e741a7540bd3864b516394192e84a09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__075399178a7dd3d67cd90d1607ffa0aa97934e269c1460c838c18f523831b421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366035b58dc17e62117b601d5d0acb1f66872f8c70b2e42356b9c05ec5764fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda5a3d9f65d3d2a12fbebd08333fa8fde6dc2652b8644d260bb2657afc01021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateInstanceEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
    },
)
class ComputeInstanceFromTemplateInstanceEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b2480c965f49174862c1cfca5aa6190e66c6f0a4b63ccbbfe6b61c01c4d4dc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_self_link ComputeInstanceFromTemplate#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#kms_key_service_account ComputeInstanceFromTemplate#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateInstanceEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateInstanceEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateInstanceEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e641837c9e427615fe3d7305c694ac323dd5ad3392b47093fcdf6ae12785eef)
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
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0a6564134fc8bc9d36159d2be3b6d7161392b600d23bedebcd41708b7be0f7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc83862a06daf2034dcf6f0ffef33fedeb54226c561d533f4b3623f8eed58e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateInstanceEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateInstanceEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateInstanceEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d27edbc73df700f7f6ac66a1dee4d5d85c78f3a279f4295e7ca7dcaba37bd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterface",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "alias_ip_range": "aliasIpRange",
        "internal_ipv6_prefix_length": "internalIpv6PrefixLength",
        "ipv6_access_config": "ipv6AccessConfig",
        "ipv6_address": "ipv6Address",
        "network": "network",
        "network_attachment": "networkAttachment",
        "network_ip": "networkIp",
        "nic_type": "nicType",
        "queue_count": "queueCount",
        "stack_type": "stackType",
        "subnetwork": "subnetwork",
        "subnetwork_project": "subnetworkProject",
    },
)
class ComputeInstanceFromTemplateNetworkInterface:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterfaceAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
        ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ipv6_address: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        network_attachment: typing.Optional[builtins.str] = None,
        network_ip: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        queue_count: typing.Optional[jsii.Number] = None,
        stack_type: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        subnetwork_project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#access_config ComputeInstanceFromTemplate#access_config}
        :param alias_ip_range: alias_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#alias_ip_range ComputeInstanceFromTemplate#alias_ip_range}
        :param internal_ipv6_prefix_length: The prefix length of the primary internal IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#internal_ipv6_prefix_length ComputeInstanceFromTemplate#internal_ipv6_prefix_length}
        :param ipv6_access_config: ipv6_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ipv6_access_config ComputeInstanceFromTemplate#ipv6_access_config}
        :param ipv6_address: An IPv6 internal network address for this network interface. If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ipv6_address ComputeInstanceFromTemplate#ipv6_address}
        :param network: The name or self_link of the network attached to this interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network ComputeInstanceFromTemplate#network}
        :param network_attachment: The URL of the network attachment that this interface should connect to in the following format: projects/{projectNumber}/regions/{region_name}/networkAttachments/{network_attachment_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_attachment ComputeInstanceFromTemplate#network_attachment}
        :param network_ip: The private IP address assigned to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_ip ComputeInstanceFromTemplate#network_ip}
        :param nic_type: The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, IDPF, MRDMA, and IRDMA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nic_type ComputeInstanceFromTemplate#nic_type}
        :param queue_count: The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It will be empty if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#queue_count ComputeInstanceFromTemplate#queue_count}
        :param stack_type: The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#stack_type ComputeInstanceFromTemplate#stack_type}
        :param subnetwork: The name or self_link of the subnetwork attached to this interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork ComputeInstanceFromTemplate#subnetwork}
        :param subnetwork_project: The project in which the subnetwork belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork_project ComputeInstanceFromTemplate#subnetwork_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24120031033231cc4cdd6490c674741b94b44ca3e9d81bf9e0f4078e4ca765b)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument alias_ip_range", value=alias_ip_range, expected_type=type_hints["alias_ip_range"])
            check_type(argname="argument internal_ipv6_prefix_length", value=internal_ipv6_prefix_length, expected_type=type_hints["internal_ipv6_prefix_length"])
            check_type(argname="argument ipv6_access_config", value=ipv6_access_config, expected_type=type_hints["ipv6_access_config"])
            check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
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
        if network_attachment is not None:
            self._values["network_attachment"] = network_attachment
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#access_config ComputeInstanceFromTemplate#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceAccessConfig"]]], result)

    @builtins.property
    def alias_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange"]]]:
        '''alias_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#alias_ip_range ComputeInstanceFromTemplate#alias_ip_range}
        '''
        result = self._values.get("alias_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange"]]], result)

    @builtins.property
    def internal_ipv6_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''The prefix length of the primary internal IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#internal_ipv6_prefix_length ComputeInstanceFromTemplate#internal_ipv6_prefix_length}
        '''
        result = self._values.get("internal_ipv6_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ipv6_access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig"]]]:
        '''ipv6_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ipv6_access_config ComputeInstanceFromTemplate#ipv6_access_config}
        '''
        result = self._values.get("ipv6_access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig"]]], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''An IPv6 internal network address for this network interface.

        If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ipv6_address ComputeInstanceFromTemplate#ipv6_address}
        '''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the network attached to this interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network ComputeInstanceFromTemplate#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_attachment(self) -> typing.Optional[builtins.str]:
        '''The URL of the network attachment that this interface should connect to in the following format: projects/{projectNumber}/regions/{region_name}/networkAttachments/{network_attachment_name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_attachment ComputeInstanceFromTemplate#network_attachment}
        '''
        result = self._values.get("network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_ip(self) -> typing.Optional[builtins.str]:
        '''The private IP address assigned to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_ip ComputeInstanceFromTemplate#network_ip}
        '''
        result = self._values.get("network_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, IDPF, MRDMA, and IRDMA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nic_type ComputeInstanceFromTemplate#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_count(self) -> typing.Optional[jsii.Number]:
        '''The networking queue count that's specified by users for the network interface.

        Both Rx and Tx queues will be set to this number. It will be empty if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#queue_count ComputeInstanceFromTemplate#queue_count}
        '''
        result = self._values.get("queue_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this network interface to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#stack_type ComputeInstanceFromTemplate#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the subnetwork attached to this interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork ComputeInstanceFromTemplate#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_project(self) -> typing.Optional[builtins.str]:
        '''The project in which the subnetwork belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork_project ComputeInstanceFromTemplate#subnetwork_project}
        '''
        result = self._values.get("subnetwork_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "nat_ip": "natIp",
        "network_tier": "networkTier",
        "public_ptr_domain_name": "publicPtrDomainName",
    },
)
class ComputeInstanceFromTemplateNetworkInterfaceAccessConfig:
    def __init__(
        self,
        *,
        nat_ip: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        public_ptr_domain_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nat_ip: The IP address that is be 1:1 mapped to the instance's network ip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nat_ip ComputeInstanceFromTemplate#nat_ip}
        :param network_tier: The networking tier used for configuring this instance. One of PREMIUM or STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_tier ComputeInstanceFromTemplate#network_tier}
        :param public_ptr_domain_name: The DNS domain name for the public PTR record. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#public_ptr_domain_name ComputeInstanceFromTemplate#public_ptr_domain_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ada775bd53e47573cea7a97f75c4f33f607994d21cc7d716b4da7c7c38d03dd)
            check_type(argname="argument nat_ip", value=nat_ip, expected_type=type_hints["nat_ip"])
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
            check_type(argname="argument public_ptr_domain_name", value=public_ptr_domain_name, expected_type=type_hints["public_ptr_domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if nat_ip is not None:
            self._values["nat_ip"] = nat_ip
        if network_tier is not None:
            self._values["network_tier"] = network_tier
        if public_ptr_domain_name is not None:
            self._values["public_ptr_domain_name"] = public_ptr_domain_name

    @builtins.property
    def nat_ip(self) -> typing.Optional[builtins.str]:
        '''The IP address that is be 1:1 mapped to the instance's network ip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nat_ip ComputeInstanceFromTemplate#nat_ip}
        '''
        result = self._values.get("nat_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tier(self) -> typing.Optional[builtins.str]:
        '''The networking tier used for configuring this instance. One of PREMIUM or STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_tier ComputeInstanceFromTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ptr_domain_name(self) -> typing.Optional[builtins.str]:
        '''The DNS domain name for the public PTR record.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#public_ptr_domain_name ComputeInstanceFromTemplate#public_ptr_domain_name}
        '''
        result = self._values.get("public_ptr_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateNetworkInterfaceAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateNetworkInterfaceAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c438a108620bccbc98c9f1ecbcb7eccf50b69d39a5a307cccfe4be8409136d52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateNetworkInterfaceAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7980f2b61133ffd68613f1e9b4bed8cfa309bf56e0a60dc5d29d1b6fae6085df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateNetworkInterfaceAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b7cb2796ee2e7e4acabfc21b3e7eeb1c26e20c49aff0a9ffbe0d30fe5301c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b25e50cbb8f3d5de48d233334f32795b5e4dea8563d35a5532d49e9c00947f93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0634219ff7dafa2b54be4277e4cb01fdf70e5638170d5409b99b57397c52f8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b268108f33af9ef2d7f847e87e7eb2a41c16096dd4ff061f1774bef0d4cae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateNetworkInterfaceAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f4d57a361a5f28b6230b3759bd94b47c29750f15615a32b4baed36c64e4de0f)
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

    @jsii.member(jsii_name="resetPublicPtrDomainName")
    def reset_public_ptr_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicPtrDomainName", []))

    @builtins.property
    @jsii.member(jsii_name="natIpInput")
    def nat_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "natIpInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTierInput")
    def network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainNameInput")
    def public_ptr_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicPtrDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="natIp")
    def nat_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "natIp"))

    @nat_ip.setter
    def nat_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f8887394ac88ce6acf5aa7c93338dd7b0029020b83a6481c36475e067eadfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65302e8edc699c1d6dc798e1658f33b087d54b436662452f71b4c66a2c78e18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @public_ptr_domain_name.setter
    def public_ptr_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa02e9aa4cfe52250e3360d77dfd048d6d4c6704d48e92861a62694c7ba2b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicPtrDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d04aac032dfd978906126f7d148eca2ed843c9764c8e7a8578fb610f146db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "ip_cidr_range": "ipCidrRange",
        "subnetwork_range_name": "subnetworkRangeName",
    },
)
class ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange:
    def __init__(
        self,
        *,
        ip_cidr_range: builtins.str,
        subnetwork_range_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_cidr_range: The IP CIDR range represented by this alias IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ip_cidr_range ComputeInstanceFromTemplate#ip_cidr_range}
        :param subnetwork_range_name: The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork_range_name ComputeInstanceFromTemplate#subnetwork_range_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225c5fa8fad47f18eaf94dec214831690c4821396cef24491b4d8fe2128a2556)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#ip_cidr_range ComputeInstanceFromTemplate#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        assert result is not None, "Required property 'ip_cidr_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnetwork_range_name(self) -> typing.Optional[builtins.str]:
        '''The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#subnetwork_range_name ComputeInstanceFromTemplate#subnetwork_range_name}
        '''
        result = self._values.get("subnetwork_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb83936b088489ac3b79c91e75ae4ad2b7ec872fdf7f45fceb8c68f79d08342c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d444536239fdb26779a179e0a6d97ca74b41aa5d2091be000e291ad8081244d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1209d4d07e491c5f604b2a05d6de9f7b12269e77ab6380560f5952061676bc58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__549b8eb7729ddb8498173b66c59b8ddb54b2ae052b8045c85d6889abb03b3172)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a521407d2518440f3c790b6ed5ab3fb5af4e5fcdc67c334ef9f731184cf9317b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8643fed612be216ef019da9f29afc2bf6cfb7565719df4e4c056493f85f40c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12f0831d0923f67b5143b4249a4aae49f1531e6bd82be0ccfa85faa88723483f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f67132653093bb61295952427c39d2b3e70a773e06deb1368b3a1d3a1c5faf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkRangeName")
    def subnetwork_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkRangeName"))

    @subnetwork_range_name.setter
    def subnetwork_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d153b50cc62301681bed492a174e49e2f8c00b41294c0111863f52e5a2bc8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be7dc6082b658149ae43add2f297a5346aeb3aa96ef5a55816e7b504f403c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "network_tier": "networkTier",
        "external_ipv6": "externalIpv6",
        "external_ipv6_prefix_length": "externalIpv6PrefixLength",
        "name": "name",
        "public_ptr_domain_name": "publicPtrDomainName",
    },
)
class ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig:
    def __init__(
        self,
        *,
        network_tier: builtins.str,
        external_ipv6: typing.Optional[builtins.str] = None,
        external_ipv6_prefix_length: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_ptr_domain_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network_tier: The service-level to be provided for IPv6 traffic when the subnet has an external subnet. Only PREMIUM tier is valid for IPv6 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_tier ComputeInstanceFromTemplate#network_tier}
        :param external_ipv6: The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. To use a static external IP address, it must be unused and in the same region as the instance's zone. If not specified, Google Cloud will automatically assign an external IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#external_ipv6 ComputeInstanceFromTemplate#external_ipv6}
        :param external_ipv6_prefix_length: The prefix length of the external IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#external_ipv6_prefix_length ComputeInstanceFromTemplate#external_ipv6_prefix_length}
        :param name: The name of this access configuration. In ipv6AccessConfigs, the recommended name is External IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#name ComputeInstanceFromTemplate#name}
        :param public_ptr_domain_name: The domain name to be used when creating DNSv6 records for the external IPv6 ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#public_ptr_domain_name ComputeInstanceFromTemplate#public_ptr_domain_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fece5d19f45ad263f1efba088d40d213c89cabb2b14ebcf47ea4b69f13585ae)
            check_type(argname="argument network_tier", value=network_tier, expected_type=type_hints["network_tier"])
            check_type(argname="argument external_ipv6", value=external_ipv6, expected_type=type_hints["external_ipv6"])
            check_type(argname="argument external_ipv6_prefix_length", value=external_ipv6_prefix_length, expected_type=type_hints["external_ipv6_prefix_length"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_ptr_domain_name", value=public_ptr_domain_name, expected_type=type_hints["public_ptr_domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_tier": network_tier,
        }
        if external_ipv6 is not None:
            self._values["external_ipv6"] = external_ipv6
        if external_ipv6_prefix_length is not None:
            self._values["external_ipv6_prefix_length"] = external_ipv6_prefix_length
        if name is not None:
            self._values["name"] = name
        if public_ptr_domain_name is not None:
            self._values["public_ptr_domain_name"] = public_ptr_domain_name

    @builtins.property
    def network_tier(self) -> builtins.str:
        '''The service-level to be provided for IPv6 traffic when the subnet has an external subnet.

        Only PREMIUM tier is valid for IPv6

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#network_tier ComputeInstanceFromTemplate#network_tier}
        '''
        result = self._values.get("network_tier")
        assert result is not None, "Required property 'network_tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_ipv6(self) -> typing.Optional[builtins.str]:
        '''The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig.

        To use a static external IP address, it must be unused and in the same region as the instance's zone. If not specified, Google Cloud will automatically assign an external IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#external_ipv6 ComputeInstanceFromTemplate#external_ipv6}
        '''
        result = self._values.get("external_ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ipv6_prefix_length(self) -> typing.Optional[builtins.str]:
        '''The prefix length of the external IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#external_ipv6_prefix_length ComputeInstanceFromTemplate#external_ipv6_prefix_length}
        '''
        result = self._values.get("external_ipv6_prefix_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access configuration. In ipv6AccessConfigs, the recommended name is External IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#name ComputeInstanceFromTemplate#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ptr_domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name to be used when creating DNSv6 records for the external IPv6 ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#public_ptr_domain_name ComputeInstanceFromTemplate#public_ptr_domain_name}
        '''
        result = self._values.get("public_ptr_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__720c11df46a18a1d969a40cbee2fad480a656eea1c8a6038e00abe26e8c3e292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8818e96469e0f52f18866b0662ac4e1c61d4b97ce539d1ba73df2f1dd9b4fdf7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4d59de3c0a80ad1aa04ef960b062284e8609289557ff84249988833393eb25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1cc2029151a49ca48952d7125ad679b2d0cdfc33e2b2661c531eff13783fbed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ae3d0496a81cb10ffd81c981df6d4002c64ae4185973061332229eac5ae6129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498f3162c144c9534504fe5274562bee6ba82c27d771eecba04cac16483c8c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c36bb2d5680ed34fc2d292718d1d3d35577fcb9df41b78c97902001820788666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExternalIpv6")
    def reset_external_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIpv6", []))

    @jsii.member(jsii_name="resetExternalIpv6PrefixLength")
    def reset_external_ipv6_prefix_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalIpv6PrefixLength", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPublicPtrDomainName")
    def reset_public_ptr_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicPtrDomainName", []))

    @builtins.property
    @jsii.member(jsii_name="externalIpv6Input")
    def external_ipv6_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIpv6Input"))

    @builtins.property
    @jsii.member(jsii_name="externalIpv6PrefixLengthInput")
    def external_ipv6_prefix_length_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalIpv6PrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTierInput")
    def network_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTierInput"))

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainNameInput")
    def public_ptr_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicPtrDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="externalIpv6")
    def external_ipv6(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6"))

    @external_ipv6.setter
    def external_ipv6(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf768b43d8bb3bfe3abce42fb6ed5438ca59e10b4e07c26b2573a85d9e0d4c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIpv6PrefixLength")
    def external_ipv6_prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6PrefixLength"))

    @external_ipv6_prefix_length.setter
    def external_ipv6_prefix_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697dcfa81221b409b999ec4d2f17ec3db34532ce98f44f4fbb1df02781beb9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d28caf2add4b26195ca75232bbdfdbba1bd0669660a68eb78a564d87e03205d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed7fdc87b331b7bb2e70185936cf298f29356442a3876b435af3f04d9016557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @public_ptr_domain_name.setter
    def public_ptr_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8e0dbabae87ed190de6a49aff482e57831c18db6f3a33299328c32e418b15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicPtrDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3767d6d31d701dfe6c447cc737afcd36de5abb7558436bb63b1beab41088162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7b4664937d3f7b5e5d6db32876944093dcf66966200626680c010653312aee2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288f195510b12b7f8e740faea243a233feb50c6d6236e617d580f6e56b372fb7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99c71991d104a0dde719ba5522fa57bcb807e55083b4dc2d6abb5c540efecf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e02c87e03825c45408489c9fae3bd249330ae5b1a07a004a5ccef4be5f37492)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01674038d7ac202a9ddbb8d839e2fbddc60e20cdd67781201fc8667a4f358b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6267b831d231ea618d811e82bf15ac7c3ce350e9b3e1dfe058f057d8f534d674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3a083c9d2168c57ba43a2dad5231a875d4288e598410ff25779ce8f0b8a283)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2163908ad15eb4d90eb63cbfebc4e0287688a7e84c3f5deb6549bb0613243e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putAliasIpRange")
    def put_alias_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a56f4c31597085717885dcc9c65dd6e46c872867133bb962251d6d683bab17b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAliasIpRange", [value]))

    @jsii.member(jsii_name="putIpv6AccessConfig")
    def put_ipv6_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176f36f8eb7ad93c302d81ff1eb76e89078200062c915132786144e58658678a)
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

    @jsii.member(jsii_name="resetNetworkAttachment")
    def reset_network_attachment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkAttachment", []))

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
    ) -> ComputeInstanceFromTemplateNetworkInterfaceAccessConfigList:
        return typing.cast(ComputeInstanceFromTemplateNetworkInterfaceAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRange")
    def alias_ip_range(
        self,
    ) -> ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeList:
        return typing.cast(ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeList, jsii.get(self, "aliasIpRange"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfig")
    def ipv6_access_config(
        self,
    ) -> ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigList:
        return typing.cast(ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigList, jsii.get(self, "ipv6AccessConfig"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRangeInput")
    def alias_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]], jsii.get(self, "aliasIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6PrefixLengthInput")
    def internal_ipv6_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalIpv6PrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfigInput")
    def ipv6_access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "ipv6AccessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AddressInput")
    def ipv6_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__67d32a138527f990e9eb1ea8406a9c84e0f7ead4626c3ead6e88b8dd153339e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749edf2c678da8ca881189432d080f1d75a47be7b4b83eb32dd720362da5e149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7271c259ef852803f9e01dd1f0b5ee7da5c7e7c8af2f3a73dbf7a22e8737484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792dcce2cb186c206dbf9596261a1a5c0c2e93147085df1fedd52d42638c47eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkIp")
    def network_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkIp"))

    @network_ip.setter
    def network_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709d96ec1565418ae8d69cc6b168e292b4b686e417ee7d65a7c1d540c2c63fb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d144eb0d2683a025c7282765d91c35851763d872870240dd96342dddd27980b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueCount")
    def queue_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueCount"))

    @queue_count.setter
    def queue_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d18367afc5a61ec73fc53b2a285e60454e6003cfc1236d9b4f353a56bf09b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9387b303632c8386c2125f122dcfb3d1e6cfb9caf57a071517ababf3256e9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e08037b67e1cae2bd8fbbaf559de20b0f35c5c8beb0297d944415b8394fe2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkProject")
    def subnetwork_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkProject"))

    @subnetwork_project.setter
    def subnetwork_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3ebea77f62ec92dc1d3449bd169dfc996f3b93fc1ce5e2de53803056aa462e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664aa9973c2ab5d9c540e5e0fba83938a93d9bc6edecb5550863cde7148e28c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class ComputeInstanceFromTemplateNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#total_egress_bandwidth_tier ComputeInstanceFromTemplate#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52816c5520658187788e3a39f6be6e322daa6dcec1087e31be1f9861418e644)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#total_egress_bandwidth_tier ComputeInstanceFromTemplate#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateNetworkPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e52fe1778b496cfa0358f93805c71faca2a66c3cde38f3a51943025ef2bb0b8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd454c431c9a2e995da9231ebf226fe001eb755d957183312894b83f4f10bef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fd2959688843a32d2169004cce010ff5f21c157261374a7a786ab95cdd1d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeInstanceFromTemplateParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf179375923e2c4cade27afda1ba2c0cd3f2837ec22b4247a3a1a0c91824902e)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#resource_manager_tags ComputeInstanceFromTemplate#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60deb9f167b174a089bbb96f92e4d1475eaa4c1c1e8e6ae9b3be20fb43f55b1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceManagerTags")
    def reset_resource_manager_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceManagerTags", []))

    @builtins.property
    @jsii.member(jsii_name="resourceManagerTagsInput")
    def resource_manager_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceManagerTagsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b54ed30d6f2820e310c0615347a78e2356fab27a98e7ff3ddac81079212f6ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceFromTemplateParams]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a983915f2341a4e3e82c6a62d301a78e946f90ce47b7bddf539154c806a951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "specific_reservation": "specificReservation"},
)
class ComputeInstanceFromTemplateReservationAffinity:
    def __init__(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceFromTemplateReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#specific_reservation ComputeInstanceFromTemplate#specific_reservation}
        '''
        if isinstance(specific_reservation, dict):
            specific_reservation = ComputeInstanceFromTemplateReservationAffinitySpecificReservation(**specific_reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15078f9588320c12193a9f98d989a8d9de2ae0a0b7e876f26d6a769a94e8a0d2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#type ComputeInstanceFromTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def specific_reservation(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateReservationAffinitySpecificReservation"]:
        '''specific_reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#specific_reservation ComputeInstanceFromTemplate#specific_reservation}
        '''
        result = self._values.get("specific_reservation")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateReservationAffinitySpecificReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a828200d7790c05d240c14ffb9f303d43f998422d4d6576f8d6c3d11eb8e9754)
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
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key ComputeInstanceFromTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#values ComputeInstanceFromTemplate#values}
        '''
        value = ComputeInstanceFromTemplateReservationAffinitySpecificReservation(
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
    ) -> "ComputeInstanceFromTemplateReservationAffinitySpecificReservationOutputReference":
        return typing.cast("ComputeInstanceFromTemplateReservationAffinitySpecificReservationOutputReference", jsii.get(self, "specificReservation"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationInput")
    def specific_reservation_input(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateReservationAffinitySpecificReservation"]:
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateReservationAffinitySpecificReservation"], jsii.get(self, "specificReservationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__97e5a2b6100bb0e790d95a9e56ee335e7f26ebb5997c3516d20f28bfc94c4c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateReservationAffinity]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88299d16011507717d5cbbe77886abbcb3a545d45c4d543032e54a20fa96da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateReservationAffinitySpecificReservation",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class ComputeInstanceFromTemplateReservationAffinitySpecificReservation:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key ComputeInstanceFromTemplate#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#values ComputeInstanceFromTemplate#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be61fa7687784d60823ce15d1d3b242ce56a1a318ea670bcf0106d94c654dd0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key ComputeInstanceFromTemplate#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Corresponds to the label values of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#values ComputeInstanceFromTemplate#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateReservationAffinitySpecificReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateReservationAffinitySpecificReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateReservationAffinitySpecificReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af3a726dab2d65fa01a881e861357990c5797b964afeaca5e15c0903ce73abee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05abda3134413869db42f2dad27e69d1e993ce496ba0dea793bf6fd14fdca503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7169097e11096da86551bbe329bf8a41369c630c9d78a68f99e7e44b35669779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateReservationAffinitySpecificReservation]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateReservationAffinitySpecificReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateReservationAffinitySpecificReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4458ce5b2ffadc3e45b9718a1c6ad8790257fa74048901335f7c87972340ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateScheduling",
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
class ComputeInstanceFromTemplateScheduling:
    def __init__(
        self,
        *,
        automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_domain: typing.Optional[jsii.Number] = None,
        instance_termination_action: typing.Optional[builtins.str] = None,
        local_ssd_recovery_timeout: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceFromTemplateSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceFromTemplateSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#automatic_restart ComputeInstanceFromTemplate#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#availability_domain ComputeInstanceFromTemplate#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_termination_action ComputeInstanceFromTemplate#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#local_ssd_recovery_timeout ComputeInstanceFromTemplate#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#max_run_duration ComputeInstanceFromTemplate#max_run_duration}
        :param min_node_cpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_node_cpus ComputeInstanceFromTemplate#min_node_cpus}.
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#node_affinities ComputeInstanceFromTemplate#node_affinities}
        :param on_host_maintenance: Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_host_maintenance ComputeInstanceFromTemplate#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_instance_stop_action ComputeInstanceFromTemplate#on_instance_stop_action}
        :param preemptible: Whether the instance is preemptible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#preemptible ComputeInstanceFromTemplate#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioning_model ComputeInstanceFromTemplate#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#termination_time ComputeInstanceFromTemplate#termination_time}
        '''
        if isinstance(local_ssd_recovery_timeout, dict):
            local_ssd_recovery_timeout = ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout(**local_ssd_recovery_timeout)
        if isinstance(max_run_duration, dict):
            max_run_duration = ComputeInstanceFromTemplateSchedulingMaxRunDuration(**max_run_duration)
        if isinstance(on_instance_stop_action, dict):
            on_instance_stop_action = ComputeInstanceFromTemplateSchedulingOnInstanceStopAction(**on_instance_stop_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4527464bf8b457c62118fcfd38157e4d37d23d33dfc83630046f8e8b1b9358db)
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
        '''Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#automatic_restart ComputeInstanceFromTemplate#automatic_restart}
        '''
        result = self._values.get("automatic_restart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_domain(self) -> typing.Optional[jsii.Number]:
        '''Specifies the availability domain, which this instance should be scheduled on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#availability_domain ComputeInstanceFromTemplate#availability_domain}
        '''
        result = self._values.get("availability_domain")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_termination_action(self) -> typing.Optional[builtins.str]:
        '''Specifies the action GCE should take when SPOT VM is preempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#instance_termination_action ComputeInstanceFromTemplate#instance_termination_action}
        '''
        result = self._values.get("instance_termination_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_recovery_timeout(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout"]:
        '''local_ssd_recovery_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#local_ssd_recovery_timeout ComputeInstanceFromTemplate#local_ssd_recovery_timeout}
        '''
        result = self._values.get("local_ssd_recovery_timeout")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout"], result)

    @builtins.property
    def max_run_duration(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateSchedulingMaxRunDuration"]:
        '''max_run_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#max_run_duration ComputeInstanceFromTemplate#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateSchedulingMaxRunDuration"], result)

    @builtins.property
    def min_node_cpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#min_node_cpus ComputeInstanceFromTemplate#min_node_cpus}.'''
        result = self._values.get("min_node_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_affinities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateSchedulingNodeAffinities"]]]:
        '''node_affinities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#node_affinities ComputeInstanceFromTemplate#node_affinities}
        '''
        result = self._values.get("node_affinities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceFromTemplateSchedulingNodeAffinities"]]], result)

    @builtins.property
    def on_host_maintenance(self) -> typing.Optional[builtins.str]:
        '''Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_host_maintenance ComputeInstanceFromTemplate#on_host_maintenance}
        '''
        result = self._values.get("on_host_maintenance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_instance_stop_action(
        self,
    ) -> typing.Optional["ComputeInstanceFromTemplateSchedulingOnInstanceStopAction"]:
        '''on_instance_stop_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#on_instance_stop_action ComputeInstanceFromTemplate#on_instance_stop_action}
        '''
        result = self._values.get("on_instance_stop_action")
        return typing.cast(typing.Optional["ComputeInstanceFromTemplateSchedulingOnInstanceStopAction"], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance is preemptible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#preemptible ComputeInstanceFromTemplate#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_model(self) -> typing.Optional[builtins.str]:
        '''Whether the instance is spot. If this is set as SPOT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#provisioning_model ComputeInstanceFromTemplate#provisioning_model}
        '''
        result = self._values.get("provisioning_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the timestamp, when the instance will be terminated, in RFC3339 text format.

        If specified, the instance termination action
        will be performed at the termination time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#termination_time ComputeInstanceFromTemplate#termination_time}
        '''
        result = self._values.get("termination_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49c47b90d6cfcb4f55f89f833acfb29eb3d003ee9ee07dd23b3ebc33bc47e351)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81e878dc4b781423358a9c53ba61941afff8dedd7000d6175ab3fa1389bbae7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b66818ae39b7d0b0934fe294b265e20cf712fee96704199f767df3f5e45b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbda7fe1782256e58244972f98cc16bf88708ca109435bae94c1aef5aafb22d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4956341f3b1eb1c80ac077764bde67c41265c83cc83ccc778486b93b7e9c41ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingMaxRunDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceFromTemplateSchedulingMaxRunDuration:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86aee4d77d4781fdf9fd524ba2b5f6b747917790d1f06c09cf3650a890d05c88)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateSchedulingMaxRunDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateSchedulingMaxRunDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingMaxRunDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b58f10292146711c336979537f3c63be90a6c797947baa528bc8e6458c3bba24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae536ae3c88de571a7577d57af51b7fb9e9d4c549be7f351aa2646c505043fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bf82e9d9dcf9f2d194ba408b1bbc9eccd5afdf3086ec520cf0ef3d836985dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8582ca8e24601bf3e93d844e01adb15985ce85675513e400230976c6ecf0af52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingNodeAffinities",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ComputeInstanceFromTemplateSchedulingNodeAffinities:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key ComputeInstanceFromTemplate#key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#operator ComputeInstanceFromTemplate#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#values ComputeInstanceFromTemplate#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863e53f330f4d85a72ffb94ae7a004b1cf6918d9cfd59eee2624c8979a13ef99)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#key ComputeInstanceFromTemplate#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#operator ComputeInstanceFromTemplate#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#values ComputeInstanceFromTemplate#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateSchedulingNodeAffinities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateSchedulingNodeAffinitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingNodeAffinitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3743f6cc44741ea77c8aeb6a07df216d4f8a676b404453e0de6a177e3cfb74f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateSchedulingNodeAffinitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404a6c81e813e8d89b778ee71f7c8109010b9bc71db0d8f6d55df63af14c4e3b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateSchedulingNodeAffinitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def2a631497b2929b4e7a42048cd6f3265a398cc2c451e3e174d427058681a94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b20cfbdc970e5922ee334008cfadf6e4733b1de9212da92855fe1758214734)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb98068948162ff162aab9d80875862f2d1d6637d76c58c3758f30e8956b763d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862f1468e1206ca0baf3789fb4487b003c23b13bfbf3f620945df2ec20d35dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateSchedulingNodeAffinitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingNodeAffinitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f57fed7af4c6d463b544df380012cfcb569e6c2363e5689fadf303ac4fbc71cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5978bbbbf909436b4b57f161f22425487e814b27f3eef769ea61b4b34560ce1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8be46d0258115a79513beaeab61c2ebd2e5af7c58eb6579888495dadf99d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d5cc5d48508da5482ce1438fcca2256bfb6cf35ac21c40e294bcd63057f8fd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateSchedulingNodeAffinities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateSchedulingNodeAffinities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateSchedulingNodeAffinities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567bcf99db2346aefb241b4a1c8cef915e98a8a9679be80942a80269b9dabccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingOnInstanceStopAction",
    jsii_struct_bases=[],
    name_mapping={"discard_local_ssd": "discardLocalSsd"},
)
class ComputeInstanceFromTemplateSchedulingOnInstanceStopAction:
    def __init__(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#discard_local_ssd ComputeInstanceFromTemplate#discard_local_ssd}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993454375b0ccd160f5cba1806f8684b71a72bace9dcccb0624e16480a009011)
            check_type(argname="argument discard_local_ssd", value=discard_local_ssd, expected_type=type_hints["discard_local_ssd"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discard_local_ssd is not None:
            self._values["discard_local_ssd"] = discard_local_ssd

    @builtins.property
    def discard_local_ssd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the contents of any attached Local SSD disks will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#discard_local_ssd ComputeInstanceFromTemplate#discard_local_ssd}
        '''
        result = self._values.get("discard_local_ssd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateSchedulingOnInstanceStopAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateSchedulingOnInstanceStopActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingOnInstanceStopActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9432cb43af5569d4a93c7c284e2542a214beae96ba5857a961e32d0a6d9ed46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba1560797a770cea749c715356834b5e32d34562434848b82af4dc9a3ef7fe95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discardLocalSsd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857d3e65bddd1dc7ecf11f750b6ba94f8fc70b578c373fb7916f6d866f7e654e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acceb00d3b9af0fdb1d570ed3ab8468e9c95c643f071d821c8ef5d0cf44eade2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLocalSsdRecoveryTimeout")
    def put_local_ssd_recovery_timeout(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        value = ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putLocalSsdRecoveryTimeout", [value]))

    @jsii.member(jsii_name="putMaxRunDuration")
    def put_max_run_duration(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#seconds ComputeInstanceFromTemplate#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#nanos ComputeInstanceFromTemplate#nanos}
        '''
        value = ComputeInstanceFromTemplateSchedulingMaxRunDuration(
            seconds=seconds, nanos=nanos
        )

        return typing.cast(None, jsii.invoke(self, "putMaxRunDuration", [value]))

    @jsii.member(jsii_name="putNodeAffinities")
    def put_node_affinities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65190ec628422f9f339cd20ad99b7ad63ab9f83b61c8d3eb0cf665d1ed8bf59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinities", [value]))

    @jsii.member(jsii_name="putOnInstanceStopAction")
    def put_on_instance_stop_action(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#discard_local_ssd ComputeInstanceFromTemplate#discard_local_ssd}
        '''
        value = ComputeInstanceFromTemplateSchedulingOnInstanceStopAction(
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
    ) -> ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference:
        return typing.cast(ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference, jsii.get(self, "localSsdRecoveryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(
        self,
    ) -> ComputeInstanceFromTemplateSchedulingMaxRunDurationOutputReference:
        return typing.cast(ComputeInstanceFromTemplateSchedulingMaxRunDurationOutputReference, jsii.get(self, "maxRunDuration"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinities")
    def node_affinities(
        self,
    ) -> ComputeInstanceFromTemplateSchedulingNodeAffinitiesList:
        return typing.cast(ComputeInstanceFromTemplateSchedulingNodeAffinitiesList, jsii.get(self, "nodeAffinities"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopAction")
    def on_instance_stop_action(
        self,
    ) -> ComputeInstanceFromTemplateSchedulingOnInstanceStopActionOutputReference:
        return typing.cast(ComputeInstanceFromTemplateSchedulingOnInstanceStopActionOutputReference, jsii.get(self, "onInstanceStopAction"))

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
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout], jsii.get(self, "localSsdRecoveryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDurationInput")
    def max_run_duration_input(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration], jsii.get(self, "maxRunDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCpusInput")
    def min_node_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinitiesInput")
    def node_affinities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]], jsii.get(self, "nodeAffinitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenanceInput")
    def on_host_maintenance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onHostMaintenanceInput"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopActionInput")
    def on_instance_stop_action_input(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction], jsii.get(self, "onInstanceStopActionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__33d5f66221fe1d42848e0296f0529216d459d798f720284d994ca2c31cc726b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticRestart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityDomain")
    def availability_domain(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomain"))

    @availability_domain.setter
    def availability_domain(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9dc1a4c7f0653e90d6a01f93e08d5b3ac003b14cde50cc0193fc56fccf608b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTerminationAction")
    def instance_termination_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminationAction"))

    @instance_termination_action.setter
    def instance_termination_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c488b3e81d09a3b8f2211955e23921d11cc6b38abe920b45185e1d9c66d429ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCpus")
    def min_node_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCpus"))

    @min_node_cpus.setter
    def min_node_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62fd5ef91190fbac6fc0f4f7ca2118fe8b0ef36edb1d120a0253c123ed67ab38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenance")
    def on_host_maintenance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onHostMaintenance"))

    @on_host_maintenance.setter
    def on_host_maintenance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1006c1f28fa1e0dda0324b681956731bb5fc19a9541f608a6a89004f08c6a9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2542dfd42dfbabe70c35a06f4b11b9b56b272f6339e00c5864ba6f73028f079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningModel")
    def provisioning_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningModel"))

    @provisioning_model.setter
    def provisioning_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de70e9227a0be1ea11be9a3b844caf76508cfbd1c1dbfe072590a63af6beb5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationTime")
    def termination_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminationTime"))

    @termination_time.setter
    def termination_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec5f089050a159299d67d59eb3882574b8ca4cf27392956c50904063a1906ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceFromTemplateScheduling]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateScheduling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce58b87acb056dac43a5abfb03267abcb465b0fc48c22ccf292c9d523bcddec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateScratchDisk",
    jsii_struct_bases=[],
    name_mapping={
        "interface": "interface",
        "device_name": "deviceName",
        "size": "size",
    },
)
class ComputeInstanceFromTemplateScratchDisk:
    def __init__(
        self,
        *,
        interface: builtins.str,
        device_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#interface ComputeInstanceFromTemplate#interface}
        :param device_name: Name with which the attached disk is accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        :param size: The size of the disk in gigabytes. One of 375 or 3000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#size ComputeInstanceFromTemplate#size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5be4d5c5c818f75f7960e945780e2190867f23f8ec8da9c510ea15f7b23a2d)
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface": interface,
        }
        if device_name is not None:
            self._values["device_name"] = device_name
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def interface(self) -> builtins.str:
        '''The disk interface used for attaching this disk. One of SCSI or NVME.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#interface ComputeInstanceFromTemplate#interface}
        '''
        result = self._values.get("interface")
        assert result is not None, "Required property 'interface' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which the attached disk is accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#device_name ComputeInstanceFromTemplate#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the disk in gigabytes. One of 375 or 3000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#size ComputeInstanceFromTemplate#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateScratchDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateScratchDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateScratchDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1b4eff896702eff440ad9ecb97bf00ba8e4cd1fb8dc0827c7819e2279d99b7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceFromTemplateScratchDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b484104284c211568aca7e7dff8ce4e250066491cd0cc932ed2d4fb2401902)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceFromTemplateScratchDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50123b3b91b5005a9f3ca5fd6604d2f0156d0bacd8621d1228fd695b98d9849a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb051970a1f4215ceb5f988913fcd0317e2de2644ec3439106131b57766fa200)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f9293fe9aeee708a46477b0713a51824c961d66302eec3b0049f235368896a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateScratchDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateScratchDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateScratchDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e615074b835395b1827cd9f7e4e7601ea046a8cd3e57e48aca5c8a577b98a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceFromTemplateScratchDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateScratchDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b60ce49d5e6c1713b47aa2df7b2a8b976eb78efbb012554288313273374fb6ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDeviceName")
    def reset_device_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceName", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="deviceNameInput")
    def device_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c827cc54153ec8c5c11aaa0d92b5130610eed6d030d159ecde2870b036c4c68c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34914414f8ed552881d39b938443d72ff5a1176a936f1d73744321424abed50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745478a878cf89c1e3c06c9ec4d92daccd73a6d01787ea916852a1e63dd71eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateScratchDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateScratchDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateScratchDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f74263ce407217ccc65544caa0c58602d35e4ad1082dcb016ae53e24b3c0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"scopes": "scopes", "email": "email"},
)
class ComputeInstanceFromTemplateServiceAccount:
    def __init__(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scopes ComputeInstanceFromTemplate#scopes}
        :param email: The service account e-mail address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#email ComputeInstanceFromTemplate#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc518013cdbedf88146b5497e217491082ecf44a3d2825a3bd8a37008337e036)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#scopes ComputeInstanceFromTemplate#scopes}
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The service account e-mail address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#email ComputeInstanceFromTemplate#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee34a8677c516e1c5fba077c940d36cdd240fb0ed2fe07e61e435cda871464e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__741002a698ffdd212c527cbd7c6d0e15537fb126973483f4840d88b98b2cbc17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c91949290b43300967bc4c54ac41b204ee65ab1134159202aeff4c2521db0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateServiceAccount]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e33ecd4e107c56bd3b6b9b43bc15018d2115c397378923ef887428141b33b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class ComputeInstanceFromTemplateShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Whether integrity monitoring is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_integrity_monitoring ComputeInstanceFromTemplate#enable_integrity_monitoring}
        :param enable_secure_boot: Whether secure boot is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_secure_boot ComputeInstanceFromTemplate#enable_secure_boot}
        :param enable_vtpm: Whether the instance uses vTPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_vtpm ComputeInstanceFromTemplate#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455ee1ebf4dd4bf213811021b69e2de383494dab5805ae7f62ca3164ccef1519)
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
        '''Whether integrity monitoring is enabled for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_integrity_monitoring ComputeInstanceFromTemplate#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether secure boot is enabled for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_secure_boot ComputeInstanceFromTemplate#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance uses vTPM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#enable_vtpm ComputeInstanceFromTemplate#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01f847d2755eb2bdf75e22589fe0af36952ab4b5c3bfa1bcab947881a67aed8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21432796cd8cf553d8d902b16d70d1c3a421472e0519d7b3db466f35aa75ad5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68ab17741e4cd391f2cd7d9145baeecc581bd02b51bd787dfe9c55581ba1db4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480a5ee53535f2760caeddca8192c5f32213218459453087c86578ca3e3882e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceFromTemplateShieldedInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceFromTemplateShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceFromTemplateShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ccd9c3b78dca0070ddc88730b4e3e0f67f10dcb2f58fa19cff636a5ae348d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInstanceFromTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#create ComputeInstanceFromTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#delete ComputeInstanceFromTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#update ComputeInstanceFromTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26705c144857a3804fd6c63df6b225b85c11ba8f2997990ff5fdb1d572163c5e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#create ComputeInstanceFromTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#delete ComputeInstanceFromTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance_from_template#update ComputeInstanceFromTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceFromTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceFromTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstanceFromTemplate.ComputeInstanceFromTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b7cc3e0e550257f1c8a0a0e91bafd650338ce4924504b27349842d2c446cc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__389e1a5616d9cd6992f79b40b364d6d63285465f672dc9dffb702898b276b49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9a7bbddbb36428a1c8c42c1840585b58794bb151ace17d27abbf4003fda836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cb012fbbdcdeed0dfcb2696f1f35c4d6948576e47dba53e96abc0f61277f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131d2f00ad120ec1e80a8f39d9164971968f2c4a6c0ca0c764090543d4fd4575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstanceFromTemplate",
    "ComputeInstanceFromTemplateAdvancedMachineFeatures",
    "ComputeInstanceFromTemplateAdvancedMachineFeaturesOutputReference",
    "ComputeInstanceFromTemplateAttachedDisk",
    "ComputeInstanceFromTemplateAttachedDiskList",
    "ComputeInstanceFromTemplateAttachedDiskOutputReference",
    "ComputeInstanceFromTemplateBootDisk",
    "ComputeInstanceFromTemplateBootDiskInitializeParams",
    "ComputeInstanceFromTemplateBootDiskInitializeParamsOutputReference",
    "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey",
    "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference",
    "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey",
    "ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference",
    "ComputeInstanceFromTemplateBootDiskOutputReference",
    "ComputeInstanceFromTemplateConfidentialInstanceConfig",
    "ComputeInstanceFromTemplateConfidentialInstanceConfigOutputReference",
    "ComputeInstanceFromTemplateConfig",
    "ComputeInstanceFromTemplateGuestAccelerator",
    "ComputeInstanceFromTemplateGuestAcceleratorList",
    "ComputeInstanceFromTemplateGuestAcceleratorOutputReference",
    "ComputeInstanceFromTemplateInstanceEncryptionKey",
    "ComputeInstanceFromTemplateInstanceEncryptionKeyOutputReference",
    "ComputeInstanceFromTemplateNetworkInterface",
    "ComputeInstanceFromTemplateNetworkInterfaceAccessConfig",
    "ComputeInstanceFromTemplateNetworkInterfaceAccessConfigList",
    "ComputeInstanceFromTemplateNetworkInterfaceAccessConfigOutputReference",
    "ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange",
    "ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeList",
    "ComputeInstanceFromTemplateNetworkInterfaceAliasIpRangeOutputReference",
    "ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig",
    "ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigList",
    "ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfigOutputReference",
    "ComputeInstanceFromTemplateNetworkInterfaceList",
    "ComputeInstanceFromTemplateNetworkInterfaceOutputReference",
    "ComputeInstanceFromTemplateNetworkPerformanceConfig",
    "ComputeInstanceFromTemplateNetworkPerformanceConfigOutputReference",
    "ComputeInstanceFromTemplateParams",
    "ComputeInstanceFromTemplateParamsOutputReference",
    "ComputeInstanceFromTemplateReservationAffinity",
    "ComputeInstanceFromTemplateReservationAffinityOutputReference",
    "ComputeInstanceFromTemplateReservationAffinitySpecificReservation",
    "ComputeInstanceFromTemplateReservationAffinitySpecificReservationOutputReference",
    "ComputeInstanceFromTemplateScheduling",
    "ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout",
    "ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeoutOutputReference",
    "ComputeInstanceFromTemplateSchedulingMaxRunDuration",
    "ComputeInstanceFromTemplateSchedulingMaxRunDurationOutputReference",
    "ComputeInstanceFromTemplateSchedulingNodeAffinities",
    "ComputeInstanceFromTemplateSchedulingNodeAffinitiesList",
    "ComputeInstanceFromTemplateSchedulingNodeAffinitiesOutputReference",
    "ComputeInstanceFromTemplateSchedulingOnInstanceStopAction",
    "ComputeInstanceFromTemplateSchedulingOnInstanceStopActionOutputReference",
    "ComputeInstanceFromTemplateSchedulingOutputReference",
    "ComputeInstanceFromTemplateScratchDisk",
    "ComputeInstanceFromTemplateScratchDiskList",
    "ComputeInstanceFromTemplateScratchDiskOutputReference",
    "ComputeInstanceFromTemplateServiceAccount",
    "ComputeInstanceFromTemplateServiceAccountOutputReference",
    "ComputeInstanceFromTemplateShieldedInstanceConfig",
    "ComputeInstanceFromTemplateShieldedInstanceConfigOutputReference",
    "ComputeInstanceFromTemplateTimeouts",
    "ComputeInstanceFromTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9124d7c3f082b1298466630389ce5b835ab60613b6b9b2156faa779358c47722(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    source_instance_template: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceFromTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    desired_status: typing.Optional[builtins.str] = None,
    enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateInstanceEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeInstanceFromTemplateParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceFromTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceFromTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateScratchDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceFromTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceFromTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__88a0d1fafa28757ccf886bd38038315b61c49d3626b41233acb7066d5fd3c16e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd86eff08c8a375305ce0b338f991d67a91e8bc75a9aa949291057d38559b92b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateAttachedDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4956625220e67b80c385a70b49445baa5839754d7cb033889e050c7628f164a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fcf30e2cb3b7c0ab85919287e3f427f6e8a6a83718807067d8f7283da21b81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee94dba9b0419cd693edd6b591babb695bf32d6ee6bb7010916fec605db92b7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateScratchDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07e9705b5f013901ff56c8841bf8548dd8cf737b56eb576e3f0f9afcf07bc03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a8f24ba5e384de867395dadd3d61ebf37b640b06822cd6a6020b8a4235ceac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862490ea015e40356bb0f0631681a158b0be717408abe19834c070f5731ed66b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc3853607653bad7fad357c5bf50410fd28ebb1f9b935ae61e274546f32ecec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a1cf26738e8f5e12422ce037d5884beb30385cdf4d8765b801394249d84950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6f1c08bc1e5a895eb75450bc72c62c3978e9a50823e04fa39f85cf51e980bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86690719363fbe0722cc19638ed108c0e58bf3de135e37d6feb89a2d74e97e9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a8d523c0ef29a48e41153bb12c136cb6cd65ae179fc396233c83f891578897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba413f81113eb78c5a0311cc459c01a6aa4c1193714fdef010d315757b7106f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d180637448a48a3d002438a1e16da3e0febd5cc6a14a0c0064ef073c48a14d57(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9377fd6fa32f761cba9fdf8e8c04397751a36f78f1c2a8b4d753b54674c1b145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdd646c9d03fa3b0aa2f97865c5c4e8b14c756d8c38a103ada18b26ac21632f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e270053afbd5695d0f10fa209b9fe7511b1e0469aa7fa4591a9654dadd3913b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc31b59384ebcbbfd7ae0ae74ca1b1e0bc66aa34807b4ce32204c49ec0ae1a46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b911f4a91f6ea031e663ccdaa2f0d3aa6c3133f321ed583b0451622729edc025(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7d6d8cfdffd3e824023624ccd71e2ffe8dbdcd84ff3dc9874c2911c8012b8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bd05fc4c124fcace57ffdc8f50d757fd983832dff59c06309e0d5b1665f0c1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869732f927acbd4478ddf44be4bfa6419eb61306e47d60f930cb64e0abde7c13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f50cb5795a6043b996800d00d36c5e141fda50b7f285b150c925cb4149316c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2661c1484b6e13c44536e6f5c1ab371e33daab81f3fb76e4a6d8644f86c10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11be50a7e28ab76bbf149f69ca128c858934fca2cb97b8fb26f071101d1ced57(
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

def _typecheckingstub__57a5550afd9eee196b103e8e68edf23ed3e07f0d203df6af68db83fac5402d19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267023582d07f2a570f6f1de102834eef9a8a509c6177b1528faaa6f912a9b68(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1708101c3ebb635e7cd12ab92989a0b8863269ea7eb0cdd646720f89b89e4f00(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06413ee307512439e3da2283cb5d6488d29bbe25aff1f18dc64d89eeb2eb1c85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1da2327c6d658bde3d3c26b563e9d088c29058d0c227b668397260f8735af16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade8a0859bc6210dfc2c757737b2f37f0355b49df9e4d4f465f9d9b04ccd526e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__435a8715913b8af94187f56fcbcf5e24ebc97712e01f535f4f624b1a02d1e6b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb4960269b6663edd643dff7cb4449e61eb70a10fae241c5c252b055777264e(
    value: typing.Optional[ComputeInstanceFromTemplateAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0472425de7657cd3c80ddc34a8a5fc3a621e4f26183b45d1ca4779a3645e55(
    *,
    source: builtins.str,
    device_name: typing.Optional[builtins.str] = None,
    disk_encryption_key_raw: typing.Optional[builtins.str] = None,
    disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
    disk_encryption_service_account: typing.Optional[builtins.str] = None,
    force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da5a31a6ca2c27fa487368ce257b53a410682b9feb213f75499d87d6f7179e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e923a9b549a36780325831b242f4aa3454a64aae6f5a115cf3eb7c50bb0cbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e89552f8844b7b9c25947ce2b81ef72259bba601265a01c0f54e55a62db9fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a5b9dce11081e7c4a57275972033f7ad05d8caf61b4db84d85c7dbee88cacf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd3473cd263d69d66bdfa95c2be5ea4df0555107439abb53ff54fe3f622c30d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e13314481467aaa9891120e827b193d3807382ad7616564f83327d436a23d2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateAttachedDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c47f8c89e8d2b8d42aef1f4f970ed7a75566f0e94609bed990f78340f92b7070(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87de0285ba3f0d9b337ad42253fee454b8a8605f3f17eb46e69edbfc080b4057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1465b85f013704a14cac2300f2ec6b9b92fa7d2b27f569fc37f264c568cb3dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea009c57c6aee2b2dea4639c2033f0b271d6af912735dbfff2b8a45cf2ef2367(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e1415744ffb9fd99d8364d3e8a68bddba52008943769a8f386cbaf18143db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2de14fe8713c1d078345a043d01166c62f8fb8c914a18e38d80a3a3cc23d83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f18efbe87c1c1f2538c0ce32012ec6b8b4eed99b2642ee7661d8cd4ba9e40d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c05f016a3dbe0c5bca6a705b4f6304a991fbef08b0ce30dc561ff96e415d8c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5befff7eb15e2001db5e86e93525aff1bb4c0453b175765efab4a8680985b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467285fa4d811d3ceb6521a6ba59231d455c553d726cae9c206ddab481d6a147(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateAttachedDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9daaccb37d7f482f186a649a6b98f91648e2f4fc825f2e9ab7a632441f110d(
    *,
    auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_name: typing.Optional[builtins.str] = None,
    disk_encryption_key_raw: typing.Optional[builtins.str] = None,
    disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
    disk_encryption_service_account: typing.Optional[builtins.str] = None,
    force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    initialize_params: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    interface: typing.Optional[builtins.str] = None,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43290875167e467d184f760e883b7d7bac501946d12ad7bcebf6119b99edf6c(
    *,
    architecture: typing.Optional[builtins.str] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    size: typing.Optional[jsii.Number] = None,
    snapshot: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_pool: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2848a2300de7685ef88373c9b81165a8174c1a3a2801e3aca5b74e86fc6d55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74dd879d10cf8f3d85663b42392e55bd6c7607f445cb08b327f75ca5a36bd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e202f6731e00a728b5b33e17459b62cd35752b87dc5918c905d8638e6d7e2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacdc3db458fe91622c27e3e9a5361dfb4fd331ffe8e591c201e490c74967407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ea74d843629481ed6254cb5328ce82e2ce4d1dd43f312b1a48919d792d73e9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a54c8d1aa8a3be970ffa3b031f3716ba9210c6bdc74406234a46fd60b9ac1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b345c8e18c974c18869564927e1800cdb2299888aaf99b66500c6842795a74a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f78198546dc63e59a8536c5c269e9ff246139ac08708bf1e3c6f8039fa35b5a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92eb080a097b9a15bde7157787dad633d7d3f6b186b38b992e6f037c22e21fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe5f467dce7a811b1150b1815bc6fb8cf17e6a52bd1fe1fb02a2cc11b151922(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fdcd371dd6f2c180ccfd5ca16e2941990e559f89dc9547969e6be2f590d0a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbeffbe2e790d7331b8682ea84ace0f64176615c735bae9a1be7848710e59b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee963abf7008e105d6a19af9405e9f74b0d6d12e91d68aece9967826711125f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84865fa8e6495b7faaad67417306f56c69742a3492841152a6d7d260ef980bd4(
    value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4ee3a30a110932668bbba67ad7a31afd4a66bc4a31cf76ebd54f265da39bf3(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1fc821f2723fe995e7654ffd398401f5288a72e058c233910cdfaa065a3101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d508b26461be832498af079e198aeb830696b4c7fe0b0208e7e037996c8e82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28966121dca933f46bcf0018116eda10db4064f37aa79a4e03009c23eed18b01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267c020da86af75062ac4ecd8a5b55abe72b4b928c5a54de9ba3336925279b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428bd8910d97c660920743ead7660d51a946b9b0ae031e1b4d375931883cf953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ffd62291c405a357da596158576f930ccb6c14dc03e4ef5ca7fc663e78cd6a(
    value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245f28686355d583457fd9f86d093e91eac0abc5f1330fce691cc1576c2674bd(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d9f2f4ea9f387f6ee555cf913882e2a9c0cfc215ef71b41e46282e395c7a5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4c2b15212cef2b14e8d26a48e2754d6a55926a2f5ad0c0635e99bb18730d0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69db9db38a438da344ec89fb550377043c8a37f110f484325d3b71863ffc8430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02273a808f61db70a41f8d1c0a3c38a34e671c772f1d6b79f8ddba5c035d018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e861b85747371be64af5abca3a851362743c4447fd1ad14e38d3779f9086947d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca0035fbff8d89b3adbb266bb768f3a55beea5a1c81d660f01929c2e57d7b8a(
    value: typing.Optional[ComputeInstanceFromTemplateBootDiskInitializeParamsSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18246e52fc616b22e8d5ce252bbb8b11d56af565996bc42c2231c8daaddb3c07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3f144bb37c858742fcb642ea4b3f668615c2635ef7d9e6014269a67401e47a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291e7ba58b52b4b28a042d61fef7a4db34047a213f978a29bfbc0a0609279ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ac7cadd8aa090eb3d1207c78a0c99b5e73b0a4f8ff0839f98eef484d87b31c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a66405c849acc5574261fe4094a6bea4b9db1cbe722df4a2941d00dd4dd31d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae445a43371e8a72f95475c0598d01c1d847143aecac79576924eccf530d0fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c49209f79de058e0b7575594f7d83b04a552464d27904262954884e9c4a605a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfec923a9d1bc148be10f812d89ec28117b218a42829effd7eb4d8424cdee229(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5e52e0df903939fbab4ba403e0e0aa5d0ace6a57d13806e1b192453947b732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1047b0368a4a068686e698c1405a818f950ddd7bf56dfcdddde552cbfb3f9246(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8f7a961c5ecb083cef8ecaf29c3945ed408998f13f2eefab2a2b89cc771405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0131e011b1d92dcbe99501802d1b6e39f20da029ff48f3b88ca3a1fe628d2572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5f694ebf278fba382dcb460452ff77473471283ea8ebb5f280a6b622469b06(
    value: typing.Optional[ComputeInstanceFromTemplateBootDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9eca2f5d5aafa2dc5ccbf8cc7fa64669eb1bac438f9db7f173d8e3cd782e6ed(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752e17e1df75abc370399c5391314e6fe89ad7f688cebd6292cc50f5ee8179e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25da22463144e82d16b643b9661fd57b8de5caf206bff936a68cc39bbee691cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d1242438d9c6d80eea4ed206752c0f4d17058087d68b204aecf4fe293cbc66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df391f44098e98d49697686cbf98a7c19e3f4c4c0827eb2a597035d2a8ec53de(
    value: typing.Optional[ComputeInstanceFromTemplateConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed7912504b0e71b044d42bf8efadad4d400bb2eac9a7ffca5a7f1ae085368a1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    source_instance_template: builtins.str,
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceFromTemplateAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk: typing.Optional[typing.Union[ComputeInstanceFromTemplateBootDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    desired_status: typing.Optional[builtins.str] = None,
    enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_encryption_key: typing.Optional[typing.Union[ComputeInstanceFromTemplateInstanceEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_type: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    network_interface: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterface, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeInstanceFromTemplateParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceFromTemplateReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceFromTemplateScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateScratchDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceFromTemplateServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceFromTemplateShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceFromTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d411b16899a41ff78cad092ee225fa75666ed0466e7119f8a3ea9c59d9ea52(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946bbfcb1f2b0efbf79aff92a87ccc8f93613b5767a6c2a117cc55dbff7a466e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74193ac4315adf7d86bc2e0dcb9ced301521f044a77b8c76240c25c1ced62b09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e47e17fafe5459ef3fd6be042853718caf0cb22d8a70546dd4d2513dea59467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7f31101c39e06206f4f1605bce1bdb8cacb0b9922cdcb3eb9cc1186ea7b31b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fc1bd326a810523b336513095836fe309772063c42a174f91426566c2e6232(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83be6e0b63000c5baf2fe9b4d72a13449e49f4b115526ddffa2769d26e021ff6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76583d8e6a66b6f435f4403a9164d4b03e741a7540bd3864b516394192e84a09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075399178a7dd3d67cd90d1607ffa0aa97934e269c1460c838c18f523831b421(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366035b58dc17e62117b601d5d0acb1f66872f8c70b2e42356b9c05ec5764fa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda5a3d9f65d3d2a12fbebd08333fa8fde6dc2652b8644d260bb2657afc01021(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b2480c965f49174862c1cfca5aa6190e66c6f0a4b63ccbbfe6b61c01c4d4dc(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e641837c9e427615fe3d7305c694ac323dd5ad3392b47093fcdf6ae12785eef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6564134fc8bc9d36159d2be3b6d7161392b600d23bedebcd41708b7be0f7f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc83862a06daf2034dcf6f0ffef33fedeb54226c561d533f4b3623f8eed58e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d27edbc73df700f7f6ac66a1dee4d5d85c78f3a279f4295e7ca7dcaba37bd50(
    value: typing.Optional[ComputeInstanceFromTemplateInstanceEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24120031033231cc4cdd6490c674741b94b44ca3e9d81bf9e0f4078e4ca765b(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
    ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ipv6_address: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    network_attachment: typing.Optional[builtins.str] = None,
    network_ip: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    queue_count: typing.Optional[jsii.Number] = None,
    stack_type: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    subnetwork_project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ada775bd53e47573cea7a97f75c4f33f607994d21cc7d716b4da7c7c38d03dd(
    *,
    nat_ip: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    public_ptr_domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c438a108620bccbc98c9f1ecbcb7eccf50b69d39a5a307cccfe4be8409136d52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7980f2b61133ffd68613f1e9b4bed8cfa309bf56e0a60dc5d29d1b6fae6085df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b7cb2796ee2e7e4acabfc21b3e7eeb1c26e20c49aff0a9ffbe0d30fe5301c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25e50cbb8f3d5de48d233334f32795b5e4dea8563d35a5532d49e9c00947f93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0634219ff7dafa2b54be4277e4cb01fdf70e5638170d5409b99b57397c52f8e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b268108f33af9ef2d7f847e87e7eb2a41c16096dd4ff061f1774bef0d4cae3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4d57a361a5f28b6230b3759bd94b47c29750f15615a32b4baed36c64e4de0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f8887394ac88ce6acf5aa7c93338dd7b0029020b83a6481c36475e067eadfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65302e8edc699c1d6dc798e1658f33b087d54b436662452f71b4c66a2c78e18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa02e9aa4cfe52250e3360d77dfd048d6d4c6704d48e92861a62694c7ba2b70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d04aac032dfd978906126f7d148eca2ed843c9764c8e7a8578fb610f146db7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225c5fa8fad47f18eaf94dec214831690c4821396cef24491b4d8fe2128a2556(
    *,
    ip_cidr_range: builtins.str,
    subnetwork_range_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb83936b088489ac3b79c91e75ae4ad2b7ec872fdf7f45fceb8c68f79d08342c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d444536239fdb26779a179e0a6d97ca74b41aa5d2091be000e291ad8081244d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1209d4d07e491c5f604b2a05d6de9f7b12269e77ab6380560f5952061676bc58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549b8eb7729ddb8498173b66c59b8ddb54b2ae052b8045c85d6889abb03b3172(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a521407d2518440f3c790b6ed5ab3fb5af4e5fcdc67c334ef9f731184cf9317b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8643fed612be216ef019da9f29afc2bf6cfb7565719df4e4c056493f85f40c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f0831d0923f67b5143b4249a4aae49f1531e6bd82be0ccfa85faa88723483f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67132653093bb61295952427c39d2b3e70a773e06deb1368b3a1d3a1c5faf30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d153b50cc62301681bed492a174e49e2f8c00b41294c0111863f52e5a2bc8f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be7dc6082b658149ae43add2f297a5346aeb3aa96ef5a55816e7b504f403c9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fece5d19f45ad263f1efba088d40d213c89cabb2b14ebcf47ea4b69f13585ae(
    *,
    network_tier: builtins.str,
    external_ipv6: typing.Optional[builtins.str] = None,
    external_ipv6_prefix_length: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    public_ptr_domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720c11df46a18a1d969a40cbee2fad480a656eea1c8a6038e00abe26e8c3e292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8818e96469e0f52f18866b0662ac4e1c61d4b97ce539d1ba73df2f1dd9b4fdf7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4d59de3c0a80ad1aa04ef960b062284e8609289557ff84249988833393eb25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cc2029151a49ca48952d7125ad679b2d0cdfc33e2b2661c531eff13783fbed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae3d0496a81cb10ffd81c981df6d4002c64ae4185973061332229eac5ae6129(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498f3162c144c9534504fe5274562bee6ba82c27d771eecba04cac16483c8c43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36bb2d5680ed34fc2d292718d1d3d35577fcb9df41b78c97902001820788666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf768b43d8bb3bfe3abce42fb6ed5438ca59e10b4e07c26b2573a85d9e0d4c0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697dcfa81221b409b999ec4d2f17ec3db34532ce98f44f4fbb1df02781beb9d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d28caf2add4b26195ca75232bbdfdbba1bd0669660a68eb78a564d87e03205d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed7fdc87b331b7bb2e70185936cf298f29356442a3876b435af3f04d9016557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8e0dbabae87ed190de6a49aff482e57831c18db6f3a33299328c32e418b15f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3767d6d31d701dfe6c447cc737afcd36de5abb7558436bb63b1beab41088162(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b4664937d3f7b5e5d6db32876944093dcf66966200626680c010653312aee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288f195510b12b7f8e740faea243a233feb50c6d6236e617d580f6e56b372fb7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99c71991d104a0dde719ba5522fa57bcb807e55083b4dc2d6abb5c540efecf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e02c87e03825c45408489c9fae3bd249330ae5b1a07a004a5ccef4be5f37492(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01674038d7ac202a9ddbb8d839e2fbddc60e20cdd67781201fc8667a4f358b6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6267b831d231ea618d811e82bf15ac7c3ce350e9b3e1dfe058f057d8f534d674(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3a083c9d2168c57ba43a2dad5231a875d4288e598410ff25779ce8f0b8a283(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2163908ad15eb4d90eb63cbfebc4e0287688a7e84c3f5deb6549bb0613243e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a56f4c31597085717885dcc9c65dd6e46c872867133bb962251d6d683bab17b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176f36f8eb7ad93c302d81ff1eb76e89078200062c915132786144e58658678a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d32a138527f990e9eb1ea8406a9c84e0f7ead4626c3ead6e88b8dd153339e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749edf2c678da8ca881189432d080f1d75a47be7b4b83eb32dd720362da5e149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7271c259ef852803f9e01dd1f0b5ee7da5c7e7c8af2f3a73dbf7a22e8737484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792dcce2cb186c206dbf9596261a1a5c0c2e93147085df1fedd52d42638c47eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709d96ec1565418ae8d69cc6b168e292b4b686e417ee7d65a7c1d540c2c63fb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d144eb0d2683a025c7282765d91c35851763d872870240dd96342dddd27980b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d18367afc5a61ec73fc53b2a285e60454e6003cfc1236d9b4f353a56bf09b61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9387b303632c8386c2125f122dcfb3d1e6cfb9caf57a071517ababf3256e9fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e08037b67e1cae2bd8fbbaf559de20b0f35c5c8beb0297d944415b8394fe2e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3ebea77f62ec92dc1d3449bd169dfc996f3b93fc1ce5e2de53803056aa462e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664aa9973c2ab5d9c540e5e0fba83938a93d9bc6edecb5550863cde7148e28c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52816c5520658187788e3a39f6be6e322daa6dcec1087e31be1f9861418e644(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52fe1778b496cfa0358f93805c71faca2a66c3cde38f3a51943025ef2bb0b8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd454c431c9a2e995da9231ebf226fe001eb755d957183312894b83f4f10bef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fd2959688843a32d2169004cce010ff5f21c157261374a7a786ab95cdd1d96(
    value: typing.Optional[ComputeInstanceFromTemplateNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf179375923e2c4cade27afda1ba2c0cd3f2837ec22b4247a3a1a0c91824902e(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60deb9f167b174a089bbb96f92e4d1475eaa4c1c1e8e6ae9b3be20fb43f55b1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54ed30d6f2820e310c0615347a78e2356fab27a98e7ff3ddac81079212f6ce7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a983915f2341a4e3e82c6a62d301a78e946f90ce47b7bddf539154c806a951(
    value: typing.Optional[ComputeInstanceFromTemplateParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15078f9588320c12193a9f98d989a8d9de2ae0a0b7e876f26d6a769a94e8a0d2(
    *,
    type: builtins.str,
    specific_reservation: typing.Optional[typing.Union[ComputeInstanceFromTemplateReservationAffinitySpecificReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a828200d7790c05d240c14ffb9f303d43f998422d4d6576f8d6c3d11eb8e9754(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e5a2b6100bb0e790d95a9e56ee335e7f26ebb5997c3516d20f28bfc94c4c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88299d16011507717d5cbbe77886abbcb3a545d45c4d543032e54a20fa96da1(
    value: typing.Optional[ComputeInstanceFromTemplateReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be61fa7687784d60823ce15d1d3b242ce56a1a318ea670bcf0106d94c654dd0(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3a726dab2d65fa01a881e861357990c5797b964afeaca5e15c0903ce73abee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05abda3134413869db42f2dad27e69d1e993ce496ba0dea793bf6fd14fdca503(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7169097e11096da86551bbe329bf8a41369c630c9d78a68f99e7e44b35669779(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4458ce5b2ffadc3e45b9718a1c6ad8790257fa74048901335f7c87972340ee(
    value: typing.Optional[ComputeInstanceFromTemplateReservationAffinitySpecificReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4527464bf8b457c62118fcfd38157e4d37d23d33dfc83630046f8e8b1b9358db(
    *,
    automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_domain: typing.Optional[jsii.Number] = None,
    instance_termination_action: typing.Optional[builtins.str] = None,
    local_ssd_recovery_timeout: typing.Optional[typing.Union[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    max_run_duration: typing.Optional[typing.Union[ComputeInstanceFromTemplateSchedulingMaxRunDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_node_cpus: typing.Optional[jsii.Number] = None,
    node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on_host_maintenance: typing.Optional[builtins.str] = None,
    on_instance_stop_action: typing.Optional[typing.Union[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_model: typing.Optional[builtins.str] = None,
    termination_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c47b90d6cfcb4f55f89f833acfb29eb3d003ee9ee07dd23b3ebc33bc47e351(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e878dc4b781423358a9c53ba61941afff8dedd7000d6175ab3fa1389bbae7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b66818ae39b7d0b0934fe294b265e20cf712fee96704199f767df3f5e45b5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbda7fe1782256e58244972f98cc16bf88708ca109435bae94c1aef5aafb22d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4956341f3b1eb1c80ac077764bde67c41265c83cc83ccc778486b93b7e9c41ff(
    value: typing.Optional[ComputeInstanceFromTemplateSchedulingLocalSsdRecoveryTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86aee4d77d4781fdf9fd524ba2b5f6b747917790d1f06c09cf3650a890d05c88(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58f10292146711c336979537f3c63be90a6c797947baa528bc8e6458c3bba24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae536ae3c88de571a7577d57af51b7fb9e9d4c549be7f351aa2646c505043fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bf82e9d9dcf9f2d194ba408b1bbc9eccd5afdf3086ec520cf0ef3d836985dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8582ca8e24601bf3e93d844e01adb15985ce85675513e400230976c6ecf0af52(
    value: typing.Optional[ComputeInstanceFromTemplateSchedulingMaxRunDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863e53f330f4d85a72ffb94ae7a004b1cf6918d9cfd59eee2624c8979a13ef99(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3743f6cc44741ea77c8aeb6a07df216d4f8a676b404453e0de6a177e3cfb74f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404a6c81e813e8d89b778ee71f7c8109010b9bc71db0d8f6d55df63af14c4e3b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def2a631497b2929b4e7a42048cd6f3265a398cc2c451e3e174d427058681a94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b20cfbdc970e5922ee334008cfadf6e4733b1de9212da92855fe1758214734(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb98068948162ff162aab9d80875862f2d1d6637d76c58c3758f30e8956b763d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862f1468e1206ca0baf3789fb4487b003c23b13bfbf3f620945df2ec20d35dd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateSchedulingNodeAffinities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57fed7af4c6d463b544df380012cfcb569e6c2363e5689fadf303ac4fbc71cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5978bbbbf909436b4b57f161f22425487e814b27f3eef769ea61b4b34560ce1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8be46d0258115a79513beaeab61c2ebd2e5af7c58eb6579888495dadf99d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5cc5d48508da5482ce1438fcca2256bfb6cf35ac21c40e294bcd63057f8fd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567bcf99db2346aefb241b4a1c8cef915e98a8a9679be80942a80269b9dabccf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateSchedulingNodeAffinities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993454375b0ccd160f5cba1806f8684b71a72bace9dcccb0624e16480a009011(
    *,
    discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9432cb43af5569d4a93c7c284e2542a214beae96ba5857a961e32d0a6d9ed46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1560797a770cea749c715356834b5e32d34562434848b82af4dc9a3ef7fe95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857d3e65bddd1dc7ecf11f750b6ba94f8fc70b578c373fb7916f6d866f7e654e(
    value: typing.Optional[ComputeInstanceFromTemplateSchedulingOnInstanceStopAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acceb00d3b9af0fdb1d570ed3ab8468e9c95c643f071d821c8ef5d0cf44eade2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65190ec628422f9f339cd20ad99b7ad63ab9f83b61c8d3eb0cf665d1ed8bf59(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceFromTemplateSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d5f66221fe1d42848e0296f0529216d459d798f720284d994ca2c31cc726b1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9dc1a4c7f0653e90d6a01f93e08d5b3ac003b14cde50cc0193fc56fccf608b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c488b3e81d09a3b8f2211955e23921d11cc6b38abe920b45185e1d9c66d429ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62fd5ef91190fbac6fc0f4f7ca2118fe8b0ef36edb1d120a0253c123ed67ab38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1006c1f28fa1e0dda0324b681956731bb5fc19a9541f608a6a89004f08c6a9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2542dfd42dfbabe70c35a06f4b11b9b56b272f6339e00c5864ba6f73028f079(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de70e9227a0be1ea11be9a3b844caf76508cfbd1c1dbfe072590a63af6beb5cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec5f089050a159299d67d59eb3882574b8ca4cf27392956c50904063a1906ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce58b87acb056dac43a5abfb03267abcb465b0fc48c22ccf292c9d523bcddec2(
    value: typing.Optional[ComputeInstanceFromTemplateScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5be4d5c5c818f75f7960e945780e2190867f23f8ec8da9c510ea15f7b23a2d(
    *,
    interface: builtins.str,
    device_name: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b4eff896702eff440ad9ecb97bf00ba8e4cd1fb8dc0827c7819e2279d99b7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b484104284c211568aca7e7dff8ce4e250066491cd0cc932ed2d4fb2401902(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50123b3b91b5005a9f3ca5fd6604d2f0156d0bacd8621d1228fd695b98d9849a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb051970a1f4215ceb5f988913fcd0317e2de2644ec3439106131b57766fa200(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9293fe9aeee708a46477b0713a51824c961d66302eec3b0049f235368896a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e615074b835395b1827cd9f7e4e7601ea046a8cd3e57e48aca5c8a577b98a89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceFromTemplateScratchDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60ce49d5e6c1713b47aa2df7b2a8b976eb78efbb012554288313273374fb6ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c827cc54153ec8c5c11aaa0d92b5130610eed6d030d159ecde2870b036c4c68c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c34914414f8ed552881d39b938443d72ff5a1176a936f1d73744321424abed50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745478a878cf89c1e3c06c9ec4d92daccd73a6d01787ea916852a1e63dd71eaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f74263ce407217ccc65544caa0c58602d35e4ad1082dcb016ae53e24b3c0f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateScratchDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc518013cdbedf88146b5497e217491082ecf44a3d2825a3bd8a37008337e036(
    *,
    scopes: typing.Sequence[builtins.str],
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee34a8677c516e1c5fba077c940d36cdd240fb0ed2fe07e61e435cda871464e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741002a698ffdd212c527cbd7c6d0e15537fb126973483f4840d88b98b2cbc17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c91949290b43300967bc4c54ac41b204ee65ab1134159202aeff4c2521db0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e33ecd4e107c56bd3b6b9b43bc15018d2115c397378923ef887428141b33b9(
    value: typing.Optional[ComputeInstanceFromTemplateServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455ee1ebf4dd4bf213811021b69e2de383494dab5805ae7f62ca3164ccef1519(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01f847d2755eb2bdf75e22589fe0af36952ab4b5c3bfa1bcab947881a67aed8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21432796cd8cf553d8d902b16d70d1c3a421472e0519d7b3db466f35aa75ad5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ab17741e4cd391f2cd7d9145baeecc581bd02b51bd787dfe9c55581ba1db4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480a5ee53535f2760caeddca8192c5f32213218459453087c86578ca3e3882e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ccd9c3b78dca0070ddc88730b4e3e0f67f10dcb2f58fa19cff636a5ae348d42(
    value: typing.Optional[ComputeInstanceFromTemplateShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26705c144857a3804fd6c63df6b225b85c11ba8f2997990ff5fdb1d572163c5e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b7cc3e0e550257f1c8a0a0e91bafd650338ce4924504b27349842d2c446cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389e1a5616d9cd6992f79b40b364d6d63285465f672dc9dffb702898b276b49c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9a7bbddbb36428a1c8c42c1840585b58794bb151ace17d27abbf4003fda836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cb012fbbdcdeed0dfcb2696f1f35c4d6948576e47dba53e96abc0f61277f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131d2f00ad120ec1e80a8f39d9164971968f2c4a6c0ca0c764090543d4fd4575(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceFromTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

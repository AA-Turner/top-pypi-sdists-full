r'''
# `google_compute_instance`

Refer to the Terraform Registry for docs: [`google_compute_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance).
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


class ComputeInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance google_compute_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        boot_disk: typing.Union["ComputeInstanceBootDisk", typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        name: builtins.str,
        network_interface: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
        advanced_machine_features: typing.Optional[typing.Union["ComputeInstanceAdvancedMachineFeatures", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceAttachedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union["ComputeInstanceConfidentialInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_status: typing.Optional[builtins.str] = None,
        enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_encryption_key: typing.Optional[typing.Union["ComputeInstanceInstanceEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeInstanceParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceScratchDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance google_compute_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#boot_disk ComputeInstance#boot_disk}
        :param machine_type: The machine type to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#machine_type ComputeInstance#machine_type}
        :param name: The name of the instance. One of name or self_link must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#name ComputeInstance#name}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_interface ComputeInstance#network_interface}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#advanced_machine_features ComputeInstance#advanced_machine_features}
        :param allow_stopping_for_update: If true, allows Terraform to stop the instance to update its properties. If you try to update a property that requires stopping the instance without setting this field, the update will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#allow_stopping_for_update ComputeInstance#allow_stopping_for_update}
        :param attached_disk: attached_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#attached_disk ComputeInstance#attached_disk}
        :param can_ip_forward: Whether sending and receiving of packets with non-matching source or destination IPs is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#can_ip_forward ComputeInstance#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_config ComputeInstance#confidential_instance_config}
        :param deletion_protection: Whether deletion protection is enabled on this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#deletion_protection ComputeInstance#deletion_protection}
        :param description: A brief description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#description ComputeInstance#description}
        :param desired_status: Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#desired_status ComputeInstance#desired_status}
        :param enable_display: Whether the instance has virtual displays enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_display ComputeInstance#enable_display}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_accelerator ComputeInstance#guest_accelerator}
        :param hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#hostname ComputeInstance#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#id ComputeInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_encryption_key: instance_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_encryption_key ComputeInstance#instance_encryption_key}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key_revocation_action_type ComputeInstance#key_revocation_action_type}
        :param labels: A set of key/value label pairs assigned to the instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        :param metadata: Metadata key/value pairs made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata ComputeInstance#metadata}
        :param metadata_startup_script: Metadata startup scripts made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata_startup_script ComputeInstance#metadata_startup_script}
        :param min_cpu_platform: The minimum CPU platform specified for the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_cpu_platform ComputeInstance#min_cpu_platform}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_performance_config ComputeInstance#network_performance_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#params ComputeInstance#params}
        :param project: The ID of the project in which the resource belongs. If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#project ComputeInstance#project}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#reservation_affinity ComputeInstance#reservation_affinity}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scheduling ComputeInstance#scheduling}
        :param scratch_disk: scratch_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scratch_disk ComputeInstance#scratch_disk}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#service_account ComputeInstance#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#shielded_instance_config ComputeInstance#shielded_instance_config}
        :param tags: The list of tags attached to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#tags ComputeInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#timeouts ComputeInstance#timeouts}
        :param zone: The zone of the instance. If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#zone ComputeInstance#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__290f2c91cfbcf5ca7d49837a3242d9ed80e731ae8831b7462d96efc24f7e736b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeInstanceConfig(
            boot_disk=boot_disk,
            machine_type=machine_type,
            name=name,
            network_interface=network_interface,
            advanced_machine_features=advanced_machine_features,
            allow_stopping_for_update=allow_stopping_for_update,
            attached_disk=attached_disk,
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
            metadata=metadata,
            metadata_startup_script=metadata_startup_script,
            min_cpu_platform=min_cpu_platform,
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
        '''Generates CDKTF code for importing a ComputeInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeInstance to import.
        :param import_from_id: The id of the existing ComputeInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53b2117eafd7532c0776ef4f697c1c68de3cdced86d3aefd043cd32b3b993cc)
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_nested_virtualization ComputeInstance#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_uefi_networking ComputeInstance#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#performance_monitoring_unit ComputeInstance#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#threads_per_core ComputeInstance#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#turbo_mode ComputeInstance#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#visible_core_count ComputeInstance#visible_core_count}
        '''
        value = ComputeInstanceAdvancedMachineFeatures(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceAttachedDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29a149b444426d9ef8fa3ead437f593af63bef723a0212f77c5201d3b70bbed)
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
        initialize_params: typing.Optional[typing.Union["ComputeInstanceBootDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete: Whether the disk will be auto-deleted when the instance is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#auto_delete ComputeInstance#auto_delete}
        :param device_name: Name with which attached disk will be accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_raw ComputeInstance#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_rsa ComputeInstance#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_service_account ComputeInstance#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#force_attach ComputeInstance#force_attach}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_os_features ComputeInstance#guest_os_features}
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#initialize_params ComputeInstance#initialize_params}
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#interface ComputeInstance#interface}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#mode ComputeInstance#mode}
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source ComputeInstance#source}
        '''
        value = ComputeInstanceBootDisk(
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
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_type ComputeInstance#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        '''
        value = ComputeInstanceConfidentialInstanceConfig(
            confidential_instance_type=confidential_instance_type,
            enable_confidential_compute=enable_confidential_compute,
        )

        return typing.cast(None, jsii.invoke(self, "putConfidentialInstanceConfig", [value]))

    @jsii.member(jsii_name="putGuestAccelerator")
    def put_guest_accelerator(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a759f3f27da877335bb6a65cd704f5a65a77c45b945f2833e3c1349e0309b82b)
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        '''
        value = ComputeInstanceInstanceEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceEncryptionKey", [value]))

    @jsii.member(jsii_name="putNetworkInterface")
    def put_network_interface(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e627681ae7c4eeff9ba8317a97c0c9ed42d3e2a3bf3b9f2bdba1a8e7e89ce8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterface", [value]))

    @jsii.member(jsii_name="putNetworkPerformanceConfig")
    def put_network_performance_config(
        self,
        *,
        total_egress_bandwidth_tier: builtins.str,
    ) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#total_egress_bandwidth_tier ComputeInstance#total_egress_bandwidth_tier}
        '''
        value = ComputeInstanceNetworkPerformanceConfig(
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
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        '''
        value = ComputeInstanceParams(resource_manager_tags=resource_manager_tags)

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#specific_reservation ComputeInstance#specific_reservation}
        '''
        value = ComputeInstanceReservationAffinity(
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
        local_ssd_recovery_timeout: typing.Optional[typing.Union["ComputeInstanceSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#automatic_restart ComputeInstance#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#availability_domain ComputeInstance#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_termination_action ComputeInstance#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#local_ssd_recovery_timeout ComputeInstance#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#max_run_duration ComputeInstance#max_run_duration}
        :param min_node_cpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_node_cpus ComputeInstance#min_node_cpus}.
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#node_affinities ComputeInstance#node_affinities}
        :param on_host_maintenance: Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_host_maintenance ComputeInstance#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_instance_stop_action ComputeInstance#on_instance_stop_action}
        :param preemptible: Whether the instance is preemptible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#preemptible ComputeInstance#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioning_model ComputeInstance#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#termination_time ComputeInstance#termination_time}
        '''
        value = ComputeInstanceScheduling(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceScratchDisk", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1768b31a9631be009813c0d73ba1d1c5df99362e1f8076d5484c149b991efc8e)
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
        :param scopes: A list of service scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scopes ComputeInstance#scopes}
        :param email: The service account e-mail address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#email ComputeInstance#email}
        '''
        value = ComputeInstanceServiceAccount(scopes=scopes, email=email)

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
        :param enable_integrity_monitoring: Whether integrity monitoring is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_integrity_monitoring ComputeInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Whether secure boot is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_secure_boot ComputeInstance#enable_secure_boot}
        :param enable_vtpm: Whether the instance uses vTPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_vtpm ComputeInstance#enable_vtpm}
        '''
        value = ComputeInstanceShieldedInstanceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#create ComputeInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#delete ComputeInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#update ComputeInstance#update}.
        '''
        value = ComputeInstanceTimeouts(create=create, delete=delete, update=update)

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

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetMetadataStartupScript")
    def reset_metadata_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataStartupScript", []))

    @jsii.member(jsii_name="resetMinCpuPlatform")
    def reset_min_cpu_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCpuPlatform", []))

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
    ) -> "ComputeInstanceAdvancedMachineFeaturesOutputReference":
        return typing.cast("ComputeInstanceAdvancedMachineFeaturesOutputReference", jsii.get(self, "advancedMachineFeatures"))

    @builtins.property
    @jsii.member(jsii_name="attachedDisk")
    def attached_disk(self) -> "ComputeInstanceAttachedDiskList":
        return typing.cast("ComputeInstanceAttachedDiskList", jsii.get(self, "attachedDisk"))

    @builtins.property
    @jsii.member(jsii_name="bootDisk")
    def boot_disk(self) -> "ComputeInstanceBootDiskOutputReference":
        return typing.cast("ComputeInstanceBootDiskOutputReference", jsii.get(self, "bootDisk"))

    @builtins.property
    @jsii.member(jsii_name="confidentialInstanceConfig")
    def confidential_instance_config(
        self,
    ) -> "ComputeInstanceConfidentialInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceConfidentialInstanceConfigOutputReference", jsii.get(self, "confidentialInstanceConfig"))

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
    def guest_accelerator(self) -> "ComputeInstanceGuestAcceleratorList":
        return typing.cast("ComputeInstanceGuestAcceleratorList", jsii.get(self, "guestAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="instanceEncryptionKey")
    def instance_encryption_key(
        self,
    ) -> "ComputeInstanceInstanceEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceInstanceEncryptionKeyOutputReference", jsii.get(self, "instanceEncryptionKey"))

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
    def network_interface(self) -> "ComputeInstanceNetworkInterfaceList":
        return typing.cast("ComputeInstanceNetworkInterfaceList", jsii.get(self, "networkInterface"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfig")
    def network_performance_config(
        self,
    ) -> "ComputeInstanceNetworkPerformanceConfigOutputReference":
        return typing.cast("ComputeInstanceNetworkPerformanceConfigOutputReference", jsii.get(self, "networkPerformanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeInstanceParamsOutputReference":
        return typing.cast("ComputeInstanceParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "ComputeInstanceReservationAffinityOutputReference":
        return typing.cast("ComputeInstanceReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "ComputeInstanceSchedulingOutputReference":
        return typing.cast("ComputeInstanceSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="scratchDisk")
    def scratch_disk(self) -> "ComputeInstanceScratchDiskList":
        return typing.cast("ComputeInstanceScratchDiskList", jsii.get(self, "scratchDisk"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> "ComputeInstanceServiceAccountOutputReference":
        return typing.cast("ComputeInstanceServiceAccountOutputReference", jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "ComputeInstanceShieldedInstanceConfigOutputReference":
        return typing.cast("ComputeInstanceShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

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
    def timeouts(self) -> "ComputeInstanceTimeoutsOutputReference":
        return typing.cast("ComputeInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedMachineFeaturesInput")
    def advanced_machine_features_input(
        self,
    ) -> typing.Optional["ComputeInstanceAdvancedMachineFeatures"]:
        return typing.cast(typing.Optional["ComputeInstanceAdvancedMachineFeatures"], jsii.get(self, "advancedMachineFeaturesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceAttachedDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceAttachedDisk"]]], jsii.get(self, "attachedDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskInput")
    def boot_disk_input(self) -> typing.Optional["ComputeInstanceBootDisk"]:
        return typing.cast(typing.Optional["ComputeInstanceBootDisk"], jsii.get(self, "bootDiskInput"))

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
    ) -> typing.Optional["ComputeInstanceConfidentialInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceConfidentialInstanceConfig"], jsii.get(self, "confidentialInstanceConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGuestAccelerator"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGuestAccelerator"]]], jsii.get(self, "guestAcceleratorInput"))

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
    ) -> typing.Optional["ComputeInstanceInstanceEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceInstanceEncryptionKey"], jsii.get(self, "instanceEncryptionKeyInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterface"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterface"]]], jsii.get(self, "networkInterfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPerformanceConfigInput")
    def network_performance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceNetworkPerformanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceNetworkPerformanceConfig"], jsii.get(self, "networkPerformanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeInstanceParams"]:
        return typing.cast(typing.Optional["ComputeInstanceParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["ComputeInstanceReservationAffinity"]:
        return typing.cast(typing.Optional["ComputeInstanceReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoliciesInput")
    def resource_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcePoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(self) -> typing.Optional["ComputeInstanceScheduling"]:
        return typing.cast(typing.Optional["ComputeInstanceScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="scratchDiskInput")
    def scratch_disk_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceScratchDisk"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceScratchDisk"]]], jsii.get(self, "scratchDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional["ComputeInstanceServiceAccount"]:
        return typing.cast(typing.Optional["ComputeInstanceServiceAccount"], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["ComputeInstanceShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["ComputeInstanceShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7756b5ed8f8406518949f0bfeaca82f635b993edb2d223614619644ce40bfd7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f960bb641a75e86cbfa3a27374f2ee28983cc434b7012de1e10ebc3bf5eefe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__427f75cb779d85c9957641c00a4840081b56b9d69e1ebb116220e4a936fa56be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd41ee930da4af3d967cfe119fc2d574b554aefafc4605574e9f6452e206898f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredStatus")
    def desired_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredStatus"))

    @desired_status.setter
    def desired_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6da9f095b73aabaabd58ea461863d88bd4e47584ad50c550a53f566fdd2588f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__065755ad43513ed805e90fc73085984b6f671c22bd9069d550a859bea392ddb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDisplay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda87abc48554832b07a2c345cad1928b92f45952334342baa95e732d535f76d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061304b8bc9570ce3fca71cac41f2b997026b95b595f7aa23429d1222ae37eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyRevocationActionType")
    def key_revocation_action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRevocationActionType"))

    @key_revocation_action_type.setter
    def key_revocation_action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef068c9e1afbe374911fcf63f0589eb503b1cd7c8398bc054b2c6cab155f0222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRevocationActionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdce184c3b2985bd988d83092ae31975b076c98c2cadd6d64b9aebfac1e437f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760dfdd55fc96516c89ffafb0fcaf8bafeada525c502ff82e31b7c3a50fbe1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb64d30161e10e4e7a70f61088ceecc41e49bf39745ec45dda29947b448deac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataStartupScript")
    def metadata_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataStartupScript"))

    @metadata_startup_script.setter
    def metadata_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827386a96976cb5b1cfba8f1bc4df2088eb270ac10456661ab94c50a35e2c532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCpuPlatform")
    def min_cpu_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minCpuPlatform"))

    @min_cpu_platform.setter
    def min_cpu_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a169c5318895aceaeb171d76cf286a94a57843f6c5b00f70d61c77261015cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCpuPlatform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8506f735770aabd3c417d5907828feac75ac4de895836d9753ce344f9ad47a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8e2ff78ae49fbe74b1a6d75b8cb2776df65ef14b9319d1ea6998f91acd3665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f66d79ab5ce3d572feb9b21e5e3d8d3b207adaaa11d2b0be17bfa1a43b1ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccdb614ea5d81676be57c95ade78da673429e7dbc3067a97ade21cabfad5ae0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693f266e167f90f7e06d05dcbcfd503199145272bd25e65646b52c2fcf3c7ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceAdvancedMachineFeatures",
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
class ComputeInstanceAdvancedMachineFeatures:
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
        :param enable_nested_virtualization: Whether to enable nested virtualization or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_nested_virtualization ComputeInstance#enable_nested_virtualization}
        :param enable_uefi_networking: Whether to enable UEFI networking for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_uefi_networking ComputeInstance#enable_uefi_networking}
        :param performance_monitoring_unit: The PMU is a hardware component within the CPU core that monitors how the processor runs code. Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#performance_monitoring_unit ComputeInstance#performance_monitoring_unit}
        :param threads_per_core: The number of threads per physical core. To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#threads_per_core ComputeInstance#threads_per_core}
        :param turbo_mode: Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#turbo_mode ComputeInstance#turbo_mode}
        :param visible_core_count: The number of physical cores to expose to an instance. Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#visible_core_count ComputeInstance#visible_core_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1f1f06dbd218092332eec29815353905478360269f95dc2c873e35932ad042)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_nested_virtualization ComputeInstance#enable_nested_virtualization}
        '''
        result = self._values.get("enable_nested_virtualization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_uefi_networking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to enable UEFI networking for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_uefi_networking ComputeInstance#enable_uefi_networking}
        '''
        result = self._values.get("enable_uefi_networking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_monitoring_unit(self) -> typing.Optional[builtins.str]:
        '''The PMU is a hardware component within the CPU core that monitors how the processor runs code.

        Valid values for the level of PMU are "STANDARD", "ENHANCED", and "ARCHITECTURAL".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#performance_monitoring_unit ComputeInstance#performance_monitoring_unit}
        '''
        result = self._values.get("performance_monitoring_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        '''The number of threads per physical core.

        To disable simultaneous multithreading (SMT) set this to 1. If unset, the maximum number of threads supported per core by the underlying processor is assumed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#threads_per_core ComputeInstance#threads_per_core}
        '''
        result = self._values.get("threads_per_core")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def turbo_mode(self) -> typing.Optional[builtins.str]:
        '''Turbo frequency mode to use for the instance. Currently supported modes is "ALL_CORE_MAX".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#turbo_mode ComputeInstance#turbo_mode}
        '''
        result = self._values.get("turbo_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visible_core_count(self) -> typing.Optional[jsii.Number]:
        '''The number of physical cores to expose to an instance.

        Multiply by the number of threads per core to compute the total number of virtual CPUs to expose to the instance. If unset, the number of cores is inferred from the instance's nominal CPU count and the underlying platform's SMT width.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#visible_core_count ComputeInstance#visible_core_count}
        '''
        result = self._values.get("visible_core_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceAdvancedMachineFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceAdvancedMachineFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceAdvancedMachineFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6896ed0c81d27b7ef0d156c58b58a4e4a9ccb4270e89c2473727a3fd4a51dad7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4449693053c0b28706e9b71deb0cd5d9bf60d082f43b2a4280a5c57782983e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3952df36ee2702b4b4842bb54875a32a071848fd511c6f48690adf60aeb678c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUefiNetworking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="performanceMonitoringUnit")
    def performance_monitoring_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceMonitoringUnit"))

    @performance_monitoring_unit.setter
    def performance_monitoring_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354e337987b5aedac5120975d7d61b67a66213fea8238ef860554d192641f7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceMonitoringUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threadsPerCore")
    def threads_per_core(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threadsPerCore"))

    @threads_per_core.setter
    def threads_per_core(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8395ad1d4fb9adaf96cf64a586f2985662e951e9545a57a78b1d67ba33633e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threadsPerCore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="turboMode")
    def turbo_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "turboMode"))

    @turbo_mode.setter
    def turbo_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ef7a206a017d81348ea1cbcb5991af649072c06da7257d4f3503ebcc68edee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "turboMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visibleCoreCount")
    def visible_core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "visibleCoreCount"))

    @visible_core_count.setter
    def visible_core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe0a6bd2b5eecc30f7e3e8bfdbabe6452a127613f76db022a8a6d42f8ef7372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visibleCoreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceAdvancedMachineFeatures]:
        return typing.cast(typing.Optional[ComputeInstanceAdvancedMachineFeatures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceAdvancedMachineFeatures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e0b15e03f5c67c3b61a4af1f597fe912b770e46e0683e97180e7ce9718a9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceAttachedDisk",
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
class ComputeInstanceAttachedDisk:
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
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source ComputeInstance#source}
        :param device_name: Name with which the attached disk is accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_raw ComputeInstance#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_rsa ComputeInstance#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_service_account ComputeInstance#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#force_attach ComputeInstance#force_attach}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#mode ComputeInstance#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5791174c7096db26469e7488aef666a0a68f8e3aae2a4ac8e91a705149be4377)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source ComputeInstance#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which the attached disk is accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_raw(self) -> typing.Optional[builtins.str]:
        '''A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_raw ComputeInstance#disk_encryption_key_raw}
        '''
        result = self._values.get("disk_encryption_key_raw")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_rsa(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_rsa ComputeInstance#disk_encryption_key_rsa}
        '''
        result = self._values.get("disk_encryption_key_rsa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_service_account ComputeInstance#disk_encryption_service_account}
        '''
        result = self._values.get("disk_encryption_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_attach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force attach the regional disk even if it's currently attached to another instance.

        If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#force_attach ComputeInstance#force_attach}
        '''
        result = self._values.get("force_attach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_rsa and disk_encryption_key_raw may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#mode ComputeInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceAttachedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceAttachedDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceAttachedDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__766a0fc5b82a2e8a47d9492efe79c4064c190b24eca2f6d3dc3bbde2044d5451)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceAttachedDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ecf2f43d9f3efb39b861950548c11f8f7f405b30505b01b13c8acdf813b2be4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceAttachedDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f8c5418147a56ea8c1a5e620494baef9e902cdd83b0a9f1465eed2ca35d7e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7efdc477bcfd00d0a07a5ce95fccb9c97e58d6a6fd3b3b4b20fb55c1c2b8f045)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9dcf52f4b01a319b1b0a260e76141bd86aac4adadae0dba30a0ac841e37ce1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58f499fda67d2879b611bfef9b56527bc6326008de397a29e2efe24d544e850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceAttachedDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceAttachedDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6ed98aee1d4a730f1d8525e6b5d994b89666d8e7e443eb38786cd534ba9bbda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b52182cf1f47dbc5902e57d7effb6caa0f031e111819ca85ff254cec5129dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRaw")
    def disk_encryption_key_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRaw"))

    @disk_encryption_key_raw.setter
    def disk_encryption_key_raw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d227f661ccb7e9912e0c5f8f2ac0b121dcac6d01a56ec77b62885884de45da7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsa")
    def disk_encryption_key_rsa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRsa"))

    @disk_encryption_key_rsa.setter
    def disk_encryption_key_rsa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549e8f7872790a4c28206c979764db7e1575beed53c1701ac1907adeaf1c65b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRsa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccount")
    def disk_encryption_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionServiceAccount"))

    @disk_encryption_service_account.setter
    def disk_encryption_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb3b153ccd366beeb48024224932ebfd4cc657f999a0ce4afc87310f8320057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17f32054bf5013428d44a28d8b5ba828ec755fc7d6804ca9c85489dbc45c4f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceAttach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e591fbd4113e32dac6dcc8c095236cff31c143f6c1cedbe06ed861d6db7f268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04daec281927de00856a055a0954faaff4306cbc4101ad05872290d10c15e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d079f8652825c7b79014c3d5f3a8957b348177c289ee69b250bc47d880c576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceAttachedDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceAttachedDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceAttachedDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf3bea91876f22316f73d4d46203be5eec809b304f28192c731a592567a93da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDisk",
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
class ComputeInstanceBootDisk:
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
        initialize_params: typing.Optional[typing.Union["ComputeInstanceBootDiskInitializeParams", typing.Dict[builtins.str, typing.Any]]] = None,
        interface: typing.Optional[builtins.str] = None,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auto_delete: Whether the disk will be auto-deleted when the instance is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#auto_delete ComputeInstance#auto_delete}
        :param device_name: Name with which attached disk will be accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        :param disk_encryption_key_raw: A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_raw ComputeInstance#disk_encryption_key_raw}
        :param disk_encryption_key_rsa: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_rsa ComputeInstance#disk_encryption_key_rsa}
        :param disk_encryption_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_service_account ComputeInstance#disk_encryption_service_account}
        :param force_attach: Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#force_attach ComputeInstance#force_attach}
        :param guest_os_features: A list of features to enable on the guest operating system. Applicable only for bootable images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_os_features ComputeInstance#guest_os_features}
        :param initialize_params: initialize_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#initialize_params ComputeInstance#initialize_params}
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#interface ComputeInstance#interface}
        :param kms_key_self_link: The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk. Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param mode: Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#mode ComputeInstance#mode}
        :param source: The name or self_link of the disk attached to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source ComputeInstance#source}
        '''
        if isinstance(initialize_params, dict):
            initialize_params = ComputeInstanceBootDiskInitializeParams(**initialize_params)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba93eb74fb1ffbdba71869e9b2ac86d5ff04794be94aeb7a30bd850572746c6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#auto_delete ComputeInstance#auto_delete}
        '''
        result = self._values.get("auto_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which attached disk will be accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_raw(self) -> typing.Optional[builtins.str]:
        '''A 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_raw ComputeInstance#disk_encryption_key_raw}
        '''
        result = self._values.get("disk_encryption_key_raw")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key_rsa(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_key_rsa ComputeInstance#disk_encryption_key_rsa}
        '''
        result = self._values.get("disk_encryption_key_rsa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#disk_encryption_service_account ComputeInstance#disk_encryption_service_account}
        '''
        result = self._values.get("disk_encryption_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_attach(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to force attach the regional disk even if it's currently attached to another instance.

        If you try to force attach a zonal disk to an instance, you will receive an error. Setting this parameter cause VM recreation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#force_attach ComputeInstance#force_attach}
        '''
        result = self._values.get("force_attach")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_os_features(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of features to enable on the guest operating system. Applicable only for bootable images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_os_features ComputeInstance#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def initialize_params(
        self,
    ) -> typing.Optional["ComputeInstanceBootDiskInitializeParams"]:
        '''initialize_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#initialize_params ComputeInstance#initialize_params}
        '''
        result = self._values.get("initialize_params")
        return typing.cast(typing.Optional["ComputeInstanceBootDiskInitializeParams"], result)

    @builtins.property
    def interface(self) -> typing.Optional[builtins.str]:
        '''The disk interface used for attaching this disk.

        One of SCSI or NVME. (This field is shared with attached_disk and only used for specific cases, please don't specify this field without advice from Google.)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#interface ComputeInstance#interface}
        '''
        result = self._values.get("interface")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self_link of the encryption key that is stored in Google Cloud KMS to encrypt this disk.

        Only one of kms_key_self_link, disk_encryption_key_raw and disk_encryption_key_rsa may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Read/write mode for the disk. One of "READ_ONLY" or "READ_WRITE".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#mode ComputeInstance#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the disk attached to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source ComputeInstance#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceBootDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParams",
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
class ComputeInstanceBootDiskInitializeParams:
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
        source_image_encryption_key: typing.Optional[typing.Union["ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the disk. One of "X86_64" or "ARM64". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#architecture ComputeInstance#architecture}
        :param enable_confidential_compute: A flag to enable confidential compute mode on boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        :param image: The image from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#image ComputeInstance#image}
        :param labels: A set of key/value label pairs assigned to the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_iops ComputeInstance#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_throughput ComputeInstance#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance's boot disk. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        :param size: The size of the image in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#size ComputeInstance#size}
        :param snapshot: The snapshot from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#snapshot ComputeInstance#snapshot}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_image_encryption_key ComputeInstance#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_snapshot_encryption_key ComputeInstance#source_snapshot_encryption_key}
        :param storage_pool: The URL of the storage pool in which the new disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#storage_pool ComputeInstance#storage_pool}
        :param type: The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3d6ad5fb33e7f9aff937fb161dc6fef73dee1d5ac9c71a10219ba1fff95633)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#architecture ComputeInstance#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A flag to enable confidential compute mode on boot disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''The image from which this disk was initialised.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#image ComputeInstance#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs assigned to the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS to provision for the disk.

        This sets the number of I/O operations per second that the disk can handle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_iops ComputeInstance#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much throughput to provision for the disk.

        This sets the number of throughput mb per second that the disk can handle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_throughput ComputeInstance#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of resource manager tags.

        Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance's boot disk.

        Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the image in gigabytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#size ComputeInstance#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot(self) -> typing.Optional[builtins.str]:
        '''The snapshot from which this disk was initialised.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#snapshot ComputeInstance#snapshot}
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_image_encryption_key ComputeInstance#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_snapshot_encryption_key ComputeInstance#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def storage_pool(self) -> typing.Optional[builtins.str]:
        '''The URL of the storage pool in which the new disk is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#storage_pool ComputeInstance#storage_pool}
        '''
        result = self._values.get("storage_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceBootDiskInitializeParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceBootDiskInitializeParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2feff607ff6b4114c93ec066e27ba686cda127e2be6984069d988915e6fc36f4)
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        value = ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey(
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
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        value = ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey(
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
    ) -> "ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

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
    ) -> typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__263da046501fbe1666d80eada26820b248e5be14e20bf74798e37407a4c324f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ea563b350858a1e59b89ac9522c7a3810873adf3426fffd6e0937d243905cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7763fc88398d4f7d163b6cc8764eb98b2bfdc3868afc323924216b5a2d7ac823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6174fdb85d0796d8da4db3f99bd753d4f5808d9cfb42ccab866ee9b3c4b43a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f342a6054bf7ccd69808100f5582090bf2f11cca7a5d2be566c3a2ded5835d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ff5c64d69bb6e40cb26d6e49ffb55f95077ab654fdd04bf6e024bde52cbb14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6efd4521a9e3fd01c8cb0c713051958d77e5ba98713236e40ef5927e819b1adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourcePolicies")
    def resource_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourcePolicies"))

    @resource_policies.setter
    def resource_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79455b257cbf00aa498719c292c6aba022e666ef1f60799543a6462f658067c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4385f7be9e0b542b021c3fddbfe6a898b59f2f7e9d2432ef5a65c7f2840c4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @snapshot.setter
    def snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710457e1e5c6ee2bca5680fcce2efb315a8a27d281aefadbdd2acd04a0f259cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabb03317208203b08db2273873a973fbadab03b17736b71182d7873c264cc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e756e787ff793572ed7e661eab19d269776290b8f6b0878ddf5a3bcc9cc2a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceBootDiskInitializeParams]:
        return typing.cast(typing.Optional[ComputeInstanceBootDiskInitializeParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceBootDiskInitializeParams],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b4a3bfb8ef194598a35ffd579ed240f4043f5a68234d2012ff38407ce59c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ea19c6983271410c306dd298bd766e885d01a4db3291c97b8b1a92b8e21d1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fca8c92638529a6f163ff0f4bd8670d7b608015b069a27d2d0a16c5efe824c43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c74b9824609d4232aa77f9e5f52809305004713228044387097d379be0a970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c89166dc95304bb67d2182aec35bf8736b55a24c56c3e96d498b390baca7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c5997146c760bf69237e6ed37a05eab26ce5bf76457a41f4c4bacb86c60265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__674cf2b0a25eea0979905440a72f7abeee3779475078bac9674bb6ccf2d3a2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b5ae2d7938cc50eb152b23fc65c010320a19c43d795207e5e76519b4cfecbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0143667c9510f954bcf1b048a0a79f91c3ccc2349ceb3c4b9d0fda2a4073d769)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#raw_key ComputeInstance#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        Only one of kms_key_self_link, rsa_encrypted_key and raw_key may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#rsa_encrypted_key ComputeInstance#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f851cca632edeaafd3430e34729b642dd553c36849cff7cd809fc38a8b95d94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d6d10f11b173a6eeca7dfcc67c13eacaa376100134152bb4d0f4469d1a422e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbc54eb94a4100588f9d64ac99b275dc65ef49e7596814f24780a41ede8e6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d700642c3448dcff00636cb10415a62296fe87c573a98e255c02394a91c3e3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae178b87574ce8d804e5bfeafa6f55cdcfa5195ec67a0342d1a860f9feb31254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc7570d4fa84751783dff7ae4ed48cf02ce0c0ca2bcea54ed5eb62c5a6ae1b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceBootDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceBootDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__338c6e5bf586fa4dce16a010800aba4b9cbada2ffb8ba862c602061069058812)
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
        source_image_encryption_key: typing.Optional[typing.Union[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param architecture: The architecture of the disk. One of "X86_64" or "ARM64". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#architecture ComputeInstance#architecture}
        :param enable_confidential_compute: A flag to enable confidential compute mode on boot disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        :param image: The image from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#image ComputeInstance#image}
        :param labels: A set of key/value label pairs assigned to the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_iops ComputeInstance#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioned_throughput ComputeInstance#provisioned_throughput}
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        :param resource_policies: A list of self_links of resource policies to attach to the instance's boot disk. Modifying this list will cause the instance to recreate. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        :param size: The size of the image in gigabytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#size ComputeInstance#size}
        :param snapshot: The snapshot from which this disk was initialised. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#snapshot ComputeInstance#snapshot}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_image_encryption_key ComputeInstance#source_image_encryption_key}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#source_snapshot_encryption_key ComputeInstance#source_snapshot_encryption_key}
        :param storage_pool: The URL of the storage pool in which the new disk is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#storage_pool ComputeInstance#storage_pool}
        :param type: The Google Compute Engine disk type. Such as pd-standard, pd-ssd or pd-balanced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        value = ComputeInstanceBootDiskInitializeParams(
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
    ) -> ComputeInstanceBootDiskInitializeParamsOutputReference:
        return typing.cast(ComputeInstanceBootDiskInitializeParamsOutputReference, jsii.get(self, "initializeParams"))

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
    ) -> typing.Optional[ComputeInstanceBootDiskInitializeParams]:
        return typing.cast(typing.Optional[ComputeInstanceBootDiskInitializeParams], jsii.get(self, "initializeParamsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7eb378aefe21f38ee695fa1310290112793543fc9e7132e37af9b683397c6c04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792d84d9c2efa556ad5991c92bdeb83de285d65eb29ed5c2a9f794cad6e4a06c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRaw")
    def disk_encryption_key_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRaw"))

    @disk_encryption_key_raw.setter
    def disk_encryption_key_raw(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9758ca65b83e42a2040375b8cd6d80c8d7c6679e640324a929a8e84fcdc91b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRaw", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyRsa")
    def disk_encryption_key_rsa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionKeyRsa"))

    @disk_encryption_key_rsa.setter
    def disk_encryption_key_rsa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503f05c7fa9933dd2163ac336eab4748de4128c5dd6daabd02d1007ad9a97e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionKeyRsa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionServiceAccount")
    def disk_encryption_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryptionServiceAccount"))

    @disk_encryption_service_account.setter
    def disk_encryption_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a808146aa1f350c02bbf3b82e1ace1867910c06a6b7e8f3b511b8ddd4f7b3d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb7450501b2205835a01c09ba10f89f890cbfe8b591b141403e06bf6c6f08961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceAttach", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "guestOsFeatures"))

    @guest_os_features.setter
    def guest_os_features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ad89a563e4d78b7cfff693bd0f00f953d9aba889a847bc278650f393e858a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guestOsFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b58b03b54746004002e5904fa2bb53afaac3e0ee4a9b77fbe4044b037b474b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1343726947627bfa1258c55b4325c042414883707cf8134fb59c40dd27f62e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81793065d3253cfb637b8fe56060f8d702c3197eb2d472398899587d91b072b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126e5979b53b28188291996386c2e475da6bc2d9ddb336dcf06d69950d28a145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceBootDisk]:
        return typing.cast(typing.Optional[ComputeInstanceBootDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeInstanceBootDisk]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a178d054d197480a110df5108db9c0f7c3317339d39947ffe158218b0d76aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceConfidentialInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "confidential_instance_type": "confidentialInstanceType",
        "enable_confidential_compute": "enableConfidentialCompute",
    },
)
class ComputeInstanceConfidentialInstanceConfig:
    def __init__(
        self,
        *,
        confidential_instance_type: typing.Optional[builtins.str] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param confidential_instance_type: The confidential computing technology the instance uses. SEV is an AMD feature. TDX is an Intel feature. One of the following values is required: SEV, SEV_SNP, TDX. If SEV_SNP, min_cpu_platform = "AMD Milan" is currently required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_type ComputeInstance#confidential_instance_type}
        :param enable_confidential_compute: Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f97210661d238da5afbc3935a612adff197fadad31e26f79150f3f12e00c2a4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_type ComputeInstance#confidential_instance_type}
        '''
        result = self._values.get("confidential_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance should have confidential compute enabled. Field will be deprecated in a future release.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_confidential_compute ComputeInstance#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceConfidentialInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceConfidentialInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceConfidentialInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a929d62eafc2e9cbca9a82c799f48003fe304f67a222f5041c9003946f88490a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b3881a0d8307dd46eb16fc9e915dfb19eaffaa1b45e5572cf6074bb913d8bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e23950a95bfa52772d9388ad95074a60df37579a1119366f89bcdb88070cafb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceConfidentialInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceConfidentialInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceConfidentialInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6d50fb4946b93ba1487a9ba1644d0d84cb0240803f2da785e343c50204cf35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "boot_disk": "bootDisk",
        "machine_type": "machineType",
        "name": "name",
        "network_interface": "networkInterface",
        "advanced_machine_features": "advancedMachineFeatures",
        "allow_stopping_for_update": "allowStoppingForUpdate",
        "attached_disk": "attachedDisk",
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
        "metadata": "metadata",
        "metadata_startup_script": "metadataStartupScript",
        "min_cpu_platform": "minCpuPlatform",
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
class ComputeInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        boot_disk: typing.Union[ComputeInstanceBootDisk, typing.Dict[builtins.str, typing.Any]],
        machine_type: builtins.str,
        name: builtins.str,
        network_interface: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterface", typing.Dict[builtins.str, typing.Any]]]],
        advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
        can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_status: typing.Optional[builtins.str] = None,
        enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceGuestAccelerator", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_encryption_key: typing.Optional[typing.Union["ComputeInstanceInstanceEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        key_revocation_action_type: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata_startup_script: typing.Optional[builtins.str] = None,
        min_cpu_platform: typing.Optional[builtins.str] = None,
        network_performance_config: typing.Optional[typing.Union["ComputeInstanceNetworkPerformanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        params: typing.Optional[typing.Union["ComputeInstanceParams", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["ComputeInstanceReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        scheduling: typing.Optional[typing.Union["ComputeInstanceScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceScratchDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        service_account: typing.Optional[typing.Union["ComputeInstanceServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_config: typing.Optional[typing.Union["ComputeInstanceShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param boot_disk: boot_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#boot_disk ComputeInstance#boot_disk}
        :param machine_type: The machine type to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#machine_type ComputeInstance#machine_type}
        :param name: The name of the instance. One of name or self_link must be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#name ComputeInstance#name}
        :param network_interface: network_interface block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_interface ComputeInstance#network_interface}
        :param advanced_machine_features: advanced_machine_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#advanced_machine_features ComputeInstance#advanced_machine_features}
        :param allow_stopping_for_update: If true, allows Terraform to stop the instance to update its properties. If you try to update a property that requires stopping the instance without setting this field, the update will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#allow_stopping_for_update ComputeInstance#allow_stopping_for_update}
        :param attached_disk: attached_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#attached_disk ComputeInstance#attached_disk}
        :param can_ip_forward: Whether sending and receiving of packets with non-matching source or destination IPs is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#can_ip_forward ComputeInstance#can_ip_forward}
        :param confidential_instance_config: confidential_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_config ComputeInstance#confidential_instance_config}
        :param deletion_protection: Whether deletion protection is enabled on this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#deletion_protection ComputeInstance#deletion_protection}
        :param description: A brief description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#description ComputeInstance#description}
        :param desired_status: Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#desired_status ComputeInstance#desired_status}
        :param enable_display: Whether the instance has virtual displays enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_display ComputeInstance#enable_display}
        :param guest_accelerator: guest_accelerator block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_accelerator ComputeInstance#guest_accelerator}
        :param hostname: A custom hostname for the instance. Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#hostname ComputeInstance#hostname}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#id ComputeInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_encryption_key: instance_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_encryption_key ComputeInstance#instance_encryption_key}
        :param key_revocation_action_type: Action to be taken when a customer's encryption key is revoked. Supports "STOP" and "NONE", with "NONE" being the default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key_revocation_action_type ComputeInstance#key_revocation_action_type}
        :param labels: A set of key/value label pairs assigned to the instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        :param metadata: Metadata key/value pairs made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata ComputeInstance#metadata}
        :param metadata_startup_script: Metadata startup scripts made available within the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata_startup_script ComputeInstance#metadata_startup_script}
        :param min_cpu_platform: The minimum CPU platform specified for the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_cpu_platform ComputeInstance#min_cpu_platform}
        :param network_performance_config: network_performance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_performance_config ComputeInstance#network_performance_config}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#params ComputeInstance#params}
        :param project: The ID of the project in which the resource belongs. If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#project ComputeInstance#project}
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#reservation_affinity ComputeInstance#reservation_affinity}
        :param resource_policies: A list of self_links of resource policies to attach to the instance. Currently a max of 1 resource policy is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scheduling ComputeInstance#scheduling}
        :param scratch_disk: scratch_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scratch_disk ComputeInstance#scratch_disk}
        :param service_account: service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#service_account ComputeInstance#service_account}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#shielded_instance_config ComputeInstance#shielded_instance_config}
        :param tags: The list of tags attached to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#tags ComputeInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#timeouts ComputeInstance#timeouts}
        :param zone: The zone of the instance. If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#zone ComputeInstance#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(boot_disk, dict):
            boot_disk = ComputeInstanceBootDisk(**boot_disk)
        if isinstance(advanced_machine_features, dict):
            advanced_machine_features = ComputeInstanceAdvancedMachineFeatures(**advanced_machine_features)
        if isinstance(confidential_instance_config, dict):
            confidential_instance_config = ComputeInstanceConfidentialInstanceConfig(**confidential_instance_config)
        if isinstance(instance_encryption_key, dict):
            instance_encryption_key = ComputeInstanceInstanceEncryptionKey(**instance_encryption_key)
        if isinstance(network_performance_config, dict):
            network_performance_config = ComputeInstanceNetworkPerformanceConfig(**network_performance_config)
        if isinstance(params, dict):
            params = ComputeInstanceParams(**params)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = ComputeInstanceReservationAffinity(**reservation_affinity)
        if isinstance(scheduling, dict):
            scheduling = ComputeInstanceScheduling(**scheduling)
        if isinstance(service_account, dict):
            service_account = ComputeInstanceServiceAccount(**service_account)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = ComputeInstanceShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7d352a39f94a2de429bc1f3219c2b473c07e3b4e97393a2f38b40019fb1d9c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument boot_disk", value=boot_disk, expected_type=type_hints["boot_disk"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument advanced_machine_features", value=advanced_machine_features, expected_type=type_hints["advanced_machine_features"])
            check_type(argname="argument allow_stopping_for_update", value=allow_stopping_for_update, expected_type=type_hints["allow_stopping_for_update"])
            check_type(argname="argument attached_disk", value=attached_disk, expected_type=type_hints["attached_disk"])
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
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument metadata_startup_script", value=metadata_startup_script, expected_type=type_hints["metadata_startup_script"])
            check_type(argname="argument min_cpu_platform", value=min_cpu_platform, expected_type=type_hints["min_cpu_platform"])
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
            "boot_disk": boot_disk,
            "machine_type": machine_type,
            "name": name,
            "network_interface": network_interface,
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
        if metadata is not None:
            self._values["metadata"] = metadata
        if metadata_startup_script is not None:
            self._values["metadata_startup_script"] = metadata_startup_script
        if min_cpu_platform is not None:
            self._values["min_cpu_platform"] = min_cpu_platform
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
    def boot_disk(self) -> ComputeInstanceBootDisk:
        '''boot_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#boot_disk ComputeInstance#boot_disk}
        '''
        result = self._values.get("boot_disk")
        assert result is not None, "Required property 'boot_disk' is missing"
        return typing.cast(ComputeInstanceBootDisk, result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''The machine type to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#machine_type ComputeInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the instance. One of name or self_link must be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#name ComputeInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_interface(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterface"]]:
        '''network_interface block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_interface ComputeInstance#network_interface}
        '''
        result = self._values.get("network_interface")
        assert result is not None, "Required property 'network_interface' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterface"]], result)

    @builtins.property
    def advanced_machine_features(
        self,
    ) -> typing.Optional[ComputeInstanceAdvancedMachineFeatures]:
        '''advanced_machine_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#advanced_machine_features ComputeInstance#advanced_machine_features}
        '''
        result = self._values.get("advanced_machine_features")
        return typing.cast(typing.Optional[ComputeInstanceAdvancedMachineFeatures], result)

    @builtins.property
    def allow_stopping_for_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, allows Terraform to stop the instance to update its properties.

        If you try to update a property that requires stopping the instance without setting this field, the update will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#allow_stopping_for_update ComputeInstance#allow_stopping_for_update}
        '''
        result = self._values.get("allow_stopping_for_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def attached_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]]:
        '''attached_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#attached_disk ComputeInstance#attached_disk}
        '''
        result = self._values.get("attached_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]], result)

    @builtins.property
    def can_ip_forward(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether sending and receiving of packets with non-matching source or destination IPs is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#can_ip_forward ComputeInstance#can_ip_forward}
        '''
        result = self._values.get("can_ip_forward")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def confidential_instance_config(
        self,
    ) -> typing.Optional[ComputeInstanceConfidentialInstanceConfig]:
        '''confidential_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#confidential_instance_config ComputeInstance#confidential_instance_config}
        '''
        result = self._values.get("confidential_instance_config")
        return typing.cast(typing.Optional[ComputeInstanceConfidentialInstanceConfig], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether deletion protection is enabled on this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#deletion_protection ComputeInstance#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#description ComputeInstance#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_status(self) -> typing.Optional[builtins.str]:
        '''Desired status of the instance. Either "RUNNING", "SUSPENDED" or "TERMINATED".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#desired_status ComputeInstance#desired_status}
        '''
        result = self._values.get("desired_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_display(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance has virtual displays enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_display ComputeInstance#enable_display}
        '''
        result = self._values.get("enable_display")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_accelerator(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGuestAccelerator"]]]:
        '''guest_accelerator block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#guest_accelerator ComputeInstance#guest_accelerator}
        '''
        result = self._values.get("guest_accelerator")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceGuestAccelerator"]]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''A custom hostname for the instance.

        Must be a fully qualified DNS name and RFC-1035-valid. Valid format is a series of labels 1-63 characters long matching the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_, concatenated with periods. The entire hostname must not exceed 253 characters. Changing this forces a new resource to be created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#hostname ComputeInstance#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#id ComputeInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_encryption_key(
        self,
    ) -> typing.Optional["ComputeInstanceInstanceEncryptionKey"]:
        '''instance_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_encryption_key ComputeInstance#instance_encryption_key}
        '''
        result = self._values.get("instance_encryption_key")
        return typing.cast(typing.Optional["ComputeInstanceInstanceEncryptionKey"], result)

    @builtins.property
    def key_revocation_action_type(self) -> typing.Optional[builtins.str]:
        '''Action to be taken when a customer's encryption key is revoked.

        Supports "STOP" and "NONE", with "NONE" being the default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key_revocation_action_type ComputeInstance#key_revocation_action_type}
        '''
        result = self._values.get("key_revocation_action_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs assigned to the instance.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#labels ComputeInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata key/value pairs made available within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata ComputeInstance#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata_startup_script(self) -> typing.Optional[builtins.str]:
        '''Metadata startup scripts made available within the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#metadata_startup_script ComputeInstance#metadata_startup_script}
        '''
        result = self._values.get("metadata_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_cpu_platform(self) -> typing.Optional[builtins.str]:
        '''The minimum CPU platform specified for the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_cpu_platform ComputeInstance#min_cpu_platform}
        '''
        result = self._values.get("min_cpu_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_performance_config(
        self,
    ) -> typing.Optional["ComputeInstanceNetworkPerformanceConfig"]:
        '''network_performance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_performance_config ComputeInstance#network_performance_config}
        '''
        result = self._values.get("network_performance_config")
        return typing.cast(typing.Optional["ComputeInstanceNetworkPerformanceConfig"], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeInstanceParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#params ComputeInstance#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeInstanceParams"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If self_link is provided, this value is ignored. If neither self_link nor project are provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#project ComputeInstance#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["ComputeInstanceReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#reservation_affinity ComputeInstance#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["ComputeInstanceReservationAffinity"], result)

    @builtins.property
    def resource_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of self_links of resource policies to attach to the instance.

        Currently a max of 1 resource policy is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_policies ComputeInstance#resource_policies}
        '''
        result = self._values.get("resource_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["ComputeInstanceScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scheduling ComputeInstance#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["ComputeInstanceScheduling"], result)

    @builtins.property
    def scratch_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceScratchDisk"]]]:
        '''scratch_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scratch_disk ComputeInstance#scratch_disk}
        '''
        result = self._values.get("scratch_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceScratchDisk"]]], result)

    @builtins.property
    def service_account(self) -> typing.Optional["ComputeInstanceServiceAccount"]:
        '''service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#service_account ComputeInstance#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional["ComputeInstanceServiceAccount"], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["ComputeInstanceShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#shielded_instance_config ComputeInstance#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["ComputeInstanceShieldedInstanceConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of tags attached to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#tags ComputeInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#timeouts ComputeInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeInstanceTimeouts"], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''The zone of the instance.

        If self_link is provided, this value is ignored. If neither self_link nor zone are provided, the provider zone is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#zone ComputeInstance#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceGuestAccelerator",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "type": "type"},
)
class ComputeInstanceGuestAccelerator:
    def __init__(self, *, count: jsii.Number, type: builtins.str) -> None:
        '''
        :param count: The number of the guest accelerator cards exposed to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#count ComputeInstance#count}
        :param type: The accelerator type resource exposed to this instance. E.g. nvidia-tesla-k80. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f59522513e66eebe5e3db09bad32c21944eb00ba774d0752b52e17cab2e615)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "type": type,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''The number of the guest accelerator cards exposed to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#count ComputeInstance#count}
        '''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The accelerator type resource exposed to this instance. E.g. nvidia-tesla-k80.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceGuestAccelerator(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceGuestAcceleratorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceGuestAcceleratorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__247c49360a9f68c823bc2a734a634ddbabaeef8eceff76707ac0d25e8e9cd0f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceGuestAcceleratorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4abc939da49232e8456836e32cc8bdddbd6e860f6ace91fd08b3e19956c2618)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceGuestAcceleratorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f919d30a474e58a343807e05f0356295633c4c89c167552c0f5b64c23fe04927)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41464d8038b578d00f34acc42e64d2cb3a2d8f4a41f269cb8e2d6edbe2ce2c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c76fd87e07b53eed3c6225dc0bc10ca2c2ba1086aee275e1755f4f665b0910e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGuestAccelerator]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGuestAccelerator]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGuestAccelerator]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ef3726f09d74c425b11130c3c5f31009100fdc0354b1e5d2d344a0e4bdb77c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceGuestAcceleratorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceGuestAcceleratorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcf87aaf44419ae1fa96722b02b0152d23eaa7b8ea6d0f68397eee5ea4de2a87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0889408c475acb4416b4d3dd6e662d8e9b1f763aaf477cad25931e6312374991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03ce4d1f08e0a4fe794a7534f0deb1ddd7a251ed7e3ba05fc3b30b4920c2f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGuestAccelerator]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGuestAccelerator]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGuestAccelerator]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a153cc800fb4b02020f39b3757fb2e1de096eb07024255f5c0a0dcc8417825b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceInstanceEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
    },
)
class ComputeInstanceInstanceEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25aebf5c11cb172bca0891060ba91689876a78195b833c114fdd0a253a98b42c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_self_link ComputeInstance#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#kms_key_service_account ComputeInstance#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceInstanceEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceInstanceEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceInstanceEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6caeefc8eb46e18d9c6c4dfadcf846e3e8f24bde6a5140fa5b3ed676fac8d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__539f1e3bb9a7c225ee9aa2c5fe7cdb210b4083a2ca02e502c32d17520e53ffff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663bd37a2afa2e0c21fc6833411d2e6d53ed89bae4c48c84b53fa68577bfa177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceInstanceEncryptionKey]:
        return typing.cast(typing.Optional[ComputeInstanceInstanceEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceInstanceEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0851e6dc69403d8b7d38b188180e97e71e8c102e5e558c34b27aa649c2fb3ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterface",
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
class ComputeInstanceNetworkInterface:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterfaceAccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterfaceAliasIpRange", typing.Dict[builtins.str, typing.Any]]]]] = None,
        internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
        ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceNetworkInterfaceIpv6AccessConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#access_config ComputeInstance#access_config}
        :param alias_ip_range: alias_ip_range block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#alias_ip_range ComputeInstance#alias_ip_range}
        :param internal_ipv6_prefix_length: The prefix length of the primary internal IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#internal_ipv6_prefix_length ComputeInstance#internal_ipv6_prefix_length}
        :param ipv6_access_config: ipv6_access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ipv6_access_config ComputeInstance#ipv6_access_config}
        :param ipv6_address: An IPv6 internal network address for this network interface. If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ipv6_address ComputeInstance#ipv6_address}
        :param network: The name or self_link of the network attached to this interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network ComputeInstance#network}
        :param network_attachment: The URL of the network attachment that this interface should connect to in the following format: projects/{projectNumber}/regions/{region_name}/networkAttachments/{network_attachment_name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_attachment ComputeInstance#network_attachment}
        :param network_ip: The private IP address assigned to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_ip ComputeInstance#network_ip}
        :param nic_type: The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, IDPF, MRDMA, and IRDMA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nic_type ComputeInstance#nic_type}
        :param queue_count: The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It will be empty if not specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#queue_count ComputeInstance#queue_count}
        :param stack_type: The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#stack_type ComputeInstance#stack_type}
        :param subnetwork: The name or self_link of the subnetwork attached to this interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork ComputeInstance#subnetwork}
        :param subnetwork_project: The project in which the subnetwork belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork_project ComputeInstance#subnetwork_project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46c619ee9726afb3cf6ea4aa1e6dec0518d9caed52ea6feda9d6195d6d37243)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceAccessConfig"]]]:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#access_config ComputeInstance#access_config}
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceAccessConfig"]]], result)

    @builtins.property
    def alias_ip_range(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceAliasIpRange"]]]:
        '''alias_ip_range block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#alias_ip_range ComputeInstance#alias_ip_range}
        '''
        result = self._values.get("alias_ip_range")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceAliasIpRange"]]], result)

    @builtins.property
    def internal_ipv6_prefix_length(self) -> typing.Optional[jsii.Number]:
        '''The prefix length of the primary internal IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#internal_ipv6_prefix_length ComputeInstance#internal_ipv6_prefix_length}
        '''
        result = self._values.get("internal_ipv6_prefix_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ipv6_access_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceIpv6AccessConfig"]]]:
        '''ipv6_access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ipv6_access_config ComputeInstance#ipv6_access_config}
        '''
        result = self._values.get("ipv6_access_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceNetworkInterfaceIpv6AccessConfig"]]], result)

    @builtins.property
    def ipv6_address(self) -> typing.Optional[builtins.str]:
        '''An IPv6 internal network address for this network interface.

        If not specified, Google Cloud will automatically assign an internal IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ipv6_address ComputeInstance#ipv6_address}
        '''
        result = self._values.get("ipv6_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the network attached to this interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network ComputeInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_attachment(self) -> typing.Optional[builtins.str]:
        '''The URL of the network attachment that this interface should connect to in the following format: projects/{projectNumber}/regions/{region_name}/networkAttachments/{network_attachment_name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_attachment ComputeInstance#network_attachment}
        '''
        result = self._values.get("network_attachment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_ip(self) -> typing.Optional[builtins.str]:
        '''The private IP address assigned to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_ip ComputeInstance#network_ip}
        '''
        result = self._values.get("network_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC to be used on this interface. Possible values:GVNIC, VIRTIO_NET, IDPF, MRDMA, and IRDMA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nic_type ComputeInstance#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_count(self) -> typing.Optional[jsii.Number]:
        '''The networking queue count that's specified by users for the network interface.

        Both Rx and Tx queues will be set to this number. It will be empty if not specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#queue_count ComputeInstance#queue_count}
        '''
        result = self._values.get("queue_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_type(self) -> typing.Optional[builtins.str]:
        '''The stack type for this network interface to identify whether the IPv6 feature is enabled or not.

        If not specified, IPV4_ONLY will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#stack_type ComputeInstance#stack_type}
        '''
        result = self._values.get("stack_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The name or self_link of the subnetwork attached to this interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork ComputeInstance#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_project(self) -> typing.Optional[builtins.str]:
        '''The project in which the subnetwork belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork_project ComputeInstance#subnetwork_project}
        '''
        result = self._values.get("subnetwork_project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceNetworkInterface(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "nat_ip": "natIp",
        "network_tier": "networkTier",
        "public_ptr_domain_name": "publicPtrDomainName",
    },
)
class ComputeInstanceNetworkInterfaceAccessConfig:
    def __init__(
        self,
        *,
        nat_ip: typing.Optional[builtins.str] = None,
        network_tier: typing.Optional[builtins.str] = None,
        public_ptr_domain_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param nat_ip: The IP address that is be 1:1 mapped to the instance's network ip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nat_ip ComputeInstance#nat_ip}
        :param network_tier: The networking tier used for configuring this instance. One of PREMIUM or STANDARD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_tier ComputeInstance#network_tier}
        :param public_ptr_domain_name: The DNS domain name for the public PTR record. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#public_ptr_domain_name ComputeInstance#public_ptr_domain_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af5a74f41cd882ec3e43040bc3cf3e4c94eb017f10bd81b7f46b329e59a3ebae)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nat_ip ComputeInstance#nat_ip}
        '''
        result = self._values.get("nat_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tier(self) -> typing.Optional[builtins.str]:
        '''The networking tier used for configuring this instance. One of PREMIUM or STANDARD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_tier ComputeInstance#network_tier}
        '''
        result = self._values.get("network_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ptr_domain_name(self) -> typing.Optional[builtins.str]:
        '''The DNS domain name for the public PTR record.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#public_ptr_domain_name ComputeInstance#public_ptr_domain_name}
        '''
        result = self._values.get("public_ptr_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceNetworkInterfaceAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceNetworkInterfaceAccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddd0d8f816e40596710c0328b5de5fa191cd673c15759e2debe47029d9f0aed3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceNetworkInterfaceAccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28edcee7721fb70f76192c823ffbc04b7df86031c30c9cc758f302d9188c071)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceNetworkInterfaceAccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7e30d0d47bdf545ec38a4f90ff090de9d6f8c44ebc939198e664ac0345738f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__235b4754e24ac7643ab4480b85eb5fffed7d9f0dd53b6c5ad2c896773a545ff9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c61a00bf8077e1d67c1a37d4c0f9272ea7819aa5921d2a8ec2112813a6d94c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d40612b5f6554cd1e1e5fdcfc1f75c3eb69c14ac778819b5deb5ecff2fd5e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceNetworkInterfaceAccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87dfe98a7f3e1212bc32878ab14a18efb5019d6e4f1e8b3e4d31fbba82b30b10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6941fb9ff0497fa8dba32b92eeb1e414a5e98d39f5976fc939690ae21afbb50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37083e62a23a56b5afc962962169fd6d6e5dd06245f0c0d8237fa14c751378ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @public_ptr_domain_name.setter
    def public_ptr_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3b785057c6b4b52956963aaccf07afd6c36597f36dfdc3bcf63c1159d66b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicPtrDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0608716d1a7065f5b5a35f6e8edb9d4937afbdbb9374a0aea8c48f7368986ea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAliasIpRange",
    jsii_struct_bases=[],
    name_mapping={
        "ip_cidr_range": "ipCidrRange",
        "subnetwork_range_name": "subnetworkRangeName",
    },
)
class ComputeInstanceNetworkInterfaceAliasIpRange:
    def __init__(
        self,
        *,
        ip_cidr_range: builtins.str,
        subnetwork_range_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ip_cidr_range: The IP CIDR range represented by this alias IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ip_cidr_range ComputeInstance#ip_cidr_range}
        :param subnetwork_range_name: The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork_range_name ComputeInstance#subnetwork_range_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e339b7cf5a7f16cc9875edfb1f8c943997c95394317ce701775ad17d044369)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#ip_cidr_range ComputeInstance#ip_cidr_range}
        '''
        result = self._values.get("ip_cidr_range")
        assert result is not None, "Required property 'ip_cidr_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnetwork_range_name(self) -> typing.Optional[builtins.str]:
        '''The subnetwork secondary range name specifying the secondary range from which to allocate the IP CIDR range for this alias IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#subnetwork_range_name ComputeInstance#subnetwork_range_name}
        '''
        result = self._values.get("subnetwork_range_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceNetworkInterfaceAliasIpRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceNetworkInterfaceAliasIpRangeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAliasIpRangeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__359cd35dbd403af81dbc7bd275994049f6bccd45c368ddf759aa9d0d2771371a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceNetworkInterfaceAliasIpRangeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c82a31b988b726f39ec0914056e9ccee3d362b3eac55a6156593ce58c711bc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceNetworkInterfaceAliasIpRangeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288deb32f3bc8271186fa112dcc44418d1e92e584dfea9358aa2e2fc4eb5ffe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c920f1571107c3f2ff035e1df753cd572f7c4c17c14c76f435f0ac8be6cf90f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__535ca034fc8f64f4baef74df7f9f57d078dd0f30410c6ce7af6430879b162e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353ebc5a84c1a6db572a470f2edf0861627f93f19f8acc8404e6d14eed5de833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceNetworkInterfaceAliasIpRangeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceAliasIpRangeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7f3490600984ff3792773a0aec12fffa6266b37a47120a064b65c9afe107064)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bd4cd25389ccd4409278120e4fe5a5cb076f03da70c4ebc11bf72fecf56299a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipCidrRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkRangeName")
    def subnetwork_range_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkRangeName"))

    @subnetwork_range_name.setter
    def subnetwork_range_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e27b8e68171976a3aaf069c35d8a1e1371e5b6a4e0f719c1bc9924fb4a8574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkRangeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAliasIpRange]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAliasIpRange]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAliasIpRange]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd246fa380faf31c39f06daf5875669dbbf3301f2e17657ee2c2d2bdec40986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceIpv6AccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "network_tier": "networkTier",
        "external_ipv6": "externalIpv6",
        "external_ipv6_prefix_length": "externalIpv6PrefixLength",
        "name": "name",
        "public_ptr_domain_name": "publicPtrDomainName",
    },
)
class ComputeInstanceNetworkInterfaceIpv6AccessConfig:
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
        :param network_tier: The service-level to be provided for IPv6 traffic when the subnet has an external subnet. Only PREMIUM tier is valid for IPv6 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_tier ComputeInstance#network_tier}
        :param external_ipv6: The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. To use a static external IP address, it must be unused and in the same region as the instance's zone. If not specified, Google Cloud will automatically assign an external IPv6 address from the instance's subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#external_ipv6 ComputeInstance#external_ipv6}
        :param external_ipv6_prefix_length: The prefix length of the external IPv6 range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#external_ipv6_prefix_length ComputeInstance#external_ipv6_prefix_length}
        :param name: The name of this access configuration. In ipv6AccessConfigs, the recommended name is External IPv6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#name ComputeInstance#name}
        :param public_ptr_domain_name: The domain name to be used when creating DNSv6 records for the external IPv6 ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#public_ptr_domain_name ComputeInstance#public_ptr_domain_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4891a0cc8ae15a81b18b2feaf13e08184e683605f10ba54b6306549c9c529329)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#network_tier ComputeInstance#network_tier}
        '''
        result = self._values.get("network_tier")
        assert result is not None, "Required property 'network_tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_ipv6(self) -> typing.Optional[builtins.str]:
        '''The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig.

        To use a static external IP address, it must be unused and in the same region as the instance's zone. If not specified, Google Cloud will automatically assign an external IPv6 address from the instance's subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#external_ipv6 ComputeInstance#external_ipv6}
        '''
        result = self._values.get("external_ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ipv6_prefix_length(self) -> typing.Optional[builtins.str]:
        '''The prefix length of the external IPv6 range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#external_ipv6_prefix_length ComputeInstance#external_ipv6_prefix_length}
        '''
        result = self._values.get("external_ipv6_prefix_length")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access configuration. In ipv6AccessConfigs, the recommended name is External IPv6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#name ComputeInstance#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ptr_domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name to be used when creating DNSv6 records for the external IPv6 ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#public_ptr_domain_name ComputeInstance#public_ptr_domain_name}
        '''
        result = self._values.get("public_ptr_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceNetworkInterfaceIpv6AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceNetworkInterfaceIpv6AccessConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceIpv6AccessConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d854ae0766530fbef642765f82edd1a5aff60f7b05db0af438dc85ede6aa191e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceNetworkInterfaceIpv6AccessConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369e62c9752defaebca0c380f8cef69421feb4312a23f44cfa81b82f1cdf8d91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceNetworkInterfaceIpv6AccessConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d3f145f16afb4624c0d454ce41b498463be2a9988826bc4ad6df8d206ea5b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa3b52f289954ec0fba0b89a887240cf5680868fb0c30ec4f6b894171e632ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b9001f136462314762f22205f0a7723dd3dddd04e9791e73bd0e0e461eb5a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1c0230f74930d28cc850a30d647cb3e6aa3d4c408272b8163f6e9a468e3626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceNetworkInterfaceIpv6AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceIpv6AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d69a3a833e55f151cdc47e08172c078242005f460cc60bc606dce58b56ba9b67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6d0a8f16708a70cc99f82ed24fb580d4732dac0f8fc8e2aab85fbcd75884a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalIpv6PrefixLength")
    def external_ipv6_prefix_length(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalIpv6PrefixLength"))

    @external_ipv6_prefix_length.setter
    def external_ipv6_prefix_length(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e425582f1f9d8fef9bc9b46b25edd3d602be00b8302b3ca352f2f868c67e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa230005ef601c467fc1f0b26619069303600ce96025457f1f3b527f67e9f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTier")
    def network_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkTier"))

    @network_tier.setter
    def network_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c78d0e9e8c552353f42f1f278d0102d6b32467b7ed3687616e60573876a5fbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicPtrDomainName")
    def public_ptr_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicPtrDomainName"))

    @public_ptr_domain_name.setter
    def public_ptr_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6f8d75885311bc3e97568e5112ddd3be53a5ff67de40fd3ab8828e0bc477b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicPtrDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceIpv6AccessConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceIpv6AccessConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceIpv6AccessConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__531eeb9bb173658d509cfc40ee97e645a6479e43443f75c8c8af369858a1781a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceNetworkInterfaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69f1557ec27aaba96b4c949986f21cab807c87d980c6247dcd4b7f50b854c97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceNetworkInterfaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775b077c37a2d474010748ac8a60fff2592b537bc41604b7ccdbdb48d0a423a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceNetworkInterfaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a89f888dbd01cc5a685294c4a1584dbdcb660d3e2407dae77f565402d95f048)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63cc524f1ad9b6d2ddff1a6e68b986ddfd6f792e74d2110edf4bdccd7de0a4e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c4995e40193819e6ef9fb481e93c2897fae8800b9b37a7bd9eeef8472f241c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterface]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterface]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterface]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dd350a388ca64a5c560a924cdf834a57b3557c2d3bf01de3d8082bb483c392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceNetworkInterfaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkInterfaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2064f81792dc7618467bc763b479fa8a189fccaef5cf570664330a369ed5fd37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760d48204628f5d6b17e7451b8a8b326e6fd925980cb2a7c435df6b89163bbb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="putAliasIpRange")
    def put_alias_ip_range(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b60605bc414e16a33c7c94b2844b403d906a39be99a4d33a855282f931269a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAliasIpRange", [value]))

    @jsii.member(jsii_name="putIpv6AccessConfig")
    def put_ipv6_access_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce85dd34ccd811e5586ffd7502b766de3bed09df5c81abe4b60223f7d36b3bde)
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
    def access_config(self) -> ComputeInstanceNetworkInterfaceAccessConfigList:
        return typing.cast(ComputeInstanceNetworkInterfaceAccessConfigList, jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRange")
    def alias_ip_range(self) -> ComputeInstanceNetworkInterfaceAliasIpRangeList:
        return typing.cast(ComputeInstanceNetworkInterfaceAliasIpRangeList, jsii.get(self, "aliasIpRange"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfig")
    def ipv6_access_config(self) -> ComputeInstanceNetworkInterfaceIpv6AccessConfigList:
        return typing.cast(ComputeInstanceNetworkInterfaceIpv6AccessConfigList, jsii.get(self, "ipv6AccessConfig"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasIpRangeInput")
    def alias_ip_range_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]], jsii.get(self, "aliasIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalIpv6PrefixLengthInput")
    def internal_ipv6_prefix_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalIpv6PrefixLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6AccessConfigInput")
    def ipv6_access_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]], jsii.get(self, "ipv6AccessConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f29b8420a5c3e2e69880c4d08712ad2d44e4d117884d83c81c3dfe019dc3d684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalIpv6PrefixLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipv6Address")
    def ipv6_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Address"))

    @ipv6_address.setter
    def ipv6_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad20a07c1c79e9f4c343fc44d83a2dd4b15ddc0bb23149ff0cf4daf91ca633f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d74fa93a0ba6069935d83bff8c966305401c52e8fa2710e543e9776dab93c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdff6c0f02549af0fb2f753ac2c173b2250bcfbfdf4eb4ee92b37ac126667674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkIp")
    def network_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkIp"))

    @network_ip.setter
    def network_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af07f8220a060a05574c893c837aefe9dff19fd8615b85b66b85ce41831732f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58214ba873e2ea1d358255241058e4d644053f05880e386f4d0487cee413e1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueCount")
    def queue_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queueCount"))

    @queue_count.setter
    def queue_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0504996b75a7c4e43c150a658c504b68c16dd7cb494be97f27242a516ca9c2a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stackType")
    def stack_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackType"))

    @stack_type.setter
    def stack_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94191757a511d552085a61e0513fc84f03deeea6539f6de9f9023186c6b07231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b16845ccd7fd58eb0806ad1689719cd78a5b120396cded4be79043bef9f4d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkProject")
    def subnetwork_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkProject"))

    @subnetwork_project.setter
    def subnetwork_project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ac4154c2b5df045e6a9db7d76a4c375805ba02c078c26491435380cdbd231f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkProject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterface]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterface]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterface]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16651765d943e435dc817c993c60297180201d0f2ac8bf7c3b1f08f9bafb83d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkPerformanceConfig",
    jsii_struct_bases=[],
    name_mapping={"total_egress_bandwidth_tier": "totalEgressBandwidthTier"},
)
class ComputeInstanceNetworkPerformanceConfig:
    def __init__(self, *, total_egress_bandwidth_tier: builtins.str) -> None:
        '''
        :param total_egress_bandwidth_tier: The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#total_egress_bandwidth_tier ComputeInstance#total_egress_bandwidth_tier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07d90409299aa4763de1508aed0efbf930280ffe749579f0e53dafc412e52d6)
            check_type(argname="argument total_egress_bandwidth_tier", value=total_egress_bandwidth_tier, expected_type=type_hints["total_egress_bandwidth_tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total_egress_bandwidth_tier": total_egress_bandwidth_tier,
        }

    @builtins.property
    def total_egress_bandwidth_tier(self) -> builtins.str:
        '''The egress bandwidth tier to enable. Possible values:TIER_1, DEFAULT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#total_egress_bandwidth_tier ComputeInstance#total_egress_bandwidth_tier}
        '''
        result = self._values.get("total_egress_bandwidth_tier")
        assert result is not None, "Required property 'total_egress_bandwidth_tier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceNetworkPerformanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceNetworkPerformanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceNetworkPerformanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__207ecca916c7d10d36ced70afd3e78fd2c7cc173e3c2bbd1449065916f0f6089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb016d4f253f3f5f8800bc239de823b779ce5ad3cff085d05ad2911e46c6c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "totalEgressBandwidthTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceNetworkPerformanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceNetworkPerformanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceNetworkPerformanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12dbf216e25f455ed4e4669dedcf274745f60244e8a938ae89b1d35942a859c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeInstanceParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: A map of resource manager tags. Resource manager tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. The field is ignored (both PUT & PATCH) when empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f16cf8c4a06f819fd3970bb06e665d5b77367370bba6b09c9ed7236844685b4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#resource_manager_tags ComputeInstance#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5fbd72040c516b37817cf5379cfc7a46b9762dbd36a8d8c894184017d1b51e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c834d6999f019395ef6e5452a718bb1f5801440412f00c445441f29503f3bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceParams]:
        return typing.cast(typing.Optional[ComputeInstanceParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeInstanceParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7411aabac1d7f2cd56a2e68b05bb0db79976d2868eb5f7abec18a834b12d3223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "specific_reservation": "specificReservation"},
)
class ComputeInstanceReservationAffinity:
    def __init__(
        self,
        *,
        type: builtins.str,
        specific_reservation: typing.Optional[typing.Union["ComputeInstanceReservationAffinitySpecificReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param type: The type of reservation from which this instance can consume resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        :param specific_reservation: specific_reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#specific_reservation ComputeInstance#specific_reservation}
        '''
        if isinstance(specific_reservation, dict):
            specific_reservation = ComputeInstanceReservationAffinitySpecificReservation(**specific_reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05704e6b49d52429abb9d6b53d99a83669ae75be9249ce530238b19962a9caa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#type ComputeInstance#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def specific_reservation(
        self,
    ) -> typing.Optional["ComputeInstanceReservationAffinitySpecificReservation"]:
        '''specific_reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#specific_reservation ComputeInstance#specific_reservation}
        '''
        result = self._values.get("specific_reservation")
        return typing.cast(typing.Optional["ComputeInstanceReservationAffinitySpecificReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69899e0b0c0bf21eb35cb0a64ad4964199da2507f73c0a2fcebfa64c0574a907)
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
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key ComputeInstance#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#values ComputeInstance#values}
        '''
        value = ComputeInstanceReservationAffinitySpecificReservation(
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
    ) -> "ComputeInstanceReservationAffinitySpecificReservationOutputReference":
        return typing.cast("ComputeInstanceReservationAffinitySpecificReservationOutputReference", jsii.get(self, "specificReservation"))

    @builtins.property
    @jsii.member(jsii_name="specificReservationInput")
    def specific_reservation_input(
        self,
    ) -> typing.Optional["ComputeInstanceReservationAffinitySpecificReservation"]:
        return typing.cast(typing.Optional["ComputeInstanceReservationAffinitySpecificReservation"], jsii.get(self, "specificReservationInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__96cd73b603fe4601575e252998c3783374c951f7b6a6b4873281b9b32d407ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceReservationAffinity]:
        return typing.cast(typing.Optional[ComputeInstanceReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c081aa02ac131e65bb2a499293eebe11816fcfc97afff4ed3b0d79a262c7ac79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceReservationAffinitySpecificReservation",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class ComputeInstanceReservationAffinitySpecificReservation:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Corresponds to the label key of a reservation resource. To target a SPECIFIC_RESERVATION by name, specify compute.googleapis.com/reservation-name as the key and specify the name of your reservation as the only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key ComputeInstance#key}
        :param values: Corresponds to the label values of a reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#values ComputeInstance#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b7d1a5c53bed5aaf0a08b9d3b70d9779b82e0c14c8a2be0a11f33ca60b0e0a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key ComputeInstance#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Corresponds to the label values of a reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#values ComputeInstance#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceReservationAffinitySpecificReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceReservationAffinitySpecificReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceReservationAffinitySpecificReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d568d950cb2e647276cd9769bcb2baecdc4a9507f282f8a4cf13bf224d85393)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63b1f3ea632a52a6f5a6256008c7c4dae45b560b86353012a9edcd7c7ccc3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07919f29adba8ffb4f5759e6f4c0e74c9946026a7c1fe7923ac5d1bedf80ad38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceReservationAffinitySpecificReservation]:
        return typing.cast(typing.Optional[ComputeInstanceReservationAffinitySpecificReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceReservationAffinitySpecificReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab5a563a66b58337ebe7db037382f08fa85d915b5470bb296988de103e982a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceScheduling",
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
class ComputeInstanceScheduling:
    def __init__(
        self,
        *,
        automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        availability_domain: typing.Optional[jsii.Number] = None,
        instance_termination_action: typing.Optional[builtins.str] = None,
        local_ssd_recovery_timeout: typing.Optional[typing.Union["ComputeInstanceSchedulingLocalSsdRecoveryTimeout", typing.Dict[builtins.str, typing.Any]]] = None,
        max_run_duration: typing.Optional[typing.Union["ComputeInstanceSchedulingMaxRunDuration", typing.Dict[builtins.str, typing.Any]]] = None,
        min_node_cpus: typing.Optional[jsii.Number] = None,
        node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeInstanceSchedulingNodeAffinities", typing.Dict[builtins.str, typing.Any]]]]] = None,
        on_host_maintenance: typing.Optional[builtins.str] = None,
        on_instance_stop_action: typing.Optional[typing.Union["ComputeInstanceSchedulingOnInstanceStopAction", typing.Dict[builtins.str, typing.Any]]] = None,
        preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        provisioning_model: typing.Optional[builtins.str] = None,
        termination_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automatic_restart: Specifies if the instance should be restarted if it was terminated by Compute Engine (not a user). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#automatic_restart ComputeInstance#automatic_restart}
        :param availability_domain: Specifies the availability domain, which this instance should be scheduled on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#availability_domain ComputeInstance#availability_domain}
        :param instance_termination_action: Specifies the action GCE should take when SPOT VM is preempted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_termination_action ComputeInstance#instance_termination_action}
        :param local_ssd_recovery_timeout: local_ssd_recovery_timeout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#local_ssd_recovery_timeout ComputeInstance#local_ssd_recovery_timeout}
        :param max_run_duration: max_run_duration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#max_run_duration ComputeInstance#max_run_duration}
        :param min_node_cpus: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_node_cpus ComputeInstance#min_node_cpus}.
        :param node_affinities: node_affinities block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#node_affinities ComputeInstance#node_affinities}
        :param on_host_maintenance: Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_host_maintenance ComputeInstance#on_host_maintenance}
        :param on_instance_stop_action: on_instance_stop_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_instance_stop_action ComputeInstance#on_instance_stop_action}
        :param preemptible: Whether the instance is preemptible. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#preemptible ComputeInstance#preemptible}
        :param provisioning_model: Whether the instance is spot. If this is set as SPOT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioning_model ComputeInstance#provisioning_model}
        :param termination_time: Specifies the timestamp, when the instance will be terminated, in RFC3339 text format. If specified, the instance termination action will be performed at the termination time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#termination_time ComputeInstance#termination_time}
        '''
        if isinstance(local_ssd_recovery_timeout, dict):
            local_ssd_recovery_timeout = ComputeInstanceSchedulingLocalSsdRecoveryTimeout(**local_ssd_recovery_timeout)
        if isinstance(max_run_duration, dict):
            max_run_duration = ComputeInstanceSchedulingMaxRunDuration(**max_run_duration)
        if isinstance(on_instance_stop_action, dict):
            on_instance_stop_action = ComputeInstanceSchedulingOnInstanceStopAction(**on_instance_stop_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072ecb19ad75aca724c504d0ae33c7e71b61d3decb5b8f27793223716c859410)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#automatic_restart ComputeInstance#automatic_restart}
        '''
        result = self._values.get("automatic_restart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def availability_domain(self) -> typing.Optional[jsii.Number]:
        '''Specifies the availability domain, which this instance should be scheduled on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#availability_domain ComputeInstance#availability_domain}
        '''
        result = self._values.get("availability_domain")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_termination_action(self) -> typing.Optional[builtins.str]:
        '''Specifies the action GCE should take when SPOT VM is preempted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#instance_termination_action ComputeInstance#instance_termination_action}
        '''
        result = self._values.get("instance_termination_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_ssd_recovery_timeout(
        self,
    ) -> typing.Optional["ComputeInstanceSchedulingLocalSsdRecoveryTimeout"]:
        '''local_ssd_recovery_timeout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#local_ssd_recovery_timeout ComputeInstance#local_ssd_recovery_timeout}
        '''
        result = self._values.get("local_ssd_recovery_timeout")
        return typing.cast(typing.Optional["ComputeInstanceSchedulingLocalSsdRecoveryTimeout"], result)

    @builtins.property
    def max_run_duration(
        self,
    ) -> typing.Optional["ComputeInstanceSchedulingMaxRunDuration"]:
        '''max_run_duration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#max_run_duration ComputeInstance#max_run_duration}
        '''
        result = self._values.get("max_run_duration")
        return typing.cast(typing.Optional["ComputeInstanceSchedulingMaxRunDuration"], result)

    @builtins.property
    def min_node_cpus(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#min_node_cpus ComputeInstance#min_node_cpus}.'''
        result = self._values.get("min_node_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_affinities(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceSchedulingNodeAffinities"]]]:
        '''node_affinities block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#node_affinities ComputeInstance#node_affinities}
        '''
        result = self._values.get("node_affinities")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeInstanceSchedulingNodeAffinities"]]], result)

    @builtins.property
    def on_host_maintenance(self) -> typing.Optional[builtins.str]:
        '''Describes maintenance behavior for the instance. One of MIGRATE or TERMINATE,.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_host_maintenance ComputeInstance#on_host_maintenance}
        '''
        result = self._values.get("on_host_maintenance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_instance_stop_action(
        self,
    ) -> typing.Optional["ComputeInstanceSchedulingOnInstanceStopAction"]:
        '''on_instance_stop_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#on_instance_stop_action ComputeInstance#on_instance_stop_action}
        '''
        result = self._values.get("on_instance_stop_action")
        return typing.cast(typing.Optional["ComputeInstanceSchedulingOnInstanceStopAction"], result)

    @builtins.property
    def preemptible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance is preemptible.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#preemptible ComputeInstance#preemptible}
        '''
        result = self._values.get("preemptible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def provisioning_model(self) -> typing.Optional[builtins.str]:
        '''Whether the instance is spot. If this is set as SPOT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#provisioning_model ComputeInstance#provisioning_model}
        '''
        result = self._values.get("provisioning_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_time(self) -> typing.Optional[builtins.str]:
        '''Specifies the timestamp, when the instance will be terminated, in RFC3339 text format.

        If specified, the instance termination action
        will be performed at the termination time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#termination_time ComputeInstance#termination_time}
        '''
        result = self._values.get("termination_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingLocalSsdRecoveryTimeout",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceSchedulingLocalSsdRecoveryTimeout:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4399ca954db5594624c615abae7958492641cba94276f59a10474f8244c9cc75)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceSchedulingLocalSsdRecoveryTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceSchedulingLocalSsdRecoveryTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingLocalSsdRecoveryTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac106351b790c739cdf5c2a2f96a43f914ff0ee67426f3efec87408fc9d5ce8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5225438710cb704b1193e4fdcff3c2af0a6470f288b92fdd451b3dbb8f19335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8336861dba02af7698979808b828a54e846da6305a0acd84bb8b7cd8ed412298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91170ce7e79d6c02d1247b1d5706c0820f548c23f28f901e686144ea31ecc15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingMaxRunDuration",
    jsii_struct_bases=[],
    name_mapping={"seconds": "seconds", "nanos": "nanos"},
)
class ComputeInstanceSchedulingMaxRunDuration:
    def __init__(
        self,
        *,
        seconds: jsii.Number,
        nanos: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63447458be67be8dc5010dba2c13183fff2546ced7ecf30a0478e4537a2054b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceSchedulingMaxRunDuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceSchedulingMaxRunDurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingMaxRunDurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9bf8d51821131896fa080183045e5023f2c58546f1d79899a59b61048294790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5017aac4b79e94b96f8ab2ba08dda685f49a1e0637b331d9fdf90590d3b73437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e4e4b343e5b0823555c18d6ccae91d5dfae07bc319a49d4267a56baf0de425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingMaxRunDuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceSchedulingMaxRunDuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0571df086c5aa3bd2c728b8d2d2bd6788269a8ecab4064b9486789e10ac00c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingNodeAffinities",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "operator": "operator", "values": "values"},
)
class ComputeInstanceSchedulingNodeAffinities:
    def __init__(
        self,
        *,
        key: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key ComputeInstance#key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#operator ComputeInstance#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#values ComputeInstance#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c36cf12b647b6f9cae5fa365ed3ec5cbbaf1318928d4e6baff69f04851d22c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#key ComputeInstance#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#operator ComputeInstance#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#values ComputeInstance#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceSchedulingNodeAffinities(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceSchedulingNodeAffinitiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingNodeAffinitiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e92e6f7deb03ea7ec17f31f2e082dd41c7696a5246f613f0f0a504e49849e104)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeInstanceSchedulingNodeAffinitiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5456ac367c258d766a886469b53b5b1e8de8ecfa9745a59001d43be52317f0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceSchedulingNodeAffinitiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a488e1cf4f7ae2607e6dc6090f2f9aeae14abb713a7dd8e849767c51622669d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84fa21cf720467dc75841f03ff9956a4a0bb26067688558030f1b51808426996)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44df5ef72d814853debd40c93f3e7ddadb7634513bea093fa58557322b0aa84f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670a18302172823a986c024fd81f68bd84e06d14ab66bf68668ffb82444c9c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceSchedulingNodeAffinitiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingNodeAffinitiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2940cd39e02564e11419d05bd0b1cc710116776d0508c14b175389114572966d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ead5d531c169bd411941ecdcea6a58378b8c140a83363536e14057f0a5d1fad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d704d2e7674952cb9d3ae5972599fd499d1b3452ec3cc1499faaa9046e0e139a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2923e0255fa6ab388dce508971d0b575fc5e0a9635b4220dd3f7d7be717d2ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceSchedulingNodeAffinities]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceSchedulingNodeAffinities]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceSchedulingNodeAffinities]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d87a0f008b17e58e40cc171e594ccb5e1e4395337ccd3d31b52f89619599ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingOnInstanceStopAction",
    jsii_struct_bases=[],
    name_mapping={"discard_local_ssd": "discardLocalSsd"},
)
class ComputeInstanceSchedulingOnInstanceStopAction:
    def __init__(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#discard_local_ssd ComputeInstance#discard_local_ssd}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db58d7f982ee370edfdd5525ce1dc0729d236995c044b37c31240199f5d2bb2e)
            check_type(argname="argument discard_local_ssd", value=discard_local_ssd, expected_type=type_hints["discard_local_ssd"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discard_local_ssd is not None:
            self._values["discard_local_ssd"] = discard_local_ssd

    @builtins.property
    def discard_local_ssd(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the contents of any attached Local SSD disks will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#discard_local_ssd ComputeInstance#discard_local_ssd}
        '''
        result = self._values.get("discard_local_ssd")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceSchedulingOnInstanceStopAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceSchedulingOnInstanceStopActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingOnInstanceStopActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e846a24371df771856ed3ea6f75d501422dd7898f7db0d9da86cd1d5d154bd02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe467caae63c3fda48e3a45c37a65e9c3419127013fb6ecf4fcae231f5833aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discardLocalSsd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce12ab29a5b8e6e138dd73dd3c3a62ef746c4d04fb0c880e153efd97775a2137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67cee1494abc3aa217547b29eb8c8475499bdd06d30d8eed3c3452e574d47dd9)
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        value = ComputeInstanceSchedulingLocalSsdRecoveryTimeout(
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
        :param seconds: Span of time at a resolution of a second. Must be from 0 to 315,576,000,000 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#seconds ComputeInstance#seconds}
        :param nanos: Span of time that's a fraction of a second at nanosecond resolution. Durations less than one second are represented with a 0 seconds field and a positive nanos field. Must be from 0 to 999,999,999 inclusive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#nanos ComputeInstance#nanos}
        '''
        value = ComputeInstanceSchedulingMaxRunDuration(seconds=seconds, nanos=nanos)

        return typing.cast(None, jsii.invoke(self, "putMaxRunDuration", [value]))

    @jsii.member(jsii_name="putNodeAffinities")
    def put_node_affinities(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a537e3580e567d29d534f41540238360e063d86506a06fa1adef6ab6b4e72c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeAffinities", [value]))

    @jsii.member(jsii_name="putOnInstanceStopAction")
    def put_on_instance_stop_action(
        self,
        *,
        discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param discard_local_ssd: If true, the contents of any attached Local SSD disks will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#discard_local_ssd ComputeInstance#discard_local_ssd}
        '''
        value = ComputeInstanceSchedulingOnInstanceStopAction(
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
    ) -> ComputeInstanceSchedulingLocalSsdRecoveryTimeoutOutputReference:
        return typing.cast(ComputeInstanceSchedulingLocalSsdRecoveryTimeoutOutputReference, jsii.get(self, "localSsdRecoveryTimeout"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDuration")
    def max_run_duration(
        self,
    ) -> ComputeInstanceSchedulingMaxRunDurationOutputReference:
        return typing.cast(ComputeInstanceSchedulingMaxRunDurationOutputReference, jsii.get(self, "maxRunDuration"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinities")
    def node_affinities(self) -> ComputeInstanceSchedulingNodeAffinitiesList:
        return typing.cast(ComputeInstanceSchedulingNodeAffinitiesList, jsii.get(self, "nodeAffinities"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopAction")
    def on_instance_stop_action(
        self,
    ) -> ComputeInstanceSchedulingOnInstanceStopActionOutputReference:
        return typing.cast(ComputeInstanceSchedulingOnInstanceStopActionOutputReference, jsii.get(self, "onInstanceStopAction"))

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
    ) -> typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout], jsii.get(self, "localSsdRecoveryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRunDurationInput")
    def max_run_duration_input(
        self,
    ) -> typing.Optional[ComputeInstanceSchedulingMaxRunDuration]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingMaxRunDuration], jsii.get(self, "maxRunDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minNodeCpusInput")
    def min_node_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNodeCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAffinitiesInput")
    def node_affinities_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]], jsii.get(self, "nodeAffinitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenanceInput")
    def on_host_maintenance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onHostMaintenanceInput"))

    @builtins.property
    @jsii.member(jsii_name="onInstanceStopActionInput")
    def on_instance_stop_action_input(
        self,
    ) -> typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction]:
        return typing.cast(typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction], jsii.get(self, "onInstanceStopActionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2abd2e4eb731341073b67b40cc948ce1b3c57353e470fe94d8317fda2df29d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticRestart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityDomain")
    def availability_domain(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availabilityDomain"))

    @availability_domain.setter
    def availability_domain(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b021173669ec965f3d07f18addb0084624e69d352a8b7163d58bde96093c909e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceTerminationAction")
    def instance_termination_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceTerminationAction"))

    @instance_termination_action.setter
    def instance_termination_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d630f7c9597372581bffed47fef5c2f6cbe20b0fd729237dabafbbf6cb90cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceTerminationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNodeCpus")
    def min_node_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNodeCpus"))

    @min_node_cpus.setter
    def min_node_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799733ab73987c94fbf2501b8eef3d9c55e23359752f59340c8766f918f00595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNodeCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onHostMaintenance")
    def on_host_maintenance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onHostMaintenance"))

    @on_host_maintenance.setter
    def on_host_maintenance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d57a47b01b87739dab8bef2254053cc22ae25f5e83cb1db81ce3e78842a1115)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a148a8d068277bd09f35ab99d66412ece414f5f7e9ff9aa00be217a464203712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisioningModel")
    def provisioning_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provisioningModel"))

    @provisioning_model.setter
    def provisioning_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ac80aba37dfb2a7cfb43a3eec1d3b5e61ab288eab5b888fab8948d22b1a5f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisioningModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminationTime")
    def termination_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terminationTime"))

    @termination_time.setter
    def termination_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90f883f1f2139a3d829d29928725e68424b6c35dc8a606ae7778e85542a7458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceScheduling]:
        return typing.cast(typing.Optional[ComputeInstanceScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeInstanceScheduling]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91daeb4cdf086725ca062ca983de7709939dfb7c3b623d21e27304d0bc4ded12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceScratchDisk",
    jsii_struct_bases=[],
    name_mapping={
        "interface": "interface",
        "device_name": "deviceName",
        "size": "size",
    },
)
class ComputeInstanceScratchDisk:
    def __init__(
        self,
        *,
        interface: builtins.str,
        device_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param interface: The disk interface used for attaching this disk. One of SCSI or NVME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#interface ComputeInstance#interface}
        :param device_name: Name with which the attached disk is accessible under /dev/disk/by-id/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        :param size: The size of the disk in gigabytes. One of 375 or 3000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#size ComputeInstance#size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1779424e4b080267967c867b43cf73426056fb47afb43fb4f96f3723a931c47d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#interface ComputeInstance#interface}
        '''
        result = self._values.get("interface")
        assert result is not None, "Required property 'interface' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''Name with which the attached disk is accessible under /dev/disk/by-id/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#device_name ComputeInstance#device_name}
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the disk in gigabytes. One of 375 or 3000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#size ComputeInstance#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceScratchDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceScratchDiskList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceScratchDiskList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eacd9ffd13adf6bb3574ffe8739da666c89e226c13d4fdbda67192430c24c4cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeInstanceScratchDiskOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f92d64ebb5dd335f3ca757de41a61d6bce50c4ec60ed2dba8aa26bc0e67ae2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeInstanceScratchDiskOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04e035e737f209249a3cb1b8a007797c3a34df761c3a297108d04c0e13baebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b41b464cbf847df86753b432031c10eac943c4122fd939ef92d00a46b0cf6c0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fce846a387ac1ecd3886e2470b52b127415e0e3f9fa08711d28d140ad6ef3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceScratchDisk]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceScratchDisk]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceScratchDisk]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9805989221e3589866dc8d185c22eda3008e7551c7e0703fffde94aa3e7fbdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeInstanceScratchDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceScratchDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c9bcb1ea1c2d14c1b9575c4e7332174018ba3249e9ca2a232e0daeb06da6c44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__490e55034113e9310407474e1f461218dee6490bfc673b2e21718d37410eb845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aeb5b57c0904f3d9df94b2ef516712ff7e2ecc530adf22b8ffd02980d214315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64f38bc4d8bf77f09bd714c33acd82b511bb56883ab098ea0c14a54a63d5c37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceScratchDisk]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceScratchDisk]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceScratchDisk]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267e7c06a4b830eb46e0a8601fe25f6121aeabe5fcdfedfd5255c79792e73dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceServiceAccount",
    jsii_struct_bases=[],
    name_mapping={"scopes": "scopes", "email": "email"},
)
class ComputeInstanceServiceAccount:
    def __init__(
        self,
        *,
        scopes: typing.Sequence[builtins.str],
        email: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scopes: A list of service scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scopes ComputeInstance#scopes}
        :param email: The service account e-mail address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#email ComputeInstance#email}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb64214dc111d98c4183535bf85b7bf478108dc2d4ce481e5bbec174e9850f4f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#scopes ComputeInstance#scopes}
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The service account e-mail address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#email ComputeInstance#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddac717c9c0e474ff7132f337ef71c494f85882bd212af5b26e51d4ad50f1a59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98673066e6bb466def3312f7bc4ecfb174db6cc32201181daa3763887a14f9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d3ace1a487ab1c6488582482896c84ec89ce1aafe09677b64692d36d721521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceServiceAccount]:
        return typing.cast(typing.Optional[ComputeInstanceServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d01ac37d71e3297379d1e328e249cf6a07eb86c4f70cfec1c5946381b7a0c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class ComputeInstanceShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Whether integrity monitoring is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_integrity_monitoring ComputeInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Whether secure boot is enabled for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_secure_boot ComputeInstance#enable_secure_boot}
        :param enable_vtpm: Whether the instance uses vTPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_vtpm ComputeInstance#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07d22eb4cb5ee6aecf46170783fbbdd3b972fa46ec38b667708307e8aa782fe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_integrity_monitoring ComputeInstance#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether secure boot is enabled for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_secure_boot ComputeInstance#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the instance uses vTPM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#enable_vtpm ComputeInstance#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3221773938187172b27106c0c17b9712decf62247436f1e1509d3fb9fe1cb99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db80dc23fb849b7e5eff42ca96a31f92c407815c605e2f755cc9f4f68c16d934)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8f61f2578b7831bf4eb0be4bbb03f18ea70890ee6d45522e0bc4166cec1a7c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ddf796b3a14b1d0e0f6f3d71ef964c3e34e5da7c1e20a70bfb1ddda8a29c7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeInstanceShieldedInstanceConfig]:
        return typing.cast(typing.Optional[ComputeInstanceShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeInstanceShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9a525424930dd4cb1ee33a8fe8d759baaf11ed5f79258d2054ffb40c85d70b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#create ComputeInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#delete ComputeInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#update ComputeInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e223aa44362252401bfff74a2718429a880c337a0b15340c918f03be0bd33e36)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#create ComputeInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#delete ComputeInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_instance#update ComputeInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeInstance.ComputeInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5a3ddcd59722b69d828f36b4dfb04bb3006386ca84218b4d51fb4dacd98fa9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f3ecb517f6301fc0d9d58271e0b032782369bf52889e6a0bc3592579069c07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319856d4d780ec94173d8f8e1573de34c040a129cfd54018e8595e6ffc1ce713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe554ab204907ff643539b40ac1757148e2def3d81410aef58cf2b2e08514839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b626fcda90bac1de9cd769a289de3a883379cb63fa87638c2465a86f19adf01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeInstance",
    "ComputeInstanceAdvancedMachineFeatures",
    "ComputeInstanceAdvancedMachineFeaturesOutputReference",
    "ComputeInstanceAttachedDisk",
    "ComputeInstanceAttachedDiskList",
    "ComputeInstanceAttachedDiskOutputReference",
    "ComputeInstanceBootDisk",
    "ComputeInstanceBootDiskInitializeParams",
    "ComputeInstanceBootDiskInitializeParamsOutputReference",
    "ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey",
    "ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKeyOutputReference",
    "ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey",
    "ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKeyOutputReference",
    "ComputeInstanceBootDiskOutputReference",
    "ComputeInstanceConfidentialInstanceConfig",
    "ComputeInstanceConfidentialInstanceConfigOutputReference",
    "ComputeInstanceConfig",
    "ComputeInstanceGuestAccelerator",
    "ComputeInstanceGuestAcceleratorList",
    "ComputeInstanceGuestAcceleratorOutputReference",
    "ComputeInstanceInstanceEncryptionKey",
    "ComputeInstanceInstanceEncryptionKeyOutputReference",
    "ComputeInstanceNetworkInterface",
    "ComputeInstanceNetworkInterfaceAccessConfig",
    "ComputeInstanceNetworkInterfaceAccessConfigList",
    "ComputeInstanceNetworkInterfaceAccessConfigOutputReference",
    "ComputeInstanceNetworkInterfaceAliasIpRange",
    "ComputeInstanceNetworkInterfaceAliasIpRangeList",
    "ComputeInstanceNetworkInterfaceAliasIpRangeOutputReference",
    "ComputeInstanceNetworkInterfaceIpv6AccessConfig",
    "ComputeInstanceNetworkInterfaceIpv6AccessConfigList",
    "ComputeInstanceNetworkInterfaceIpv6AccessConfigOutputReference",
    "ComputeInstanceNetworkInterfaceList",
    "ComputeInstanceNetworkInterfaceOutputReference",
    "ComputeInstanceNetworkPerformanceConfig",
    "ComputeInstanceNetworkPerformanceConfigOutputReference",
    "ComputeInstanceParams",
    "ComputeInstanceParamsOutputReference",
    "ComputeInstanceReservationAffinity",
    "ComputeInstanceReservationAffinityOutputReference",
    "ComputeInstanceReservationAffinitySpecificReservation",
    "ComputeInstanceReservationAffinitySpecificReservationOutputReference",
    "ComputeInstanceScheduling",
    "ComputeInstanceSchedulingLocalSsdRecoveryTimeout",
    "ComputeInstanceSchedulingLocalSsdRecoveryTimeoutOutputReference",
    "ComputeInstanceSchedulingMaxRunDuration",
    "ComputeInstanceSchedulingMaxRunDurationOutputReference",
    "ComputeInstanceSchedulingNodeAffinities",
    "ComputeInstanceSchedulingNodeAffinitiesList",
    "ComputeInstanceSchedulingNodeAffinitiesOutputReference",
    "ComputeInstanceSchedulingOnInstanceStopAction",
    "ComputeInstanceSchedulingOnInstanceStopActionOutputReference",
    "ComputeInstanceSchedulingOutputReference",
    "ComputeInstanceScratchDisk",
    "ComputeInstanceScratchDiskList",
    "ComputeInstanceScratchDiskOutputReference",
    "ComputeInstanceServiceAccount",
    "ComputeInstanceServiceAccountOutputReference",
    "ComputeInstanceShieldedInstanceConfig",
    "ComputeInstanceShieldedInstanceConfigOutputReference",
    "ComputeInstanceTimeouts",
    "ComputeInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__290f2c91cfbcf5ca7d49837a3242d9ed80e731ae8831b7462d96efc24f7e736b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    boot_disk: typing.Union[ComputeInstanceBootDisk, typing.Dict[builtins.str, typing.Any]],
    machine_type: builtins.str,
    name: builtins.str,
    network_interface: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    desired_status: typing.Optional[builtins.str] = None,
    enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_encryption_key: typing.Optional[typing.Union[ComputeInstanceInstanceEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeInstanceParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceScratchDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d53b2117eafd7532c0776ef4f697c1c68de3cdced86d3aefd043cd32b3b993cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29a149b444426d9ef8fa3ead437f593af63bef723a0212f77c5201d3b70bbed(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceAttachedDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a759f3f27da877335bb6a65cd704f5a65a77c45b945f2833e3c1349e0309b82b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e627681ae7c4eeff9ba8317a97c0c9ed42d3e2a3bf3b9f2bdba1a8e7e89ce8b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1768b31a9631be009813c0d73ba1d1c5df99362e1f8076d5484c149b991efc8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceScratchDisk, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7756b5ed8f8406518949f0bfeaca82f635b993edb2d223614619644ce40bfd7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f960bb641a75e86cbfa3a27374f2ee28983cc434b7012de1e10ebc3bf5eefe1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427f75cb779d85c9957641c00a4840081b56b9d69e1ebb116220e4a936fa56be(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd41ee930da4af3d967cfe119fc2d574b554aefafc4605574e9f6452e206898f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6da9f095b73aabaabd58ea461863d88bd4e47584ad50c550a53f566fdd2588f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065755ad43513ed805e90fc73085984b6f671c22bd9069d550a859bea392ddb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda87abc48554832b07a2c345cad1928b92f45952334342baa95e732d535f76d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061304b8bc9570ce3fca71cac41f2b997026b95b595f7aa23429d1222ae37eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef068c9e1afbe374911fcf63f0589eb503b1cd7c8398bc054b2c6cab155f0222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdce184c3b2985bd988d83092ae31975b076c98c2cadd6d64b9aebfac1e437f6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760dfdd55fc96516c89ffafb0fcaf8bafeada525c502ff82e31b7c3a50fbe1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb64d30161e10e4e7a70f61088ceecc41e49bf39745ec45dda29947b448deac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827386a96976cb5b1cfba8f1bc4df2088eb270ac10456661ab94c50a35e2c532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a169c5318895aceaeb171d76cf286a94a57843f6c5b00f70d61c77261015cb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8506f735770aabd3c417d5907828feac75ac4de895836d9753ce344f9ad47a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8e2ff78ae49fbe74b1a6d75b8cb2776df65ef14b9319d1ea6998f91acd3665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f66d79ab5ce3d572feb9b21e5e3d8d3b207adaaa11d2b0be17bfa1a43b1ffb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccdb614ea5d81676be57c95ade78da673429e7dbc3067a97ade21cabfad5ae0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693f266e167f90f7e06d05dcbcfd503199145272bd25e65646b52c2fcf3c7ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1f1f06dbd218092332eec29815353905478360269f95dc2c873e35932ad042(
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

def _typecheckingstub__6896ed0c81d27b7ef0d156c58b58a4e4a9ccb4270e89c2473727a3fd4a51dad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4449693053c0b28706e9b71deb0cd5d9bf60d082f43b2a4280a5c57782983e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3952df36ee2702b4b4842bb54875a32a071848fd511c6f48690adf60aeb678c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354e337987b5aedac5120975d7d61b67a66213fea8238ef860554d192641f7af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8395ad1d4fb9adaf96cf64a586f2985662e951e9545a57a78b1d67ba33633e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ef7a206a017d81348ea1cbcb5991af649072c06da7257d4f3503ebcc68edee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe0a6bd2b5eecc30f7e3e8bfdbabe6452a127613f76db022a8a6d42f8ef7372(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e0b15e03f5c67c3b61a4af1f597fe912b770e46e0683e97180e7ce9718a9ab(
    value: typing.Optional[ComputeInstanceAdvancedMachineFeatures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5791174c7096db26469e7488aef666a0a68f8e3aae2a4ac8e91a705149be4377(
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

def _typecheckingstub__766a0fc5b82a2e8a47d9492efe79c4064c190b24eca2f6d3dc3bbde2044d5451(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ecf2f43d9f3efb39b861950548c11f8f7f405b30505b01b13c8acdf813b2be4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f8c5418147a56ea8c1a5e620494baef9e902cdd83b0a9f1465eed2ca35d7e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efdc477bcfd00d0a07a5ce95fccb9c97e58d6a6fd3b3b4b20fb55c1c2b8f045(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dcf52f4b01a319b1b0a260e76141bd86aac4adadae0dba30a0ac841e37ce1c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58f499fda67d2879b611bfef9b56527bc6326008de397a29e2efe24d544e850(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceAttachedDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ed98aee1d4a730f1d8525e6b5d994b89666d8e7e443eb38786cd534ba9bbda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b52182cf1f47dbc5902e57d7effb6caa0f031e111819ca85ff254cec5129dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d227f661ccb7e9912e0c5f8f2ac0b121dcac6d01a56ec77b62885884de45da7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549e8f7872790a4c28206c979764db7e1575beed53c1701ac1907adeaf1c65b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb3b153ccd366beeb48024224932ebfd4cc657f999a0ce4afc87310f8320057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f32054bf5013428d44a28d8b5ba828ec755fc7d6804ca9c85489dbc45c4f8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e591fbd4113e32dac6dcc8c095236cff31c143f6c1cedbe06ed861d6db7f268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04daec281927de00856a055a0954faaff4306cbc4101ad05872290d10c15e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d079f8652825c7b79014c3d5f3a8957b348177c289ee69b250bc47d880c576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf3bea91876f22316f73d4d46203be5eec809b304f28192c731a592567a93da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceAttachedDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba93eb74fb1ffbdba71869e9b2ac86d5ff04794be94aeb7a30bd850572746c6(
    *,
    auto_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    device_name: typing.Optional[builtins.str] = None,
    disk_encryption_key_raw: typing.Optional[builtins.str] = None,
    disk_encryption_key_rsa: typing.Optional[builtins.str] = None,
    disk_encryption_service_account: typing.Optional[builtins.str] = None,
    force_attach: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_os_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    initialize_params: typing.Optional[typing.Union[ComputeInstanceBootDiskInitializeParams, typing.Dict[builtins.str, typing.Any]]] = None,
    interface: typing.Optional[builtins.str] = None,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3d6ad5fb33e7f9aff937fb161dc6fef73dee1d5ac9c71a10219ba1fff95633(
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
    source_image_encryption_key: typing.Optional[typing.Union[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_pool: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2feff607ff6b4114c93ec066e27ba686cda127e2be6984069d988915e6fc36f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263da046501fbe1666d80eada26820b248e5be14e20bf74798e37407a4c324f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ea563b350858a1e59b89ac9522c7a3810873adf3426fffd6e0937d243905cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7763fc88398d4f7d163b6cc8764eb98b2bfdc3868afc323924216b5a2d7ac823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6174fdb85d0796d8da4db3f99bd753d4f5808d9cfb42ccab866ee9b3c4b43a4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f342a6054bf7ccd69808100f5582090bf2f11cca7a5d2be566c3a2ded5835d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ff5c64d69bb6e40cb26d6e49ffb55f95077ab654fdd04bf6e024bde52cbb14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efd4521a9e3fd01c8cb0c713051958d77e5ba98713236e40ef5927e819b1adc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79455b257cbf00aa498719c292c6aba022e666ef1f60799543a6462f658067c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4385f7be9e0b542b021c3fddbfe6a898b59f2f7e9d2432ef5a65c7f2840c4c6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710457e1e5c6ee2bca5680fcce2efb315a8a27d281aefadbdd2acd04a0f259cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabb03317208203b08db2273873a973fbadab03b17736b71182d7873c264cc4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e756e787ff793572ed7e661eab19d269776290b8f6b0878ddf5a3bcc9cc2a1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b4a3bfb8ef194598a35ffd579ed240f4043f5a68234d2012ff38407ce59c2e(
    value: typing.Optional[ComputeInstanceBootDiskInitializeParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ea19c6983271410c306dd298bd766e885d01a4db3291c97b8b1a92b8e21d1(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca8c92638529a6f163ff0f4bd8670d7b608015b069a27d2d0a16c5efe824c43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c74b9824609d4232aa77f9e5f52809305004713228044387097d379be0a970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c89166dc95304bb67d2182aec35bf8736b55a24c56c3e96d498b390baca7f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c5997146c760bf69237e6ed37a05eab26ce5bf76457a41f4c4bacb86c60265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674cf2b0a25eea0979905440a72f7abeee3779475078bac9674bb6ccf2d3a2f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b5ae2d7938cc50eb152b23fc65c010320a19c43d795207e5e76519b4cfecbf(
    value: typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0143667c9510f954bcf1b048a0a79f91c3ccc2349ceb3c4b9d0fda2a4073d769(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f851cca632edeaafd3430e34729b642dd553c36849cff7cd809fc38a8b95d94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6d10f11b173a6eeca7dfcc67c13eacaa376100134152bb4d0f4469d1a422e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbc54eb94a4100588f9d64ac99b275dc65ef49e7596814f24780a41ede8e6a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d700642c3448dcff00636cb10415a62296fe87c573a98e255c02394a91c3e3b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae178b87574ce8d804e5bfeafa6f55cdcfa5195ec67a0342d1a860f9feb31254(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc7570d4fa84751783dff7ae4ed48cf02ce0c0ca2bcea54ed5eb62c5a6ae1b7(
    value: typing.Optional[ComputeInstanceBootDiskInitializeParamsSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338c6e5bf586fa4dce16a010800aba4b9cbada2ffb8ba862c602061069058812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb378aefe21f38ee695fa1310290112793543fc9e7132e37af9b683397c6c04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792d84d9c2efa556ad5991c92bdeb83de285d65eb29ed5c2a9f794cad6e4a06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9758ca65b83e42a2040375b8cd6d80c8d7c6679e640324a929a8e84fcdc91b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503f05c7fa9933dd2163ac336eab4748de4128c5dd6daabd02d1007ad9a97e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a808146aa1f350c02bbf3b82e1ace1867910c06a6b7e8f3b511b8ddd4f7b3d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7450501b2205835a01c09ba10f89f890cbfe8b591b141403e06bf6c6f08961(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ad89a563e4d78b7cfff693bd0f00f953d9aba889a847bc278650f393e858a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b58b03b54746004002e5904fa2bb53afaac3e0ee4a9b77fbe4044b037b474b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1343726947627bfa1258c55b4325c042414883707cf8134fb59c40dd27f62e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81793065d3253cfb637b8fe56060f8d702c3197eb2d472398899587d91b072b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126e5979b53b28188291996386c2e475da6bc2d9ddb336dcf06d69950d28a145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a178d054d197480a110df5108db9c0f7c3317339d39947ffe158218b0d76aa(
    value: typing.Optional[ComputeInstanceBootDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f97210661d238da5afbc3935a612adff197fadad31e26f79150f3f12e00c2a4(
    *,
    confidential_instance_type: typing.Optional[builtins.str] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a929d62eafc2e9cbca9a82c799f48003fe304f67a222f5041c9003946f88490a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b3881a0d8307dd46eb16fc9e915dfb19eaffaa1b45e5572cf6074bb913d8bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e23950a95bfa52772d9388ad95074a60df37579a1119366f89bcdb88070cafb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6d50fb4946b93ba1487a9ba1644d0d84cb0240803f2da785e343c50204cf35(
    value: typing.Optional[ComputeInstanceConfidentialInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7d352a39f94a2de429bc1f3219c2b473c07e3b4e97393a2f38b40019fb1d9c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    boot_disk: typing.Union[ComputeInstanceBootDisk, typing.Dict[builtins.str, typing.Any]],
    machine_type: builtins.str,
    name: builtins.str,
    network_interface: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterface, typing.Dict[builtins.str, typing.Any]]]],
    advanced_machine_features: typing.Optional[typing.Union[ComputeInstanceAdvancedMachineFeatures, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_stopping_for_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    attached_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceAttachedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    can_ip_forward: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    confidential_instance_config: typing.Optional[typing.Union[ComputeInstanceConfidentialInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    desired_status: typing.Optional[builtins.str] = None,
    enable_display: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_accelerator: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceGuestAccelerator, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_encryption_key: typing.Optional[typing.Union[ComputeInstanceInstanceEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    key_revocation_action_type: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata_startup_script: typing.Optional[builtins.str] = None,
    min_cpu_platform: typing.Optional[builtins.str] = None,
    network_performance_config: typing.Optional[typing.Union[ComputeInstanceNetworkPerformanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    params: typing.Optional[typing.Union[ComputeInstanceParams, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[ComputeInstanceReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    scheduling: typing.Optional[typing.Union[ComputeInstanceScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    scratch_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceScratchDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service_account: typing.Optional[typing.Union[ComputeInstanceServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_config: typing.Optional[typing.Union[ComputeInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f59522513e66eebe5e3db09bad32c21944eb00ba774d0752b52e17cab2e615(
    *,
    count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247c49360a9f68c823bc2a734a634ddbabaeef8eceff76707ac0d25e8e9cd0f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4abc939da49232e8456836e32cc8bdddbd6e860f6ace91fd08b3e19956c2618(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f919d30a474e58a343807e05f0356295633c4c89c167552c0f5b64c23fe04927(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41464d8038b578d00f34acc42e64d2cb3a2d8f4a41f269cb8e2d6edbe2ce2c8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76fd87e07b53eed3c6225dc0bc10ca2c2ba1086aee275e1755f4f665b0910e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ef3726f09d74c425b11130c3c5f31009100fdc0354b1e5d2d344a0e4bdb77c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceGuestAccelerator]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf87aaf44419ae1fa96722b02b0152d23eaa7b8ea6d0f68397eee5ea4de2a87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0889408c475acb4416b4d3dd6e662d8e9b1f763aaf477cad25931e6312374991(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03ce4d1f08e0a4fe794a7534f0deb1ddd7a251ed7e3ba05fc3b30b4920c2f0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a153cc800fb4b02020f39b3757fb2e1de096eb07024255f5c0a0dcc8417825b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceGuestAccelerator]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aebf5c11cb172bca0891060ba91689876a78195b833c114fdd0a253a98b42c(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6caeefc8eb46e18d9c6c4dfadcf846e3e8f24bde6a5140fa5b3ed676fac8d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539f1e3bb9a7c225ee9aa2c5fe7cdb210b4083a2ca02e502c32d17520e53ffff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663bd37a2afa2e0c21fc6833411d2e6d53ed89bae4c48c84b53fa68577bfa177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0851e6dc69403d8b7d38b188180e97e71e8c102e5e558c34b27aa649c2fb3ff3(
    value: typing.Optional[ComputeInstanceInstanceEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46c619ee9726afb3cf6ea4aa1e6dec0518d9caed52ea6feda9d6195d6d37243(
    *,
    access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias_ip_range: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]]] = None,
    internal_ipv6_prefix_length: typing.Optional[jsii.Number] = None,
    ipv6_access_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__af5a74f41cd882ec3e43040bc3cf3e4c94eb017f10bd81b7f46b329e59a3ebae(
    *,
    nat_ip: typing.Optional[builtins.str] = None,
    network_tier: typing.Optional[builtins.str] = None,
    public_ptr_domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd0d8f816e40596710c0328b5de5fa191cd673c15759e2debe47029d9f0aed3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28edcee7721fb70f76192c823ffbc04b7df86031c30c9cc758f302d9188c071(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7e30d0d47bdf545ec38a4f90ff090de9d6f8c44ebc939198e664ac0345738f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235b4754e24ac7643ab4480b85eb5fffed7d9f0dd53b6c5ad2c896773a545ff9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61a00bf8077e1d67c1a37d4c0f9272ea7819aa5921d2a8ec2112813a6d94c24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d40612b5f6554cd1e1e5fdcfc1f75c3eb69c14ac778819b5deb5ecff2fd5e11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dfe98a7f3e1212bc32878ab14a18efb5019d6e4f1e8b3e4d31fbba82b30b10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6941fb9ff0497fa8dba32b92eeb1e414a5e98d39f5976fc939690ae21afbb50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37083e62a23a56b5afc962962169fd6d6e5dd06245f0c0d8237fa14c751378ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3b785057c6b4b52956963aaccf07afd6c36597f36dfdc3bcf63c1159d66b69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0608716d1a7065f5b5a35f6e8edb9d4937afbdbb9374a0aea8c48f7368986ea9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e339b7cf5a7f16cc9875edfb1f8c943997c95394317ce701775ad17d044369(
    *,
    ip_cidr_range: builtins.str,
    subnetwork_range_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359cd35dbd403af81dbc7bd275994049f6bccd45c368ddf759aa9d0d2771371a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c82a31b988b726f39ec0914056e9ccee3d362b3eac55a6156593ce58c711bc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288deb32f3bc8271186fa112dcc44418d1e92e584dfea9358aa2e2fc4eb5ffe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c920f1571107c3f2ff035e1df753cd572f7c4c17c14c76f435f0ac8be6cf90f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535ca034fc8f64f4baef74df7f9f57d078dd0f30410c6ce7af6430879b162e48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353ebc5a84c1a6db572a470f2edf0861627f93f19f8acc8404e6d14eed5de833(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceAliasIpRange]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f3490600984ff3792773a0aec12fffa6266b37a47120a064b65c9afe107064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd4cd25389ccd4409278120e4fe5a5cb076f03da70c4ebc11bf72fecf56299a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e27b8e68171976a3aaf069c35d8a1e1371e5b6a4e0f719c1bc9924fb4a8574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd246fa380faf31c39f06daf5875669dbbf3301f2e17657ee2c2d2bdec40986(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceAliasIpRange]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4891a0cc8ae15a81b18b2feaf13e08184e683605f10ba54b6306549c9c529329(
    *,
    network_tier: builtins.str,
    external_ipv6: typing.Optional[builtins.str] = None,
    external_ipv6_prefix_length: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    public_ptr_domain_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d854ae0766530fbef642765f82edd1a5aff60f7b05db0af438dc85ede6aa191e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369e62c9752defaebca0c380f8cef69421feb4312a23f44cfa81b82f1cdf8d91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d3f145f16afb4624c0d454ce41b498463be2a9988826bc4ad6df8d206ea5b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa3b52f289954ec0fba0b89a887240cf5680868fb0c30ec4f6b894171e632ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9001f136462314762f22205f0a7723dd3dddd04e9791e73bd0e0e461eb5a85(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1c0230f74930d28cc850a30d647cb3e6aa3d4c408272b8163f6e9a468e3626(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterfaceIpv6AccessConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69a3a833e55f151cdc47e08172c078242005f460cc60bc606dce58b56ba9b67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6d0a8f16708a70cc99f82ed24fb580d4732dac0f8fc8e2aab85fbcd75884a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e425582f1f9d8fef9bc9b46b25edd3d602be00b8302b3ca352f2f868c67e00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa230005ef601c467fc1f0b26619069303600ce96025457f1f3b527f67e9f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78d0e9e8c552353f42f1f278d0102d6b32467b7ed3687616e60573876a5fbac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6f8d75885311bc3e97568e5112ddd3be53a5ff67de40fd3ab8828e0bc477b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531eeb9bb173658d509cfc40ee97e645a6479e43443f75c8c8af369858a1781a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterfaceIpv6AccessConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69f1557ec27aaba96b4c949986f21cab807c87d980c6247dcd4b7f50b854c97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775b077c37a2d474010748ac8a60fff2592b537bc41604b7ccdbdb48d0a423a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a89f888dbd01cc5a685294c4a1584dbdcb660d3e2407dae77f565402d95f048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63cc524f1ad9b6d2ddff1a6e68b986ddfd6f792e74d2110edf4bdccd7de0a4e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4995e40193819e6ef9fb481e93c2897fae8800b9b37a7bd9eeef8472f241c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dd350a388ca64a5c560a924cdf834a57b3557c2d3bf01de3d8082bb483c392(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceNetworkInterface]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2064f81792dc7618467bc763b479fa8a189fccaef5cf570664330a369ed5fd37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760d48204628f5d6b17e7451b8a8b326e6fd925980cb2a7c435df6b89163bbb0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b60605bc414e16a33c7c94b2844b403d906a39be99a4d33a855282f931269a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceAliasIpRange, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce85dd34ccd811e5586ffd7502b766de3bed09df5c81abe4b60223f7d36b3bde(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceNetworkInterfaceIpv6AccessConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29b8420a5c3e2e69880c4d08712ad2d44e4d117884d83c81c3dfe019dc3d684(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad20a07c1c79e9f4c343fc44d83a2dd4b15ddc0bb23149ff0cf4daf91ca633f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74fa93a0ba6069935d83bff8c966305401c52e8fa2710e543e9776dab93c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdff6c0f02549af0fb2f753ac2c173b2250bcfbfdf4eb4ee92b37ac126667674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af07f8220a060a05574c893c837aefe9dff19fd8615b85b66b85ce41831732f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58214ba873e2ea1d358255241058e4d644053f05880e386f4d0487cee413e1b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0504996b75a7c4e43c150a658c504b68c16dd7cb494be97f27242a516ca9c2a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94191757a511d552085a61e0513fc84f03deeea6539f6de9f9023186c6b07231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b16845ccd7fd58eb0806ad1689719cd78a5b120396cded4be79043bef9f4d9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ac4154c2b5df045e6a9db7d76a4c375805ba02c078c26491435380cdbd231f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16651765d943e435dc817c993c60297180201d0f2ac8bf7c3b1f08f9bafb83d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceNetworkInterface]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07d90409299aa4763de1508aed0efbf930280ffe749579f0e53dafc412e52d6(
    *,
    total_egress_bandwidth_tier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207ecca916c7d10d36ced70afd3e78fd2c7cc173e3c2bbd1449065916f0f6089(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb016d4f253f3f5f8800bc239de823b779ce5ad3cff085d05ad2911e46c6c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12dbf216e25f455ed4e4669dedcf274745f60244e8a938ae89b1d35942a859c4(
    value: typing.Optional[ComputeInstanceNetworkPerformanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f16cf8c4a06f819fd3970bb06e665d5b77367370bba6b09c9ed7236844685b4(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5fbd72040c516b37817cf5379cfc7a46b9762dbd36a8d8c894184017d1b51e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c834d6999f019395ef6e5452a718bb1f5801440412f00c445441f29503f3bf5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7411aabac1d7f2cd56a2e68b05bb0db79976d2868eb5f7abec18a834b12d3223(
    value: typing.Optional[ComputeInstanceParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05704e6b49d52429abb9d6b53d99a83669ae75be9249ce530238b19962a9caa(
    *,
    type: builtins.str,
    specific_reservation: typing.Optional[typing.Union[ComputeInstanceReservationAffinitySpecificReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69899e0b0c0bf21eb35cb0a64ad4964199da2507f73c0a2fcebfa64c0574a907(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cd73b603fe4601575e252998c3783374c951f7b6a6b4873281b9b32d407ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c081aa02ac131e65bb2a499293eebe11816fcfc97afff4ed3b0d79a262c7ac79(
    value: typing.Optional[ComputeInstanceReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b7d1a5c53bed5aaf0a08b9d3b70d9779b82e0c14c8a2be0a11f33ca60b0e0a(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d568d950cb2e647276cd9769bcb2baecdc4a9507f282f8a4cf13bf224d85393(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63b1f3ea632a52a6f5a6256008c7c4dae45b560b86353012a9edcd7c7ccc3dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07919f29adba8ffb4f5759e6f4c0e74c9946026a7c1fe7923ac5d1bedf80ad38(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab5a563a66b58337ebe7db037382f08fa85d915b5470bb296988de103e982a5(
    value: typing.Optional[ComputeInstanceReservationAffinitySpecificReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072ecb19ad75aca724c504d0ae33c7e71b61d3decb5b8f27793223716c859410(
    *,
    automatic_restart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    availability_domain: typing.Optional[jsii.Number] = None,
    instance_termination_action: typing.Optional[builtins.str] = None,
    local_ssd_recovery_timeout: typing.Optional[typing.Union[ComputeInstanceSchedulingLocalSsdRecoveryTimeout, typing.Dict[builtins.str, typing.Any]]] = None,
    max_run_duration: typing.Optional[typing.Union[ComputeInstanceSchedulingMaxRunDuration, typing.Dict[builtins.str, typing.Any]]] = None,
    min_node_cpus: typing.Optional[jsii.Number] = None,
    node_affinities: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]]] = None,
    on_host_maintenance: typing.Optional[builtins.str] = None,
    on_instance_stop_action: typing.Optional[typing.Union[ComputeInstanceSchedulingOnInstanceStopAction, typing.Dict[builtins.str, typing.Any]]] = None,
    preemptible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    provisioning_model: typing.Optional[builtins.str] = None,
    termination_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4399ca954db5594624c615abae7958492641cba94276f59a10474f8244c9cc75(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac106351b790c739cdf5c2a2f96a43f914ff0ee67426f3efec87408fc9d5ce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5225438710cb704b1193e4fdcff3c2af0a6470f288b92fdd451b3dbb8f19335(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8336861dba02af7698979808b828a54e846da6305a0acd84bb8b7cd8ed412298(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91170ce7e79d6c02d1247b1d5706c0820f548c23f28f901e686144ea31ecc15e(
    value: typing.Optional[ComputeInstanceSchedulingLocalSsdRecoveryTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63447458be67be8dc5010dba2c13183fff2546ced7ecf30a0478e4537a2054b(
    *,
    seconds: jsii.Number,
    nanos: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bf8d51821131896fa080183045e5023f2c58546f1d79899a59b61048294790(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5017aac4b79e94b96f8ab2ba08dda685f49a1e0637b331d9fdf90590d3b73437(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e4e4b343e5b0823555c18d6ccae91d5dfae07bc319a49d4267a56baf0de425(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0571df086c5aa3bd2c728b8d2d2bd6788269a8ecab4064b9486789e10ac00c0(
    value: typing.Optional[ComputeInstanceSchedulingMaxRunDuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c36cf12b647b6f9cae5fa365ed3ec5cbbaf1318928d4e6baff69f04851d22c(
    *,
    key: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92e6f7deb03ea7ec17f31f2e082dd41c7696a5246f613f0f0a504e49849e104(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5456ac367c258d766a886469b53b5b1e8de8ecfa9745a59001d43be52317f0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a488e1cf4f7ae2607e6dc6090f2f9aeae14abb713a7dd8e849767c51622669d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84fa21cf720467dc75841f03ff9956a4a0bb26067688558030f1b51808426996(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44df5ef72d814853debd40c93f3e7ddadb7634513bea093fa58557322b0aa84f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670a18302172823a986c024fd81f68bd84e06d14ab66bf68668ffb82444c9c11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceSchedulingNodeAffinities]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2940cd39e02564e11419d05bd0b1cc710116776d0508c14b175389114572966d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead5d531c169bd411941ecdcea6a58378b8c140a83363536e14057f0a5d1fad5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d704d2e7674952cb9d3ae5972599fd499d1b3452ec3cc1499faaa9046e0e139a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2923e0255fa6ab388dce508971d0b575fc5e0a9635b4220dd3f7d7be717d2ed8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d87a0f008b17e58e40cc171e594ccb5e1e4395337ccd3d31b52f89619599ef4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceSchedulingNodeAffinities]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db58d7f982ee370edfdd5525ce1dc0729d236995c044b37c31240199f5d2bb2e(
    *,
    discard_local_ssd: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e846a24371df771856ed3ea6f75d501422dd7898f7db0d9da86cd1d5d154bd02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe467caae63c3fda48e3a45c37a65e9c3419127013fb6ecf4fcae231f5833aba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce12ab29a5b8e6e138dd73dd3c3a62ef746c4d04fb0c880e153efd97775a2137(
    value: typing.Optional[ComputeInstanceSchedulingOnInstanceStopAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cee1494abc3aa217547b29eb8c8475499bdd06d30d8eed3c3452e574d47dd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a537e3580e567d29d534f41540238360e063d86506a06fa1adef6ab6b4e72c98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeInstanceSchedulingNodeAffinities, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abd2e4eb731341073b67b40cc948ce1b3c57353e470fe94d8317fda2df29d32(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b021173669ec965f3d07f18addb0084624e69d352a8b7163d58bde96093c909e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d630f7c9597372581bffed47fef5c2f6cbe20b0fd729237dabafbbf6cb90cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799733ab73987c94fbf2501b8eef3d9c55e23359752f59340c8766f918f00595(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d57a47b01b87739dab8bef2254053cc22ae25f5e83cb1db81ce3e78842a1115(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a148a8d068277bd09f35ab99d66412ece414f5f7e9ff9aa00be217a464203712(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ac80aba37dfb2a7cfb43a3eec1d3b5e61ab288eab5b888fab8948d22b1a5f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90f883f1f2139a3d829d29928725e68424b6c35dc8a606ae7778e85542a7458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91daeb4cdf086725ca062ca983de7709939dfb7c3b623d21e27304d0bc4ded12(
    value: typing.Optional[ComputeInstanceScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1779424e4b080267967c867b43cf73426056fb47afb43fb4f96f3723a931c47d(
    *,
    interface: builtins.str,
    device_name: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacd9ffd13adf6bb3574ffe8739da666c89e226c13d4fdbda67192430c24c4cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f92d64ebb5dd335f3ca757de41a61d6bce50c4ec60ed2dba8aa26bc0e67ae2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04e035e737f209249a3cb1b8a007797c3a34df761c3a297108d04c0e13baebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41b464cbf847df86753b432031c10eac943c4122fd939ef92d00a46b0cf6c0f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fce846a387ac1ecd3886e2470b52b127415e0e3f9fa08711d28d140ad6ef3d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9805989221e3589866dc8d185c22eda3008e7551c7e0703fffde94aa3e7fbdf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeInstanceScratchDisk]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9bcb1ea1c2d14c1b9575c4e7332174018ba3249e9ca2a232e0daeb06da6c44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490e55034113e9310407474e1f461218dee6490bfc673b2e21718d37410eb845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aeb5b57c0904f3d9df94b2ef516712ff7e2ecc530adf22b8ffd02980d214315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f38bc4d8bf77f09bd714c33acd82b511bb56883ab098ea0c14a54a63d5c37d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267e7c06a4b830eb46e0a8601fe25f6121aeabe5fcdfedfd5255c79792e73dc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceScratchDisk]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb64214dc111d98c4183535bf85b7bf478108dc2d4ce481e5bbec174e9850f4f(
    *,
    scopes: typing.Sequence[builtins.str],
    email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddac717c9c0e474ff7132f337ef71c494f85882bd212af5b26e51d4ad50f1a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98673066e6bb466def3312f7bc4ecfb174db6cc32201181daa3763887a14f9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d3ace1a487ab1c6488582482896c84ec89ce1aafe09677b64692d36d721521(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d01ac37d71e3297379d1e328e249cf6a07eb86c4f70cfec1c5946381b7a0c4(
    value: typing.Optional[ComputeInstanceServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07d22eb4cb5ee6aecf46170783fbbdd3b972fa46ec38b667708307e8aa782fe(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3221773938187172b27106c0c17b9712decf62247436f1e1509d3fb9fe1cb99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db80dc23fb849b7e5eff42ca96a31f92c407815c605e2f755cc9f4f68c16d934(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f61f2578b7831bf4eb0be4bbb03f18ea70890ee6d45522e0bc4166cec1a7c1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ddf796b3a14b1d0e0f6f3d71ef964c3e34e5da7c1e20a70bfb1ddda8a29c7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9a525424930dd4cb1ee33a8fe8d759baaf11ed5f79258d2054ffb40c85d70b(
    value: typing.Optional[ComputeInstanceShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e223aa44362252401bfff74a2718429a880c337a0b15340c918f03be0bd33e36(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a3ddcd59722b69d828f36b4dfb04bb3006386ca84218b4d51fb4dacd98fa9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f3ecb517f6301fc0d9d58271e0b032782369bf52889e6a0bc3592579069c07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319856d4d780ec94173d8f8e1573de34c040a129cfd54018e8595e6ffc1ce713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe554ab204907ff643539b40ac1757148e2def3d81410aef58cf2b2e08514839(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b626fcda90bac1de9cd769a289de3a883379cb63fa87638c2465a86f19adf01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

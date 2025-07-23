r'''
# `google_notebooks_instance`

Refer to the Terraform Registry for docs: [`google_notebooks_instance`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance).
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


class NotebooksInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance google_notebooks_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        machine_type: builtins.str,
        name: builtins.str,
        accelerator_config: typing.Optional[typing.Union["NotebooksInstanceAcceleratorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[typing.Union["NotebooksInstanceContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        create_time: typing.Optional[builtins.str] = None,
        custom_gpu_driver_path: typing.Optional[builtins.str] = None,
        data_disk_size_gb: typing.Optional[jsii.Number] = None,
        data_disk_type: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        disk_encryption: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        no_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_remove_data_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["NotebooksInstanceReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["NotebooksInstanceShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NotebooksInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
        vm_image: typing.Optional[typing.Union["NotebooksInstanceVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance google_notebooks_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#location NotebooksInstance#location}
        :param machine_type: A reference to a machine type which defines VM kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#machine_type NotebooksInstance#machine_type}
        :param name: The name specified for the Notebook instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#name NotebooksInstance#name}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#accelerator_config NotebooksInstance#accelerator_config}
        :param boot_disk_size_gb: The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). The minimum recommended value is 100 GB. If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_size_gb NotebooksInstance#boot_disk_size_gb}
        :param boot_disk_type: Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_type NotebooksInstance#boot_disk_type}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#container_image NotebooksInstance#container_image}
        :param create_time: Instance creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create_time NotebooksInstance#create_time}
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#custom_gpu_driver_path NotebooksInstance#custom_gpu_driver_path}
        :param data_disk_size_gb: The size of the data disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). You can choose the size of the data disk based on how big your notebooks and data are. If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_size_gb NotebooksInstance#data_disk_size_gb}
        :param data_disk_type: Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_type NotebooksInstance#data_disk_type}
        :param desired_state: Desired state of the Notebook Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#desired_state NotebooksInstance#desired_state}
        :param disk_encryption: Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["DISK_ENCRYPTION_UNSPECIFIED", "GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#disk_encryption NotebooksInstance#disk_encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#id NotebooksInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param install_gpu_driver: Whether the end user authorizes Google Cloud to install GPU driver on this instance. If this field is empty or set to false, the GPU driver won't be installed. Only applicable to instances with GPUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#install_gpu_driver NotebooksInstance#install_gpu_driver}
        :param instance_owners: The list of owners of this instance after creation. Format: alias@example.com. Currently supports one owner only. If not specified, all of the service account users of your VM instance's service account can use the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#instance_owners NotebooksInstance#instance_owners}
        :param kms_key: The KMS key used to encrypt the disks, only applicable if diskEncryption is CMEK. Format: projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#kms_key NotebooksInstance#kms_key}
        :param labels: Labels to apply to this instance. These can be later modified by the setLabels method. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#labels NotebooksInstance#labels}
        :param metadata: Custom metadata to apply to this instance. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#metadata NotebooksInstance#metadata}
        :param network: The name of the VPC that this instance is in. Format: projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#network NotebooksInstance#network}
        :param nic_type: The type of vNIC driver. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#nic_type NotebooksInstance#nic_type}
        :param no_proxy_access: The notebook instance will not register with the proxy.. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_proxy_access NotebooksInstance#no_proxy_access}
        :param no_public_ip: No public IP will be assigned to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_public_ip NotebooksInstance#no_public_ip}
        :param no_remove_data_disk: If true, the data disk will not be auto deleted when deleting the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_remove_data_disk NotebooksInstance#no_remove_data_disk}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#post_startup_script NotebooksInstance#post_startup_script}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}.
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#reservation_affinity NotebooksInstance#reservation_affinity}
        :param service_account: The service account on this instance, giving access to other Google Cloud services. You can use any service account within the same project, but you must have the service account user permission to use the instance. If not specified, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account NotebooksInstance#service_account}
        :param service_account_scopes: Optional. The URIs of service account scopes to be included in Compute Engine instances. If not specified, the following scopes are defined: - https://www.googleapis.com/auth/cloud-platform - https://www.googleapis.com/auth/userinfo.email Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account_scopes NotebooksInstance#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#shielded_instance_config NotebooksInstance#shielded_instance_config}
        :param subnet: The name of the subnet that this instance is in. Format: projects/{project_id}/regions/{region}/subnetworks/{subnetwork_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#subnet NotebooksInstance#subnet}
        :param tags: The Compute Engine tags to add to instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tags NotebooksInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#timeouts NotebooksInstance#timeouts}
        :param update_time: Instance update time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update_time NotebooksInstance#update_time}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#vm_image NotebooksInstance#vm_image}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380dc868810684db7e40643563cfd009fd9af8b81fb377ea355e308dd8d51801)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NotebooksInstanceConfig(
            location=location,
            machine_type=machine_type,
            name=name,
            accelerator_config=accelerator_config,
            boot_disk_size_gb=boot_disk_size_gb,
            boot_disk_type=boot_disk_type,
            container_image=container_image,
            create_time=create_time,
            custom_gpu_driver_path=custom_gpu_driver_path,
            data_disk_size_gb=data_disk_size_gb,
            data_disk_type=data_disk_type,
            desired_state=desired_state,
            disk_encryption=disk_encryption,
            id=id,
            install_gpu_driver=install_gpu_driver,
            instance_owners=instance_owners,
            kms_key=kms_key,
            labels=labels,
            metadata=metadata,
            network=network,
            nic_type=nic_type,
            no_proxy_access=no_proxy_access,
            no_public_ip=no_public_ip,
            no_remove_data_disk=no_remove_data_disk,
            post_startup_script=post_startup_script,
            project=project,
            reservation_affinity=reservation_affinity,
            service_account=service_account,
            service_account_scopes=service_account_scopes,
            shielded_instance_config=shielded_instance_config,
            subnet=subnet,
            tags=tags,
            timeouts=timeouts,
            update_time=update_time,
            vm_image=vm_image,
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
        '''Generates CDKTF code for importing a NotebooksInstance resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NotebooksInstance to import.
        :param import_from_id: The id of the existing NotebooksInstance that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NotebooksInstance to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b1227173ac2d367b13faf2984ea6b4043e35321f429e620f211bfbe7e8f7d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAcceleratorConfig")
    def put_accelerator_config(
        self,
        *,
        core_count: jsii.Number,
        type: builtins.str,
    ) -> None:
        '''
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#core_count NotebooksInstance#core_count}
        :param type: Type of this accelerator. Possible values: ["ACCELERATOR_TYPE_UNSPECIFIED", "NVIDIA_TESLA_K80", "NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS", "NVIDIA_TESLA_A100", "TPU_V2", "TPU_V3"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#type NotebooksInstance#type}
        '''
        value = NotebooksInstanceAcceleratorConfig(core_count=core_count, type=type)

        return typing.cast(None, jsii.invoke(self, "putAcceleratorConfig", [value]))

    @jsii.member(jsii_name="putContainerImage")
    def put_container_image(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#repository NotebooksInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tag NotebooksInstance#tag}
        '''
        value = NotebooksInstanceContainerImage(repository=repository, tag=tag)

        return typing.cast(None, jsii.invoke(self, "putContainerImage", [value]))

    @jsii.member(jsii_name="putReservationAffinity")
    def put_reservation_affinity(
        self,
        *,
        consume_reservation_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: The type of Compute Reservation. Possible values: ["NO_RESERVATION", "ANY_RESERVATION", "SPECIFIC_RESERVATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#consume_reservation_type NotebooksInstance#consume_reservation_type}
        :param key: Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#key NotebooksInstance#key}
        :param values: Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#values NotebooksInstance#values}
        '''
        value = NotebooksInstanceReservationAffinity(
            consume_reservation_type=consume_reservation_type, key=key, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putReservationAffinity", [value]))

    @jsii.member(jsii_name="putShieldedInstanceConfig")
    def put_shielded_instance_config(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_integrity_monitoring NotebooksInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_secure_boot NotebooksInstance#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_vtpm NotebooksInstance#enable_vtpm}
        '''
        value = NotebooksInstanceShieldedInstanceConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create NotebooksInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#delete NotebooksInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update NotebooksInstance#update}.
        '''
        value = NotebooksInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVmImage")
    def put_vm_image(
        self,
        *,
        project: builtins.str,
        image_family: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: projects/{project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}
        :param image_family: Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_family NotebooksInstance#image_family}
        :param image_name: Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_name NotebooksInstance#image_name}
        '''
        value = NotebooksInstanceVmImage(
            project=project, image_family=image_family, image_name=image_name
        )

        return typing.cast(None, jsii.invoke(self, "putVmImage", [value]))

    @jsii.member(jsii_name="resetAcceleratorConfig")
    def reset_accelerator_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorConfig", []))

    @jsii.member(jsii_name="resetBootDiskSizeGb")
    def reset_boot_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskSizeGb", []))

    @jsii.member(jsii_name="resetBootDiskType")
    def reset_boot_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootDiskType", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetCreateTime")
    def reset_create_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateTime", []))

    @jsii.member(jsii_name="resetCustomGpuDriverPath")
    def reset_custom_gpu_driver_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomGpuDriverPath", []))

    @jsii.member(jsii_name="resetDataDiskSizeGb")
    def reset_data_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskSizeGb", []))

    @jsii.member(jsii_name="resetDataDiskType")
    def reset_data_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDiskType", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetDiskEncryption")
    def reset_disk_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryption", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstallGpuDriver")
    def reset_install_gpu_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallGpuDriver", []))

    @jsii.member(jsii_name="resetInstanceOwners")
    def reset_instance_owners(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceOwners", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNicType")
    def reset_nic_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNicType", []))

    @jsii.member(jsii_name="resetNoProxyAccess")
    def reset_no_proxy_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoProxyAccess", []))

    @jsii.member(jsii_name="resetNoPublicIp")
    def reset_no_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoPublicIp", []))

    @jsii.member(jsii_name="resetNoRemoveDataDisk")
    def reset_no_remove_data_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoRemoveDataDisk", []))

    @jsii.member(jsii_name="resetPostStartupScript")
    def reset_post_startup_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostStartupScript", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReservationAffinity")
    def reset_reservation_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservationAffinity", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceAccountScopes")
    def reset_service_account_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccountScopes", []))

    @jsii.member(jsii_name="resetShieldedInstanceConfig")
    def reset_shielded_instance_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceConfig", []))

    @jsii.member(jsii_name="resetSubnet")
    def reset_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnet", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUpdateTime")
    def reset_update_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateTime", []))

    @jsii.member(jsii_name="resetVmImage")
    def reset_vm_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmImage", []))

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
    @jsii.member(jsii_name="acceleratorConfig")
    def accelerator_config(self) -> "NotebooksInstanceAcceleratorConfigOutputReference":
        return typing.cast("NotebooksInstanceAcceleratorConfigOutputReference", jsii.get(self, "acceleratorConfig"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> "NotebooksInstanceContainerImageOutputReference":
        return typing.cast("NotebooksInstanceContainerImageOutputReference", jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="proxyUri")
    def proxy_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyUri"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinity")
    def reservation_affinity(
        self,
    ) -> "NotebooksInstanceReservationAffinityOutputReference":
        return typing.cast("NotebooksInstanceReservationAffinityOutputReference", jsii.get(self, "reservationAffinity"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfig")
    def shielded_instance_config(
        self,
    ) -> "NotebooksInstanceShieldedInstanceConfigOutputReference":
        return typing.cast("NotebooksInstanceShieldedInstanceConfigOutputReference", jsii.get(self, "shieldedInstanceConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NotebooksInstanceTimeoutsOutputReference":
        return typing.cast("NotebooksInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vmImage")
    def vm_image(self) -> "NotebooksInstanceVmImageOutputReference":
        return typing.cast("NotebooksInstanceVmImageOutputReference", jsii.get(self, "vmImage"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorConfigInput")
    def accelerator_config_input(
        self,
    ) -> typing.Optional["NotebooksInstanceAcceleratorConfig"]:
        return typing.cast(typing.Optional["NotebooksInstanceAcceleratorConfig"], jsii.get(self, "acceleratorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGbInput")
    def boot_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bootDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskTypeInput")
    def boot_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional["NotebooksInstanceContainerImage"]:
        return typing.cast(typing.Optional["NotebooksInstanceContainerImage"], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="createTimeInput")
    def create_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="customGpuDriverPathInput")
    def custom_gpu_driver_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customGpuDriverPathInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGbInput")
    def data_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDiskTypeInput")
    def data_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionInput")
    def disk_encryption_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="installGpuDriverInput")
    def install_gpu_driver_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "installGpuDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceOwnersInput")
    def instance_owners_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instanceOwnersInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="nicTypeInput")
    def nic_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nicTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="noProxyAccessInput")
    def no_proxy_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noProxyAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="noPublicIpInput")
    def no_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noPublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="noRemoveDataDiskInput")
    def no_remove_data_disk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noRemoveDataDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="postStartupScriptInput")
    def post_startup_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postStartupScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationAffinityInput")
    def reservation_affinity_input(
        self,
    ) -> typing.Optional["NotebooksInstanceReservationAffinity"]:
        return typing.cast(typing.Optional["NotebooksInstanceReservationAffinity"], jsii.get(self, "reservationAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopesInput")
    def service_account_scopes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAccountScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceConfigInput")
    def shielded_instance_config_input(
        self,
    ) -> typing.Optional["NotebooksInstanceShieldedInstanceConfig"]:
        return typing.cast(typing.Optional["NotebooksInstanceShieldedInstanceConfig"], jsii.get(self, "shieldedInstanceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NotebooksInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NotebooksInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeInput")
    def update_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="vmImageInput")
    def vm_image_input(self) -> typing.Optional["NotebooksInstanceVmImage"]:
        return typing.cast(typing.Optional["NotebooksInstanceVmImage"], jsii.get(self, "vmImageInput"))

    @builtins.property
    @jsii.member(jsii_name="bootDiskSizeGb")
    def boot_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bootDiskSizeGb"))

    @boot_disk_size_gb.setter
    def boot_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabd6e29a0452e6e88c0790f8889cfdbcd54c2512fc8415af0c5399726c40bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootDiskType")
    def boot_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bootDiskType"))

    @boot_disk_type.setter
    def boot_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6984b672ef381761fca3fb8283baa6eeea0fa66450d6c040ada956af95d298e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @create_time.setter
    def create_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b3531e69c33240ed5b804f701fea9fbf89c82213379d5e3ec03550ccf1fc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customGpuDriverPath")
    def custom_gpu_driver_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customGpuDriverPath"))

    @custom_gpu_driver_path.setter
    def custom_gpu_driver_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef83a1f84372489101c179a907c600f2b957a800aa4c2fdc9bc9f10af16ff45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customGpuDriverPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskSizeGb")
    def data_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataDiskSizeGb"))

    @data_disk_size_gb.setter
    def data_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0a3b16242c74f5a7f20b0209d804ec622910731039ad82826af3dfdd04db7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataDiskType")
    def data_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDiskType"))

    @data_disk_type.setter
    def data_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74560d0e0d5f6a6968d68c84d622f4bb54dc51f6fbe9247268f8f519247aaf08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDiskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80331c270dab5bbdba1b63a19a50a496bfeecff693cfee7c5d90096ebac730ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskEncryption")
    def disk_encryption(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskEncryption"))

    @disk_encryption.setter
    def disk_encryption(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8319f19e0f25710d572e6e9258a03716265bfc14af2018082545c20740613892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066beaec18a3f52fef360fd77ae0514d9a7fa2c6dcdbde2112438aaf74872b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installGpuDriver")
    def install_gpu_driver(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "installGpuDriver"))

    @install_gpu_driver.setter
    def install_gpu_driver(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d581525df7acae6d794e8e2f740ecf615cf88b57ed6cae505a5ab63ede4d201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installGpuDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceOwners")
    def instance_owners(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceOwners"))

    @instance_owners.setter
    def instance_owners(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4fb8d7e9763c02a5bca03741a83ec2c7ddcc60854a3cee6617fd9a579e9122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceOwners", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6395ba02b1cd90eb7cbdef2d9c99364d28e9b46ce9fdef0eaa0e7d161abf6057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1867ed2316add0c53d2b5857f8efe37319bc802da1d1d6e8e6f4ebcab2d4e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a325f21a2db8045730d72e9ac72c62f19035419adaeea4d0612a25e8a0a59f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2651c8ec8344464f967962a3f414ee1d723a05702422101acaafcfb4ca1d3d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3304d6f6167e43df491b7992e34951e0ebe3dbc5529ea26a3f1e9988994402f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e63e63efc6d126868e7417fe98b3106e78b60642536cb5f35b363f44a16e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca56a5e8ea9615a49d9d3f99b4a2f102d2aba786a4bf23a4a8bb01a8029d309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nicType")
    def nic_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nicType"))

    @nic_type.setter
    def nic_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a59e1a0fe8e2019566987bbbf920719ae12ea2cac4d0d194c0b91a48208532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nicType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noProxyAccess")
    def no_proxy_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noProxyAccess"))

    @no_proxy_access.setter
    def no_proxy_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5dbbab8b6cca98f2b34ecebcbd51fc5951de4da02ef4924f4a0c7a09b13508b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noProxyAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noPublicIp")
    def no_public_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noPublicIp"))

    @no_public_ip.setter
    def no_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230dea74d001145854118570c1bc6d02e71a4636f4c28e9d01490c3edb6edd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPublicIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noRemoveDataDisk")
    def no_remove_data_disk(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noRemoveDataDisk"))

    @no_remove_data_disk.setter
    def no_remove_data_disk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41affe514ae26af19fcb02ab128586af0117989823f469d959f680947706a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noRemoveDataDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postStartupScript")
    def post_startup_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postStartupScript"))

    @post_startup_script.setter
    def post_startup_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8faea7dad76fc4e81f8debab27005c9e22d345e72cda0af4796e55260f8f4768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postStartupScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971ed16cc9bcee65a5d4baf9041fd584fbf1b44749874d74a54145b8b03e0da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04c254a74f556f0563d68b0121414669fbf08dd366d0d9867e4115c17d5b2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccountScopes")
    def service_account_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAccountScopes"))

    @service_account_scopes.setter
    def service_account_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63718a073d4da0a88dd46ee84b6e00543a24b782ffff618ae6d6897856f278e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323533e84cc68d0cc72e85d7a09531223f32dd8b4a9f4fac9fa236bf82cb8a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d79b972eac37ce03ebb2ba5b7e6e9e788f6dd2b3e5ec53ed73cdd7b4984b02f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @update_time.setter
    def update_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d8fdc64bcca088e89a2514958f31b4f5c8435e80f53d1f43618c2762f79a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateTime", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceAcceleratorConfig",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "type": "type"},
)
class NotebooksInstanceAcceleratorConfig:
    def __init__(self, *, core_count: jsii.Number, type: builtins.str) -> None:
        '''
        :param core_count: Count of cores of this accelerator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#core_count NotebooksInstance#core_count}
        :param type: Type of this accelerator. Possible values: ["ACCELERATOR_TYPE_UNSPECIFIED", "NVIDIA_TESLA_K80", "NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS", "NVIDIA_TESLA_A100", "TPU_V2", "TPU_V3"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#type NotebooksInstance#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7872f67ecccb32d44738ebbaa201e3198e98bc0089148b12d16b53c1a932a136)
            check_type(argname="argument core_count", value=core_count, expected_type=type_hints["core_count"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_count": core_count,
            "type": type,
        }

    @builtins.property
    def core_count(self) -> jsii.Number:
        '''Count of cores of this accelerator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#core_count NotebooksInstance#core_count}
        '''
        result = self._values.get("core_count")
        assert result is not None, "Required property 'core_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of this accelerator. Possible values: ["ACCELERATOR_TYPE_UNSPECIFIED", "NVIDIA_TESLA_K80", "NVIDIA_TESLA_P100", "NVIDIA_TESLA_V100", "NVIDIA_TESLA_P4", "NVIDIA_TESLA_T4", "NVIDIA_TESLA_T4_VWS", "NVIDIA_TESLA_P100_VWS", "NVIDIA_TESLA_P4_VWS", "NVIDIA_TESLA_A100", "TPU_V2", "TPU_V3"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#type NotebooksInstance#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceAcceleratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceAcceleratorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceAcceleratorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e00a8c9dd989682ef5461935147bf2e5538bf4ea89af78735c825ab88ad96760)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="coreCountInput")
    def core_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coreCountInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="coreCount")
    def core_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coreCount"))

    @core_count.setter
    def core_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608c13eaddd04195972da06efafe23e9b5f33fb38e4ac6170bd9b895fd819adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7cb08719e07e635aa4485fe69be15723f0c30ef1fe83716342490c5b7053f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksInstanceAcceleratorConfig]:
        return typing.cast(typing.Optional[NotebooksInstanceAcceleratorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksInstanceAcceleratorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76948b0d54ba8b7aaaa31a627de98ccfbfdc439d5b974336c4673ee9b421f5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceConfig",
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
        "machine_type": "machineType",
        "name": "name",
        "accelerator_config": "acceleratorConfig",
        "boot_disk_size_gb": "bootDiskSizeGb",
        "boot_disk_type": "bootDiskType",
        "container_image": "containerImage",
        "create_time": "createTime",
        "custom_gpu_driver_path": "customGpuDriverPath",
        "data_disk_size_gb": "dataDiskSizeGb",
        "data_disk_type": "dataDiskType",
        "desired_state": "desiredState",
        "disk_encryption": "diskEncryption",
        "id": "id",
        "install_gpu_driver": "installGpuDriver",
        "instance_owners": "instanceOwners",
        "kms_key": "kmsKey",
        "labels": "labels",
        "metadata": "metadata",
        "network": "network",
        "nic_type": "nicType",
        "no_proxy_access": "noProxyAccess",
        "no_public_ip": "noPublicIp",
        "no_remove_data_disk": "noRemoveDataDisk",
        "post_startup_script": "postStartupScript",
        "project": "project",
        "reservation_affinity": "reservationAffinity",
        "service_account": "serviceAccount",
        "service_account_scopes": "serviceAccountScopes",
        "shielded_instance_config": "shieldedInstanceConfig",
        "subnet": "subnet",
        "tags": "tags",
        "timeouts": "timeouts",
        "update_time": "updateTime",
        "vm_image": "vmImage",
    },
)
class NotebooksInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        machine_type: builtins.str,
        name: builtins.str,
        accelerator_config: typing.Optional[typing.Union[NotebooksInstanceAcceleratorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        boot_disk_size_gb: typing.Optional[jsii.Number] = None,
        boot_disk_type: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[typing.Union["NotebooksInstanceContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        create_time: typing.Optional[builtins.str] = None,
        custom_gpu_driver_path: typing.Optional[builtins.str] = None,
        data_disk_size_gb: typing.Optional[jsii.Number] = None,
        data_disk_type: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        disk_encryption: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        nic_type: typing.Optional[builtins.str] = None,
        no_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_remove_data_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        post_startup_script: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        reservation_affinity: typing.Optional[typing.Union["NotebooksInstanceReservationAffinity", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        shielded_instance_config: typing.Optional[typing.Union["NotebooksInstanceShieldedInstanceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        subnet: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["NotebooksInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        update_time: typing.Optional[builtins.str] = None,
        vm_image: typing.Optional[typing.Union["NotebooksInstanceVmImage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: A reference to the zone where the machine resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#location NotebooksInstance#location}
        :param machine_type: A reference to a machine type which defines VM kind. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#machine_type NotebooksInstance#machine_type}
        :param name: The name specified for the Notebook instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#name NotebooksInstance#name}
        :param accelerator_config: accelerator_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#accelerator_config NotebooksInstance#accelerator_config}
        :param boot_disk_size_gb: The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). The minimum recommended value is 100 GB. If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_size_gb NotebooksInstance#boot_disk_size_gb}
        :param boot_disk_type: Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_type NotebooksInstance#boot_disk_type}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#container_image NotebooksInstance#container_image}
        :param create_time: Instance creation time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create_time NotebooksInstance#create_time}
        :param custom_gpu_driver_path: Specify a custom Cloud Storage path where the GPU driver is stored. If not specified, we'll automatically choose from official GPU drivers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#custom_gpu_driver_path NotebooksInstance#custom_gpu_driver_path}
        :param data_disk_size_gb: The size of the data disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB). You can choose the size of the data disk based on how big your notebooks and data are. If not specified, this defaults to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_size_gb NotebooksInstance#data_disk_size_gb}
        :param data_disk_type: Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_type NotebooksInstance#data_disk_type}
        :param desired_state: Desired state of the Notebook Instance. Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#desired_state NotebooksInstance#desired_state}
        :param disk_encryption: Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["DISK_ENCRYPTION_UNSPECIFIED", "GMEK", "CMEK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#disk_encryption NotebooksInstance#disk_encryption}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#id NotebooksInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param install_gpu_driver: Whether the end user authorizes Google Cloud to install GPU driver on this instance. If this field is empty or set to false, the GPU driver won't be installed. Only applicable to instances with GPUs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#install_gpu_driver NotebooksInstance#install_gpu_driver}
        :param instance_owners: The list of owners of this instance after creation. Format: alias@example.com. Currently supports one owner only. If not specified, all of the service account users of your VM instance's service account can use the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#instance_owners NotebooksInstance#instance_owners}
        :param kms_key: The KMS key used to encrypt the disks, only applicable if diskEncryption is CMEK. Format: projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#kms_key NotebooksInstance#kms_key}
        :param labels: Labels to apply to this instance. These can be later modified by the setLabels method. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#labels NotebooksInstance#labels}
        :param metadata: Custom metadata to apply to this instance. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#metadata NotebooksInstance#metadata}
        :param network: The name of the VPC that this instance is in. Format: projects/{project_id}/global/networks/{network_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#network NotebooksInstance#network}
        :param nic_type: The type of vNIC driver. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#nic_type NotebooksInstance#nic_type}
        :param no_proxy_access: The notebook instance will not register with the proxy.. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_proxy_access NotebooksInstance#no_proxy_access}
        :param no_public_ip: No public IP will be assigned to this instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_public_ip NotebooksInstance#no_public_ip}
        :param no_remove_data_disk: If true, the data disk will not be auto deleted when deleting the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_remove_data_disk NotebooksInstance#no_remove_data_disk}
        :param post_startup_script: Path to a Bash script that automatically runs after a notebook instance fully boots up. The path must be a URL or Cloud Storage path (gs://path-to-file/file-name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#post_startup_script NotebooksInstance#post_startup_script}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}.
        :param reservation_affinity: reservation_affinity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#reservation_affinity NotebooksInstance#reservation_affinity}
        :param service_account: The service account on this instance, giving access to other Google Cloud services. You can use any service account within the same project, but you must have the service account user permission to use the instance. If not specified, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account NotebooksInstance#service_account}
        :param service_account_scopes: Optional. The URIs of service account scopes to be included in Compute Engine instances. If not specified, the following scopes are defined: - https://www.googleapis.com/auth/cloud-platform - https://www.googleapis.com/auth/userinfo.email Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account_scopes NotebooksInstance#service_account_scopes}
        :param shielded_instance_config: shielded_instance_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#shielded_instance_config NotebooksInstance#shielded_instance_config}
        :param subnet: The name of the subnet that this instance is in. Format: projects/{project_id}/regions/{region}/subnetworks/{subnetwork_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#subnet NotebooksInstance#subnet}
        :param tags: The Compute Engine tags to add to instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tags NotebooksInstance#tags}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#timeouts NotebooksInstance#timeouts}
        :param update_time: Instance update time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update_time NotebooksInstance#update_time}
        :param vm_image: vm_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#vm_image NotebooksInstance#vm_image}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(accelerator_config, dict):
            accelerator_config = NotebooksInstanceAcceleratorConfig(**accelerator_config)
        if isinstance(container_image, dict):
            container_image = NotebooksInstanceContainerImage(**container_image)
        if isinstance(reservation_affinity, dict):
            reservation_affinity = NotebooksInstanceReservationAffinity(**reservation_affinity)
        if isinstance(shielded_instance_config, dict):
            shielded_instance_config = NotebooksInstanceShieldedInstanceConfig(**shielded_instance_config)
        if isinstance(timeouts, dict):
            timeouts = NotebooksInstanceTimeouts(**timeouts)
        if isinstance(vm_image, dict):
            vm_image = NotebooksInstanceVmImage(**vm_image)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc793eca9b18680ed47a42ae841980f526aae72dbf3af16315d170168cad64f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument accelerator_config", value=accelerator_config, expected_type=type_hints["accelerator_config"])
            check_type(argname="argument boot_disk_size_gb", value=boot_disk_size_gb, expected_type=type_hints["boot_disk_size_gb"])
            check_type(argname="argument boot_disk_type", value=boot_disk_type, expected_type=type_hints["boot_disk_type"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument create_time", value=create_time, expected_type=type_hints["create_time"])
            check_type(argname="argument custom_gpu_driver_path", value=custom_gpu_driver_path, expected_type=type_hints["custom_gpu_driver_path"])
            check_type(argname="argument data_disk_size_gb", value=data_disk_size_gb, expected_type=type_hints["data_disk_size_gb"])
            check_type(argname="argument data_disk_type", value=data_disk_type, expected_type=type_hints["data_disk_type"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument disk_encryption", value=disk_encryption, expected_type=type_hints["disk_encryption"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument install_gpu_driver", value=install_gpu_driver, expected_type=type_hints["install_gpu_driver"])
            check_type(argname="argument instance_owners", value=instance_owners, expected_type=type_hints["instance_owners"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument nic_type", value=nic_type, expected_type=type_hints["nic_type"])
            check_type(argname="argument no_proxy_access", value=no_proxy_access, expected_type=type_hints["no_proxy_access"])
            check_type(argname="argument no_public_ip", value=no_public_ip, expected_type=type_hints["no_public_ip"])
            check_type(argname="argument no_remove_data_disk", value=no_remove_data_disk, expected_type=type_hints["no_remove_data_disk"])
            check_type(argname="argument post_startup_script", value=post_startup_script, expected_type=type_hints["post_startup_script"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reservation_affinity", value=reservation_affinity, expected_type=type_hints["reservation_affinity"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_account_scopes", value=service_account_scopes, expected_type=type_hints["service_account_scopes"])
            check_type(argname="argument shielded_instance_config", value=shielded_instance_config, expected_type=type_hints["shielded_instance_config"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument update_time", value=update_time, expected_type=type_hints["update_time"])
            check_type(argname="argument vm_image", value=vm_image, expected_type=type_hints["vm_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "machine_type": machine_type,
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
        if accelerator_config is not None:
            self._values["accelerator_config"] = accelerator_config
        if boot_disk_size_gb is not None:
            self._values["boot_disk_size_gb"] = boot_disk_size_gb
        if boot_disk_type is not None:
            self._values["boot_disk_type"] = boot_disk_type
        if container_image is not None:
            self._values["container_image"] = container_image
        if create_time is not None:
            self._values["create_time"] = create_time
        if custom_gpu_driver_path is not None:
            self._values["custom_gpu_driver_path"] = custom_gpu_driver_path
        if data_disk_size_gb is not None:
            self._values["data_disk_size_gb"] = data_disk_size_gb
        if data_disk_type is not None:
            self._values["data_disk_type"] = data_disk_type
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if disk_encryption is not None:
            self._values["disk_encryption"] = disk_encryption
        if id is not None:
            self._values["id"] = id
        if install_gpu_driver is not None:
            self._values["install_gpu_driver"] = install_gpu_driver
        if instance_owners is not None:
            self._values["instance_owners"] = instance_owners
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if labels is not None:
            self._values["labels"] = labels
        if metadata is not None:
            self._values["metadata"] = metadata
        if network is not None:
            self._values["network"] = network
        if nic_type is not None:
            self._values["nic_type"] = nic_type
        if no_proxy_access is not None:
            self._values["no_proxy_access"] = no_proxy_access
        if no_public_ip is not None:
            self._values["no_public_ip"] = no_public_ip
        if no_remove_data_disk is not None:
            self._values["no_remove_data_disk"] = no_remove_data_disk
        if post_startup_script is not None:
            self._values["post_startup_script"] = post_startup_script
        if project is not None:
            self._values["project"] = project
        if reservation_affinity is not None:
            self._values["reservation_affinity"] = reservation_affinity
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_account_scopes is not None:
            self._values["service_account_scopes"] = service_account_scopes
        if shielded_instance_config is not None:
            self._values["shielded_instance_config"] = shielded_instance_config
        if subnet is not None:
            self._values["subnet"] = subnet
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if update_time is not None:
            self._values["update_time"] = update_time
        if vm_image is not None:
            self._values["vm_image"] = vm_image

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
        '''A reference to the zone where the machine resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#location NotebooksInstance#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def machine_type(self) -> builtins.str:
        '''A reference to a machine type which defines VM kind.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#machine_type NotebooksInstance#machine_type}
        '''
        result = self._values.get("machine_type")
        assert result is not None, "Required property 'machine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name specified for the Notebook instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#name NotebooksInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def accelerator_config(self) -> typing.Optional[NotebooksInstanceAcceleratorConfig]:
        '''accelerator_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#accelerator_config NotebooksInstance#accelerator_config}
        '''
        result = self._values.get("accelerator_config")
        return typing.cast(typing.Optional[NotebooksInstanceAcceleratorConfig], result)

    @builtins.property
    def boot_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the boot disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB).

        The minimum recommended value is 100 GB.
        If not specified, this defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_size_gb NotebooksInstance#boot_disk_size_gb}
        '''
        result = self._values.get("boot_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def boot_disk_type(self) -> typing.Optional[builtins.str]:
        '''Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#boot_disk_type NotebooksInstance#boot_disk_type}
        '''
        result = self._values.get("boot_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional["NotebooksInstanceContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#container_image NotebooksInstance#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["NotebooksInstanceContainerImage"], result)

    @builtins.property
    def create_time(self) -> typing.Optional[builtins.str]:
        '''Instance creation time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create_time NotebooksInstance#create_time}
        '''
        result = self._values.get("create_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_gpu_driver_path(self) -> typing.Optional[builtins.str]:
        '''Specify a custom Cloud Storage path where the GPU driver is stored.

        If not specified, we'll automatically choose from official GPU drivers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#custom_gpu_driver_path NotebooksInstance#custom_gpu_driver_path}
        '''
        result = self._values.get("custom_gpu_driver_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the data disk in GB attached to this instance, up to a maximum of 64000 GB (64 TB).

        You can choose the size of the data disk based on how big your notebooks and data are.
        If not specified, this defaults to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_size_gb NotebooksInstance#data_disk_size_gb}
        '''
        result = self._values.get("data_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_disk_type(self) -> typing.Optional[builtins.str]:
        '''Possible disk types for notebook instances. Possible values: ["DISK_TYPE_UNSPECIFIED", "PD_STANDARD", "PD_SSD", "PD_BALANCED", "PD_EXTREME"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#data_disk_type NotebooksInstance#data_disk_type}
        '''
        result = self._values.get("data_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Notebook Instance.

        Set this field to 'ACTIVE' to start the Instance, and 'STOPPED' to stop the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#desired_state NotebooksInstance#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption(self) -> typing.Optional[builtins.str]:
        '''Disk encryption method used on the boot and data disks, defaults to GMEK. Possible values: ["DISK_ENCRYPTION_UNSPECIFIED", "GMEK", "CMEK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#disk_encryption NotebooksInstance#disk_encryption}
        '''
        result = self._values.get("disk_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#id NotebooksInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_gpu_driver(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the end user authorizes Google Cloud to install GPU driver on this instance.

        If this field is empty or set to false, the GPU driver
        won't be installed. Only applicable to instances with GPUs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#install_gpu_driver NotebooksInstance#install_gpu_driver}
        '''
        result = self._values.get("install_gpu_driver")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def instance_owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of owners of this instance after creation.

        Format: alias@example.com.
        Currently supports one owner only.
        If not specified, all of the service account users of
        your VM instance's service account can use the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#instance_owners NotebooksInstance#instance_owners}
        '''
        result = self._values.get("instance_owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used to encrypt the disks, only applicable if diskEncryption is CMEK. Format: projects/{project_id}/locations/{location}/keyRings/{key_ring_id}/cryptoKeys/{key_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#kms_key NotebooksInstance#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this instance.

        These can be later modified by the setLabels method.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#labels NotebooksInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def metadata(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom metadata to apply to this instance.

        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#metadata NotebooksInstance#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC that this instance is in. Format: projects/{project_id}/global/networks/{network_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#network NotebooksInstance#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nic_type(self) -> typing.Optional[builtins.str]:
        '''The type of vNIC driver. Possible values: ["UNSPECIFIED_NIC_TYPE", "VIRTIO_NET", "GVNIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#nic_type NotebooksInstance#nic_type}
        '''
        result = self._values.get("nic_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_proxy_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The notebook instance will not register with the proxy..

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_proxy_access NotebooksInstance#no_proxy_access}
        '''
        result = self._values.get("no_proxy_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''No public IP will be assigned to this instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_public_ip NotebooksInstance#no_public_ip}
        '''
        result = self._values.get("no_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_remove_data_disk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the data disk will not be auto deleted when deleting the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#no_remove_data_disk NotebooksInstance#no_remove_data_disk}
        '''
        result = self._values.get("no_remove_data_disk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def post_startup_script(self) -> typing.Optional[builtins.str]:
        '''Path to a Bash script that automatically runs after a notebook instance fully boots up.

        The path must be a URL
        or Cloud Storage path (gs://path-to-file/file-name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#post_startup_script NotebooksInstance#post_startup_script}
        '''
        result = self._values.get("post_startup_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reservation_affinity(
        self,
    ) -> typing.Optional["NotebooksInstanceReservationAffinity"]:
        '''reservation_affinity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#reservation_affinity NotebooksInstance#reservation_affinity}
        '''
        result = self._values.get("reservation_affinity")
        return typing.cast(typing.Optional["NotebooksInstanceReservationAffinity"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The service account on this instance, giving access to other Google Cloud services.

        You can use any service account within
        the same project, but you must have the service account user
        permission to use the instance. If not specified,
        the Compute Engine default service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account NotebooksInstance#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The URIs of service account scopes to be included in Compute Engine instances.
        If not specified, the following scopes are defined:

        - https://www.googleapis.com/auth/cloud-platform
        - https://www.googleapis.com/auth/userinfo.email

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#service_account_scopes NotebooksInstance#service_account_scopes}
        '''
        result = self._values.get("service_account_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shielded_instance_config(
        self,
    ) -> typing.Optional["NotebooksInstanceShieldedInstanceConfig"]:
        '''shielded_instance_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#shielded_instance_config NotebooksInstance#shielded_instance_config}
        '''
        result = self._values.get("shielded_instance_config")
        return typing.cast(typing.Optional["NotebooksInstanceShieldedInstanceConfig"], result)

    @builtins.property
    def subnet(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet that this instance is in. Format: projects/{project_id}/regions/{region}/subnetworks/{subnetwork_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#subnet NotebooksInstance#subnet}
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Compute Engine tags to add to instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tags NotebooksInstance#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NotebooksInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#timeouts NotebooksInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NotebooksInstanceTimeouts"], result)

    @builtins.property
    def update_time(self) -> typing.Optional[builtins.str]:
        '''Instance update time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update_time NotebooksInstance#update_time}
        '''
        result = self._values.get("update_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vm_image(self) -> typing.Optional["NotebooksInstanceVmImage"]:
        '''vm_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#vm_image NotebooksInstance#vm_image}
        '''
        result = self._values.get("vm_image")
        return typing.cast(typing.Optional["NotebooksInstanceVmImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceContainerImage",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository", "tag": "tag"},
)
class NotebooksInstanceContainerImage:
    def __init__(
        self,
        *,
        repository: builtins.str,
        tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository: The path to the container image repository. For example: gcr.io/{project_id}/{imageName}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#repository NotebooksInstance#repository}
        :param tag: The tag of the container image. If not specified, this defaults to the latest tag. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tag NotebooksInstance#tag}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbd506d98625c0a5ac6d2db4e1e05d54f4e2e50bb3942c9b1e40ab78fc84d72)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if tag is not None:
            self._values["tag"] = tag

    @builtins.property
    def repository(self) -> builtins.str:
        '''The path to the container image repository. For example: gcr.io/{project_id}/{imageName}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#repository NotebooksInstance#repository}
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag of the container image. If not specified, this defaults to the latest tag.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#tag NotebooksInstance#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96621c0f67e01ae600caa87d296857a9c3d04b994f427e4d931f960b425c93fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd657cb5920746031ddc75b640c71594f5fca5e3af3cac073b611dae2107effb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3625022acf06a5e688aada638fe494f4d83141266a25433e829f83a54451e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksInstanceContainerImage]:
        return typing.cast(typing.Optional[NotebooksInstanceContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksInstanceContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46de5fb3cc2552c6314b636c0f6bbe878da097bf463dfba855845b3e8744f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceReservationAffinity",
    jsii_struct_bases=[],
    name_mapping={
        "consume_reservation_type": "consumeReservationType",
        "key": "key",
        "values": "values",
    },
)
class NotebooksInstanceReservationAffinity:
    def __init__(
        self,
        *,
        consume_reservation_type: builtins.str,
        key: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param consume_reservation_type: The type of Compute Reservation. Possible values: ["NO_RESERVATION", "ANY_RESERVATION", "SPECIFIC_RESERVATION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#consume_reservation_type NotebooksInstance#consume_reservation_type}
        :param key: Corresponds to the label key of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#key NotebooksInstance#key}
        :param values: Corresponds to the label values of reservation resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#values NotebooksInstance#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02ad466da57492f1b9195991bfb6338a91174179fbc42e24c83fa9e64b240f7)
            check_type(argname="argument consume_reservation_type", value=consume_reservation_type, expected_type=type_hints["consume_reservation_type"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consume_reservation_type": consume_reservation_type,
        }
        if key is not None:
            self._values["key"] = key
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def consume_reservation_type(self) -> builtins.str:
        '''The type of Compute Reservation. Possible values: ["NO_RESERVATION", "ANY_RESERVATION", "SPECIFIC_RESERVATION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#consume_reservation_type NotebooksInstance#consume_reservation_type}
        '''
        result = self._values.get("consume_reservation_type")
        assert result is not None, "Required property 'consume_reservation_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Corresponds to the label key of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#key NotebooksInstance#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Corresponds to the label values of reservation resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#values NotebooksInstance#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceReservationAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceReservationAffinityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceReservationAffinityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81da3f351213314a0f0cc1839ba6c63767e360869dae7b1689cbdf9cbecbc714)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationTypeInput")
    def consume_reservation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumeReservationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="consumeReservationType")
    def consume_reservation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumeReservationType"))

    @consume_reservation_type.setter
    def consume_reservation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db68306c6bb8f134159b1449c23fafdebef05bc248f0b651efa94eea3100458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumeReservationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c193a436d40415d69f42354460cfff7ae110845b61681a5e89ccdb5ec156fd2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69639293dff3c525c9a47aff8fc3b5ddd161aa0d0149c7e95e8f2d497c50fb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksInstanceReservationAffinity]:
        return typing.cast(typing.Optional[NotebooksInstanceReservationAffinity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksInstanceReservationAffinity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07553d6b86587716c3bafddab7d563edc47af2397b871ae3d405c8fa8030889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceShieldedInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_integrity_monitoring": "enableIntegrityMonitoring",
        "enable_secure_boot": "enableSecureBoot",
        "enable_vtpm": "enableVtpm",
    },
)
class NotebooksInstanceShieldedInstanceConfig:
    def __init__(
        self,
        *,
        enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_integrity_monitoring: Defines whether the instance has integrity monitoring enabled. Enables monitoring and attestation of the boot integrity of the instance. The attestation is performed against the integrity policy baseline. This baseline is initially derived from the implicitly trusted boot image when the instance is created. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_integrity_monitoring NotebooksInstance#enable_integrity_monitoring}
        :param enable_secure_boot: Defines whether the instance has Secure Boot enabled. Secure Boot helps ensure that the system only runs authentic software by verifying the digital signature of all boot components, and halting the boot process if signature verification fails. Disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_secure_boot NotebooksInstance#enable_secure_boot}
        :param enable_vtpm: Defines whether the instance has the vTPM enabled. Enabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_vtpm NotebooksInstance#enable_vtpm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d040454a3429f621ca665842415402ce2871814c07474a403d9f02a275be3ca2)
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
        '''Defines whether the instance has integrity monitoring enabled.

        Enables monitoring and attestation of the
        boot integrity of the instance. The attestation is performed against the integrity policy baseline.
        This baseline is initially derived from the implicitly trusted boot image when the instance is created.
        Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_integrity_monitoring NotebooksInstance#enable_integrity_monitoring}
        '''
        result = self._values.get("enable_integrity_monitoring")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_secure_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has Secure Boot enabled.

        Secure Boot helps ensure that the system only runs
        authentic software by verifying the digital signature of all boot components, and halting the boot process
        if signature verification fails.
        Disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_secure_boot NotebooksInstance#enable_secure_boot}
        '''
        result = self._values.get("enable_secure_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_vtpm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defines whether the instance has the vTPM enabled. Enabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#enable_vtpm NotebooksInstance#enable_vtpm}
        '''
        result = self._values.get("enable_vtpm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceShieldedInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceShieldedInstanceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceShieldedInstanceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb46849f3d6284767ace7f67dae767620158efcf164c7f289f9cf8636cbea93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d7863d9677f6e5d818c8f65a54029a56fad0c0e22e2c4f96ec73c1ec634d49a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fabb8808c3c8432216733ea228169446cb0f4f695bb64e720593e259ffe4177)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2c750ad92ccf3c1a8bf89237294fb6dd4fc480bb5f3395a02259f1b5f7f969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableVtpm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NotebooksInstanceShieldedInstanceConfig]:
        return typing.cast(typing.Optional[NotebooksInstanceShieldedInstanceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NotebooksInstanceShieldedInstanceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788b949837daeacea6047a6364de6b458699c36df80c832a1f649340dd1208c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NotebooksInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create NotebooksInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#delete NotebooksInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update NotebooksInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2326dc0d93f118955c3f2a3c82bfa7a4ad1c833053a4e1a345fe762bf48e2e7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#create NotebooksInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#delete NotebooksInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#update NotebooksInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9861f89603d82cef355081a89798633fee03f427a345063080beb1242785c90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdf938030a7a126f6e27b0253043f7845457f0d278176b7d6941c7955d924d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719ba265f6717540c8dea8f41b600b773c9a6cf1f52321d340aa2f1d590201ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70bfd1fe8313dd105b3be064dd58ae5d37b674a8f13dd62661a5162300f2758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb92fca755655e7626a7e78d1392b792e93899560df587cce581a83581176400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceVmImage",
    jsii_struct_bases=[],
    name_mapping={
        "project": "project",
        "image_family": "imageFamily",
        "image_name": "imageName",
    },
)
class NotebooksInstanceVmImage:
    def __init__(
        self,
        *,
        project: builtins.str,
        image_family: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: The name of the Google Cloud project that this VM image belongs to. Format: projects/{project_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}
        :param image_family: Use this VM image family to find the image; the newest image in this family will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_family NotebooksInstance#image_family}
        :param image_name: Use VM image name to find the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_name NotebooksInstance#image_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba5275d4b28d0e99aa185ec13ea1a6657cdd23ee0dc4678eac357c6178e56b5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument image_family", value=image_family, expected_type=type_hints["image_family"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project": project,
        }
        if image_family is not None:
            self._values["image_family"] = image_family
        if image_name is not None:
            self._values["image_name"] = image_name

    @builtins.property
    def project(self) -> builtins.str:
        '''The name of the Google Cloud project that this VM image belongs to. Format: projects/{project_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#project NotebooksInstance#project}
        '''
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_family(self) -> typing.Optional[builtins.str]:
        '''Use this VM image family to find the image; the newest image in this family will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_family NotebooksInstance#image_family}
        '''
        result = self._values.get("image_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''Use VM image name to find the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/notebooks_instance#image_name NotebooksInstance#image_name}
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotebooksInstanceVmImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NotebooksInstanceVmImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.notebooksInstance.NotebooksInstanceVmImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c364c5b41d35971205bf4ed8ba55271dc57b111a93e57375013f32c170f1bf8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImageFamily")
    def reset_image_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageFamily", []))

    @jsii.member(jsii_name="resetImageName")
    def reset_image_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageName", []))

    @builtins.property
    @jsii.member(jsii_name="imageFamilyInput")
    def image_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="imageFamily")
    def image_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageFamily"))

    @image_family.setter
    def image_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c13aa18fa383b178d9d3d68c2ed5fa8786860d4fc72b862097dc04f50ea1327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageFamily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985a9aa82eba3acdfc72a7f9baee3092b63da2addcd890a37eaeb545f2982b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d740847e629b9cfe73453fa7960d63b0387c9a9222b4b730bb46cf5b0e082f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NotebooksInstanceVmImage]:
        return typing.cast(typing.Optional[NotebooksInstanceVmImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NotebooksInstanceVmImage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c684ab47c1ae784ab835ffa0e3ec66b8ccfb9ce3b3294233f0db3bfb1c67b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NotebooksInstance",
    "NotebooksInstanceAcceleratorConfig",
    "NotebooksInstanceAcceleratorConfigOutputReference",
    "NotebooksInstanceConfig",
    "NotebooksInstanceContainerImage",
    "NotebooksInstanceContainerImageOutputReference",
    "NotebooksInstanceReservationAffinity",
    "NotebooksInstanceReservationAffinityOutputReference",
    "NotebooksInstanceShieldedInstanceConfig",
    "NotebooksInstanceShieldedInstanceConfigOutputReference",
    "NotebooksInstanceTimeouts",
    "NotebooksInstanceTimeoutsOutputReference",
    "NotebooksInstanceVmImage",
    "NotebooksInstanceVmImageOutputReference",
]

publication.publish()

def _typecheckingstub__380dc868810684db7e40643563cfd009fd9af8b81fb377ea355e308dd8d51801(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    machine_type: builtins.str,
    name: builtins.str,
    accelerator_config: typing.Optional[typing.Union[NotebooksInstanceAcceleratorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[typing.Union[NotebooksInstanceContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    create_time: typing.Optional[builtins.str] = None,
    custom_gpu_driver_path: typing.Optional[builtins.str] = None,
    data_disk_size_gb: typing.Optional[jsii.Number] = None,
    data_disk_type: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    disk_encryption: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    no_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_remove_data_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    post_startup_script: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[NotebooksInstanceReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[NotebooksInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NotebooksInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_time: typing.Optional[builtins.str] = None,
    vm_image: typing.Optional[typing.Union[NotebooksInstanceVmImage, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f8b1227173ac2d367b13faf2984ea6b4043e35321f429e620f211bfbe7e8f7d2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabd6e29a0452e6e88c0790f8889cfdbcd54c2512fc8415af0c5399726c40bc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6984b672ef381761fca3fb8283baa6eeea0fa66450d6c040ada956af95d298e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b3531e69c33240ed5b804f701fea9fbf89c82213379d5e3ec03550ccf1fc12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef83a1f84372489101c179a907c600f2b957a800aa4c2fdc9bc9f10af16ff45a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0a3b16242c74f5a7f20b0209d804ec622910731039ad82826af3dfdd04db7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74560d0e0d5f6a6968d68c84d622f4bb54dc51f6fbe9247268f8f519247aaf08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80331c270dab5bbdba1b63a19a50a496bfeecff693cfee7c5d90096ebac730ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8319f19e0f25710d572e6e9258a03716265bfc14af2018082545c20740613892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066beaec18a3f52fef360fd77ae0514d9a7fa2c6dcdbde2112438aaf74872b33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d581525df7acae6d794e8e2f740ecf615cf88b57ed6cae505a5ab63ede4d201(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4fb8d7e9763c02a5bca03741a83ec2c7ddcc60854a3cee6617fd9a579e9122(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6395ba02b1cd90eb7cbdef2d9c99364d28e9b46ce9fdef0eaa0e7d161abf6057(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1867ed2316add0c53d2b5857f8efe37319bc802da1d1d6e8e6f4ebcab2d4e41(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a325f21a2db8045730d72e9ac72c62f19035419adaeea4d0612a25e8a0a59f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2651c8ec8344464f967962a3f414ee1d723a05702422101acaafcfb4ca1d3d3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3304d6f6167e43df491b7992e34951e0ebe3dbc5529ea26a3f1e9988994402f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e63e63efc6d126868e7417fe98b3106e78b60642536cb5f35b363f44a16e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca56a5e8ea9615a49d9d3f99b4a2f102d2aba786a4bf23a4a8bb01a8029d309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a59e1a0fe8e2019566987bbbf920719ae12ea2cac4d0d194c0b91a48208532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5dbbab8b6cca98f2b34ecebcbd51fc5951de4da02ef4924f4a0c7a09b13508b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230dea74d001145854118570c1bc6d02e71a4636f4c28e9d01490c3edb6edd9b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41affe514ae26af19fcb02ab128586af0117989823f469d959f680947706a46(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8faea7dad76fc4e81f8debab27005c9e22d345e72cda0af4796e55260f8f4768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971ed16cc9bcee65a5d4baf9041fd584fbf1b44749874d74a54145b8b03e0da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04c254a74f556f0563d68b0121414669fbf08dd366d0d9867e4115c17d5b2cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63718a073d4da0a88dd46ee84b6e00543a24b782ffff618ae6d6897856f278e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323533e84cc68d0cc72e85d7a09531223f32dd8b4a9f4fac9fa236bf82cb8a8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d79b972eac37ce03ebb2ba5b7e6e9e788f6dd2b3e5ec53ed73cdd7b4984b02f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d8fdc64bcca088e89a2514958f31b4f5c8435e80f53d1f43618c2762f79a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7872f67ecccb32d44738ebbaa201e3198e98bc0089148b12d16b53c1a932a136(
    *,
    core_count: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00a8c9dd989682ef5461935147bf2e5538bf4ea89af78735c825ab88ad96760(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608c13eaddd04195972da06efafe23e9b5f33fb38e4ac6170bd9b895fd819adf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7cb08719e07e635aa4485fe69be15723f0c30ef1fe83716342490c5b7053f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76948b0d54ba8b7aaaa31a627de98ccfbfdc439d5b974336c4673ee9b421f5c7(
    value: typing.Optional[NotebooksInstanceAcceleratorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc793eca9b18680ed47a42ae841980f526aae72dbf3af16315d170168cad64f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    machine_type: builtins.str,
    name: builtins.str,
    accelerator_config: typing.Optional[typing.Union[NotebooksInstanceAcceleratorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    boot_disk_size_gb: typing.Optional[jsii.Number] = None,
    boot_disk_type: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[typing.Union[NotebooksInstanceContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    create_time: typing.Optional[builtins.str] = None,
    custom_gpu_driver_path: typing.Optional[builtins.str] = None,
    data_disk_size_gb: typing.Optional[jsii.Number] = None,
    data_disk_type: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    disk_encryption: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    install_gpu_driver: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    instance_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    nic_type: typing.Optional[builtins.str] = None,
    no_proxy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_remove_data_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    post_startup_script: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    reservation_affinity: typing.Optional[typing.Union[NotebooksInstanceReservationAffinity, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_account_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    shielded_instance_config: typing.Optional[typing.Union[NotebooksInstanceShieldedInstanceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    subnet: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[NotebooksInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    update_time: typing.Optional[builtins.str] = None,
    vm_image: typing.Optional[typing.Union[NotebooksInstanceVmImage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbd506d98625c0a5ac6d2db4e1e05d54f4e2e50bb3942c9b1e40ab78fc84d72(
    *,
    repository: builtins.str,
    tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96621c0f67e01ae600caa87d296857a9c3d04b994f427e4d931f960b425c93fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd657cb5920746031ddc75b640c71594f5fca5e3af3cac073b611dae2107effb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3625022acf06a5e688aada638fe494f4d83141266a25433e829f83a54451e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46de5fb3cc2552c6314b636c0f6bbe878da097bf463dfba855845b3e8744f72(
    value: typing.Optional[NotebooksInstanceContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02ad466da57492f1b9195991bfb6338a91174179fbc42e24c83fa9e64b240f7(
    *,
    consume_reservation_type: builtins.str,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81da3f351213314a0f0cc1839ba6c63767e360869dae7b1689cbdf9cbecbc714(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db68306c6bb8f134159b1449c23fafdebef05bc248f0b651efa94eea3100458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c193a436d40415d69f42354460cfff7ae110845b61681a5e89ccdb5ec156fd2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69639293dff3c525c9a47aff8fc3b5ddd161aa0d0149c7e95e8f2d497c50fb58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07553d6b86587716c3bafddab7d563edc47af2397b871ae3d405c8fa8030889(
    value: typing.Optional[NotebooksInstanceReservationAffinity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d040454a3429f621ca665842415402ce2871814c07474a403d9f02a275be3ca2(
    *,
    enable_integrity_monitoring: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_secure_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_vtpm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb46849f3d6284767ace7f67dae767620158efcf164c7f289f9cf8636cbea93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7863d9677f6e5d818c8f65a54029a56fad0c0e22e2c4f96ec73c1ec634d49a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fabb8808c3c8432216733ea228169446cb0f4f695bb64e720593e259ffe4177(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c750ad92ccf3c1a8bf89237294fb6dd4fc480bb5f3395a02259f1b5f7f969f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788b949837daeacea6047a6364de6b458699c36df80c832a1f649340dd1208c7(
    value: typing.Optional[NotebooksInstanceShieldedInstanceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2326dc0d93f118955c3f2a3c82bfa7a4ad1c833053a4e1a345fe762bf48e2e7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9861f89603d82cef355081a89798633fee03f427a345063080beb1242785c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf938030a7a126f6e27b0253043f7845457f0d278176b7d6941c7955d924d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719ba265f6717540c8dea8f41b600b773c9a6cf1f52321d340aa2f1d590201ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70bfd1fe8313dd105b3be064dd58ae5d37b674a8f13dd62661a5162300f2758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb92fca755655e7626a7e78d1392b792e93899560df587cce581a83581176400(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NotebooksInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba5275d4b28d0e99aa185ec13ea1a6657cdd23ee0dc4678eac357c6178e56b5(
    *,
    project: builtins.str,
    image_family: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c364c5b41d35971205bf4ed8ba55271dc57b111a93e57375013f32c170f1bf8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c13aa18fa383b178d9d3d68c2ed5fa8786860d4fc72b862097dc04f50ea1327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985a9aa82eba3acdfc72a7f9baee3092b63da2addcd890a37eaeb545f2982b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d740847e629b9cfe73453fa7960d63b0387c9a9222b4b730bb46cf5b0e082f95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c684ab47c1ae784ab835ffa0e3ec66b8ccfb9ce3b3294233f0db3bfb1c67b84(
    value: typing.Optional[NotebooksInstanceVmImage],
) -> None:
    """Type checking stubs"""
    pass

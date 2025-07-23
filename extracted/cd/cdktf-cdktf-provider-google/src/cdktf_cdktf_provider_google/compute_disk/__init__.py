r'''
# `google_compute_disk`

Refer to the Terraform Registry for docs: [`google_compute_disk`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk).
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


class ComputeDisk(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDisk",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk google_compute_disk}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        access_mode: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[builtins.str] = None,
        async_primary_disk: typing.Optional[typing.Union["ComputeDiskAsyncPrimaryDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        params: typing.Optional[typing.Union["ComputeDiskParams", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instant_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_storage_object: typing.Optional[builtins.str] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk google_compute_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#name ComputeDisk#name}
        :param access_mode: The access mode of the disk. For example: - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode. - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode. - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode. The AccessMode is only valid for Hyperdisk disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#access_mode ComputeDisk#access_mode}
        :param architecture: The architecture of the disk. Values include 'X86_64', 'ARM64'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#architecture ComputeDisk#architecture}
        :param async_primary_disk: async_primary_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#async_primary_disk ComputeDisk#async_primary_disk}
        :param create_snapshot_before_destroy: If set to true, a snapshot of the disk will be created before it is destroyed. If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation. The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy ComputeDisk#create_snapshot_before_destroy}
        :param create_snapshot_before_destroy_prefix: This will set a custom name prefix for the snapshot that's created when the disk is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy_prefix ComputeDisk#create_snapshot_before_destroy_prefix}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#description ComputeDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        :param enable_confidential_compute: Whether this disk is using confidential compute mode. Note: Only supported on hyperdisk skus, disk_encryption_key is required when setting to true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#enable_confidential_compute ComputeDisk#enable_confidential_compute}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#guest_os_features ComputeDisk#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#id ComputeDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: The image from which to initialize this disk. This can be one of: the image's 'self_link', 'projects/{project}/global/images/{image}', 'projects/{project}/global/images/family/{family}', 'global/images/{image}', 'global/images/family/{family}', 'family/{family}', '{project}/{family}', '{project}/{image}', '{family}', or '{image}'. If referred by family, the images names must include the family name. If they don't, use the `google_compute_image data source </docs/providers/google/d/compute_image.html>`_. For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'. These images can be referred by family name here. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#image ComputeDisk#image}
        :param labels: Labels to apply to this disk. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#labels ComputeDisk#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#licenses ComputeDisk#licenses}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#params ComputeDisk#params}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#project ComputeDisk#project}.
        :param provisioned_iops: Indicates how many IOPS must be provisioned for the disk. Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk allows for an update of IOPS every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        :param provisioned_throughput: Indicates how much Throughput must be provisioned for the disk. Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk allows for an update of Throughput every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_throughput ComputeDisk#provisioned_throughput}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the 'image' or 'snapshot' parameter, or specify it alone to create an empty persistent disk. If you specify this field along with 'image' or 'snapshot', the value must not be less than the size of the image or the size of the snapshot. ~>**NOTE** If you change the size, Terraform updates the disk size if upsizing is detected but recreates the disk if downsizing is requested. You can add 'lifecycle.prevent_destroy' in the config to prevent destroying and recreating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#size ComputeDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. If the snapshot is in another project than this disk, you must supply a full URL. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' - 'projects/project/global/snapshots/snapshot' - 'global/snapshots/snapshot' - 'snapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#snapshot ComputeDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} - https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} - projects/{project}/zones/{zone}/disks/{disk} - projects/{project}/regions/{region}/disks/{disk} - zones/{zone}/disks/{disk} - regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_disk ComputeDisk#source_disk}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        :param source_instant_snapshot: The source instant snapshot used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instantSnapshots/instantSnapshot' - 'projects/project/zones/zone/instantSnapshots/instantSnapshot' - 'zones/zone/instantSnapshots/instantSnapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_instant_snapshot ComputeDisk#source_instant_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        :param source_storage_object: The full Google Cloud Storage URI where the disk image is stored. This file must be a gzip-compressed tarball whose name ends in .tar.gz or virtual machine disk whose name ends in vmdk. Valid URIs may start with gs:// or https://storage.googleapis.com/. This flag is not optimized for creating multiple disks from a source storage object. To create many disks from a source storage object, use gcloud compute images import instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_storage_object ComputeDisk#source_storage_object}
        :param storage_pool: The URL or the name of the storage pool in which the new disk is created. For example: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/storagePools/{storagePool} - /projects/{project}/zones/{zone}/storagePools/{storagePool} - /zones/{zone}/storagePools/{storagePool} - /{storagePool} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#storage_pool ComputeDisk#storage_pool}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#timeouts ComputeDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#type ComputeDisk#type}
        :param zone: A reference to the zone where the disk resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#zone ComputeDisk#zone}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bfcff2e5a97a5b91ac8d6d70a38ea054bc83c0e8e09864edb474805c50de74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeDiskConfig(
            name=name,
            access_mode=access_mode,
            architecture=architecture,
            async_primary_disk=async_primary_disk,
            create_snapshot_before_destroy=create_snapshot_before_destroy,
            create_snapshot_before_destroy_prefix=create_snapshot_before_destroy_prefix,
            description=description,
            disk_encryption_key=disk_encryption_key,
            enable_confidential_compute=enable_confidential_compute,
            guest_os_features=guest_os_features,
            id=id,
            image=image,
            labels=labels,
            licenses=licenses,
            params=params,
            physical_block_size_bytes=physical_block_size_bytes,
            project=project,
            provisioned_iops=provisioned_iops,
            provisioned_throughput=provisioned_throughput,
            size=size,
            snapshot=snapshot,
            source_disk=source_disk,
            source_image_encryption_key=source_image_encryption_key,
            source_instant_snapshot=source_instant_snapshot,
            source_snapshot_encryption_key=source_snapshot_encryption_key,
            source_storage_object=source_storage_object,
            storage_pool=storage_pool,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a ComputeDisk resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeDisk to import.
        :param import_from_id: The id of the existing ComputeDisk that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeDisk to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7adc51219cf57c72979fc7abe5d167be8014c772677883cb9557a6999a6d1e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAsyncPrimaryDisk")
    def put_async_primary_disk(self, *, disk: builtins.str) -> None:
        '''
        :param disk: Primary disk for asynchronous disk replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk ComputeDisk#disk}
        '''
        value = ComputeDiskAsyncPrimaryDisk(disk=disk)

        return typing.cast(None, jsii.invoke(self, "putAsyncPrimaryDisk", [value]))

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#rsa_encrypted_key ComputeDisk#rsa_encrypted_key}
        '''
        value = ComputeDiskDiskEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putGuestOsFeatures")
    def put_guest_os_features(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51c7e11e72ee5afc069e0e871d4c9558c840915ef3db952e369adb5607836d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestOsFeatures", [value]))

    @jsii.member(jsii_name="putParams")
    def put_params(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the disk. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#resource_manager_tags ComputeDisk#resource_manager_tags}
        '''
        value = ComputeDiskParams(resource_manager_tags=resource_manager_tags)

        return typing.cast(None, jsii.invoke(self, "putParams", [value]))

    @jsii.member(jsii_name="putSourceImageEncryptionKey")
    def put_source_image_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        value = ComputeDiskSourceImageEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceImageEncryptionKey", [value]))

    @jsii.member(jsii_name="putSourceSnapshotEncryptionKey")
    def put_source_snapshot_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        value = ComputeDiskSourceSnapshotEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceSnapshotEncryptionKey", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create ComputeDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#delete ComputeDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#update ComputeDisk#update}.
        '''
        value = ComputeDiskTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessMode")
    def reset_access_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessMode", []))

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetAsyncPrimaryDisk")
    def reset_async_primary_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsyncPrimaryDisk", []))

    @jsii.member(jsii_name="resetCreateSnapshotBeforeDestroy")
    def reset_create_snapshot_before_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSnapshotBeforeDestroy", []))

    @jsii.member(jsii_name="resetCreateSnapshotBeforeDestroyPrefix")
    def reset_create_snapshot_before_destroy_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateSnapshotBeforeDestroyPrefix", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskEncryptionKey")
    def reset_disk_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionKey", []))

    @jsii.member(jsii_name="resetEnableConfidentialCompute")
    def reset_enable_confidential_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConfidentialCompute", []))

    @jsii.member(jsii_name="resetGuestOsFeatures")
    def reset_guest_os_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestOsFeatures", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLicenses")
    def reset_licenses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenses", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetPhysicalBlockSizeBytes")
    def reset_physical_block_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalBlockSizeBytes", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProvisionedIops")
    def reset_provisioned_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedIops", []))

    @jsii.member(jsii_name="resetProvisionedThroughput")
    def reset_provisioned_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvisionedThroughput", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetSourceDisk")
    def reset_source_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDisk", []))

    @jsii.member(jsii_name="resetSourceImageEncryptionKey")
    def reset_source_image_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceImageEncryptionKey", []))

    @jsii.member(jsii_name="resetSourceInstantSnapshot")
    def reset_source_instant_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceInstantSnapshot", []))

    @jsii.member(jsii_name="resetSourceSnapshotEncryptionKey")
    def reset_source_snapshot_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshotEncryptionKey", []))

    @jsii.member(jsii_name="resetSourceStorageObject")
    def reset_source_storage_object(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceStorageObject", []))

    @jsii.member(jsii_name="resetStoragePool")
    def reset_storage_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoragePool", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="asyncPrimaryDisk")
    def async_primary_disk(self) -> "ComputeDiskAsyncPrimaryDiskOutputReference":
        return typing.cast("ComputeDiskAsyncPrimaryDiskOutputReference", jsii.get(self, "asyncPrimaryDisk"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(self) -> "ComputeDiskDiskEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskDiskEncryptionKeyOutputReference", jsii.get(self, "diskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="diskId")
    def disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskId"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> "ComputeDiskGuestOsFeaturesList":
        return typing.cast("ComputeDiskGuestOsFeaturesList", jsii.get(self, "guestOsFeatures"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="lastAttachTimestamp")
    def last_attach_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastAttachTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="lastDetachTimestamp")
    def last_detach_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastDetachTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> "ComputeDiskParamsOutputReference":
        return typing.cast("ComputeDiskParamsOutputReference", jsii.get(self, "params"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskId")
    def source_disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDiskId"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeDiskSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageId")
    def source_image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImageId"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstantSnapshotId")
    def source_instant_snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstantSnapshotId"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeDiskSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeDiskSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotId")
    def source_snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshotId"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeDiskTimeoutsOutputReference":
        return typing.cast("ComputeDiskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="accessModeInput")
    def access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="asyncPrimaryDiskInput")
    def async_primary_disk_input(
        self,
    ) -> typing.Optional["ComputeDiskAsyncPrimaryDisk"]:
        return typing.cast(typing.Optional["ComputeDiskAsyncPrimaryDisk"], jsii.get(self, "asyncPrimaryDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="createSnapshotBeforeDestroyInput")
    def create_snapshot_before_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createSnapshotBeforeDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="createSnapshotBeforeDestroyPrefixInput")
    def create_snapshot_before_destroy_prefix_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createSnapshotBeforeDestroyPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKeyInput")
    def disk_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskDiskEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskDiskEncryptionKey"], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConfidentialComputeInput")
    def enable_confidential_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConfidentialComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeaturesInput")
    def guest_os_features_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeDiskGuestOsFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeDiskGuestOsFeatures"]]], jsii.get(self, "guestOsFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="licensesInput")
    def licenses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "licensesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(self) -> typing.Optional["ComputeDiskParams"]:
        return typing.cast(typing.Optional["ComputeDiskParams"], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalBlockSizeBytesInput")
    def physical_block_size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "physicalBlockSizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedIopsInput")
    def provisioned_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughputInput")
    def provisioned_throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "provisionedThroughputInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotInput")
    def snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskInput")
    def source_disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKeyInput")
    def source_image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInstantSnapshotInput")
    def source_instant_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInstantSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceStorageObjectInput")
    def source_storage_object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceStorageObjectInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolInput")
    def storage_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeDiskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeDiskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="accessMode")
    def access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessMode"))

    @access_mode.setter
    def access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7caf0072a59d0194af2daae402156888ceaf7419cd05849c536d4990e312c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956eec9ab81662eb1a6cff49f29d0384a8210ae378efecda7f25d89618ffe89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createSnapshotBeforeDestroy")
    def create_snapshot_before_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createSnapshotBeforeDestroy"))

    @create_snapshot_before_destroy.setter
    def create_snapshot_before_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8a9acbe13111f01681c06140cdefa7a5b463a32e7a9bde1934b17134a19981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSnapshotBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createSnapshotBeforeDestroyPrefix")
    def create_snapshot_before_destroy_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createSnapshotBeforeDestroyPrefix"))

    @create_snapshot_before_destroy_prefix.setter
    def create_snapshot_before_destroy_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216b084e4f2ac21a70b7f7c5b1b54d636b8e2f49295b2139609bb221e5049f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSnapshotBeforeDestroyPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3919d36486bdf792304c470097ee66e2e32efb5c31ef417055a435a83d1784ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd590df93fae2d73a6bdc5ad11fd11f9e298873446b9ca6ded333d733fda06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConfidentialCompute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421dccd80ce70aeee4b835b0fb77127f495b7a997fe2e304373439c9ee55d07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a568517c9c4d821f294c5bee8835bbf3d8fd02082f1f15135ef9c09b2991f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44c01724cdcc1aa0e107b51105d2e2835331f62a863f25e9f628fdca80413b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenses")
    def licenses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "licenses"))

    @licenses.setter
    def licenses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1bbc3111abd1a3a890ebdba8bcce277127e11a732be3681e78cb2b2808e5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bca2b83efb453295d36bb66e0ad6ab1a2a941ba9cbe86292b67a4808abd66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalBlockSizeBytes")
    def physical_block_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "physicalBlockSizeBytes"))

    @physical_block_size_bytes.setter
    def physical_block_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9784aee5d59111a31495bcb80c0e8786aec475f1da07b885715a1da1020dd89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalBlockSizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb1757eb2e4d7983859989210d35126a046e366e39be97962b313b2cc196e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b25d25dc4ba4493a95ec1ee43397068b1a51054bbfb03397149b1def0c85d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5e9e3db82750f7da0894ca7c44dafee088367101930a52a2b7c6b61b8de7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daac7aafeb9bad65b4a5d0bffa8306c6a4de7ec307a111d72cd73cac4a349bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @snapshot.setter
    def snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bc3f40c0049d17c91f0c537033d61ec9a099a3d54a35ac8722a71de22f054fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDisk")
    def source_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDisk"))

    @source_disk.setter
    def source_disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fcc538dba5c46462b2dbfe3ef81b4de779431394282fe4a1146c78949dabb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceInstantSnapshot")
    def source_instant_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceInstantSnapshot"))

    @source_instant_snapshot.setter
    def source_instant_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63a4f3afd1d35c142fdb0f228508e11c66390ad584f4af54dd4b8e928e4b993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceInstantSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceStorageObject")
    def source_storage_object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceStorageObject"))

    @source_storage_object.setter
    def source_storage_object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b5a5490ca8b4090561e4456543662c7156d7ba9072198b355f1d6c5c2c10cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceStorageObject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa99245e7ec8b9a637eaeab0dd082589d0aa29f9123ac486cfcb76ca2899f8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb482980c686f1bf59ff0c4bfc9ce25754ffe27e5c066ba64f86225ace896c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921dcdd7e7358b92a2096ef929ea23ea29e390e334b84f6a93339105c4a23d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskAsyncPrimaryDisk",
    jsii_struct_bases=[],
    name_mapping={"disk": "disk"},
)
class ComputeDiskAsyncPrimaryDisk:
    def __init__(self, *, disk: builtins.str) -> None:
        '''
        :param disk: Primary disk for asynchronous disk replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk ComputeDisk#disk}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1d7ee4773aeef4e9cc871b5eb16b0f8bf2f634eefdcd0acefca0832b6ea800)
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk": disk,
        }

    @builtins.property
    def disk(self) -> builtins.str:
        '''Primary disk for asynchronous disk replication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk ComputeDisk#disk}
        '''
        result = self._values.get("disk")
        assert result is not None, "Required property 'disk' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskAsyncPrimaryDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskAsyncPrimaryDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskAsyncPrimaryDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0e14f9358604e50b19099a6ef03003bfab868fbdf0a8b80f12baba7ac14c801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="diskInput")
    def disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskInput"))

    @builtins.property
    @jsii.member(jsii_name="disk")
    def disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disk"))

    @disk.setter
    def disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6277e845cb68a3a8d5ddab5715b4bf33081e5c96e45a57d08f6153f2269dfe40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskAsyncPrimaryDisk]:
        return typing.cast(typing.Optional[ComputeDiskAsyncPrimaryDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskAsyncPrimaryDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def07023dfa220839beb5655e2d6a7f2262531bee9b23aac89bdb244bc204ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskConfig",
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
        "access_mode": "accessMode",
        "architecture": "architecture",
        "async_primary_disk": "asyncPrimaryDisk",
        "create_snapshot_before_destroy": "createSnapshotBeforeDestroy",
        "create_snapshot_before_destroy_prefix": "createSnapshotBeforeDestroyPrefix",
        "description": "description",
        "disk_encryption_key": "diskEncryptionKey",
        "enable_confidential_compute": "enableConfidentialCompute",
        "guest_os_features": "guestOsFeatures",
        "id": "id",
        "image": "image",
        "labels": "labels",
        "licenses": "licenses",
        "params": "params",
        "physical_block_size_bytes": "physicalBlockSizeBytes",
        "project": "project",
        "provisioned_iops": "provisionedIops",
        "provisioned_throughput": "provisionedThroughput",
        "size": "size",
        "snapshot": "snapshot",
        "source_disk": "sourceDisk",
        "source_image_encryption_key": "sourceImageEncryptionKey",
        "source_instant_snapshot": "sourceInstantSnapshot",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "source_storage_object": "sourceStorageObject",
        "storage_pool": "storagePool",
        "timeouts": "timeouts",
        "type": "type",
        "zone": "zone",
    },
)
class ComputeDiskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_mode: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[builtins.str] = None,
        async_primary_disk: typing.Optional[typing.Union[ComputeDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        params: typing.Optional[typing.Union["ComputeDiskParams", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_instant_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_storage_object: typing.Optional[builtins.str] = None,
        storage_pool: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
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
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#name ComputeDisk#name}
        :param access_mode: The access mode of the disk. For example: - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode. - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode. - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode. The AccessMode is only valid for Hyperdisk disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#access_mode ComputeDisk#access_mode}
        :param architecture: The architecture of the disk. Values include 'X86_64', 'ARM64'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#architecture ComputeDisk#architecture}
        :param async_primary_disk: async_primary_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#async_primary_disk ComputeDisk#async_primary_disk}
        :param create_snapshot_before_destroy: If set to true, a snapshot of the disk will be created before it is destroyed. If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation. The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy ComputeDisk#create_snapshot_before_destroy}
        :param create_snapshot_before_destroy_prefix: This will set a custom name prefix for the snapshot that's created when the disk is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy_prefix ComputeDisk#create_snapshot_before_destroy_prefix}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#description ComputeDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        :param enable_confidential_compute: Whether this disk is using confidential compute mode. Note: Only supported on hyperdisk skus, disk_encryption_key is required when setting to true Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#enable_confidential_compute ComputeDisk#enable_confidential_compute}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#guest_os_features ComputeDisk#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#id ComputeDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image: The image from which to initialize this disk. This can be one of: the image's 'self_link', 'projects/{project}/global/images/{image}', 'projects/{project}/global/images/family/{family}', 'global/images/{image}', 'global/images/family/{family}', 'family/{family}', '{project}/{family}', '{project}/{image}', '{family}', or '{image}'. If referred by family, the images names must include the family name. If they don't, use the `google_compute_image data source </docs/providers/google/d/compute_image.html>`_. For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'. These images can be referred by family name here. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#image ComputeDisk#image}
        :param labels: Labels to apply to this disk. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#labels ComputeDisk#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#licenses ComputeDisk#licenses}
        :param params: params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#params ComputeDisk#params}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#project ComputeDisk#project}.
        :param provisioned_iops: Indicates how many IOPS must be provisioned for the disk. Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk allows for an update of IOPS every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        :param provisioned_throughput: Indicates how much Throughput must be provisioned for the disk. Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk allows for an update of Throughput every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_throughput ComputeDisk#provisioned_throughput}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the 'image' or 'snapshot' parameter, or specify it alone to create an empty persistent disk. If you specify this field along with 'image' or 'snapshot', the value must not be less than the size of the image or the size of the snapshot. ~>**NOTE** If you change the size, Terraform updates the disk size if upsizing is detected but recreates the disk if downsizing is requested. You can add 'lifecycle.prevent_destroy' in the config to prevent destroying and recreating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#size ComputeDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. If the snapshot is in another project than this disk, you must supply a full URL. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' - 'projects/project/global/snapshots/snapshot' - 'global/snapshots/snapshot' - 'snapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#snapshot ComputeDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} - https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} - projects/{project}/zones/{zone}/disks/{disk} - projects/{project}/regions/{region}/disks/{disk} - zones/{zone}/disks/{disk} - regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_disk ComputeDisk#source_disk}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        :param source_instant_snapshot: The source instant snapshot used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instantSnapshots/instantSnapshot' - 'projects/project/zones/zone/instantSnapshots/instantSnapshot' - 'zones/zone/instantSnapshots/instantSnapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_instant_snapshot ComputeDisk#source_instant_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        :param source_storage_object: The full Google Cloud Storage URI where the disk image is stored. This file must be a gzip-compressed tarball whose name ends in .tar.gz or virtual machine disk whose name ends in vmdk. Valid URIs may start with gs:// or https://storage.googleapis.com/. This flag is not optimized for creating multiple disks from a source storage object. To create many disks from a source storage object, use gcloud compute images import instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_storage_object ComputeDisk#source_storage_object}
        :param storage_pool: The URL or the name of the storage pool in which the new disk is created. For example: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/storagePools/{storagePool} - /projects/{project}/zones/{zone}/storagePools/{storagePool} - /zones/{zone}/storagePools/{storagePool} - /{storagePool} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#storage_pool ComputeDisk#storage_pool}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#timeouts ComputeDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#type ComputeDisk#type}
        :param zone: A reference to the zone where the disk resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#zone ComputeDisk#zone}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(async_primary_disk, dict):
            async_primary_disk = ComputeDiskAsyncPrimaryDisk(**async_primary_disk)
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ComputeDiskDiskEncryptionKey(**disk_encryption_key)
        if isinstance(params, dict):
            params = ComputeDiskParams(**params)
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeDiskSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeDiskSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if isinstance(timeouts, dict):
            timeouts = ComputeDiskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d8a2e3fd81d6c788595557425485f7dcf1fa4d83ccb4f3d42670518a0aefa0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument async_primary_disk", value=async_primary_disk, expected_type=type_hints["async_primary_disk"])
            check_type(argname="argument create_snapshot_before_destroy", value=create_snapshot_before_destroy, expected_type=type_hints["create_snapshot_before_destroy"])
            check_type(argname="argument create_snapshot_before_destroy_prefix", value=create_snapshot_before_destroy_prefix, expected_type=type_hints["create_snapshot_before_destroy_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument enable_confidential_compute", value=enable_confidential_compute, expected_type=type_hints["enable_confidential_compute"])
            check_type(argname="argument guest_os_features", value=guest_os_features, expected_type=type_hints["guest_os_features"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument licenses", value=licenses, expected_type=type_hints["licenses"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument physical_block_size_bytes", value=physical_block_size_bytes, expected_type=type_hints["physical_block_size_bytes"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument provisioned_iops", value=provisioned_iops, expected_type=type_hints["provisioned_iops"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument source_disk", value=source_disk, expected_type=type_hints["source_disk"])
            check_type(argname="argument source_image_encryption_key", value=source_image_encryption_key, expected_type=type_hints["source_image_encryption_key"])
            check_type(argname="argument source_instant_snapshot", value=source_instant_snapshot, expected_type=type_hints["source_instant_snapshot"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument source_storage_object", value=source_storage_object, expected_type=type_hints["source_storage_object"])
            check_type(argname="argument storage_pool", value=storage_pool, expected_type=type_hints["storage_pool"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
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
        if access_mode is not None:
            self._values["access_mode"] = access_mode
        if architecture is not None:
            self._values["architecture"] = architecture
        if async_primary_disk is not None:
            self._values["async_primary_disk"] = async_primary_disk
        if create_snapshot_before_destroy is not None:
            self._values["create_snapshot_before_destroy"] = create_snapshot_before_destroy
        if create_snapshot_before_destroy_prefix is not None:
            self._values["create_snapshot_before_destroy_prefix"] = create_snapshot_before_destroy_prefix
        if description is not None:
            self._values["description"] = description
        if disk_encryption_key is not None:
            self._values["disk_encryption_key"] = disk_encryption_key
        if enable_confidential_compute is not None:
            self._values["enable_confidential_compute"] = enable_confidential_compute
        if guest_os_features is not None:
            self._values["guest_os_features"] = guest_os_features
        if id is not None:
            self._values["id"] = id
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if licenses is not None:
            self._values["licenses"] = licenses
        if params is not None:
            self._values["params"] = params
        if physical_block_size_bytes is not None:
            self._values["physical_block_size_bytes"] = physical_block_size_bytes
        if project is not None:
            self._values["project"] = project
        if provisioned_iops is not None:
            self._values["provisioned_iops"] = provisioned_iops
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if size is not None:
            self._values["size"] = size
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if source_disk is not None:
            self._values["source_disk"] = source_disk
        if source_image_encryption_key is not None:
            self._values["source_image_encryption_key"] = source_image_encryption_key
        if source_instant_snapshot is not None:
            self._values["source_instant_snapshot"] = source_instant_snapshot
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if source_storage_object is not None:
            self._values["source_storage_object"] = source_storage_object
        if storage_pool is not None:
            self._values["storage_pool"] = storage_pool
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
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
        '''Name of the resource.

        Provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and match
        the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the
        first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the last
        character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#name ComputeDisk#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_mode(self) -> typing.Optional[builtins.str]:
        '''The access mode of the disk.

        For example:

        - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode.
        - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode.
        - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode.
          The AccessMode is only valid for Hyperdisk disk types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#access_mode ComputeDisk#access_mode}
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The architecture of the disk. Values include 'X86_64', 'ARM64'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#architecture ComputeDisk#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def async_primary_disk(self) -> typing.Optional[ComputeDiskAsyncPrimaryDisk]:
        '''async_primary_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#async_primary_disk ComputeDisk#async_primary_disk}
        '''
        result = self._values.get("async_primary_disk")
        return typing.cast(typing.Optional[ComputeDiskAsyncPrimaryDisk], result)

    @builtins.property
    def create_snapshot_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a snapshot of the disk will be created before it is destroyed.

        If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation.
        The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy ComputeDisk#create_snapshot_before_destroy}
        '''
        result = self._values.get("create_snapshot_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_snapshot_before_destroy_prefix(self) -> typing.Optional[builtins.str]:
        '''This will set a custom name prefix for the snapshot that's created when the disk is deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create_snapshot_before_destroy_prefix ComputeDisk#create_snapshot_before_destroy_prefix}
        '''
        result = self._values.get("create_snapshot_before_destroy_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#description ComputeDisk#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key(self) -> typing.Optional["ComputeDiskDiskEncryptionKey"]:
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#disk_encryption_key ComputeDisk#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskDiskEncryptionKey"], result)

    @builtins.property
    def enable_confidential_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this disk is using confidential compute mode.

        Note: Only supported on hyperdisk skus, disk_encryption_key is required when setting to true

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#enable_confidential_compute ComputeDisk#enable_confidential_compute}
        '''
        result = self._values.get("enable_confidential_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def guest_os_features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeDiskGuestOsFeatures"]]]:
        '''guest_os_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#guest_os_features ComputeDisk#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeDiskGuestOsFeatures"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#id ComputeDisk#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''The image from which to initialize this disk.

        This can be
        one of: the image's 'self_link', 'projects/{project}/global/images/{image}',
        'projects/{project}/global/images/family/{family}', 'global/images/{image}',
        'global/images/family/{family}', 'family/{family}', '{project}/{family}',
        '{project}/{image}', '{family}', or '{image}'. If referred by family, the
        images names must include the family name. If they don't, use the
        `google_compute_image data source </docs/providers/google/d/compute_image.html>`_.
        For instance, the image 'centos-6-v20180104' includes its family name 'centos-6'.
        These images can be referred by family name here.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#image ComputeDisk#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this disk.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#labels ComputeDisk#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def licenses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Any applicable license URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#licenses ComputeDisk#licenses}
        '''
        result = self._values.get("licenses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def params(self) -> typing.Optional["ComputeDiskParams"]:
        '''params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#params ComputeDisk#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional["ComputeDiskParams"], result)

    @builtins.property
    def physical_block_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Physical block size of the persistent disk, in bytes.

        If not present
        in a request, a default value is used. Currently supported sizes
        are 4096 and 16384, other sizes may be added in the future.
        If an unsupported value is requested, the error message will list
        the supported values for the caller's project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#physical_block_size_bytes ComputeDisk#physical_block_size_bytes}
        '''
        result = self._values.get("physical_block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#project ComputeDisk#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS must be provisioned for the disk.

        Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk
        allows for an update of IOPS every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_iops ComputeDisk#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much Throughput must be provisioned for the disk.

        Note: Updating currently is only supported by hyperdisk skus without the need to delete and recreate the disk, hyperdisk
        allows for an update of Throughput every 4 hours. To update your hyperdisk more frequently, you'll need to manually delete and recreate it

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#provisioned_throughput ComputeDisk#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Size of the persistent disk, specified in GB.

        You can specify this
        field when creating a persistent disk using the 'image' or
        'snapshot' parameter, or specify it alone to create an empty
        persistent disk.

        If you specify this field along with 'image' or 'snapshot',
        the value must not be less than the size of the image
        or the size of the snapshot.

        ~>**NOTE** If you change the size, Terraform updates the disk size
        if upsizing is detected but recreates the disk if downsizing is requested.
        You can add 'lifecycle.prevent_destroy' in the config to prevent destroying
        and recreating.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#size ComputeDisk#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot(self) -> typing.Optional[builtins.str]:
        '''The source snapshot used to create this disk.

        You can provide this as
        a partial or full URL to the resource. If the snapshot is in another
        project than this disk, you must supply a full URL. For example, the
        following are valid values:

        - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot'
        - 'projects/project/global/snapshots/snapshot'
        - 'global/snapshots/snapshot'
        - 'snapshot'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#snapshot ComputeDisk#snapshot}
        '''
        result = self._values.get("snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_disk(self) -> typing.Optional[builtins.str]:
        '''The source disk used to create this disk.

        You can provide this as a partial or full URL to the resource.
        For example, the following are valid values:

        - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk}
        - https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk}
        - projects/{project}/zones/{zone}/disks/{disk}
        - projects/{project}/regions/{region}/disks/{disk}
        - zones/{zone}/disks/{disk}
        - regions/{region}/disks/{disk}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_disk ComputeDisk#source_disk}
        '''
        result = self._values.get("source_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeDiskSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_image_encryption_key ComputeDisk#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskSourceImageEncryptionKey"], result)

    @builtins.property
    def source_instant_snapshot(self) -> typing.Optional[builtins.str]:
        '''The source instant snapshot used to create this disk.

        You can provide this as a partial or full URL to the resource.
        For example, the following are valid values:

        - 'https://www.googleapis.com/compute/v1/projects/project/zones/zone/instantSnapshots/instantSnapshot'
        - 'projects/project/zones/zone/instantSnapshots/instantSnapshot'
        - 'zones/zone/instantSnapshots/instantSnapshot'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_instant_snapshot ComputeDisk#source_instant_snapshot}
        '''
        result = self._values.get("source_instant_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_snapshot_encryption_key ComputeDisk#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeDiskSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def source_storage_object(self) -> typing.Optional[builtins.str]:
        '''The full Google Cloud Storage URI where the disk image is stored.

        This file must be a gzip-compressed tarball whose name ends in .tar.gz or virtual machine disk whose name ends in vmdk.
        Valid URIs may start with gs:// or https://storage.googleapis.com/.
        This flag is not optimized for creating multiple disks from a source storage object.
        To create many disks from a source storage object, use gcloud compute images import instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#source_storage_object ComputeDisk#source_storage_object}
        '''
        result = self._values.get("source_storage_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_pool(self) -> typing.Optional[builtins.str]:
        '''The URL or the name of the storage pool in which the new disk is created.

        For example:

        - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/storagePools/{storagePool}
        - /projects/{project}/zones/{zone}/storagePools/{storagePool}
        - /zones/{zone}/storagePools/{storagePool}
        - /{storagePool}

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#storage_pool ComputeDisk#storage_pool}
        '''
        result = self._values.get("storage_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeDiskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#timeouts ComputeDisk#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeDiskTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''URL of the disk type resource describing which disk type to use to create the disk.

        Provide this when creating the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#type ComputeDisk#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''A reference to the zone where the disk resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#zone ComputeDisk#zone}
        '''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeDiskDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#rsa_encrypted_key ComputeDisk#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ebf1cdf2a41c69a73405387d2fa098ed53a30fd4e6ac495e5e5a625e56e0893)
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
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        You can provide either the rawKey or the rsaEncryptedKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#rsa_encrypted_key ComputeDisk#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24d89d19e0ec78c9d20f137f921c7319c469e430f51d70e089ea3198b2d2a73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c49ea84d5cf38d5adc864f1dbd354988b85e8ee593364a03ad198ba8c23b177b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__987609f5cdc37eec68941271f99db71f35bc3dea5a986ad4b01749aa8fb9fa55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392ef4ccb23e13c9f95b91e7ad885ea892bf479c55dbbb30f9c8532370a510da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f036c386b03c9b16a197d1e3d97a9a6be968a6126ed8b851faa1fe7c8a8b4f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e86db03c195ef1195cd4fbfb001f8193d6bd115ec224f126e3fe7b7383b4867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskGuestOsFeatures",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ComputeDiskGuestOsFeatures:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: The type of supported feature. Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#type ComputeDisk#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39984d25513ecbb5abad7682708d831b737917f270ba354b056fcfe5df2b415)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of supported feature. Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#type ComputeDisk#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskGuestOsFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskGuestOsFeaturesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskGuestOsFeaturesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a5aea2b58dd90bae95843c74b92450856a90493497c0a593b24cbcac72862c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeDiskGuestOsFeaturesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6dee4e4e25da1d13250366a7b773113ec2901e667d65cb5926e02915ff12b7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeDiskGuestOsFeaturesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d2b4293c72b82dd76d7133c68b5b18a9ab1f4d66229347b25b347d340af05c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b8b6af020b3da02f167be821ac0fdf09c89f870039a015013f1c5231bc85a68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d25bfa95c3bcb73b41a5c7e0cb215943571a54ddcb86881bb0fa6ebb1ce70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeDiskGuestOsFeatures]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeDiskGuestOsFeatures]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeDiskGuestOsFeatures]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bb5fb17db54e0418448bb0af2b2166e0ea13016e21c49bd2946691d4c857b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeDiskGuestOsFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskGuestOsFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd7e81a48ee647c7296109e96b2882e1d2f5d5548017e7f4123a2a4c1dc93de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
            type_hints = typing.get_type_hints(_typecheckingstub__375408809e84c23a228ff92f5814edd2373a993774a99cb0b6c8a278220c52bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskGuestOsFeatures]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskGuestOsFeatures]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskGuestOsFeatures]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b6cac8f4179e5ef6854db958b0ed1dc97e02367d78ccb3a0c4b2338f1341a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskParams",
    jsii_struct_bases=[],
    name_mapping={"resource_manager_tags": "resourceManagerTags"},
)
class ComputeDiskParams:
    def __init__(
        self,
        *,
        resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param resource_manager_tags: Resource manager tags to be bound to the disk. Tag keys and values have the same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id}, and values are in the format tagValues/456. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#resource_manager_tags ComputeDisk#resource_manager_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dba1c01bcda318e86f541f06b40f7d8e8e350e3d52f8fa8fa1348979b1d8316)
            check_type(argname="argument resource_manager_tags", value=resource_manager_tags, expected_type=type_hints["resource_manager_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_manager_tags is not None:
            self._values["resource_manager_tags"] = resource_manager_tags

    @builtins.property
    def resource_manager_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource manager tags to be bound to the disk.

        Tag keys and values have the
        same definition as resource manager tags. Keys must be in the format tagKeys/{tag_key_id},
        and values are in the format tagValues/456.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#resource_manager_tags ComputeDisk#resource_manager_tags}
        '''
        result = self._values.get("resource_manager_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f11229e1ffcc4920c1c45cf4c26605ada0786ab363609adb4e25129b4953540b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef31bdcb999e6004fa21b5aef373b42fc81d8f4c8fa932f1829792633ae0617c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceManagerTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskParams]:
        return typing.cast(typing.Optional[ComputeDiskParams], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeDiskParams]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54207599525e9bd74674fd2c48374c300dea86dc3d6267ec17ad710b7d6c9406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
    },
)
class ComputeDiskSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f68332b6ce7fe9557016352f50e6925bbb6c91970aa522ff97140f5048edc2a)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__957e5e4e30b39f5e8f3a970f11394e55cfc199d044c2486e6d394af2a13fa3b6)
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
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2726a5e8dbe08d27a8bb963905fd61387c6490cc6e6d00862ba55222c087f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61136deaa937db3d4ce3b46e24e6cccd8048ec2203b99db35782ae03d4197a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffee1ad5b09db8f5ed1ab13d46e0505fe75d96e57da864bbf5ddc0ec013b7b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe5f27419701e9c3dcb378dc972ab7ab028f4c1f87c45510b9fd4d99d5130a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
    },
)
class ComputeDiskSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to encrypt the disk. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        :param kms_key_service_account: The service account used for the encryption request for the given KMS key. If absent, the Compute Engine Service Agent service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2ff00ebdef92d0366e43a944f4eb712f7c5b2bfb23507b1559a8b212ed6cee)
            check_type(argname="argument kms_key_self_link", value=kms_key_self_link, expected_type=type_hints["kms_key_self_link"])
            check_type(argname="argument kms_key_service_account", value=kms_key_service_account, expected_type=type_hints["kms_key_service_account"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_self_link is not None:
            self._values["kms_key_self_link"] = kms_key_self_link
        if kms_key_service_account is not None:
            self._values["kms_key_service_account"] = kms_key_service_account
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def kms_key_self_link(self) -> typing.Optional[builtins.str]:
        '''The self link of the encryption key used to encrypt the disk.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_self_link ComputeDisk#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account used for the encryption request for the given KMS key.

        If absent, the Compute Engine Service Agent service account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#kms_key_service_account ComputeDisk#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#raw_key ComputeDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe052bff22446c4f2cef5c3a457b87bf4b452a256b90028f23ccbf84d61c3c1)
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
    @jsii.member(jsii_name="kmsKeySelfLink")
    def kms_key_self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeySelfLink"))

    @kms_key_self_link.setter
    def kms_key_self_link(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7c33c01a2d9efbe73198c7d88fc7c2bb181cbcbaa93ced432fe51e788b6a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d95102cea3b3bfac7283feaa3d5768bdba4695b32e394c56f3e4dc0b93ddce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d6203be8770759e497d93d03b7a8347015399a53fd28f596cf77eaae2277db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeDiskSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeDiskSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeDiskSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4676218883c620067b7266894eedb11878d30477aa66b0ba37c9e221683a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeDiskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create ComputeDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#delete ComputeDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#update ComputeDisk#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf38879418230f0583232c7bc005eaa4a56f0425a5694702543cd80f20e76f6b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#create ComputeDisk#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#delete ComputeDisk#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_disk#update ComputeDisk#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeDiskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeDiskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeDisk.ComputeDiskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89bf547ee69aca23fe2101341c353801a8851a6cd684c6cbf4038eba5abc9c56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3582ac1204411f13e6e17c796e8be27c898efe753ca959cf41f0507e55b4b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c50c6645403cbe8781ce55dcf42aa616bca94395232bfd09991ca5144e3753d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976e426b66bce506d24ae9a73f34e4a1d47f9caabc7fa0dec2cf5297b26194be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8f8d6a264f6c679f2b8928824abd6b37b4abc91901fb5add3519454d500d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeDisk",
    "ComputeDiskAsyncPrimaryDisk",
    "ComputeDiskAsyncPrimaryDiskOutputReference",
    "ComputeDiskConfig",
    "ComputeDiskDiskEncryptionKey",
    "ComputeDiskDiskEncryptionKeyOutputReference",
    "ComputeDiskGuestOsFeatures",
    "ComputeDiskGuestOsFeaturesList",
    "ComputeDiskGuestOsFeaturesOutputReference",
    "ComputeDiskParams",
    "ComputeDiskParamsOutputReference",
    "ComputeDiskSourceImageEncryptionKey",
    "ComputeDiskSourceImageEncryptionKeyOutputReference",
    "ComputeDiskSourceSnapshotEncryptionKey",
    "ComputeDiskSourceSnapshotEncryptionKeyOutputReference",
    "ComputeDiskTimeouts",
    "ComputeDiskTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__27bfcff2e5a97a5b91ac8d6d70a38ea054bc83c0e8e09864edb474805c50de74(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    access_mode: typing.Optional[builtins.str] = None,
    architecture: typing.Optional[builtins.str] = None,
    async_primary_disk: typing.Optional[typing.Union[ComputeDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    params: typing.Optional[typing.Union[ComputeDiskParams, typing.Dict[builtins.str, typing.Any]]] = None,
    physical_block_size_bytes: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    snapshot: typing.Optional[builtins.str] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_instant_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_storage_object: typing.Optional[builtins.str] = None,
    storage_pool: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b7adc51219cf57c72979fc7abe5d167be8014c772677883cb9557a6999a6d1e8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51c7e11e72ee5afc069e0e871d4c9558c840915ef3db952e369adb5607836d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7caf0072a59d0194af2daae402156888ceaf7419cd05849c536d4990e312c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956eec9ab81662eb1a6cff49f29d0384a8210ae378efecda7f25d89618ffe89d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8a9acbe13111f01681c06140cdefa7a5b463a32e7a9bde1934b17134a19981(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216b084e4f2ac21a70b7f7c5b1b54d636b8e2f49295b2139609bb221e5049f1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3919d36486bdf792304c470097ee66e2e32efb5c31ef417055a435a83d1784ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd590df93fae2d73a6bdc5ad11fd11f9e298873446b9ca6ded333d733fda06f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421dccd80ce70aeee4b835b0fb77127f495b7a997fe2e304373439c9ee55d07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a568517c9c4d821f294c5bee8835bbf3d8fd02082f1f15135ef9c09b2991f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44c01724cdcc1aa0e107b51105d2e2835331f62a863f25e9f628fdca80413b8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1bbc3111abd1a3a890ebdba8bcce277127e11a732be3681e78cb2b2808e5eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bca2b83efb453295d36bb66e0ad6ab1a2a941ba9cbe86292b67a4808abd66d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9784aee5d59111a31495bcb80c0e8786aec475f1da07b885715a1da1020dd89b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb1757eb2e4d7983859989210d35126a046e366e39be97962b313b2cc196e2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b25d25dc4ba4493a95ec1ee43397068b1a51054bbfb03397149b1def0c85d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5e9e3db82750f7da0894ca7c44dafee088367101930a52a2b7c6b61b8de7bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daac7aafeb9bad65b4a5d0bffa8306c6a4de7ec307a111d72cd73cac4a349bb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc3f40c0049d17c91f0c537033d61ec9a099a3d54a35ac8722a71de22f054fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fcc538dba5c46462b2dbfe3ef81b4de779431394282fe4a1146c78949dabb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63a4f3afd1d35c142fdb0f228508e11c66390ad584f4af54dd4b8e928e4b993(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b5a5490ca8b4090561e4456543662c7156d7ba9072198b355f1d6c5c2c10cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa99245e7ec8b9a637eaeab0dd082589d0aa29f9123ac486cfcb76ca2899f8fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb482980c686f1bf59ff0c4bfc9ce25754ffe27e5c066ba64f86225ace896c1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921dcdd7e7358b92a2096ef929ea23ea29e390e334b84f6a93339105c4a23d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1d7ee4773aeef4e9cc871b5eb16b0f8bf2f634eefdcd0acefca0832b6ea800(
    *,
    disk: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e14f9358604e50b19099a6ef03003bfab868fbdf0a8b80f12baba7ac14c801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6277e845cb68a3a8d5ddab5715b4bf33081e5c96e45a57d08f6153f2269dfe40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def07023dfa220839beb5655e2d6a7f2262531bee9b23aac89bdb244bc204ac0(
    value: typing.Optional[ComputeDiskAsyncPrimaryDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d8a2e3fd81d6c788595557425485f7dcf1fa4d83ccb4f3d42670518a0aefa0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    access_mode: typing.Optional[builtins.str] = None,
    architecture: typing.Optional[builtins.str] = None,
    async_primary_disk: typing.Optional[typing.Union[ComputeDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_confidential_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    image: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    params: typing.Optional[typing.Union[ComputeDiskParams, typing.Dict[builtins.str, typing.Any]]] = None,
    physical_block_size_bytes: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    snapshot: typing.Optional[builtins.str] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_instant_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_storage_object: typing.Optional[builtins.str] = None,
    storage_pool: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ebf1cdf2a41c69a73405387d2fa098ed53a30fd4e6ac495e5e5a625e56e0893(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24d89d19e0ec78c9d20f137f921c7319c469e430f51d70e089ea3198b2d2a73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49ea84d5cf38d5adc864f1dbd354988b85e8ee593364a03ad198ba8c23b177b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987609f5cdc37eec68941271f99db71f35bc3dea5a986ad4b01749aa8fb9fa55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392ef4ccb23e13c9f95b91e7ad885ea892bf479c55dbbb30f9c8532370a510da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f036c386b03c9b16a197d1e3d97a9a6be968a6126ed8b851faa1fe7c8a8b4f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e86db03c195ef1195cd4fbfb001f8193d6bd115ec224f126e3fe7b7383b4867(
    value: typing.Optional[ComputeDiskDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39984d25513ecbb5abad7682708d831b737917f270ba354b056fcfe5df2b415(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5aea2b58dd90bae95843c74b92450856a90493497c0a593b24cbcac72862c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6dee4e4e25da1d13250366a7b773113ec2901e667d65cb5926e02915ff12b7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d2b4293c72b82dd76d7133c68b5b18a9ab1f4d66229347b25b347d340af05c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8b6af020b3da02f167be821ac0fdf09c89f870039a015013f1c5231bc85a68(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d25bfa95c3bcb73b41a5c7e0cb215943571a54ddcb86881bb0fa6ebb1ce70a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bb5fb17db54e0418448bb0af2b2166e0ea13016e21c49bd2946691d4c857b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeDiskGuestOsFeatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd7e81a48ee647c7296109e96b2882e1d2f5d5548017e7f4123a2a4c1dc93de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375408809e84c23a228ff92f5814edd2373a993774a99cb0b6c8a278220c52bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b6cac8f4179e5ef6854db958b0ed1dc97e02367d78ccb3a0c4b2338f1341a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskGuestOsFeatures]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dba1c01bcda318e86f541f06b40f7d8e8e350e3d52f8fa8fa1348979b1d8316(
    *,
    resource_manager_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11229e1ffcc4920c1c45cf4c26605ada0786ab363609adb4e25129b4953540b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef31bdcb999e6004fa21b5aef373b42fc81d8f4c8fa932f1829792633ae0617c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54207599525e9bd74674fd2c48374c300dea86dc3d6267ec17ad710b7d6c9406(
    value: typing.Optional[ComputeDiskParams],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f68332b6ce7fe9557016352f50e6925bbb6c91970aa522ff97140f5048edc2a(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957e5e4e30b39f5e8f3a970f11394e55cfc199d044c2486e6d394af2a13fa3b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2726a5e8dbe08d27a8bb963905fd61387c6490cc6e6d00862ba55222c087f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61136deaa937db3d4ce3b46e24e6cccd8048ec2203b99db35782ae03d4197a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffee1ad5b09db8f5ed1ab13d46e0505fe75d96e57da864bbf5ddc0ec013b7b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe5f27419701e9c3dcb378dc972ab7ab028f4c1f87c45510b9fd4d99d5130a6(
    value: typing.Optional[ComputeDiskSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2ff00ebdef92d0366e43a944f4eb712f7c5b2bfb23507b1559a8b212ed6cee(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe052bff22446c4f2cef5c3a457b87bf4b452a256b90028f23ccbf84d61c3c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7c33c01a2d9efbe73198c7d88fc7c2bb181cbcbaa93ced432fe51e788b6a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d95102cea3b3bfac7283feaa3d5768bdba4695b32e394c56f3e4dc0b93ddce3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d6203be8770759e497d93d03b7a8347015399a53fd28f596cf77eaae2277db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4676218883c620067b7266894eedb11878d30477aa66b0ba37c9e221683a62(
    value: typing.Optional[ComputeDiskSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf38879418230f0583232c7bc005eaa4a56f0425a5694702543cd80f20e76f6b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bf547ee69aca23fe2101341c353801a8851a6cd684c6cbf4038eba5abc9c56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3582ac1204411f13e6e17c796e8be27c898efe753ca959cf41f0507e55b4b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c50c6645403cbe8781ce55dcf42aa616bca94395232bfd09991ca5144e3753d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976e426b66bce506d24ae9a73f34e4a1d47f9caabc7fa0dec2cf5297b26194be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8f8d6a264f6c679f2b8928824abd6b37b4abc91901fb5add3519454d500d28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeDiskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

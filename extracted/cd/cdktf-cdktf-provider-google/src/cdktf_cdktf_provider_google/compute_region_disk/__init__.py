r'''
# `google_compute_region_disk`

Refer to the Terraform Registry for docs: [`google_compute_region_disk`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk).
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


class ComputeRegionDisk(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDisk",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk google_compute_region_disk}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        replica_zones: typing.Sequence[builtins.str],
        access_mode: typing.Optional[builtins.str] = None,
        async_primary_disk: typing.Optional[typing.Union["ComputeRegionDiskAsyncPrimaryDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeRegionDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeRegionDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk google_compute_region_disk} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#name ComputeRegionDisk#name}
        :param replica_zones: URLs of the zones where the disk should be replicated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#replica_zones ComputeRegionDisk#replica_zones}
        :param access_mode: The access mode of the disk. For example: - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode. - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode. - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode. The AccessMode is only valid for Hyperdisk disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#access_mode ComputeRegionDisk#access_mode}
        :param async_primary_disk: async_primary_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#async_primary_disk ComputeRegionDisk#async_primary_disk}
        :param create_snapshot_before_destroy: If set to true, a snapshot of the disk will be created before it is destroyed. If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation. The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy ComputeRegionDisk#create_snapshot_before_destroy}
        :param create_snapshot_before_destroy_prefix: This will set a custom name prefix for the snapshot that's created when the disk is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy_prefix ComputeRegionDisk#create_snapshot_before_destroy_prefix}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#description ComputeRegionDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk_encryption_key ComputeRegionDisk#disk_encryption_key}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#guest_os_features ComputeRegionDisk#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#id ComputeRegionDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels to apply to this disk. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#labels ComputeRegionDisk#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#licenses ComputeRegionDisk#licenses}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#physical_block_size_bytes ComputeRegionDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#project ComputeRegionDisk#project}.
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Values must be between 10,000 and 120,000. For more details, see the Extreme persistent disk `documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_iops ComputeRegionDisk#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Values must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_throughput ComputeRegionDisk#provisioned_throughput}
        :param region: A reference to the region where the disk resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#region ComputeRegionDisk#region}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the sourceImage or sourceSnapshot parameter, or specify it alone to create an empty persistent disk. If you specify this field along with sourceImage or sourceSnapshot, the value of sizeGb must not be less than the size of the sourceImage or the size of the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#size ComputeRegionDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' - 'projects/project/global/snapshots/snapshot' - 'global/snapshots/snapshot' - 'snapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#snapshot ComputeRegionDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} - https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} - projects/{project}/zones/{zone}/disks/{disk} - projects/{project}/regions/{region}/disks/{disk} - zones/{zone}/disks/{disk} - regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_disk ComputeRegionDisk#source_disk}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_snapshot_encryption_key ComputeRegionDisk#source_snapshot_encryption_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#timeouts ComputeRegionDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#type ComputeRegionDisk#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c610edb37c6ae160f198e97817b985816379182802710b424aa6ae13701295be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionDiskConfig(
            name=name,
            replica_zones=replica_zones,
            access_mode=access_mode,
            async_primary_disk=async_primary_disk,
            create_snapshot_before_destroy=create_snapshot_before_destroy,
            create_snapshot_before_destroy_prefix=create_snapshot_before_destroy_prefix,
            description=description,
            disk_encryption_key=disk_encryption_key,
            guest_os_features=guest_os_features,
            id=id,
            labels=labels,
            licenses=licenses,
            physical_block_size_bytes=physical_block_size_bytes,
            project=project,
            provisioned_iops=provisioned_iops,
            provisioned_throughput=provisioned_throughput,
            region=region,
            size=size,
            snapshot=snapshot,
            source_disk=source_disk,
            source_snapshot_encryption_key=source_snapshot_encryption_key,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a ComputeRegionDisk resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionDisk to import.
        :param import_from_id: The id of the existing ComputeRegionDisk that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionDisk to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1600b01481aa55da7235f5bc99ffd8f544a929be51c20fc601115473f48317d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAsyncPrimaryDisk")
    def put_async_primary_disk(self, *, disk: builtins.str) -> None:
        '''
        :param disk: Primary disk for asynchronous disk replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk ComputeRegionDisk#disk}
        '''
        value = ComputeRegionDiskAsyncPrimaryDisk(disk=disk)

        return typing.cast(None, jsii.invoke(self, "putAsyncPrimaryDisk", [value]))

    @jsii.member(jsii_name="putDiskEncryptionKey")
    def put_disk_encryption_key(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The name of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#kms_key_name ComputeRegionDisk#kms_key_name}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#rsa_encrypted_key ComputeRegionDisk#rsa_encrypted_key}
        '''
        value = ComputeRegionDiskDiskEncryptionKey(
            kms_key_name=kms_key_name,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putDiskEncryptionKey", [value]))

    @jsii.member(jsii_name="putGuestOsFeatures")
    def put_guest_os_features(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650f750219369d7777d749180b44f21895c259d0d91408c521469da583ddf1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestOsFeatures", [value]))

    @jsii.member(jsii_name="putSourceSnapshotEncryptionKey")
    def put_source_snapshot_encryption_key(
        self,
        *,
        raw_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        '''
        value = ComputeRegionDiskSourceSnapshotEncryptionKey(raw_key=raw_key)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create ComputeRegionDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#delete ComputeRegionDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#update ComputeRegionDisk#update}.
        '''
        value = ComputeRegionDiskTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessMode")
    def reset_access_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessMode", []))

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

    @jsii.member(jsii_name="resetGuestOsFeatures")
    def reset_guest_os_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestOsFeatures", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLicenses")
    def reset_licenses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenses", []))

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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @jsii.member(jsii_name="resetSnapshot")
    def reset_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshot", []))

    @jsii.member(jsii_name="resetSourceDisk")
    def reset_source_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDisk", []))

    @jsii.member(jsii_name="resetSourceSnapshotEncryptionKey")
    def reset_source_snapshot_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshotEncryptionKey", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    def async_primary_disk(self) -> "ComputeRegionDiskAsyncPrimaryDiskOutputReference":
        return typing.cast("ComputeRegionDiskAsyncPrimaryDiskOutputReference", jsii.get(self, "asyncPrimaryDisk"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionKey")
    def disk_encryption_key(
        self,
    ) -> "ComputeRegionDiskDiskEncryptionKeyOutputReference":
        return typing.cast("ComputeRegionDiskDiskEncryptionKeyOutputReference", jsii.get(self, "diskEncryptionKey"))

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
    def guest_os_features(self) -> "ComputeRegionDiskGuestOsFeaturesList":
        return typing.cast("ComputeRegionDiskGuestOsFeaturesList", jsii.get(self, "guestOsFeatures"))

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
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskId")
    def source_disk_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDiskId"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeRegionDiskSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeRegionDiskSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

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
    def timeouts(self) -> "ComputeRegionDiskTimeoutsOutputReference":
        return typing.cast("ComputeRegionDiskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="accessModeInput")
    def access_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessModeInput"))

    @builtins.property
    @jsii.member(jsii_name="asyncPrimaryDiskInput")
    def async_primary_disk_input(
        self,
    ) -> typing.Optional["ComputeRegionDiskAsyncPrimaryDisk"]:
        return typing.cast(typing.Optional["ComputeRegionDiskAsyncPrimaryDisk"], jsii.get(self, "asyncPrimaryDiskInput"))

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
    ) -> typing.Optional["ComputeRegionDiskDiskEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeRegionDiskDiskEncryptionKey"], jsii.get(self, "diskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeaturesInput")
    def guest_os_features_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionDiskGuestOsFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionDiskGuestOsFeatures"]]], jsii.get(self, "guestOsFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaZonesInput")
    def replica_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "replicaZonesInput"))

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
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeRegionDiskSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeRegionDiskSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionDiskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionDiskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accessMode")
    def access_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessMode"))

    @access_mode.setter
    def access_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8686fc178fe915d5cad513127083c587ad41747b140a6ecf8ffe01af22aac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessMode", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e427da61924af2a45765f8e00d0c3426b911c1cd5b31ab7b8d3804fa6b113cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSnapshotBeforeDestroy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createSnapshotBeforeDestroyPrefix")
    def create_snapshot_before_destroy_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createSnapshotBeforeDestroyPrefix"))

    @create_snapshot_before_destroy_prefix.setter
    def create_snapshot_before_destroy_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9df1c410978e827207463378ee89d5b5727a6acf7348cc8e06d25c520555dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createSnapshotBeforeDestroyPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bc745b6bbe95cbef84c2ed70600ca3ea07735cb050217d0fa513dbd5c8d530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bd5832a0ba20a85f27fe6b100dd9fc1abddba78c427e5d176a9db39d0402ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7f3c6d58fece6bb49e691d16873286e22ea06b568ef2ef6bb9b312b6e7c825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenses")
    def licenses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "licenses"))

    @licenses.setter
    def licenses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8675177a9e7f5c6d8bc0e258b00454018c5e6bbe3153d568f16bce978d68413e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b287f4711840cbe2fe14b2a1c430222c21ad72e55e7a90a971f6de9801dc6ee2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalBlockSizeBytes")
    def physical_block_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "physicalBlockSizeBytes"))

    @physical_block_size_bytes.setter
    def physical_block_size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a21a90528a6f5a33e6f5dca461ca3a576deb7e53e44bb0cf1d0cb543e6bc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalBlockSizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25b6480f301997c8491048d248b69c28aa5bb39132941c269c2277c06b0acf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedIops")
    def provisioned_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedIops"))

    @provisioned_iops.setter
    def provisioned_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4d637fec36c1bd7c9d16fc0b19bf0aedfcaac82ae795c3515ca3656fe11316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedIops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb98728a07ed67a74eb843dbe38c2f89d3af7cc5c26bbee8554b508a2dc89aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provisionedThroughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fefd8ac28c5a2b38d6461626f19f322a22a69b345bf5b38ba222b92617959ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicaZones")
    def replica_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "replicaZones"))

    @replica_zones.setter
    def replica_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08f1b960156d25f1a8ba5360c712be9b0dee652fb8d4e2c86ce1b28c8f9e788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicaZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddb2b3ba64a26c24bebca8053cf3297cce11b6356a05932ad3b57ad5fb49780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshot")
    def snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshot"))

    @snapshot.setter
    def snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b8e2d9a0650005adc10c9667fba3d278a6ae795e035b5fbbd6f5a46ed44392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDisk")
    def source_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDisk"))

    @source_disk.setter
    def source_disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286c172113fc8fa0afeae14e0b78953889b464014936508bddb90e8947308234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9131c17298a7fef2b1f66a182399014fecee5964540364050ce8af204eb20e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskAsyncPrimaryDisk",
    jsii_struct_bases=[],
    name_mapping={"disk": "disk"},
)
class ComputeRegionDiskAsyncPrimaryDisk:
    def __init__(self, *, disk: builtins.str) -> None:
        '''
        :param disk: Primary disk for asynchronous disk replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk ComputeRegionDisk#disk}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86b347df4b85775fe1997aca7c20bdd27440d0af00f7f170bdb19cf8b872a3d)
            check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk": disk,
        }

    @builtins.property
    def disk(self) -> builtins.str:
        '''Primary disk for asynchronous disk replication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk ComputeRegionDisk#disk}
        '''
        result = self._values.get("disk")
        assert result is not None, "Required property 'disk' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskAsyncPrimaryDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionDiskAsyncPrimaryDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskAsyncPrimaryDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ad345eeeda3897e59573480d910bd17c9129d1f3756f8eb59a4c90bec2124a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8749ee7b36d1e180e6c4bdefd4cfadd9780ff6ab808afe55b08aa0cd65162d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionDiskAsyncPrimaryDisk]:
        return typing.cast(typing.Optional[ComputeRegionDiskAsyncPrimaryDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionDiskAsyncPrimaryDisk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec49b19e76a4c81df62aa8275cb24f1e2cfbefb2b1f9ca9830b941b7a9cd7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskConfig",
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
        "replica_zones": "replicaZones",
        "access_mode": "accessMode",
        "async_primary_disk": "asyncPrimaryDisk",
        "create_snapshot_before_destroy": "createSnapshotBeforeDestroy",
        "create_snapshot_before_destroy_prefix": "createSnapshotBeforeDestroyPrefix",
        "description": "description",
        "disk_encryption_key": "diskEncryptionKey",
        "guest_os_features": "guestOsFeatures",
        "id": "id",
        "labels": "labels",
        "licenses": "licenses",
        "physical_block_size_bytes": "physicalBlockSizeBytes",
        "project": "project",
        "provisioned_iops": "provisionedIops",
        "provisioned_throughput": "provisionedThroughput",
        "region": "region",
        "size": "size",
        "snapshot": "snapshot",
        "source_disk": "sourceDisk",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class ComputeRegionDiskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        replica_zones: typing.Sequence[builtins.str],
        access_mode: typing.Optional[builtins.str] = None,
        async_primary_disk: typing.Optional[typing.Union[ComputeRegionDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
        create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disk_encryption_key: typing.Optional[typing.Union["ComputeRegionDiskDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionDiskGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        physical_block_size_bytes: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        provisioned_iops: typing.Optional[jsii.Number] = None,
        provisioned_throughput: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
        snapshot: typing.Optional[builtins.str] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeRegionDiskSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionDiskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#name ComputeRegionDisk#name}
        :param replica_zones: URLs of the zones where the disk should be replicated to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#replica_zones ComputeRegionDisk#replica_zones}
        :param access_mode: The access mode of the disk. For example: - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode. - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode. - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode. The AccessMode is only valid for Hyperdisk disk types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#access_mode ComputeRegionDisk#access_mode}
        :param async_primary_disk: async_primary_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#async_primary_disk ComputeRegionDisk#async_primary_disk}
        :param create_snapshot_before_destroy: If set to true, a snapshot of the disk will be created before it is destroyed. If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation. The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy ComputeRegionDisk#create_snapshot_before_destroy}
        :param create_snapshot_before_destroy_prefix: This will set a custom name prefix for the snapshot that's created when the disk is deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy_prefix ComputeRegionDisk#create_snapshot_before_destroy_prefix}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#description ComputeRegionDisk#description}
        :param disk_encryption_key: disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk_encryption_key ComputeRegionDisk#disk_encryption_key}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#guest_os_features ComputeRegionDisk#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#id ComputeRegionDisk#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels to apply to this disk. A list of key->value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#labels ComputeRegionDisk#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#licenses ComputeRegionDisk#licenses}
        :param physical_block_size_bytes: Physical block size of the persistent disk, in bytes. If not present in a request, a default value is used. Currently supported sizes are 4096 and 16384, other sizes may be added in the future. If an unsupported value is requested, the error message will list the supported values for the caller's project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#physical_block_size_bytes ComputeRegionDisk#physical_block_size_bytes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#project ComputeRegionDisk#project}.
        :param provisioned_iops: Indicates how many IOPS to provision for the disk. This sets the number of I/O operations per second that the disk can handle. Values must be between 10,000 and 120,000. For more details, see the Extreme persistent disk `documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_iops ComputeRegionDisk#provisioned_iops}
        :param provisioned_throughput: Indicates how much throughput to provision for the disk. This sets the number of throughput mb per second that the disk can handle. Values must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_throughput ComputeRegionDisk#provisioned_throughput}
        :param region: A reference to the region where the disk resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#region ComputeRegionDisk#region}
        :param size: Size of the persistent disk, specified in GB. You can specify this field when creating a persistent disk using the sourceImage or sourceSnapshot parameter, or specify it alone to create an empty persistent disk. If you specify this field along with sourceImage or sourceSnapshot, the value of sizeGb must not be less than the size of the sourceImage or the size of the snapshot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#size ComputeRegionDisk#size}
        :param snapshot: The source snapshot used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot' - 'projects/project/global/snapshots/snapshot' - 'global/snapshots/snapshot' - 'snapshot' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#snapshot ComputeRegionDisk#snapshot}
        :param source_disk: The source disk used to create this disk. You can provide this as a partial or full URL to the resource. For example, the following are valid values: - https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{disk} - https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/disks/{disk} - projects/{project}/zones/{zone}/disks/{disk} - projects/{project}/regions/{region}/disks/{disk} - zones/{zone}/disks/{disk} - regions/{region}/disks/{disk} Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_disk ComputeRegionDisk#source_disk}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_snapshot_encryption_key ComputeRegionDisk#source_snapshot_encryption_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#timeouts ComputeRegionDisk#timeouts}
        :param type: URL of the disk type resource describing which disk type to use to create the disk. Provide this when creating the disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#type ComputeRegionDisk#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(async_primary_disk, dict):
            async_primary_disk = ComputeRegionDiskAsyncPrimaryDisk(**async_primary_disk)
        if isinstance(disk_encryption_key, dict):
            disk_encryption_key = ComputeRegionDiskDiskEncryptionKey(**disk_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeRegionDiskSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionDiskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63b9b98d080a2aa2d0a9b648fb13c0c3e1389b728aff0c2dc3d8bffd91f422c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replica_zones", value=replica_zones, expected_type=type_hints["replica_zones"])
            check_type(argname="argument access_mode", value=access_mode, expected_type=type_hints["access_mode"])
            check_type(argname="argument async_primary_disk", value=async_primary_disk, expected_type=type_hints["async_primary_disk"])
            check_type(argname="argument create_snapshot_before_destroy", value=create_snapshot_before_destroy, expected_type=type_hints["create_snapshot_before_destroy"])
            check_type(argname="argument create_snapshot_before_destroy_prefix", value=create_snapshot_before_destroy_prefix, expected_type=type_hints["create_snapshot_before_destroy_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_encryption_key", value=disk_encryption_key, expected_type=type_hints["disk_encryption_key"])
            check_type(argname="argument guest_os_features", value=guest_os_features, expected_type=type_hints["guest_os_features"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument licenses", value=licenses, expected_type=type_hints["licenses"])
            check_type(argname="argument physical_block_size_bytes", value=physical_block_size_bytes, expected_type=type_hints["physical_block_size_bytes"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument provisioned_iops", value=provisioned_iops, expected_type=type_hints["provisioned_iops"])
            check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument snapshot", value=snapshot, expected_type=type_hints["snapshot"])
            check_type(argname="argument source_disk", value=source_disk, expected_type=type_hints["source_disk"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "replica_zones": replica_zones,
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
        if guest_os_features is not None:
            self._values["guest_os_features"] = guest_os_features
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if licenses is not None:
            self._values["licenses"] = licenses
        if physical_block_size_bytes is not None:
            self._values["physical_block_size_bytes"] = physical_block_size_bytes
        if project is not None:
            self._values["project"] = project
        if provisioned_iops is not None:
            self._values["provisioned_iops"] = provisioned_iops
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if region is not None:
            self._values["region"] = region
        if size is not None:
            self._values["size"] = size
        if snapshot is not None:
            self._values["snapshot"] = snapshot
        if source_disk is not None:
            self._values["source_disk"] = source_disk
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#name ComputeRegionDisk#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replica_zones(self) -> typing.List[builtins.str]:
        '''URLs of the zones where the disk should be replicated to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#replica_zones ComputeRegionDisk#replica_zones}
        '''
        result = self._values.get("replica_zones")
        assert result is not None, "Required property 'replica_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def access_mode(self) -> typing.Optional[builtins.str]:
        '''The access mode of the disk.

        For example:

        - READ_WRITE_SINGLE: The default AccessMode, means the disk can be attached to single instance in RW mode.
        - READ_WRITE_MANY: The AccessMode means the disk can be attached to multiple instances in RW mode.
        - READ_ONLY_SINGLE: The AccessMode means the disk can be attached to multiple instances in RO mode.
          The AccessMode is only valid for Hyperdisk disk types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#access_mode ComputeRegionDisk#access_mode}
        '''
        result = self._values.get("access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def async_primary_disk(self) -> typing.Optional[ComputeRegionDiskAsyncPrimaryDisk]:
        '''async_primary_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#async_primary_disk ComputeRegionDisk#async_primary_disk}
        '''
        result = self._values.get("async_primary_disk")
        return typing.cast(typing.Optional[ComputeRegionDiskAsyncPrimaryDisk], result)

    @builtins.property
    def create_snapshot_before_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, a snapshot of the disk will be created before it is destroyed.

        If your disk is encrypted with customer managed encryption keys these will be reused for the snapshot creation.
        The name of the snapshot by default will be '{{disk-name}}-YYYYMMDD-HHmm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy ComputeRegionDisk#create_snapshot_before_destroy}
        '''
        result = self._values.get("create_snapshot_before_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_snapshot_before_destroy_prefix(self) -> typing.Optional[builtins.str]:
        '''This will set a custom name prefix for the snapshot that's created when the disk is deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create_snapshot_before_destroy_prefix ComputeRegionDisk#create_snapshot_before_destroy_prefix}
        '''
        result = self._values.get("create_snapshot_before_destroy_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#description ComputeRegionDisk#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_encryption_key(
        self,
    ) -> typing.Optional["ComputeRegionDiskDiskEncryptionKey"]:
        '''disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#disk_encryption_key ComputeRegionDisk#disk_encryption_key}
        '''
        result = self._values.get("disk_encryption_key")
        return typing.cast(typing.Optional["ComputeRegionDiskDiskEncryptionKey"], result)

    @builtins.property
    def guest_os_features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionDiskGuestOsFeatures"]]]:
        '''guest_os_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#guest_os_features ComputeRegionDisk#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionDiskGuestOsFeatures"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#id ComputeRegionDisk#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this disk.  A list of key->value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#labels ComputeRegionDisk#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def licenses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Any applicable license URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#licenses ComputeRegionDisk#licenses}
        '''
        result = self._values.get("licenses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def physical_block_size_bytes(self) -> typing.Optional[jsii.Number]:
        '''Physical block size of the persistent disk, in bytes.

        If not present
        in a request, a default value is used. Currently supported sizes
        are 4096 and 16384, other sizes may be added in the future.
        If an unsupported value is requested, the error message will list
        the supported values for the caller's project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#physical_block_size_bytes ComputeRegionDisk#physical_block_size_bytes}
        '''
        result = self._values.get("physical_block_size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#project ComputeRegionDisk#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_iops(self) -> typing.Optional[jsii.Number]:
        '''Indicates how many IOPS to provision for the disk.

        This sets the number of I/O operations per second
        that the disk can handle. Values must be between 10,000 and 120,000.
        For more details, see the Extreme persistent disk `documentation <https://cloud.google.com/compute/docs/disks/extreme-persistent-disk>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_iops ComputeRegionDisk#provisioned_iops}
        '''
        result = self._values.get("provisioned_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def provisioned_throughput(self) -> typing.Optional[jsii.Number]:
        '''Indicates how much throughput to provision for the disk.

        This sets the number of throughput
        mb per second that the disk can handle. Values must be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#provisioned_throughput ComputeRegionDisk#provisioned_throughput}
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region where the disk resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#region ComputeRegionDisk#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Size of the persistent disk, specified in GB.

        You can specify this
        field when creating a persistent disk using the sourceImage or
        sourceSnapshot parameter, or specify it alone to create an empty
        persistent disk.

        If you specify this field along with sourceImage or sourceSnapshot,
        the value of sizeGb must not be less than the size of the sourceImage
        or the size of the snapshot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#size ComputeRegionDisk#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot(self) -> typing.Optional[builtins.str]:
        '''The source snapshot used to create this disk.

        You can provide this as
        a partial or full URL to the resource. For example, the following are
        valid values:

        - 'https://www.googleapis.com/compute/v1/projects/project/global/snapshots/snapshot'
        - 'projects/project/global/snapshots/snapshot'
        - 'global/snapshots/snapshot'
        - 'snapshot'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#snapshot ComputeRegionDisk#snapshot}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_disk ComputeRegionDisk#source_disk}
        '''
        result = self._values.get("source_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeRegionDiskSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#source_snapshot_encryption_key ComputeRegionDisk#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeRegionDiskSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionDiskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#timeouts ComputeRegionDisk#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionDiskTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''URL of the disk type resource describing which disk type to use to create the disk.

        Provide this when creating the disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#type ComputeRegionDisk#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_name": "kmsKeyName",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeRegionDiskDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The name of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#kms_key_name ComputeRegionDisk#kms_key_name}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#rsa_encrypted_key ComputeRegionDisk#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b0536bc6cb6bbf06969bed012bf2c631d4b2224751301951ae281093e8043d)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
            check_type(argname="argument rsa_encrypted_key", value=rsa_encrypted_key, expected_type=type_hints["rsa_encrypted_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if raw_key is not None:
            self._values["raw_key"] = raw_key
        if rsa_encrypted_key is not None:
            self._values["rsa_encrypted_key"] = rsa_encrypted_key

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The name of the encryption key that is stored in Google Cloud KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#kms_key_name ComputeRegionDisk#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        You can provide either the rawKey or the rsaEncryptedKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#rsa_encrypted_key ComputeRegionDisk#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionDiskDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20ce93bc431802ac9493d649ba18f49b57f04159c7eb5df27378de916cf1597f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

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
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKeyInput")
    def rsa_encrypted_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaEncryptedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7811f17bc298e69f35ecd16bc79bae5d21f4d72cd58502e8cf9df5f4b43ccc33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f49f7713201d41c29c38bf8f0516ecfddfc230b0d517b00ea4b1ab11dc890f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c057fc54cbf1beb666e4d5ee0a01b218de1da4211c5ea666148f29fa06afbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionDiskDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionDiskDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionDiskDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e759daa39db6297832e986988b90322eef267f3ce4c345f704afd13664738c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskGuestOsFeatures",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ComputeRegionDiskGuestOsFeatures:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: The type of supported feature. Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options. Possible values: ["MULTI_IP_SUBNET", "SECURE_BOOT", "SEV_CAPABLE", "UEFI_COMPATIBLE", "VIRTIO_SCSI_MULTIQUEUE", "WINDOWS", "GVNIC", "SEV_LIVE_MIGRATABLE", "SEV_SNP_CAPABLE", "SUSPEND_RESUME_COMPATIBLE", "TDX_CAPABLE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#type ComputeRegionDisk#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aec82723e31cc2be59368bd69015bd3acb834ed6d60a96516f3c10d07abaefe)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of supported feature.

        Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options. Possible values: ["MULTI_IP_SUBNET", "SECURE_BOOT", "SEV_CAPABLE", "UEFI_COMPATIBLE", "VIRTIO_SCSI_MULTIQUEUE", "WINDOWS", "GVNIC", "SEV_LIVE_MIGRATABLE", "SEV_SNP_CAPABLE", "SUSPEND_RESUME_COMPATIBLE", "TDX_CAPABLE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#type ComputeRegionDisk#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskGuestOsFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionDiskGuestOsFeaturesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskGuestOsFeaturesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14bd2c664ab41cf950616a3044e5be4a9f4cb63a89666d008025f4b0a90878b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionDiskGuestOsFeaturesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad21c41c386669aa3ce7860277e895ca8f62d5659ae01edc40f0729e5073bef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionDiskGuestOsFeaturesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8620623f77288bbd82a8312d544647312456aeefb49b4b5b426d1cb61cacc028)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f79bdaf55fb9383524bf12def687e89b778c14a6b74625e43bffbbdc78b2b00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39f4d9f46ec0584e9ebb64509fa11f9b344d6ccf5a0e29ffa4a7f0d863001047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionDiskGuestOsFeatures]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionDiskGuestOsFeatures]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionDiskGuestOsFeatures]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1b4348d0ee58583a8841dcf06bcf08cc7db4b316fb6bd2e62b1ac7d4d3c09b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionDiskGuestOsFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskGuestOsFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c33bd1c802535f7aa22647a131ecbcaac32c110aee0caa1ce8cbf447681c6ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c68778d66ef644f2f8e98680c40c3bc8372b16f9814ff04626cecfdf60f0ce5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskGuestOsFeatures]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskGuestOsFeatures]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskGuestOsFeatures]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2739d34749319738b90041c06894ae6e87a360551e72816ee1f9346ffd9973f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"raw_key": "rawKey"},
)
class ComputeRegionDiskSourceSnapshotEncryptionKey:
    def __init__(self, *, raw_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286503b8d3dcdea8abb35d23a382ff570fec9a816b8b2036469307a666a696b2)
            check_type(argname="argument raw_key", value=raw_key, expected_type=type_hints["raw_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if raw_key is not None:
            self._values["raw_key"] = raw_key

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#raw_key ComputeRegionDisk#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionDiskSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2bcb576746709b31e90a16c111f46c6cdf2238b8afd7a8f50075383e5d55b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRawKey")
    def reset_raw_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawKey", []))

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @builtins.property
    @jsii.member(jsii_name="rawKeyInput")
    def raw_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb93fe3b6368a4bac8c66a4f212156c7ed7630d00583baa132b7b990d70c100f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionDiskSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeRegionDiskSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionDiskSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26edc05df208662e8479d2604b5ab03b76063ee832e3e78ac0bb2fc3d84e3f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionDiskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create ComputeRegionDisk#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#delete ComputeRegionDisk#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#update ComputeRegionDisk#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1a90c0b08dee31c8743857eceedfc2491c0128364c0a6433573712a28f7eab)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#create ComputeRegionDisk#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#delete ComputeRegionDisk#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_disk#update ComputeRegionDisk#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionDiskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionDiskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionDisk.ComputeRegionDiskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b18c3cc2342b46fa3f2c2ee01766d7735271aeb9a63808496fcb5d5f57203fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40b0ed824a396cb3ca8739159d9cfc15bc26b0b91a642d687a71db4e55b0808b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4119f36b85dcc90059d38dee7fdb0101186988167b90180c31eebe21782eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bbdbe2438a20712ff27d3030f06495e6bb333f5f6711c022361a45175972a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8fc9f886268a17e91483c65794eeae8800996d5d2d2779601d50f6addd95b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionDisk",
    "ComputeRegionDiskAsyncPrimaryDisk",
    "ComputeRegionDiskAsyncPrimaryDiskOutputReference",
    "ComputeRegionDiskConfig",
    "ComputeRegionDiskDiskEncryptionKey",
    "ComputeRegionDiskDiskEncryptionKeyOutputReference",
    "ComputeRegionDiskGuestOsFeatures",
    "ComputeRegionDiskGuestOsFeaturesList",
    "ComputeRegionDiskGuestOsFeaturesOutputReference",
    "ComputeRegionDiskSourceSnapshotEncryptionKey",
    "ComputeRegionDiskSourceSnapshotEncryptionKeyOutputReference",
    "ComputeRegionDiskTimeouts",
    "ComputeRegionDiskTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c610edb37c6ae160f198e97817b985816379182802710b424aa6ae13701295be(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    replica_zones: typing.Sequence[builtins.str],
    access_mode: typing.Optional[builtins.str] = None,
    async_primary_disk: typing.Optional[typing.Union[ComputeRegionDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeRegionDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    physical_block_size_bytes: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
    snapshot: typing.Optional[builtins.str] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeRegionDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1600b01481aa55da7235f5bc99ffd8f544a929be51c20fc601115473f48317d3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650f750219369d7777d749180b44f21895c259d0d91408c521469da583ddf1df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8686fc178fe915d5cad513127083c587ad41747b140a6ecf8ffe01af22aac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e427da61924af2a45765f8e00d0c3426b911c1cd5b31ab7b8d3804fa6b113cbd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9df1c410978e827207463378ee89d5b5727a6acf7348cc8e06d25c520555dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bc745b6bbe95cbef84c2ed70600ca3ea07735cb050217d0fa513dbd5c8d530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bd5832a0ba20a85f27fe6b100dd9fc1abddba78c427e5d176a9db39d0402ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7f3c6d58fece6bb49e691d16873286e22ea06b568ef2ef6bb9b312b6e7c825(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8675177a9e7f5c6d8bc0e258b00454018c5e6bbe3153d568f16bce978d68413e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b287f4711840cbe2fe14b2a1c430222c21ad72e55e7a90a971f6de9801dc6ee2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a21a90528a6f5a33e6f5dca461ca3a576deb7e53e44bb0cf1d0cb543e6bc4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25b6480f301997c8491048d248b69c28aa5bb39132941c269c2277c06b0acf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4d637fec36c1bd7c9d16fc0b19bf0aedfcaac82ae795c3515ca3656fe11316(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb98728a07ed67a74eb843dbe38c2f89d3af7cc5c26bbee8554b508a2dc89aee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fefd8ac28c5a2b38d6461626f19f322a22a69b345bf5b38ba222b92617959ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08f1b960156d25f1a8ba5360c712be9b0dee652fb8d4e2c86ce1b28c8f9e788(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddb2b3ba64a26c24bebca8053cf3297cce11b6356a05932ad3b57ad5fb49780(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b8e2d9a0650005adc10c9667fba3d278a6ae795e035b5fbbd6f5a46ed44392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286c172113fc8fa0afeae14e0b78953889b464014936508bddb90e8947308234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9131c17298a7fef2b1f66a182399014fecee5964540364050ce8af204eb20e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86b347df4b85775fe1997aca7c20bdd27440d0af00f7f170bdb19cf8b872a3d(
    *,
    disk: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ad345eeeda3897e59573480d910bd17c9129d1f3756f8eb59a4c90bec2124a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8749ee7b36d1e180e6c4bdefd4cfadd9780ff6ab808afe55b08aa0cd65162d1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec49b19e76a4c81df62aa8275cb24f1e2cfbefb2b1f9ca9830b941b7a9cd7f7(
    value: typing.Optional[ComputeRegionDiskAsyncPrimaryDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63b9b98d080a2aa2d0a9b648fb13c0c3e1389b728aff0c2dc3d8bffd91f422c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    replica_zones: typing.Sequence[builtins.str],
    access_mode: typing.Optional[builtins.str] = None,
    async_primary_disk: typing.Optional[typing.Union[ComputeRegionDiskAsyncPrimaryDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    create_snapshot_before_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_snapshot_before_destroy_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disk_encryption_key: typing.Optional[typing.Union[ComputeRegionDiskDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionDiskGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    physical_block_size_bytes: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    provisioned_iops: typing.Optional[jsii.Number] = None,
    provisioned_throughput: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
    snapshot: typing.Optional[builtins.str] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeRegionDiskSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionDiskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b0536bc6cb6bbf06969bed012bf2c631d4b2224751301951ae281093e8043d(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ce93bc431802ac9493d649ba18f49b57f04159c7eb5df27378de916cf1597f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7811f17bc298e69f35ecd16bc79bae5d21f4d72cd58502e8cf9df5f4b43ccc33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f49f7713201d41c29c38bf8f0516ecfddfc230b0d517b00ea4b1ab11dc890f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c057fc54cbf1beb666e4d5ee0a01b218de1da4211c5ea666148f29fa06afbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e759daa39db6297832e986988b90322eef267f3ce4c345f704afd13664738c6(
    value: typing.Optional[ComputeRegionDiskDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aec82723e31cc2be59368bd69015bd3acb834ed6d60a96516f3c10d07abaefe(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14bd2c664ab41cf950616a3044e5be4a9f4cb63a89666d008025f4b0a90878b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad21c41c386669aa3ce7860277e895ca8f62d5659ae01edc40f0729e5073bef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8620623f77288bbd82a8312d544647312456aeefb49b4b5b426d1cb61cacc028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f79bdaf55fb9383524bf12def687e89b778c14a6b74625e43bffbbdc78b2b00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f4d9f46ec0584e9ebb64509fa11f9b344d6ccf5a0e29ffa4a7f0d863001047(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1b4348d0ee58583a8841dcf06bcf08cc7db4b316fb6bd2e62b1ac7d4d3c09b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionDiskGuestOsFeatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c33bd1c802535f7aa22647a131ecbcaac32c110aee0caa1ce8cbf447681c6ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68778d66ef644f2f8e98680c40c3bc8372b16f9814ff04626cecfdf60f0ce5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2739d34749319738b90041c06894ae6e87a360551e72816ee1f9346ffd9973f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskGuestOsFeatures]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286503b8d3dcdea8abb35d23a382ff570fec9a816b8b2036469307a666a696b2(
    *,
    raw_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2bcb576746709b31e90a16c111f46c6cdf2238b8afd7a8f50075383e5d55b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb93fe3b6368a4bac8c66a4f212156c7ed7630d00583baa132b7b990d70c100f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26edc05df208662e8479d2604b5ab03b76063ee832e3e78ac0bb2fc3d84e3f6f(
    value: typing.Optional[ComputeRegionDiskSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1a90c0b08dee31c8743857eceedfc2491c0128364c0a6433573712a28f7eab(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b18c3cc2342b46fa3f2c2ee01766d7735271aeb9a63808496fcb5d5f57203fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b0ed824a396cb3ca8739159d9cfc15bc26b0b91a642d687a71db4e55b0808b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4119f36b85dcc90059d38dee7fdb0101186988167b90180c31eebe21782eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bbdbe2438a20712ff27d3030f06495e6bb333f5f6711c022361a45175972a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8fc9f886268a17e91483c65794eeae8800996d5d2d2779601d50f6addd95b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionDiskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

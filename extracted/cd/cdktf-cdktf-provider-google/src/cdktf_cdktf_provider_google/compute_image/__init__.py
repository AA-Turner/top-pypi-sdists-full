r'''
# `google_compute_image`

Refer to the Terraform Registry for docs: [`google_compute_image`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image).
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


class ComputeImage(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImage",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image google_compute_image}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        family: typing.Optional[builtins.str] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_encryption_key: typing.Optional[typing.Union["ComputeImageImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        raw_disk: typing.Optional[typing.Union["ComputeImageRawDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_initial_state: typing.Optional[typing.Union["ComputeImageShieldedInstanceInitialState", typing.Dict[builtins.str, typing.Any]]] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_disk_encryption_key: typing.Optional[typing.Union["ComputeImageSourceDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_image: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeImageSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeImageSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image google_compute_image} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#name ComputeImage#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#description ComputeImage#description}
        :param disk_size_gb: Size of the image when restored onto a persistent disk (in GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#disk_size_gb ComputeImage#disk_size_gb}
        :param family: The name of the image family to which this image belongs. You can create disks by specifying an image family instead of a specific image name. The image family always returns its latest image that is not deprecated. The name of the image family must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#family ComputeImage#family}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#guest_os_features ComputeImage#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#id ComputeImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_encryption_key: image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#image_encryption_key ComputeImage#image_encryption_key}
        :param labels: Labels to apply to this Image. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#labels ComputeImage#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#licenses ComputeImage#licenses}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#project ComputeImage#project}.
        :param raw_disk: raw_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_disk ComputeImage#raw_disk}
        :param shielded_instance_initial_state: shielded_instance_initial_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#shielded_instance_initial_state ComputeImage#shielded_instance_initial_state}
        :param source_disk: The source disk to create this image based on. You must provide either this property or the rawDisk.source property but not both to create an image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk ComputeImage#source_disk}
        :param source_disk_encryption_key: source_disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk_encryption_key ComputeImage#source_disk_encryption_key}
        :param source_image: URL of the source image used to create this image. In order to create an image, you must provide the full or partial URL of one of the following: - The selfLink URL - This property - The rawDisk.source URL - The sourceDisk URL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image ComputeImage#source_image}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image_encryption_key ComputeImage#source_image_encryption_key}
        :param source_snapshot: URL of the source snapshot used to create this image. In order to create an image, you must provide the full or partial URL of one of the following: - The selfLink URL - This property - The sourceImage URL - The rawDisk.source URL - The sourceDisk URL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot ComputeImage#source_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot_encryption_key ComputeImage#source_snapshot_encryption_key}
        :param storage_locations: Cloud Storage bucket storage location of the image (regional or multi-regional). Reference link: https://cloud.google.com/compute/docs/reference/rest/v1/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#storage_locations ComputeImage#storage_locations}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#timeouts ComputeImage#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db186ccca621d3bba917597977be725110a6bc621e1a100cc2d2b8e4303075db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeImageConfig(
            name=name,
            description=description,
            disk_size_gb=disk_size_gb,
            family=family,
            guest_os_features=guest_os_features,
            id=id,
            image_encryption_key=image_encryption_key,
            labels=labels,
            licenses=licenses,
            project=project,
            raw_disk=raw_disk,
            shielded_instance_initial_state=shielded_instance_initial_state,
            source_disk=source_disk,
            source_disk_encryption_key=source_disk_encryption_key,
            source_image=source_image,
            source_image_encryption_key=source_image_encryption_key,
            source_snapshot=source_snapshot,
            source_snapshot_encryption_key=source_snapshot_encryption_key,
            storage_locations=storage_locations,
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
        '''Generates CDKTF code for importing a ComputeImage resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeImage to import.
        :param import_from_id: The id of the existing ComputeImage that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeImage to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4acfa9ff49357f21a852ab572dbfb5b4f14b03a03b5f6d1827ff81053a6adbbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGuestOsFeatures")
    def put_guest_os_features(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654954b892674c9be78a2b400933dba8326853524a58a46cace55fcdb56e2a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGuestOsFeatures", [value]))

    @jsii.member(jsii_name="putImageEncryptionKey")
    def put_image_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        value = ComputeImageImageEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putImageEncryptionKey", [value]))

    @jsii.member(jsii_name="putRawDisk")
    def put_raw_disk(
        self,
        *,
        source: builtins.str,
        container_type: typing.Optional[builtins.str] = None,
        sha1: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: The full Google Cloud Storage URL where disk storage is stored You must provide either this property or the sourceDisk property but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source ComputeImage#source}
        :param container_type: The format used to encode and transmit the block device, which should be TAR. This is just a container and transmission format and not a runtime format. Provided by the client when the disk image is created. Default value: "TAR" Possible values: ["TAR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#container_type ComputeImage#container_type}
        :param sha1: An optional SHA1 checksum of the disk image before unpackaging. This is provided by the client when the disk image is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#sha1 ComputeImage#sha1}
        '''
        value = ComputeImageRawDisk(
            source=source, container_type=container_type, sha1=sha1
        )

        return typing.cast(None, jsii.invoke(self, "putRawDisk", [value]))

    @jsii.member(jsii_name="putShieldedInstanceInitialState")
    def put_shielded_instance_initial_state(
        self,
        *,
        dbs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateDbs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dbxs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateDbxs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateKeks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pk: typing.Optional[typing.Union["ComputeImageShieldedInstanceInitialStatePk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbs: dbs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbs ComputeImage#dbs}
        :param dbxs: dbxs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbxs ComputeImage#dbxs}
        :param keks: keks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#keks ComputeImage#keks}
        :param pk: pk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#pk ComputeImage#pk}
        '''
        value = ComputeImageShieldedInstanceInitialState(
            dbs=dbs, dbxs=dbxs, keks=keks, pk=pk
        )

        return typing.cast(None, jsii.invoke(self, "putShieldedInstanceInitialState", [value]))

    @jsii.member(jsii_name="putSourceDiskEncryptionKey")
    def put_source_disk_encryption_key(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        value = ComputeImageSourceDiskEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceDiskEncryptionKey", [value]))

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
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        value = ComputeImageSourceImageEncryptionKey(
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
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        value = ComputeImageSourceSnapshotEncryptionKey(
            kms_key_self_link=kms_key_self_link,
            kms_key_service_account=kms_key_service_account,
            raw_key=raw_key,
            rsa_encrypted_key=rsa_encrypted_key,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#create ComputeImage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#delete ComputeImage#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#update ComputeImage#update}.
        '''
        value = ComputeImageTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetFamily")
    def reset_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFamily", []))

    @jsii.member(jsii_name="resetGuestOsFeatures")
    def reset_guest_os_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuestOsFeatures", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageEncryptionKey")
    def reset_image_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageEncryptionKey", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLicenses")
    def reset_licenses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenses", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRawDisk")
    def reset_raw_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawDisk", []))

    @jsii.member(jsii_name="resetShieldedInstanceInitialState")
    def reset_shielded_instance_initial_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShieldedInstanceInitialState", []))

    @jsii.member(jsii_name="resetSourceDisk")
    def reset_source_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDisk", []))

    @jsii.member(jsii_name="resetSourceDiskEncryptionKey")
    def reset_source_disk_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDiskEncryptionKey", []))

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

    @jsii.member(jsii_name="resetStorageLocations")
    def reset_storage_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageLocations", []))

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
    @jsii.member(jsii_name="archiveSizeBytes")
    def archive_size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "archiveSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeatures")
    def guest_os_features(self) -> "ComputeImageGuestOsFeaturesList":
        return typing.cast("ComputeImageGuestOsFeaturesList", jsii.get(self, "guestOsFeatures"))

    @builtins.property
    @jsii.member(jsii_name="imageEncryptionKey")
    def image_encryption_key(self) -> "ComputeImageImageEncryptionKeyOutputReference":
        return typing.cast("ComputeImageImageEncryptionKeyOutputReference", jsii.get(self, "imageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="labelFingerprint")
    def label_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labelFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="rawDisk")
    def raw_disk(self) -> "ComputeImageRawDiskOutputReference":
        return typing.cast("ComputeImageRawDiskOutputReference", jsii.get(self, "rawDisk"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceInitialState")
    def shielded_instance_initial_state(
        self,
    ) -> "ComputeImageShieldedInstanceInitialStateOutputReference":
        return typing.cast("ComputeImageShieldedInstanceInitialStateOutputReference", jsii.get(self, "shieldedInstanceInitialState"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskEncryptionKey")
    def source_disk_encryption_key(
        self,
    ) -> "ComputeImageSourceDiskEncryptionKeyOutputReference":
        return typing.cast("ComputeImageSourceDiskEncryptionKeyOutputReference", jsii.get(self, "sourceDiskEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKey")
    def source_image_encryption_key(
        self,
    ) -> "ComputeImageSourceImageEncryptionKeyOutputReference":
        return typing.cast("ComputeImageSourceImageEncryptionKeyOutputReference", jsii.get(self, "sourceImageEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKey")
    def source_snapshot_encryption_key(
        self,
    ) -> "ComputeImageSourceSnapshotEncryptionKeyOutputReference":
        return typing.cast("ComputeImageSourceSnapshotEncryptionKeyOutputReference", jsii.get(self, "sourceSnapshotEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeImageTimeoutsOutputReference":
        return typing.cast("ComputeImageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="familyInput")
    def family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyInput"))

    @builtins.property
    @jsii.member(jsii_name="guestOsFeaturesInput")
    def guest_os_features_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageGuestOsFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageGuestOsFeatures"]]], jsii.get(self, "guestOsFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageEncryptionKeyInput")
    def image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeImageImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeImageImageEncryptionKey"], jsii.get(self, "imageEncryptionKeyInput"))

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
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rawDiskInput")
    def raw_disk_input(self) -> typing.Optional["ComputeImageRawDisk"]:
        return typing.cast(typing.Optional["ComputeImageRawDisk"], jsii.get(self, "rawDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="shieldedInstanceInitialStateInput")
    def shielded_instance_initial_state_input(
        self,
    ) -> typing.Optional["ComputeImageShieldedInstanceInitialState"]:
        return typing.cast(typing.Optional["ComputeImageShieldedInstanceInitialState"], jsii.get(self, "shieldedInstanceInitialStateInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskEncryptionKeyInput")
    def source_disk_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeImageSourceDiskEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeImageSourceDiskEncryptionKey"], jsii.get(self, "sourceDiskEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDiskInput")
    def source_disk_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageEncryptionKeyInput")
    def source_image_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeImageSourceImageEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeImageSourceImageEncryptionKey"], jsii.get(self, "sourceImageEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceImageInput")
    def source_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceImageInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotEncryptionKeyInput")
    def source_snapshot_encryption_key_input(
        self,
    ) -> typing.Optional["ComputeImageSourceSnapshotEncryptionKey"]:
        return typing.cast(typing.Optional["ComputeImageSourceSnapshotEncryptionKey"], jsii.get(self, "sourceSnapshotEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotInput")
    def source_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="storageLocationsInput")
    def storage_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storageLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeImageTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeImageTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af8c280f01ceef7d99ead09cb409f9f5520031386229a93ccafbcb0ee63cb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6046846f1dcd4ce7a5ed5b9597e3dc754b3b7202f440aaf6937579a276511c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce61c4626cafeb49418707051d6dfb854c36bfa7f4064fc1f1e091f3dc3fc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e7f55438b63c10de62cbb174cf69ab539ed46efee0f463d93a8ad9386de3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2af7c73bb39be64e68c34678ceb0ec79e12f3b7f08195832c801989baed41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenses")
    def licenses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "licenses"))

    @licenses.setter
    def licenses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2309988435dbb09113ffe7102975e2002d1fc64dcabc171185e8888dbadda0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f035e3d37f82f3be9084868033e8b7c3c72d179c079d58b8b5d82b7f0cf3c411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999c1c724ed963ad4ac14b21af70b6ec7f75346273b23e4aeef7006ff17e2e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDisk")
    def source_disk(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDisk"))

    @source_disk.setter
    def source_disk(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd28798181098120ae373c473bbc61ca04ec5afb0e686c60fab2f7026359f94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceImage")
    def source_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceImage"))

    @source_image.setter
    def source_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecab956e5e3f93950633a62ba9f17a2e0d5e9e0056bec8014c42cf5a4c9cdab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba91037c4fded260fc7433abc697fe2696bc68b6501a9f734c9b6ace57cf53e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageLocations")
    def storage_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storageLocations"))

    @storage_locations.setter
    def storage_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71fd5c34c807c9d7d5a6cfd9fe58691676758d7b89be4426ba06b827ba62c123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageLocations", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageConfig",
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
        "disk_size_gb": "diskSizeGb",
        "family": "family",
        "guest_os_features": "guestOsFeatures",
        "id": "id",
        "image_encryption_key": "imageEncryptionKey",
        "labels": "labels",
        "licenses": "licenses",
        "project": "project",
        "raw_disk": "rawDisk",
        "shielded_instance_initial_state": "shieldedInstanceInitialState",
        "source_disk": "sourceDisk",
        "source_disk_encryption_key": "sourceDiskEncryptionKey",
        "source_image": "sourceImage",
        "source_image_encryption_key": "sourceImageEncryptionKey",
        "source_snapshot": "sourceSnapshot",
        "source_snapshot_encryption_key": "sourceSnapshotEncryptionKey",
        "storage_locations": "storageLocations",
        "timeouts": "timeouts",
    },
)
class ComputeImageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk_size_gb: typing.Optional[jsii.Number] = None,
        family: typing.Optional[builtins.str] = None,
        guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageGuestOsFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        image_encryption_key: typing.Optional[typing.Union["ComputeImageImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        raw_disk: typing.Optional[typing.Union["ComputeImageRawDisk", typing.Dict[builtins.str, typing.Any]]] = None,
        shielded_instance_initial_state: typing.Optional[typing.Union["ComputeImageShieldedInstanceInitialState", typing.Dict[builtins.str, typing.Any]]] = None,
        source_disk: typing.Optional[builtins.str] = None,
        source_disk_encryption_key: typing.Optional[typing.Union["ComputeImageSourceDiskEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_image: typing.Optional[builtins.str] = None,
        source_image_encryption_key: typing.Optional[typing.Union["ComputeImageSourceImageEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
        source_snapshot_encryption_key: typing.Optional[typing.Union["ComputeImageSourceSnapshotEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ComputeImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#name ComputeImage#name}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#description ComputeImage#description}
        :param disk_size_gb: Size of the image when restored onto a persistent disk (in GB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#disk_size_gb ComputeImage#disk_size_gb}
        :param family: The name of the image family to which this image belongs. You can create disks by specifying an image family instead of a specific image name. The image family always returns its latest image that is not deprecated. The name of the image family must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#family ComputeImage#family}
        :param guest_os_features: guest_os_features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#guest_os_features ComputeImage#guest_os_features}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#id ComputeImage#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_encryption_key: image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#image_encryption_key ComputeImage#image_encryption_key}
        :param labels: Labels to apply to this Image. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#labels ComputeImage#labels}
        :param licenses: Any applicable license URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#licenses ComputeImage#licenses}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#project ComputeImage#project}.
        :param raw_disk: raw_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_disk ComputeImage#raw_disk}
        :param shielded_instance_initial_state: shielded_instance_initial_state block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#shielded_instance_initial_state ComputeImage#shielded_instance_initial_state}
        :param source_disk: The source disk to create this image based on. You must provide either this property or the rawDisk.source property but not both to create an image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk ComputeImage#source_disk}
        :param source_disk_encryption_key: source_disk_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk_encryption_key ComputeImage#source_disk_encryption_key}
        :param source_image: URL of the source image used to create this image. In order to create an image, you must provide the full or partial URL of one of the following: - The selfLink URL - This property - The rawDisk.source URL - The sourceDisk URL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image ComputeImage#source_image}
        :param source_image_encryption_key: source_image_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image_encryption_key ComputeImage#source_image_encryption_key}
        :param source_snapshot: URL of the source snapshot used to create this image. In order to create an image, you must provide the full or partial URL of one of the following: - The selfLink URL - This property - The sourceImage URL - The rawDisk.source URL - The sourceDisk URL Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot ComputeImage#source_snapshot}
        :param source_snapshot_encryption_key: source_snapshot_encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot_encryption_key ComputeImage#source_snapshot_encryption_key}
        :param storage_locations: Cloud Storage bucket storage location of the image (regional or multi-regional). Reference link: https://cloud.google.com/compute/docs/reference/rest/v1/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#storage_locations ComputeImage#storage_locations}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#timeouts ComputeImage#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(image_encryption_key, dict):
            image_encryption_key = ComputeImageImageEncryptionKey(**image_encryption_key)
        if isinstance(raw_disk, dict):
            raw_disk = ComputeImageRawDisk(**raw_disk)
        if isinstance(shielded_instance_initial_state, dict):
            shielded_instance_initial_state = ComputeImageShieldedInstanceInitialState(**shielded_instance_initial_state)
        if isinstance(source_disk_encryption_key, dict):
            source_disk_encryption_key = ComputeImageSourceDiskEncryptionKey(**source_disk_encryption_key)
        if isinstance(source_image_encryption_key, dict):
            source_image_encryption_key = ComputeImageSourceImageEncryptionKey(**source_image_encryption_key)
        if isinstance(source_snapshot_encryption_key, dict):
            source_snapshot_encryption_key = ComputeImageSourceSnapshotEncryptionKey(**source_snapshot_encryption_key)
        if isinstance(timeouts, dict):
            timeouts = ComputeImageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26a0f8c1a850944817e1af06bd45347e21f727e580d26313512b76e639431f4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument guest_os_features", value=guest_os_features, expected_type=type_hints["guest_os_features"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_encryption_key", value=image_encryption_key, expected_type=type_hints["image_encryption_key"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument licenses", value=licenses, expected_type=type_hints["licenses"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument raw_disk", value=raw_disk, expected_type=type_hints["raw_disk"])
            check_type(argname="argument shielded_instance_initial_state", value=shielded_instance_initial_state, expected_type=type_hints["shielded_instance_initial_state"])
            check_type(argname="argument source_disk", value=source_disk, expected_type=type_hints["source_disk"])
            check_type(argname="argument source_disk_encryption_key", value=source_disk_encryption_key, expected_type=type_hints["source_disk_encryption_key"])
            check_type(argname="argument source_image", value=source_image, expected_type=type_hints["source_image"])
            check_type(argname="argument source_image_encryption_key", value=source_image_encryption_key, expected_type=type_hints["source_image_encryption_key"])
            check_type(argname="argument source_snapshot", value=source_snapshot, expected_type=type_hints["source_snapshot"])
            check_type(argname="argument source_snapshot_encryption_key", value=source_snapshot_encryption_key, expected_type=type_hints["source_snapshot_encryption_key"])
            check_type(argname="argument storage_locations", value=storage_locations, expected_type=type_hints["storage_locations"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if family is not None:
            self._values["family"] = family
        if guest_os_features is not None:
            self._values["guest_os_features"] = guest_os_features
        if id is not None:
            self._values["id"] = id
        if image_encryption_key is not None:
            self._values["image_encryption_key"] = image_encryption_key
        if labels is not None:
            self._values["labels"] = labels
        if licenses is not None:
            self._values["licenses"] = licenses
        if project is not None:
            self._values["project"] = project
        if raw_disk is not None:
            self._values["raw_disk"] = raw_disk
        if shielded_instance_initial_state is not None:
            self._values["shielded_instance_initial_state"] = shielded_instance_initial_state
        if source_disk is not None:
            self._values["source_disk"] = source_disk
        if source_disk_encryption_key is not None:
            self._values["source_disk_encryption_key"] = source_disk_encryption_key
        if source_image is not None:
            self._values["source_image"] = source_image
        if source_image_encryption_key is not None:
            self._values["source_image_encryption_key"] = source_image_encryption_key
        if source_snapshot is not None:
            self._values["source_snapshot"] = source_snapshot
        if source_snapshot_encryption_key is not None:
            self._values["source_snapshot_encryption_key"] = source_snapshot_encryption_key
        if storage_locations is not None:
            self._values["storage_locations"] = storage_locations
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
    def name(self) -> builtins.str:
        '''Name of the resource;

        provided by the client when the resource is
        created. The name must be 1-63 characters long, and comply with
        RFC1035. Specifically, the name must be 1-63 characters long and
        match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means
        the first character must be a lowercase letter, and all following
        characters must be a dash, lowercase letter, or digit, except the
        last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#name ComputeImage#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#description ComputeImage#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Size of the image when restored onto a persistent disk (in GB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#disk_size_gb ComputeImage#disk_size_gb}
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of the image family to which this image belongs.

        You can
        create disks by specifying an image family instead of a specific
        image name. The image family always returns its latest image that is
        not deprecated. The name of the image family must comply with
        RFC1035.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#family ComputeImage#family}
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def guest_os_features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageGuestOsFeatures"]]]:
        '''guest_os_features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#guest_os_features ComputeImage#guest_os_features}
        '''
        result = self._values.get("guest_os_features")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageGuestOsFeatures"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#id ComputeImage#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_encryption_key(self) -> typing.Optional["ComputeImageImageEncryptionKey"]:
        '''image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#image_encryption_key ComputeImage#image_encryption_key}
        '''
        result = self._values.get("image_encryption_key")
        return typing.cast(typing.Optional["ComputeImageImageEncryptionKey"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to this Image.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#labels ComputeImage#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def licenses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Any applicable license URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#licenses ComputeImage#licenses}
        '''
        result = self._values.get("licenses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#project ComputeImage#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_disk(self) -> typing.Optional["ComputeImageRawDisk"]:
        '''raw_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_disk ComputeImage#raw_disk}
        '''
        result = self._values.get("raw_disk")
        return typing.cast(typing.Optional["ComputeImageRawDisk"], result)

    @builtins.property
    def shielded_instance_initial_state(
        self,
    ) -> typing.Optional["ComputeImageShieldedInstanceInitialState"]:
        '''shielded_instance_initial_state block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#shielded_instance_initial_state ComputeImage#shielded_instance_initial_state}
        '''
        result = self._values.get("shielded_instance_initial_state")
        return typing.cast(typing.Optional["ComputeImageShieldedInstanceInitialState"], result)

    @builtins.property
    def source_disk(self) -> typing.Optional[builtins.str]:
        '''The source disk to create this image based on.

        You must provide either this property or the
        rawDisk.source property but not both to create an image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk ComputeImage#source_disk}
        '''
        result = self._values.get("source_disk")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_disk_encryption_key(
        self,
    ) -> typing.Optional["ComputeImageSourceDiskEncryptionKey"]:
        '''source_disk_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_disk_encryption_key ComputeImage#source_disk_encryption_key}
        '''
        result = self._values.get("source_disk_encryption_key")
        return typing.cast(typing.Optional["ComputeImageSourceDiskEncryptionKey"], result)

    @builtins.property
    def source_image(self) -> typing.Optional[builtins.str]:
        '''URL of the source image used to create this image.

        In order to create an image, you must provide the full or partial
        URL of one of the following:

        - The selfLink URL
        - This property
        - The rawDisk.source URL
        - The sourceDisk URL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image ComputeImage#source_image}
        '''
        result = self._values.get("source_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_image_encryption_key(
        self,
    ) -> typing.Optional["ComputeImageSourceImageEncryptionKey"]:
        '''source_image_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_image_encryption_key ComputeImage#source_image_encryption_key}
        '''
        result = self._values.get("source_image_encryption_key")
        return typing.cast(typing.Optional["ComputeImageSourceImageEncryptionKey"], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''URL of the source snapshot used to create this image.

        In order to create an image, you must provide the full or partial URL of one of the following:

        - The selfLink URL
        - This property
        - The sourceImage URL
        - The rawDisk.source URL
        - The sourceDisk URL

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot ComputeImage#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot_encryption_key(
        self,
    ) -> typing.Optional["ComputeImageSourceSnapshotEncryptionKey"]:
        '''source_snapshot_encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source_snapshot_encryption_key ComputeImage#source_snapshot_encryption_key}
        '''
        result = self._values.get("source_snapshot_encryption_key")
        return typing.cast(typing.Optional["ComputeImageSourceSnapshotEncryptionKey"], result)

    @builtins.property
    def storage_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage bucket storage location of the image (regional or multi-regional). Reference link: https://cloud.google.com/compute/docs/reference/rest/v1/images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#storage_locations ComputeImage#storage_locations}
        '''
        result = self._values.get("storage_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeImageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#timeouts ComputeImage#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeImageTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageGuestOsFeatures",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class ComputeImageGuestOsFeatures:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: The type of supported feature. Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options. Possible values: ["MULTI_IP_SUBNET", "SECURE_BOOT", "SEV_CAPABLE", "UEFI_COMPATIBLE", "VIRTIO_SCSI_MULTIQUEUE", "WINDOWS", "GVNIC", "IDPF", "SEV_LIVE_MIGRATABLE", "SEV_SNP_CAPABLE", "SUSPEND_RESUME_COMPATIBLE", "TDX_CAPABLE", "SEV_LIVE_MIGRATABLE_V2"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#type ComputeImage#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb20a727ca1621aec6a441ceee139e627efdf844c3333cdbe4ba9c56c27f37fb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of supported feature.

        Read `Enabling guest operating system features <https://cloud.google.com/compute/docs/images/create-delete-deprecate-private-images#guest-os-features>`_ to see a list of available options. Possible values: ["MULTI_IP_SUBNET", "SECURE_BOOT", "SEV_CAPABLE", "UEFI_COMPATIBLE", "VIRTIO_SCSI_MULTIQUEUE", "WINDOWS", "GVNIC", "IDPF", "SEV_LIVE_MIGRATABLE", "SEV_SNP_CAPABLE", "SUSPEND_RESUME_COMPATIBLE", "TDX_CAPABLE", "SEV_LIVE_MIGRATABLE_V2"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#type ComputeImage#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageGuestOsFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageGuestOsFeaturesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageGuestOsFeaturesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__137e74e897126c6cbb05e4b49a1a3bd305f1dff01ee8d83d3b09941565e5dd0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeImageGuestOsFeaturesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cbcb41fd3dfb5021a0e188adf0f2ae2e594bd4875ba613a1b5f569e9d1d8c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeImageGuestOsFeaturesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214168275c8edc1debf0ee2bc144244c232d692c16bb9504f612ad0a4eb7003c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de68ad4994cc45bf50265e4e4bcf885258b60f83785bbacc0490aff2aa3a4689)
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
            type_hints = typing.get_type_hints(_typecheckingstub__798de1ea896a624acf6ec6fb5914ae79fe6079d6885f3bcabf078edd57eff4da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageGuestOsFeatures]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageGuestOsFeatures]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageGuestOsFeatures]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99b7c25307489eaddcecbee4e4a613eacc9170350e039b070300ebe74392abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeImageGuestOsFeaturesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageGuestOsFeaturesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef3c513ecbaee181e2887e63763f57c97f6390dfb86041b2a6ae8170bbdf2a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b493ea927cd46bcb462748dc494158a1f61ee6a05a380e32076bafa0162c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageGuestOsFeatures]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageGuestOsFeatures]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageGuestOsFeatures]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa7dbb465835505d22ef13ab2fd273212dfa691735c673497802871561da6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeImageImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key that is stored in Google Cloud KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d156c62a17a9a712dfb844ba4b1cd40ce1015e6a8af2aa9bf773fb328d6f7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service
        account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52345bf7f16614e5b4b8ef09b3e4b237de95d6ee51f34d560b1c495ffe2fc4c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7854c4defaa56de415ab30c8e0e29e094ac9bf403d744e56453fb2eabc7c0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2b494009d00b647cb94040f418fa0f92ec0fb80a27c5377103e8077ff94314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0e4a7d14342655ebbfb406d9983a18374de858d47cc3f9ee5489c4d86be5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d6eed00c8570a8079ad9fd7fad1ea2c43ae071a85f69a4a92daeca02ec3327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeImageImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeImageImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c7f7773e901455017a23b513034f51c1237ea49b9e26e8a666862c40deb44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageRawDisk",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "container_type": "containerType",
        "sha1": "sha1",
    },
)
class ComputeImageRawDisk:
    def __init__(
        self,
        *,
        source: builtins.str,
        container_type: typing.Optional[builtins.str] = None,
        sha1: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: The full Google Cloud Storage URL where disk storage is stored You must provide either this property or the sourceDisk property but not both. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source ComputeImage#source}
        :param container_type: The format used to encode and transmit the block device, which should be TAR. This is just a container and transmission format and not a runtime format. Provided by the client when the disk image is created. Default value: "TAR" Possible values: ["TAR"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#container_type ComputeImage#container_type}
        :param sha1: An optional SHA1 checksum of the disk image before unpackaging. This is provided by the client when the disk image is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#sha1 ComputeImage#sha1}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e8a9ddd5bbdb138a52dc6deb7479c6eaf30521203cac975ffb6e1d3568875a)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument container_type", value=container_type, expected_type=type_hints["container_type"])
            check_type(argname="argument sha1", value=sha1, expected_type=type_hints["sha1"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if container_type is not None:
            self._values["container_type"] = container_type
        if sha1 is not None:
            self._values["sha1"] = sha1

    @builtins.property
    def source(self) -> builtins.str:
        '''The full Google Cloud Storage URL where disk storage is stored You must provide either this property or the sourceDisk property but not both.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#source ComputeImage#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_type(self) -> typing.Optional[builtins.str]:
        '''The format used to encode and transmit the block device, which should be TAR.

        This is just a container and transmission format
        and not a runtime format. Provided by the client when the disk
        image is created. Default value: "TAR" Possible values: ["TAR"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#container_type ComputeImage#container_type}
        '''
        result = self._values.get("container_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sha1(self) -> typing.Optional[builtins.str]:
        '''An optional SHA1 checksum of the disk image before unpackaging.

        This is provided by the client when the disk image is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#sha1 ComputeImage#sha1}
        '''
        result = self._values.get("sha1")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageRawDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageRawDiskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageRawDiskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd7a27c31078f6a20a0dbe2c80ca77545be18d2f6f794d543935735720e547a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerType")
    def reset_container_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerType", []))

    @jsii.member(jsii_name="resetSha1")
    def reset_sha1(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha1", []))

    @builtins.property
    @jsii.member(jsii_name="containerTypeInput")
    def container_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sha1Input")
    def sha1_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha1Input"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="containerType")
    def container_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerType"))

    @container_type.setter
    def container_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacefa3fc8cf7858ea2025fcb456b7498351d5a65d5c815243a3231680c2e70c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sha1")
    def sha1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha1"))

    @sha1.setter
    def sha1(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca462bf9fb80f6e5337c55ce7b552a73365eac587358556e7ebde6e89b68210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha1", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ccabbaf47cd40486c49da57d7bdf374505db9c214a0bf4de53a9dd6c22ffc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeImageRawDisk]:
        return typing.cast(typing.Optional[ComputeImageRawDisk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeImageRawDisk]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054292c082e2ff9afde90f14f93fa92daadc190ab5a812a8faa344b86196e2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialState",
    jsii_struct_bases=[],
    name_mapping={"dbs": "dbs", "dbxs": "dbxs", "keks": "keks", "pk": "pk"},
)
class ComputeImageShieldedInstanceInitialState:
    def __init__(
        self,
        *,
        dbs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateDbs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dbxs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateDbxs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeImageShieldedInstanceInitialStateKeks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pk: typing.Optional[typing.Union["ComputeImageShieldedInstanceInitialStatePk", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dbs: dbs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbs ComputeImage#dbs}
        :param dbxs: dbxs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbxs ComputeImage#dbxs}
        :param keks: keks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#keks ComputeImage#keks}
        :param pk: pk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#pk ComputeImage#pk}
        '''
        if isinstance(pk, dict):
            pk = ComputeImageShieldedInstanceInitialStatePk(**pk)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75a0af0a945498f4c115689c6c14ce6592636a12f0822fb54e239d319e029cf)
            check_type(argname="argument dbs", value=dbs, expected_type=type_hints["dbs"])
            check_type(argname="argument dbxs", value=dbxs, expected_type=type_hints["dbxs"])
            check_type(argname="argument keks", value=keks, expected_type=type_hints["keks"])
            check_type(argname="argument pk", value=pk, expected_type=type_hints["pk"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dbs is not None:
            self._values["dbs"] = dbs
        if dbxs is not None:
            self._values["dbxs"] = dbxs
        if keks is not None:
            self._values["keks"] = keks
        if pk is not None:
            self._values["pk"] = pk

    @builtins.property
    def dbs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateDbs"]]]:
        '''dbs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbs ComputeImage#dbs}
        '''
        result = self._values.get("dbs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateDbs"]]], result)

    @builtins.property
    def dbxs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateDbxs"]]]:
        '''dbxs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#dbxs ComputeImage#dbxs}
        '''
        result = self._values.get("dbxs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateDbxs"]]], result)

    @builtins.property
    def keks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateKeks"]]]:
        '''keks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#keks ComputeImage#keks}
        '''
        result = self._values.get("keks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeImageShieldedInstanceInitialStateKeks"]]], result)

    @builtins.property
    def pk(self) -> typing.Optional["ComputeImageShieldedInstanceInitialStatePk"]:
        '''pk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#pk ComputeImage#pk}
        '''
        result = self._values.get("pk")
        return typing.cast(typing.Optional["ComputeImageShieldedInstanceInitialStatePk"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageShieldedInstanceInitialState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbs",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "file_type": "fileType"},
)
class ComputeImageShieldedInstanceInitialStateDbs:
    def __init__(
        self,
        *,
        content: builtins.str,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The raw content in the secure keys file. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        :param file_type: The file type of source file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9955449bfc8b695894ba4ce247fd35627e5edc6dd32a1729a9401c0f1ccd8efc)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def content(self) -> builtins.str:
        '''The raw content in the secure keys file.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''The file type of source file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageShieldedInstanceInitialStateDbs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageShieldedInstanceInitialStateDbsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__057e9e77d445150e3692cde6edd9be78e7a7a68a111a1dc2be6ac31a68b2be06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeImageShieldedInstanceInitialStateDbsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b1a3767d9d8458af4f1e7f8b46e22c5a13eafd0248a3a78bfc3f2583263414)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeImageShieldedInstanceInitialStateDbsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff30e0345f2eab05770f7602281c028c623d7a85c8d98e314fe1bd9598bad294)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddf56984d39be67113edcf72f7d7bd30e82f2855b368488b125c702efb876ae5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48465aff748a211077457df9a060c3707bde81f62aadbad3867eb5fd8c6b973a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e81b9b03ee57123cffca15f2c259755549a64534e1686b6e708598fd7cd0d2aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeImageShieldedInstanceInitialStateDbsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b973f2d5e5553db1bdfad786ae7ac782c80b4277a5ce2f693c41dcba9888c6f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de422af7a02dab20147a4ce48c0002cd221872503e4877f96ea8b83811551894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21d63d05f7a66709a974bc6e3b8121a224b034e1267fa893f011f5bfaa15b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56371233909682cdb292cf42db98c7a4b73a9abdae29e70036f08637da7f0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbxs",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "file_type": "fileType"},
)
class ComputeImageShieldedInstanceInitialStateDbxs:
    def __init__(
        self,
        *,
        content: builtins.str,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The raw content in the secure keys file. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        :param file_type: The file type of source file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc5f95ab6566cc3e720f2ec1c19a5f2f6d33b3e487d178a5b1b834c86c1312f)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def content(self) -> builtins.str:
        '''The raw content in the secure keys file.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''The file type of source file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageShieldedInstanceInitialStateDbxs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageShieldedInstanceInitialStateDbxsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbxsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cfee39ccb26939dff000dca041de333e4043f73da26da69c61fb03753587d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeImageShieldedInstanceInitialStateDbxsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b06d5c661d9f5407d60c6dd19ed1f172b7fe37bfc842fe2d96cc0ed517416f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeImageShieldedInstanceInitialStateDbxsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85de2505cd232bc26fa82f8c13ed16cdef070dc9e8f1a89c897595a816d5bc7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbdbbc3fe2940df86281bfba350fdcf49d24ba2eba53161e9467ef401625071)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6c5f26875fdcdb2f7ef7b2647da8ad4d36a36c0632c398ceb9aae075ec90881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c682e6ca27cdc165311ae2d22dc4c1315e998669bb2584148b50605a5f7860a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeImageShieldedInstanceInitialStateDbxsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateDbxsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b217d5868025355e8bfd462cc05ddce68fabc74516f21d6f22bed055283deaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a54e5f8bf32310ff6918f3535eeff928b78bbc180a80a9eb7bf231c8392fcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0f9b3851dfcbc6b854861c4273eae16772ccf30666905b8616432a5d7bf8c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbxs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbxs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbxs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3540e4388293f5c27844f923c6def04bb03187629f12abca53c6c0bf7ccade1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateKeks",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "file_type": "fileType"},
)
class ComputeImageShieldedInstanceInitialStateKeks:
    def __init__(
        self,
        *,
        content: builtins.str,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The raw content in the secure keys file. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        :param file_type: The file type of source file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f6e59890eedfae02049e7fa793302e88edfdd7bf2568c381a303e32b60090d)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def content(self) -> builtins.str:
        '''The raw content in the secure keys file.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''The file type of source file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageShieldedInstanceInitialStateKeks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageShieldedInstanceInitialStateKeksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateKeksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__258b580099dd734a79731d5b999765b3c6e61067e9e0e63900bd611ff9748b9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeImageShieldedInstanceInitialStateKeksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8dcd04e12a7044ea5d2f5fa892fb49b5f09b966a8fcaa679e41163d37b56974)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeImageShieldedInstanceInitialStateKeksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3b0875f4132eb6ab58052971ae7fc89f507767a160af23b44ca50368c491f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96b4c7200a2e795cd75b3c8e8602791326644c6967c8b61590b53fab3bb4b790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bee7dfdaba17226b00ea08f448ebe33c00ca2bf2c31bfe3bc36212934458607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f5685e15beb8129395b8dc36b0ef34ac1706326d39f7720dc0e7fa0d5bab4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeImageShieldedInstanceInitialStateKeksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateKeksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2069bc587f69ce5761f460fdffb574255cacce9137820bfe9ee4e2a677547ea8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41d89934c32c2253356ae4fff0a356395ca9352539606768935643eb6ec920e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ceb6776a93df4ad65f7af05ae2b3685c552316e4b88dd20bc7235deb5f8014f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateKeks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateKeks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateKeks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d68da3cf733c815490803a689939930f8d9d0fe1565736c049ff89688553665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeImageShieldedInstanceInitialStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d340e54d80ade5ef1d9d9b23912adee605e4970f230b3f7742b9e6d8324956f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDbs")
    def put_dbs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18273595af8c9b048041bcc1fc74ee40368cf86699167631de39ef5ef371a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDbs", [value]))

    @jsii.member(jsii_name="putDbxs")
    def put_dbxs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbxs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942893922a3d70751fcfd6ee544d55e9bbb34b544deebbcb3ddd42ea050fa576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDbxs", [value]))

    @jsii.member(jsii_name="putKeks")
    def put_keks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateKeks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0cba4331dd77b702635d81e60cbf21a2cf5742311cec7e07ea9703592b9f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeks", [value]))

    @jsii.member(jsii_name="putPk")
    def put_pk(
        self,
        *,
        content: builtins.str,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The raw content in the secure keys file. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        :param file_type: The file type of source file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        value = ComputeImageShieldedInstanceInitialStatePk(
            content=content, file_type=file_type
        )

        return typing.cast(None, jsii.invoke(self, "putPk", [value]))

    @jsii.member(jsii_name="resetDbs")
    def reset_dbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbs", []))

    @jsii.member(jsii_name="resetDbxs")
    def reset_dbxs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbxs", []))

    @jsii.member(jsii_name="resetKeks")
    def reset_keks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeks", []))

    @jsii.member(jsii_name="resetPk")
    def reset_pk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPk", []))

    @builtins.property
    @jsii.member(jsii_name="dbs")
    def dbs(self) -> ComputeImageShieldedInstanceInitialStateDbsList:
        return typing.cast(ComputeImageShieldedInstanceInitialStateDbsList, jsii.get(self, "dbs"))

    @builtins.property
    @jsii.member(jsii_name="dbxs")
    def dbxs(self) -> ComputeImageShieldedInstanceInitialStateDbxsList:
        return typing.cast(ComputeImageShieldedInstanceInitialStateDbxsList, jsii.get(self, "dbxs"))

    @builtins.property
    @jsii.member(jsii_name="keks")
    def keks(self) -> ComputeImageShieldedInstanceInitialStateKeksList:
        return typing.cast(ComputeImageShieldedInstanceInitialStateKeksList, jsii.get(self, "keks"))

    @builtins.property
    @jsii.member(jsii_name="pk")
    def pk(self) -> "ComputeImageShieldedInstanceInitialStatePkOutputReference":
        return typing.cast("ComputeImageShieldedInstanceInitialStatePkOutputReference", jsii.get(self, "pk"))

    @builtins.property
    @jsii.member(jsii_name="dbsInput")
    def dbs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]], jsii.get(self, "dbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbxsInput")
    def dbxs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]], jsii.get(self, "dbxsInput"))

    @builtins.property
    @jsii.member(jsii_name="keksInput")
    def keks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]], jsii.get(self, "keksInput"))

    @builtins.property
    @jsii.member(jsii_name="pkInput")
    def pk_input(self) -> typing.Optional["ComputeImageShieldedInstanceInitialStatePk"]:
        return typing.cast(typing.Optional["ComputeImageShieldedInstanceInitialStatePk"], jsii.get(self, "pkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeImageShieldedInstanceInitialState]:
        return typing.cast(typing.Optional[ComputeImageShieldedInstanceInitialState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageShieldedInstanceInitialState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6c03e0a4f06b8e3aafc196e34807be51b66d631ba6ecd3bb4a3b248e55983d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStatePk",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "file_type": "fileType"},
)
class ComputeImageShieldedInstanceInitialStatePk:
    def __init__(
        self,
        *,
        content: builtins.str,
        file_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: The raw content in the secure keys file. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        :param file_type: The file type of source file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5929c31d2a54231a458f38183556215422b3c0dc099889669e1cef8300dd4d)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file_type", value=file_type, expected_type=type_hints["file_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
        }
        if file_type is not None:
            self._values["file_type"] = file_type

    @builtins.property
    def content(self) -> builtins.str:
        '''The raw content in the secure keys file.

        A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#content ComputeImage#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_type(self) -> typing.Optional[builtins.str]:
        '''The file type of source file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#file_type ComputeImage#file_type}
        '''
        result = self._values.get("file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageShieldedInstanceInitialStatePk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageShieldedInstanceInitialStatePkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageShieldedInstanceInitialStatePkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__178b496e3f1386c79b8727f5611c651ba8a3859d2dc0ca9429991f78adbfe42b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileType")
    def reset_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileType", []))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTypeInput")
    def file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a022dfbea2e9747781f228781f2efa99fd329e1de878fce4200e43a0aa7b63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileType")
    def file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileType"))

    @file_type.setter
    def file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e219ac2b917a213444834bd1c8e5458c6df6cb73a4d6d9ecd338c29d9e78d356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeImageShieldedInstanceInitialStatePk]:
        return typing.cast(typing.Optional[ComputeImageShieldedInstanceInitialStatePk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageShieldedInstanceInitialStatePk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1310178ac536add3db4579376c34a9002a0d687032743968838547a103d2ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceDiskEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeImageSourceDiskEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a9f24261f806f88a1d4388866b7cd3ceeff9a9199965696e2d65a138b1fb69)
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
        '''The self link of the encryption key used to decrypt this resource.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service
        account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        You can provide either the rawKey or the rsaEncryptedKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageSourceDiskEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageSourceDiskEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceDiskEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63171eac660648da4091014185c2ec8aa9473fc1731a3407ec460a2796b83945)
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
            type_hints = typing.get_type_hints(_typecheckingstub__080e108c804da17e9d4870ebd516325b59fbb826f74ca463d5b81d863774b219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f845305093a7372a42321bb78b11044018032d3dcd0364cf6e7f3341c4569b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f509520cc31422deb5d07c56ab8bbf45db1ae4297b2af647c2a759ab9ecb615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc05f2e41d4f9b110d829717c05f6eae1bd4261915bc461d54e54f9285e310b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeImageSourceDiskEncryptionKey]:
        return typing.cast(typing.Optional[ComputeImageSourceDiskEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageSourceDiskEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22828d913aceb00b45cb37b15faa0bde6d07024db0463448c3aac983ce2fd8bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceImageEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeImageSourceImageEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4ca63c01ec91e16b649f224cef2ceaa34731beaf7c92ae0dfbb84c2c9ef903)
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
        '''The self link of the encryption key used to decrypt this resource.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service
        account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        You can provide either the rawKey or the rsaEncryptedKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageSourceImageEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageSourceImageEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceImageEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c8fc7bbca93a20ee7d2cde9e1c6d160834982518b9008e63411536344130b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c9a80d04787b1dd0590b391c3026ac52e677a04b8349137e0f70fdde0d55649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4458e9191898156b22fda8e192467804ca9de67ca48e0f085d0eb585c4749d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd90bdebd352b592aec1149e5267787dbe84718738de910fba02d66d9d65baf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bdbec854387d9e63937fc0f1ac71557dfa75dc0a5a85c775cff13898b5a59e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeImageSourceImageEncryptionKey]:
        return typing.cast(typing.Optional[ComputeImageSourceImageEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageSourceImageEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b869acee35b15ea71d3867442ddddd070309b1d2e4426a52db9075abc6f7fd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceSnapshotEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_self_link": "kmsKeySelfLink",
        "kms_key_service_account": "kmsKeyServiceAccount",
        "raw_key": "rawKey",
        "rsa_encrypted_key": "rsaEncryptedKey",
    },
)
class ComputeImageSourceSnapshotEncryptionKey:
    def __init__(
        self,
        *,
        kms_key_self_link: typing.Optional[builtins.str] = None,
        kms_key_service_account: typing.Optional[builtins.str] = None,
        raw_key: typing.Optional[builtins.str] = None,
        rsa_encrypted_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_self_link: The self link of the encryption key used to decrypt this resource. Also called KmsKeyName in the cloud console. Your project's Compute Engine System service account ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have 'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature. See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        :param kms_key_service_account: The service account being used for the encryption request for the given KMS key. If absent, the Compute Engine default service account is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        :param raw_key: Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        :param rsa_encrypted_key: Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource. You can provide either the rawKey or the rsaEncryptedKey. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b586ec884e1e430026dcc3320846c8595bee4ea166f2e665471457778930b6)
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
        '''The self link of the encryption key used to decrypt this resource.

        Also called KmsKeyName
        in the cloud console. Your project's Compute Engine System service account
        ('service-{{PROJECT_NUMBER}}@compute-system.iam.gserviceaccount.com') must have
        'roles/cloudkms.cryptoKeyEncrypterDecrypter' to use this feature.
        See https://cloud.google.com/compute/docs/disks/customer-managed-encryption#encrypt_a_new_persistent_disk_with_your_own_keys

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_self_link ComputeImage#kms_key_self_link}
        '''
        result = self._values.get("kms_key_self_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_service_account(self) -> typing.Optional[builtins.str]:
        '''The service account being used for the encryption request for the given KMS key.

        If absent, the Compute Engine default service
        account is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#kms_key_service_account ComputeImage#kms_key_service_account}
        '''
        result = self._values.get("kms_key_service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a 256-bit customer-supplied encryption key, encoded in RFC 4648 base64 to either encrypt or decrypt this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#raw_key ComputeImage#raw_key}
        '''
        result = self._values.get("raw_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_encrypted_key(self) -> typing.Optional[builtins.str]:
        '''Specifies an RFC 4648 base64 encoded, RSA-wrapped 2048-bit customer-supplied encryption key to either encrypt or decrypt this resource.

        You can provide either the rawKey or the rsaEncryptedKey.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#rsa_encrypted_key ComputeImage#rsa_encrypted_key}
        '''
        result = self._values.get("rsa_encrypted_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageSourceSnapshotEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageSourceSnapshotEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageSourceSnapshotEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68248131990c4a4647714a7dc21ed446c528db1fa6e9de71c35a8563d58d28e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0634cb474b79d176ff5744fc9b9e0fa46422da5e17d7d13e0f0849332fac799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeySelfLink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyServiceAccount")
    def kms_key_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyServiceAccount"))

    @kms_key_service_account.setter
    def kms_key_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21ac88cda35a0b061a466ba35cccdb2e8dafe5ab86fa2fad17be43e975f34a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rawKey")
    def raw_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawKey"))

    @raw_key.setter
    def raw_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca339ddaac65789d1cc05b8e5d83cfb2dcb321cfd3d63bb418c95f12a1311542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaEncryptedKey")
    def rsa_encrypted_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaEncryptedKey"))

    @rsa_encrypted_key.setter
    def rsa_encrypted_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2faf74068c952ac12ecb6455fc8dbb11db5c8c94e0e5cc0313069416e5178737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaEncryptedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeImageSourceSnapshotEncryptionKey]:
        return typing.cast(typing.Optional[ComputeImageSourceSnapshotEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeImageSourceSnapshotEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abb234b5cd53c96b3994f2e53eeb811295c50e9605a4fd9bc8566a5eba9218a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeImageTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#create ComputeImage#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#delete ComputeImage#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#update ComputeImage#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fff255e313c8b5f71de2d2020ad8e7c69bdf14c8f9ee704236219944a689a07)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#create ComputeImage#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#delete ComputeImage#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_image#update ComputeImage#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeImageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeImageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeImage.ComputeImageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e1ead5f4cac4b8b75c7f2fa2427aaac008f264d58d955e8e1dbcabe8231be8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e962a4a927561aa758dfa39bf65848e34c63fb7bde26805a161766ad208f90f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3eb2229ef2904fed9c9606bb401697e5e86d892bfd19929986bb16153d6b6cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f09db7c6cf48b14e806280074f18ae7527a2c2b35f563d56e6b079b1c0621d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c48c6c16e65d615437f81583e285c902431540f4bccbceb3ca647d63f1db5fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeImage",
    "ComputeImageConfig",
    "ComputeImageGuestOsFeatures",
    "ComputeImageGuestOsFeaturesList",
    "ComputeImageGuestOsFeaturesOutputReference",
    "ComputeImageImageEncryptionKey",
    "ComputeImageImageEncryptionKeyOutputReference",
    "ComputeImageRawDisk",
    "ComputeImageRawDiskOutputReference",
    "ComputeImageShieldedInstanceInitialState",
    "ComputeImageShieldedInstanceInitialStateDbs",
    "ComputeImageShieldedInstanceInitialStateDbsList",
    "ComputeImageShieldedInstanceInitialStateDbsOutputReference",
    "ComputeImageShieldedInstanceInitialStateDbxs",
    "ComputeImageShieldedInstanceInitialStateDbxsList",
    "ComputeImageShieldedInstanceInitialStateDbxsOutputReference",
    "ComputeImageShieldedInstanceInitialStateKeks",
    "ComputeImageShieldedInstanceInitialStateKeksList",
    "ComputeImageShieldedInstanceInitialStateKeksOutputReference",
    "ComputeImageShieldedInstanceInitialStateOutputReference",
    "ComputeImageShieldedInstanceInitialStatePk",
    "ComputeImageShieldedInstanceInitialStatePkOutputReference",
    "ComputeImageSourceDiskEncryptionKey",
    "ComputeImageSourceDiskEncryptionKeyOutputReference",
    "ComputeImageSourceImageEncryptionKey",
    "ComputeImageSourceImageEncryptionKeyOutputReference",
    "ComputeImageSourceSnapshotEncryptionKey",
    "ComputeImageSourceSnapshotEncryptionKeyOutputReference",
    "ComputeImageTimeouts",
    "ComputeImageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db186ccca621d3bba917597977be725110a6bc621e1a100cc2d2b8e4303075db(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    family: typing.Optional[builtins.str] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_encryption_key: typing.Optional[typing.Union[ComputeImageImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    raw_disk: typing.Optional[typing.Union[ComputeImageRawDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_initial_state: typing.Optional[typing.Union[ComputeImageShieldedInstanceInitialState, typing.Dict[builtins.str, typing.Any]]] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_disk_encryption_key: typing.Optional[typing.Union[ComputeImageSourceDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_image: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeImageSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeImageSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4acfa9ff49357f21a852ab572dbfb5b4f14b03a03b5f6d1827ff81053a6adbbf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654954b892674c9be78a2b400933dba8326853524a58a46cace55fcdb56e2a07(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8c280f01ceef7d99ead09cb409f9f5520031386229a93ccafbcb0ee63cb3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6046846f1dcd4ce7a5ed5b9597e3dc754b3b7202f440aaf6937579a276511c2a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce61c4626cafeb49418707051d6dfb854c36bfa7f4064fc1f1e091f3dc3fc95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e7f55438b63c10de62cbb174cf69ab539ed46efee0f463d93a8ad9386de3f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2af7c73bb39be64e68c34678ceb0ec79e12f3b7f08195832c801989baed41f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2309988435dbb09113ffe7102975e2002d1fc64dcabc171185e8888dbadda0b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f035e3d37f82f3be9084868033e8b7c3c72d179c079d58b8b5d82b7f0cf3c411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999c1c724ed963ad4ac14b21af70b6ec7f75346273b23e4aeef7006ff17e2e33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd28798181098120ae373c473bbc61ca04ec5afb0e686c60fab2f7026359f94f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecab956e5e3f93950633a62ba9f17a2e0d5e9e0056bec8014c42cf5a4c9cdab0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba91037c4fded260fc7433abc697fe2696bc68b6501a9f734c9b6ace57cf53e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71fd5c34c807c9d7d5a6cfd9fe58691676758d7b89be4426ba06b827ba62c123(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26a0f8c1a850944817e1af06bd45347e21f727e580d26313512b76e639431f4(
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
    disk_size_gb: typing.Optional[jsii.Number] = None,
    family: typing.Optional[builtins.str] = None,
    guest_os_features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageGuestOsFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    image_encryption_key: typing.Optional[typing.Union[ComputeImageImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    licenses: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    raw_disk: typing.Optional[typing.Union[ComputeImageRawDisk, typing.Dict[builtins.str, typing.Any]]] = None,
    shielded_instance_initial_state: typing.Optional[typing.Union[ComputeImageShieldedInstanceInitialState, typing.Dict[builtins.str, typing.Any]]] = None,
    source_disk: typing.Optional[builtins.str] = None,
    source_disk_encryption_key: typing.Optional[typing.Union[ComputeImageSourceDiskEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_image: typing.Optional[builtins.str] = None,
    source_image_encryption_key: typing.Optional[typing.Union[ComputeImageSourceImageEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
    source_snapshot_encryption_key: typing.Optional[typing.Union[ComputeImageSourceSnapshotEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ComputeImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb20a727ca1621aec6a441ceee139e627efdf844c3333cdbe4ba9c56c27f37fb(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137e74e897126c6cbb05e4b49a1a3bd305f1dff01ee8d83d3b09941565e5dd0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cbcb41fd3dfb5021a0e188adf0f2ae2e594bd4875ba613a1b5f569e9d1d8c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214168275c8edc1debf0ee2bc144244c232d692c16bb9504f612ad0a4eb7003c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de68ad4994cc45bf50265e4e4bcf885258b60f83785bbacc0490aff2aa3a4689(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798de1ea896a624acf6ec6fb5914ae79fe6079d6885f3bcabf078edd57eff4da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99b7c25307489eaddcecbee4e4a613eacc9170350e039b070300ebe74392abb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageGuestOsFeatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3c513ecbaee181e2887e63763f57c97f6390dfb86041b2a6ae8170bbdf2a20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b493ea927cd46bcb462748dc494158a1f61ee6a05a380e32076bafa0162c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa7dbb465835505d22ef13ab2fd273212dfa691735c673497802871561da6fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageGuestOsFeatures]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d156c62a17a9a712dfb844ba4b1cd40ce1015e6a8af2aa9bf773fb328d6f7a(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52345bf7f16614e5b4b8ef09b3e4b237de95d6ee51f34d560b1c495ffe2fc4c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7854c4defaa56de415ab30c8e0e29e094ac9bf403d744e56453fb2eabc7c0c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2b494009d00b647cb94040f418fa0f92ec0fb80a27c5377103e8077ff94314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0e4a7d14342655ebbfb406d9983a18374de858d47cc3f9ee5489c4d86be5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d6eed00c8570a8079ad9fd7fad1ea2c43ae071a85f69a4a92daeca02ec3327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c7f7773e901455017a23b513034f51c1237ea49b9e26e8a666862c40deb44e(
    value: typing.Optional[ComputeImageImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e8a9ddd5bbdb138a52dc6deb7479c6eaf30521203cac975ffb6e1d3568875a(
    *,
    source: builtins.str,
    container_type: typing.Optional[builtins.str] = None,
    sha1: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd7a27c31078f6a20a0dbe2c80ca77545be18d2f6f794d543935735720e547a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacefa3fc8cf7858ea2025fcb456b7498351d5a65d5c815243a3231680c2e70c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca462bf9fb80f6e5337c55ce7b552a73365eac587358556e7ebde6e89b68210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ccabbaf47cd40486c49da57d7bdf374505db9c214a0bf4de53a9dd6c22ffc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054292c082e2ff9afde90f14f93fa92daadc190ab5a812a8faa344b86196e2d1(
    value: typing.Optional[ComputeImageRawDisk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75a0af0a945498f4c115689c6c14ce6592636a12f0822fb54e239d319e029cf(
    *,
    dbs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dbxs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbxs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    keks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateKeks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pk: typing.Optional[typing.Union[ComputeImageShieldedInstanceInitialStatePk, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9955449bfc8b695894ba4ce247fd35627e5edc6dd32a1729a9401c0f1ccd8efc(
    *,
    content: builtins.str,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057e9e77d445150e3692cde6edd9be78e7a7a68a111a1dc2be6ac31a68b2be06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b1a3767d9d8458af4f1e7f8b46e22c5a13eafd0248a3a78bfc3f2583263414(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff30e0345f2eab05770f7602281c028c623d7a85c8d98e314fe1bd9598bad294(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddf56984d39be67113edcf72f7d7bd30e82f2855b368488b125c702efb876ae5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48465aff748a211077457df9a060c3707bde81f62aadbad3867eb5fd8c6b973a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b9b03ee57123cffca15f2c259755549a64534e1686b6e708598fd7cd0d2aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b973f2d5e5553db1bdfad786ae7ac782c80b4277a5ce2f693c41dcba9888c6f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de422af7a02dab20147a4ce48c0002cd221872503e4877f96ea8b83811551894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21d63d05f7a66709a974bc6e3b8121a224b034e1267fa893f011f5bfaa15b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56371233909682cdb292cf42db98c7a4b73a9abdae29e70036f08637da7f0d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc5f95ab6566cc3e720f2ec1c19a5f2f6d33b3e487d178a5b1b834c86c1312f(
    *,
    content: builtins.str,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cfee39ccb26939dff000dca041de333e4043f73da26da69c61fb03753587d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b06d5c661d9f5407d60c6dd19ed1f172b7fe37bfc842fe2d96cc0ed517416f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85de2505cd232bc26fa82f8c13ed16cdef070dc9e8f1a89c897595a816d5bc7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbdbbc3fe2940df86281bfba350fdcf49d24ba2eba53161e9467ef401625071(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c5f26875fdcdb2f7ef7b2647da8ad4d36a36c0632c398ceb9aae075ec90881(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c682e6ca27cdc165311ae2d22dc4c1315e998669bb2584148b50605a5f7860a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateDbxs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b217d5868025355e8bfd462cc05ddce68fabc74516f21d6f22bed055283deaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a54e5f8bf32310ff6918f3535eeff928b78bbc180a80a9eb7bf231c8392fcc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0f9b3851dfcbc6b854861c4273eae16772ccf30666905b8616432a5d7bf8c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3540e4388293f5c27844f923c6def04bb03187629f12abca53c6c0bf7ccade1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateDbxs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f6e59890eedfae02049e7fa793302e88edfdd7bf2568c381a303e32b60090d(
    *,
    content: builtins.str,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258b580099dd734a79731d5b999765b3c6e61067e9e0e63900bd611ff9748b9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8dcd04e12a7044ea5d2f5fa892fb49b5f09b966a8fcaa679e41163d37b56974(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3b0875f4132eb6ab58052971ae7fc89f507767a160af23b44ca50368c491f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b4c7200a2e795cd75b3c8e8602791326644c6967c8b61590b53fab3bb4b790(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bee7dfdaba17226b00ea08f448ebe33c00ca2bf2c31bfe3bc36212934458607(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f5685e15beb8129395b8dc36b0ef34ac1706326d39f7720dc0e7fa0d5bab4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeImageShieldedInstanceInitialStateKeks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2069bc587f69ce5761f460fdffb574255cacce9137820bfe9ee4e2a677547ea8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41d89934c32c2253356ae4fff0a356395ca9352539606768935643eb6ec920e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ceb6776a93df4ad65f7af05ae2b3685c552316e4b88dd20bc7235deb5f8014f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d68da3cf733c815490803a689939930f8d9d0fe1565736c049ff89688553665(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageShieldedInstanceInitialStateKeks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d340e54d80ade5ef1d9d9b23912adee605e4970f230b3f7742b9e6d8324956f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18273595af8c9b048041bcc1fc74ee40368cf86699167631de39ef5ef371a91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942893922a3d70751fcfd6ee544d55e9bbb34b544deebbcb3ddd42ea050fa576(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateDbxs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0cba4331dd77b702635d81e60cbf21a2cf5742311cec7e07ea9703592b9f97(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeImageShieldedInstanceInitialStateKeks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6c03e0a4f06b8e3aafc196e34807be51b66d631ba6ecd3bb4a3b248e55983d(
    value: typing.Optional[ComputeImageShieldedInstanceInitialState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5929c31d2a54231a458f38183556215422b3c0dc099889669e1cef8300dd4d(
    *,
    content: builtins.str,
    file_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178b496e3f1386c79b8727f5611c651ba8a3859d2dc0ca9429991f78adbfe42b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a022dfbea2e9747781f228781f2efa99fd329e1de878fce4200e43a0aa7b63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e219ac2b917a213444834bd1c8e5458c6df6cb73a4d6d9ecd338c29d9e78d356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1310178ac536add3db4579376c34a9002a0d687032743968838547a103d2ef7(
    value: typing.Optional[ComputeImageShieldedInstanceInitialStatePk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a9f24261f806f88a1d4388866b7cd3ceeff9a9199965696e2d65a138b1fb69(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63171eac660648da4091014185c2ec8aa9473fc1731a3407ec460a2796b83945(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080e108c804da17e9d4870ebd516325b59fbb826f74ca463d5b81d863774b219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f845305093a7372a42321bb78b11044018032d3dcd0364cf6e7f3341c4569b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f509520cc31422deb5d07c56ab8bbf45db1ae4297b2af647c2a759ab9ecb615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc05f2e41d4f9b110d829717c05f6eae1bd4261915bc461d54e54f9285e310b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22828d913aceb00b45cb37b15faa0bde6d07024db0463448c3aac983ce2fd8bd(
    value: typing.Optional[ComputeImageSourceDiskEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4ca63c01ec91e16b649f224cef2ceaa34731beaf7c92ae0dfbb84c2c9ef903(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c8fc7bbca93a20ee7d2cde9e1c6d160834982518b9008e63411536344130b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9a80d04787b1dd0590b391c3026ac52e677a04b8349137e0f70fdde0d55649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4458e9191898156b22fda8e192467804ca9de67ca48e0f085d0eb585c4749d74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd90bdebd352b592aec1149e5267787dbe84718738de910fba02d66d9d65baf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdbec854387d9e63937fc0f1ac71557dfa75dc0a5a85c775cff13898b5a59e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b869acee35b15ea71d3867442ddddd070309b1d2e4426a52db9075abc6f7fd73(
    value: typing.Optional[ComputeImageSourceImageEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b586ec884e1e430026dcc3320846c8595bee4ea166f2e665471457778930b6(
    *,
    kms_key_self_link: typing.Optional[builtins.str] = None,
    kms_key_service_account: typing.Optional[builtins.str] = None,
    raw_key: typing.Optional[builtins.str] = None,
    rsa_encrypted_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68248131990c4a4647714a7dc21ed446c528db1fa6e9de71c35a8563d58d28e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0634cb474b79d176ff5744fc9b9e0fa46422da5e17d7d13e0f0849332fac799(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21ac88cda35a0b061a466ba35cccdb2e8dafe5ab86fa2fad17be43e975f34a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca339ddaac65789d1cc05b8e5d83cfb2dcb321cfd3d63bb418c95f12a1311542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2faf74068c952ac12ecb6455fc8dbb11db5c8c94e0e5cc0313069416e5178737(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abb234b5cd53c96b3994f2e53eeb811295c50e9605a4fd9bc8566a5eba9218a(
    value: typing.Optional[ComputeImageSourceSnapshotEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fff255e313c8b5f71de2d2020ad8e7c69bdf14c8f9ee704236219944a689a07(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e1ead5f4cac4b8b75c7f2fa2427aaac008f264d58d955e8e1dbcabe8231be8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e962a4a927561aa758dfa39bf65848e34c63fb7bde26805a161766ad208f90f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eb2229ef2904fed9c9606bb401697e5e86d892bfd19929986bb16153d6b6cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f09db7c6cf48b14e806280074f18ae7527a2c2b35f563d56e6b079b1c0621d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c48c6c16e65d615437f81583e285c902431540f4bccbceb3ca647d63f1db5fa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeImageTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `data_opentelekomcloud_cbr_backup_v3`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_cbr_backup_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3).
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


class DataOpentelekomcloudCbrBackupV3(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCbrBackupV3.DataOpentelekomcloudCbrBackupV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3 opentelekomcloud_cbr_backup_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auto_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bootable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        checkpoint_id: typing.Optional[builtins.str] = None,
        contain_system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expired_at: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        incremental: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        parent_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        resource_az: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        resource_size: typing.Optional[jsii.Number] = None,
        resource_type: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        supported_restore_mode: typing.Optional[builtins.str] = None,
        support_lld: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        updated_at: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3 opentelekomcloud_cbr_backup_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auto_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#auto_trigger DataOpentelekomcloudCbrBackupV3#auto_trigger}.
        :param bootable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#bootable DataOpentelekomcloudCbrBackupV3#bootable}.
        :param checkpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#checkpoint_id DataOpentelekomcloudCbrBackupV3#checkpoint_id}.
        :param contain_system_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#contain_system_disk DataOpentelekomcloudCbrBackupV3#contain_system_disk}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#created_at DataOpentelekomcloudCbrBackupV3#created_at}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#description DataOpentelekomcloudCbrBackupV3#description}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#encrypted DataOpentelekomcloudCbrBackupV3#encrypted}.
        :param expired_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#expired_at DataOpentelekomcloudCbrBackupV3#expired_at}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#id DataOpentelekomcloudCbrBackupV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#image_type DataOpentelekomcloudCbrBackupV3#image_type}.
        :param incremental: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#incremental DataOpentelekomcloudCbrBackupV3#incremental}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#name DataOpentelekomcloudCbrBackupV3#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#parent_id DataOpentelekomcloudCbrBackupV3#parent_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#project_id DataOpentelekomcloudCbrBackupV3#project_id}.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#provider_id DataOpentelekomcloudCbrBackupV3#provider_id}.
        :param resource_az: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_az DataOpentelekomcloudCbrBackupV3#resource_az}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_id DataOpentelekomcloudCbrBackupV3#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_name DataOpentelekomcloudCbrBackupV3#resource_name}.
        :param resource_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_size DataOpentelekomcloudCbrBackupV3#resource_size}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_type DataOpentelekomcloudCbrBackupV3#resource_type}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#snapshot_id DataOpentelekomcloudCbrBackupV3#snapshot_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#status DataOpentelekomcloudCbrBackupV3#status}.
        :param supported_restore_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#supported_restore_mode DataOpentelekomcloudCbrBackupV3#supported_restore_mode}.
        :param support_lld: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#support_lld DataOpentelekomcloudCbrBackupV3#support_lld}.
        :param system_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#system_disk DataOpentelekomcloudCbrBackupV3#system_disk}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#updated_at DataOpentelekomcloudCbrBackupV3#updated_at}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#vault_id DataOpentelekomcloudCbrBackupV3#vault_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9024af06edd213affb1e58f9c28ea4b2047fbed4877981cb613ac3447ff729e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudCbrBackupV3Config(
            auto_trigger=auto_trigger,
            bootable=bootable,
            checkpoint_id=checkpoint_id,
            contain_system_disk=contain_system_disk,
            created_at=created_at,
            description=description,
            encrypted=encrypted,
            expired_at=expired_at,
            id=id,
            image_type=image_type,
            incremental=incremental,
            name=name,
            parent_id=parent_id,
            project_id=project_id,
            provider_id=provider_id,
            resource_az=resource_az,
            resource_id=resource_id,
            resource_name=resource_name,
            resource_size=resource_size,
            resource_type=resource_type,
            snapshot_id=snapshot_id,
            status=status,
            supported_restore_mode=supported_restore_mode,
            support_lld=support_lld,
            system_disk=system_disk,
            updated_at=updated_at,
            vault_id=vault_id,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudCbrBackupV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudCbrBackupV3 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudCbrBackupV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudCbrBackupV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e619767350f0155dda91abdf99c6ba241a3de0d083aaabd90c99111feade76f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAutoTrigger")
    def reset_auto_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoTrigger", []))

    @jsii.member(jsii_name="resetBootable")
    def reset_bootable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootable", []))

    @jsii.member(jsii_name="resetCheckpointId")
    def reset_checkpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckpointId", []))

    @jsii.member(jsii_name="resetContainSystemDisk")
    def reset_contain_system_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainSystemDisk", []))

    @jsii.member(jsii_name="resetCreatedAt")
    def reset_created_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreatedAt", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncrypted")
    def reset_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncrypted", []))

    @jsii.member(jsii_name="resetExpiredAt")
    def reset_expired_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiredAt", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImageType")
    def reset_image_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageType", []))

    @jsii.member(jsii_name="resetIncremental")
    def reset_incremental(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncremental", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetParentId")
    def reset_parent_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentId", []))

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetProviderId")
    def reset_provider_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderId", []))

    @jsii.member(jsii_name="resetResourceAz")
    def reset_resource_az(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceAz", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceName")
    def reset_resource_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceName", []))

    @jsii.member(jsii_name="resetResourceSize")
    def reset_resource_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceSize", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetSnapshotId")
    def reset_snapshot_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotId", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSupportedRestoreMode")
    def reset_supported_restore_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportedRestoreMode", []))

    @jsii.member(jsii_name="resetSupportLld")
    def reset_support_lld(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportLld", []))

    @jsii.member(jsii_name="resetSystemDisk")
    def reset_system_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDisk", []))

    @jsii.member(jsii_name="resetUpdatedAt")
    def reset_updated_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdatedAt", []))

    @jsii.member(jsii_name="resetVaultId")
    def reset_vault_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVaultId", []))

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
    @jsii.member(jsii_name="autoTriggerInput")
    def auto_trigger_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="bootableInput")
    def bootable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootableInput"))

    @builtins.property
    @jsii.member(jsii_name="checkpointIdInput")
    def checkpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "checkpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containSystemDiskInput")
    def contain_system_disk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containSystemDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="createdAtInput")
    def created_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createdAtInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="expiredAtInput")
    def expired_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiredAtInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTypeInput")
    def image_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalInput")
    def incremental_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "incrementalInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parentIdInput")
    def parent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerIdInput")
    def provider_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceAzInput")
    def resource_az_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceAzInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceNameInput")
    def resource_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceSizeInput")
    def resource_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "resourceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotIdInput")
    def snapshot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="supportedRestoreModeInput")
    def supported_restore_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "supportedRestoreModeInput"))

    @builtins.property
    @jsii.member(jsii_name="supportLldInput")
    def support_lld_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportLldInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskInput")
    def system_disk_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="updatedAtInput")
    def updated_at_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updatedAtInput"))

    @builtins.property
    @jsii.member(jsii_name="vaultIdInput")
    def vault_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vaultIdInput"))

    @builtins.property
    @jsii.member(jsii_name="autoTrigger")
    def auto_trigger(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoTrigger"))

    @auto_trigger.setter
    def auto_trigger(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e320f41327400e9f43a67848c0be506c5f59b9268aa48c98fe52991bb3ea005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoTrigger", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootable")
    def bootable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootable"))

    @bootable.setter
    def bootable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf780784318b8765a12849f6f8202c272865b8d0f2a4dcf6e742ff2582074efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="checkpointId")
    def checkpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "checkpointId"))

    @checkpoint_id.setter
    def checkpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9d94b5ea581cf973f083c948270f399840da1ca35f2b0fad87bb599d356735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containSystemDisk")
    def contain_system_disk(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containSystemDisk"))

    @contain_system_disk.setter
    def contain_system_disk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc338304fede41816a50ca9f9f5370b7e1a6a960c21f91e48fd6055c229bb92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containSystemDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @created_at.setter
    def created_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c57614679d7772b080c402ec342f2f3164386fec1ca5b7fee216966b681c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createdAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f708925da54194ce326675cade63665d996df0a0c82e87d889d7615a6320b06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c720ff0dc7dc48c8f1c6ac94457f2089bfefd30b17c8f790b3e5e63ed396508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiredAt")
    def expired_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiredAt"))

    @expired_at.setter
    def expired_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0e153034b30702a6738e444d702c4492e997ec069ddf06929ad73db81f544c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiredAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66e3a567edc27f18b84e72e02ab5e42ea12525ab434b0b1e9c7c40a506b2b7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageType")
    def image_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageType"))

    @image_type.setter
    def image_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e5e515be70e3ba00252a4c3f53ac418cf62dfdf2245d41c93c75a70f9af821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="incremental")
    def incremental(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "incremental"))

    @incremental.setter
    def incremental(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7d74d5a3db2a843f2f98460cab110f3ea5c9a9e21b7c00a96ad6da9fc68e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incremental", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396942d49d524db7b7297f451c53f1948fe5600a6ccf4e2d8eab3eec327398a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentId")
    def parent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentId"))

    @parent_id.setter
    def parent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b72da8c8a0a3b2d32f6430c941c1a4840aa5be20ea004bf5640bcaa540a0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c09eb5b50731b79874d22bb61df136f0a8eca6ad0c9d015ea42b95f4774e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerId")
    def provider_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerId"))

    @provider_id.setter
    def provider_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a561274370ee9c0dec28bda33cdfa18fb7fb71fc707e4d2e149cbbd763883d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceAz")
    def resource_az(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceAz"))

    @resource_az.setter
    def resource_az(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e14b1c9e2db5f0f129a178bf65893baab0e33c6068594138ac3b4f03ab9830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceAz", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de238ae250387f5643c38be98ad75e2647df3ad038dd4f3f253e69e7958da121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceName")
    def resource_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceName"))

    @resource_name.setter
    def resource_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a75c8218e35fd28a4d4ba8bb5431dd56c0f8ba2e63707015ca1070cb41df77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceSize")
    def resource_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceSize"))

    @resource_size.setter
    def resource_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18be1333832c61373ca03c5c700adc2b4951763134d815e2b4ced09d86ac10d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802c286af83cba9004bdee5d5c772f0d2b9fb7d8ec4d1b38ef15c5488cff643a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotId"))

    @snapshot_id.setter
    def snapshot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f537721d2cee38cbcfa5bc4a7d35783ffad4c293af4daee5e57549da2ccb52b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcb414c0b5e6417a8e85bed97af936c76d0ab1f56cde15633e3d301707c6177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportedRestoreMode")
    def supported_restore_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "supportedRestoreMode"))

    @supported_restore_mode.setter
    def supported_restore_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc42d76ede822233318a86734a54fe40761c7626e219572c4c092ae8003451a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportedRestoreMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportLld")
    def support_lld(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportLld"))

    @support_lld.setter
    def support_lld(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3017bf9bb896976615d1c31c01d79f73d693a407a3b6f1c93b19dec789593f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportLld", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDisk")
    def system_disk(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "systemDisk"))

    @system_disk.setter
    def system_disk(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99813349b4bcceae10468352f3ec211cc2942a4f8577a2ecf724c3719524006b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDisk", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @updated_at.setter
    def updated_at(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a30046fdf8ff47d2cfd1888c26425c3addf2c1b89f82fe10dcae56d459d8e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatedAt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vaultId")
    def vault_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vaultId"))

    @vault_id.setter
    def vault_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e20875c12be94f02e9ea22eb94b3f67c73c7fb7694343fc9322bf291ae4dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vaultId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudCbrBackupV3.DataOpentelekomcloudCbrBackupV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auto_trigger": "autoTrigger",
        "bootable": "bootable",
        "checkpoint_id": "checkpointId",
        "contain_system_disk": "containSystemDisk",
        "created_at": "createdAt",
        "description": "description",
        "encrypted": "encrypted",
        "expired_at": "expiredAt",
        "id": "id",
        "image_type": "imageType",
        "incremental": "incremental",
        "name": "name",
        "parent_id": "parentId",
        "project_id": "projectId",
        "provider_id": "providerId",
        "resource_az": "resourceAz",
        "resource_id": "resourceId",
        "resource_name": "resourceName",
        "resource_size": "resourceSize",
        "resource_type": "resourceType",
        "snapshot_id": "snapshotId",
        "status": "status",
        "supported_restore_mode": "supportedRestoreMode",
        "support_lld": "supportLld",
        "system_disk": "systemDisk",
        "updated_at": "updatedAt",
        "vault_id": "vaultId",
    },
)
class DataOpentelekomcloudCbrBackupV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auto_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bootable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        checkpoint_id: typing.Optional[builtins.str] = None,
        contain_system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expired_at: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        image_type: typing.Optional[builtins.str] = None,
        incremental: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        parent_id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        provider_id: typing.Optional[builtins.str] = None,
        resource_az: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        resource_size: typing.Optional[jsii.Number] = None,
        resource_type: typing.Optional[builtins.str] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        supported_restore_mode: typing.Optional[builtins.str] = None,
        support_lld: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        updated_at: typing.Optional[builtins.str] = None,
        vault_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auto_trigger: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#auto_trigger DataOpentelekomcloudCbrBackupV3#auto_trigger}.
        :param bootable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#bootable DataOpentelekomcloudCbrBackupV3#bootable}.
        :param checkpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#checkpoint_id DataOpentelekomcloudCbrBackupV3#checkpoint_id}.
        :param contain_system_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#contain_system_disk DataOpentelekomcloudCbrBackupV3#contain_system_disk}.
        :param created_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#created_at DataOpentelekomcloudCbrBackupV3#created_at}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#description DataOpentelekomcloudCbrBackupV3#description}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#encrypted DataOpentelekomcloudCbrBackupV3#encrypted}.
        :param expired_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#expired_at DataOpentelekomcloudCbrBackupV3#expired_at}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#id DataOpentelekomcloudCbrBackupV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param image_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#image_type DataOpentelekomcloudCbrBackupV3#image_type}.
        :param incremental: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#incremental DataOpentelekomcloudCbrBackupV3#incremental}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#name DataOpentelekomcloudCbrBackupV3#name}.
        :param parent_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#parent_id DataOpentelekomcloudCbrBackupV3#parent_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#project_id DataOpentelekomcloudCbrBackupV3#project_id}.
        :param provider_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#provider_id DataOpentelekomcloudCbrBackupV3#provider_id}.
        :param resource_az: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_az DataOpentelekomcloudCbrBackupV3#resource_az}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_id DataOpentelekomcloudCbrBackupV3#resource_id}.
        :param resource_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_name DataOpentelekomcloudCbrBackupV3#resource_name}.
        :param resource_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_size DataOpentelekomcloudCbrBackupV3#resource_size}.
        :param resource_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_type DataOpentelekomcloudCbrBackupV3#resource_type}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#snapshot_id DataOpentelekomcloudCbrBackupV3#snapshot_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#status DataOpentelekomcloudCbrBackupV3#status}.
        :param supported_restore_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#supported_restore_mode DataOpentelekomcloudCbrBackupV3#supported_restore_mode}.
        :param support_lld: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#support_lld DataOpentelekomcloudCbrBackupV3#support_lld}.
        :param system_disk: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#system_disk DataOpentelekomcloudCbrBackupV3#system_disk}.
        :param updated_at: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#updated_at DataOpentelekomcloudCbrBackupV3#updated_at}.
        :param vault_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#vault_id DataOpentelekomcloudCbrBackupV3#vault_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8121e0eb08e8d3cd0c2e19651f084e03b7bee3d4c33c99ac804e7c9573b0a5d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auto_trigger", value=auto_trigger, expected_type=type_hints["auto_trigger"])
            check_type(argname="argument bootable", value=bootable, expected_type=type_hints["bootable"])
            check_type(argname="argument checkpoint_id", value=checkpoint_id, expected_type=type_hints["checkpoint_id"])
            check_type(argname="argument contain_system_disk", value=contain_system_disk, expected_type=type_hints["contain_system_disk"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument expired_at", value=expired_at, expected_type=type_hints["expired_at"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
            check_type(argname="argument incremental", value=incremental, expected_type=type_hints["incremental"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument provider_id", value=provider_id, expected_type=type_hints["provider_id"])
            check_type(argname="argument resource_az", value=resource_az, expected_type=type_hints["resource_az"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
            check_type(argname="argument resource_size", value=resource_size, expected_type=type_hints["resource_size"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument supported_restore_mode", value=supported_restore_mode, expected_type=type_hints["supported_restore_mode"])
            check_type(argname="argument support_lld", value=support_lld, expected_type=type_hints["support_lld"])
            check_type(argname="argument system_disk", value=system_disk, expected_type=type_hints["system_disk"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument vault_id", value=vault_id, expected_type=type_hints["vault_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if auto_trigger is not None:
            self._values["auto_trigger"] = auto_trigger
        if bootable is not None:
            self._values["bootable"] = bootable
        if checkpoint_id is not None:
            self._values["checkpoint_id"] = checkpoint_id
        if contain_system_disk is not None:
            self._values["contain_system_disk"] = contain_system_disk
        if created_at is not None:
            self._values["created_at"] = created_at
        if description is not None:
            self._values["description"] = description
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if expired_at is not None:
            self._values["expired_at"] = expired_at
        if id is not None:
            self._values["id"] = id
        if image_type is not None:
            self._values["image_type"] = image_type
        if incremental is not None:
            self._values["incremental"] = incremental
        if name is not None:
            self._values["name"] = name
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if project_id is not None:
            self._values["project_id"] = project_id
        if provider_id is not None:
            self._values["provider_id"] = provider_id
        if resource_az is not None:
            self._values["resource_az"] = resource_az
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_name is not None:
            self._values["resource_name"] = resource_name
        if resource_size is not None:
            self._values["resource_size"] = resource_size
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id
        if status is not None:
            self._values["status"] = status
        if supported_restore_mode is not None:
            self._values["supported_restore_mode"] = supported_restore_mode
        if support_lld is not None:
            self._values["support_lld"] = support_lld
        if system_disk is not None:
            self._values["system_disk"] = system_disk
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if vault_id is not None:
            self._values["vault_id"] = vault_id

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
    def auto_trigger(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#auto_trigger DataOpentelekomcloudCbrBackupV3#auto_trigger}.'''
        result = self._values.get("auto_trigger")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bootable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#bootable DataOpentelekomcloudCbrBackupV3#bootable}.'''
        result = self._values.get("bootable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def checkpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#checkpoint_id DataOpentelekomcloudCbrBackupV3#checkpoint_id}.'''
        result = self._values.get("checkpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contain_system_disk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#contain_system_disk DataOpentelekomcloudCbrBackupV3#contain_system_disk}.'''
        result = self._values.get("contain_system_disk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def created_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#created_at DataOpentelekomcloudCbrBackupV3#created_at}.'''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#description DataOpentelekomcloudCbrBackupV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#encrypted DataOpentelekomcloudCbrBackupV3#encrypted}.'''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expired_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#expired_at DataOpentelekomcloudCbrBackupV3#expired_at}.'''
        result = self._values.get("expired_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#id DataOpentelekomcloudCbrBackupV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#image_type DataOpentelekomcloudCbrBackupV3#image_type}.'''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#incremental DataOpentelekomcloudCbrBackupV3#incremental}.'''
        result = self._values.get("incremental")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#name DataOpentelekomcloudCbrBackupV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#parent_id DataOpentelekomcloudCbrBackupV3#parent_id}.'''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#project_id DataOpentelekomcloudCbrBackupV3#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#provider_id DataOpentelekomcloudCbrBackupV3#provider_id}.'''
        result = self._values.get("provider_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_az(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_az DataOpentelekomcloudCbrBackupV3#resource_az}.'''
        result = self._values.get("resource_az")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_id DataOpentelekomcloudCbrBackupV3#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_name DataOpentelekomcloudCbrBackupV3#resource_name}.'''
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_size DataOpentelekomcloudCbrBackupV3#resource_size}.'''
        result = self._values.get("resource_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#resource_type DataOpentelekomcloudCbrBackupV3#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#snapshot_id DataOpentelekomcloudCbrBackupV3#snapshot_id}.'''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#status DataOpentelekomcloudCbrBackupV3#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supported_restore_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#supported_restore_mode DataOpentelekomcloudCbrBackupV3#supported_restore_mode}.'''
        result = self._values.get("supported_restore_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_lld(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#support_lld DataOpentelekomcloudCbrBackupV3#support_lld}.'''
        result = self._values.get("support_lld")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def system_disk(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#system_disk DataOpentelekomcloudCbrBackupV3#system_disk}.'''
        result = self._values.get("system_disk")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#updated_at DataOpentelekomcloudCbrBackupV3#updated_at}.'''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vault_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/cbr_backup_v3#vault_id DataOpentelekomcloudCbrBackupV3#vault_id}.'''
        result = self._values.get("vault_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudCbrBackupV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataOpentelekomcloudCbrBackupV3",
    "DataOpentelekomcloudCbrBackupV3Config",
]

publication.publish()

def _typecheckingstub__9024af06edd213affb1e58f9c28ea4b2047fbed4877981cb613ac3447ff729e6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auto_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bootable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    checkpoint_id: typing.Optional[builtins.str] = None,
    contain_system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expired_at: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    incremental: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    parent_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    provider_id: typing.Optional[builtins.str] = None,
    resource_az: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    resource_size: typing.Optional[jsii.Number] = None,
    resource_type: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    supported_restore_mode: typing.Optional[builtins.str] = None,
    support_lld: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    updated_at: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7e619767350f0155dda91abdf99c6ba241a3de0d083aaabd90c99111feade76f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e320f41327400e9f43a67848c0be506c5f59b9268aa48c98fe52991bb3ea005(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf780784318b8765a12849f6f8202c272865b8d0f2a4dcf6e742ff2582074efa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9d94b5ea581cf973f083c948270f399840da1ca35f2b0fad87bb599d356735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc338304fede41816a50ca9f9f5370b7e1a6a960c21f91e48fd6055c229bb92(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c57614679d7772b080c402ec342f2f3164386fec1ca5b7fee216966b681c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f708925da54194ce326675cade63665d996df0a0c82e87d889d7615a6320b06a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c720ff0dc7dc48c8f1c6ac94457f2089bfefd30b17c8f790b3e5e63ed396508(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0e153034b30702a6738e444d702c4492e997ec069ddf06929ad73db81f544c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66e3a567edc27f18b84e72e02ab5e42ea12525ab434b0b1e9c7c40a506b2b7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e5e515be70e3ba00252a4c3f53ac418cf62dfdf2245d41c93c75a70f9af821(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7d74d5a3db2a843f2f98460cab110f3ea5c9a9e21b7c00a96ad6da9fc68e85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396942d49d524db7b7297f451c53f1948fe5600a6ccf4e2d8eab3eec327398a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b72da8c8a0a3b2d32f6430c941c1a4840aa5be20ea004bf5640bcaa540a0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c09eb5b50731b79874d22bb61df136f0a8eca6ad0c9d015ea42b95f4774e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a561274370ee9c0dec28bda33cdfa18fb7fb71fc707e4d2e149cbbd763883d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e14b1c9e2db5f0f129a178bf65893baab0e33c6068594138ac3b4f03ab9830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de238ae250387f5643c38be98ad75e2647df3ad038dd4f3f253e69e7958da121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a75c8218e35fd28a4d4ba8bb5431dd56c0f8ba2e63707015ca1070cb41df77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18be1333832c61373ca03c5c700adc2b4951763134d815e2b4ced09d86ac10d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802c286af83cba9004bdee5d5c772f0d2b9fb7d8ec4d1b38ef15c5488cff643a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f537721d2cee38cbcfa5bc4a7d35783ffad4c293af4daee5e57549da2ccb52b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcb414c0b5e6417a8e85bed97af936c76d0ab1f56cde15633e3d301707c6177(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc42d76ede822233318a86734a54fe40761c7626e219572c4c092ae8003451a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3017bf9bb896976615d1c31c01d79f73d693a407a3b6f1c93b19dec789593f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99813349b4bcceae10468352f3ec211cc2942a4f8577a2ecf724c3719524006b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a30046fdf8ff47d2cfd1888c26425c3addf2c1b89f82fe10dcae56d459d8e44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e20875c12be94f02e9ea22eb94b3f67c73c7fb7694343fc9322bf291ae4dff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8121e0eb08e8d3cd0c2e19651f084e03b7bee3d4c33c99ac804e7c9573b0a5d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auto_trigger: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bootable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    checkpoint_id: typing.Optional[builtins.str] = None,
    contain_system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expired_at: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    image_type: typing.Optional[builtins.str] = None,
    incremental: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    parent_id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    provider_id: typing.Optional[builtins.str] = None,
    resource_az: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    resource_size: typing.Optional[jsii.Number] = None,
    resource_type: typing.Optional[builtins.str] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    supported_restore_mode: typing.Optional[builtins.str] = None,
    support_lld: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    system_disk: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    updated_at: typing.Optional[builtins.str] = None,
    vault_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

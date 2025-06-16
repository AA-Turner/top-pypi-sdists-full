r'''
# `google_netapp_volume`

Refer to the Terraform Registry for docs: [`google_netapp_volume`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume).
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


class GoogleNetappVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolume",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume google_netapp_volume}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        capacity_gib: builtins.str,
        location: builtins.str,
        name: builtins.str,
        protocols: typing.Sequence[builtins.str],
        share_name: builtins.str,
        storage_pool: builtins.str,
        backup_config: typing.Optional[typing.Union["GoogleNetappVolumeBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        export_policy: typing.Optional[typing.Union["GoogleNetappVolumeExportPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_replication_parameters: typing.Optional[typing.Union["GoogleNetappVolumeHybridReplicationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        restore_parameters: typing.Optional[typing.Union["GoogleNetappVolumeRestoreParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_policy: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["GoogleNetappVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unix_permissions: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume google_netapp_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_gib: Capacity of the volume (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#capacity_gib GoogleNetappVolume#capacity_gib}
        :param location: Name of the pool location. Usually a region name, expect for some STANDARD service level pools which require a zone name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#location GoogleNetappVolume#location}
        :param name: The name of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#name GoogleNetappVolume#name}
        :param protocols: The protocol of the volume. Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#protocols GoogleNetappVolume#protocols}
        :param share_name: Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#share_name GoogleNetappVolume#share_name}
        :param storage_pool: Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#storage_pool GoogleNetappVolume#storage_pool}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_config GoogleNetappVolume#backup_config}
        :param deletion_policy: Policy to determine if the volume should be deleted forcefully. Volumes may have nested snapshot resources. Deleting such a volume will fail. Setting this parameter to FORCE will delete volumes including nested snapshots. Possible values: DEFAULT, FORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#deletion_policy GoogleNetappVolume#deletion_policy}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        :param export_policy: export_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#export_policy GoogleNetappVolume#export_policy}
        :param hybrid_replication_parameters: hybrid_replication_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hybrid_replication_parameters GoogleNetappVolume#hybrid_replication_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#id GoogleNetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kerberos_enabled: Flag indicating if the volume is a kerberos volume or not, export policy rules control kerberos security modes (krb5, krb5i, krb5p). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos_enabled GoogleNetappVolume#kerberos_enabled}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        :param large_capacity: Optional. Flag indicating if the volume will be a large capacity volume or a regular volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#large_capacity GoogleNetappVolume#large_capacity}
        :param multiple_endpoints: Optional. Flag indicating if the volume will have an IP address per node for volumes supporting multiple IP endpoints. Only the volume with largeCapacity will be allowed to have multiple endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#multiple_endpoints GoogleNetappVolume#multiple_endpoints}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#project GoogleNetappVolume#project}.
        :param restore_parameters: restore_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restore_parameters GoogleNetappVolume#restore_parameters}
        :param restricted_actions: List of actions that are restricted on this volume. Possible values: ["DELETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restricted_actions GoogleNetappVolume#restricted_actions}
        :param security_style: Security Style of the Volume. Use UNIX to use UNIX or NFSV4 ACLs for file permissions. Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#security_style GoogleNetappVolume#security_style}
        :param smb_settings: Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#smb_settings GoogleNetappVolume#smb_settings}
        :param snapshot_directory: If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_directory GoogleNetappVolume#snapshot_directory}
        :param snapshot_policy: snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_policy GoogleNetappVolume#snapshot_policy}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tiering_policy GoogleNetappVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#timeouts GoogleNetappVolume#timeouts}
        :param unix_permissions: Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#unix_permissions GoogleNetappVolume#unix_permissions}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e21c242e5dcbf9770c1425c3151ee1f6876e863d681a995d4539cd1698944e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetappVolumeConfig(
            capacity_gib=capacity_gib,
            location=location,
            name=name,
            protocols=protocols,
            share_name=share_name,
            storage_pool=storage_pool,
            backup_config=backup_config,
            deletion_policy=deletion_policy,
            description=description,
            export_policy=export_policy,
            hybrid_replication_parameters=hybrid_replication_parameters,
            id=id,
            kerberos_enabled=kerberos_enabled,
            labels=labels,
            large_capacity=large_capacity,
            multiple_endpoints=multiple_endpoints,
            project=project,
            restore_parameters=restore_parameters,
            restricted_actions=restricted_actions,
            security_style=security_style,
            smb_settings=smb_settings,
            snapshot_directory=snapshot_directory,
            snapshot_policy=snapshot_policy,
            tiering_policy=tiering_policy,
            timeouts=timeouts,
            unix_permissions=unix_permissions,
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
        '''Generates CDKTF code for importing a GoogleNetappVolume resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetappVolume to import.
        :param import_from_id: The id of the existing GoogleNetappVolume that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetappVolume to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf8e58191eb210917195c4ff7037647fd0649f60d263df1cb986e23cf4fa36a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupConfig")
    def put_backup_config(
        self,
        *,
        backup_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        backup_vault: typing.Optional[builtins.str] = None,
        scheduled_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_policies: Specify a single backup policy ID for scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupPolicies/{{backupPolicyName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_policies GoogleNetappVolume#backup_policies}
        :param backup_vault: ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_vault GoogleNetappVolume#backup_vault}
        :param scheduled_backup_enabled: When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#scheduled_backup_enabled GoogleNetappVolume#scheduled_backup_enabled}
        '''
        value = GoogleNetappVolumeBackupConfig(
            backup_policies=backup_policies,
            backup_vault=backup_vault,
            scheduled_backup_enabled=scheduled_backup_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupConfig", [value]))

    @jsii.member(jsii_name="putExportPolicy")
    def put_export_policy(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#rules GoogleNetappVolume#rules}
        '''
        value = GoogleNetappVolumeExportPolicy(rules=rules)

        return typing.cast(None, jsii.invoke(self, "putExportPolicy", [value]))

    @jsii.member(jsii_name="putHybridReplicationParameters")
    def put_hybrid_replication_parameters(
        self,
        *,
        cluster_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peer_cluster_name: typing.Optional[builtins.str] = None,
        peer_ip_addresses: typing.Optional[builtins.str] = None,
        peer_svm_name: typing.Optional[builtins.str] = None,
        peer_volume_name: typing.Optional[builtins.str] = None,
        replication: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_location: Optional. Name of source cluster location associated with the Hybrid replication. This is a free-form field for the display purpose only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cluster_location GoogleNetappVolume#cluster_location}
        :param description: Optional. Description of the replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        :param labels: Optional. Labels to be added to the replication as the key value pairs. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        :param peer_cluster_name: Required. Name of the user's local source cluster to be peered with the destination cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_cluster_name GoogleNetappVolume#peer_cluster_name}
        :param peer_ip_addresses: Required. List of node ip addresses to be peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_ip_addresses GoogleNetappVolume#peer_ip_addresses}
        :param peer_svm_name: Required. Name of the user's local source vserver svm to be peered with the destination vserver svm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_svm_name GoogleNetappVolume#peer_svm_name}
        :param peer_volume_name: Required. Name of the user's local source volume to be peered with the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_volume_name GoogleNetappVolume#peer_volume_name}
        :param replication: Required. Desired name for the replication of this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#replication GoogleNetappVolume#replication}
        '''
        value = GoogleNetappVolumeHybridReplicationParameters(
            cluster_location=cluster_location,
            description=description,
            labels=labels,
            peer_cluster_name=peer_cluster_name,
            peer_ip_addresses=peer_ip_addresses,
            peer_svm_name=peer_svm_name,
            peer_volume_name=peer_volume_name,
            replication=replication,
        )

        return typing.cast(None, jsii.invoke(self, "putHybridReplicationParameters", [value]))

    @jsii.member(jsii_name="putRestoreParameters")
    def put_restore_parameters(
        self,
        *,
        source_backup: typing.Optional[builtins.str] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_backup: Full name of the backup to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/backupVaults/{{backupVaultId}}/backups/{{backup}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_backup GoogleNetappVolume#source_backup}
        :param source_snapshot: Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_snapshot GoogleNetappVolume#source_snapshot}
        '''
        value = GoogleNetappVolumeRestoreParameters(
            source_backup=source_backup, source_snapshot=source_snapshot
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreParameters", [value]))

    @jsii.member(jsii_name="putSnapshotPolicy")
    def put_snapshot_policy(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hourly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        monthly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#daily_schedule GoogleNetappVolume#daily_schedule}
        :param enabled: Enables automated snapshot creation according to defined schedule. Default is false. To disable automatic snapshot creation you have to remove the whole snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#enabled GoogleNetappVolume#enabled}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hourly_schedule GoogleNetappVolume#hourly_schedule}
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#monthly_schedule GoogleNetappVolume#monthly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#weekly_schedule GoogleNetappVolume#weekly_schedule}
        '''
        value = GoogleNetappVolumeSnapshotPolicy(
            daily_schedule=daily_schedule,
            enabled=enabled,
            hourly_schedule=hourly_schedule,
            monthly_schedule=monthly_schedule,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotPolicy", [value]))

    @jsii.member(jsii_name="putTieringPolicy")
    def put_tiering_policy(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cooling_threshold_days GoogleNetappVolume#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tier_action GoogleNetappVolume#tier_action}
        '''
        value = GoogleNetappVolumeTieringPolicy(
            cooling_threshold_days=cooling_threshold_days, tier_action=tier_action
        )

        return typing.cast(None, jsii.invoke(self, "putTieringPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#create GoogleNetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#delete GoogleNetappVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#update GoogleNetappVolume#update}.
        '''
        value = GoogleNetappVolumeTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupConfig")
    def reset_backup_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupConfig", []))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExportPolicy")
    def reset_export_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportPolicy", []))

    @jsii.member(jsii_name="resetHybridReplicationParameters")
    def reset_hybrid_replication_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHybridReplicationParameters", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKerberosEnabled")
    def reset_kerberos_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosEnabled", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLargeCapacity")
    def reset_large_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLargeCapacity", []))

    @jsii.member(jsii_name="resetMultipleEndpoints")
    def reset_multiple_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultipleEndpoints", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRestoreParameters")
    def reset_restore_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreParameters", []))

    @jsii.member(jsii_name="resetRestrictedActions")
    def reset_restricted_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedActions", []))

    @jsii.member(jsii_name="resetSecurityStyle")
    def reset_security_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityStyle", []))

    @jsii.member(jsii_name="resetSmbSettings")
    def reset_smb_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmbSettings", []))

    @jsii.member(jsii_name="resetSnapshotDirectory")
    def reset_snapshot_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotDirectory", []))

    @jsii.member(jsii_name="resetSnapshotPolicy")
    def reset_snapshot_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotPolicy", []))

    @jsii.member(jsii_name="resetTieringPolicy")
    def reset_tiering_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTieringPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUnixPermissions")
    def reset_unix_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixPermissions", []))

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
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="backupConfig")
    def backup_config(self) -> "GoogleNetappVolumeBackupConfigOutputReference":
        return typing.cast("GoogleNetappVolumeBackupConfigOutputReference", jsii.get(self, "backupConfig"))

    @builtins.property
    @jsii.member(jsii_name="coldTierSizeGib")
    def cold_tier_size_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "coldTierSizeGib"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicy")
    def export_policy(self) -> "GoogleNetappVolumeExportPolicyOutputReference":
        return typing.cast("GoogleNetappVolumeExportPolicyOutputReference", jsii.get(self, "exportPolicy"))

    @builtins.property
    @jsii.member(jsii_name="hasReplication")
    def has_replication(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasReplication"))

    @builtins.property
    @jsii.member(jsii_name="hybridReplicationParameters")
    def hybrid_replication_parameters(
        self,
    ) -> "GoogleNetappVolumeHybridReplicationParametersOutputReference":
        return typing.cast("GoogleNetappVolumeHybridReplicationParametersOutputReference", jsii.get(self, "hybridReplicationParameters"))

    @builtins.property
    @jsii.member(jsii_name="kmsConfig")
    def kms_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsConfig"))

    @builtins.property
    @jsii.member(jsii_name="ldapEnabled")
    def ldap_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ldapEnabled"))

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> "GoogleNetappVolumeMountOptionsList":
        return typing.cast("GoogleNetappVolumeMountOptionsList", jsii.get(self, "mountOptions"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="psaRange")
    def psa_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "psaRange"))

    @builtins.property
    @jsii.member(jsii_name="replicaZone")
    def replica_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicaZone"))

    @builtins.property
    @jsii.member(jsii_name="restoreParameters")
    def restore_parameters(
        self,
    ) -> "GoogleNetappVolumeRestoreParametersOutputReference":
        return typing.cast("GoogleNetappVolumeRestoreParametersOutputReference", jsii.get(self, "restoreParameters"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicy")
    def snapshot_policy(self) -> "GoogleNetappVolumeSnapshotPolicyOutputReference":
        return typing.cast("GoogleNetappVolumeSnapshotPolicyOutputReference", jsii.get(self, "snapshotPolicy"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateDetails")
    def state_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateDetails"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicy")
    def tiering_policy(self) -> "GoogleNetappVolumeTieringPolicyOutputReference":
        return typing.cast("GoogleNetappVolumeTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetappVolumeTimeoutsOutputReference":
        return typing.cast("GoogleNetappVolumeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="usedGib")
    def used_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usedGib"))

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @builtins.property
    @jsii.member(jsii_name="backupConfigInput")
    def backup_config_input(self) -> typing.Optional["GoogleNetappVolumeBackupConfig"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeBackupConfig"], jsii.get(self, "backupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityGibInput")
    def capacity_gib_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityGibInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyInput")
    def export_policy_input(self) -> typing.Optional["GoogleNetappVolumeExportPolicy"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeExportPolicy"], jsii.get(self, "exportPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridReplicationParametersInput")
    def hybrid_replication_parameters_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeHybridReplicationParameters"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeHybridReplicationParameters"], jsii.get(self, "hybridReplicationParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberosEnabledInput")
    def kerberos_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberosEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="largeCapacityInput")
    def large_capacity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "largeCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="multipleEndpointsInput")
    def multiple_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multipleEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreParametersInput")
    def restore_parameters_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeRestoreParameters"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeRestoreParameters"], jsii.get(self, "restoreParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedActionsInput")
    def restricted_actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="shareNameInput")
    def share_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareNameInput"))

    @builtins.property
    @jsii.member(jsii_name="smbSettingsInput")
    def smb_settings_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "smbSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryInput")
    def snapshot_directory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snapshotDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyInput")
    def snapshot_policy_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicy"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicy"], jsii.get(self, "snapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolInput")
    def storage_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeTieringPolicy"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappVolumeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappVolumeTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="unixPermissionsInput")
    def unix_permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unixPermissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityGib")
    def capacity_gib(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityGib"))

    @capacity_gib.setter
    def capacity_gib(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2383f957af554b9fa4fa135909655ff5232b0e6ebd7c345d4af501e40870c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112d80c76d5e01c875051577296a1e126d7cb366ac5df450ce2d20e78de7c306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__884104cb5a98da56bd9148d301d7b9deba71b4c6873eed69bbd22f8b80f7b843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085837658cdd4ae457cf0806909b7acf6f6369a5e49fc8177af20709bb9bf919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberosEnabled")
    def kerberos_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberosEnabled"))

    @kerberos_enabled.setter
    def kerberos_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9008003e60f3cff76439ce87f7cc2143dbaf140f765078963e61e1d1663f5f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd63d2c7068d9c4a20dacd087d081f194c0e6ef47a9da6f02adfb28ceb039c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="largeCapacity")
    def large_capacity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "largeCapacity"))

    @large_capacity.setter
    def large_capacity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9c0f5884f90379059dfc10defa991a9decadc8588d341bc63fdc7f4cdd82eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "largeCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42fe3178186f28a5242513d6845964ba78db4aaca946baa0828fd0f2b5c17614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multipleEndpoints")
    def multiple_endpoints(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multipleEndpoints"))

    @multiple_endpoints.setter
    def multiple_endpoints(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660369efb141e6733a063305b733710be9b7e6e4880adcd94149f8587226935a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multipleEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb757e7a4bc47ca182e449e1beb31842514e07ed09f05d1cb1fcd8d8989fa062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd87b16dfb03df2dc86ff41a0c8370a1f5d0e1b2adc59398117b58ef43055a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2823dff06595eb7a756168f3c87a70f4edfc4b3a8913f29690677da35715ba16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedActions")
    def restricted_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedActions"))

    @restricted_actions.setter
    def restricted_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e082f80c27e1691a9e7520c420d550f69f9f97dc8f40e9199125dcc5c13e2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728bb42ca53c0e58f616f1a96885b0e562cffc0a02ec178fc8ff0bdc2cd024b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55745881bee27949417003ffd82086e7c356c131466d4b0d53fa123003d24b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbSettings")
    def smb_settings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "smbSettings"))

    @smb_settings.setter
    def smb_settings(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0313c4c30f123ac82f06c368f80b91aa0aaa973d2090ef76d12e2669896b4247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smbSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectory")
    def snapshot_directory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snapshotDirectory"))

    @snapshot_directory.setter
    def snapshot_directory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4927c238867fd269b0acfc8a448e0065a6422e8e3daf69b0d1279c7f5e3307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329d9e72744f76615f2605d66ebc26c9768bb81ea337ce921f2f5320157a7ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixPermissions")
    def unix_permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unixPermissions"))

    @unix_permissions.setter
    def unix_permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e094a11ec734cc509348eaac3d5dc58bf664a9cecd5eb5f0ceae6f3a9a3778a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixPermissions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "backup_policies": "backupPolicies",
        "backup_vault": "backupVault",
        "scheduled_backup_enabled": "scheduledBackupEnabled",
    },
)
class GoogleNetappVolumeBackupConfig:
    def __init__(
        self,
        *,
        backup_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        backup_vault: typing.Optional[builtins.str] = None,
        scheduled_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_policies: Specify a single backup policy ID for scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupPolicies/{{backupPolicyName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_policies GoogleNetappVolume#backup_policies}
        :param backup_vault: ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_vault GoogleNetappVolume#backup_vault}
        :param scheduled_backup_enabled: When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#scheduled_backup_enabled GoogleNetappVolume#scheduled_backup_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f961946daf98f960e6c3cab39d7ea827e9cd3c13f1dd5c809fec697e8dc0ccd)
            check_type(argname="argument backup_policies", value=backup_policies, expected_type=type_hints["backup_policies"])
            check_type(argname="argument backup_vault", value=backup_vault, expected_type=type_hints["backup_vault"])
            check_type(argname="argument scheduled_backup_enabled", value=scheduled_backup_enabled, expected_type=type_hints["scheduled_backup_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_policies is not None:
            self._values["backup_policies"] = backup_policies
        if backup_vault is not None:
            self._values["backup_vault"] = backup_vault
        if scheduled_backup_enabled is not None:
            self._values["scheduled_backup_enabled"] = scheduled_backup_enabled

    @builtins.property
    def backup_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify a single backup policy ID for scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupPolicies/{{backupPolicyName}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_policies GoogleNetappVolume#backup_policies}
        '''
        result = self._values.get("backup_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def backup_vault(self) -> typing.Optional[builtins.str]:
        '''ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_vault GoogleNetappVolume#backup_vault}
        '''
        result = self._values.get("backup_vault")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#scheduled_backup_enabled GoogleNetappVolume#scheduled_backup_enabled}
        '''
        result = self._values.get("scheduled_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f41467bbd52a249096aaf02c587eabecf40dcb0709c659e04d587f0a75ff83b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupPolicies")
    def reset_backup_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupPolicies", []))

    @jsii.member(jsii_name="resetBackupVault")
    def reset_backup_vault(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupVault", []))

    @jsii.member(jsii_name="resetScheduledBackupEnabled")
    def reset_scheduled_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledBackupEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="backupPoliciesInput")
    def backup_policies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backupPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="backupVaultInput")
    def backup_vault_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupVaultInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupEnabledInput")
    def scheduled_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scheduledBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPolicies")
    def backup_policies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backupPolicies"))

    @backup_policies.setter
    def backup_policies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babf56a51a88a82e1b2fedd248424e454a234edd02a697c4c0f915ac03ede31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupVault"))

    @backup_vault.setter
    def backup_vault(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c70cd0785497252ec8a8305fc71139b6fe2e50a620ee039ee0260c7177cea27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupVault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheduledBackupEnabled")
    def scheduled_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scheduledBackupEnabled"))

    @scheduled_backup_enabled.setter
    def scheduled_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cab566fc6d8efdbc3b048d416d250a643592b09468118c191669a6f7bcc2ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeBackupConfig]:
        return typing.cast(typing.Optional[GoogleNetappVolumeBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfed497762409592b9a4c944ac3c65af0dfe98de85b5244ea1fc0dd4b2f7c039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "capacity_gib": "capacityGib",
        "location": "location",
        "name": "name",
        "protocols": "protocols",
        "share_name": "shareName",
        "storage_pool": "storagePool",
        "backup_config": "backupConfig",
        "deletion_policy": "deletionPolicy",
        "description": "description",
        "export_policy": "exportPolicy",
        "hybrid_replication_parameters": "hybridReplicationParameters",
        "id": "id",
        "kerberos_enabled": "kerberosEnabled",
        "labels": "labels",
        "large_capacity": "largeCapacity",
        "multiple_endpoints": "multipleEndpoints",
        "project": "project",
        "restore_parameters": "restoreParameters",
        "restricted_actions": "restrictedActions",
        "security_style": "securityStyle",
        "smb_settings": "smbSettings",
        "snapshot_directory": "snapshotDirectory",
        "snapshot_policy": "snapshotPolicy",
        "tiering_policy": "tieringPolicy",
        "timeouts": "timeouts",
        "unix_permissions": "unixPermissions",
    },
)
class GoogleNetappVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_gib: builtins.str,
        location: builtins.str,
        name: builtins.str,
        protocols: typing.Sequence[builtins.str],
        share_name: builtins.str,
        storage_pool: builtins.str,
        backup_config: typing.Optional[typing.Union[GoogleNetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        export_policy: typing.Optional[typing.Union["GoogleNetappVolumeExportPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_replication_parameters: typing.Optional[typing.Union["GoogleNetappVolumeHybridReplicationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        restore_parameters: typing.Optional[typing.Union["GoogleNetappVolumeRestoreParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_policy: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["GoogleNetappVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unix_permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param capacity_gib: Capacity of the volume (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#capacity_gib GoogleNetappVolume#capacity_gib}
        :param location: Name of the pool location. Usually a region name, expect for some STANDARD service level pools which require a zone name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#location GoogleNetappVolume#location}
        :param name: The name of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#name GoogleNetappVolume#name}
        :param protocols: The protocol of the volume. Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#protocols GoogleNetappVolume#protocols}
        :param share_name: Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#share_name GoogleNetappVolume#share_name}
        :param storage_pool: Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#storage_pool GoogleNetappVolume#storage_pool}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_config GoogleNetappVolume#backup_config}
        :param deletion_policy: Policy to determine if the volume should be deleted forcefully. Volumes may have nested snapshot resources. Deleting such a volume will fail. Setting this parameter to FORCE will delete volumes including nested snapshots. Possible values: DEFAULT, FORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#deletion_policy GoogleNetappVolume#deletion_policy}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        :param export_policy: export_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#export_policy GoogleNetappVolume#export_policy}
        :param hybrid_replication_parameters: hybrid_replication_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hybrid_replication_parameters GoogleNetappVolume#hybrid_replication_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#id GoogleNetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kerberos_enabled: Flag indicating if the volume is a kerberos volume or not, export policy rules control kerberos security modes (krb5, krb5i, krb5p). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos_enabled GoogleNetappVolume#kerberos_enabled}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        :param large_capacity: Optional. Flag indicating if the volume will be a large capacity volume or a regular volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#large_capacity GoogleNetappVolume#large_capacity}
        :param multiple_endpoints: Optional. Flag indicating if the volume will have an IP address per node for volumes supporting multiple IP endpoints. Only the volume with largeCapacity will be allowed to have multiple endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#multiple_endpoints GoogleNetappVolume#multiple_endpoints}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#project GoogleNetappVolume#project}.
        :param restore_parameters: restore_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restore_parameters GoogleNetappVolume#restore_parameters}
        :param restricted_actions: List of actions that are restricted on this volume. Possible values: ["DELETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restricted_actions GoogleNetappVolume#restricted_actions}
        :param security_style: Security Style of the Volume. Use UNIX to use UNIX or NFSV4 ACLs for file permissions. Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#security_style GoogleNetappVolume#security_style}
        :param smb_settings: Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#smb_settings GoogleNetappVolume#smb_settings}
        :param snapshot_directory: If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_directory GoogleNetappVolume#snapshot_directory}
        :param snapshot_policy: snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_policy GoogleNetappVolume#snapshot_policy}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tiering_policy GoogleNetappVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#timeouts GoogleNetappVolume#timeouts}
        :param unix_permissions: Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#unix_permissions GoogleNetappVolume#unix_permissions}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_config, dict):
            backup_config = GoogleNetappVolumeBackupConfig(**backup_config)
        if isinstance(export_policy, dict):
            export_policy = GoogleNetappVolumeExportPolicy(**export_policy)
        if isinstance(hybrid_replication_parameters, dict):
            hybrid_replication_parameters = GoogleNetappVolumeHybridReplicationParameters(**hybrid_replication_parameters)
        if isinstance(restore_parameters, dict):
            restore_parameters = GoogleNetappVolumeRestoreParameters(**restore_parameters)
        if isinstance(snapshot_policy, dict):
            snapshot_policy = GoogleNetappVolumeSnapshotPolicy(**snapshot_policy)
        if isinstance(tiering_policy, dict):
            tiering_policy = GoogleNetappVolumeTieringPolicy(**tiering_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetappVolumeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9f8c33ba05cfd30e24d15d0d3b5785e3d256f968af7d78a49c40e8404b0acb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument capacity_gib", value=capacity_gib, expected_type=type_hints["capacity_gib"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
            check_type(argname="argument storage_pool", value=storage_pool, expected_type=type_hints["storage_pool"])
            check_type(argname="argument backup_config", value=backup_config, expected_type=type_hints["backup_config"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument export_policy", value=export_policy, expected_type=type_hints["export_policy"])
            check_type(argname="argument hybrid_replication_parameters", value=hybrid_replication_parameters, expected_type=type_hints["hybrid_replication_parameters"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kerberos_enabled", value=kerberos_enabled, expected_type=type_hints["kerberos_enabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument large_capacity", value=large_capacity, expected_type=type_hints["large_capacity"])
            check_type(argname="argument multiple_endpoints", value=multiple_endpoints, expected_type=type_hints["multiple_endpoints"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument restore_parameters", value=restore_parameters, expected_type=type_hints["restore_parameters"])
            check_type(argname="argument restricted_actions", value=restricted_actions, expected_type=type_hints["restricted_actions"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument smb_settings", value=smb_settings, expected_type=type_hints["smb_settings"])
            check_type(argname="argument snapshot_directory", value=snapshot_directory, expected_type=type_hints["snapshot_directory"])
            check_type(argname="argument snapshot_policy", value=snapshot_policy, expected_type=type_hints["snapshot_policy"])
            check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument unix_permissions", value=unix_permissions, expected_type=type_hints["unix_permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_gib": capacity_gib,
            "location": location,
            "name": name,
            "protocols": protocols,
            "share_name": share_name,
            "storage_pool": storage_pool,
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
        if backup_config is not None:
            self._values["backup_config"] = backup_config
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if description is not None:
            self._values["description"] = description
        if export_policy is not None:
            self._values["export_policy"] = export_policy
        if hybrid_replication_parameters is not None:
            self._values["hybrid_replication_parameters"] = hybrid_replication_parameters
        if id is not None:
            self._values["id"] = id
        if kerberos_enabled is not None:
            self._values["kerberos_enabled"] = kerberos_enabled
        if labels is not None:
            self._values["labels"] = labels
        if large_capacity is not None:
            self._values["large_capacity"] = large_capacity
        if multiple_endpoints is not None:
            self._values["multiple_endpoints"] = multiple_endpoints
        if project is not None:
            self._values["project"] = project
        if restore_parameters is not None:
            self._values["restore_parameters"] = restore_parameters
        if restricted_actions is not None:
            self._values["restricted_actions"] = restricted_actions
        if security_style is not None:
            self._values["security_style"] = security_style
        if smb_settings is not None:
            self._values["smb_settings"] = smb_settings
        if snapshot_directory is not None:
            self._values["snapshot_directory"] = snapshot_directory
        if snapshot_policy is not None:
            self._values["snapshot_policy"] = snapshot_policy
        if tiering_policy is not None:
            self._values["tiering_policy"] = tiering_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if unix_permissions is not None:
            self._values["unix_permissions"] = unix_permissions

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
    def capacity_gib(self) -> builtins.str:
        '''Capacity of the volume (in GiB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#capacity_gib GoogleNetappVolume#capacity_gib}
        '''
        result = self._values.get("capacity_gib")
        assert result is not None, "Required property 'capacity_gib' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Name of the pool location.

        Usually a region name, expect for some STANDARD service level pools which require a zone name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#location GoogleNetappVolume#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the volume. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#name GoogleNetappVolume#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocols(self) -> typing.List[builtins.str]:
        '''The protocol of the volume.

        Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#protocols GoogleNetappVolume#protocols}
        '''
        result = self._values.get("protocols")
        assert result is not None, "Required property 'protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def share_name(self) -> builtins.str:
        '''Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#share_name GoogleNetappVolume#share_name}
        '''
        result = self._values.get("share_name")
        assert result is not None, "Required property 'share_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_pool(self) -> builtins.str:
        '''Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#storage_pool GoogleNetappVolume#storage_pool}
        '''
        result = self._values.get("storage_pool")
        assert result is not None, "Required property 'storage_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_config(self) -> typing.Optional[GoogleNetappVolumeBackupConfig]:
        '''backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#backup_config GoogleNetappVolume#backup_config}
        '''
        result = self._values.get("backup_config")
        return typing.cast(typing.Optional[GoogleNetappVolumeBackupConfig], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine if the volume should be deleted forcefully.

        Volumes may have nested snapshot resources. Deleting such a volume will fail.
        Setting this parameter to FORCE will delete volumes including nested snapshots.
        Possible values: DEFAULT, FORCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#deletion_policy GoogleNetappVolume#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_policy(self) -> typing.Optional["GoogleNetappVolumeExportPolicy"]:
        '''export_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#export_policy GoogleNetappVolume#export_policy}
        '''
        result = self._values.get("export_policy")
        return typing.cast(typing.Optional["GoogleNetappVolumeExportPolicy"], result)

    @builtins.property
    def hybrid_replication_parameters(
        self,
    ) -> typing.Optional["GoogleNetappVolumeHybridReplicationParameters"]:
        '''hybrid_replication_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hybrid_replication_parameters GoogleNetappVolume#hybrid_replication_parameters}
        '''
        result = self._values.get("hybrid_replication_parameters")
        return typing.cast(typing.Optional["GoogleNetappVolumeHybridReplicationParameters"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#id GoogleNetappVolume#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag indicating if the volume is a kerberos volume or not, export policy rules control kerberos security modes (krb5, krb5i, krb5p).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos_enabled GoogleNetappVolume#kerberos_enabled}
        '''
        result = self._values.get("kerberos_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def large_capacity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Flag indicating if the volume will be a large capacity volume or a regular volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#large_capacity GoogleNetappVolume#large_capacity}
        '''
        result = self._values.get("large_capacity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def multiple_endpoints(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Flag indicating if the volume will have an IP address per node for volumes supporting multiple IP endpoints.
        Only the volume with largeCapacity will be allowed to have multiple endpoints.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#multiple_endpoints GoogleNetappVolume#multiple_endpoints}
        '''
        result = self._values.get("multiple_endpoints")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#project GoogleNetappVolume#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_parameters(
        self,
    ) -> typing.Optional["GoogleNetappVolumeRestoreParameters"]:
        '''restore_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restore_parameters GoogleNetappVolume#restore_parameters}
        '''
        result = self._values.get("restore_parameters")
        return typing.cast(typing.Optional["GoogleNetappVolumeRestoreParameters"], result)

    @builtins.property
    def restricted_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of actions that are restricted on this volume. Possible values: ["DELETE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#restricted_actions GoogleNetappVolume#restricted_actions}
        '''
        result = self._values.get("restricted_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_style(self) -> typing.Optional[builtins.str]:
        '''Security Style of the Volume.

        Use UNIX to use UNIX or NFSV4 ACLs for file permissions.
        Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#security_style GoogleNetappVolume#security_style}
        '''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smb_settings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#smb_settings GoogleNetappVolume#smb_settings}
        '''
        result = self._values.get("smb_settings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_directory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_directory GoogleNetappVolume#snapshot_directory}
        '''
        result = self._values.get("snapshot_directory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snapshot_policy(self) -> typing.Optional["GoogleNetappVolumeSnapshotPolicy"]:
        '''snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshot_policy GoogleNetappVolume#snapshot_policy}
        '''
        result = self._values.get("snapshot_policy")
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicy"], result)

    @builtins.property
    def tiering_policy(self) -> typing.Optional["GoogleNetappVolumeTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tiering_policy GoogleNetappVolume#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["GoogleNetappVolumeTieringPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNetappVolumeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#timeouts GoogleNetappVolume#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetappVolumeTimeouts"], result)

    @builtins.property
    def unix_permissions(self) -> typing.Optional[builtins.str]:
        '''Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#unix_permissions GoogleNetappVolume#unix_permissions}
        '''
        result = self._values.get("unix_permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeExportPolicy",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules"},
)
class GoogleNetappVolumeExportPolicy:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#rules GoogleNetappVolume#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3192070522e69d773c8a0dd3419d178a5a696d05c2e52e45033b899f02ffc9c)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rules": rules,
        }

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetappVolumeExportPolicyRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#rules GoogleNetappVolume#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetappVolumeExportPolicyRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeExportPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeExportPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeExportPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0dbd01efb2484e8ed5d0ac904fbd7399b3785e39631714fe4d4c3b020688c89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1891c7fc975fdd8bb53764c8bf321b019674989bd2f9091aa3d6a09e44b92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "GoogleNetappVolumeExportPolicyRulesList":
        return typing.cast("GoogleNetappVolumeExportPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetappVolumeExportPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetappVolumeExportPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeExportPolicy]:
        return typing.cast(typing.Optional[GoogleNetappVolumeExportPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeExportPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fe276db7ee0d92483afd2ea69ee9cd1e89b8f4951122ea5e781ef2782f6461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeExportPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "access_type": "accessType",
        "allowed_clients": "allowedClients",
        "has_root_access": "hasRootAccess",
        "kerberos5_i_read_only": "kerberos5IReadOnly",
        "kerberos5_i_read_write": "kerberos5IReadWrite",
        "kerberos5_p_read_only": "kerberos5PReadOnly",
        "kerberos5_p_read_write": "kerberos5PReadWrite",
        "kerberos5_read_only": "kerberos5ReadOnly",
        "kerberos5_read_write": "kerberos5ReadWrite",
        "nfsv3": "nfsv3",
        "nfsv4": "nfsv4",
    },
)
class GoogleNetappVolumeExportPolicyRules:
    def __init__(
        self,
        *,
        access_type: typing.Optional[builtins.str] = None,
        allowed_clients: typing.Optional[builtins.str] = None,
        has_root_access: typing.Optional[builtins.str] = None,
        kerberos5_i_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos5_i_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos5_p_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos5_p_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos5_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos5_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        nfsv3: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        nfsv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_type: Defines the access type for clients matching the 'allowedClients' specification. Possible values: ["READ_ONLY", "READ_WRITE", "READ_NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#access_type GoogleNetappVolume#access_type}
        :param allowed_clients: Defines the client ingress specification (allowed clients) as a comma separated list with IPv4 CIDRs or IPv4 host addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#allowed_clients GoogleNetappVolume#allowed_clients}
        :param has_root_access: If enabled, the root user (UID = 0) of the specified clients doesn't get mapped to nobody (UID = 65534). This is also known as no_root_squash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#has_root_access GoogleNetappVolume#has_root_access}
        :param kerberos5_i_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'integrity' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5i_read_only GoogleNetappVolume#kerberos5i_read_only}
        :param kerberos5_i_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'integrity' kerberos security mode. The 'kerberos5iReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5i_read_write GoogleNetappVolume#kerberos5i_read_write}
        :param kerberos5_p_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'privacy' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5p_read_only GoogleNetappVolume#kerberos5p_read_only}
        :param kerberos5_p_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'privacy' kerberos security mode. The 'kerberos5pReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5p_read_write GoogleNetappVolume#kerberos5p_read_write}
        :param kerberos5_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'authentication' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5_read_only GoogleNetappVolume#kerberos5_read_only}
        :param kerberos5_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'authentication' kerberos security mode. The 'kerberos5ReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5_read_write GoogleNetappVolume#kerberos5_read_write}
        :param nfsv3: Enable to apply the export rule to NFSV3 clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#nfsv3 GoogleNetappVolume#nfsv3}
        :param nfsv4: Enable to apply the export rule to NFSV4.1 clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#nfsv4 GoogleNetappVolume#nfsv4}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3b5628272f33af6cf812c1189624fdecfbf347146fcb6491a98e8c5711986e)
            check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
            check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
            check_type(argname="argument has_root_access", value=has_root_access, expected_type=type_hints["has_root_access"])
            check_type(argname="argument kerberos5_i_read_only", value=kerberos5_i_read_only, expected_type=type_hints["kerberos5_i_read_only"])
            check_type(argname="argument kerberos5_i_read_write", value=kerberos5_i_read_write, expected_type=type_hints["kerberos5_i_read_write"])
            check_type(argname="argument kerberos5_p_read_only", value=kerberos5_p_read_only, expected_type=type_hints["kerberos5_p_read_only"])
            check_type(argname="argument kerberos5_p_read_write", value=kerberos5_p_read_write, expected_type=type_hints["kerberos5_p_read_write"])
            check_type(argname="argument kerberos5_read_only", value=kerberos5_read_only, expected_type=type_hints["kerberos5_read_only"])
            check_type(argname="argument kerberos5_read_write", value=kerberos5_read_write, expected_type=type_hints["kerberos5_read_write"])
            check_type(argname="argument nfsv3", value=nfsv3, expected_type=type_hints["nfsv3"])
            check_type(argname="argument nfsv4", value=nfsv4, expected_type=type_hints["nfsv4"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_type is not None:
            self._values["access_type"] = access_type
        if allowed_clients is not None:
            self._values["allowed_clients"] = allowed_clients
        if has_root_access is not None:
            self._values["has_root_access"] = has_root_access
        if kerberos5_i_read_only is not None:
            self._values["kerberos5_i_read_only"] = kerberos5_i_read_only
        if kerberos5_i_read_write is not None:
            self._values["kerberos5_i_read_write"] = kerberos5_i_read_write
        if kerberos5_p_read_only is not None:
            self._values["kerberos5_p_read_only"] = kerberos5_p_read_only
        if kerberos5_p_read_write is not None:
            self._values["kerberos5_p_read_write"] = kerberos5_p_read_write
        if kerberos5_read_only is not None:
            self._values["kerberos5_read_only"] = kerberos5_read_only
        if kerberos5_read_write is not None:
            self._values["kerberos5_read_write"] = kerberos5_read_write
        if nfsv3 is not None:
            self._values["nfsv3"] = nfsv3
        if nfsv4 is not None:
            self._values["nfsv4"] = nfsv4

    @builtins.property
    def access_type(self) -> typing.Optional[builtins.str]:
        '''Defines the access type for clients matching the 'allowedClients' specification. Possible values: ["READ_ONLY", "READ_WRITE", "READ_NONE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#access_type GoogleNetappVolume#access_type}
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_clients(self) -> typing.Optional[builtins.str]:
        '''Defines the client ingress specification (allowed clients) as a comma separated list with IPv4 CIDRs or IPv4 host addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#allowed_clients GoogleNetappVolume#allowed_clients}
        '''
        result = self._values.get("allowed_clients")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_root_access(self) -> typing.Optional[builtins.str]:
        '''If enabled, the root user (UID = 0) of the specified clients doesn't get mapped to nobody (UID = 65534).

        This is also known as no_root_squash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#has_root_access GoogleNetappVolume#has_root_access}
        '''
        result = self._values.get("has_root_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos5_i_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'integrity' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5i_read_only GoogleNetappVolume#kerberos5i_read_only}
        '''
        result = self._values.get("kerberos5_i_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_i_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'integrity' kerberos security mode. The 'kerberos5iReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5i_read_write GoogleNetappVolume#kerberos5i_read_write}
        '''
        result = self._values.get("kerberos5_i_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_p_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'privacy' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5p_read_only GoogleNetappVolume#kerberos5p_read_only}
        '''
        result = self._values.get("kerberos5_p_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_p_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'privacy' kerberos security mode. The 'kerberos5pReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5p_read_write GoogleNetappVolume#kerberos5p_read_write}
        '''
        result = self._values.get("kerberos5_p_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'authentication' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5_read_only GoogleNetappVolume#kerberos5_read_only}
        '''
        result = self._values.get("kerberos5_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'authentication' kerberos security mode. The 'kerberos5ReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#kerberos5_read_write GoogleNetappVolume#kerberos5_read_write}
        '''
        result = self._values.get("kerberos5_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def nfsv3(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable to apply the export rule to NFSV3 clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#nfsv3 GoogleNetappVolume#nfsv3}
        '''
        result = self._values.get("nfsv3")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def nfsv4(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable to apply the export rule to NFSV4.1 clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#nfsv4 GoogleNetappVolume#nfsv4}
        '''
        result = self._values.get("nfsv4")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeExportPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeExportPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeExportPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed395a201d6ae5a57354cd320f7d18efe40681179b121c3c2bec160bedccb95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetappVolumeExportPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43585812ac9dfcad937f0d4b9f8a8eef8a992a232d1c87966dba20fcfafd4c59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetappVolumeExportPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa4cdde74c46e3a2d0bc9f1635d6c868e03f814e4e628b79f8efb657835e819)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b639e645178f0bbd85b55f94a9a45f6ec509b4b60cb6974e109d45ebfd5e8237)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69746b65d65abf7fd0ad7c529d41b01e525aefb32a8c23482cbb29b5a145bf60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetappVolumeExportPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetappVolumeExportPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetappVolumeExportPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31b90d662c61b06ade0e47c7b482662977b99c40e05ec7dc70b776abf13dfd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetappVolumeExportPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeExportPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c7a8197c1148491a7c6b0016e40fca6c7146912b5f73e02fd062e8ebf52ede2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccessType")
    def reset_access_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessType", []))

    @jsii.member(jsii_name="resetAllowedClients")
    def reset_allowed_clients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedClients", []))

    @jsii.member(jsii_name="resetHasRootAccess")
    def reset_has_root_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHasRootAccess", []))

    @jsii.member(jsii_name="resetKerberos5IReadOnly")
    def reset_kerberos5_i_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5IReadOnly", []))

    @jsii.member(jsii_name="resetKerberos5IReadWrite")
    def reset_kerberos5_i_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5IReadWrite", []))

    @jsii.member(jsii_name="resetKerberos5PReadOnly")
    def reset_kerberos5_p_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5PReadOnly", []))

    @jsii.member(jsii_name="resetKerberos5PReadWrite")
    def reset_kerberos5_p_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5PReadWrite", []))

    @jsii.member(jsii_name="resetKerberos5ReadOnly")
    def reset_kerberos5_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5ReadOnly", []))

    @jsii.member(jsii_name="resetKerberos5ReadWrite")
    def reset_kerberos5_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberos5ReadWrite", []))

    @jsii.member(jsii_name="resetNfsv3")
    def reset_nfsv3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsv3", []))

    @jsii.member(jsii_name="resetNfsv4")
    def reset_nfsv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsv4", []))

    @builtins.property
    @jsii.member(jsii_name="accessTypeInput")
    def access_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedClientsInput")
    def allowed_clients_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="hasRootAccessInput")
    def has_root_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hasRootAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5IReadOnlyInput")
    def kerberos5_i_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5IReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5IReadWriteInput")
    def kerberos5_i_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5IReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5PReadOnlyInput")
    def kerberos5_p_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5PReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5PReadWriteInput")
    def kerberos5_p_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5PReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5ReadOnlyInput")
    def kerberos5_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5ReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberos5ReadWriteInput")
    def kerberos5_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberos5ReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv3Input")
    def nfsv3_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv3Input"))

    @builtins.property
    @jsii.member(jsii_name="nfsv4Input")
    def nfsv4_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv4Input"))

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessType"))

    @access_type.setter
    def access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5015f19452b73a66582868534b445add7d79c3e2c976af1324c9249b96bb28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedClients")
    def allowed_clients(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedClients"))

    @allowed_clients.setter
    def allowed_clients(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b474dff35279928df5686c43db2cf140f881bcce8a493572ca0581b301f3f56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasRootAccess")
    def has_root_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hasRootAccess"))

    @has_root_access.setter
    def has_root_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892924244f4ccab8ad5e05d7f8c39b64d96cc6e3d8c6f083042427c4fa8fce78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hasRootAccess", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5IReadOnly")
    def kerberos5_i_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5IReadOnly"))

    @kerberos5_i_read_only.setter
    def kerberos5_i_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1c0ea56dc4a685e66ec206e5bb8b0618a5f6e6d84b835a8311193001c644cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5IReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5IReadWrite")
    def kerberos5_i_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5IReadWrite"))

    @kerberos5_i_read_write.setter
    def kerberos5_i_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe9c48bf1a34f4abdf7b0dccf2e80babe7743356e00b41b543725da99509c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5IReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5PReadOnly")
    def kerberos5_p_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5PReadOnly"))

    @kerberos5_p_read_only.setter
    def kerberos5_p_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f9ae0d573cb1b51795b068007d806c99567dfd8716cc5e023d1c1327efb154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5PReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5PReadWrite")
    def kerberos5_p_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5PReadWrite"))

    @kerberos5_p_read_write.setter
    def kerberos5_p_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b4d6119346d218871c482e27c46b16ff1ae6f97ab312f8eb7307c890bc9b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5PReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5ReadOnly")
    def kerberos5_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5ReadOnly"))

    @kerberos5_read_only.setter
    def kerberos5_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c8e8fcc745b1a22d8bd962cf9be53a3711063e5f934cf43ad49ebb28292973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5ReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberos5ReadWrite")
    def kerberos5_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberos5ReadWrite"))

    @kerberos5_read_write.setter
    def kerberos5_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e54f24cb2983fb0faa8c2035522d05d4c64e43c49c24b22917272afa521299a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberos5ReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv3")
    def nfsv3(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv3"))

    @nfsv3.setter
    def nfsv3(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba4a4674fe9acfdb44cd5d39ea7b4d8a571863a724cd281f946a969201b4987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv3", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv4")
    def nfsv4(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv4"))

    @nfsv4.setter
    def nfsv4(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__181cd4bca6c889a2d53b720d9f49f382323d74816748cea100a0359084c35165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeExportPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeExportPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeExportPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18becd0d3e6a6cc3caf83aa6934520276cb74ad79776e60ce0b891ac19a9fa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeHybridReplicationParameters",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_location": "clusterLocation",
        "description": "description",
        "labels": "labels",
        "peer_cluster_name": "peerClusterName",
        "peer_ip_addresses": "peerIpAddresses",
        "peer_svm_name": "peerSvmName",
        "peer_volume_name": "peerVolumeName",
        "replication": "replication",
    },
)
class GoogleNetappVolumeHybridReplicationParameters:
    def __init__(
        self,
        *,
        cluster_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        peer_cluster_name: typing.Optional[builtins.str] = None,
        peer_ip_addresses: typing.Optional[builtins.str] = None,
        peer_svm_name: typing.Optional[builtins.str] = None,
        peer_volume_name: typing.Optional[builtins.str] = None,
        replication: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_location: Optional. Name of source cluster location associated with the Hybrid replication. This is a free-form field for the display purpose only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cluster_location GoogleNetappVolume#cluster_location}
        :param description: Optional. Description of the replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        :param labels: Optional. Labels to be added to the replication as the key value pairs. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        :param peer_cluster_name: Required. Name of the user's local source cluster to be peered with the destination cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_cluster_name GoogleNetappVolume#peer_cluster_name}
        :param peer_ip_addresses: Required. List of node ip addresses to be peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_ip_addresses GoogleNetappVolume#peer_ip_addresses}
        :param peer_svm_name: Required. Name of the user's local source vserver svm to be peered with the destination vserver svm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_svm_name GoogleNetappVolume#peer_svm_name}
        :param peer_volume_name: Required. Name of the user's local source volume to be peered with the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_volume_name GoogleNetappVolume#peer_volume_name}
        :param replication: Required. Desired name for the replication of this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#replication GoogleNetappVolume#replication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb4719daf7e59648e6cb08e7b91b30c55ba310ef4f4d605ff9dae1b82425f47)
            check_type(argname="argument cluster_location", value=cluster_location, expected_type=type_hints["cluster_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument peer_cluster_name", value=peer_cluster_name, expected_type=type_hints["peer_cluster_name"])
            check_type(argname="argument peer_ip_addresses", value=peer_ip_addresses, expected_type=type_hints["peer_ip_addresses"])
            check_type(argname="argument peer_svm_name", value=peer_svm_name, expected_type=type_hints["peer_svm_name"])
            check_type(argname="argument peer_volume_name", value=peer_volume_name, expected_type=type_hints["peer_volume_name"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_location is not None:
            self._values["cluster_location"] = cluster_location
        if description is not None:
            self._values["description"] = description
        if labels is not None:
            self._values["labels"] = labels
        if peer_cluster_name is not None:
            self._values["peer_cluster_name"] = peer_cluster_name
        if peer_ip_addresses is not None:
            self._values["peer_ip_addresses"] = peer_ip_addresses
        if peer_svm_name is not None:
            self._values["peer_svm_name"] = peer_svm_name
        if peer_volume_name is not None:
            self._values["peer_volume_name"] = peer_volume_name
        if replication is not None:
            self._values["replication"] = replication

    @builtins.property
    def cluster_location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Name of source cluster location associated with the Hybrid replication. This is a free-form field for the display purpose only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cluster_location GoogleNetappVolume#cluster_location}
        '''
        result = self._values.get("cluster_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the replication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#description GoogleNetappVolume#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Labels to be added to the replication as the key value pairs.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#labels GoogleNetappVolume#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def peer_cluster_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source cluster to be peered with the destination cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_cluster_name GoogleNetappVolume#peer_cluster_name}
        '''
        result = self._values.get("peer_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ip_addresses(self) -> typing.Optional[builtins.str]:
        '''Required. List of node ip addresses to be peered with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_ip_addresses GoogleNetappVolume#peer_ip_addresses}
        '''
        result = self._values.get("peer_ip_addresses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_svm_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source vserver svm to be peered with the destination vserver svm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_svm_name GoogleNetappVolume#peer_svm_name}
        '''
        result = self._values.get("peer_svm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_volume_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source volume to be peered with the destination volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#peer_volume_name GoogleNetappVolume#peer_volume_name}
        '''
        result = self._values.get("peer_volume_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication(self) -> typing.Optional[builtins.str]:
        '''Required. Desired name for the replication of this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#replication GoogleNetappVolume#replication}
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeHybridReplicationParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeHybridReplicationParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeHybridReplicationParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a516ddfa6f092c0ca72a2607e500f5cf82aad1f7558c678c31ddc52aad5b80ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterLocation")
    def reset_cluster_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterLocation", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPeerClusterName")
    def reset_peer_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerClusterName", []))

    @jsii.member(jsii_name="resetPeerIpAddresses")
    def reset_peer_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpAddresses", []))

    @jsii.member(jsii_name="resetPeerSvmName")
    def reset_peer_svm_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerSvmName", []))

    @jsii.member(jsii_name="resetPeerVolumeName")
    def reset_peer_volume_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerVolumeName", []))

    @jsii.member(jsii_name="resetReplication")
    def reset_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplication", []))

    @builtins.property
    @jsii.member(jsii_name="clusterLocationInput")
    def cluster_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="peerClusterNameInput")
    def peer_cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerClusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpAddressesInput")
    def peer_ip_addresses_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="peerSvmNameInput")
    def peer_svm_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerSvmNameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerVolumeNameInput")
    def peer_volume_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerVolumeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationInput")
    def replication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterLocation")
    def cluster_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterLocation"))

    @cluster_location.setter
    def cluster_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9fe0b089ffebee967a16d389852112751b19da89b865b4cecfd2ab7e6cfd98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e22e5874f2248ad9102b30b48b9ab69b6659ab84d04ca2cb333f52b1e6affe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e1d3b28743ce10e86a5ca361326aefde98cb158831a5e15f44775794b71ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerClusterName")
    def peer_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerClusterName"))

    @peer_cluster_name.setter
    def peer_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b4762e80c0d1ccfc62aebc4ed3b02039ff8936a19a41b57274851269346bbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIpAddresses")
    def peer_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddresses"))

    @peer_ip_addresses.setter
    def peer_ip_addresses(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249d7c7c453b46afb41e7f7719c66a383d68d7a8f7bee4d120f2647597fc4c23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerSvmName")
    def peer_svm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSvmName"))

    @peer_svm_name.setter
    def peer_svm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5407ce13b482c7fc67c2a2d67d6197b00c2ab7934cb98004a8b4f9d08d5745e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSvmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerVolumeName")
    def peer_volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVolumeName"))

    @peer_volume_name.setter
    def peer_volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f206d7285c17c07a6603247f57da7961c79afdbaba8361afd325f0f86ec391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerVolumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replication")
    def replication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replication"))

    @replication.setter
    def replication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc617ef4180bd20a033ee5b7afc39e41748f940b80c25f0c8483e4cbfdfcc084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeHybridReplicationParameters]:
        return typing.cast(typing.Optional[GoogleNetappVolumeHybridReplicationParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeHybridReplicationParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd172387de1f99dfaeb16e9829a012e81fa4313a6faf3af6fc2df5caaff6ad9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeMountOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleNetappVolumeMountOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeMountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeMountOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeMountOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01e7fda37f7878f53b2399437c725ce1b551161eb69201c16eb2e87208c64dad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetappVolumeMountOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113acd8de542fdb2d53b1b5ae3a95f8d9a5e8de17707fc177c57522a74f0cec5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetappVolumeMountOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0535586930226854326e7a9bb69dfd3962b422d978f8367f2a96b121fbc86bb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b5d4c7a36d953d8a4a8cbd57b9c4b7aee5a5c2ae1a798d2b6a8bc3b7f76ed5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e999ffcd469025c17a33575ec7c99e8c869238133b71744f7344038cddcbfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleNetappVolumeMountOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeMountOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64a803f13f6dc13bfdd1b2164710ada5d52f4f34d1b250b80d9a92edf044aeeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="export")
    def export(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "export"))

    @builtins.property
    @jsii.member(jsii_name="exportFull")
    def export_full(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exportFull"))

    @builtins.property
    @jsii.member(jsii_name="instructions")
    def instructions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instructions"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeMountOptions]:
        return typing.cast(typing.Optional[GoogleNetappVolumeMountOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeMountOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0927a33bada0833c8cfc3acc438a8c96e57d4d3ddc38d2cb91163eb5659108e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeRestoreParameters",
    jsii_struct_bases=[],
    name_mapping={
        "source_backup": "sourceBackup",
        "source_snapshot": "sourceSnapshot",
    },
)
class GoogleNetappVolumeRestoreParameters:
    def __init__(
        self,
        *,
        source_backup: typing.Optional[builtins.str] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_backup: Full name of the backup to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/backupVaults/{{backupVaultId}}/backups/{{backup}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_backup GoogleNetappVolume#source_backup}
        :param source_snapshot: Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_snapshot GoogleNetappVolume#source_snapshot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15bcc9157d100c57c623a474cb59a3c70ad0256255afe73e558927d9c7f28a0)
            check_type(argname="argument source_backup", value=source_backup, expected_type=type_hints["source_backup"])
            check_type(argname="argument source_snapshot", value=source_snapshot, expected_type=type_hints["source_snapshot"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if source_backup is not None:
            self._values["source_backup"] = source_backup
        if source_snapshot is not None:
            self._values["source_snapshot"] = source_snapshot

    @builtins.property
    def source_backup(self) -> typing.Optional[builtins.str]:
        '''Full name of the backup to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/backupVaults/{{backupVaultId}}/backups/{{backup}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_backup GoogleNetappVolume#source_backup}
        '''
        result = self._values.get("source_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#source_snapshot GoogleNetappVolume#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeRestoreParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeRestoreParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeRestoreParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2315902f946e5368d2046a5f8e06b65615d4d89a7e40b4908416148d33577af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSourceBackup")
    def reset_source_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceBackup", []))

    @jsii.member(jsii_name="resetSourceSnapshot")
    def reset_source_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceSnapshot", []))

    @builtins.property
    @jsii.member(jsii_name="sourceBackupInput")
    def source_backup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshotInput")
    def source_snapshot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceBackup")
    def source_backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceBackup"))

    @source_backup.setter
    def source_backup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a569f6d8e0718ee4b8df1dce8ab06d1dcb0eee6d3d56d7f319d47dfa4765c2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fa04f19fb7fa523cb0f226cd37b9613ca98cd334e3ac89bd9a1d107d800705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeRestoreParameters]:
        return typing.cast(typing.Optional[GoogleNetappVolumeRestoreParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeRestoreParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf1f90093555a603fa6b69162787ce4f897cc2149fed69ba48ecd6e6dee3a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "enabled": "enabled",
        "hourly_schedule": "hourlySchedule",
        "monthly_schedule": "monthlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class GoogleNetappVolumeSnapshotPolicy:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hourly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        monthly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleNetappVolumeSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#daily_schedule GoogleNetappVolume#daily_schedule}
        :param enabled: Enables automated snapshot creation according to defined schedule. Default is false. To disable automatic snapshot creation you have to remove the whole snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#enabled GoogleNetappVolume#enabled}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hourly_schedule GoogleNetappVolume#hourly_schedule}
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#monthly_schedule GoogleNetappVolume#monthly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#weekly_schedule GoogleNetappVolume#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = GoogleNetappVolumeSnapshotPolicyDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = GoogleNetappVolumeSnapshotPolicyHourlySchedule(**hourly_schedule)
        if isinstance(monthly_schedule, dict):
            monthly_schedule = GoogleNetappVolumeSnapshotPolicyMonthlySchedule(**monthly_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = GoogleNetappVolumeSnapshotPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3848958d1dd418925ac5278c6c5c4a106bbd128f9860d5d11aa463ebf20d66)
            check_type(argname="argument daily_schedule", value=daily_schedule, expected_type=type_hints["daily_schedule"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument hourly_schedule", value=hourly_schedule, expected_type=type_hints["hourly_schedule"])
            check_type(argname="argument monthly_schedule", value=monthly_schedule, expected_type=type_hints["monthly_schedule"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily_schedule is not None:
            self._values["daily_schedule"] = daily_schedule
        if enabled is not None:
            self._values["enabled"] = enabled
        if hourly_schedule is not None:
            self._values["hourly_schedule"] = hourly_schedule
        if monthly_schedule is not None:
            self._values["monthly_schedule"] = monthly_schedule
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def daily_schedule(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicyDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#daily_schedule GoogleNetappVolume#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicyDailySchedule"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables automated snapshot creation according to defined schedule.

        Default is false.
        To disable automatic snapshot creation you have to remove the whole snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#enabled GoogleNetappVolume#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hourly_schedule(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicyHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hourly_schedule GoogleNetappVolume#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicyHourlySchedule"], result)

    @builtins.property
    def monthly_schedule(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicyMonthlySchedule"]:
        '''monthly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#monthly_schedule GoogleNetappVolume#monthly_schedule}
        '''
        result = self._values.get("monthly_schedule")
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicyMonthlySchedule"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#weekly_schedule GoogleNetappVolume#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeSnapshotPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyDailySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "hour": "hour",
        "minute": "minute",
    },
)
class GoogleNetappVolumeSnapshotPolicyDailySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the daily schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68da9a6568c22e0ce62676510712c06f17fd62097866eef8386c7249b39fc3db)
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshots_to_keep": snapshots_to_keep,
        }
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''The maximum number of snapshots to keep for the daily schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeSnapshotPolicyDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeSnapshotPolicyDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__355c4211630ff81485399ef2940ae7aaa44f1590add4b5c1b60ac792ec7a98a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHour")
    def reset_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHour", []))

    @jsii.member(jsii_name="resetMinute")
    def reset_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinute", []))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca452675143a4eafcf5295585a9e31de1e58a178f60ab130da9a28748402e28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d43c0b1eebcb62a3d484f51d3858043b09ca17afdeb50a77b86dc1704ccd48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10d7d106570b2b06a3578df14c7946e41ed737bd559c86f6b7df95c01fae057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627a449ca534dc6895c0a0890c34749a5e292fb0af97ddbb34ad9daf06134a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"snapshots_to_keep": "snapshotsToKeep", "minute": "minute"},
)
class GoogleNetappVolumeSnapshotPolicyHourlySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the hourly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622f4f9ef4b7a3e67e66a63751196c45dc19c40bc6309dfefa5d31fb1a3661d7)
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshots_to_keep": snapshots_to_keep,
        }
        if minute is not None:
            self._values["minute"] = minute

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''The maximum number of snapshots to keep for the hourly schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeSnapshotPolicyHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeSnapshotPolicyHourlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyHourlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e7f7a6e84e039f7bbc9cf706372a75527f2feb2c6e0946373d5c2f9b48c3ac7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinute")
    def reset_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinute", []))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150018c82c11f11e15fd20a348f612b1dde396f77ea6d0d3d4320a7e62c8114b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21cdd9d72e1c5cf7a1c9cc5c0f9624ba87c689f8683a0c7e51af64d68ad55f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e63c0c7675a0c7394d2041d61285104c580bb87fac24848294002b298f7348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyMonthlySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "days_of_month": "daysOfMonth",
        "hour": "hour",
        "minute": "minute",
    },
)
class GoogleNetappVolumeSnapshotPolicyMonthlySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        days_of_month: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the monthly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param days_of_month: Set the day or days of the month to make a snapshot (1-31). Accepts a comma separated number of days. Defaults to '1'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#days_of_month GoogleNetappVolume#days_of_month}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf9b912697b4e177730566f9f049b95e32542f0609a657171f53ea49cc98d17)
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshots_to_keep": snapshots_to_keep,
        }
        if days_of_month is not None:
            self._values["days_of_month"] = days_of_month
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''The maximum number of snapshots to keep for the monthly schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def days_of_month(self) -> typing.Optional[builtins.str]:
        '''Set the day or days of the month to make a snapshot (1-31).

        Accepts a comma separated number of days. Defaults to '1'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#days_of_month GoogleNetappVolume#days_of_month}
        '''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeSnapshotPolicyMonthlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeSnapshotPolicyMonthlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyMonthlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b00244d246efa6a1581fe49a1fd11a43de5a1c65af4c1cad8649ffe6cf4ef933)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDaysOfMonth")
    def reset_days_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfMonth", []))

    @jsii.member(jsii_name="resetHour")
    def reset_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHour", []))

    @jsii.member(jsii_name="resetMinute")
    def reset_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinute", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "daysOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03389f89703f7f1aaa4d9c4f9925b2bc76b47f4b37ca39a117884c06d673ea61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e27bd4e63a83309ece2de1d4601c088255cd387f8a2856d98f455bfd84119c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0ef9f04402943b3261d0cb32d9709bbe677b7266179890f78209c00771bd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974c4d533b1ec325399fe29d267df77d870475356cdc1ac2304b2baa7cbbb1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6412db2a28c0c1da39efbe68ef85ce9b93b34647aa63de963e9e89119322f1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetappVolumeSnapshotPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc57abf75c1c068c9593ba168f2903d9dea84eefc9ccdc41456b686dcb4afa04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDailySchedule")
    def put_daily_schedule(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the daily schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        value = GoogleNetappVolumeSnapshotPolicyDailySchedule(
            snapshots_to_keep=snapshots_to_keep, hour=hour, minute=minute
        )

        return typing.cast(None, jsii.invoke(self, "putDailySchedule", [value]))

    @jsii.member(jsii_name="putHourlySchedule")
    def put_hourly_schedule(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the hourly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        value = GoogleNetappVolumeSnapshotPolicyHourlySchedule(
            snapshots_to_keep=snapshots_to_keep, minute=minute
        )

        return typing.cast(None, jsii.invoke(self, "putHourlySchedule", [value]))

    @jsii.member(jsii_name="putMonthlySchedule")
    def put_monthly_schedule(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        days_of_month: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the monthly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param days_of_month: Set the day or days of the month to make a snapshot (1-31). Accepts a comma separated number of days. Defaults to '1'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#days_of_month GoogleNetappVolume#days_of_month}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        value = GoogleNetappVolumeSnapshotPolicyMonthlySchedule(
            snapshots_to_keep=snapshots_to_keep,
            days_of_month=days_of_month,
            hour=hour,
            minute=minute,
        )

        return typing.cast(None, jsii.invoke(self, "putMonthlySchedule", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the weekly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param day: Set the day or days of the week to make a snapshot. Accepts a comma separated days of the week. Defaults to 'Sunday'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#day GoogleNetappVolume#day}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        value = GoogleNetappVolumeSnapshotPolicyWeeklySchedule(
            snapshots_to_keep=snapshots_to_keep, day=day, hour=hour, minute=minute
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetDailySchedule")
    def reset_daily_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailySchedule", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetHourlySchedule")
    def reset_hourly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlySchedule", []))

    @jsii.member(jsii_name="resetMonthlySchedule")
    def reset_monthly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlySchedule", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="dailySchedule")
    def daily_schedule(
        self,
    ) -> GoogleNetappVolumeSnapshotPolicyDailyScheduleOutputReference:
        return typing.cast(GoogleNetappVolumeSnapshotPolicyDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(
        self,
    ) -> GoogleNetappVolumeSnapshotPolicyHourlyScheduleOutputReference:
        return typing.cast(GoogleNetappVolumeSnapshotPolicyHourlyScheduleOutputReference, jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="monthlySchedule")
    def monthly_schedule(
        self,
    ) -> GoogleNetappVolumeSnapshotPolicyMonthlyScheduleOutputReference:
        return typing.cast(GoogleNetappVolumeSnapshotPolicyMonthlyScheduleOutputReference, jsii.get(self, "monthlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "GoogleNetappVolumeSnapshotPolicyWeeklyScheduleOutputReference":
        return typing.cast("GoogleNetappVolumeSnapshotPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule], jsii.get(self, "dailyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyScheduleInput")
    def hourly_schedule_input(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyScheduleInput")
    def monthly_schedule_input(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule], jsii.get(self, "monthlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["GoogleNetappVolumeSnapshotPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["GoogleNetappVolumeSnapshotPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__42309f32be2456dee36305dcc0c7f759880f3959ff3c5f79aa3725feffcc0966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeSnapshotPolicy]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeSnapshotPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2219d9b4345fa2af20cd59247dafbe0a7bf0c1264effe099a767f0c38a084547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "day": "day",
        "hour": "hour",
        "minute": "minute",
    },
)
class GoogleNetappVolumeSnapshotPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the weekly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        :param day: Set the day or days of the week to make a snapshot. Accepts a comma separated days of the week. Defaults to 'Sunday'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#day GoogleNetappVolume#day}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f250966f5e207a80901adf4a6904db0d0f9c3d464d801a2190cdbf44226ba2d)
            check_type(argname="argument snapshots_to_keep", value=snapshots_to_keep, expected_type=type_hints["snapshots_to_keep"])
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshots_to_keep": snapshots_to_keep,
        }
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute

    @builtins.property
    def snapshots_to_keep(self) -> jsii.Number:
        '''The maximum number of snapshots to keep for the weekly schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#snapshots_to_keep GoogleNetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''Set the day or days of the week to make a snapshot.

        Accepts a comma separated days of the week. Defaults to 'Sunday'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#day GoogleNetappVolume#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#hour GoogleNetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#minute GoogleNetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeSnapshotPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeSnapshotPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeSnapshotPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc86d90fea4808f21260b653ea9d40796250ba602fc0203e8b3ec6245300eb8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetHour")
    def reset_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHour", []))

    @jsii.member(jsii_name="resetMinute")
    def reset_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinute", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="hourInput")
    def hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteInput")
    def minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minuteInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeepInput")
    def snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0e2f60b5de3387f0f06000672817863263b891c9c6fd3f817e3181d0e0ec09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed868dd3ecc9d04d6e9dee3d44bd9881eef1bc5ce6f34d29fe3cb2cb3ac45b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca1cca7a7ddeece8fa140a538be2fefc7dba0db86e742be7e5d8b81931e030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641e4f106f13f61d6e3eb6f8532bac046bd1a3f3a95c306d67e9c2391f40e469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetappVolumeSnapshotPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[GoogleNetappVolumeSnapshotPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeSnapshotPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daff0c86f3f00bbf17691e48e6cda3f12e4af94e298d83c445c74978e3e73434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cooling_threshold_days": "coolingThresholdDays",
        "tier_action": "tierAction",
    },
)
class GoogleNetappVolumeTieringPolicy:
    def __init__(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cooling_threshold_days GoogleNetappVolume#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tier_action GoogleNetappVolume#tier_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e2e8cc8691526ef058933bcb6eb13faf8ad9edf7c49ec4fd1f1198fc7993c0)
            check_type(argname="argument cooling_threshold_days", value=cooling_threshold_days, expected_type=type_hints["cooling_threshold_days"])
            check_type(argname="argument tier_action", value=tier_action, expected_type=type_hints["tier_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cooling_threshold_days is not None:
            self._values["cooling_threshold_days"] = cooling_threshold_days
        if tier_action is not None:
            self._values["tier_action"] = tier_action

    @builtins.property
    def cooling_threshold_days(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183.
        Default is 31.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#cooling_threshold_days GoogleNetappVolume#cooling_threshold_days}
        '''
        result = self._values.get("cooling_threshold_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_action(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#tier_action GoogleNetappVolume#tier_action}
        '''
        result = self._values.get("tier_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc151d399eef1e3b93c579e89b6170cb2f725ec40caf9b599a91c970d17e0215)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCoolingThresholdDays")
    def reset_cooling_threshold_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCoolingThresholdDays", []))

    @jsii.member(jsii_name="resetTierAction")
    def reset_tier_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTierAction", []))

    @builtins.property
    @jsii.member(jsii_name="coolingThresholdDaysInput")
    def cooling_threshold_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coolingThresholdDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="tierActionInput")
    def tier_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tierActionInput"))

    @builtins.property
    @jsii.member(jsii_name="coolingThresholdDays")
    def cooling_threshold_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "coolingThresholdDays"))

    @cooling_threshold_days.setter
    def cooling_threshold_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aab09342cbcdf88edcf8f245435a4c290b795c10df3290405b9ef9b9251248c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingThresholdDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierAction")
    def tier_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierAction"))

    @tier_action.setter
    def tier_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ada88ff661ddbfc725e6d5c2053d5e7dff89bf27360461e3e6ec1ccf77f546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleNetappVolumeTieringPolicy]:
        return typing.cast(typing.Optional[GoogleNetappVolumeTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetappVolumeTieringPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ccdfd72260041925f71d415c14e921392868aee7ffff85a71f5826e9a7279b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetappVolumeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#create GoogleNetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#delete GoogleNetappVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#update GoogleNetappVolume#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb5e7e408772f5d87b114d298655b0330685a072892523c6c1dfc06dad8d5ea)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#create GoogleNetappVolume#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#delete GoogleNetappVolume#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_volume#update GoogleNetappVolume#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappVolumeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappVolumeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappVolume.GoogleNetappVolumeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7618de6733bca85664dd771a98768bbfb22671d6208418f94dd1dae42717043)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e677257b6ffe391ae1f003e7863fb2804d7aed495c6bb250f57cdcaf3c6570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab9425928e7179605bbfdd3c32aa8d6bdf4fb47fd9745268fdf1bce9b8af1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cbc9a0c5a9d7cae5fe2332ca77226541ee59d52cd7b820fd393836529c298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7722fd0e315ddf6ffd4c5da61ea151bed650722e66a2389a2e77748693d7e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetappVolume",
    "GoogleNetappVolumeBackupConfig",
    "GoogleNetappVolumeBackupConfigOutputReference",
    "GoogleNetappVolumeConfig",
    "GoogleNetappVolumeExportPolicy",
    "GoogleNetappVolumeExportPolicyOutputReference",
    "GoogleNetappVolumeExportPolicyRules",
    "GoogleNetappVolumeExportPolicyRulesList",
    "GoogleNetappVolumeExportPolicyRulesOutputReference",
    "GoogleNetappVolumeHybridReplicationParameters",
    "GoogleNetappVolumeHybridReplicationParametersOutputReference",
    "GoogleNetappVolumeMountOptions",
    "GoogleNetappVolumeMountOptionsList",
    "GoogleNetappVolumeMountOptionsOutputReference",
    "GoogleNetappVolumeRestoreParameters",
    "GoogleNetappVolumeRestoreParametersOutputReference",
    "GoogleNetappVolumeSnapshotPolicy",
    "GoogleNetappVolumeSnapshotPolicyDailySchedule",
    "GoogleNetappVolumeSnapshotPolicyDailyScheduleOutputReference",
    "GoogleNetappVolumeSnapshotPolicyHourlySchedule",
    "GoogleNetappVolumeSnapshotPolicyHourlyScheduleOutputReference",
    "GoogleNetappVolumeSnapshotPolicyMonthlySchedule",
    "GoogleNetappVolumeSnapshotPolicyMonthlyScheduleOutputReference",
    "GoogleNetappVolumeSnapshotPolicyOutputReference",
    "GoogleNetappVolumeSnapshotPolicyWeeklySchedule",
    "GoogleNetappVolumeSnapshotPolicyWeeklyScheduleOutputReference",
    "GoogleNetappVolumeTieringPolicy",
    "GoogleNetappVolumeTieringPolicyOutputReference",
    "GoogleNetappVolumeTimeouts",
    "GoogleNetappVolumeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6e21c242e5dcbf9770c1425c3151ee1f6876e863d681a995d4539cd1698944e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_gib: builtins.str,
    location: builtins.str,
    name: builtins.str,
    protocols: typing.Sequence[builtins.str],
    share_name: builtins.str,
    storage_pool: builtins.str,
    backup_config: typing.Optional[typing.Union[GoogleNetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    export_policy: typing.Optional[typing.Union[GoogleNetappVolumeExportPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_replication_parameters: typing.Optional[typing.Union[GoogleNetappVolumeHybridReplicationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    restore_parameters: typing.Optional[typing.Union[GoogleNetappVolumeRestoreParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snapshot_policy: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[GoogleNetappVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unix_permissions: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ebf8e58191eb210917195c4ff7037647fd0649f60d263df1cb986e23cf4fa36a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2383f957af554b9fa4fa135909655ff5232b0e6ebd7c345d4af501e40870c06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112d80c76d5e01c875051577296a1e126d7cb366ac5df450ce2d20e78de7c306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__884104cb5a98da56bd9148d301d7b9deba71b4c6873eed69bbd22f8b80f7b843(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085837658cdd4ae457cf0806909b7acf6f6369a5e49fc8177af20709bb9bf919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9008003e60f3cff76439ce87f7cc2143dbaf140f765078963e61e1d1663f5f71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd63d2c7068d9c4a20dacd087d081f194c0e6ef47a9da6f02adfb28ceb039c1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9c0f5884f90379059dfc10defa991a9decadc8588d341bc63fdc7f4cdd82eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fe3178186f28a5242513d6845964ba78db4aaca946baa0828fd0f2b5c17614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660369efb141e6733a063305b733710be9b7e6e4880adcd94149f8587226935a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb757e7a4bc47ca182e449e1beb31842514e07ed09f05d1cb1fcd8d8989fa062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd87b16dfb03df2dc86ff41a0c8370a1f5d0e1b2adc59398117b58ef43055a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2823dff06595eb7a756168f3c87a70f4edfc4b3a8913f29690677da35715ba16(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e082f80c27e1691a9e7520c420d550f69f9f97dc8f40e9199125dcc5c13e2dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728bb42ca53c0e58f616f1a96885b0e562cffc0a02ec178fc8ff0bdc2cd024b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55745881bee27949417003ffd82086e7c356c131466d4b0d53fa123003d24b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0313c4c30f123ac82f06c368f80b91aa0aaa973d2090ef76d12e2669896b4247(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4927c238867fd269b0acfc8a448e0065a6422e8e3daf69b0d1279c7f5e3307(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329d9e72744f76615f2605d66ebc26c9768bb81ea337ce921f2f5320157a7ec7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e094a11ec734cc509348eaac3d5dc58bf664a9cecd5eb5f0ceae6f3a9a3778a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f961946daf98f960e6c3cab39d7ea827e9cd3c13f1dd5c809fec697e8dc0ccd(
    *,
    backup_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    backup_vault: typing.Optional[builtins.str] = None,
    scheduled_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f41467bbd52a249096aaf02c587eabecf40dcb0709c659e04d587f0a75ff83b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babf56a51a88a82e1b2fedd248424e454a234edd02a697c4c0f915ac03ede31c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c70cd0785497252ec8a8305fc71139b6fe2e50a620ee039ee0260c7177cea27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cab566fc6d8efdbc3b048d416d250a643592b09468118c191669a6f7bcc2ad3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfed497762409592b9a4c944ac3c65af0dfe98de85b5244ea1fc0dd4b2f7c039(
    value: typing.Optional[GoogleNetappVolumeBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9f8c33ba05cfd30e24d15d0d3b5785e3d256f968af7d78a49c40e8404b0acb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    capacity_gib: builtins.str,
    location: builtins.str,
    name: builtins.str,
    protocols: typing.Sequence[builtins.str],
    share_name: builtins.str,
    storage_pool: builtins.str,
    backup_config: typing.Optional[typing.Union[GoogleNetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    export_policy: typing.Optional[typing.Union[GoogleNetappVolumeExportPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_replication_parameters: typing.Optional[typing.Union[GoogleNetappVolumeHybridReplicationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    restore_parameters: typing.Optional[typing.Union[GoogleNetappVolumeRestoreParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snapshot_policy: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[GoogleNetappVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unix_permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3192070522e69d773c8a0dd3419d178a5a696d05c2e52e45033b899f02ffc9c(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetappVolumeExportPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dbd01efb2484e8ed5d0ac904fbd7399b3785e39631714fe4d4c3b020688c89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1891c7fc975fdd8bb53764c8bf321b019674989bd2f9091aa3d6a09e44b92b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetappVolumeExportPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fe276db7ee0d92483afd2ea69ee9cd1e89b8f4951122ea5e781ef2782f6461(
    value: typing.Optional[GoogleNetappVolumeExportPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3b5628272f33af6cf812c1189624fdecfbf347146fcb6491a98e8c5711986e(
    *,
    access_type: typing.Optional[builtins.str] = None,
    allowed_clients: typing.Optional[builtins.str] = None,
    has_root_access: typing.Optional[builtins.str] = None,
    kerberos5_i_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos5_i_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos5_p_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos5_p_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos5_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos5_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    nfsv3: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    nfsv4: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed395a201d6ae5a57354cd320f7d18efe40681179b121c3c2bec160bedccb95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43585812ac9dfcad937f0d4b9f8a8eef8a992a232d1c87966dba20fcfafd4c59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa4cdde74c46e3a2d0bc9f1635d6c868e03f814e4e628b79f8efb657835e819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b639e645178f0bbd85b55f94a9a45f6ec509b4b60cb6974e109d45ebfd5e8237(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69746b65d65abf7fd0ad7c529d41b01e525aefb32a8c23482cbb29b5a145bf60(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b90d662c61b06ade0e47c7b482662977b99c40e05ec7dc70b776abf13dfd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetappVolumeExportPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7a8197c1148491a7c6b0016e40fca6c7146912b5f73e02fd062e8ebf52ede2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5015f19452b73a66582868534b445add7d79c3e2c976af1324c9249b96bb28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b474dff35279928df5686c43db2cf140f881bcce8a493572ca0581b301f3f56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892924244f4ccab8ad5e05d7f8c39b64d96cc6e3d8c6f083042427c4fa8fce78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1c0ea56dc4a685e66ec206e5bb8b0618a5f6e6d84b835a8311193001c644cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe9c48bf1a34f4abdf7b0dccf2e80babe7743356e00b41b543725da99509c22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f9ae0d573cb1b51795b068007d806c99567dfd8716cc5e023d1c1327efb154(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b4d6119346d218871c482e27c46b16ff1ae6f97ab312f8eb7307c890bc9b6e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c8e8fcc745b1a22d8bd962cf9be53a3711063e5f934cf43ad49ebb28292973(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e54f24cb2983fb0faa8c2035522d05d4c64e43c49c24b22917272afa521299a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba4a4674fe9acfdb44cd5d39ea7b4d8a571863a724cd281f946a969201b4987(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181cd4bca6c889a2d53b720d9f49f382323d74816748cea100a0359084c35165(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18becd0d3e6a6cc3caf83aa6934520276cb74ad79776e60ce0b891ac19a9fa76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeExportPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb4719daf7e59648e6cb08e7b91b30c55ba310ef4f4d605ff9dae1b82425f47(
    *,
    cluster_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    peer_cluster_name: typing.Optional[builtins.str] = None,
    peer_ip_addresses: typing.Optional[builtins.str] = None,
    peer_svm_name: typing.Optional[builtins.str] = None,
    peer_volume_name: typing.Optional[builtins.str] = None,
    replication: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a516ddfa6f092c0ca72a2607e500f5cf82aad1f7558c678c31ddc52aad5b80ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9fe0b089ffebee967a16d389852112751b19da89b865b4cecfd2ab7e6cfd98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e22e5874f2248ad9102b30b48b9ab69b6659ab84d04ca2cb333f52b1e6affe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e1d3b28743ce10e86a5ca361326aefde98cb158831a5e15f44775794b71ee1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b4762e80c0d1ccfc62aebc4ed3b02039ff8936a19a41b57274851269346bbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249d7c7c453b46afb41e7f7719c66a383d68d7a8f7bee4d120f2647597fc4c23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5407ce13b482c7fc67c2a2d67d6197b00c2ab7934cb98004a8b4f9d08d5745e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f206d7285c17c07a6603247f57da7961c79afdbaba8361afd325f0f86ec391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc617ef4180bd20a033ee5b7afc39e41748f940b80c25f0c8483e4cbfdfcc084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd172387de1f99dfaeb16e9829a012e81fa4313a6faf3af6fc2df5caaff6ad9b(
    value: typing.Optional[GoogleNetappVolumeHybridReplicationParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e7fda37f7878f53b2399437c725ce1b551161eb69201c16eb2e87208c64dad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113acd8de542fdb2d53b1b5ae3a95f8d9a5e8de17707fc177c57522a74f0cec5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0535586930226854326e7a9bb69dfd3962b422d978f8367f2a96b121fbc86bb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b5d4c7a36d953d8a4a8cbd57b9c4b7aee5a5c2ae1a798d2b6a8bc3b7f76ed5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e999ffcd469025c17a33575ec7c99e8c869238133b71744f7344038cddcbfb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a803f13f6dc13bfdd1b2164710ada5d52f4f34d1b250b80d9a92edf044aeeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0927a33bada0833c8cfc3acc438a8c96e57d4d3ddc38d2cb91163eb5659108e6(
    value: typing.Optional[GoogleNetappVolumeMountOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15bcc9157d100c57c623a474cb59a3c70ad0256255afe73e558927d9c7f28a0(
    *,
    source_backup: typing.Optional[builtins.str] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2315902f946e5368d2046a5f8e06b65615d4d89a7e40b4908416148d33577af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a569f6d8e0718ee4b8df1dce8ab06d1dcb0eee6d3d56d7f319d47dfa4765c2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fa04f19fb7fa523cb0f226cd37b9613ca98cd334e3ac89bd9a1d107d800705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf1f90093555a603fa6b69162787ce4f897cc2149fed69ba48ecd6e6dee3a73(
    value: typing.Optional[GoogleNetappVolumeRestoreParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3848958d1dd418925ac5278c6c5c4a106bbd128f9860d5d11aa463ebf20d66(
    *,
    daily_schedule: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicyDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hourly_schedule: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicyHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    monthly_schedule: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicyMonthlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[GoogleNetappVolumeSnapshotPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68da9a6568c22e0ce62676510712c06f17fd62097866eef8386c7249b39fc3db(
    *,
    snapshots_to_keep: jsii.Number,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355c4211630ff81485399ef2940ae7aaa44f1590add4b5c1b60ac792ec7a98a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca452675143a4eafcf5295585a9e31de1e58a178f60ab130da9a28748402e28a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d43c0b1eebcb62a3d484f51d3858043b09ca17afdeb50a77b86dc1704ccd48(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10d7d106570b2b06a3578df14c7946e41ed737bd559c86f6b7df95c01fae057(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627a449ca534dc6895c0a0890c34749a5e292fb0af97ddbb34ad9daf06134a70(
    value: typing.Optional[GoogleNetappVolumeSnapshotPolicyDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622f4f9ef4b7a3e67e66a63751196c45dc19c40bc6309dfefa5d31fb1a3661d7(
    *,
    snapshots_to_keep: jsii.Number,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7f7a6e84e039f7bbc9cf706372a75527f2feb2c6e0946373d5c2f9b48c3ac7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150018c82c11f11e15fd20a348f612b1dde396f77ea6d0d3d4320a7e62c8114b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21cdd9d72e1c5cf7a1c9cc5c0f9624ba87c689f8683a0c7e51af64d68ad55f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e63c0c7675a0c7394d2041d61285104c580bb87fac24848294002b298f7348(
    value: typing.Optional[GoogleNetappVolumeSnapshotPolicyHourlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf9b912697b4e177730566f9f049b95e32542f0609a657171f53ea49cc98d17(
    *,
    snapshots_to_keep: jsii.Number,
    days_of_month: typing.Optional[builtins.str] = None,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00244d246efa6a1581fe49a1fd11a43de5a1c65af4c1cad8649ffe6cf4ef933(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03389f89703f7f1aaa4d9c4f9925b2bc76b47f4b37ca39a117884c06d673ea61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e27bd4e63a83309ece2de1d4601c088255cd387f8a2856d98f455bfd84119c8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0ef9f04402943b3261d0cb32d9709bbe677b7266179890f78209c00771bd07(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974c4d533b1ec325399fe29d267df77d870475356cdc1ac2304b2baa7cbbb1c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6412db2a28c0c1da39efbe68ef85ce9b93b34647aa63de963e9e89119322f1d4(
    value: typing.Optional[GoogleNetappVolumeSnapshotPolicyMonthlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc57abf75c1c068c9593ba168f2903d9dea84eefc9ccdc41456b686dcb4afa04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42309f32be2456dee36305dcc0c7f759880f3959ff3c5f79aa3725feffcc0966(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2219d9b4345fa2af20cd59247dafbe0a7bf0c1264effe099a767f0c38a084547(
    value: typing.Optional[GoogleNetappVolumeSnapshotPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f250966f5e207a80901adf4a6904db0d0f9c3d464d801a2190cdbf44226ba2d(
    *,
    snapshots_to_keep: jsii.Number,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc86d90fea4808f21260b653ea9d40796250ba602fc0203e8b3ec6245300eb8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0e2f60b5de3387f0f06000672817863263b891c9c6fd3f817e3181d0e0ec09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed868dd3ecc9d04d6e9dee3d44bd9881eef1bc5ce6f34d29fe3cb2cb3ac45b21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca1cca7a7ddeece8fa140a538be2fefc7dba0db86e742be7e5d8b81931e030d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641e4f106f13f61d6e3eb6f8532bac046bd1a3f3a95c306d67e9c2391f40e469(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daff0c86f3f00bbf17691e48e6cda3f12e4af94e298d83c445c74978e3e73434(
    value: typing.Optional[GoogleNetappVolumeSnapshotPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e2e8cc8691526ef058933bcb6eb13faf8ad9edf7c49ec4fd1f1198fc7993c0(
    *,
    cooling_threshold_days: typing.Optional[jsii.Number] = None,
    tier_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc151d399eef1e3b93c579e89b6170cb2f725ec40caf9b599a91c970d17e0215(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aab09342cbcdf88edcf8f245435a4c290b795c10df3290405b9ef9b9251248c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ada88ff661ddbfc725e6d5c2053d5e7dff89bf27360461e3e6ec1ccf77f546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ccdfd72260041925f71d415c14e921392868aee7ffff85a71f5826e9a7279b(
    value: typing.Optional[GoogleNetappVolumeTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb5e7e408772f5d87b114d298655b0330685a072892523c6c1dfc06dad8d5ea(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7618de6733bca85664dd771a98768bbfb22671d6208418f94dd1dae42717043(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e677257b6ffe391ae1f003e7863fb2804d7aed495c6bb250f57cdcaf3c6570(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab9425928e7179605bbfdd3c32aa8d6bdf4fb47fd9745268fdf1bce9b8af1cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cbc9a0c5a9d7cae5fe2332ca77226541ee59d52cd7b820fd393836529c298b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7722fd0e315ddf6ffd4c5da61ea151bed650722e66a2389a2e77748693d7e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappVolumeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

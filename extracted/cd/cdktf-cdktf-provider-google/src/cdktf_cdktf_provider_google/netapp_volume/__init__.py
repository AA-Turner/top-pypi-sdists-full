r'''
# `google_netapp_volume`

Refer to the Terraform Registry for docs: [`google_netapp_volume`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume).
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


class NetappVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolume",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume google_netapp_volume}.'''

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
        backup_config: typing.Optional[typing.Union["NetappVolumeBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        export_policy: typing.Optional[typing.Union["NetappVolumeExportPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_replication_parameters: typing.Optional[typing.Union["NetappVolumeHybridReplicationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        restore_parameters: typing.Optional[typing.Union["NetappVolumeRestoreParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_policy: typing.Optional[typing.Union["NetappVolumeSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["NetappVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        unix_permissions: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume google_netapp_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param capacity_gib: Capacity of the volume (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#capacity_gib NetappVolume#capacity_gib}
        :param location: Name of the pool location. Usually a region name, expect for some STANDARD service level pools which require a zone name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#location NetappVolume#location}
        :param name: The name of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#name NetappVolume#name}
        :param protocols: The protocol of the volume. Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#protocols NetappVolume#protocols}
        :param share_name: Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#share_name NetappVolume#share_name}
        :param storage_pool: Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#storage_pool NetappVolume#storage_pool}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_config NetappVolume#backup_config}
        :param deletion_policy: Policy to determine if the volume should be deleted forcefully. Volumes may have nested snapshot resources. Deleting such a volume will fail. Setting this parameter to FORCE will delete volumes including nested snapshots. Possible values: DEFAULT, FORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#deletion_policy NetappVolume#deletion_policy}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        :param export_policy: export_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#export_policy NetappVolume#export_policy}
        :param hybrid_replication_parameters: hybrid_replication_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hybrid_replication_parameters NetappVolume#hybrid_replication_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#id NetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kerberos_enabled: Flag indicating if the volume is a kerberos volume or not, export policy rules control kerberos security modes (krb5, krb5i, krb5p). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos_enabled NetappVolume#kerberos_enabled}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        :param large_capacity: Optional. Flag indicating if the volume will be a large capacity volume or a regular volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#large_capacity NetappVolume#large_capacity}
        :param multiple_endpoints: Optional. Flag indicating if the volume will have an IP address per node for volumes supporting multiple IP endpoints. Only the volume with largeCapacity will be allowed to have multiple endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#multiple_endpoints NetappVolume#multiple_endpoints}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#project NetappVolume#project}.
        :param restore_parameters: restore_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restore_parameters NetappVolume#restore_parameters}
        :param restricted_actions: List of actions that are restricted on this volume. Possible values: ["DELETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restricted_actions NetappVolume#restricted_actions}
        :param security_style: Security Style of the Volume. Use UNIX to use UNIX or NFSV4 ACLs for file permissions. Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#security_style NetappVolume#security_style}
        :param smb_settings: Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#smb_settings NetappVolume#smb_settings}
        :param snapshot_directory: If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_directory NetappVolume#snapshot_directory}
        :param snapshot_policy: snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_policy NetappVolume#snapshot_policy}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tiering_policy NetappVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#timeouts NetappVolume#timeouts}
        :param unix_permissions: Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#unix_permissions NetappVolume#unix_permissions}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756b0e0531c296683a1b515630718ef6075ccdc093df4f2b5e3e65a31d8be771)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappVolumeConfig(
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
        '''Generates CDKTF code for importing a NetappVolume resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappVolume to import.
        :param import_from_id: The id of the existing NetappVolume that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappVolume to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3368ebe2e6920e8c2d609e7f5147fafc5ca391cfc982906b6ec966adc4b499ae)
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
        :param backup_policies: Specify a single backup policy ID for scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupPolicies/{{backupPolicyName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_policies NetappVolume#backup_policies}
        :param backup_vault: ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_vault NetappVolume#backup_vault}
        :param scheduled_backup_enabled: When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#scheduled_backup_enabled NetappVolume#scheduled_backup_enabled}
        '''
        value = NetappVolumeBackupConfig(
            backup_policies=backup_policies,
            backup_vault=backup_vault,
            scheduled_backup_enabled=scheduled_backup_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupConfig", [value]))

    @jsii.member(jsii_name="putExportPolicy")
    def put_export_policy(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#rules NetappVolume#rules}
        '''
        value = NetappVolumeExportPolicy(rules=rules)

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
        :param cluster_location: Optional. Name of source cluster location associated with the Hybrid replication. This is a free-form field for the display purpose only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cluster_location NetappVolume#cluster_location}
        :param description: Optional. Description of the replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        :param labels: Optional. Labels to be added to the replication as the key value pairs. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        :param peer_cluster_name: Required. Name of the user's local source cluster to be peered with the destination cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_cluster_name NetappVolume#peer_cluster_name}
        :param peer_ip_addresses: Required. List of node ip addresses to be peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_ip_addresses NetappVolume#peer_ip_addresses}
        :param peer_svm_name: Required. Name of the user's local source vserver svm to be peered with the destination vserver svm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_svm_name NetappVolume#peer_svm_name}
        :param peer_volume_name: Required. Name of the user's local source volume to be peered with the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_volume_name NetappVolume#peer_volume_name}
        :param replication: Required. Desired name for the replication of this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#replication NetappVolume#replication}
        '''
        value = NetappVolumeHybridReplicationParameters(
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
        :param source_backup: Full name of the backup to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/backupVaults/{{backupVaultId}}/backups/{{backup}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_backup NetappVolume#source_backup}
        :param source_snapshot: Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_snapshot NetappVolume#source_snapshot}
        '''
        value = NetappVolumeRestoreParameters(
            source_backup=source_backup, source_snapshot=source_snapshot
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreParameters", [value]))

    @jsii.member(jsii_name="putSnapshotPolicy")
    def put_snapshot_policy(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hourly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        monthly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#daily_schedule NetappVolume#daily_schedule}
        :param enabled: Enables automated snapshot creation according to defined schedule. Default is false. To disable automatic snapshot creation you have to remove the whole snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#enabled NetappVolume#enabled}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hourly_schedule NetappVolume#hourly_schedule}
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#monthly_schedule NetappVolume#monthly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#weekly_schedule NetappVolume#weekly_schedule}
        '''
        value = NetappVolumeSnapshotPolicy(
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
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cooling_threshold_days NetappVolume#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tier_action NetappVolume#tier_action}
        '''
        value = NetappVolumeTieringPolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#create NetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#delete NetappVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#update NetappVolume#update}.
        '''
        value = NetappVolumeTimeouts(create=create, delete=delete, update=update)

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
    def backup_config(self) -> "NetappVolumeBackupConfigOutputReference":
        return typing.cast("NetappVolumeBackupConfigOutputReference", jsii.get(self, "backupConfig"))

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
    def export_policy(self) -> "NetappVolumeExportPolicyOutputReference":
        return typing.cast("NetappVolumeExportPolicyOutputReference", jsii.get(self, "exportPolicy"))

    @builtins.property
    @jsii.member(jsii_name="hasReplication")
    def has_replication(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasReplication"))

    @builtins.property
    @jsii.member(jsii_name="hybridReplicationParameters")
    def hybrid_replication_parameters(
        self,
    ) -> "NetappVolumeHybridReplicationParametersOutputReference":
        return typing.cast("NetappVolumeHybridReplicationParametersOutputReference", jsii.get(self, "hybridReplicationParameters"))

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
    def mount_options(self) -> "NetappVolumeMountOptionsList":
        return typing.cast("NetappVolumeMountOptionsList", jsii.get(self, "mountOptions"))

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
    def restore_parameters(self) -> "NetappVolumeRestoreParametersOutputReference":
        return typing.cast("NetappVolumeRestoreParametersOutputReference", jsii.get(self, "restoreParameters"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicy")
    def snapshot_policy(self) -> "NetappVolumeSnapshotPolicyOutputReference":
        return typing.cast("NetappVolumeSnapshotPolicyOutputReference", jsii.get(self, "snapshotPolicy"))

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
    def tiering_policy(self) -> "NetappVolumeTieringPolicyOutputReference":
        return typing.cast("NetappVolumeTieringPolicyOutputReference", jsii.get(self, "tieringPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappVolumeTimeoutsOutputReference":
        return typing.cast("NetappVolumeTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    def backup_config_input(self) -> typing.Optional["NetappVolumeBackupConfig"]:
        return typing.cast(typing.Optional["NetappVolumeBackupConfig"], jsii.get(self, "backupConfigInput"))

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
    def export_policy_input(self) -> typing.Optional["NetappVolumeExportPolicy"]:
        return typing.cast(typing.Optional["NetappVolumeExportPolicy"], jsii.get(self, "exportPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridReplicationParametersInput")
    def hybrid_replication_parameters_input(
        self,
    ) -> typing.Optional["NetappVolumeHybridReplicationParameters"]:
        return typing.cast(typing.Optional["NetappVolumeHybridReplicationParameters"], jsii.get(self, "hybridReplicationParametersInput"))

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
    ) -> typing.Optional["NetappVolumeRestoreParameters"]:
        return typing.cast(typing.Optional["NetappVolumeRestoreParameters"], jsii.get(self, "restoreParametersInput"))

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
    def snapshot_policy_input(self) -> typing.Optional["NetappVolumeSnapshotPolicy"]:
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicy"], jsii.get(self, "snapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="storagePoolInput")
    def storage_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storagePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="tieringPolicyInput")
    def tiering_policy_input(self) -> typing.Optional["NetappVolumeTieringPolicy"]:
        return typing.cast(typing.Optional["NetappVolumeTieringPolicy"], jsii.get(self, "tieringPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d2c2b78394d72bc9540ab85f3ba8e846fb1783db0b4e073bf76885dc01f1f2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49593e3fc444d52ad5c0028ce8dde7c0399c9a76d0425c01dc1d5e5fe6e4704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbebcb80fe350c829d3506f8a42a1fb1d00d72b4191ef3bc010d79ace32cf2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91f9c897a8b7c353e89f6548a4a593d12a528f9714c020405392299d4aa4b29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791797807756eb681ee483d1f53b3d8f5f586b79cc425639c2ea5f6bf3f57512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be259c99b8c21a3e24f43d8020919bb290217e55926f961788d0ddafeb4d3e0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__528fe80be900909771c427866707634044d0bd73631d9c934398c983910acc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "largeCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5507ce041c37d67f109449a8c33896c648d63f7b8599bddec2549865987aa035)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b090dfb02047f0c43ae3b39297ca0305c005719dd7db115b48d81f9d32cca1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multipleEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095de2e9ea5e6188c05dd57e05687eeee8bae4a7557acd51345610e81b35de3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54477555475da74738a410b06e6a79e099eaff9e56cf15e1284637e1c577b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f40217352c4224b2387a4aed75ec209b88a309900adf15b25947c943823324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restrictedActions")
    def restricted_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedActions"))

    @restricted_actions.setter
    def restricted_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d04df13e3f58227fda8360d6317ccd864164b5b4d6a126e05daf540bb1e0508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d16d1f73a1258b0486827e261f581a467e6ca4afde965f076a11b149946318d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec7f635296392f90e4d8bfc099237e97671c85f3d342a1f02b0503395d58cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="smbSettings")
    def smb_settings(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "smbSettings"))

    @smb_settings.setter
    def smb_settings(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9e270034d0660e5beaa24ce94e89653c9bf22deca17ed8de745884366e3b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab8faf8b3ae08491f9486c120a81020bfd37d52ee5c0945bba38326a0235078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotDirectory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storagePool")
    def storage_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storagePool"))

    @storage_pool.setter
    def storage_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9964dba1b3e73be05e75e7a74c2437af4fde5b8ae9dad48eb3fb1d2aa894d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storagePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixPermissions")
    def unix_permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unixPermissions"))

    @unix_permissions.setter
    def unix_permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457b991fc823149f77d4c6decbb2239a5ced5b22e3354fb1110ae0da5deb6e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixPermissions", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "backup_policies": "backupPolicies",
        "backup_vault": "backupVault",
        "scheduled_backup_enabled": "scheduledBackupEnabled",
    },
)
class NetappVolumeBackupConfig:
    def __init__(
        self,
        *,
        backup_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        backup_vault: typing.Optional[builtins.str] = None,
        scheduled_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_policies: Specify a single backup policy ID for scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupPolicies/{{backupPolicyName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_policies NetappVolume#backup_policies}
        :param backup_vault: ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_vault NetappVolume#backup_vault}
        :param scheduled_backup_enabled: When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#scheduled_backup_enabled NetappVolume#scheduled_backup_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821ac5814a922a46b6d368158d449c5781ce67ae288ed0156fc0f80bebcbb2aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_policies NetappVolume#backup_policies}
        '''
        result = self._values.get("backup_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def backup_vault(self) -> typing.Optional[builtins.str]:
        '''ID of the backup vault to use. A backup vault is reqired to create manual or scheduled backups. Format: 'projects/{{projectId}}/locations/{{location}}/backupVaults/{{backupVaultName}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_vault NetappVolume#backup_vault}
        '''
        result = self._values.get("backup_vault")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to true, scheduled backup is enabled on the volume. Omit if no backup_policy is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#scheduled_backup_enabled NetappVolume#scheduled_backup_enabled}
        '''
        result = self._values.get("scheduled_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a36cd85f4c184d02d7c836981b62c3849467b537c4c06e00aa709cfb1dfe6ff5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__affa0fc878851c0d1a3dddf308af097548383b46e76440b30ca7f570432aa356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPolicies", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupVault"))

    @backup_vault.setter
    def backup_vault(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae3756a786df4bf9aad4534eab3231db1a7362d4e0955d1dd5d9449b9a26774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3614eaa2739127ec4119c2073578b158134accb6bbcbc14bcf86713e55a4798e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeBackupConfig]:
        return typing.cast(typing.Optional[NetappVolumeBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NetappVolumeBackupConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a525a9e3c68642186578e3f2a630c6e2cf17d36aad02efb9b4d5750319488b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeConfig",
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
class NetappVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_config: typing.Optional[typing.Union[NetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        export_policy: typing.Optional[typing.Union["NetappVolumeExportPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        hybrid_replication_parameters: typing.Optional[typing.Union["NetappVolumeHybridReplicationParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        restore_parameters: typing.Optional[typing.Union["NetappVolumeRestoreParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snapshot_policy: typing.Optional[typing.Union["NetappVolumeSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tiering_policy: typing.Optional[typing.Union["NetappVolumeTieringPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param capacity_gib: Capacity of the volume (in GiB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#capacity_gib NetappVolume#capacity_gib}
        :param location: Name of the pool location. Usually a region name, expect for some STANDARD service level pools which require a zone name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#location NetappVolume#location}
        :param name: The name of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#name NetappVolume#name}
        :param protocols: The protocol of the volume. Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#protocols NetappVolume#protocols}
        :param share_name: Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#share_name NetappVolume#share_name}
        :param storage_pool: Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#storage_pool NetappVolume#storage_pool}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_config NetappVolume#backup_config}
        :param deletion_policy: Policy to determine if the volume should be deleted forcefully. Volumes may have nested snapshot resources. Deleting such a volume will fail. Setting this parameter to FORCE will delete volumes including nested snapshots. Possible values: DEFAULT, FORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#deletion_policy NetappVolume#deletion_policy}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        :param export_policy: export_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#export_policy NetappVolume#export_policy}
        :param hybrid_replication_parameters: hybrid_replication_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hybrid_replication_parameters NetappVolume#hybrid_replication_parameters}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#id NetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kerberos_enabled: Flag indicating if the volume is a kerberos volume or not, export policy rules control kerberos security modes (krb5, krb5i, krb5p). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos_enabled NetappVolume#kerberos_enabled}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        :param large_capacity: Optional. Flag indicating if the volume will be a large capacity volume or a regular volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#large_capacity NetappVolume#large_capacity}
        :param multiple_endpoints: Optional. Flag indicating if the volume will have an IP address per node for volumes supporting multiple IP endpoints. Only the volume with largeCapacity will be allowed to have multiple endpoints. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#multiple_endpoints NetappVolume#multiple_endpoints}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#project NetappVolume#project}.
        :param restore_parameters: restore_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restore_parameters NetappVolume#restore_parameters}
        :param restricted_actions: List of actions that are restricted on this volume. Possible values: ["DELETE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restricted_actions NetappVolume#restricted_actions}
        :param security_style: Security Style of the Volume. Use UNIX to use UNIX or NFSV4 ACLs for file permissions. Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#security_style NetappVolume#security_style}
        :param smb_settings: Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#smb_settings NetappVolume#smb_settings}
        :param snapshot_directory: If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_directory NetappVolume#snapshot_directory}
        :param snapshot_policy: snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_policy NetappVolume#snapshot_policy}
        :param tiering_policy: tiering_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tiering_policy NetappVolume#tiering_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#timeouts NetappVolume#timeouts}
        :param unix_permissions: Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#unix_permissions NetappVolume#unix_permissions}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_config, dict):
            backup_config = NetappVolumeBackupConfig(**backup_config)
        if isinstance(export_policy, dict):
            export_policy = NetappVolumeExportPolicy(**export_policy)
        if isinstance(hybrid_replication_parameters, dict):
            hybrid_replication_parameters = NetappVolumeHybridReplicationParameters(**hybrid_replication_parameters)
        if isinstance(restore_parameters, dict):
            restore_parameters = NetappVolumeRestoreParameters(**restore_parameters)
        if isinstance(snapshot_policy, dict):
            snapshot_policy = NetappVolumeSnapshotPolicy(**snapshot_policy)
        if isinstance(tiering_policy, dict):
            tiering_policy = NetappVolumeTieringPolicy(**tiering_policy)
        if isinstance(timeouts, dict):
            timeouts = NetappVolumeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad98a27455e58dfa336fd4f9f80e24e32892d5595644a44af81c9810ac4af2cf)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#capacity_gib NetappVolume#capacity_gib}
        '''
        result = self._values.get("capacity_gib")
        assert result is not None, "Required property 'capacity_gib' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Name of the pool location.

        Usually a region name, expect for some STANDARD service level pools which require a zone name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#location NetappVolume#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the volume. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#name NetappVolume#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocols(self) -> typing.List[builtins.str]:
        '''The protocol of the volume.

        Allowed combinations are '['NFSV3']', '['NFSV4']', '['SMB']', '['NFSV3', 'NFSV4']', '['SMB', 'NFSV3']' and '['SMB', 'NFSV4']'. Possible values: ["NFSV3", "NFSV4", "SMB"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#protocols NetappVolume#protocols}
        '''
        result = self._values.get("protocols")
        assert result is not None, "Required property 'protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def share_name(self) -> builtins.str:
        '''Share name (SMB) or export path (NFS) of the volume. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#share_name NetappVolume#share_name}
        '''
        result = self._values.get("share_name")
        assert result is not None, "Required property 'share_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_pool(self) -> builtins.str:
        '''Name of the storage pool to create the volume in. Pool needs enough spare capacity to accommodate the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#storage_pool NetappVolume#storage_pool}
        '''
        result = self._values.get("storage_pool")
        assert result is not None, "Required property 'storage_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_config(self) -> typing.Optional[NetappVolumeBackupConfig]:
        '''backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#backup_config NetappVolume#backup_config}
        '''
        result = self._values.get("backup_config")
        return typing.cast(typing.Optional[NetappVolumeBackupConfig], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine if the volume should be deleted forcefully.

        Volumes may have nested snapshot resources. Deleting such a volume will fail.
        Setting this parameter to FORCE will delete volumes including nested snapshots.
        Possible values: DEFAULT, FORCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#deletion_policy NetappVolume#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_policy(self) -> typing.Optional["NetappVolumeExportPolicy"]:
        '''export_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#export_policy NetappVolume#export_policy}
        '''
        result = self._values.get("export_policy")
        return typing.cast(typing.Optional["NetappVolumeExportPolicy"], result)

    @builtins.property
    def hybrid_replication_parameters(
        self,
    ) -> typing.Optional["NetappVolumeHybridReplicationParameters"]:
        '''hybrid_replication_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hybrid_replication_parameters NetappVolume#hybrid_replication_parameters}
        '''
        result = self._values.get("hybrid_replication_parameters")
        return typing.cast(typing.Optional["NetappVolumeHybridReplicationParameters"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#id NetappVolume#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos_enabled NetappVolume#kerberos_enabled}
        '''
        result = self._values.get("kerberos_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def large_capacity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional. Flag indicating if the volume will be a large capacity volume or a regular volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#large_capacity NetappVolume#large_capacity}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#multiple_endpoints NetappVolume#multiple_endpoints}
        '''
        result = self._values.get("multiple_endpoints")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#project NetappVolume#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_parameters(self) -> typing.Optional["NetappVolumeRestoreParameters"]:
        '''restore_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restore_parameters NetappVolume#restore_parameters}
        '''
        result = self._values.get("restore_parameters")
        return typing.cast(typing.Optional["NetappVolumeRestoreParameters"], result)

    @builtins.property
    def restricted_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of actions that are restricted on this volume. Possible values: ["DELETE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#restricted_actions NetappVolume#restricted_actions}
        '''
        result = self._values.get("restricted_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_style(self) -> typing.Optional[builtins.str]:
        '''Security Style of the Volume.

        Use UNIX to use UNIX or NFSV4 ACLs for file permissions.
        Use NTFS to use NTFS ACLs for file permissions. Can only be set for volumes which use SMB together with NFS as protocol. Possible values: ["NTFS", "UNIX"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#security_style NetappVolume#security_style}
        '''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smb_settings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Settings for volumes with SMB access. Possible values: ["ENCRYPT_DATA", "BROWSABLE", "CHANGE_NOTIFY", "NON_BROWSABLE", "OPLOCKS", "SHOW_SNAPSHOT", "SHOW_PREVIOUS_VERSIONS", "ACCESS_BASED_ENUMERATION", "CONTINUOUSLY_AVAILABLE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#smb_settings NetappVolume#smb_settings}
        '''
        result = self._values.get("smb_settings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_directory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled, a NFS volume will contain a read-only .snapshot directory which provides access to each of the volume's snapshots. Will enable "Previous Versions" support for SMB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_directory NetappVolume#snapshot_directory}
        '''
        result = self._values.get("snapshot_directory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snapshot_policy(self) -> typing.Optional["NetappVolumeSnapshotPolicy"]:
        '''snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshot_policy NetappVolume#snapshot_policy}
        '''
        result = self._values.get("snapshot_policy")
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicy"], result)

    @builtins.property
    def tiering_policy(self) -> typing.Optional["NetappVolumeTieringPolicy"]:
        '''tiering_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tiering_policy NetappVolume#tiering_policy}
        '''
        result = self._values.get("tiering_policy")
        return typing.cast(typing.Optional["NetappVolumeTieringPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappVolumeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#timeouts NetappVolume#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappVolumeTimeouts"], result)

    @builtins.property
    def unix_permissions(self) -> typing.Optional[builtins.str]:
        '''Unix permission the mount point will be created with. Default is 0770. Applicable for UNIX security style volumes only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#unix_permissions NetappVolume#unix_permissions}
        '''
        result = self._values.get("unix_permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeExportPolicy",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules"},
)
class NetappVolumeExportPolicy:
    def __init__(
        self,
        *,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#rules NetappVolume#rules}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a90f90d6a1dcf18b544dba035ef668febee31b34316d57ec43fd11b327a95d)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rules": rules,
        }

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#rules NetappVolume#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeExportPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeExportPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeExportPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df67f14ae8bedbe0ae45145db4a3a41a61f37fbf96536153805404d39c6b9011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fc347e449150a35830d1d7773494383975bb86e9389c3985354faac956234c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "NetappVolumeExportPolicyRulesList":
        return typing.cast("NetappVolumeExportPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeExportPolicy]:
        return typing.cast(typing.Optional[NetappVolumeExportPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NetappVolumeExportPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__143c08148da09b616b83f498cc3b0b6825df4ca6613d4773ef4b6a118991efae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeExportPolicyRules",
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
class NetappVolumeExportPolicyRules:
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
        :param access_type: Defines the access type for clients matching the 'allowedClients' specification. Possible values: ["READ_ONLY", "READ_WRITE", "READ_NONE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#access_type NetappVolume#access_type}
        :param allowed_clients: Defines the client ingress specification (allowed clients) as a comma separated list with IPv4 CIDRs or IPv4 host addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#allowed_clients NetappVolume#allowed_clients}
        :param has_root_access: If enabled, the root user (UID = 0) of the specified clients doesn't get mapped to nobody (UID = 65534). This is also known as no_root_squash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#has_root_access NetappVolume#has_root_access}
        :param kerberos5_i_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'integrity' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5i_read_only NetappVolume#kerberos5i_read_only}
        :param kerberos5_i_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'integrity' kerberos security mode. The 'kerberos5iReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5i_read_write NetappVolume#kerberos5i_read_write}
        :param kerberos5_p_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'privacy' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5p_read_only NetappVolume#kerberos5p_read_only}
        :param kerberos5_p_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'privacy' kerberos security mode. The 'kerberos5pReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5p_read_write NetappVolume#kerberos5p_read_write}
        :param kerberos5_read_only: If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'authentication' kerberos security mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5_read_only NetappVolume#kerberos5_read_only}
        :param kerberos5_read_write: If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification. It enables nfs clients to mount using 'authentication' kerberos security mode. The 'kerberos5ReadOnly' value is ignored if this is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5_read_write NetappVolume#kerberos5_read_write}
        :param nfsv3: Enable to apply the export rule to NFSV3 clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#nfsv3 NetappVolume#nfsv3}
        :param nfsv4: Enable to apply the export rule to NFSV4.1 clients. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#nfsv4 NetappVolume#nfsv4}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99bf72bf1e8172cb9eeabe38e4be2a396d9555134a81b25d995862a62b67d66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#access_type NetappVolume#access_type}
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_clients(self) -> typing.Optional[builtins.str]:
        '''Defines the client ingress specification (allowed clients) as a comma separated list with IPv4 CIDRs or IPv4 host addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#allowed_clients NetappVolume#allowed_clients}
        '''
        result = self._values.get("allowed_clients")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_root_access(self) -> typing.Optional[builtins.str]:
        '''If enabled, the root user (UID = 0) of the specified clients doesn't get mapped to nobody (UID = 65534).

        This is also known as no_root_squash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#has_root_access NetappVolume#has_root_access}
        '''
        result = self._values.get("has_root_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos5_i_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'integrity' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5i_read_only NetappVolume#kerberos5i_read_only}
        '''
        result = self._values.get("kerberos5_i_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_i_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'integrity' kerberos security mode. The 'kerberos5iReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5i_read_write NetappVolume#kerberos5i_read_write}
        '''
        result = self._values.get("kerberos5_i_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_p_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'privacy' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5p_read_only NetappVolume#kerberos5p_read_only}
        '''
        result = self._values.get("kerberos5_p_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_p_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'privacy' kerberos security mode. The 'kerberos5pReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5p_read_write NetappVolume#kerberos5p_read_write}
        '''
        result = self._values.get("kerberos5_p_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines a read only access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'authentication' kerberos security mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5_read_only NetappVolume#kerberos5_read_only}
        '''
        result = self._values.get("kerberos5_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos5_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled (true) the rule defines read and write access for clients matching the 'allowedClients' specification.

        It enables nfs clients to mount using 'authentication' kerberos security mode. The 'kerberos5ReadOnly' value is ignored if this is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#kerberos5_read_write NetappVolume#kerberos5_read_write}
        '''
        result = self._values.get("kerberos5_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def nfsv3(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable to apply the export rule to NFSV3 clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#nfsv3 NetappVolume#nfsv3}
        '''
        result = self._values.get("nfsv3")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def nfsv4(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable to apply the export rule to NFSV4.1 clients.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#nfsv4 NetappVolume#nfsv4}
        '''
        result = self._values.get("nfsv4")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeExportPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeExportPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeExportPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a96de88b4e1c795e5dae4dd239669b3bc506738076d4a31f1e66f94c6a68226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetappVolumeExportPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1599b8c7e08127ed57befb15a9eedca985ea88059de9c9a2a1ea38eb1886d4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeExportPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2929469446c8d6b5afedae3bc04cd466cb6a920be64ba0da06b7d04c2fe979)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e248f0b1d01f7ec23989a2253ec804ea082d4481481a7f11d7fd2325b13f9c9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0f187cc75ab65ef42cb36207252b3b93cc16c1b5811de0bfd50d2e11c9c690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242422ef16556c1c50284face054670c2eb66951acac79a8db539c20e412cf23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeExportPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeExportPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f252439190fe25679dfee6f85495600f092051ab8c155eee2287db83443bcd9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8524a3f4d138676288378527a496dbed7749065a4e86fcae36e72ae67ee4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedClients")
    def allowed_clients(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedClients"))

    @allowed_clients.setter
    def allowed_clients(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b666b8f97502df43cd0d1f0f6ceedd7ed6898a78b3187d1472e4977291001ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hasRootAccess")
    def has_root_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hasRootAccess"))

    @has_root_access.setter
    def has_root_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3afc66b87207a8f96ca5db6c9fea7db874b18773c729ce199f1acb67d17b189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c5539f8c17ff379e138cfdd96530d839f462ee5dd0fffc8bc5cc430f090db8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8305515f63f61ca64be49741610eee5f5ff4a6f82d8db030510ff9e0c7184889)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69fe95db5a564205e459ec264731035984973885f33b85aa3c636b3c087a94b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9379db7a9973bd6555591b8ed469f3f9f8a6387b277276cf72930b6505ae70d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7378a1a742cffb560755ca5e109532210c49f1f6b4a28a5000d4ed111a22cd50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b23be5d5111396d13ba140fb64e3d971729fb97e0dae0f1b334d27103241c1f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24275cd337e67bb13c700d614eebca86ec2495b37af184be7cb41b7178033b87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc96ce83673cf4f93478e3f78bfaf01196c638d726f1a2b9fe4dae4aeb3baa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv4", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeExportPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeExportPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeExportPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488231851f702c806e040b55217664a29dfefa464a50eb53beb3790b63bc6fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeHybridReplicationParameters",
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
class NetappVolumeHybridReplicationParameters:
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
        :param cluster_location: Optional. Name of source cluster location associated with the Hybrid replication. This is a free-form field for the display purpose only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cluster_location NetappVolume#cluster_location}
        :param description: Optional. Description of the replication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        :param labels: Optional. Labels to be added to the replication as the key value pairs. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        :param peer_cluster_name: Required. Name of the user's local source cluster to be peered with the destination cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_cluster_name NetappVolume#peer_cluster_name}
        :param peer_ip_addresses: Required. List of node ip addresses to be peered with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_ip_addresses NetappVolume#peer_ip_addresses}
        :param peer_svm_name: Required. Name of the user's local source vserver svm to be peered with the destination vserver svm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_svm_name NetappVolume#peer_svm_name}
        :param peer_volume_name: Required. Name of the user's local source volume to be peered with the destination volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_volume_name NetappVolume#peer_volume_name}
        :param replication: Required. Desired name for the replication of this volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#replication NetappVolume#replication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20681fc7aa5103bc85b61d250ac9e34cc01799a568085b0e4dc64b12a30b25db)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cluster_location NetappVolume#cluster_location}
        '''
        result = self._values.get("cluster_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Description of the replication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#description NetappVolume#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Labels to be added to the replication as the key value pairs.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#labels NetappVolume#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def peer_cluster_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source cluster to be peered with the destination cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_cluster_name NetappVolume#peer_cluster_name}
        '''
        result = self._values.get("peer_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ip_addresses(self) -> typing.Optional[builtins.str]:
        '''Required. List of node ip addresses to be peered with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_ip_addresses NetappVolume#peer_ip_addresses}
        '''
        result = self._values.get("peer_ip_addresses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_svm_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source vserver svm to be peered with the destination vserver svm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_svm_name NetappVolume#peer_svm_name}
        '''
        result = self._values.get("peer_svm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_volume_name(self) -> typing.Optional[builtins.str]:
        '''Required. Name of the user's local source volume to be peered with the destination volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#peer_volume_name NetappVolume#peer_volume_name}
        '''
        result = self._values.get("peer_volume_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication(self) -> typing.Optional[builtins.str]:
        '''Required. Desired name for the replication of this volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#replication NetappVolume#replication}
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeHybridReplicationParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeHybridReplicationParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeHybridReplicationParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c70921ef447ebc606b8260ba562e33efd4c7353766f02670278c0cbce07fcf24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e72a65fec7f910fbb85a183cc1a6dd2c953f3a01e0c8403bbdda7d35fd0632b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3709a64fc5705ba454568ddbd86a4fbca213abcf961aa2f9cbcd6491fa53c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b8e6a0dbe12fccad54b642ac3f248df89bfc5426ee7eee91fbc94c02afdaf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerClusterName")
    def peer_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerClusterName"))

    @peer_cluster_name.setter
    def peer_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864ea075683fdbdadd6174730d753e0038c819c3442568b2affb9248068bdec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerIpAddresses")
    def peer_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddresses"))

    @peer_ip_addresses.setter
    def peer_ip_addresses(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea46649dd074344e88821c837e3c7294e2834483fb5691b581d423c9779338a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerSvmName")
    def peer_svm_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerSvmName"))

    @peer_svm_name.setter
    def peer_svm_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4db3e28eac933b61283943baa4aaff6a0eace3e45be9342ac97ed68f48f0b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerSvmName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerVolumeName")
    def peer_volume_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVolumeName"))

    @peer_volume_name.setter
    def peer_volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18483e4d12ccc0d632ec46ac18e964a4ab8864c17f04565fca3c496d598dcf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerVolumeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replication")
    def replication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replication"))

    @replication.setter
    def replication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856811874888454a1d0e0386761ecdfd0be6d84b5174c5405239640dc7a698d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeHybridReplicationParameters]:
        return typing.cast(typing.Optional[NetappVolumeHybridReplicationParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeHybridReplicationParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4452a8d2f0f643b89aa92c6f1e4c55b50b2234bdc6f0a56897af5356cf40b9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeMountOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetappVolumeMountOptions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeMountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeMountOptionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeMountOptionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b89202a878d01b259006a10ec8326c9f3d6c978164eea0629fc38b84993c304a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetappVolumeMountOptionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de8e0187d9eb890b101de78cc6ee4dca301449b7274cea5ba56ab3666b4d0ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeMountOptionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a0216d3c15e39b163a1284794ebfcde3bd3b5ea94616546743aa6ef3fc4689)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b9605a866d500913510ce60ef441ffe5817d5bfe22e78ab41d28a89129e521)
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
            type_hints = typing.get_type_hints(_typecheckingstub__905a6bacc2a00bc6adcd9aeb9da19904080e51f9a799a58e93ca9576d7bcb583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetappVolumeMountOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeMountOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7e67dd3b1fa8006816c258649f30f6cc72daaff55c3b6c3f065ec662d2d4d31)
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
    def internal_value(self) -> typing.Optional[NetappVolumeMountOptions]:
        return typing.cast(typing.Optional[NetappVolumeMountOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NetappVolumeMountOptions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3cde023d481c3b14ab10282a548ed434b8e8b9978b821f6afab0b0e2a69108a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeRestoreParameters",
    jsii_struct_bases=[],
    name_mapping={
        "source_backup": "sourceBackup",
        "source_snapshot": "sourceSnapshot",
    },
)
class NetappVolumeRestoreParameters:
    def __init__(
        self,
        *,
        source_backup: typing.Optional[builtins.str] = None,
        source_snapshot: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_backup: Full name of the backup to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/backupVaults/{{backupVaultId}}/backups/{{backup}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_backup NetappVolume#source_backup}
        :param source_snapshot: Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_snapshot NetappVolume#source_snapshot}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4c82883f88ec04ab7dcbf1a0f0e0f56cdbd116d885aa3ebe10641743dd7173)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_backup NetappVolume#source_backup}
        '''
        result = self._values.get("source_backup")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_snapshot(self) -> typing.Optional[builtins.str]:
        '''Full name of the snapshot to use for creating this volume. 'source_snapshot' and 'source_backup' cannot be used simultaneously. Format: 'projects/{{project}}/locations/{{location}}/volumes/{{volume}}/snapshots/{{snapshot}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#source_snapshot NetappVolume#source_snapshot}
        '''
        result = self._values.get("source_snapshot")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeRestoreParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeRestoreParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeRestoreParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__539bcb433add9ffb54cb971e4cbd87e1bb91faca915d3e1d18acaa588093bd8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f087cbbaffd830f93909c3e8339abb832e8cba6c555b35590bfb2ea3c61a660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceSnapshot")
    def source_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceSnapshot"))

    @source_snapshot.setter
    def source_snapshot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7faf9ebe256eae4b6b7d890ef1026e68a988e00602682b2f10fb0bfb8ea405ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeRestoreParameters]:
        return typing.cast(typing.Optional[NetappVolumeRestoreParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeRestoreParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680d3801714509aef9991884d6a039b7cc491a5c52819d43cbcc78c1c4088e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "daily_schedule": "dailySchedule",
        "enabled": "enabled",
        "hourly_schedule": "hourlySchedule",
        "monthly_schedule": "monthlySchedule",
        "weekly_schedule": "weeklySchedule",
    },
)
class NetappVolumeSnapshotPolicy:
    def __init__(
        self,
        *,
        daily_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyDailySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hourly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyHourlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        monthly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyMonthlySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["NetappVolumeSnapshotPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param daily_schedule: daily_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#daily_schedule NetappVolume#daily_schedule}
        :param enabled: Enables automated snapshot creation according to defined schedule. Default is false. To disable automatic snapshot creation you have to remove the whole snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#enabled NetappVolume#enabled}
        :param hourly_schedule: hourly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hourly_schedule NetappVolume#hourly_schedule}
        :param monthly_schedule: monthly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#monthly_schedule NetappVolume#monthly_schedule}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#weekly_schedule NetappVolume#weekly_schedule}
        '''
        if isinstance(daily_schedule, dict):
            daily_schedule = NetappVolumeSnapshotPolicyDailySchedule(**daily_schedule)
        if isinstance(hourly_schedule, dict):
            hourly_schedule = NetappVolumeSnapshotPolicyHourlySchedule(**hourly_schedule)
        if isinstance(monthly_schedule, dict):
            monthly_schedule = NetappVolumeSnapshotPolicyMonthlySchedule(**monthly_schedule)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = NetappVolumeSnapshotPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22693c5b2870f2b921721b8acf1395fc11c73ed2ed59af22bd8bbeb571f0498d)
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
    ) -> typing.Optional["NetappVolumeSnapshotPolicyDailySchedule"]:
        '''daily_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#daily_schedule NetappVolume#daily_schedule}
        '''
        result = self._values.get("daily_schedule")
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicyDailySchedule"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables automated snapshot creation according to defined schedule.

        Default is false.
        To disable automatic snapshot creation you have to remove the whole snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#enabled NetappVolume#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hourly_schedule(
        self,
    ) -> typing.Optional["NetappVolumeSnapshotPolicyHourlySchedule"]:
        '''hourly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hourly_schedule NetappVolume#hourly_schedule}
        '''
        result = self._values.get("hourly_schedule")
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicyHourlySchedule"], result)

    @builtins.property
    def monthly_schedule(
        self,
    ) -> typing.Optional["NetappVolumeSnapshotPolicyMonthlySchedule"]:
        '''monthly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#monthly_schedule NetappVolume#monthly_schedule}
        '''
        result = self._values.get("monthly_schedule")
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicyMonthlySchedule"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["NetappVolumeSnapshotPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#weekly_schedule NetappVolume#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeSnapshotPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyDailySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "hour": "hour",
        "minute": "minute",
    },
)
class NetappVolumeSnapshotPolicyDailySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the daily schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441a3aca9996f688cc92e41a22afad801b43d0df5eb220f885cd3e64bc8c352a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeSnapshotPolicyDailySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeSnapshotPolicyDailyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyDailyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9585ffecf83251da8a134b6696e8b8eea902083854e6164c0fd314d7bd229a00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a8ed8969aa1a40c3dc02440194b1095f050d3cf2a3e3d4af32bb7bab834581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe84479b7d750e37bb84140f16c62102115ac6b870efba60b2553954a9ed453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51d7564f2a6b13bdffcdb64308cd6911197a535fd91382dad31841b7329616d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyDailySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyDailySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeSnapshotPolicyDailySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a43905592e86ce9357de03a3b54314c915e5c5609085c898892cf44101a65f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyHourlySchedule",
    jsii_struct_bases=[],
    name_mapping={"snapshots_to_keep": "snapshotsToKeep", "minute": "minute"},
)
class NetappVolumeSnapshotPolicyHourlySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the hourly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fd70592509813918929528998f37f440cf64caab29bcff644a23ccae1b5544)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeSnapshotPolicyHourlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeSnapshotPolicyHourlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyHourlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__209d2131c5a00e88cde4af57b11abd4cd010c9f11910c766a317afabdabc4b1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd2aedd0c888d309fe12946604f0b01c73285e9e378dad2117009a040641852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cacf9e31c02afe3edcce23c7e73c8abdcfe138f1a6787a709400190e17055c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d3acf223ec3930bcbc1f18f10422285f173cffa9678a24d5f59eb15d34ce42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyMonthlySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "days_of_month": "daysOfMonth",
        "hour": "hour",
        "minute": "minute",
    },
)
class NetappVolumeSnapshotPolicyMonthlySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        days_of_month: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the monthly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param days_of_month: Set the day or days of the month to make a snapshot (1-31). Accepts a comma separated number of days. Defaults to '1'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#days_of_month NetappVolume#days_of_month}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68e6de25be66d9f49dd352ef18d0cdf1a3666345a41ed595616ac0b40f70655)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def days_of_month(self) -> typing.Optional[builtins.str]:
        '''Set the day or days of the month to make a snapshot (1-31).

        Accepts a comma separated number of days. Defaults to '1'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#days_of_month NetappVolume#days_of_month}
        '''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeSnapshotPolicyMonthlySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeSnapshotPolicyMonthlyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyMonthlyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abf3327d1e2d957dc904067f321eaeb0fba483b8147b4f61b134071b47c4590e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__136946dfe81be315c27afad69f60c3a4d908d43a4fbad603265188c9abbabe97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e48744164f070ab7e681d80a28cc2f8fc4294c7a1e2882941d38c51d749393d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b3138ba14e3a4c950a0a81a8678cb6a66fb5db963de621d10d639d9c928c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2416d45e49fd8eccb2abbb56b63f6e2b694e63c18fc6ef07344dcd2287717057)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d74ce37e6e4cc13bf0f5bc13989d2f173922aed267ec9197239e7380ef7af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeSnapshotPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5347a2840b5e1157fca9fb356ab35d9be88c3fb19e0b6df83bf9030c4c4b8779)
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
        :param snapshots_to_keep: The maximum number of snapshots to keep for the daily schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        value = NetappVolumeSnapshotPolicyDailySchedule(
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
        :param snapshots_to_keep: The maximum number of snapshots to keep for the hourly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        value = NetappVolumeSnapshotPolicyHourlySchedule(
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
        :param snapshots_to_keep: The maximum number of snapshots to keep for the monthly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param days_of_month: Set the day or days of the month to make a snapshot (1-31). Accepts a comma separated number of days. Defaults to '1'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#days_of_month NetappVolume#days_of_month}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        value = NetappVolumeSnapshotPolicyMonthlySchedule(
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
        :param snapshots_to_keep: The maximum number of snapshots to keep for the weekly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param day: Set the day or days of the week to make a snapshot. Accepts a comma separated days of the week. Defaults to 'Sunday'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#day NetappVolume#day}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        value = NetappVolumeSnapshotPolicyWeeklySchedule(
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
    def daily_schedule(self) -> NetappVolumeSnapshotPolicyDailyScheduleOutputReference:
        return typing.cast(NetappVolumeSnapshotPolicyDailyScheduleOutputReference, jsii.get(self, "dailySchedule"))

    @builtins.property
    @jsii.member(jsii_name="hourlySchedule")
    def hourly_schedule(
        self,
    ) -> NetappVolumeSnapshotPolicyHourlyScheduleOutputReference:
        return typing.cast(NetappVolumeSnapshotPolicyHourlyScheduleOutputReference, jsii.get(self, "hourlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="monthlySchedule")
    def monthly_schedule(
        self,
    ) -> NetappVolumeSnapshotPolicyMonthlyScheduleOutputReference:
        return typing.cast(NetappVolumeSnapshotPolicyMonthlyScheduleOutputReference, jsii.get(self, "monthlySchedule"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "NetappVolumeSnapshotPolicyWeeklyScheduleOutputReference":
        return typing.cast("NetappVolumeSnapshotPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="dailyScheduleInput")
    def daily_schedule_input(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyDailySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyDailySchedule], jsii.get(self, "dailyScheduleInput"))

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
    ) -> typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule], jsii.get(self, "hourlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyScheduleInput")
    def monthly_schedule_input(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule], jsii.get(self, "monthlyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["NetappVolumeSnapshotPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["NetappVolumeSnapshotPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__176c16198867917358d05381913b4c7147ed1b69764c90f54e9541d47cbfcb69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeSnapshotPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2435f2c7d92661007d14d0e0a4fdcc3a5c740afaa83fc81c49ce3c595eaf173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={
        "snapshots_to_keep": "snapshotsToKeep",
        "day": "day",
        "hour": "hour",
        "minute": "minute",
    },
)
class NetappVolumeSnapshotPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        snapshots_to_keep: jsii.Number,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[jsii.Number] = None,
        minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param snapshots_to_keep: The maximum number of snapshots to keep for the weekly schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        :param day: Set the day or days of the week to make a snapshot. Accepts a comma separated days of the week. Defaults to 'Sunday'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#day NetappVolume#day}
        :param hour: Set the hour to create the snapshot (0-23), defaults to midnight (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        :param minute: Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2931361a4dde5f9ea8d38e75d7b86891cb8c03a5b19d0d5edf483a40455b37b0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#snapshots_to_keep NetappVolume#snapshots_to_keep}
        '''
        result = self._values.get("snapshots_to_keep")
        assert result is not None, "Required property 'snapshots_to_keep' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''Set the day or days of the week to make a snapshot.

        Accepts a comma separated days of the week. Defaults to 'Sunday'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#day NetappVolume#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[jsii.Number]:
        '''Set the hour to create the snapshot (0-23), defaults to midnight (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#hour NetappVolume#hour}
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minute(self) -> typing.Optional[jsii.Number]:
        '''Set the minute of the hour to create the snapshot (0-59), defaults to the top of the hour (0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#minute NetappVolume#minute}
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeSnapshotPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeSnapshotPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeSnapshotPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__320725f7ae2fc5f3a8a406b54940c3e65ccf13f350c25c203f6183dfbaba04c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec8a866d59e73ae16ff082473bf3fceb5635d005070a0f0fdafd355f7c89b51b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hour")
    def hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hour"))

    @hour.setter
    def hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5594120f4f2554f104ea0a5e8034c091dce0eb549adfbf828b679ac835512b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minute")
    def minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minute"))

    @minute.setter
    def minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7195742da77b7fe41b79428ffb15642ba3800ff368c7d8134bca0abf62a692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotsToKeep")
    def snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snapshotsToKeep"))

    @snapshots_to_keep.setter
    def snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b9b1cf7c1b7a5211105a60a24c61202b89a194e6f6ae1f4a952c4739e7745a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeSnapshotPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[NetappVolumeSnapshotPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeSnapshotPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f556203dd0de6208931a598e5a3df74e20b624fabc1549286408784d4fecd05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeTieringPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "cooling_threshold_days": "coolingThresholdDays",
        "tier_action": "tierAction",
    },
)
class NetappVolumeTieringPolicy:
    def __init__(
        self,
        *,
        cooling_threshold_days: typing.Optional[jsii.Number] = None,
        tier_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cooling_threshold_days: Optional. Time in days to mark the volume's data block as cold and make it eligible for tiering, can be range from 2-183. Default is 31. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cooling_threshold_days NetappVolume#cooling_threshold_days}
        :param tier_action: Optional. Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tier_action NetappVolume#tier_action}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509c53214293776f39dd4ba23dfbb6edd4c3535d8375bd67c8632a69e812335f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#cooling_threshold_days NetappVolume#cooling_threshold_days}
        '''
        result = self._values.get("cooling_threshold_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tier_action(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Flag indicating if the volume has tiering policy enable/pause. Default is PAUSED. Default value: "PAUSED" Possible values: ["ENABLED", "PAUSED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#tier_action NetappVolume#tier_action}
        '''
        result = self._values.get("tier_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeTieringPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeTieringPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeTieringPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a83a9fdd39ae6771ddbed5fc3bbca3c48ba5d62196f6bcfcf5499f653398e06e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2af3b64f124f150bc7b59f50e9d68816f501fcf2a8ceeae238c93d249f8a813f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coolingThresholdDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tierAction")
    def tier_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tierAction"))

    @tier_action.setter
    def tier_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad0b4fc3fdc57f152afeb30a04d38675c0d11e556a09f757d8e7df0da7d26df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tierAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeTieringPolicy]:
        return typing.cast(typing.Optional[NetappVolumeTieringPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[NetappVolumeTieringPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e950830f9405ed9ecf7980ed5bd8313c62e54ee2c1be7b3e8c933edff819d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetappVolumeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#create NetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#delete NetappVolume#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#update NetappVolume#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c14f6cc296b4e9597387ed2a40bd4972ab11f5b1c6b3875c378e78501efb527)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#create NetappVolume#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#delete NetappVolume#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/netapp_volume#update NetappVolume#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.netappVolume.NetappVolumeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37fc73f65ece36e2a594e79242b362b3857bff3014bc5eb4d599bda36ac89c22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8f86c374c2a1a7fc643c7aa2bf19da0999b4c6a24bb1ead100e3abb66189e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc2902ea373d37784fb6bdeca15417eb4253a0725bcfe7649804112c1e7c9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358bbc2670f1cd840d4caa3e2e23674d20753f907f5749a042cd7040656aa5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e526f90e244903670fb4eaa311ea5d28a308714ff4e2dce2994eac79794cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappVolume",
    "NetappVolumeBackupConfig",
    "NetappVolumeBackupConfigOutputReference",
    "NetappVolumeConfig",
    "NetappVolumeExportPolicy",
    "NetappVolumeExportPolicyOutputReference",
    "NetappVolumeExportPolicyRules",
    "NetappVolumeExportPolicyRulesList",
    "NetappVolumeExportPolicyRulesOutputReference",
    "NetappVolumeHybridReplicationParameters",
    "NetappVolumeHybridReplicationParametersOutputReference",
    "NetappVolumeMountOptions",
    "NetappVolumeMountOptionsList",
    "NetappVolumeMountOptionsOutputReference",
    "NetappVolumeRestoreParameters",
    "NetappVolumeRestoreParametersOutputReference",
    "NetappVolumeSnapshotPolicy",
    "NetappVolumeSnapshotPolicyDailySchedule",
    "NetappVolumeSnapshotPolicyDailyScheduleOutputReference",
    "NetappVolumeSnapshotPolicyHourlySchedule",
    "NetappVolumeSnapshotPolicyHourlyScheduleOutputReference",
    "NetappVolumeSnapshotPolicyMonthlySchedule",
    "NetappVolumeSnapshotPolicyMonthlyScheduleOutputReference",
    "NetappVolumeSnapshotPolicyOutputReference",
    "NetappVolumeSnapshotPolicyWeeklySchedule",
    "NetappVolumeSnapshotPolicyWeeklyScheduleOutputReference",
    "NetappVolumeTieringPolicy",
    "NetappVolumeTieringPolicyOutputReference",
    "NetappVolumeTimeouts",
    "NetappVolumeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__756b0e0531c296683a1b515630718ef6075ccdc093df4f2b5e3e65a31d8be771(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    capacity_gib: builtins.str,
    location: builtins.str,
    name: builtins.str,
    protocols: typing.Sequence[builtins.str],
    share_name: builtins.str,
    storage_pool: builtins.str,
    backup_config: typing.Optional[typing.Union[NetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    export_policy: typing.Optional[typing.Union[NetappVolumeExportPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_replication_parameters: typing.Optional[typing.Union[NetappVolumeHybridReplicationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    restore_parameters: typing.Optional[typing.Union[NetappVolumeRestoreParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snapshot_policy: typing.Optional[typing.Union[NetappVolumeSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[NetappVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3368ebe2e6920e8c2d609e7f5147fafc5ca391cfc982906b6ec966adc4b499ae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c2b78394d72bc9540ab85f3ba8e846fb1783db0b4e073bf76885dc01f1f2d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49593e3fc444d52ad5c0028ce8dde7c0399c9a76d0425c01dc1d5e5fe6e4704(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbebcb80fe350c829d3506f8a42a1fb1d00d72b4191ef3bc010d79ace32cf2e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91f9c897a8b7c353e89f6548a4a593d12a528f9714c020405392299d4aa4b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791797807756eb681ee483d1f53b3d8f5f586b79cc425639c2ea5f6bf3f57512(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be259c99b8c21a3e24f43d8020919bb290217e55926f961788d0ddafeb4d3e0c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528fe80be900909771c427866707634044d0bd73631d9c934398c983910acc05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5507ce041c37d67f109449a8c33896c648d63f7b8599bddec2549865987aa035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b090dfb02047f0c43ae3b39297ca0305c005719dd7db115b48d81f9d32cca1b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095de2e9ea5e6188c05dd57e05687eeee8bae4a7557acd51345610e81b35de3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54477555475da74738a410b06e6a79e099eaff9e56cf15e1284637e1c577b2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f40217352c4224b2387a4aed75ec209b88a309900adf15b25947c943823324(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d04df13e3f58227fda8360d6317ccd864164b5b4d6a126e05daf540bb1e0508(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d16d1f73a1258b0486827e261f581a467e6ca4afde965f076a11b149946318d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec7f635296392f90e4d8bfc099237e97671c85f3d342a1f02b0503395d58cbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9e270034d0660e5beaa24ce94e89653c9bf22deca17ed8de745884366e3b75(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab8faf8b3ae08491f9486c120a81020bfd37d52ee5c0945bba38326a0235078(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9964dba1b3e73be05e75e7a74c2437af4fde5b8ae9dad48eb3fb1d2aa894d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457b991fc823149f77d4c6decbb2239a5ced5b22e3354fb1110ae0da5deb6e52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821ac5814a922a46b6d368158d449c5781ce67ae288ed0156fc0f80bebcbb2aa(
    *,
    backup_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    backup_vault: typing.Optional[builtins.str] = None,
    scheduled_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36cd85f4c184d02d7c836981b62c3849467b537c4c06e00aa709cfb1dfe6ff5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affa0fc878851c0d1a3dddf308af097548383b46e76440b30ca7f570432aa356(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae3756a786df4bf9aad4534eab3231db1a7362d4e0955d1dd5d9449b9a26774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3614eaa2739127ec4119c2073578b158134accb6bbcbc14bcf86713e55a4798e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a525a9e3c68642186578e3f2a630c6e2cf17d36aad02efb9b4d5750319488b54(
    value: typing.Optional[NetappVolumeBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad98a27455e58dfa336fd4f9f80e24e32892d5595644a44af81c9810ac4af2cf(
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
    backup_config: typing.Optional[typing.Union[NetappVolumeBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    export_policy: typing.Optional[typing.Union[NetappVolumeExportPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    hybrid_replication_parameters: typing.Optional[typing.Union[NetappVolumeHybridReplicationParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kerberos_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    large_capacity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    multiple_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    restore_parameters: typing.Optional[typing.Union[NetappVolumeRestoreParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    restricted_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    smb_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_directory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snapshot_policy: typing.Optional[typing.Union[NetappVolumeSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tiering_policy: typing.Optional[typing.Union[NetappVolumeTieringPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    unix_permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a90f90d6a1dcf18b544dba035ef668febee31b34316d57ec43fd11b327a95d(
    *,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeExportPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df67f14ae8bedbe0ae45145db4a3a41a61f37fbf96536153805404d39c6b9011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fc347e449150a35830d1d7773494383975bb86e9389c3985354faac956234c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeExportPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143c08148da09b616b83f498cc3b0b6825df4ca6613d4773ef4b6a118991efae(
    value: typing.Optional[NetappVolumeExportPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99bf72bf1e8172cb9eeabe38e4be2a396d9555134a81b25d995862a62b67d66(
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

def _typecheckingstub__9a96de88b4e1c795e5dae4dd239669b3bc506738076d4a31f1e66f94c6a68226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1599b8c7e08127ed57befb15a9eedca985ea88059de9c9a2a1ea38eb1886d4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2929469446c8d6b5afedae3bc04cd466cb6a920be64ba0da06b7d04c2fe979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e248f0b1d01f7ec23989a2253ec804ea082d4481481a7f11d7fd2325b13f9c9d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0f187cc75ab65ef42cb36207252b3b93cc16c1b5811de0bfd50d2e11c9c690(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242422ef16556c1c50284face054670c2eb66951acac79a8db539c20e412cf23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f252439190fe25679dfee6f85495600f092051ab8c155eee2287db83443bcd9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8524a3f4d138676288378527a496dbed7749065a4e86fcae36e72ae67ee4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b666b8f97502df43cd0d1f0f6ceedd7ed6898a78b3187d1472e4977291001ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3afc66b87207a8f96ca5db6c9fea7db874b18773c729ce199f1acb67d17b189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c5539f8c17ff379e138cfdd96530d839f462ee5dd0fffc8bc5cc430f090db8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8305515f63f61ca64be49741610eee5f5ff4a6f82d8db030510ff9e0c7184889(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fe95db5a564205e459ec264731035984973885f33b85aa3c636b3c087a94b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9379db7a9973bd6555591b8ed469f3f9f8a6387b277276cf72930b6505ae70d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7378a1a742cffb560755ca5e109532210c49f1f6b4a28a5000d4ed111a22cd50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23be5d5111396d13ba140fb64e3d971729fb97e0dae0f1b334d27103241c1f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24275cd337e67bb13c700d614eebca86ec2495b37af184be7cb41b7178033b87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc96ce83673cf4f93478e3f78bfaf01196c638d726f1a2b9fe4dae4aeb3baa1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488231851f702c806e040b55217664a29dfefa464a50eb53beb3790b63bc6fa3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeExportPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20681fc7aa5103bc85b61d250ac9e34cc01799a568085b0e4dc64b12a30b25db(
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

def _typecheckingstub__c70921ef447ebc606b8260ba562e33efd4c7353766f02670278c0cbce07fcf24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e72a65fec7f910fbb85a183cc1a6dd2c953f3a01e0c8403bbdda7d35fd0632b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3709a64fc5705ba454568ddbd86a4fbca213abcf961aa2f9cbcd6491fa53c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b8e6a0dbe12fccad54b642ac3f248df89bfc5426ee7eee91fbc94c02afdaf2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864ea075683fdbdadd6174730d753e0038c819c3442568b2affb9248068bdec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea46649dd074344e88821c837e3c7294e2834483fb5691b581d423c9779338a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4db3e28eac933b61283943baa4aaff6a0eace3e45be9342ac97ed68f48f0b3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18483e4d12ccc0d632ec46ac18e964a4ab8864c17f04565fca3c496d598dcf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856811874888454a1d0e0386761ecdfd0be6d84b5174c5405239640dc7a698d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4452a8d2f0f643b89aa92c6f1e4c55b50b2234bdc6f0a56897af5356cf40b9f7(
    value: typing.Optional[NetappVolumeHybridReplicationParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89202a878d01b259006a10ec8326c9f3d6c978164eea0629fc38b84993c304a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de8e0187d9eb890b101de78cc6ee4dca301449b7274cea5ba56ab3666b4d0ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a0216d3c15e39b163a1284794ebfcde3bd3b5ea94616546743aa6ef3fc4689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b9605a866d500913510ce60ef441ffe5817d5bfe22e78ab41d28a89129e521(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905a6bacc2a00bc6adcd9aeb9da19904080e51f9a799a58e93ca9576d7bcb583(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e67dd3b1fa8006816c258649f30f6cc72daaff55c3b6c3f065ec662d2d4d31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3cde023d481c3b14ab10282a548ed434b8e8b9978b821f6afab0b0e2a69108a(
    value: typing.Optional[NetappVolumeMountOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4c82883f88ec04ab7dcbf1a0f0e0f56cdbd116d885aa3ebe10641743dd7173(
    *,
    source_backup: typing.Optional[builtins.str] = None,
    source_snapshot: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539bcb433add9ffb54cb971e4cbd87e1bb91faca915d3e1d18acaa588093bd8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f087cbbaffd830f93909c3e8339abb832e8cba6c555b35590bfb2ea3c61a660(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7faf9ebe256eae4b6b7d890ef1026e68a988e00602682b2f10fb0bfb8ea405ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680d3801714509aef9991884d6a039b7cc491a5c52819d43cbcc78c1c4088e68(
    value: typing.Optional[NetappVolumeRestoreParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22693c5b2870f2b921721b8acf1395fc11c73ed2ed59af22bd8bbeb571f0498d(
    *,
    daily_schedule: typing.Optional[typing.Union[NetappVolumeSnapshotPolicyDailySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hourly_schedule: typing.Optional[typing.Union[NetappVolumeSnapshotPolicyHourlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    monthly_schedule: typing.Optional[typing.Union[NetappVolumeSnapshotPolicyMonthlySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[NetappVolumeSnapshotPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441a3aca9996f688cc92e41a22afad801b43d0df5eb220f885cd3e64bc8c352a(
    *,
    snapshots_to_keep: jsii.Number,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9585ffecf83251da8a134b6696e8b8eea902083854e6164c0fd314d7bd229a00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a8ed8969aa1a40c3dc02440194b1095f050d3cf2a3e3d4af32bb7bab834581(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe84479b7d750e37bb84140f16c62102115ac6b870efba60b2553954a9ed453(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51d7564f2a6b13bdffcdb64308cd6911197a535fd91382dad31841b7329616d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a43905592e86ce9357de03a3b54314c915e5c5609085c898892cf44101a65f5(
    value: typing.Optional[NetappVolumeSnapshotPolicyDailySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fd70592509813918929528998f37f440cf64caab29bcff644a23ccae1b5544(
    *,
    snapshots_to_keep: jsii.Number,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209d2131c5a00e88cde4af57b11abd4cd010c9f11910c766a317afabdabc4b1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd2aedd0c888d309fe12946604f0b01c73285e9e378dad2117009a040641852(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cacf9e31c02afe3edcce23c7e73c8abdcfe138f1a6787a709400190e17055c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d3acf223ec3930bcbc1f18f10422285f173cffa9678a24d5f59eb15d34ce42(
    value: typing.Optional[NetappVolumeSnapshotPolicyHourlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68e6de25be66d9f49dd352ef18d0cdf1a3666345a41ed595616ac0b40f70655(
    *,
    snapshots_to_keep: jsii.Number,
    days_of_month: typing.Optional[builtins.str] = None,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf3327d1e2d957dc904067f321eaeb0fba483b8147b4f61b134071b47c4590e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136946dfe81be315c27afad69f60c3a4d908d43a4fbad603265188c9abbabe97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e48744164f070ab7e681d80a28cc2f8fc4294c7a1e2882941d38c51d749393d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b3138ba14e3a4c950a0a81a8678cb6a66fb5db963de621d10d639d9c928c09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2416d45e49fd8eccb2abbb56b63f6e2b694e63c18fc6ef07344dcd2287717057(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d74ce37e6e4cc13bf0f5bc13989d2f173922aed267ec9197239e7380ef7af1(
    value: typing.Optional[NetappVolumeSnapshotPolicyMonthlySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5347a2840b5e1157fca9fb356ab35d9be88c3fb19e0b6df83bf9030c4c4b8779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176c16198867917358d05381913b4c7147ed1b69764c90f54e9541d47cbfcb69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2435f2c7d92661007d14d0e0a4fdcc3a5c740afaa83fc81c49ce3c595eaf173(
    value: typing.Optional[NetappVolumeSnapshotPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2931361a4dde5f9ea8d38e75d7b86891cb8c03a5b19d0d5edf483a40455b37b0(
    *,
    snapshots_to_keep: jsii.Number,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[jsii.Number] = None,
    minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320725f7ae2fc5f3a8a406b54940c3e65ccf13f350c25c203f6183dfbaba04c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8a866d59e73ae16ff082473bf3fceb5635d005070a0f0fdafd355f7c89b51b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5594120f4f2554f104ea0a5e8034c091dce0eb549adfbf828b679ac835512b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7195742da77b7fe41b79428ffb15642ba3800ff368c7d8134bca0abf62a692(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b9b1cf7c1b7a5211105a60a24c61202b89a194e6f6ae1f4a952c4739e7745a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f556203dd0de6208931a598e5a3df74e20b624fabc1549286408784d4fecd05b(
    value: typing.Optional[NetappVolumeSnapshotPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509c53214293776f39dd4ba23dfbb6edd4c3535d8375bd67c8632a69e812335f(
    *,
    cooling_threshold_days: typing.Optional[jsii.Number] = None,
    tier_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83a9fdd39ae6771ddbed5fc3bbca3c48ba5d62196f6bcfcf5499f653398e06e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af3b64f124f150bc7b59f50e9d68816f501fcf2a8ceeae238c93d249f8a813f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad0b4fc3fdc57f152afeb30a04d38675c0d11e556a09f757d8e7df0da7d26df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e950830f9405ed9ecf7980ed5bd8313c62e54ee2c1be7b3e8c933edff819d63(
    value: typing.Optional[NetappVolumeTieringPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c14f6cc296b4e9597387ed2a40bd4972ab11f5b1c6b3875c378e78501efb527(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fc73f65ece36e2a594e79242b362b3857bff3014bc5eb4d599bda36ac89c22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f86c374c2a1a7fc643c7aa2bf19da0999b4c6a24bb1ead100e3abb66189e00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc2902ea373d37784fb6bdeca15417eb4253a0725bcfe7649804112c1e7c9a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358bbc2670f1cd840d4caa3e2e23674d20753f907f5749a042cd7040656aa5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e526f90e244903670fb4eaa311ea5d28a308714ff4e2dce2994eac79794cfc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

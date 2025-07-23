r'''
# `google_alloydb_cluster`

Refer to the Terraform Registry for docs: [`google_alloydb_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster).
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


class AlloydbCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster google_alloydb_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_backup_policy: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        continuous_backup_config: typing.Optional[typing.Union["AlloydbClusterContinuousBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_version: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_user: typing.Optional[typing.Union["AlloydbClusterInitialUser", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_update_policy: typing.Optional[typing.Union["AlloydbClusterMaintenanceUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["AlloydbClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["AlloydbClusterPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_source: typing.Optional[typing.Union["AlloydbClusterRestoreBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_continuous_backup_source: typing.Optional[typing.Union["AlloydbClusterRestoreContinuousBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_config: typing.Optional[typing.Union["AlloydbClusterSecondaryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AlloydbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster google_alloydb_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The ID of the alloydb cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_id AlloydbCluster#cluster_id}
        :param location: The location where the alloydb cluster should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. https://google.aip.dev/128 An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#annotations AlloydbCluster#annotations}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#automated_backup_policy AlloydbCluster#automated_backup_policy}
        :param cluster_type: The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_type AlloydbCluster#cluster_type}
        :param continuous_backup_config: continuous_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#continuous_backup_config AlloydbCluster#continuous_backup_config}
        :param database_version: The database engine major version. This is an optional field and it's populated at the Cluster creation time. Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#database_version AlloydbCluster#database_version}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster. Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#deletion_policy AlloydbCluster#deletion_policy}
        :param display_name: User-settable and human-readable display name for the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#display_name AlloydbCluster#display_name}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param etag: For Resource freshness validation (https://google.aip.dev/154). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#etag AlloydbCluster#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#id AlloydbCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#initial_user AlloydbCluster#initial_user}
        :param labels: User-defined labels for the alloydb cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        :param maintenance_update_policy: maintenance_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_update_policy AlloydbCluster#maintenance_update_policy}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network_config AlloydbCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#project AlloydbCluster#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_config AlloydbCluster#psc_config}
        :param restore_backup_source: restore_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_backup_source AlloydbCluster#restore_backup_source}
        :param restore_continuous_backup_source: restore_continuous_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_continuous_backup_source AlloydbCluster#restore_continuous_backup_source}
        :param secondary_config: secondary_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#secondary_config AlloydbCluster#secondary_config}
        :param skip_await_major_version_upgrade: Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#skip_await_major_version_upgrade AlloydbCluster#skip_await_major_version_upgrade}
        :param subscription_type: The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#subscription_type AlloydbCluster#subscription_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#timeouts AlloydbCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d145ca28e4602c05b7b94ee3bbf3ecd8ecffc6d9aae4eba52f13fd625a2efad7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AlloydbClusterConfig(
            cluster_id=cluster_id,
            location=location,
            annotations=annotations,
            automated_backup_policy=automated_backup_policy,
            cluster_type=cluster_type,
            continuous_backup_config=continuous_backup_config,
            database_version=database_version,
            deletion_policy=deletion_policy,
            display_name=display_name,
            encryption_config=encryption_config,
            etag=etag,
            id=id,
            initial_user=initial_user,
            labels=labels,
            maintenance_update_policy=maintenance_update_policy,
            network_config=network_config,
            project=project,
            psc_config=psc_config,
            restore_backup_source=restore_backup_source,
            restore_continuous_backup_source=restore_continuous_backup_source,
            secondary_config=secondary_config,
            skip_await_major_version_upgrade=skip_await_major_version_upgrade,
            subscription_type=subscription_type,
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
        '''Generates CDKTF code for importing a AlloydbCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AlloydbCluster to import.
        :param import_from_id: The id of the existing AlloydbCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AlloydbCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a213532fd321009927e8a57f3c4ab6c8e12b9ffeccb7d8d823a0a61292c97c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomatedBackupPolicy")
    def put_automated_backup_policy(
        self,
        *,
        backup_window: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        quantity_based_retention: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_retention: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backup_window: The length of the time window during which a backup can be taken. If a backup does not succeed within this time window, it will be canceled and considered failed. The backup window must be at least 5 minutes long. There is no upper bound on the window. If not set, it will default to 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_window AlloydbCluster#backup_window}
        :param enabled: Whether automated backups are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param labels: Labels to apply to backups created using this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        :param location: The location where the backup will be stored. Currently, the only supported option is to store the backup in the same region as the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        :param quantity_based_retention: quantity_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#quantity_based_retention AlloydbCluster#quantity_based_retention}
        :param time_based_retention: time_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#time_based_retention AlloydbCluster#time_based_retention}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#weekly_schedule AlloydbCluster#weekly_schedule}
        '''
        value = AlloydbClusterAutomatedBackupPolicy(
            backup_window=backup_window,
            enabled=enabled,
            encryption_config=encryption_config,
            labels=labels,
            location=location,
            quantity_based_retention=quantity_based_retention,
            time_based_retention=time_based_retention,
            weekly_schedule=weekly_schedule,
        )

        return typing.cast(None, jsii.invoke(self, "putAutomatedBackupPolicy", [value]))

    @jsii.member(jsii_name="putContinuousBackupConfig")
    def put_continuous_backup_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterContinuousBackupConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Whether continuous backup recovery is enabled. If not set, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param recovery_window_days: The numbers of days that are eligible to restore from using PITR. To support the entire recovery window, backups and logs are retained for one day more than the recovery window. If not set, defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#recovery_window_days AlloydbCluster#recovery_window_days}
        '''
        value = AlloydbClusterContinuousBackupConfig(
            enabled=enabled,
            encryption_config=encryption_config,
            recovery_window_days=recovery_window_days,
        )

        return typing.cast(None, jsii.invoke(self, "putContinuousBackupConfig", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        value = AlloydbClusterEncryptionConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putInitialUser")
    def put_initial_user(
        self,
        *,
        password: builtins.str,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#password AlloydbCluster#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#user AlloydbCluster#user}
        '''
        value = AlloydbClusterInitialUser(password=password, user=user)

        return typing.cast(None, jsii.invoke(self, "putInitialUser", [value]))

    @jsii.member(jsii_name="putMaintenanceUpdatePolicy")
    def put_maintenance_update_policy(
        self,
        *,
        maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param maintenance_windows: maintenance_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_windows AlloydbCluster#maintenance_windows}
        '''
        value = AlloydbClusterMaintenanceUpdatePolicy(
            maintenance_windows=maintenance_windows
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceUpdatePolicy", [value]))

    @jsii.member(jsii_name="putNetworkConfig")
    def put_network_config(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated IP range for the private IP AlloyDB cluster. For example: "google-managed-services-default". If set, the instance IPs for this cluster will be created in the allocated range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#allocated_ip_range AlloydbCluster#allocated_ip_range}
        :param network: The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network AlloydbCluster#network}
        '''
        value = AlloydbClusterNetworkConfig(
            allocated_ip_range=allocated_ip_range, network=network
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkConfig", [value]))

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        *,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param psc_enabled: Create an instance that allows connections from Private Service Connect endpoints to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_enabled AlloydbCluster#psc_enabled}
        '''
        value = AlloydbClusterPscConfig(psc_enabled=psc_enabled)

        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="putRestoreBackupSource")
    def put_restore_backup_source(self, *, backup_name: builtins.str) -> None:
        '''
        :param backup_name: The name of the backup that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_name AlloydbCluster#backup_name}
        '''
        value = AlloydbClusterRestoreBackupSource(backup_name=backup_name)

        return typing.cast(None, jsii.invoke(self, "putRestoreBackupSource", [value]))

    @jsii.member(jsii_name="putRestoreContinuousBackupSource")
    def put_restore_continuous_backup_source(
        self,
        *,
        cluster: builtins.str,
        point_in_time: builtins.str,
    ) -> None:
        '''
        :param cluster: The name of the source cluster that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster AlloydbCluster#cluster}
        :param point_in_time: The point in time that this cluster is restored to, in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#point_in_time AlloydbCluster#point_in_time}
        '''
        value = AlloydbClusterRestoreContinuousBackupSource(
            cluster=cluster, point_in_time=point_in_time
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreContinuousBackupSource", [value]))

    @jsii.member(jsii_name="putSecondaryConfig")
    def put_secondary_config(self, *, primary_cluster_name: builtins.str) -> None:
        '''
        :param primary_cluster_name: Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#primary_cluster_name AlloydbCluster#primary_cluster_name}
        '''
        value = AlloydbClusterSecondaryConfig(
            primary_cluster_name=primary_cluster_name
        )

        return typing.cast(None, jsii.invoke(self, "putSecondaryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#create AlloydbCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#delete AlloydbCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#update AlloydbCluster#update}.
        '''
        value = AlloydbClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAutomatedBackupPolicy")
    def reset_automated_backup_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatedBackupPolicy", []))

    @jsii.member(jsii_name="resetClusterType")
    def reset_cluster_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterType", []))

    @jsii.member(jsii_name="resetContinuousBackupConfig")
    def reset_continuous_backup_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuousBackupConfig", []))

    @jsii.member(jsii_name="resetDatabaseVersion")
    def reset_database_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseVersion", []))

    @jsii.member(jsii_name="resetDeletionPolicy")
    def reset_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionPolicy", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialUser")
    def reset_initial_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialUser", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaintenanceUpdatePolicy")
    def reset_maintenance_update_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceUpdatePolicy", []))

    @jsii.member(jsii_name="resetNetworkConfig")
    def reset_network_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscConfig")
    def reset_psc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfig", []))

    @jsii.member(jsii_name="resetRestoreBackupSource")
    def reset_restore_backup_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreBackupSource", []))

    @jsii.member(jsii_name="resetRestoreContinuousBackupSource")
    def reset_restore_continuous_backup_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreContinuousBackupSource", []))

    @jsii.member(jsii_name="resetSecondaryConfig")
    def reset_secondary_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryConfig", []))

    @jsii.member(jsii_name="resetSkipAwaitMajorVersionUpgrade")
    def reset_skip_await_major_version_upgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipAwaitMajorVersionUpgrade", []))

    @jsii.member(jsii_name="resetSubscriptionType")
    def reset_subscription_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionType", []))

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
    @jsii.member(jsii_name="automatedBackupPolicy")
    def automated_backup_policy(
        self,
    ) -> "AlloydbClusterAutomatedBackupPolicyOutputReference":
        return typing.cast("AlloydbClusterAutomatedBackupPolicyOutputReference", jsii.get(self, "automatedBackupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="backupSource")
    def backup_source(self) -> "AlloydbClusterBackupSourceList":
        return typing.cast("AlloydbClusterBackupSourceList", jsii.get(self, "backupSource"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupConfig")
    def continuous_backup_config(
        self,
    ) -> "AlloydbClusterContinuousBackupConfigOutputReference":
        return typing.cast("AlloydbClusterContinuousBackupConfigOutputReference", jsii.get(self, "continuousBackupConfig"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupInfo")
    def continuous_backup_info(self) -> "AlloydbClusterContinuousBackupInfoList":
        return typing.cast("AlloydbClusterContinuousBackupInfoList", jsii.get(self, "continuousBackupInfo"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> "AlloydbClusterEncryptionConfigOutputReference":
        return typing.cast("AlloydbClusterEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInfo")
    def encryption_info(self) -> "AlloydbClusterEncryptionInfoList":
        return typing.cast("AlloydbClusterEncryptionInfoList", jsii.get(self, "encryptionInfo"))

    @builtins.property
    @jsii.member(jsii_name="initialUser")
    def initial_user(self) -> "AlloydbClusterInitialUserOutputReference":
        return typing.cast("AlloydbClusterInitialUserOutputReference", jsii.get(self, "initialUser"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceUpdatePolicy")
    def maintenance_update_policy(
        self,
    ) -> "AlloydbClusterMaintenanceUpdatePolicyOutputReference":
        return typing.cast("AlloydbClusterMaintenanceUpdatePolicyOutputReference", jsii.get(self, "maintenanceUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="migrationSource")
    def migration_source(self) -> "AlloydbClusterMigrationSourceList":
        return typing.cast("AlloydbClusterMigrationSourceList", jsii.get(self, "migrationSource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "AlloydbClusterNetworkConfigOutputReference":
        return typing.cast("AlloydbClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "AlloydbClusterPscConfigOutputReference":
        return typing.cast("AlloydbClusterPscConfigOutputReference", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupSource")
    def restore_backup_source(
        self,
    ) -> "AlloydbClusterRestoreBackupSourceOutputReference":
        return typing.cast("AlloydbClusterRestoreBackupSourceOutputReference", jsii.get(self, "restoreBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="restoreContinuousBackupSource")
    def restore_continuous_backup_source(
        self,
    ) -> "AlloydbClusterRestoreContinuousBackupSourceOutputReference":
        return typing.cast("AlloydbClusterRestoreContinuousBackupSourceOutputReference", jsii.get(self, "restoreContinuousBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConfig")
    def secondary_config(self) -> "AlloydbClusterSecondaryConfigOutputReference":
        return typing.cast("AlloydbClusterSecondaryConfigOutputReference", jsii.get(self, "secondaryConfig"))

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
    def timeouts(self) -> "AlloydbClusterTimeoutsOutputReference":
        return typing.cast("AlloydbClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialMetadata")
    def trial_metadata(self) -> "AlloydbClusterTrialMetadataList":
        return typing.cast("AlloydbClusterTrialMetadataList", jsii.get(self, "trialMetadata"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="automatedBackupPolicyInput")
    def automated_backup_policy_input(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicy"]:
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicy"], jsii.get(self, "automatedBackupPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterTypeInput")
    def cluster_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupConfigInput")
    def continuous_backup_config_input(
        self,
    ) -> typing.Optional["AlloydbClusterContinuousBackupConfig"]:
        return typing.cast(typing.Optional["AlloydbClusterContinuousBackupConfig"], jsii.get(self, "continuousBackupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseVersionInput")
    def database_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionPolicyInput")
    def deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["AlloydbClusterEncryptionConfig"]:
        return typing.cast(typing.Optional["AlloydbClusterEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialUserInput")
    def initial_user_input(self) -> typing.Optional["AlloydbClusterInitialUser"]:
        return typing.cast(typing.Optional["AlloydbClusterInitialUser"], jsii.get(self, "initialUserInput"))

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
    @jsii.member(jsii_name="maintenanceUpdatePolicyInput")
    def maintenance_update_policy_input(
        self,
    ) -> typing.Optional["AlloydbClusterMaintenanceUpdatePolicy"]:
        return typing.cast(typing.Optional["AlloydbClusterMaintenanceUpdatePolicy"], jsii.get(self, "maintenanceUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(self) -> typing.Optional["AlloydbClusterNetworkConfig"]:
        return typing.cast(typing.Optional["AlloydbClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(self) -> typing.Optional["AlloydbClusterPscConfig"]:
        return typing.cast(typing.Optional["AlloydbClusterPscConfig"], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupSourceInput")
    def restore_backup_source_input(
        self,
    ) -> typing.Optional["AlloydbClusterRestoreBackupSource"]:
        return typing.cast(typing.Optional["AlloydbClusterRestoreBackupSource"], jsii.get(self, "restoreBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreContinuousBackupSourceInput")
    def restore_continuous_backup_source_input(
        self,
    ) -> typing.Optional["AlloydbClusterRestoreContinuousBackupSource"]:
        return typing.cast(typing.Optional["AlloydbClusterRestoreContinuousBackupSource"], jsii.get(self, "restoreContinuousBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConfigInput")
    def secondary_config_input(
        self,
    ) -> typing.Optional["AlloydbClusterSecondaryConfig"]:
        return typing.cast(typing.Optional["AlloydbClusterSecondaryConfig"], jsii.get(self, "secondaryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="skipAwaitMajorVersionUpgradeInput")
    def skip_await_major_version_upgrade_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipAwaitMajorVersionUpgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionTypeInput")
    def subscription_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764339c270a6d47ab279d3e7ee12ea2821dc9bfd943b8a949c763d989cf19b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439efe1918252e0930377473c490244a7bafc7f661839176f3b105309b85b724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterType"))

    @cluster_type.setter
    def cluster_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb40fd830a8c5ca98f001ab33c164db77dbaf40727a335b4ad9495695cf0c629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55994ee9e27a4f4cd9dff8c04c97cf95cfc6c2681801617b1424d416a7175d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd20e322b01001de4bf7af3972dca9afdf9e7b1613371c497b09fec70847b070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91eb688ee973671a5f322f343aabbbaae331ad0a743128b7412ec0754434166f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0a16615c8ce95ddcebcc27f02450072fda4b108c45b4a9f54ec41878593645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d0d2472e0ea8c4c5bfc2b104fcdfd33305e7a88f07fe1b9c08f8895879257b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b6325ae7d968c5440f869796b5bc1ffea2195fed816555a7715b3d7bae2ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede20721aa9c497a84fa4f3f6f74027a2ad03093572ef2adbd55d8046b303fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cc1d8e3a8ec2044cf8fb528dda20df90c3a29dca267528935326aa5f4dee9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipAwaitMajorVersionUpgrade")
    def skip_await_major_version_upgrade(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipAwaitMajorVersionUpgrade"))

    @skip_await_major_version_upgrade.setter
    def skip_await_major_version_upgrade(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47a197b99427e61bb497c716ab9113bc69c2f34ad08a79a307e59b100f17eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipAwaitMajorVersionUpgrade", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @subscription_type.setter
    def subscription_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8036ea2c3165867e2dc8394735019729c939208c0f75fb811da94b98ac7d8a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup_window": "backupWindow",
        "enabled": "enabled",
        "encryption_config": "encryptionConfig",
        "labels": "labels",
        "location": "location",
        "quantity_based_retention": "quantityBasedRetention",
        "time_based_retention": "timeBasedRetention",
        "weekly_schedule": "weeklySchedule",
    },
)
class AlloydbClusterAutomatedBackupPolicy:
    def __init__(
        self,
        *,
        backup_window: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        quantity_based_retention: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_retention: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["AlloydbClusterAutomatedBackupPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backup_window: The length of the time window during which a backup can be taken. If a backup does not succeed within this time window, it will be canceled and considered failed. The backup window must be at least 5 minutes long. There is no upper bound on the window. If not set, it will default to 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_window AlloydbCluster#backup_window}
        :param enabled: Whether automated backups are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param labels: Labels to apply to backups created using this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        :param location: The location where the backup will be stored. Currently, the only supported option is to store the backup in the same region as the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        :param quantity_based_retention: quantity_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#quantity_based_retention AlloydbCluster#quantity_based_retention}
        :param time_based_retention: time_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#time_based_retention AlloydbCluster#time_based_retention}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#weekly_schedule AlloydbCluster#weekly_schedule}
        '''
        if isinstance(encryption_config, dict):
            encryption_config = AlloydbClusterAutomatedBackupPolicyEncryptionConfig(**encryption_config)
        if isinstance(quantity_based_retention, dict):
            quantity_based_retention = AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(**quantity_based_retention)
        if isinstance(time_based_retention, dict):
            time_based_retention = AlloydbClusterAutomatedBackupPolicyTimeBasedRetention(**time_based_retention)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = AlloydbClusterAutomatedBackupPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7667d55dddaf43965b794275881487762a9612abcfeaeac2f33620c2be7fe6f9)
            check_type(argname="argument backup_window", value=backup_window, expected_type=type_hints["backup_window"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument quantity_based_retention", value=quantity_based_retention, expected_type=type_hints["quantity_based_retention"])
            check_type(argname="argument time_based_retention", value=time_based_retention, expected_type=type_hints["time_based_retention"])
            check_type(argname="argument weekly_schedule", value=weekly_schedule, expected_type=type_hints["weekly_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_window is not None:
            self._values["backup_window"] = backup_window
        if enabled is not None:
            self._values["enabled"] = enabled
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if quantity_based_retention is not None:
            self._values["quantity_based_retention"] = quantity_based_retention
        if time_based_retention is not None:
            self._values["time_based_retention"] = time_based_retention
        if weekly_schedule is not None:
            self._values["weekly_schedule"] = weekly_schedule

    @builtins.property
    def backup_window(self) -> typing.Optional[builtins.str]:
        '''The length of the time window during which a backup can be taken.

        If a backup does not succeed within this time window, it will be canceled and considered failed.

        The backup window must be at least 5 minutes long. There is no upper bound on the window. If not set, it will default to 1 hour.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_window AlloydbCluster#backup_window}
        '''
        result = self._values.get("backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether automated backups are enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyEncryptionConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to backups created using this configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the backup will be stored.

        Currently, the only supported option is to store the backup in the same region as the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quantity_based_retention(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"]:
        '''quantity_based_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#quantity_based_retention AlloydbCluster#quantity_based_retention}
        '''
        result = self._values.get("quantity_based_retention")
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"], result)

    @builtins.property
    def time_based_retention(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention"]:
        '''time_based_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#time_based_retention AlloydbCluster#time_based_retention}
        '''
        result = self._values.get("time_based_retention")
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#weekly_schedule AlloydbCluster#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class AlloydbClusterAutomatedBackupPolicyEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fcfd20c029cac6700068a9c70e1e442b2f73d2b5ce90bd45b7c156aea98ff2)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicyEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cec7f1c3c476e582723b04f397c046c8df92c510f4da0de714b2dcb8dce966b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcd9a7df97cc2ca33c0e1f6b95ffb0f3b10c6612a3958a3b5f171a55ddb9081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca13ba6041d4585cb04340d3e3042e4a16c83289ba6436f1ca9b2a38b637db72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterAutomatedBackupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec1dfb052e437db2d88f61b989fa3ff01db75a2a5eab5c280e9d408714d787cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        value = AlloydbClusterAutomatedBackupPolicyEncryptionConfig(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putQuantityBasedRetention")
    def put_quantity_based_retention(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: The number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#count AlloydbCluster#count}
        '''
        value = AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(count=count)

        return typing.cast(None, jsii.invoke(self, "putQuantityBasedRetention", [value]))

    @jsii.member(jsii_name="putTimeBasedRetention")
    def put_time_based_retention(
        self,
        *,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_period: The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#retention_period AlloydbCluster#retention_period}
        '''
        value = AlloydbClusterAutomatedBackupPolicyTimeBasedRetention(
            retention_period=retention_period
        )

        return typing.cast(None, jsii.invoke(self, "putTimeBasedRetention", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param start_times: start_times block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#start_times AlloydbCluster#start_times}
        :param days_of_week: The days of the week to perform a backup. At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#days_of_week AlloydbCluster#days_of_week}
        '''
        value = AlloydbClusterAutomatedBackupPolicyWeeklySchedule(
            start_times=start_times, days_of_week=days_of_week
        )

        return typing.cast(None, jsii.invoke(self, "putWeeklySchedule", [value]))

    @jsii.member(jsii_name="resetBackupWindow")
    def reset_backup_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupWindow", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetQuantityBasedRetention")
    def reset_quantity_based_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuantityBasedRetention", []))

    @jsii.member(jsii_name="resetTimeBasedRetention")
    def reset_time_based_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeBasedRetention", []))

    @jsii.member(jsii_name="resetWeeklySchedule")
    def reset_weekly_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklySchedule", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> AlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference:
        return typing.cast(AlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="quantityBasedRetention")
    def quantity_based_retention(
        self,
    ) -> "AlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference":
        return typing.cast("AlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference", jsii.get(self, "quantityBasedRetention"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedRetention")
    def time_based_retention(
        self,
    ) -> "AlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference":
        return typing.cast("AlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference", jsii.get(self, "timeBasedRetention"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference":
        return typing.cast("AlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

    @builtins.property
    @jsii.member(jsii_name="backupWindowInput")
    def backup_window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

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
    @jsii.member(jsii_name="quantityBasedRetentionInput")
    def quantity_based_retention_input(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"]:
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"], jsii.get(self, "quantityBasedRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedRetentionInput")
    def time_based_retention_input(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention"]:
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyTimeBasedRetention"], jsii.get(self, "timeBasedRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["AlloydbClusterAutomatedBackupPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["AlloydbClusterAutomatedBackupPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="backupWindow")
    def backup_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupWindow"))

    @backup_window.setter
    def backup_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d227da1713b5c0b627ee3e3120d43cdc927bba3f1b8e37be8e4e428a7b0651ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupWindow", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1b965e76c3a769d016a387d7d5b87272bef0fd3dfecd34cd3187ff16361e3ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87827fa43ac42f9893f656ce95c52f0f5059c75f7a86c4c0c0be778bc625311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d66b591c5d85071d69770a773facce191a504a3da05c319160f9652eb83774b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterAutomatedBackupPolicy]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterAutomatedBackupPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08666d92482962b80bf789d5f9bf7c271e3398d2eba04701672df04910cfa9a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention:
    def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: The number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#count AlloydbCluster#count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b09b39fa36aecda67246d75136f98ffff1096efb6b605dad52e528439a67d1)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of backups to retain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#count AlloydbCluster#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c81c54d2cb4cd453dd8abe2374619c68ac8f2be7c565071b96cc2ec6c3e4b46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0680fc7213dfb4c17fdc236b744475c31bc79daf886e659a46f2205689ca65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c06f30fdc5f78db7952082465b3732ef59d9b29bf6d83bce8e68c62e13ea8df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyTimeBasedRetention",
    jsii_struct_bases=[],
    name_mapping={"retention_period": "retentionPeriod"},
)
class AlloydbClusterAutomatedBackupPolicyTimeBasedRetention:
    def __init__(
        self,
        *,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_period: The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#retention_period AlloydbCluster#retention_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf30a2c2f1d7b484622d5145d784361aec1f3ea28b4c4ec1c87418ae10c8740)
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_period is not None:
            self._values["retention_period"] = retention_period

    @builtins.property
    def retention_period(self) -> typing.Optional[builtins.str]:
        '''The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#retention_period AlloydbCluster#retention_period}
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicyTimeBasedRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__659ed70e9b532f869cad26aaa40f3dd53738221fa45671976501be1aa6eed0ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionPeriod")
    def reset_retention_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriod", []))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInput")
    def retention_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873581c22841677761f38d2fad59fa141c0ff8a5da64d4aacf6f641f1de2307c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicyTimeBasedRetention]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicyTimeBasedRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterAutomatedBackupPolicyTimeBasedRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e8f7e652ece4bbf9f707b3de17a342020e9ae7d118667d4671f7db284d410e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_times": "startTimes", "days_of_week": "daysOfWeek"},
)
class AlloydbClusterAutomatedBackupPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param start_times: start_times block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#start_times AlloydbCluster#start_times}
        :param days_of_week: The days of the week to perform a backup. At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#days_of_week AlloydbCluster#days_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee78e2df00350e7e6e90bb7a4773021475d543f68867dbb848e0dfe81df68210)
            check_type(argname="argument start_times", value=start_times, expected_type=type_hints["start_times"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_times": start_times,
        }
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week

    @builtins.property
    def start_times(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]:
        '''start_times block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#start_times AlloydbCluster#start_times}
        '''
        result = self._values.get("start_times")
        assert result is not None, "Required property 'start_times' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The days of the week to perform a backup.

        At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#days_of_week AlloydbCluster#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6280858fbed5023c75146265ea52f55aedd6271bb164371edec46410bcb5002b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTimes")
    def put_start_times(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc646f38113434dd09b231a222ec67961ba61b17d934cded87cf9b9f5a56315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartTimes", [value]))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @builtins.property
    @jsii.member(jsii_name="startTimes")
    def start_times(
        self,
    ) -> "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList":
        return typing.cast("AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList", jsii.get(self, "startTimes"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimesInput")
    def start_times_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]], jsii.get(self, "startTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6642dff0be68e4a8a8c95e03821a226e8aba4d9a6b5e9a8bfb5af99d845fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterAutomatedBackupPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7dd8a788205e84a2e11651e7ee3663cfefabcd1baebc537249dfd0f9857d5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#hours AlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#minutes AlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#nanos AlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#seconds AlloydbCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82137497c53951546c9a793a05844239bb2353e00075367a828517da6d6c4347)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format.

        Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#hours AlloydbCluster#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#minutes AlloydbCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#nanos AlloydbCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#seconds AlloydbCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__024e2ebb92f61a5bd1c53fa7247b38604c9b95e116139f455822453ee1533185)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166dd79b7c1280c387d5a0abfea57616505859773e3058d5ad31a596ebf9cf0a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b44c86c8468c0cb16c3a9b79f0d3e98024e585dc2145e84a4b9bed4c3d3cc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0c89de0c1add25e14e876136a05cf504b6b942639f8af2944c189d01d0a07d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__311206cbbdf7a3133326be5975e695ffae2ce4011951bfbacce0d001248571c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5606a4176768c6e9363234830df9f2bffd97cb9f33f0324c9f694f573ebc7d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f210df30afca1865d8516c176d9a160384b0d50600dab5eb6de8de1f07c44692)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97a0ad7dcd7240b4566f2235fc2db09a9fe66355bd1fc9ac2953eeb9b241f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fba27cb379580ca29525ca7a9812ac8a40c5ce1242862f479c260db8ad9fa82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60320c0d889af67cc54ba4fc947685928bc2941415d7d4c0f9f47f1a7f70702c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d538dc2cacb089fe1a6942c3dc746af90b065d592dba5da851e58b00e76512c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044beedfd479ac8a8378077516ec862feb82855fa39f20e28a6e59ed0844949c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterBackupSource",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterBackupSource:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterBackupSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterBackupSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab9c83a779b110bd9f09bb385c455030699d1e1839096df3521314e8c954ccc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AlloydbClusterBackupSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de056f3b57ddbe37cecdaf03cd72bbd2a2d97e32c9af44ef8748f67a859e7353)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterBackupSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3540ad810e5ebdcfb52c184ee130ccbf35a3c2b8e836362e19fdb1992addaccf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__759117fe7418d7c4d54f3e6f2a9d7e80434fa24af89c3cacf89d86d179317b7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de5c13b481226335764a4b91584145b2914f8e9233b4dc7e1d5edd0ecc0c6cf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c78b915db88fc2cc2c9fd64d1432af48ccbc3612956e049dec6c5facd6d23ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="backupName")
    def backup_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterBackupSource]:
        return typing.cast(typing.Optional[AlloydbClusterBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c6335aa1028ed1423e3ab3daf0c267d41041849c74c1deea8130efc86a7d49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "location": "location",
        "annotations": "annotations",
        "automated_backup_policy": "automatedBackupPolicy",
        "cluster_type": "clusterType",
        "continuous_backup_config": "continuousBackupConfig",
        "database_version": "databaseVersion",
        "deletion_policy": "deletionPolicy",
        "display_name": "displayName",
        "encryption_config": "encryptionConfig",
        "etag": "etag",
        "id": "id",
        "initial_user": "initialUser",
        "labels": "labels",
        "maintenance_update_policy": "maintenanceUpdatePolicy",
        "network_config": "networkConfig",
        "project": "project",
        "psc_config": "pscConfig",
        "restore_backup_source": "restoreBackupSource",
        "restore_continuous_backup_source": "restoreContinuousBackupSource",
        "secondary_config": "secondaryConfig",
        "skip_await_major_version_upgrade": "skipAwaitMajorVersionUpgrade",
        "subscription_type": "subscriptionType",
        "timeouts": "timeouts",
    },
)
class AlloydbClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_backup_policy: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        continuous_backup_config: typing.Optional[typing.Union["AlloydbClusterContinuousBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_version: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_user: typing.Optional[typing.Union["AlloydbClusterInitialUser", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_update_policy: typing.Optional[typing.Union["AlloydbClusterMaintenanceUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["AlloydbClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["AlloydbClusterPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_source: typing.Optional[typing.Union["AlloydbClusterRestoreBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_continuous_backup_source: typing.Optional[typing.Union["AlloydbClusterRestoreContinuousBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_config: typing.Optional[typing.Union["AlloydbClusterSecondaryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["AlloydbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The ID of the alloydb cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_id AlloydbCluster#cluster_id}
        :param location: The location where the alloydb cluster should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. https://google.aip.dev/128 An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#annotations AlloydbCluster#annotations}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#automated_backup_policy AlloydbCluster#automated_backup_policy}
        :param cluster_type: The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_type AlloydbCluster#cluster_type}
        :param continuous_backup_config: continuous_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#continuous_backup_config AlloydbCluster#continuous_backup_config}
        :param database_version: The database engine major version. This is an optional field and it's populated at the Cluster creation time. Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#database_version AlloydbCluster#database_version}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster. Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#deletion_policy AlloydbCluster#deletion_policy}
        :param display_name: User-settable and human-readable display name for the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#display_name AlloydbCluster#display_name}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param etag: For Resource freshness validation (https://google.aip.dev/154). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#etag AlloydbCluster#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#id AlloydbCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#initial_user AlloydbCluster#initial_user}
        :param labels: User-defined labels for the alloydb cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        :param maintenance_update_policy: maintenance_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_update_policy AlloydbCluster#maintenance_update_policy}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network_config AlloydbCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#project AlloydbCluster#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_config AlloydbCluster#psc_config}
        :param restore_backup_source: restore_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_backup_source AlloydbCluster#restore_backup_source}
        :param restore_continuous_backup_source: restore_continuous_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_continuous_backup_source AlloydbCluster#restore_continuous_backup_source}
        :param secondary_config: secondary_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#secondary_config AlloydbCluster#secondary_config}
        :param skip_await_major_version_upgrade: Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#skip_await_major_version_upgrade AlloydbCluster#skip_await_major_version_upgrade}
        :param subscription_type: The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#subscription_type AlloydbCluster#subscription_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#timeouts AlloydbCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_policy, dict):
            automated_backup_policy = AlloydbClusterAutomatedBackupPolicy(**automated_backup_policy)
        if isinstance(continuous_backup_config, dict):
            continuous_backup_config = AlloydbClusterContinuousBackupConfig(**continuous_backup_config)
        if isinstance(encryption_config, dict):
            encryption_config = AlloydbClusterEncryptionConfig(**encryption_config)
        if isinstance(initial_user, dict):
            initial_user = AlloydbClusterInitialUser(**initial_user)
        if isinstance(maintenance_update_policy, dict):
            maintenance_update_policy = AlloydbClusterMaintenanceUpdatePolicy(**maintenance_update_policy)
        if isinstance(network_config, dict):
            network_config = AlloydbClusterNetworkConfig(**network_config)
        if isinstance(psc_config, dict):
            psc_config = AlloydbClusterPscConfig(**psc_config)
        if isinstance(restore_backup_source, dict):
            restore_backup_source = AlloydbClusterRestoreBackupSource(**restore_backup_source)
        if isinstance(restore_continuous_backup_source, dict):
            restore_continuous_backup_source = AlloydbClusterRestoreContinuousBackupSource(**restore_continuous_backup_source)
        if isinstance(secondary_config, dict):
            secondary_config = AlloydbClusterSecondaryConfig(**secondary_config)
        if isinstance(timeouts, dict):
            timeouts = AlloydbClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666c73a341b657e5f004cbdeb09551a4ae1e3473bde2f39518cae28c1f795ad5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument automated_backup_policy", value=automated_backup_policy, expected_type=type_hints["automated_backup_policy"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument continuous_backup_config", value=continuous_backup_config, expected_type=type_hints["continuous_backup_config"])
            check_type(argname="argument database_version", value=database_version, expected_type=type_hints["database_version"])
            check_type(argname="argument deletion_policy", value=deletion_policy, expected_type=type_hints["deletion_policy"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_user", value=initial_user, expected_type=type_hints["initial_user"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument maintenance_update_policy", value=maintenance_update_policy, expected_type=type_hints["maintenance_update_policy"])
            check_type(argname="argument network_config", value=network_config, expected_type=type_hints["network_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_config", value=psc_config, expected_type=type_hints["psc_config"])
            check_type(argname="argument restore_backup_source", value=restore_backup_source, expected_type=type_hints["restore_backup_source"])
            check_type(argname="argument restore_continuous_backup_source", value=restore_continuous_backup_source, expected_type=type_hints["restore_continuous_backup_source"])
            check_type(argname="argument secondary_config", value=secondary_config, expected_type=type_hints["secondary_config"])
            check_type(argname="argument skip_await_major_version_upgrade", value=skip_await_major_version_upgrade, expected_type=type_hints["skip_await_major_version_upgrade"])
            check_type(argname="argument subscription_type", value=subscription_type, expected_type=type_hints["subscription_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "location": location,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if automated_backup_policy is not None:
            self._values["automated_backup_policy"] = automated_backup_policy
        if cluster_type is not None:
            self._values["cluster_type"] = cluster_type
        if continuous_backup_config is not None:
            self._values["continuous_backup_config"] = continuous_backup_config
        if database_version is not None:
            self._values["database_version"] = database_version
        if deletion_policy is not None:
            self._values["deletion_policy"] = deletion_policy
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if etag is not None:
            self._values["etag"] = etag
        if id is not None:
            self._values["id"] = id
        if initial_user is not None:
            self._values["initial_user"] = initial_user
        if labels is not None:
            self._values["labels"] = labels
        if maintenance_update_policy is not None:
            self._values["maintenance_update_policy"] = maintenance_update_policy
        if network_config is not None:
            self._values["network_config"] = network_config
        if project is not None:
            self._values["project"] = project
        if psc_config is not None:
            self._values["psc_config"] = psc_config
        if restore_backup_source is not None:
            self._values["restore_backup_source"] = restore_backup_source
        if restore_continuous_backup_source is not None:
            self._values["restore_continuous_backup_source"] = restore_continuous_backup_source
        if secondary_config is not None:
            self._values["secondary_config"] = secondary_config
        if skip_await_major_version_upgrade is not None:
            self._values["skip_await_major_version_upgrade"] = skip_await_major_version_upgrade
        if subscription_type is not None:
            self._values["subscription_type"] = subscription_type
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
    def cluster_id(self) -> builtins.str:
        '''The ID of the alloydb cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_id AlloydbCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location where the alloydb cluster should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#location AlloydbCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations to allow client tools to store small amount of arbitrary data.

        This is distinct from labels. https://google.aip.dev/128
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#annotations AlloydbCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def automated_backup_policy(
        self,
    ) -> typing.Optional[AlloydbClusterAutomatedBackupPolicy]:
        '''automated_backup_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#automated_backup_policy AlloydbCluster#automated_backup_policy}
        '''
        result = self._values.get("automated_backup_policy")
        return typing.cast(typing.Optional[AlloydbClusterAutomatedBackupPolicy], result)

    @builtins.property
    def cluster_type(self) -> typing.Optional[builtins.str]:
        '''The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster_type AlloydbCluster#cluster_type}
        '''
        result = self._values.get("cluster_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continuous_backup_config(
        self,
    ) -> typing.Optional["AlloydbClusterContinuousBackupConfig"]:
        '''continuous_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#continuous_backup_config AlloydbCluster#continuous_backup_config}
        '''
        result = self._values.get("continuous_backup_config")
        return typing.cast(typing.Optional["AlloydbClusterContinuousBackupConfig"], result)

    @builtins.property
    def database_version(self) -> typing.Optional[builtins.str]:
        '''The database engine major version.

        This is an optional field and it's populated at the Cluster creation time.
        Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#database_version AlloydbCluster#database_version}
        '''
        result = self._values.get("database_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine if the cluster should be deleted forcefully.

        Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster.
        Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance.
        Possible values: DEFAULT, FORCE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#deletion_policy AlloydbCluster#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-settable and human-readable display name for the Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#display_name AlloydbCluster#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_config(self) -> typing.Optional["AlloydbClusterEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["AlloydbClusterEncryptionConfig"], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''For Resource freshness validation (https://google.aip.dev/154).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#etag AlloydbCluster#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#id AlloydbCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_user(self) -> typing.Optional["AlloydbClusterInitialUser"]:
        '''initial_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#initial_user AlloydbCluster#initial_user}
        '''
        result = self._values.get("initial_user")
        return typing.cast(typing.Optional["AlloydbClusterInitialUser"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the alloydb cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#labels AlloydbCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_update_policy(
        self,
    ) -> typing.Optional["AlloydbClusterMaintenanceUpdatePolicy"]:
        '''maintenance_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_update_policy AlloydbCluster#maintenance_update_policy}
        '''
        result = self._values.get("maintenance_update_policy")
        return typing.cast(typing.Optional["AlloydbClusterMaintenanceUpdatePolicy"], result)

    @builtins.property
    def network_config(self) -> typing.Optional["AlloydbClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network_config AlloydbCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["AlloydbClusterNetworkConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#project AlloydbCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(self) -> typing.Optional["AlloydbClusterPscConfig"]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_config AlloydbCluster#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional["AlloydbClusterPscConfig"], result)

    @builtins.property
    def restore_backup_source(
        self,
    ) -> typing.Optional["AlloydbClusterRestoreBackupSource"]:
        '''restore_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_backup_source AlloydbCluster#restore_backup_source}
        '''
        result = self._values.get("restore_backup_source")
        return typing.cast(typing.Optional["AlloydbClusterRestoreBackupSource"], result)

    @builtins.property
    def restore_continuous_backup_source(
        self,
    ) -> typing.Optional["AlloydbClusterRestoreContinuousBackupSource"]:
        '''restore_continuous_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#restore_continuous_backup_source AlloydbCluster#restore_continuous_backup_source}
        '''
        result = self._values.get("restore_continuous_backup_source")
        return typing.cast(typing.Optional["AlloydbClusterRestoreContinuousBackupSource"], result)

    @builtins.property
    def secondary_config(self) -> typing.Optional["AlloydbClusterSecondaryConfig"]:
        '''secondary_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#secondary_config AlloydbCluster#secondary_config}
        '''
        result = self._values.get("secondary_config")
        return typing.cast(typing.Optional["AlloydbClusterSecondaryConfig"], result)

    @builtins.property
    def skip_await_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#skip_await_major_version_upgrade AlloydbCluster#skip_await_major_version_upgrade}
        '''
        result = self._values.get("skip_await_major_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subscription_type(self) -> typing.Optional[builtins.str]:
        '''The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#subscription_type AlloydbCluster#subscription_type}
        '''
        result = self._values.get("subscription_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AlloydbClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#timeouts AlloydbCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AlloydbClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "encryption_config": "encryptionConfig",
        "recovery_window_days": "recoveryWindowDays",
    },
)
class AlloydbClusterContinuousBackupConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["AlloydbClusterContinuousBackupConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Whether continuous backup recovery is enabled. If not set, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        :param recovery_window_days: The numbers of days that are eligible to restore from using PITR. To support the entire recovery window, backups and logs are retained for one day more than the recovery window. If not set, defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#recovery_window_days AlloydbCluster#recovery_window_days}
        '''
        if isinstance(encryption_config, dict):
            encryption_config = AlloydbClusterContinuousBackupConfigEncryptionConfig(**encryption_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d67cb425e1eb15233d354e31695fd91f28b3afc4c8fdaca0aff7ee91884f34)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument recovery_window_days", value=recovery_window_days, expected_type=type_hints["recovery_window_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if recovery_window_days is not None:
            self._values["recovery_window_days"] = recovery_window_days

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether continuous backup recovery is enabled. If not set, defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#enabled AlloydbCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["AlloydbClusterContinuousBackupConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#encryption_config AlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["AlloydbClusterContinuousBackupConfigEncryptionConfig"], result)

    @builtins.property
    def recovery_window_days(self) -> typing.Optional[jsii.Number]:
        '''The numbers of days that are eligible to restore from using PITR.

        To support the entire recovery window, backups and logs are retained for one day more than the recovery window.

        If not set, defaults to 14 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#recovery_window_days AlloydbCluster#recovery_window_days}
        '''
        result = self._values.get("recovery_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterContinuousBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class AlloydbClusterContinuousBackupConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a2bb7e0a1b2f5c63dcd8c44a660444932b7e68b1eb3b2ee1248598ee787e94)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterContinuousBackupConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22b05594a70a6ce863ec4fda37b0ebed26410d569cb8014b211192ea37432a4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6349eba6fbbbd2079e96fecf914d10d7460cc255831db3c99e034fa1d8e023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig]:
        return typing.cast(typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354779bd862cf13d6dbd0903dc25e640a3163c7132f47487aa8581f2f2c35d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterContinuousBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__065459385cac1db81843c3a23a1b9da5351ab29f796e42b2c8a1fa264cf27c32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        value = AlloydbClusterContinuousBackupConfigEncryptionConfig(
            kms_key_name=kms_key_name
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetRecoveryWindowDays")
    def reset_recovery_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryWindowDays", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> AlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference:
        return typing.cast(AlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig]:
        return typing.cast(typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryWindowDaysInput")
    def recovery_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recoveryWindowDaysInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__542095a70d0657d15b48274796bab627843b1124659bd43814eea170906d2c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryWindowDays")
    def recovery_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recoveryWindowDays"))

    @recovery_window_days.setter
    def recovery_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34513f51f79dbcef2d66413ed581dd5e9ab71699f5e56969bce215cbb452f1c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterContinuousBackupConfig]:
        return typing.cast(typing.Optional[AlloydbClusterContinuousBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterContinuousBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e9dd2e56e5749bf6df1b1ed771c10ba054335bab971d0dd99a571609bea337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterContinuousBackupInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterContinuousBackupInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfoEncryptionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterContinuousBackupInfoEncryptionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterContinuousBackupInfoEncryptionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterContinuousBackupInfoEncryptionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfoEncryptionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee417cc3bfb029915fb26a6e6bfd8aa9f5fc9253c0ca45b07587bb69bcffe98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619092dfe2e9ab13e267239fa3acfd27c4059981fc87d2e576ec485edcdabb91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1330810c60589c67b2891de610b41f86ddd136be9c3d44970c56da7c33c7bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13f5677713e987c5efc2106542f788017ed322298576f62a876976a3583e0bbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e4486035f6f83541cafe8c92a61259b1743c6f6963c027c6777c677b6102ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da13db777b84047ac9b7bfa910e3b2fbbe77aae839fb019c853a4ec98d09c1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyVersions")
    def kms_key_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kmsKeyVersions"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterContinuousBackupInfoEncryptionInfo]:
        return typing.cast(typing.Optional[AlloydbClusterContinuousBackupInfoEncryptionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterContinuousBackupInfoEncryptionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2e97ea2e548143346d7f9d03d763dcc53d2d947ceb45567622c28c7f169d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterContinuousBackupInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__452437e96133b533b0985e0dfda1e9534e0aedc4bf86309adeada94e2bc0ba0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbClusterContinuousBackupInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47a75231a87d3e7043df05eac41a52b59a81c45947dc28bdbce82feb7d5c95e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterContinuousBackupInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ea2001774a3bffdc6b66284b63c898f70e893f436d97dc28bcbe6d37989c5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5c5e179e38e4e67030f70c0d05e29568ace6378df0f5e81a92ccfe3f5994eff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1556119fa8f8028055a8717457a2e1cdf415040ff18f88b1a16caff99679ce28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterContinuousBackupInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterContinuousBackupInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa85cd5d836b47bdf3aed802faafc86389a0daa46c389d0b6f4125d47b9678b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="earliestRestorableTime")
    def earliest_restorable_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "earliestRestorableTime"))

    @builtins.property
    @jsii.member(jsii_name="enabledTime")
    def enabled_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabledTime"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInfo")
    def encryption_info(self) -> AlloydbClusterContinuousBackupInfoEncryptionInfoList:
        return typing.cast(AlloydbClusterContinuousBackupInfoEncryptionInfoList, jsii.get(self, "encryptionInfo"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterContinuousBackupInfo]:
        return typing.cast(typing.Optional[AlloydbClusterContinuousBackupInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterContinuousBackupInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e189b52581f640ba29690488ce91aad998a6325853c7d962c84211be1dec115e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class AlloydbClusterEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3ccfa1442b2632eb99e1db4fd59372981fa277f6d3fb72229f954c6f939552)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#kms_key_name AlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da9ced5b4c3b58bbbd55914ee9e8939f089ba6c916ae42b918542a73400d5d9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054f8740270a343baeddf9bb9d0423f21f9b53a269b4fdd461bd152791b0f227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterEncryptionConfig]:
        return typing.cast(typing.Optional[AlloydbClusterEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43a557e3b1ec2f145ca24d1618f05c82f9fcb843fc18b27196b4f68162cf6a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterEncryptionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterEncryptionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterEncryptionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterEncryptionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterEncryptionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25294c1876a80d954d526bfd107c96b62bcfaeda53031bf838bbefea716da86d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AlloydbClusterEncryptionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9ab58cd3139dc14384f42ccea7dafd96638d59ecc40f88e3c2ae7b399d681a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterEncryptionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845b7bb96cb9330ae262e7cc6eb6984588fe06f621f676b96fb10e063e46d9cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be1b96ce79b8a21f85c027a188624ae309043d0e4599a80ff5441068dace7a20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e73a966de9c797d7b7322339fc400838567503f64f97898aded66350a0c3603b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterEncryptionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterEncryptionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e9090179bb0042ca12b107ba8b0a20a6536c05b6b13f60f3bf1407337ddd12c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="encryptionType")
    def encryption_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionType"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyVersions")
    def kms_key_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kmsKeyVersions"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterEncryptionInfo]:
        return typing.cast(typing.Optional[AlloydbClusterEncryptionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterEncryptionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad775aa10da784e87900921e2ea0e10b648691e478ad8b5367fcaa73498ae9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterInitialUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "user": "user"},
)
class AlloydbClusterInitialUser:
    def __init__(
        self,
        *,
        password: builtins.str,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#password AlloydbCluster#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#user AlloydbCluster#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a51c4fc1a050e2b748a9815f82c3c35e1c91f8b602742bcf9a9023d484730)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
        }
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def password(self) -> builtins.str:
        '''The initial password for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#password AlloydbCluster#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The database username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#user AlloydbCluster#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterInitialUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterInitialUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterInitialUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac62ceac622eacb103f51a56962d4d949fb67bcfd76e0ab83efa394e855995d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2055a30f05781fc5eade3c3aea3db114f94e528b26755c203d1b2641b2eeab93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b281cdae937277dc800b6a1d9db625180c6c7fa44be33e48bc6ca87bacfaa95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterInitialUser]:
        return typing.cast(typing.Optional[AlloydbClusterInitialUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AlloydbClusterInitialUser]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663be403a5bd5390cc9689ede0b47a9d5e941e60f5b51d11007c35f68c36bb40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={"maintenance_windows": "maintenanceWindows"},
)
class AlloydbClusterMaintenanceUpdatePolicy:
    def __init__(
        self,
        *,
        maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param maintenance_windows: maintenance_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_windows AlloydbCluster#maintenance_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96703074d858116b41d0052e3e5b9bca0af90990aba7d02893d8657a67e5753)
            check_type(argname="argument maintenance_windows", value=maintenance_windows, expected_type=type_hints["maintenance_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maintenance_windows is not None:
            self._values["maintenance_windows"] = maintenance_windows

    @builtins.property
    def maintenance_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows"]]]:
        '''maintenance_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#maintenance_windows AlloydbCluster#maintenance_windows}
        '''
        result = self._values.get("maintenance_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterMaintenanceUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Preferred day of the week for maintenance, e.g. MONDAY, TUESDAY, etc. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#day AlloydbCluster#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#start_time AlloydbCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a18a2255f876c20a31f7a56cc85cf81775c116dac3ac6bd7931794a42d85e4)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Preferred day of the week for maintenance, e.g. MONDAY, TUESDAY, etc. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#day AlloydbCluster#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#start_time AlloydbCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4ff549ab0ca4dd32ff80eabfcb36b410a5ef51831556fdbb424b8f631cff38a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc5cd27cae54c8b9d8a75e28ed976a85bb3b29817447dd997d3feece312d313)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a02f39771681630c681065e8812409b2b3da999da6ffc9de002326c14fd080a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a59a067fbf9d1f9b3f50b896222d0e513e5c3aba1f3a4b63d21ae50ae45f31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1668638897687cefcbb9ab519b0220152a601ecdbee23897ee9e6df56f222765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90635ba8d02caa033bf1080f47c2d3bc23f501a3cdb2b55c26d719e5a41774d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ed5b5d16391b353a74028fa075f9197a88fd361523c2ff737f5c1ed54bbd5e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: jsii.Number,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#hours AlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#minutes AlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#nanos AlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#seconds AlloydbCluster#seconds}
        '''
        value = AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference":
        return typing.cast("AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime"]:
        return typing.cast(typing.Optional["AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c9ccb8c1a7c0c47248a3ba9d16bae6a0a4cebcdf3e5e24c51b2bc848514b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef0520c8fbca7e368bee85458d155abcf13e084f22c52d4bd6036d0f7813619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime:
    def __init__(
        self,
        *,
        hours: jsii.Number,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#hours AlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#minutes AlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#nanos AlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#seconds AlloydbCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e864c04cb1d697bf9ac265d2144b6401bdf8a6a2f8cef1464d7f8ef31e81f232)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hours": hours,
        }
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> jsii.Number:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#hours AlloydbCluster#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#minutes AlloydbCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#nanos AlloydbCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#seconds AlloydbCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61a9aa27fbfa1be1995b5b75c14db542674572a64a9523868075bfd68a69f2a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c8951d17133a59dc25ea3a78111257cbe1d356cb96c3e9f89701734b32f7a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686b53c85db054de6c4b7ff02f9a75a8d197b0405df2c0ea2f5eacfb8a9dcdf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3b8a9dd7c593d66974e737aae51d8d211f32ad5b9980170dcd53b732defe70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960d36c7715ed176df87f57f602538871559d6b3200a9bfe440a79008820ad92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime]:
        return typing.cast(typing.Optional[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d2de15a6a55ebe874d0f9f903f15771b90a609217f5019d460db1c5a66a7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterMaintenanceUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMaintenanceUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a55bb159bdbc1564b426b4e56c1b64a771d7ece1eee61b00ed4df5cf66bdee1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaintenanceWindows")
    def put_maintenance_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485edfaa9930ad7349242b9a807a4eaba70425c1bfe01692153605dce7afbe6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindows", [value]))

    @jsii.member(jsii_name="resetMaintenanceWindows")
    def reset_maintenance_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindows", []))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindows")
    def maintenance_windows(
        self,
    ) -> AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList:
        return typing.cast(AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList, jsii.get(self, "maintenanceWindows"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowsInput")
    def maintenance_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]], jsii.get(self, "maintenanceWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterMaintenanceUpdatePolicy]:
        return typing.cast(typing.Optional[AlloydbClusterMaintenanceUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterMaintenanceUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf74a1b8bf49a93f4689544e0ac747002506b7c089aeb6d813a42ac7dbf05ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMigrationSource",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterMigrationSource:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterMigrationSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterMigrationSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMigrationSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74fa799828cd744746ca2eecefb2d3f63fcfdf173bb6c4bf285265fa0ea3516f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AlloydbClusterMigrationSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6b525e616d3c00fc22f43edf6d5f300b8cffcee50ab782bb1cae39135c11f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterMigrationSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6653a85dbf86d61498c26ae7ef8bd1590a867869649f7e7ed452c83207873fb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b152a340d2cd1d1420fdd46a1316d6f00ec6ca175cce975958f55c15077a050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef6855bd6c10120999a4f3749296c6396da710198aad55db0d4b715212760f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterMigrationSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterMigrationSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc7881b29a6322b3c5a1d762cb21919408c8cc52a863eb6858bfed5a7dc16630)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hostPort")
    def host_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostPort"))

    @builtins.property
    @jsii.member(jsii_name="referenceId")
    def reference_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "referenceId"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterMigrationSource]:
        return typing.cast(typing.Optional[AlloydbClusterMigrationSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterMigrationSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6f8c4ce6d539f82b33951034a3323e35cd14fa690a99b8f9eb616c6dfcbee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"allocated_ip_range": "allocatedIpRange", "network": "network"},
)
class AlloydbClusterNetworkConfig:
    def __init__(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated IP range for the private IP AlloyDB cluster. For example: "google-managed-services-default". If set, the instance IPs for this cluster will be created in the allocated range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#allocated_ip_range AlloydbCluster#allocated_ip_range}
        :param network: The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network AlloydbCluster#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129d6f8f01d10939b34aafa3eb7051c095e5de3ff32514ca7fb96f2f5c057844)
            check_type(argname="argument allocated_ip_range", value=allocated_ip_range, expected_type=type_hints["allocated_ip_range"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_ip_range is not None:
            self._values["allocated_ip_range"] = allocated_ip_range
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def allocated_ip_range(self) -> typing.Optional[builtins.str]:
        '''The name of the allocated IP range for the private IP AlloyDB cluster.

        For example: "google-managed-services-default".
        If set, the instance IPs for this cluster will be created in the allocated range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#allocated_ip_range AlloydbCluster#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP.

        The network must belong to the same project as the cluster.
        It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#network AlloydbCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72e7432ae189154e8d6ae18223e5585467a1d5acb8756d1a1bbc1a2abeae3a5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllocatedIpRange")
    def reset_allocated_ip_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocatedIpRange", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRangeInput")
    def allocated_ip_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allocatedIpRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedIpRange")
    def allocated_ip_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allocatedIpRange"))

    @allocated_ip_range.setter
    def allocated_ip_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7392c4d254e465211c33655177d07d3f15bf0cb98a9c1566854b1995a967689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e6be651bfcb4bdb24069faba0e6079a5e4a072779ec7ef6cfc441e384c4235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterNetworkConfig]:
        return typing.cast(typing.Optional[AlloydbClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13023aaf89e534afa6eeca73275f34c03f55778e4fdd40c7361aa78ee2dfe0bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterPscConfig",
    jsii_struct_bases=[],
    name_mapping={"psc_enabled": "pscEnabled"},
)
class AlloydbClusterPscConfig:
    def __init__(
        self,
        *,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param psc_enabled: Create an instance that allows connections from Private Service Connect endpoints to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_enabled AlloydbCluster#psc_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06727f16a0420e5afea6a4909d9e343ff7867c5577bf1aaebef5d42c45a31a70)
            check_type(argname="argument psc_enabled", value=psc_enabled, expected_type=type_hints["psc_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if psc_enabled is not None:
            self._values["psc_enabled"] = psc_enabled

    @builtins.property
    def psc_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create an instance that allows connections from Private Service Connect endpoints to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#psc_enabled AlloydbCluster#psc_enabled}
        '''
        result = self._values.get("psc_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f427ea8c537f506b387f87b5a024167654345cc8609663a7b041617cf6f5e955)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPscEnabled")
    def reset_psc_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="serviceOwnedProjectNumber")
    def service_owned_project_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "serviceOwnedProjectNumber"))

    @builtins.property
    @jsii.member(jsii_name="pscEnabledInput")
    def psc_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pscEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="pscEnabled")
    def psc_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pscEnabled"))

    @psc_enabled.setter
    def psc_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e10840286e79408eef06e78b7e851ddb8ab86ab89935623842548190e57a998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterPscConfig]:
        return typing.cast(typing.Optional[AlloydbClusterPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AlloydbClusterPscConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054f590db3bc199c257f2f540928371ec42f3c4dc52a76ee5fb03274ec567777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterRestoreBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup_name": "backupName"},
)
class AlloydbClusterRestoreBackupSource:
    def __init__(self, *, backup_name: builtins.str) -> None:
        '''
        :param backup_name: The name of the backup that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_name AlloydbCluster#backup_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7181194a70f38f22a4d9aebb9a799dc69d6aa49fef78dd2ac4b2e3e434d7d32)
            check_type(argname="argument backup_name", value=backup_name, expected_type=type_hints["backup_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_name": backup_name,
        }

    @builtins.property
    def backup_name(self) -> builtins.str:
        '''The name of the backup that this cluster is restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#backup_name AlloydbCluster#backup_name}
        '''
        result = self._values.get("backup_name")
        assert result is not None, "Required property 'backup_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterRestoreBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterRestoreBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterRestoreBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5ef5c6c07eeebe74ef5154a553168f237a996553b48a93be160b01ee00f9f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="backupNameInput")
    def backup_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backupName")
    def backup_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupName"))

    @backup_name.setter
    def backup_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d266eaa0a168141da7353ccd8701c6a0013005e87e3157db787cb3554ebd62fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterRestoreBackupSource]:
        return typing.cast(typing.Optional[AlloydbClusterRestoreBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterRestoreBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ab02b39d7038c18370a3b6bd1929d90c88600627220c7c9fd271561a380eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterRestoreContinuousBackupSource",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "point_in_time": "pointInTime"},
)
class AlloydbClusterRestoreContinuousBackupSource:
    def __init__(self, *, cluster: builtins.str, point_in_time: builtins.str) -> None:
        '''
        :param cluster: The name of the source cluster that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster AlloydbCluster#cluster}
        :param point_in_time: The point in time that this cluster is restored to, in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#point_in_time AlloydbCluster#point_in_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2035d25a536417b3c925021f750c64dfe5b9a6d491dd1ed6fc28349d9b833f5f)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument point_in_time", value=point_in_time, expected_type=type_hints["point_in_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "point_in_time": point_in_time,
        }

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The name of the source cluster that this cluster is restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#cluster AlloydbCluster#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def point_in_time(self) -> builtins.str:
        '''The point in time that this cluster is restored to, in RFC 3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#point_in_time AlloydbCluster#point_in_time}
        '''
        result = self._values.get("point_in_time")
        assert result is not None, "Required property 'point_in_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterRestoreContinuousBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterRestoreContinuousBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterRestoreContinuousBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__937b1789a3c476f4c4ad0bc968afec90acb76b4bb90d6852cb0489d56ba05a35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeInput")
    def point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60269e5756c0a5bf90f2b3fb24937acfc0b342e3fac4c65a8333e38efcf1236f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTime")
    def point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTime"))

    @point_in_time.setter
    def point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51adeb3146be59aa597d449a462197fa220dc99913a8fff20fc0c72fcaa0208c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AlloydbClusterRestoreContinuousBackupSource]:
        return typing.cast(typing.Optional[AlloydbClusterRestoreContinuousBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterRestoreContinuousBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741d3c6f9bc0c4c513fb9308f0ef10ce33138566ea644ab2a10ec4766f8a01d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterSecondaryConfig",
    jsii_struct_bases=[],
    name_mapping={"primary_cluster_name": "primaryClusterName"},
)
class AlloydbClusterSecondaryConfig:
    def __init__(self, *, primary_cluster_name: builtins.str) -> None:
        '''
        :param primary_cluster_name: Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#primary_cluster_name AlloydbCluster#primary_cluster_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a5ebb291002bc79675f3eba82e4abdff3ee50d08240e99c77c5d49f4f2e9db)
            check_type(argname="argument primary_cluster_name", value=primary_cluster_name, expected_type=type_hints["primary_cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_cluster_name": primary_cluster_name,
        }

    @builtins.property
    def primary_cluster_name(self) -> builtins.str:
        '''Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#primary_cluster_name AlloydbCluster#primary_cluster_name}
        '''
        result = self._values.get("primary_cluster_name")
        assert result is not None, "Required property 'primary_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterSecondaryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterSecondaryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterSecondaryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27cd72d9f29a658a9bbdd6814310f7fef0f5d3857e76749f5d85da37ea5739a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="primaryClusterNameInput")
    def primary_cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryClusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryClusterName")
    def primary_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryClusterName"))

    @primary_cluster_name.setter
    def primary_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddd1228218218510876b3c9180522e08fb9738351a6668cbd830376c735bffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterSecondaryConfig]:
        return typing.cast(typing.Optional[AlloydbClusterSecondaryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterSecondaryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bbecd8718706de4c370959349ea589d063bba2c061ad3bb502f2317b7154de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AlloydbClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#create AlloydbCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#delete AlloydbCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#update AlloydbCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbe50cf2e4b23bbc2c62a71a05cd46d7932de15c40ed6e66b155f0a6cf9360b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#create AlloydbCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#delete AlloydbCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/alloydb_cluster#update AlloydbCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adab4e39032d83339725978bbd87b85efa81966bf28b6195df269e825019a7de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5895f7e2ff6d7c76d8e294e43b53bb5d969751b3ff5b3e90565a99abdb76337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775086be08d0e7cf19468a2f0fc4135d2678db37ac11f61e8ea0798441bd8aaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237a984252eef25d83a6a95c287501e61cf2f38fe6e103f1b229f1ca0ed953a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5958295a012d287a52b9e6bab46a472063e3e5d39b533b2e0bdabc1df51ffd5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterTrialMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlloydbClusterTrialMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbClusterTrialMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbClusterTrialMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterTrialMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f3b733ca060fac132801fd0be14bc2e53c14a7980f65899db161280c1151834)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AlloydbClusterTrialMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc9b7ed404dfb9230d2bf4b08c4c502bcdef82510b0c7ce6f36fa0e970be11e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlloydbClusterTrialMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3635ef1094c556c453144315d9fbb602c527c0cf3ab4b35b3ff0326458b6bd2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea203e61432758dc3e849be0756c8ab9497da07ac0e3ca26843b7046ca6b5ea8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9edce829eeb625b3aa44ecb848509e40295ef02c035ab635b57f04fb4be05d9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class AlloydbClusterTrialMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbCluster.AlloydbClusterTrialMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4341a577cc97224059a7c9bab114e581b85b9d8246076d9543a418733f137d5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="graceEndTime")
    def grace_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "graceEndTime"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="upgradeTime")
    def upgrade_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "upgradeTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbClusterTrialMetadata]:
        return typing.cast(typing.Optional[AlloydbClusterTrialMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbClusterTrialMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df991930effd84e2d0cf4e7c43a42bae11e6e8a5963365a63047f50a888c62f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AlloydbCluster",
    "AlloydbClusterAutomatedBackupPolicy",
    "AlloydbClusterAutomatedBackupPolicyEncryptionConfig",
    "AlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference",
    "AlloydbClusterAutomatedBackupPolicyOutputReference",
    "AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention",
    "AlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference",
    "AlloydbClusterAutomatedBackupPolicyTimeBasedRetention",
    "AlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference",
    "AlloydbClusterAutomatedBackupPolicyWeeklySchedule",
    "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference",
    "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes",
    "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList",
    "AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference",
    "AlloydbClusterBackupSource",
    "AlloydbClusterBackupSourceList",
    "AlloydbClusterBackupSourceOutputReference",
    "AlloydbClusterConfig",
    "AlloydbClusterContinuousBackupConfig",
    "AlloydbClusterContinuousBackupConfigEncryptionConfig",
    "AlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference",
    "AlloydbClusterContinuousBackupConfigOutputReference",
    "AlloydbClusterContinuousBackupInfo",
    "AlloydbClusterContinuousBackupInfoEncryptionInfo",
    "AlloydbClusterContinuousBackupInfoEncryptionInfoList",
    "AlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference",
    "AlloydbClusterContinuousBackupInfoList",
    "AlloydbClusterContinuousBackupInfoOutputReference",
    "AlloydbClusterEncryptionConfig",
    "AlloydbClusterEncryptionConfigOutputReference",
    "AlloydbClusterEncryptionInfo",
    "AlloydbClusterEncryptionInfoList",
    "AlloydbClusterEncryptionInfoOutputReference",
    "AlloydbClusterInitialUser",
    "AlloydbClusterInitialUserOutputReference",
    "AlloydbClusterMaintenanceUpdatePolicy",
    "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows",
    "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList",
    "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference",
    "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime",
    "AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference",
    "AlloydbClusterMaintenanceUpdatePolicyOutputReference",
    "AlloydbClusterMigrationSource",
    "AlloydbClusterMigrationSourceList",
    "AlloydbClusterMigrationSourceOutputReference",
    "AlloydbClusterNetworkConfig",
    "AlloydbClusterNetworkConfigOutputReference",
    "AlloydbClusterPscConfig",
    "AlloydbClusterPscConfigOutputReference",
    "AlloydbClusterRestoreBackupSource",
    "AlloydbClusterRestoreBackupSourceOutputReference",
    "AlloydbClusterRestoreContinuousBackupSource",
    "AlloydbClusterRestoreContinuousBackupSourceOutputReference",
    "AlloydbClusterSecondaryConfig",
    "AlloydbClusterSecondaryConfigOutputReference",
    "AlloydbClusterTimeouts",
    "AlloydbClusterTimeoutsOutputReference",
    "AlloydbClusterTrialMetadata",
    "AlloydbClusterTrialMetadataList",
    "AlloydbClusterTrialMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__d145ca28e4602c05b7b94ee3bbf3ecd8ecffc6d9aae4eba52f13fd625a2efad7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_backup_policy: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    continuous_backup_config: typing.Optional[typing.Union[AlloydbClusterContinuousBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_version: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[AlloydbClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_user: typing.Optional[typing.Union[AlloydbClusterInitialUser, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_update_policy: typing.Optional[typing.Union[AlloydbClusterMaintenanceUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[AlloydbClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[AlloydbClusterPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_source: typing.Optional[typing.Union[AlloydbClusterRestoreBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_continuous_backup_source: typing.Optional[typing.Union[AlloydbClusterRestoreContinuousBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_config: typing.Optional[typing.Union[AlloydbClusterSecondaryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AlloydbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d5a213532fd321009927e8a57f3c4ab6c8e12b9ffeccb7d8d823a0a61292c97c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764339c270a6d47ab279d3e7ee12ea2821dc9bfd943b8a949c763d989cf19b20(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439efe1918252e0930377473c490244a7bafc7f661839176f3b105309b85b724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb40fd830a8c5ca98f001ab33c164db77dbaf40727a335b4ad9495695cf0c629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55994ee9e27a4f4cd9dff8c04c97cf95cfc6c2681801617b1424d416a7175d32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd20e322b01001de4bf7af3972dca9afdf9e7b1613371c497b09fec70847b070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91eb688ee973671a5f322f343aabbbaae331ad0a743128b7412ec0754434166f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0a16615c8ce95ddcebcc27f02450072fda4b108c45b4a9f54ec41878593645(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d0d2472e0ea8c4c5bfc2b104fcdfd33305e7a88f07fe1b9c08f8895879257b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b6325ae7d968c5440f869796b5bc1ffea2195fed816555a7715b3d7bae2ea5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede20721aa9c497a84fa4f3f6f74027a2ad03093572ef2adbd55d8046b303fcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cc1d8e3a8ec2044cf8fb528dda20df90c3a29dca267528935326aa5f4dee9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47a197b99427e61bb497c716ab9113bc69c2f34ad08a79a307e59b100f17eb2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8036ea2c3165867e2dc8394735019729c939208c0f75fb811da94b98ac7d8a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7667d55dddaf43965b794275881487762a9612abcfeaeac2f33620c2be7fe6f9(
    *,
    backup_window: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicyEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    quantity_based_retention: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    time_based_retention: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicyTimeBasedRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fcfd20c029cac6700068a9c70e1e442b2f73d2b5ce90bd45b7c156aea98ff2(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cec7f1c3c476e582723b04f397c046c8df92c510f4da0de714b2dcb8dce966b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcd9a7df97cc2ca33c0e1f6b95ffb0f3b10c6612a3958a3b5f171a55ddb9081(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca13ba6041d4585cb04340d3e3042e4a16c83289ba6436f1ca9b2a38b637db72(
    value: typing.Optional[AlloydbClusterAutomatedBackupPolicyEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1dfb052e437db2d88f61b989fa3ff01db75a2a5eab5c280e9d408714d787cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d227da1713b5c0b627ee3e3120d43cdc927bba3f1b8e37be8e4e428a7b0651ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b965e76c3a769d016a387d7d5b87272bef0fd3dfecd34cd3187ff16361e3ea0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87827fa43ac42f9893f656ce95c52f0f5059c75f7a86c4c0c0be778bc625311(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d66b591c5d85071d69770a773facce191a504a3da05c319160f9652eb83774b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08666d92482962b80bf789d5f9bf7c271e3398d2eba04701672df04910cfa9a1(
    value: typing.Optional[AlloydbClusterAutomatedBackupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b09b39fa36aecda67246d75136f98ffff1096efb6b605dad52e528439a67d1(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c81c54d2cb4cd453dd8abe2374619c68ac8f2be7c565071b96cc2ec6c3e4b46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0680fc7213dfb4c17fdc236b744475c31bc79daf886e659a46f2205689ca65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c06f30fdc5f78db7952082465b3732ef59d9b29bf6d83bce8e68c62e13ea8df(
    value: typing.Optional[AlloydbClusterAutomatedBackupPolicyQuantityBasedRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf30a2c2f1d7b484622d5145d784361aec1f3ea28b4c4ec1c87418ae10c8740(
    *,
    retention_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659ed70e9b532f869cad26aaa40f3dd53738221fa45671976501be1aa6eed0ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873581c22841677761f38d2fad59fa141c0ff8a5da64d4aacf6f641f1de2307c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e8f7e652ece4bbf9f707b3de17a342020e9ae7d118667d4671f7db284d410e(
    value: typing.Optional[AlloydbClusterAutomatedBackupPolicyTimeBasedRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee78e2df00350e7e6e90bb7a4773021475d543f68867dbb848e0dfe81df68210(
    *,
    start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes, typing.Dict[builtins.str, typing.Any]]]],
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6280858fbed5023c75146265ea52f55aedd6271bb164371edec46410bcb5002b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc646f38113434dd09b231a222ec67961ba61b17d934cded87cf9b9f5a56315(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6642dff0be68e4a8a8c95e03821a226e8aba4d9a6b5e9a8bfb5af99d845fae(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7dd8a788205e84a2e11651e7ee3663cfefabcd1baebc537249dfd0f9857d5b8(
    value: typing.Optional[AlloydbClusterAutomatedBackupPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82137497c53951546c9a793a05844239bb2353e00075367a828517da6d6c4347(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024e2ebb92f61a5bd1c53fa7247b38604c9b95e116139f455822453ee1533185(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166dd79b7c1280c387d5a0abfea57616505859773e3058d5ad31a596ebf9cf0a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b44c86c8468c0cb16c3a9b79f0d3e98024e585dc2145e84a4b9bed4c3d3cc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0c89de0c1add25e14e876136a05cf504b6b942639f8af2944c189d01d0a07d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311206cbbdf7a3133326be5975e695ffae2ce4011951bfbacce0d001248571c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5606a4176768c6e9363234830df9f2bffd97cb9f33f0324c9f694f573ebc7d81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f210df30afca1865d8516c176d9a160384b0d50600dab5eb6de8de1f07c44692(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97a0ad7dcd7240b4566f2235fc2db09a9fe66355bd1fc9ac2953eeb9b241f3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fba27cb379580ca29525ca7a9812ac8a40c5ce1242862f479c260db8ad9fa82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60320c0d889af67cc54ba4fc947685928bc2941415d7d4c0f9f47f1a7f70702c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d538dc2cacb089fe1a6942c3dc746af90b065d592dba5da851e58b00e76512c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044beedfd479ac8a8378077516ec862feb82855fa39f20e28a6e59ed0844949c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9c83a779b110bd9f09bb385c455030699d1e1839096df3521314e8c954ccc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de056f3b57ddbe37cecdaf03cd72bbd2a2d97e32c9af44ef8748f67a859e7353(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3540ad810e5ebdcfb52c184ee130ccbf35a3c2b8e836362e19fdb1992addaccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759117fe7418d7c4d54f3e6f2a9d7e80434fa24af89c3cacf89d86d179317b7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5c13b481226335764a4b91584145b2914f8e9233b4dc7e1d5edd0ecc0c6cf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c78b915db88fc2cc2c9fd64d1432af48ccbc3612956e049dec6c5facd6d23ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c6335aa1028ed1423e3ab3daf0c267d41041849c74c1deea8130efc86a7d49(
    value: typing.Optional[AlloydbClusterBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666c73a341b657e5f004cbdeb09551a4ae1e3473bde2f39518cae28c1f795ad5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_backup_policy: typing.Optional[typing.Union[AlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    continuous_backup_config: typing.Optional[typing.Union[AlloydbClusterContinuousBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_version: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[AlloydbClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_user: typing.Optional[typing.Union[AlloydbClusterInitialUser, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_update_policy: typing.Optional[typing.Union[AlloydbClusterMaintenanceUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[AlloydbClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[AlloydbClusterPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_source: typing.Optional[typing.Union[AlloydbClusterRestoreBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_continuous_backup_source: typing.Optional[typing.Union[AlloydbClusterRestoreContinuousBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_config: typing.Optional[typing.Union[AlloydbClusterSecondaryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[AlloydbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d67cb425e1eb15233d354e31695fd91f28b3afc4c8fdaca0aff7ee91884f34(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[AlloydbClusterContinuousBackupConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_window_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a2bb7e0a1b2f5c63dcd8c44a660444932b7e68b1eb3b2ee1248598ee787e94(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b05594a70a6ce863ec4fda37b0ebed26410d569cb8014b211192ea37432a4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6349eba6fbbbd2079e96fecf914d10d7460cc255831db3c99e034fa1d8e023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354779bd862cf13d6dbd0903dc25e640a3163c7132f47487aa8581f2f2c35d1f(
    value: typing.Optional[AlloydbClusterContinuousBackupConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065459385cac1db81843c3a23a1b9da5351ab29f796e42b2c8a1fa264cf27c32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542095a70d0657d15b48274796bab627843b1124659bd43814eea170906d2c9a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34513f51f79dbcef2d66413ed581dd5e9ab71699f5e56969bce215cbb452f1c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e9dd2e56e5749bf6df1b1ed771c10ba054335bab971d0dd99a571609bea337(
    value: typing.Optional[AlloydbClusterContinuousBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee417cc3bfb029915fb26a6e6bfd8aa9f5fc9253c0ca45b07587bb69bcffe98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619092dfe2e9ab13e267239fa3acfd27c4059981fc87d2e576ec485edcdabb91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1330810c60589c67b2891de610b41f86ddd136be9c3d44970c56da7c33c7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f5677713e987c5efc2106542f788017ed322298576f62a876976a3583e0bbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e4486035f6f83541cafe8c92a61259b1743c6f6963c027c6777c677b6102ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da13db777b84047ac9b7bfa910e3b2fbbe77aae839fb019c853a4ec98d09c1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2e97ea2e548143346d7f9d03d763dcc53d2d947ceb45567622c28c7f169d84(
    value: typing.Optional[AlloydbClusterContinuousBackupInfoEncryptionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452437e96133b533b0985e0dfda1e9534e0aedc4bf86309adeada94e2bc0ba0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47a75231a87d3e7043df05eac41a52b59a81c45947dc28bdbce82feb7d5c95e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ea2001774a3bffdc6b66284b63c898f70e893f436d97dc28bcbe6d37989c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c5e179e38e4e67030f70c0d05e29568ace6378df0f5e81a92ccfe3f5994eff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1556119fa8f8028055a8717457a2e1cdf415040ff18f88b1a16caff99679ce28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa85cd5d836b47bdf3aed802faafc86389a0daa46c389d0b6f4125d47b9678b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e189b52581f640ba29690488ce91aad998a6325853c7d962c84211be1dec115e(
    value: typing.Optional[AlloydbClusterContinuousBackupInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3ccfa1442b2632eb99e1db4fd59372981fa277f6d3fb72229f954c6f939552(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9ced5b4c3b58bbbd55914ee9e8939f089ba6c916ae42b918542a73400d5d9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054f8740270a343baeddf9bb9d0423f21f9b53a269b4fdd461bd152791b0f227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43a557e3b1ec2f145ca24d1618f05c82f9fcb843fc18b27196b4f68162cf6a7(
    value: typing.Optional[AlloydbClusterEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25294c1876a80d954d526bfd107c96b62bcfaeda53031bf838bbefea716da86d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9ab58cd3139dc14384f42ccea7dafd96638d59ecc40f88e3c2ae7b399d681a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845b7bb96cb9330ae262e7cc6eb6984588fe06f621f676b96fb10e063e46d9cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1b96ce79b8a21f85c027a188624ae309043d0e4599a80ff5441068dace7a20(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73a966de9c797d7b7322339fc400838567503f64f97898aded66350a0c3603b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9090179bb0042ca12b107ba8b0a20a6536c05b6b13f60f3bf1407337ddd12c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad775aa10da784e87900921e2ea0e10b648691e478ad8b5367fcaa73498ae9f(
    value: typing.Optional[AlloydbClusterEncryptionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a51c4fc1a050e2b748a9815f82c3c35e1c91f8b602742bcf9a9023d484730(
    *,
    password: builtins.str,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac62ceac622eacb103f51a56962d4d949fb67bcfd76e0ab83efa394e855995d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2055a30f05781fc5eade3c3aea3db114f94e528b26755c203d1b2641b2eeab93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b281cdae937277dc800b6a1d9db625180c6c7fa44be33e48bc6ca87bacfaa95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663be403a5bd5390cc9689ede0b47a9d5e941e60f5b51d11007c35f68c36bb40(
    value: typing.Optional[AlloydbClusterInitialUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96703074d858116b41d0052e3e5b9bca0af90990aba7d02893d8657a67e5753(
    *,
    maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a18a2255f876c20a31f7a56cc85cf81775c116dac3ac6bd7931794a42d85e4(
    *,
    day: builtins.str,
    start_time: typing.Union[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ff549ab0ca4dd32ff80eabfcb36b410a5ef51831556fdbb424b8f631cff38a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc5cd27cae54c8b9d8a75e28ed976a85bb3b29817447dd997d3feece312d313(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a02f39771681630c681065e8812409b2b3da999da6ffc9de002326c14fd080a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a59a067fbf9d1f9b3f50b896222d0e513e5c3aba1f3a4b63d21ae50ae45f31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1668638897687cefcbb9ab519b0220152a601ecdbee23897ee9e6df56f222765(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90635ba8d02caa033bf1080f47c2d3bc23f501a3cdb2b55c26d719e5a41774d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed5b5d16391b353a74028fa075f9197a88fd361523c2ff737f5c1ed54bbd5e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c9ccb8c1a7c0c47248a3ba9d16bae6a0a4cebcdf3e5e24c51b2bc848514b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef0520c8fbca7e368bee85458d155abcf13e084f22c52d4bd6036d0f7813619(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e864c04cb1d697bf9ac265d2144b6401bdf8a6a2f8cef1464d7f8ef31e81f232(
    *,
    hours: jsii.Number,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a9aa27fbfa1be1995b5b75c14db542674572a64a9523868075bfd68a69f2a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c8951d17133a59dc25ea3a78111257cbe1d356cb96c3e9f89701734b32f7a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686b53c85db054de6c4b7ff02f9a75a8d197b0405df2c0ea2f5eacfb8a9dcdf7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3b8a9dd7c593d66974e737aae51d8d211f32ad5b9980170dcd53b732defe70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960d36c7715ed176df87f57f602538871559d6b3200a9bfe440a79008820ad92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d2de15a6a55ebe874d0f9f903f15771b90a609217f5019d460db1c5a66a7ca(
    value: typing.Optional[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a55bb159bdbc1564b426b4e56c1b64a771d7ece1eee61b00ed4df5cf66bdee1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485edfaa9930ad7349242b9a807a4eaba70425c1bfe01692153605dce7afbe6e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf74a1b8bf49a93f4689544e0ac747002506b7c089aeb6d813a42ac7dbf05ca(
    value: typing.Optional[AlloydbClusterMaintenanceUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fa799828cd744746ca2eecefb2d3f63fcfdf173bb6c4bf285265fa0ea3516f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6b525e616d3c00fc22f43edf6d5f300b8cffcee50ab782bb1cae39135c11f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6653a85dbf86d61498c26ae7ef8bd1590a867869649f7e7ed452c83207873fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b152a340d2cd1d1420fdd46a1316d6f00ec6ca175cce975958f55c15077a050(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6855bd6c10120999a4f3749296c6396da710198aad55db0d4b715212760f95(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7881b29a6322b3c5a1d762cb21919408c8cc52a863eb6858bfed5a7dc16630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6f8c4ce6d539f82b33951034a3323e35cd14fa690a99b8f9eb616c6dfcbee4(
    value: typing.Optional[AlloydbClusterMigrationSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129d6f8f01d10939b34aafa3eb7051c095e5de3ff32514ca7fb96f2f5c057844(
    *,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e7432ae189154e8d6ae18223e5585467a1d5acb8756d1a1bbc1a2abeae3a5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7392c4d254e465211c33655177d07d3f15bf0cb98a9c1566854b1995a967689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e6be651bfcb4bdb24069faba0e6079a5e4a072779ec7ef6cfc441e384c4235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13023aaf89e534afa6eeca73275f34c03f55778e4fdd40c7361aa78ee2dfe0bf(
    value: typing.Optional[AlloydbClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06727f16a0420e5afea6a4909d9e343ff7867c5577bf1aaebef5d42c45a31a70(
    *,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f427ea8c537f506b387f87b5a024167654345cc8609663a7b041617cf6f5e955(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e10840286e79408eef06e78b7e851ddb8ab86ab89935623842548190e57a998(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054f590db3bc199c257f2f540928371ec42f3c4dc52a76ee5fb03274ec567777(
    value: typing.Optional[AlloydbClusterPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7181194a70f38f22a4d9aebb9a799dc69d6aa49fef78dd2ac4b2e3e434d7d32(
    *,
    backup_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5ef5c6c07eeebe74ef5154a553168f237a996553b48a93be160b01ee00f9f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d266eaa0a168141da7353ccd8701c6a0013005e87e3157db787cb3554ebd62fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ab02b39d7038c18370a3b6bd1929d90c88600627220c7c9fd271561a380eef(
    value: typing.Optional[AlloydbClusterRestoreBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2035d25a536417b3c925021f750c64dfe5b9a6d491dd1ed6fc28349d9b833f5f(
    *,
    cluster: builtins.str,
    point_in_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937b1789a3c476f4c4ad0bc968afec90acb76b4bb90d6852cb0489d56ba05a35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60269e5756c0a5bf90f2b3fb24937acfc0b342e3fac4c65a8333e38efcf1236f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51adeb3146be59aa597d449a462197fa220dc99913a8fff20fc0c72fcaa0208c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741d3c6f9bc0c4c513fb9308f0ef10ce33138566ea644ab2a10ec4766f8a01d2(
    value: typing.Optional[AlloydbClusterRestoreContinuousBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a5ebb291002bc79675f3eba82e4abdff3ee50d08240e99c77c5d49f4f2e9db(
    *,
    primary_cluster_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cd72d9f29a658a9bbdd6814310f7fef0f5d3857e76749f5d85da37ea5739a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddd1228218218510876b3c9180522e08fb9738351a6668cbd830376c735bffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bbecd8718706de4c370959349ea589d063bba2c061ad3bb502f2317b7154de(
    value: typing.Optional[AlloydbClusterSecondaryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbe50cf2e4b23bbc2c62a71a05cd46d7932de15c40ed6e66b155f0a6cf9360b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adab4e39032d83339725978bbd87b85efa81966bf28b6195df269e825019a7de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5895f7e2ff6d7c76d8e294e43b53bb5d969751b3ff5b3e90565a99abdb76337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775086be08d0e7cf19468a2f0fc4135d2678db37ac11f61e8ea0798441bd8aaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237a984252eef25d83a6a95c287501e61cf2f38fe6e103f1b229f1ca0ed953a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5958295a012d287a52b9e6bab46a472063e3e5d39b533b2e0bdabc1df51ffd5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3b733ca060fac132801fd0be14bc2e53c14a7980f65899db161280c1151834(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc9b7ed404dfb9230d2bf4b08c4c502bcdef82510b0c7ce6f36fa0e970be11e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3635ef1094c556c453144315d9fbb602c527c0cf3ab4b35b3ff0326458b6bd2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea203e61432758dc3e849be0756c8ab9497da07ac0e3ca26843b7046ca6b5ea8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edce829eeb625b3aa44ecb848509e40295ef02c035ab635b57f04fb4be05d9d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4341a577cc97224059a7c9bab114e581b85b9d8246076d9543a418733f137d5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df991930effd84e2d0cf4e7c43a42bae11e6e8a5963365a63047f50a888c62f1(
    value: typing.Optional[AlloydbClusterTrialMetadata],
) -> None:
    """Type checking stubs"""
    pass

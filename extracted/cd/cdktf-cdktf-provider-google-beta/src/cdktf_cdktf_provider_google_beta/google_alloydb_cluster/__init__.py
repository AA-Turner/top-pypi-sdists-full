r'''
# `google_alloydb_cluster`

Refer to the Terraform Registry for docs: [`google_alloydb_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster).
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


class GoogleAlloydbCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster google_alloydb_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        location: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_backup_policy: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        continuous_backup_config: typing.Optional[typing.Union["GoogleAlloydbClusterContinuousBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_version: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_user: typing.Optional[typing.Union["GoogleAlloydbClusterInitialUser", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_update_policy: typing.Optional[typing.Union["GoogleAlloydbClusterMaintenanceUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleAlloydbClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["GoogleAlloydbClusterPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_source: typing.Optional[typing.Union["GoogleAlloydbClusterRestoreBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_continuous_backup_source: typing.Optional[typing.Union["GoogleAlloydbClusterRestoreContinuousBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_config: typing.Optional[typing.Union["GoogleAlloydbClusterSecondaryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAlloydbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster google_alloydb_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: The ID of the alloydb cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_id GoogleAlloydbCluster#cluster_id}
        :param location: The location where the alloydb cluster should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. https://google.aip.dev/128 An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#annotations GoogleAlloydbCluster#annotations}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#automated_backup_policy GoogleAlloydbCluster#automated_backup_policy}
        :param cluster_type: The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_type GoogleAlloydbCluster#cluster_type}
        :param continuous_backup_config: continuous_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#continuous_backup_config GoogleAlloydbCluster#continuous_backup_config}
        :param database_version: The database engine major version. This is an optional field and it's populated at the Cluster creation time. Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#database_version GoogleAlloydbCluster#database_version}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster. Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#deletion_policy GoogleAlloydbCluster#deletion_policy}
        :param display_name: User-settable and human-readable display name for the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#display_name GoogleAlloydbCluster#display_name}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param etag: For Resource freshness validation (https://google.aip.dev/154). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#etag GoogleAlloydbCluster#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#id GoogleAlloydbCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#initial_user GoogleAlloydbCluster#initial_user}
        :param labels: User-defined labels for the alloydb cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        :param maintenance_update_policy: maintenance_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_update_policy GoogleAlloydbCluster#maintenance_update_policy}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network_config GoogleAlloydbCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#project GoogleAlloydbCluster#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_config GoogleAlloydbCluster#psc_config}
        :param restore_backup_source: restore_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_backup_source GoogleAlloydbCluster#restore_backup_source}
        :param restore_continuous_backup_source: restore_continuous_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_continuous_backup_source GoogleAlloydbCluster#restore_continuous_backup_source}
        :param secondary_config: secondary_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#secondary_config GoogleAlloydbCluster#secondary_config}
        :param skip_await_major_version_upgrade: Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#skip_await_major_version_upgrade GoogleAlloydbCluster#skip_await_major_version_upgrade}
        :param subscription_type: The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#subscription_type GoogleAlloydbCluster#subscription_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#timeouts GoogleAlloydbCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db65a27640e86cadf9ccf9a5d2f732bed2f44bd2ccdf2c3cec616e30382915d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleAlloydbClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleAlloydbCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleAlloydbCluster to import.
        :param import_from_id: The id of the existing GoogleAlloydbCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleAlloydbCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc74511c620f0a9a20993ea32b9e5a8dcfc678297407f8d90de68e129348d744)
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
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        quantity_based_retention: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_retention: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backup_window: The length of the time window during which a backup can be taken. If a backup does not succeed within this time window, it will be canceled and considered failed. The backup window must be at least 5 minutes long. There is no upper bound on the window. If not set, it will default to 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_window GoogleAlloydbCluster#backup_window}
        :param enabled: Whether automated backups are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param labels: Labels to apply to backups created using this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        :param location: The location where the backup will be stored. Currently, the only supported option is to store the backup in the same region as the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
        :param quantity_based_retention: quantity_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#quantity_based_retention GoogleAlloydbCluster#quantity_based_retention}
        :param time_based_retention: time_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#time_based_retention GoogleAlloydbCluster#time_based_retention}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#weekly_schedule GoogleAlloydbCluster#weekly_schedule}
        '''
        value = GoogleAlloydbClusterAutomatedBackupPolicy(
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
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Whether continuous backup recovery is enabled. If not set, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param recovery_window_days: The numbers of days that are eligible to restore from using PITR. To support the entire recovery window, backups and logs are retained for one day more than the recovery window. If not set, defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#recovery_window_days GoogleAlloydbCluster#recovery_window_days}
        '''
        value = GoogleAlloydbClusterContinuousBackupConfig(
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
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        value = GoogleAlloydbClusterEncryptionConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putInitialUser")
    def put_initial_user(
        self,
        *,
        password: builtins.str,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#password GoogleAlloydbCluster#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#user GoogleAlloydbCluster#user}
        '''
        value = GoogleAlloydbClusterInitialUser(password=password, user=user)

        return typing.cast(None, jsii.invoke(self, "putInitialUser", [value]))

    @jsii.member(jsii_name="putMaintenanceUpdatePolicy")
    def put_maintenance_update_policy(
        self,
        *,
        maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param maintenance_windows: maintenance_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_windows GoogleAlloydbCluster#maintenance_windows}
        '''
        value = GoogleAlloydbClusterMaintenanceUpdatePolicy(
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
        :param allocated_ip_range: The name of the allocated IP range for the private IP AlloyDB cluster. For example: "google-managed-services-default". If set, the instance IPs for this cluster will be created in the allocated range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#allocated_ip_range GoogleAlloydbCluster#allocated_ip_range}
        :param network: The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network GoogleAlloydbCluster#network}
        '''
        value = GoogleAlloydbClusterNetworkConfig(
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
        :param psc_enabled: Create an instance that allows connections from Private Service Connect endpoints to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_enabled GoogleAlloydbCluster#psc_enabled}
        '''
        value = GoogleAlloydbClusterPscConfig(psc_enabled=psc_enabled)

        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="putRestoreBackupSource")
    def put_restore_backup_source(self, *, backup_name: builtins.str) -> None:
        '''
        :param backup_name: The name of the backup that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_name GoogleAlloydbCluster#backup_name}
        '''
        value = GoogleAlloydbClusterRestoreBackupSource(backup_name=backup_name)

        return typing.cast(None, jsii.invoke(self, "putRestoreBackupSource", [value]))

    @jsii.member(jsii_name="putRestoreContinuousBackupSource")
    def put_restore_continuous_backup_source(
        self,
        *,
        cluster: builtins.str,
        point_in_time: builtins.str,
    ) -> None:
        '''
        :param cluster: The name of the source cluster that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster GoogleAlloydbCluster#cluster}
        :param point_in_time: The point in time that this cluster is restored to, in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#point_in_time GoogleAlloydbCluster#point_in_time}
        '''
        value = GoogleAlloydbClusterRestoreContinuousBackupSource(
            cluster=cluster, point_in_time=point_in_time
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreContinuousBackupSource", [value]))

    @jsii.member(jsii_name="putSecondaryConfig")
    def put_secondary_config(self, *, primary_cluster_name: builtins.str) -> None:
        '''
        :param primary_cluster_name: Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#primary_cluster_name GoogleAlloydbCluster#primary_cluster_name}
        '''
        value = GoogleAlloydbClusterSecondaryConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#create GoogleAlloydbCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#delete GoogleAlloydbCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#update GoogleAlloydbCluster#update}.
        '''
        value = GoogleAlloydbClusterTimeouts(
            create=create, delete=delete, update=update
        )

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
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyOutputReference":
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyOutputReference", jsii.get(self, "automatedBackupPolicy"))

    @builtins.property
    @jsii.member(jsii_name="backupSource")
    def backup_source(self) -> "GoogleAlloydbClusterBackupSourceList":
        return typing.cast("GoogleAlloydbClusterBackupSourceList", jsii.get(self, "backupSource"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupConfig")
    def continuous_backup_config(
        self,
    ) -> "GoogleAlloydbClusterContinuousBackupConfigOutputReference":
        return typing.cast("GoogleAlloydbClusterContinuousBackupConfigOutputReference", jsii.get(self, "continuousBackupConfig"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupInfo")
    def continuous_backup_info(self) -> "GoogleAlloydbClusterContinuousBackupInfoList":
        return typing.cast("GoogleAlloydbClusterContinuousBackupInfoList", jsii.get(self, "continuousBackupInfo"))

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
    def encryption_config(
        self,
    ) -> "GoogleAlloydbClusterEncryptionConfigOutputReference":
        return typing.cast("GoogleAlloydbClusterEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="encryptionInfo")
    def encryption_info(self) -> "GoogleAlloydbClusterEncryptionInfoList":
        return typing.cast("GoogleAlloydbClusterEncryptionInfoList", jsii.get(self, "encryptionInfo"))

    @builtins.property
    @jsii.member(jsii_name="initialUser")
    def initial_user(self) -> "GoogleAlloydbClusterInitialUserOutputReference":
        return typing.cast("GoogleAlloydbClusterInitialUserOutputReference", jsii.get(self, "initialUser"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceUpdatePolicy")
    def maintenance_update_policy(
        self,
    ) -> "GoogleAlloydbClusterMaintenanceUpdatePolicyOutputReference":
        return typing.cast("GoogleAlloydbClusterMaintenanceUpdatePolicyOutputReference", jsii.get(self, "maintenanceUpdatePolicy"))

    @builtins.property
    @jsii.member(jsii_name="migrationSource")
    def migration_source(self) -> "GoogleAlloydbClusterMigrationSourceList":
        return typing.cast("GoogleAlloydbClusterMigrationSourceList", jsii.get(self, "migrationSource"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="networkConfig")
    def network_config(self) -> "GoogleAlloydbClusterNetworkConfigOutputReference":
        return typing.cast("GoogleAlloydbClusterNetworkConfigOutputReference", jsii.get(self, "networkConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(self) -> "GoogleAlloydbClusterPscConfigOutputReference":
        return typing.cast("GoogleAlloydbClusterPscConfigOutputReference", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupSource")
    def restore_backup_source(
        self,
    ) -> "GoogleAlloydbClusterRestoreBackupSourceOutputReference":
        return typing.cast("GoogleAlloydbClusterRestoreBackupSourceOutputReference", jsii.get(self, "restoreBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="restoreContinuousBackupSource")
    def restore_continuous_backup_source(
        self,
    ) -> "GoogleAlloydbClusterRestoreContinuousBackupSourceOutputReference":
        return typing.cast("GoogleAlloydbClusterRestoreContinuousBackupSourceOutputReference", jsii.get(self, "restoreContinuousBackupSource"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConfig")
    def secondary_config(self) -> "GoogleAlloydbClusterSecondaryConfigOutputReference":
        return typing.cast("GoogleAlloydbClusterSecondaryConfigOutputReference", jsii.get(self, "secondaryConfig"))

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
    def timeouts(self) -> "GoogleAlloydbClusterTimeoutsOutputReference":
        return typing.cast("GoogleAlloydbClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trialMetadata")
    def trial_metadata(self) -> "GoogleAlloydbClusterTrialMetadataList":
        return typing.cast("GoogleAlloydbClusterTrialMetadataList", jsii.get(self, "trialMetadata"))

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
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicy"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicy"], jsii.get(self, "automatedBackupPolicyInput"))

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
    ) -> typing.Optional["GoogleAlloydbClusterContinuousBackupConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterContinuousBackupConfig"], jsii.get(self, "continuousBackupConfigInput"))

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
    ) -> typing.Optional["GoogleAlloydbClusterEncryptionConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

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
    def initial_user_input(self) -> typing.Optional["GoogleAlloydbClusterInitialUser"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterInitialUser"], jsii.get(self, "initialUserInput"))

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
    ) -> typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicy"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicy"], jsii.get(self, "maintenanceUpdatePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigInput")
    def network_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterNetworkConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterNetworkConfig"], jsii.get(self, "networkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(self) -> typing.Optional["GoogleAlloydbClusterPscConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterPscConfig"], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreBackupSourceInput")
    def restore_backup_source_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterRestoreBackupSource"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterRestoreBackupSource"], jsii.get(self, "restoreBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreContinuousBackupSourceInput")
    def restore_continuous_backup_source_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterRestoreContinuousBackupSource"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterRestoreContinuousBackupSource"], jsii.get(self, "restoreContinuousBackupSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConfigInput")
    def secondary_config_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterSecondaryConfig"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterSecondaryConfig"], jsii.get(self, "secondaryConfigInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAlloydbClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleAlloydbClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b6a5ad9fa85a9489d173232ed64c1dd00475a219064adc6753a86fb364b291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a7620f01240d2ba7aa7fb236ff97100160a02d010e3f5d00b695373dc1e317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterType"))

    @cluster_type.setter
    def cluster_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787e13ee492d3903ec95a3ea9594b35d24cd4479724d8e1a3e8c9359c171ed70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseVersion")
    def database_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseVersion"))

    @database_version.setter
    def database_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acdd71b570c5e9144054a0604cd3165b4aa3901e7d05ce66e6d1c73991b73bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionPolicy")
    def deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionPolicy"))

    @deletion_policy.setter
    def deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f861d1925127d7abfbb38f9cabd38538b4ed79d1e9d2004de739f111f20558d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a882d681d627d0f7f4bcc496a2e0f9c3851ee56b82ed077d11c8bb501e5db6a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e002dc26d8425bbcda7b87369f5e6f772fc66260fb691cf16cbd0cfe5cb68c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b842cc9829af11ec72fd1ece428b2600da3d949ac5226ad3f43da1fb87a3375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2306f18dfa639a28a7ec00d8e7b57995734caff0969a353b30cc544450005a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2646a147d141c8f146a4e875db4dbfbc4cf4755c5337e26d00b73005a42ed32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c78536b9fbd0c48d1db02e8d3daf5481063e0cd8f8a0705035b10e164d111bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61e631ea42970e9b5f03fdd590ecea3f9bb5ce6451e9a9bc4b9a2fba9a4a6b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipAwaitMajorVersionUpgrade", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionType")
    def subscription_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionType"))

    @subscription_type.setter
    def subscription_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2765a979255317cb68005382c21a84e3cea817e8a178262cf8b7054db392f450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicy",
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
class GoogleAlloydbClusterAutomatedBackupPolicy:
    def __init__(
        self,
        *,
        backup_window: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        quantity_based_retention: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        time_based_retention: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        weekly_schedule: typing.Optional[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param backup_window: The length of the time window during which a backup can be taken. If a backup does not succeed within this time window, it will be canceled and considered failed. The backup window must be at least 5 minutes long. There is no upper bound on the window. If not set, it will default to 1 hour. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_window GoogleAlloydbCluster#backup_window}
        :param enabled: Whether automated backups are enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param labels: Labels to apply to backups created using this configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        :param location: The location where the backup will be stored. Currently, the only supported option is to store the backup in the same region as the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
        :param quantity_based_retention: quantity_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#quantity_based_retention GoogleAlloydbCluster#quantity_based_retention}
        :param time_based_retention: time_based_retention block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#time_based_retention GoogleAlloydbCluster#time_based_retention}
        :param weekly_schedule: weekly_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#weekly_schedule GoogleAlloydbCluster#weekly_schedule}
        '''
        if isinstance(encryption_config, dict):
            encryption_config = GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig(**encryption_config)
        if isinstance(quantity_based_retention, dict):
            quantity_based_retention = GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(**quantity_based_retention)
        if isinstance(time_based_retention, dict):
            time_based_retention = GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention(**time_based_retention)
        if isinstance(weekly_schedule, dict):
            weekly_schedule = GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule(**weekly_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3da0e06e22c95b0d03456da3c707825aba3e76ede46f22a30a5fe722c174c33)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_window GoogleAlloydbCluster#backup_window}
        '''
        result = self._values.get("backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether automated backups are enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to backups created using this configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location where the backup will be stored.

        Currently, the only supported option is to store the backup in the same region as the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quantity_based_retention(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"]:
        '''quantity_based_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#quantity_based_retention GoogleAlloydbCluster#quantity_based_retention}
        '''
        result = self._values.get("quantity_based_retention")
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"], result)

    @builtins.property
    def time_based_retention(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention"]:
        '''time_based_retention block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#time_based_retention GoogleAlloydbCluster#time_based_retention}
        '''
        result = self._values.get("time_based_retention")
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention"], result)

    @builtins.property
    def weekly_schedule(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule"]:
        '''weekly_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#weekly_schedule GoogleAlloydbCluster#weekly_schedule}
        '''
        result = self._values.get("weekly_schedule")
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad549652af7f536259d75dab386c7ad4d799adca246c1cf0608b17e38231b35)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f83c8a30518470242d8e15c4cdfa04ebd8f975b5a5d2e456f02803d1125fc4f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a1f0da605e9f573c9a8c6c82a8d04a319d8a600a31b194edd2eb9cf29c2465b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03936fc1d319f0df372ba453c9c25953fdc2bfbeabd8bd0652f58732e76e8c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterAutomatedBackupPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ab2db6a8cb5a98f96e21df83dc612c6fbc9cc0cb2405aff3eedfc656fce1bbd)
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
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        value = GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig(
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
        :param count: The number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#count GoogleAlloydbCluster#count}
        '''
        value = GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(
            count=count
        )

        return typing.cast(None, jsii.invoke(self, "putQuantityBasedRetention", [value]))

    @jsii.member(jsii_name="putTimeBasedRetention")
    def put_time_based_retention(
        self,
        *,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_period: The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#retention_period GoogleAlloydbCluster#retention_period}
        '''
        value = GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention(
            retention_period=retention_period
        )

        return typing.cast(None, jsii.invoke(self, "putTimeBasedRetention", [value]))

    @jsii.member(jsii_name="putWeeklySchedule")
    def put_weekly_schedule(
        self,
        *,
        start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param start_times: start_times block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#start_times GoogleAlloydbCluster#start_times}
        :param days_of_week: The days of the week to perform a backup. At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#days_of_week GoogleAlloydbCluster#days_of_week}
        '''
        value = GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule(
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
    ) -> GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference:
        return typing.cast(GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="quantityBasedRetention")
    def quantity_based_retention(
        self,
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference":
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference", jsii.get(self, "quantityBasedRetention"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedRetention")
    def time_based_retention(
        self,
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference":
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference", jsii.get(self, "timeBasedRetention"))

    @builtins.property
    @jsii.member(jsii_name="weeklySchedule")
    def weekly_schedule(
        self,
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference":
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference", jsii.get(self, "weeklySchedule"))

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
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

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
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention"], jsii.get(self, "quantityBasedRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeBasedRetentionInput")
    def time_based_retention_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention"], jsii.get(self, "timeBasedRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyScheduleInput")
    def weekly_schedule_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule"], jsii.get(self, "weeklyScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="backupWindow")
    def backup_window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupWindow"))

    @backup_window.setter
    def backup_window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d68daf9345c94f5a8bf390ee5771c377eb63e2f585b0fdec0f08d280c1e3c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b28aae1364d26f93e610d6d45463a302021ee1c111517adf9d656218cd17972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7769f56e282ca50ff96b87f6d5e99cf8e4f296000329f1e1ac8d035eee22b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ac33ea7a39572987a92d27445b30daf0072a63bae1cc257f4b06111a2077d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b421f85dc33344842f722f47d816cde9650adf9d08dd911bd35d8bbfd7793e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention",
    jsii_struct_bases=[],
    name_mapping={"count": "count"},
)
class GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention:
    def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param count: The number of backups to retain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#count GoogleAlloydbCluster#count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d380605aadc72361bd69bc3971e0ff2149a0c331fbb63facaaf4684929a7d2e9)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of backups to retain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#count GoogleAlloydbCluster#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72ac4f456fc6e62fb682a239c2138b8d1647802451ed776811ccd8bccd4363e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b46797f7b67c6cdf55318feec865f926e8a743b1eab77219cbdead27b17821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f316c885fb77529e82947887b50c8877a10b4e8499e0437bd68f9aa337059a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention",
    jsii_struct_bases=[],
    name_mapping={"retention_period": "retentionPeriod"},
)
class GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention:
    def __init__(
        self,
        *,
        retention_period: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param retention_period: The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#retention_period GoogleAlloydbCluster#retention_period}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b168068dd37391716c4d0f8899c38bf6a7328cbc6e36a90cd5167549f7b6138b)
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if retention_period is not None:
            self._values["retention_period"] = retention_period

    @builtins.property
    def retention_period(self) -> typing.Optional[builtins.str]:
        '''The retention period. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#retention_period GoogleAlloydbCluster#retention_period}
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c8ea99c158aa375445175547fd771359e407e1d42774d293747edabd0d6194)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5db1f2a66375a2a1d84796811b6db17046fa777eba1f90e6c384f273cf8dff35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc3437cf89e187d65679baffb096c943dedeb1b150097e277c2d2be0ed4bbf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule",
    jsii_struct_bases=[],
    name_mapping={"start_times": "startTimes", "days_of_week": "daysOfWeek"},
)
class GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule:
    def __init__(
        self,
        *,
        start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param start_times: start_times block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#start_times GoogleAlloydbCluster#start_times}
        :param days_of_week: The days of the week to perform a backup. At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#days_of_week GoogleAlloydbCluster#days_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733a37b2b059f2f44ff196160fc6347d76b6803ba3753de096ba22e65f242890)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]:
        '''start_times block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#start_times GoogleAlloydbCluster#start_times}
        '''
        result = self._values.get("start_times")
        assert result is not None, "Required property 'start_times' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The days of the week to perform a backup.

        At least one day of the week must be provided. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#days_of_week GoogleAlloydbCluster#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef267acd2437ef250cd68eaf958576018dcf5c8aa451d33b4aa258bf382bdd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTimes")
    def put_start_times(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec5a11ab67ecec77b94b074f713f8a834e01ca88c97a6621b36a4fd7495664e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStartTimes", [value]))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @builtins.property
    @jsii.member(jsii_name="startTimes")
    def start_times(
        self,
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList":
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList", jsii.get(self, "startTimes"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimesInput")
    def start_times_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes"]]], jsii.get(self, "startTimesInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220d49d3f35abaeffd2e3ba838bd7ce17a0d4f517dd9b4acf723c59ef3ec8820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d26827086ce29c58545d1c0e99b0557b81863283084ce34f5d885ab111b3324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. An API may choose to allow the value "24:00:00" for scenarios like business closing time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#hours GoogleAlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#minutes GoogleAlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#nanos GoogleAlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#seconds GoogleAlloydbCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55636ca490f44ef49772449712b9fa758f92ede4e43aed580446ab072e99f50)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#hours GoogleAlloydbCluster#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#minutes GoogleAlloydbCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#nanos GoogleAlloydbCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#seconds GoogleAlloydbCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7df070ced58ee5837f77cbe65bbe045e3c9052ae62f047049f3ec0c52db32d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8c8eb09c83595da8215d161ba88a4a5ffa7bfdff65bdf33b4c7c5bd0bb639f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d31427526488a4ac1c5ef3d707337e44863c90911ab2b0f3bd975b09b0f9ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6febb310895f75a7569933450b6c3a19488f9c4aa34cac207f5858fe30625)
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
            type_hints = typing.get_type_hints(_typecheckingstub__454c34abac78f9d1b3e7d8712cb58777dfce77af71e97ae2d5a1708652be4b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2600d24a725b43f26219f48c626ea93dbc75618c1d406ba6bc98be4bf383487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__882d45a0efd08dd1de84095b26d29f475d38f572d14e467cb68db1255844663b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2a250285e3509188c7b3b102dd69b9711a5844f988b55e021ea0fd8c4c3021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79eb4716560402825b3d80daa53b9caedf2e8ad5d204849d3deaf1176891a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2ea0c0f8974d283a714c728e078d37b865b9b0398eb33f5abaf72bc0d71af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd01f2e68e3e1b741bf5e4a509891470acbd1ad97b819eeeb61d9a781c6d7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8125f9e039e46e2fbd9d98fab6b5fb97b849e29499607750f154eec87e97c5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterBackupSource",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterBackupSource:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterBackupSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterBackupSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ff6aba4da0f4406b1d4a5addcf2be30b63cb8f58143b21a9d6f16a473f2e8be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterBackupSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0872998ce951c74ebcea2082fceb1a73755c6af09bc14fe25fd46cfaf291eb8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterBackupSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5657fc0b07766da1a57bf5a8a1f7e73e46d5b627079bfe5b51c5cd99f242f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52f76e74c36b9eec0369db2f4f8d6d15a924c46947d19a8ea8191ecd0804bf1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bf28f3abf25f1697336324f754a10616ba3417985862edf7fec2c2ed766c3f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f033de15b75cb7a4a0bf2295181856dfa78d5ff6d687510092eb0f5a7a78b1)
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
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterBackupSource]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92df2119583f7820be86b23a525de4d20175b4ad6cb2200f1a9c98e6e894df74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterConfig",
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
class GoogleAlloydbClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automated_backup_policy: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        continuous_backup_config: typing.Optional[typing.Union["GoogleAlloydbClusterContinuousBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        database_version: typing.Optional[builtins.str] = None,
        deletion_policy: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initial_user: typing.Optional[typing.Union["GoogleAlloydbClusterInitialUser", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maintenance_update_policy: typing.Optional[typing.Union["GoogleAlloydbClusterMaintenanceUpdatePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        network_config: typing.Optional[typing.Union["GoogleAlloydbClusterNetworkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["GoogleAlloydbClusterPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_backup_source: typing.Optional[typing.Union["GoogleAlloydbClusterRestoreBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        restore_continuous_backup_source: typing.Optional[typing.Union["GoogleAlloydbClusterRestoreContinuousBackupSource", typing.Dict[builtins.str, typing.Any]]] = None,
        secondary_config: typing.Optional[typing.Union["GoogleAlloydbClusterSecondaryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleAlloydbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: The ID of the alloydb cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_id GoogleAlloydbCluster#cluster_id}
        :param location: The location where the alloydb cluster should reside. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. https://google.aip.dev/128 An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#annotations GoogleAlloydbCluster#annotations}
        :param automated_backup_policy: automated_backup_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#automated_backup_policy GoogleAlloydbCluster#automated_backup_policy}
        :param cluster_type: The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_type GoogleAlloydbCluster#cluster_type}
        :param continuous_backup_config: continuous_backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#continuous_backup_config GoogleAlloydbCluster#continuous_backup_config}
        :param database_version: The database engine major version. This is an optional field and it's populated at the Cluster creation time. Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#database_version GoogleAlloydbCluster#database_version}
        :param deletion_policy: Policy to determine if the cluster should be deleted forcefully. Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster. Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance. Possible values: DEFAULT, FORCE Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#deletion_policy GoogleAlloydbCluster#deletion_policy}
        :param display_name: User-settable and human-readable display name for the Cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#display_name GoogleAlloydbCluster#display_name}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param etag: For Resource freshness validation (https://google.aip.dev/154). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#etag GoogleAlloydbCluster#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#id GoogleAlloydbCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_user: initial_user block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#initial_user GoogleAlloydbCluster#initial_user}
        :param labels: User-defined labels for the alloydb cluster. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        :param maintenance_update_policy: maintenance_update_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_update_policy GoogleAlloydbCluster#maintenance_update_policy}
        :param network_config: network_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network_config GoogleAlloydbCluster#network_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#project GoogleAlloydbCluster#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_config GoogleAlloydbCluster#psc_config}
        :param restore_backup_source: restore_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_backup_source GoogleAlloydbCluster#restore_backup_source}
        :param restore_continuous_backup_source: restore_continuous_backup_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_continuous_backup_source GoogleAlloydbCluster#restore_continuous_backup_source}
        :param secondary_config: secondary_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#secondary_config GoogleAlloydbCluster#secondary_config}
        :param skip_await_major_version_upgrade: Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#skip_await_major_version_upgrade GoogleAlloydbCluster#skip_await_major_version_upgrade}
        :param subscription_type: The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#subscription_type GoogleAlloydbCluster#subscription_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#timeouts GoogleAlloydbCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automated_backup_policy, dict):
            automated_backup_policy = GoogleAlloydbClusterAutomatedBackupPolicy(**automated_backup_policy)
        if isinstance(continuous_backup_config, dict):
            continuous_backup_config = GoogleAlloydbClusterContinuousBackupConfig(**continuous_backup_config)
        if isinstance(encryption_config, dict):
            encryption_config = GoogleAlloydbClusterEncryptionConfig(**encryption_config)
        if isinstance(initial_user, dict):
            initial_user = GoogleAlloydbClusterInitialUser(**initial_user)
        if isinstance(maintenance_update_policy, dict):
            maintenance_update_policy = GoogleAlloydbClusterMaintenanceUpdatePolicy(**maintenance_update_policy)
        if isinstance(network_config, dict):
            network_config = GoogleAlloydbClusterNetworkConfig(**network_config)
        if isinstance(psc_config, dict):
            psc_config = GoogleAlloydbClusterPscConfig(**psc_config)
        if isinstance(restore_backup_source, dict):
            restore_backup_source = GoogleAlloydbClusterRestoreBackupSource(**restore_backup_source)
        if isinstance(restore_continuous_backup_source, dict):
            restore_continuous_backup_source = GoogleAlloydbClusterRestoreContinuousBackupSource(**restore_continuous_backup_source)
        if isinstance(secondary_config, dict):
            secondary_config = GoogleAlloydbClusterSecondaryConfig(**secondary_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleAlloydbClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fbe21be7436ddeb4b208a6660791ff03b76ae3d6303805f56a61810cd66694)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_id GoogleAlloydbCluster#cluster_id}
        '''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location where the alloydb cluster should reside.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#location GoogleAlloydbCluster#location}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#annotations GoogleAlloydbCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def automated_backup_policy(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy]:
        '''automated_backup_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#automated_backup_policy GoogleAlloydbCluster#automated_backup_policy}
        '''
        result = self._values.get("automated_backup_policy")
        return typing.cast(typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy], result)

    @builtins.property
    def cluster_type(self) -> typing.Optional[builtins.str]:
        '''The type of cluster. If not set, defaults to PRIMARY. Default value: "PRIMARY" Possible values: ["PRIMARY", "SECONDARY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster_type GoogleAlloydbCluster#cluster_type}
        '''
        result = self._values.get("cluster_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def continuous_backup_config(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterContinuousBackupConfig"]:
        '''continuous_backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#continuous_backup_config GoogleAlloydbCluster#continuous_backup_config}
        '''
        result = self._values.get("continuous_backup_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterContinuousBackupConfig"], result)

    @builtins.property
    def database_version(self) -> typing.Optional[builtins.str]:
        '''The database engine major version.

        This is an optional field and it's populated at the Cluster creation time.
        Note: Changing this field to a higer version results in upgrading the AlloyDB cluster which is an irreversible change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#database_version GoogleAlloydbCluster#database_version}
        '''
        result = self._values.get("database_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Policy to determine if the cluster should be deleted forcefully.

        Deleting a cluster forcefully, deletes the cluster and all its associated instances within the cluster.
        Deleting a Secondary cluster with a secondary instance REQUIRES setting deletion_policy = "FORCE" otherwise an error is returned. This is needed as there is no support to delete just the secondary instance, and the only way to delete secondary instance is to delete the associated secondary cluster forcefully which also deletes the secondary instance.
        Possible values: DEFAULT, FORCE

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#deletion_policy GoogleAlloydbCluster#deletion_policy}
        '''
        result = self._values.get("deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-settable and human-readable display name for the Cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#display_name GoogleAlloydbCluster#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterEncryptionConfig"], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''For Resource freshness validation (https://google.aip.dev/154).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#etag GoogleAlloydbCluster#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#id GoogleAlloydbCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_user(self) -> typing.Optional["GoogleAlloydbClusterInitialUser"]:
        '''initial_user block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#initial_user GoogleAlloydbCluster#initial_user}
        '''
        result = self._values.get("initial_user")
        return typing.cast(typing.Optional["GoogleAlloydbClusterInitialUser"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the alloydb cluster.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#labels GoogleAlloydbCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maintenance_update_policy(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicy"]:
        '''maintenance_update_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_update_policy GoogleAlloydbCluster#maintenance_update_policy}
        '''
        result = self._values.get("maintenance_update_policy")
        return typing.cast(typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicy"], result)

    @builtins.property
    def network_config(self) -> typing.Optional["GoogleAlloydbClusterNetworkConfig"]:
        '''network_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network_config GoogleAlloydbCluster#network_config}
        '''
        result = self._values.get("network_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterNetworkConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#project GoogleAlloydbCluster#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(self) -> typing.Optional["GoogleAlloydbClusterPscConfig"]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_config GoogleAlloydbCluster#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterPscConfig"], result)

    @builtins.property
    def restore_backup_source(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterRestoreBackupSource"]:
        '''restore_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_backup_source GoogleAlloydbCluster#restore_backup_source}
        '''
        result = self._values.get("restore_backup_source")
        return typing.cast(typing.Optional["GoogleAlloydbClusterRestoreBackupSource"], result)

    @builtins.property
    def restore_continuous_backup_source(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterRestoreContinuousBackupSource"]:
        '''restore_continuous_backup_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#restore_continuous_backup_source GoogleAlloydbCluster#restore_continuous_backup_source}
        '''
        result = self._values.get("restore_continuous_backup_source")
        return typing.cast(typing.Optional["GoogleAlloydbClusterRestoreContinuousBackupSource"], result)

    @builtins.property
    def secondary_config(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterSecondaryConfig"]:
        '''secondary_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#secondary_config GoogleAlloydbCluster#secondary_config}
        '''
        result = self._values.get("secondary_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterSecondaryConfig"], result)

    @builtins.property
    def skip_await_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to skip awaiting on the major version upgrade of the cluster. Possible values: true, false Default value: "true".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#skip_await_major_version_upgrade GoogleAlloydbCluster#skip_await_major_version_upgrade}
        '''
        result = self._values.get("skip_await_major_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subscription_type(self) -> typing.Optional[builtins.str]:
        '''The subscrition type of cluster. Possible values: ["TRIAL", "STANDARD"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#subscription_type GoogleAlloydbCluster#subscription_type}
        '''
        result = self._values.get("subscription_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleAlloydbClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#timeouts GoogleAlloydbCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleAlloydbClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "encryption_config": "encryptionConfig",
        "recovery_window_days": "recoveryWindowDays",
    },
)
class GoogleAlloydbClusterContinuousBackupConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union["GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_window_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Whether continuous backup recovery is enabled. If not set, defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        :param recovery_window_days: The numbers of days that are eligible to restore from using PITR. To support the entire recovery window, backups and logs are retained for one day more than the recovery window. If not set, defaults to 14 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#recovery_window_days GoogleAlloydbCluster#recovery_window_days}
        '''
        if isinstance(encryption_config, dict):
            encryption_config = GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig(**encryption_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b327a1ca6300f1b0d19ee99ffad88368e21fb90bb8bc6763297f55402535529)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#enabled GoogleAlloydbCluster#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#encryption_config GoogleAlloydbCluster#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig"], result)

    @builtins.property
    def recovery_window_days(self) -> typing.Optional[jsii.Number]:
        '''The numbers of days that are eligible to restore from using PITR.

        To support the entire recovery window, backups and logs are retained for one day more than the recovery window.

        If not set, defaults to 14 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#recovery_window_days GoogleAlloydbCluster#recovery_window_days}
        '''
        result = self._values.get("recovery_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterContinuousBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788f0ec21185476d6f132d7ca1454d29eff662a9b5392937b2fc7a7431583f1f)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44ca868bf0677e564c65712b82001045ccebde024d5b50aa85079f36d98257a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__433510c820c87fb93625ee96865e219533e463fda249c419ae186f1c00e31614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31400fdad8281a70b0fceacd2d597845b1fdd5f37178d52966ff3916407d55ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterContinuousBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2d3d1e243062c2e906dcf9f04e164d598f4521094a9a8c0b88d4ed64a3dcf1c)
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
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        value = GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig(
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
    ) -> GoogleAlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference:
        return typing.cast(GoogleAlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference, jsii.get(self, "encryptionConfig"))

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
    ) -> typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig], jsii.get(self, "encryptionConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__456b3008ee008197f46e32afc5e8471b799024b81027e83f1357e6c793661772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryWindowDays")
    def recovery_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recoveryWindowDays"))

    @recovery_window_days.setter
    def recovery_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d370032addf72cf2744edf3b56c78309d844da75b983045688f8f777378a06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryWindowDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterContinuousBackupConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterContinuousBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterContinuousBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce69f233c784670be5e37ec145eb52eabf68c5c218968dfc99e5cf0380bb691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterContinuousBackupInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterContinuousBackupInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb4022ae0a04dd73db2fc8389ca769f25e1e6e40e130550339eb4db436acba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad506bfa32cd9813bc9b467215980e03a8013a9d813b72338bafd399ef4bf6cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4b4f531276fbf60773c42311404526087ecd163a773b53b7d539fe3e6803c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea1ad2bdc4f63808a243c2e12c2f77fcbc839b18f314b6fc6b17c28c403490a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2af788d788d8379a5c20b7f00942af0de89743db3fd8616dbd39ac66559f2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__067aea8770f7f3c4b0f724a1ef0997b5464bc40b6a62c55de1ab83dc6ccb058e)
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
    ) -> typing.Optional[GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be62a727ce31a6cee7bc2d6eb2c113870c6ce86dc07f20816369e8bb5ffbb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterContinuousBackupInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4408bd0d37aabbf08162776eba834db7f93df18ff88b3ad3fc3eb7b34243cc1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterContinuousBackupInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123689370e62c4cd4926e319c74915816088144e3487d2187aacc6d01ceedff1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterContinuousBackupInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503f54cd4a8276b269cee5515dc7a6ef303127cc96f3d426ec55b89dc1352482)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d9f76085d510be67af42ac73f90ea3d86d7a76b9769723d7f138bb41c475daa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__494d9a1bcd22d3ac64c13f502b7e03daede9dccdbd2129d871edefb18543722c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterContinuousBackupInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterContinuousBackupInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__200fe6d82ea47a018be70f9c937fc6c8ecf8cfb7f74b2be1775a27a53d2a6a07)
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
    def encryption_info(
        self,
    ) -> GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoList:
        return typing.cast(GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoList, jsii.get(self, "encryptionInfo"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterContinuousBackupInfo]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterContinuousBackupInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterContinuousBackupInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deddf95d0a7af74cdb3eb08c3c3f41c50ab68410ac662faf1b0859f08df0a946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class GoogleAlloydbClusterEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: The fully-qualified resource name of the KMS key. Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6994e48e54ff2b9ca317808e2c0e7efc87c70029c476648484b4a0266f71ea9d)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The fully-qualified resource name of the KMS key.

        Each Cloud KMS key is regionalized and has the following format: projects/[PROJECT]/locations/[REGION]/keyRings/[RING]/cryptoKeys/[KEY_NAME].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#kms_key_name GoogleAlloydbCluster#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df7029fc6ff3ad5003ef4cd1deaa5e24a4c17795e7deb68dece4487a64ecbf53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c896d7370935984bb78c20e0129678a54e67eb159d9e1c47cd1cda4ef48209c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterEncryptionConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12abf09d1ec65184e481a83f4d35ba08dd969b0590e8ca98606655420376724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterEncryptionInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterEncryptionInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterEncryptionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterEncryptionInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterEncryptionInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e458073409d2117540252c72ab32a671a1155d43d012bdd48cba389a88cdf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterEncryptionInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe02cbddb6495b6f8c3c2fb90e82cc5078840631d04ab5f7b3c982f48c288eb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterEncryptionInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c3d0650964210923bed0547923dac416e355b0c0bbc487291c7805fd1a0c3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c6dd133b546820621ba291a2dc62b88340f8194da01d8f9cede6cfa2e37e909)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd260299fe1bd3ac971b02761f563d753e0601133d31d99589a7867c1899a55d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterEncryptionInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterEncryptionInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7b0527ed0ee850e5d06a591411135720c7fce3cef7b199f31d6987af163f79)
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
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterEncryptionInfo]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterEncryptionInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterEncryptionInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c65f5e686f5c5014ac38bb3b22a96c8f71396fbb58abb9588c59887e9fe1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterInitialUser",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "user": "user"},
)
class GoogleAlloydbClusterInitialUser:
    def __init__(
        self,
        *,
        password: builtins.str,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param password: The initial password for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#password GoogleAlloydbCluster#password}
        :param user: The database username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#user GoogleAlloydbCluster#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1112959200f4c6a14d4f3185120f30764f95b83fb8bc3959906a6fef0b75a049)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#password GoogleAlloydbCluster#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The database username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#user GoogleAlloydbCluster#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterInitialUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterInitialUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterInitialUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e850851a4012c4472f36665321bf2e46df8ab26a57aa1cbc49abe0199721236b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__533782a8de237a3361afc14cf00062009106935850a963f89e626954afc4e45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1787ec10196ad222103da783265e5439845d7c50255d3a2f869b23eb7be04190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterInitialUser]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterInitialUser], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterInitialUser],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac5d1eeb81dc8799366769a3207a199da187838208da24c8fe5d10885b5a09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicy",
    jsii_struct_bases=[],
    name_mapping={"maintenance_windows": "maintenanceWindows"},
)
class GoogleAlloydbClusterMaintenanceUpdatePolicy:
    def __init__(
        self,
        *,
        maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param maintenance_windows: maintenance_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_windows GoogleAlloydbCluster#maintenance_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb1eff2012f9ed67f19955e9b6cc22b73b006a4bf63aca24e16223a64b68774)
            check_type(argname="argument maintenance_windows", value=maintenance_windows, expected_type=type_hints["maintenance_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maintenance_windows is not None:
            self._values["maintenance_windows"] = maintenance_windows

    @builtins.property
    def maintenance_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows"]]]:
        '''maintenance_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#maintenance_windows GoogleAlloydbCluster#maintenance_windows}
        '''
        result = self._values.get("maintenance_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterMaintenanceUpdatePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "start_time": "startTime"},
)
class GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows:
    def __init__(
        self,
        *,
        day: builtins.str,
        start_time: typing.Union["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day: Preferred day of the week for maintenance, e.g. MONDAY, TUESDAY, etc. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#day GoogleAlloydbCluster#day}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#start_time GoogleAlloydbCluster#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8debbf5550ad1f1e0ab0b37929f7aab9f2ef9810b950c25ac344b1429b775db)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day": day,
            "start_time": start_time,
        }

    @builtins.property
    def day(self) -> builtins.str:
        '''Preferred day of the week for maintenance, e.g. MONDAY, TUESDAY, etc. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#day GoogleAlloydbCluster#day}
        '''
        result = self._values.get("day")
        assert result is not None, "Required property 'day' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#start_time GoogleAlloydbCluster#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b7df89afc4420b057460dfccc08126fd7191459a99d2522478598e1f5c79cbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321adc16b7c57585d8f1996ec233af5802bd951ee0337e94aa66a72bbb85c850)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69eb142ca446494b37a19280d9332687be7624becae9453395f2b64f33a8770)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f86d7e416c1d294de75c7262c89294260127bd83156b0ebe870f72e26163ec8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ddba3541ef0cbdfd2b2ad9a73f31077a21d602cd9ba6122d8a9846b7bdc18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179b962e57538e6e4c2795b70ecbc80f5ce06dce60c7641a6a0a88f8b485440d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ca647e62c53add2a8fd2e9b178e7115f4e269b8b0549f2e4c1f06d7eb15312c)
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
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#hours GoogleAlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#minutes GoogleAlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#nanos GoogleAlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#seconds GoogleAlloydbCluster#seconds}
        '''
        value = GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference":
        return typing.cast("GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime"]:
        return typing.cast(typing.Optional["GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "day"))

    @day.setter
    def day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8437113010253270c541de41b7401fcbfd1f69144f2f86b30ec83b58a2acfc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41ea56b45206cfe14acb5e7afa2d0a4fc83eb8b286f13f0bdd84d573e691c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime:
    def __init__(
        self,
        *,
        hours: jsii.Number,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#hours GoogleAlloydbCluster#hours}
        :param minutes: Minutes of hour of day. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#minutes GoogleAlloydbCluster#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#nanos GoogleAlloydbCluster#nanos}
        :param seconds: Seconds of minutes of the time. Currently, only the value 0 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#seconds GoogleAlloydbCluster#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db904570492af176540b0e4c454f608b57f49c3a90f86c53a4d3252b99553d52)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#hours GoogleAlloydbCluster#hours}
        '''
        result = self._values.get("hours")
        assert result is not None, "Required property 'hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#minutes GoogleAlloydbCluster#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#nanos GoogleAlloydbCluster#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Currently, only the value 0 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#seconds GoogleAlloydbCluster#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1b6e840b180cdc46c4ea02d7f8791c6a29bafd181caa4c30bded2d4d79ca9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3355aeaf335131c65028f0316e11779745005532ece5f44773be1c781756386c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2831022f371f40ebdfaa0bd0a87bb619e0047a0a615f320478aa2e5100ffa197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ce2f58872ce499b55580da4a6497affa7dcbf42ac9bb8d522fcc22aff304b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e3ce011686addc8a4008eb8474bc459b2136575f60ffe188b35acc9df6c660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9363f00a8b9c5e98e6a6d7a099afa2d78bdaf206b04610446d4bd835fb32e0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterMaintenanceUpdatePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMaintenanceUpdatePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2aec9a55df18133ce022688a4409cae3e757b94ff15f49842e50fd60de34a22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaintenanceWindows")
    def put_maintenance_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec094c1488bf1142145639e7de592fe2c00c015e0df1e9a887af7d04d40a1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindows", [value]))

    @jsii.member(jsii_name="resetMaintenanceWindows")
    def reset_maintenance_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindows", []))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindows")
    def maintenance_windows(
        self,
    ) -> GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList:
        return typing.cast(GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList, jsii.get(self, "maintenanceWindows"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowsInput")
    def maintenance_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]], jsii.get(self, "maintenanceWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicy]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29051d358c8ef29cc8029ddb34a99ac065c87f5ff5f283a1631b829f04e7643d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMigrationSource",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterMigrationSource:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterMigrationSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterMigrationSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMigrationSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66edc61c225d9c9c7013a7dc2567c33c213653a268fceaf7debe4f4140cb43aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterMigrationSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bddf6452e9c02210493c8db50562afd82364fa8127459d7bbcfb3f23ba0618fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterMigrationSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61efbe775e2475af2909b978884c2478a9d32b53b60f077c8d12f942cc6a6049)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1393c18f012be66f69d22447b9f86322d8460f19c7a9e2ef6c926261fb8ca111)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12f50af29c723fedc6136e76186c8385b0cf4b64a991ab272455d30f56116595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterMigrationSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterMigrationSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da11eeb0dbaf7d56699075f5694edcabad50204e2499e69e168700e1db0bbd1)
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
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterMigrationSource]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterMigrationSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterMigrationSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1122c82b7a75bd98e8924cdc6beb482306990a6fd348744545949d9791acba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterNetworkConfig",
    jsii_struct_bases=[],
    name_mapping={"allocated_ip_range": "allocatedIpRange", "network": "network"},
)
class GoogleAlloydbClusterNetworkConfig:
    def __init__(
        self,
        *,
        allocated_ip_range: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allocated_ip_range: The name of the allocated IP range for the private IP AlloyDB cluster. For example: "google-managed-services-default". If set, the instance IPs for this cluster will be created in the allocated range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#allocated_ip_range GoogleAlloydbCluster#allocated_ip_range}
        :param network: The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP. The network must belong to the same project as the cluster. It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network GoogleAlloydbCluster#network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b73f4c2c7e7dd2c6f007a593bfed0fbd1240297c001b6af0b5ee0dc144e924a7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#allocated_ip_range GoogleAlloydbCluster#allocated_ip_range}
        '''
        result = self._values.get("allocated_ip_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The resource link for the VPC network in which cluster resources are created and from which they are accessible via Private IP.

        The network must belong to the same project as the cluster.
        It is specified in the form: "projects/{projectNumber}/global/networks/{network_id}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#network GoogleAlloydbCluster#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterNetworkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterNetworkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterNetworkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e092cae0ad3cedaeec7d87b8fa36d95dfed9ed2714b88812172dae8d8aaae21b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3549ae96a8b13e89f53fc26f515461002daa89f5ae52a6d25990a94acdaa8f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedIpRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4424dcd2415fe48afc3bfa226d9cbcad20ba7f46648c6442f8b61eeb62e189fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterNetworkConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterNetworkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterNetworkConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfebdf4b5b6292d800ae0d3c65f26b4157319a0d5aeb39b146ce0437b9794ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterPscConfig",
    jsii_struct_bases=[],
    name_mapping={"psc_enabled": "pscEnabled"},
)
class GoogleAlloydbClusterPscConfig:
    def __init__(
        self,
        *,
        psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param psc_enabled: Create an instance that allows connections from Private Service Connect endpoints to the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_enabled GoogleAlloydbCluster#psc_enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d1e72a56b5459ac52b3c4d447204cdd7b825a45047ce504356b25a8c9b8209)
            check_type(argname="argument psc_enabled", value=psc_enabled, expected_type=type_hints["psc_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if psc_enabled is not None:
            self._values["psc_enabled"] = psc_enabled

    @builtins.property
    def psc_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create an instance that allows connections from Private Service Connect endpoints to the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#psc_enabled GoogleAlloydbCluster#psc_enabled}
        '''
        result = self._values.get("psc_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65534889d63a09b661d595fde820ff1053af9023494714ba071179c63b4f88e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af62d891a70f303831526db29e18f4073485ff017cb144585238860500a913d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pscEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterPscConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterPscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567b5fb09fd37e998864adeb8378b63aa1904f5ae4b472df932f8480fb9fc45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterRestoreBackupSource",
    jsii_struct_bases=[],
    name_mapping={"backup_name": "backupName"},
)
class GoogleAlloydbClusterRestoreBackupSource:
    def __init__(self, *, backup_name: builtins.str) -> None:
        '''
        :param backup_name: The name of the backup that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_name GoogleAlloydbCluster#backup_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9351b0cc0dd539947c2cbb65968d1d3124bac756182c7290eafbf5f8900a91c4)
            check_type(argname="argument backup_name", value=backup_name, expected_type=type_hints["backup_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_name": backup_name,
        }

    @builtins.property
    def backup_name(self) -> builtins.str:
        '''The name of the backup that this cluster is restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#backup_name GoogleAlloydbCluster#backup_name}
        '''
        result = self._values.get("backup_name")
        assert result is not None, "Required property 'backup_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterRestoreBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterRestoreBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterRestoreBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0f60ed7b77057e7092af8217dc9e00b1c269953a834c04be0c4e0c70786a21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dfd39e68c35086d1d8da879377f98df0a8ca44d5dbb3d33a1f023c0051c7f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterRestoreBackupSource]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterRestoreBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterRestoreBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428812253ac22def8554576cad11e8edf0736ceb439c76c21f1f668d7f42efdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterRestoreContinuousBackupSource",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "point_in_time": "pointInTime"},
)
class GoogleAlloydbClusterRestoreContinuousBackupSource:
    def __init__(self, *, cluster: builtins.str, point_in_time: builtins.str) -> None:
        '''
        :param cluster: The name of the source cluster that this cluster is restored from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster GoogleAlloydbCluster#cluster}
        :param point_in_time: The point in time that this cluster is restored to, in RFC 3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#point_in_time GoogleAlloydbCluster#point_in_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcc6e18ea170785bdae35372a226575c61c14e7be6e79310d832eac00c3d8cd)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument point_in_time", value=point_in_time, expected_type=type_hints["point_in_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "point_in_time": point_in_time,
        }

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The name of the source cluster that this cluster is restored from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#cluster GoogleAlloydbCluster#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def point_in_time(self) -> builtins.str:
        '''The point in time that this cluster is restored to, in RFC 3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#point_in_time GoogleAlloydbCluster#point_in_time}
        '''
        result = self._values.get("point_in_time")
        assert result is not None, "Required property 'point_in_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterRestoreContinuousBackupSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterRestoreContinuousBackupSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterRestoreContinuousBackupSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef69307bcc02f1fb127501506c26c236e7a867d586791c183b6863b0fb3cd0e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14401c403e3c1fd8f661d598cd8f5e2ed23af83a6825870848d5cece76222145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTime")
    def point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTime"))

    @point_in_time.setter
    def point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a1cd60c1efdf3945d424e95ee0ae26ec5578114ebeed60370d5d2fdbcd0076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleAlloydbClusterRestoreContinuousBackupSource]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterRestoreContinuousBackupSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterRestoreContinuousBackupSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bfdf6c7159541b1ad0552eed553aa8f982c57053ecdf0dc5a4604a069ab6d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterSecondaryConfig",
    jsii_struct_bases=[],
    name_mapping={"primary_cluster_name": "primaryClusterName"},
)
class GoogleAlloydbClusterSecondaryConfig:
    def __init__(self, *, primary_cluster_name: builtins.str) -> None:
        '''
        :param primary_cluster_name: Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#primary_cluster_name GoogleAlloydbCluster#primary_cluster_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07e0f798a22ddd2cf1cd48e80604b56751760543dfcf657c15f28ff55bb2ce2)
            check_type(argname="argument primary_cluster_name", value=primary_cluster_name, expected_type=type_hints["primary_cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "primary_cluster_name": primary_cluster_name,
        }

    @builtins.property
    def primary_cluster_name(self) -> builtins.str:
        '''Name of the primary cluster must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#primary_cluster_name GoogleAlloydbCluster#primary_cluster_name}
        '''
        result = self._values.get("primary_cluster_name")
        assert result is not None, "Required property 'primary_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterSecondaryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterSecondaryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterSecondaryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f9393c9cb854ae13def52003512559d338d9832bc9c0fbd043d148b8dc1e05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b1dcff3ec3caf2e05ef738a613b314ea3b14d24bb62f51a5186216db9102cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryClusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterSecondaryConfig]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterSecondaryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterSecondaryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a109cf915101b8955b3307d1d1e48c0fbc0b5b45acc8aaefb03ad259ede2db7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleAlloydbClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#create GoogleAlloydbCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#delete GoogleAlloydbCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#update GoogleAlloydbCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc9f589fc75a5ae9b9ad5595a341aace357c4e7cb123df3948774c01fddf483)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#create GoogleAlloydbCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#delete GoogleAlloydbCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_alloydb_cluster#update GoogleAlloydbCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1f7066df60d3a6d7d9eba417b6b182c7d2780bc219dba4eecbd7c9f9edc023)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21d71bf8df21c9354dd28dc4b2cb2f4c411400b927c255276cbf19de43655cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63160ad80a64d1b1f4cf42951b982fa97d1da796a98c0d47ff7c42722b5991f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db11d3f69b95b71bde392b377a7bb955a7abd449f7fd02b387a3f6e75f145d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8050ae0357948add71a3cbd3b87f40442377e7c99acf20f8577f36ebd5eeae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterTrialMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleAlloydbClusterTrialMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleAlloydbClusterTrialMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleAlloydbClusterTrialMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterTrialMetadataList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e6868582e5cbdc62b9fea2d5d2d814f14c7f6d5703cfff3c52c23ec8a56616)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleAlloydbClusterTrialMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a19e6c949864e524766c9c7d604f53f74786df71cfc461bbeae38a4b1a33316)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleAlloydbClusterTrialMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ef3f25e065e6fd289d15a48056e87bf48a7d3d37c260326d6f542b2ae94d4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b7c14d5d4b797d83a1ce7a3babd9d1e1af80784f3aac2837ec634732b7f24d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8329099f7705db1c2a8b0560d427191e4d17c0326e521c96253d68b091fc6021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleAlloydbClusterTrialMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleAlloydbCluster.GoogleAlloydbClusterTrialMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__485b4cd50eb4e153752005ab223ebda77aa93fc7ab01c8e9c2b5633203c68aa8)
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
    def internal_value(self) -> typing.Optional[GoogleAlloydbClusterTrialMetadata]:
        return typing.cast(typing.Optional[GoogleAlloydbClusterTrialMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleAlloydbClusterTrialMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f24ceabd5354b58fad32079dd243f185cef242c197276d3f5951bfe28676f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleAlloydbCluster",
    "GoogleAlloydbClusterAutomatedBackupPolicy",
    "GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig",
    "GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfigOutputReference",
    "GoogleAlloydbClusterAutomatedBackupPolicyOutputReference",
    "GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention",
    "GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetentionOutputReference",
    "GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention",
    "GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetentionOutputReference",
    "GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule",
    "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleOutputReference",
    "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes",
    "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesList",
    "GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimesOutputReference",
    "GoogleAlloydbClusterBackupSource",
    "GoogleAlloydbClusterBackupSourceList",
    "GoogleAlloydbClusterBackupSourceOutputReference",
    "GoogleAlloydbClusterConfig",
    "GoogleAlloydbClusterContinuousBackupConfig",
    "GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig",
    "GoogleAlloydbClusterContinuousBackupConfigEncryptionConfigOutputReference",
    "GoogleAlloydbClusterContinuousBackupConfigOutputReference",
    "GoogleAlloydbClusterContinuousBackupInfo",
    "GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo",
    "GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoList",
    "GoogleAlloydbClusterContinuousBackupInfoEncryptionInfoOutputReference",
    "GoogleAlloydbClusterContinuousBackupInfoList",
    "GoogleAlloydbClusterContinuousBackupInfoOutputReference",
    "GoogleAlloydbClusterEncryptionConfig",
    "GoogleAlloydbClusterEncryptionConfigOutputReference",
    "GoogleAlloydbClusterEncryptionInfo",
    "GoogleAlloydbClusterEncryptionInfoList",
    "GoogleAlloydbClusterEncryptionInfoOutputReference",
    "GoogleAlloydbClusterInitialUser",
    "GoogleAlloydbClusterInitialUserOutputReference",
    "GoogleAlloydbClusterMaintenanceUpdatePolicy",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsList",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsOutputReference",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTimeOutputReference",
    "GoogleAlloydbClusterMaintenanceUpdatePolicyOutputReference",
    "GoogleAlloydbClusterMigrationSource",
    "GoogleAlloydbClusterMigrationSourceList",
    "GoogleAlloydbClusterMigrationSourceOutputReference",
    "GoogleAlloydbClusterNetworkConfig",
    "GoogleAlloydbClusterNetworkConfigOutputReference",
    "GoogleAlloydbClusterPscConfig",
    "GoogleAlloydbClusterPscConfigOutputReference",
    "GoogleAlloydbClusterRestoreBackupSource",
    "GoogleAlloydbClusterRestoreBackupSourceOutputReference",
    "GoogleAlloydbClusterRestoreContinuousBackupSource",
    "GoogleAlloydbClusterRestoreContinuousBackupSourceOutputReference",
    "GoogleAlloydbClusterSecondaryConfig",
    "GoogleAlloydbClusterSecondaryConfigOutputReference",
    "GoogleAlloydbClusterTimeouts",
    "GoogleAlloydbClusterTimeoutsOutputReference",
    "GoogleAlloydbClusterTrialMetadata",
    "GoogleAlloydbClusterTrialMetadataList",
    "GoogleAlloydbClusterTrialMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__3db65a27640e86cadf9ccf9a5d2f732bed2f44bd2ccdf2c3cec616e30382915d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    location: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    automated_backup_policy: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    continuous_backup_config: typing.Optional[typing.Union[GoogleAlloydbClusterContinuousBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_version: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[GoogleAlloydbClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_user: typing.Optional[typing.Union[GoogleAlloydbClusterInitialUser, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_update_policy: typing.Optional[typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleAlloydbClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[GoogleAlloydbClusterPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_source: typing.Optional[typing.Union[GoogleAlloydbClusterRestoreBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_continuous_backup_source: typing.Optional[typing.Union[GoogleAlloydbClusterRestoreContinuousBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_config: typing.Optional[typing.Union[GoogleAlloydbClusterSecondaryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAlloydbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__dc74511c620f0a9a20993ea32b9e5a8dcfc678297407f8d90de68e129348d744(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b6a5ad9fa85a9489d173232ed64c1dd00475a219064adc6753a86fb364b291(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a7620f01240d2ba7aa7fb236ff97100160a02d010e3f5d00b695373dc1e317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787e13ee492d3903ec95a3ea9594b35d24cd4479724d8e1a3e8c9359c171ed70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acdd71b570c5e9144054a0604cd3165b4aa3901e7d05ce66e6d1c73991b73bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f861d1925127d7abfbb38f9cabd38538b4ed79d1e9d2004de739f111f20558d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a882d681d627d0f7f4bcc496a2e0f9c3851ee56b82ed077d11c8bb501e5db6a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e002dc26d8425bbcda7b87369f5e6f772fc66260fb691cf16cbd0cfe5cb68c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b842cc9829af11ec72fd1ece428b2600da3d949ac5226ad3f43da1fb87a3375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2306f18dfa639a28a7ec00d8e7b57995734caff0969a353b30cc544450005a15(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2646a147d141c8f146a4e875db4dbfbc4cf4755c5337e26d00b73005a42ed32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c78536b9fbd0c48d1db02e8d3daf5481063e0cd8f8a0705035b10e164d111bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e631ea42970e9b5f03fdd590ecea3f9bb5ce6451e9a9bc4b9a2fba9a4a6b66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2765a979255317cb68005382c21a84e3cea817e8a178262cf8b7054db392f450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3da0e06e22c95b0d03456da3c707825aba3e76ede46f22a30a5fe722c174c33(
    *,
    backup_window: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    quantity_based_retention: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    time_based_retention: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    weekly_schedule: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad549652af7f536259d75dab386c7ad4d799adca246c1cf0608b17e38231b35(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83c8a30518470242d8e15c4cdfa04ebd8f975b5a5d2e456f02803d1125fc4f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1f0da605e9f573c9a8c6c82a8d04a319d8a600a31b194edd2eb9cf29c2465b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03936fc1d319f0df372ba453c9c25953fdc2bfbeabd8bd0652f58732e76e8c24(
    value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab2db6a8cb5a98f96e21df83dc612c6fbc9cc0cb2405aff3eedfc656fce1bbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d68daf9345c94f5a8bf390ee5771c377eb63e2f585b0fdec0f08d280c1e3c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b28aae1364d26f93e610d6d45463a302021ee1c111517adf9d656218cd17972(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7769f56e282ca50ff96b87f6d5e99cf8e4f296000329f1e1ac8d035eee22b4d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ac33ea7a39572987a92d27445b30daf0072a63bae1cc257f4b06111a2077d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b421f85dc33344842f722f47d816cde9650adf9d08dd911bd35d8bbfd7793e(
    value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d380605aadc72361bd69bc3971e0ff2149a0c331fbb63facaaf4684929a7d2e9(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ac4f456fc6e62fb682a239c2138b8d1647802451ed776811ccd8bccd4363e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b46797f7b67c6cdf55318feec865f926e8a743b1eab77219cbdead27b17821(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f316c885fb77529e82947887b50c8877a10b4e8499e0437bd68f9aa337059a(
    value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyQuantityBasedRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b168068dd37391716c4d0f8899c38bf6a7328cbc6e36a90cd5167549f7b6138b(
    *,
    retention_period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c8ea99c158aa375445175547fd771359e407e1d42774d293747edabd0d6194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db1f2a66375a2a1d84796811b6db17046fa777eba1f90e6c384f273cf8dff35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc3437cf89e187d65679baffb096c943dedeb1b150097e277c2d2be0ed4bbf4(
    value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyTimeBasedRetention],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733a37b2b059f2f44ff196160fc6347d76b6803ba3753de096ba22e65f242890(
    *,
    start_times: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes, typing.Dict[builtins.str, typing.Any]]]],
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef267acd2437ef250cd68eaf958576018dcf5c8aa451d33b4aa258bf382bdd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec5a11ab67ecec77b94b074f713f8a834e01ca88c97a6621b36a4fd7495664e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220d49d3f35abaeffd2e3ba838bd7ce17a0d4f517dd9b4acf723c59ef3ec8820(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d26827086ce29c58545d1c0e99b0557b81863283084ce34f5d885ab111b3324(
    value: typing.Optional[GoogleAlloydbClusterAutomatedBackupPolicyWeeklySchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55636ca490f44ef49772449712b9fa758f92ede4e43aed580446ab072e99f50(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7df070ced58ee5837f77cbe65bbe045e3c9052ae62f047049f3ec0c52db32d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8c8eb09c83595da8215d161ba88a4a5ffa7bfdff65bdf33b4c7c5bd0bb639f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d31427526488a4ac1c5ef3d707337e44863c90911ab2b0f3bd975b09b0f9ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6febb310895f75a7569933450b6c3a19488f9c4aa34cac207f5858fe30625(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454c34abac78f9d1b3e7d8712cb58777dfce77af71e97ae2d5a1708652be4b28(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2600d24a725b43f26219f48c626ea93dbc75618c1d406ba6bc98be4bf383487(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882d45a0efd08dd1de84095b26d29f475d38f572d14e467cb68db1255844663b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2a250285e3509188c7b3b102dd69b9711a5844f988b55e021ea0fd8c4c3021(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79eb4716560402825b3d80daa53b9caedf2e8ad5d204849d3deaf1176891a22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2ea0c0f8974d283a714c728e078d37b865b9b0398eb33f5abaf72bc0d71af1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd01f2e68e3e1b741bf5e4a509891470acbd1ad97b819eeeb61d9a781c6d7da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8125f9e039e46e2fbd9d98fab6b5fb97b849e29499607750f154eec87e97c5c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterAutomatedBackupPolicyWeeklyScheduleStartTimes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff6aba4da0f4406b1d4a5addcf2be30b63cb8f58143b21a9d6f16a473f2e8be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0872998ce951c74ebcea2082fceb1a73755c6af09bc14fe25fd46cfaf291eb8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5657fc0b07766da1a57bf5a8a1f7e73e46d5b627079bfe5b51c5cd99f242f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f76e74c36b9eec0369db2f4f8d6d15a924c46947d19a8ea8191ecd0804bf1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf28f3abf25f1697336324f754a10616ba3417985862edf7fec2c2ed766c3f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f033de15b75cb7a4a0bf2295181856dfa78d5ff6d687510092eb0f5a7a78b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92df2119583f7820be86b23a525de4d20175b4ad6cb2200f1a9c98e6e894df74(
    value: typing.Optional[GoogleAlloydbClusterBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fbe21be7436ddeb4b208a6660791ff03b76ae3d6303805f56a61810cd66694(
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
    automated_backup_policy: typing.Optional[typing.Union[GoogleAlloydbClusterAutomatedBackupPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    continuous_backup_config: typing.Optional[typing.Union[GoogleAlloydbClusterContinuousBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    database_version: typing.Optional[builtins.str] = None,
    deletion_policy: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[GoogleAlloydbClusterEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initial_user: typing.Optional[typing.Union[GoogleAlloydbClusterInitialUser, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maintenance_update_policy: typing.Optional[typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    network_config: typing.Optional[typing.Union[GoogleAlloydbClusterNetworkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[GoogleAlloydbClusterPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_backup_source: typing.Optional[typing.Union[GoogleAlloydbClusterRestoreBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    restore_continuous_backup_source: typing.Optional[typing.Union[GoogleAlloydbClusterRestoreContinuousBackupSource, typing.Dict[builtins.str, typing.Any]]] = None,
    secondary_config: typing.Optional[typing.Union[GoogleAlloydbClusterSecondaryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    skip_await_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleAlloydbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b327a1ca6300f1b0d19ee99ffad88368e21fb90bb8bc6763297f55402535529(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_window_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788f0ec21185476d6f132d7ca1454d29eff662a9b5392937b2fc7a7431583f1f(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ca868bf0677e564c65712b82001045ccebde024d5b50aa85079f36d98257a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433510c820c87fb93625ee96865e219533e463fda249c419ae186f1c00e31614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31400fdad8281a70b0fceacd2d597845b1fdd5f37178d52966ff3916407d55ed(
    value: typing.Optional[GoogleAlloydbClusterContinuousBackupConfigEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d3d1e243062c2e906dcf9f04e164d598f4521094a9a8c0b88d4ed64a3dcf1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456b3008ee008197f46e32afc5e8471b799024b81027e83f1357e6c793661772(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d370032addf72cf2744edf3b56c78309d844da75b983045688f8f777378a06d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce69f233c784670be5e37ec145eb52eabf68c5c218968dfc99e5cf0380bb691(
    value: typing.Optional[GoogleAlloydbClusterContinuousBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb4022ae0a04dd73db2fc8389ca769f25e1e6e40e130550339eb4db436acba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad506bfa32cd9813bc9b467215980e03a8013a9d813b72338bafd399ef4bf6cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4b4f531276fbf60773c42311404526087ecd163a773b53b7d539fe3e6803c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1ad2bdc4f63808a243c2e12c2f77fcbc839b18f314b6fc6b17c28c403490a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2af788d788d8379a5c20b7f00942af0de89743db3fd8616dbd39ac66559f2c8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067aea8770f7f3c4b0f724a1ef0997b5464bc40b6a62c55de1ab83dc6ccb058e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be62a727ce31a6cee7bc2d6eb2c113870c6ce86dc07f20816369e8bb5ffbb61(
    value: typing.Optional[GoogleAlloydbClusterContinuousBackupInfoEncryptionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4408bd0d37aabbf08162776eba834db7f93df18ff88b3ad3fc3eb7b34243cc1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123689370e62c4cd4926e319c74915816088144e3487d2187aacc6d01ceedff1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503f54cd4a8276b269cee5515dc7a6ef303127cc96f3d426ec55b89dc1352482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9f76085d510be67af42ac73f90ea3d86d7a76b9769723d7f138bb41c475daa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494d9a1bcd22d3ac64c13f502b7e03daede9dccdbd2129d871edefb18543722c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200fe6d82ea47a018be70f9c937fc6c8ecf8cfb7f74b2be1775a27a53d2a6a07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deddf95d0a7af74cdb3eb08c3c3f41c50ab68410ac662faf1b0859f08df0a946(
    value: typing.Optional[GoogleAlloydbClusterContinuousBackupInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6994e48e54ff2b9ca317808e2c0e7efc87c70029c476648484b4a0266f71ea9d(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7029fc6ff3ad5003ef4cd1deaa5e24a4c17795e7deb68dece4487a64ecbf53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c896d7370935984bb78c20e0129678a54e67eb159d9e1c47cd1cda4ef48209c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12abf09d1ec65184e481a83f4d35ba08dd969b0590e8ca98606655420376724(
    value: typing.Optional[GoogleAlloydbClusterEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e458073409d2117540252c72ab32a671a1155d43d012bdd48cba389a88cdf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe02cbddb6495b6f8c3c2fb90e82cc5078840631d04ab5f7b3c982f48c288eb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c3d0650964210923bed0547923dac416e355b0c0bbc487291c7805fd1a0c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6dd133b546820621ba291a2dc62b88340f8194da01d8f9cede6cfa2e37e909(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd260299fe1bd3ac971b02761f563d753e0601133d31d99589a7867c1899a55d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7b0527ed0ee850e5d06a591411135720c7fce3cef7b199f31d6987af163f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c65f5e686f5c5014ac38bb3b22a96c8f71396fbb58abb9588c59887e9fe1b5(
    value: typing.Optional[GoogleAlloydbClusterEncryptionInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1112959200f4c6a14d4f3185120f30764f95b83fb8bc3959906a6fef0b75a049(
    *,
    password: builtins.str,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e850851a4012c4472f36665321bf2e46df8ab26a57aa1cbc49abe0199721236b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533782a8de237a3361afc14cf00062009106935850a963f89e626954afc4e45e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1787ec10196ad222103da783265e5439845d7c50255d3a2f869b23eb7be04190(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac5d1eeb81dc8799366769a3207a199da187838208da24c8fe5d10885b5a09c(
    value: typing.Optional[GoogleAlloydbClusterInitialUser],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb1eff2012f9ed67f19955e9b6cc22b73b006a4bf63aca24e16223a64b68774(
    *,
    maintenance_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8debbf5550ad1f1e0ab0b37929f7aab9f2ef9810b950c25ac344b1429b775db(
    *,
    day: builtins.str,
    start_time: typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7df89afc4420b057460dfccc08126fd7191459a99d2522478598e1f5c79cbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321adc16b7c57585d8f1996ec233af5802bd951ee0337e94aa66a72bbb85c850(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69eb142ca446494b37a19280d9332687be7624becae9453395f2b64f33a8770(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f86d7e416c1d294de75c7262c89294260127bd83156b0ebe870f72e26163ec8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ddba3541ef0cbdfd2b2ad9a73f31077a21d602cd9ba6122d8a9846b7bdc18c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179b962e57538e6e4c2795b70ecbc80f5ce06dce60c7641a6a0a88f8b485440d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca647e62c53add2a8fd2e9b178e7115f4e269b8b0549f2e4c1f06d7eb15312c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8437113010253270c541de41b7401fcbfd1f69144f2f86b30ec83b58a2acfc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41ea56b45206cfe14acb5e7afa2d0a4fc83eb8b286f13f0bdd84d573e691c10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db904570492af176540b0e4c454f608b57f49c3a90f86c53a4d3252b99553d52(
    *,
    hours: jsii.Number,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1b6e840b180cdc46c4ea02d7f8791c6a29bafd181caa4c30bded2d4d79ca9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3355aeaf335131c65028f0316e11779745005532ece5f44773be1c781756386c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2831022f371f40ebdfaa0bd0a87bb619e0047a0a615f320478aa2e5100ffa197(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ce2f58872ce499b55580da4a6497affa7dcbf42ac9bb8d522fcc22aff304b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e3ce011686addc8a4008eb8474bc459b2136575f60ffe188b35acc9df6c660(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9363f00a8b9c5e98e6a6d7a099afa2d78bdaf206b04610446d4bd835fb32e0f5(
    value: typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aec9a55df18133ce022688a4409cae3e757b94ff15f49842e50fd60de34a22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec094c1488bf1142145639e7de592fe2c00c015e0df1e9a887af7d04d40a1be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleAlloydbClusterMaintenanceUpdatePolicyMaintenanceWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29051d358c8ef29cc8029ddb34a99ac065c87f5ff5f283a1631b829f04e7643d(
    value: typing.Optional[GoogleAlloydbClusterMaintenanceUpdatePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66edc61c225d9c9c7013a7dc2567c33c213653a268fceaf7debe4f4140cb43aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bddf6452e9c02210493c8db50562afd82364fa8127459d7bbcfb3f23ba0618fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61efbe775e2475af2909b978884c2478a9d32b53b60f077c8d12f942cc6a6049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1393c18f012be66f69d22447b9f86322d8460f19c7a9e2ef6c926261fb8ca111(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f50af29c723fedc6136e76186c8385b0cf4b64a991ab272455d30f56116595(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da11eeb0dbaf7d56699075f5694edcabad50204e2499e69e168700e1db0bbd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1122c82b7a75bd98e8924cdc6beb482306990a6fd348744545949d9791acba(
    value: typing.Optional[GoogleAlloydbClusterMigrationSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73f4c2c7e7dd2c6f007a593bfed0fbd1240297c001b6af0b5ee0dc144e924a7(
    *,
    allocated_ip_range: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e092cae0ad3cedaeec7d87b8fa36d95dfed9ed2714b88812172dae8d8aaae21b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3549ae96a8b13e89f53fc26f515461002daa89f5ae52a6d25990a94acdaa8f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4424dcd2415fe48afc3bfa226d9cbcad20ba7f46648c6442f8b61eeb62e189fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfebdf4b5b6292d800ae0d3c65f26b4157319a0d5aeb39b146ce0437b9794ee4(
    value: typing.Optional[GoogleAlloydbClusterNetworkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d1e72a56b5459ac52b3c4d447204cdd7b825a45047ce504356b25a8c9b8209(
    *,
    psc_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65534889d63a09b661d595fde820ff1053af9023494714ba071179c63b4f88e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af62d891a70f303831526db29e18f4073485ff017cb144585238860500a913d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b5fb09fd37e998864adeb8378b63aa1904f5ae4b472df932f8480fb9fc45b(
    value: typing.Optional[GoogleAlloydbClusterPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9351b0cc0dd539947c2cbb65968d1d3124bac756182c7290eafbf5f8900a91c4(
    *,
    backup_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0f60ed7b77057e7092af8217dc9e00b1c269953a834c04be0c4e0c70786a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfd39e68c35086d1d8da879377f98df0a8ca44d5dbb3d33a1f023c0051c7f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428812253ac22def8554576cad11e8edf0736ceb439c76c21f1f668d7f42efdb(
    value: typing.Optional[GoogleAlloydbClusterRestoreBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcc6e18ea170785bdae35372a226575c61c14e7be6e79310d832eac00c3d8cd(
    *,
    cluster: builtins.str,
    point_in_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef69307bcc02f1fb127501506c26c236e7a867d586791c183b6863b0fb3cd0e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14401c403e3c1fd8f661d598cd8f5e2ed23af83a6825870848d5cece76222145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a1cd60c1efdf3945d424e95ee0ae26ec5578114ebeed60370d5d2fdbcd0076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfdf6c7159541b1ad0552eed553aa8f982c57053ecdf0dc5a4604a069ab6d73(
    value: typing.Optional[GoogleAlloydbClusterRestoreContinuousBackupSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07e0f798a22ddd2cf1cd48e80604b56751760543dfcf657c15f28ff55bb2ce2(
    *,
    primary_cluster_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f9393c9cb854ae13def52003512559d338d9832bc9c0fbd043d148b8dc1e05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1dcff3ec3caf2e05ef738a613b314ea3b14d24bb62f51a5186216db9102cf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a109cf915101b8955b3307d1d1e48c0fbc0b5b45acc8aaefb03ad259ede2db7c(
    value: typing.Optional[GoogleAlloydbClusterSecondaryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc9f589fc75a5ae9b9ad5595a341aace357c4e7cb123df3948774c01fddf483(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1f7066df60d3a6d7d9eba417b6b182c7d2780bc219dba4eecbd7c9f9edc023(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d71bf8df21c9354dd28dc4b2cb2f4c411400b927c255276cbf19de43655cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63160ad80a64d1b1f4cf42951b982fa97d1da796a98c0d47ff7c42722b5991f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db11d3f69b95b71bde392b377a7bb955a7abd449f7fd02b387a3f6e75f145d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8050ae0357948add71a3cbd3b87f40442377e7c99acf20f8577f36ebd5eeae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleAlloydbClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e6868582e5cbdc62b9fea2d5d2d814f14c7f6d5703cfff3c52c23ec8a56616(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a19e6c949864e524766c9c7d604f53f74786df71cfc461bbeae38a4b1a33316(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ef3f25e065e6fd289d15a48056e87bf48a7d3d37c260326d6f542b2ae94d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b7c14d5d4b797d83a1ce7a3babd9d1e1af80784f3aac2837ec634732b7f24d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8329099f7705db1c2a8b0560d427191e4d17c0326e521c96253d68b091fc6021(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485b4cd50eb4e153752005ab223ebda77aa93fc7ab01c8e9c2b5633203c68aa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f24ceabd5354b58fad32079dd243f185cef242c197276d3f5951bfe28676f9(
    value: typing.Optional[GoogleAlloydbClusterTrialMetadata],
) -> None:
    """Type checking stubs"""
    pass

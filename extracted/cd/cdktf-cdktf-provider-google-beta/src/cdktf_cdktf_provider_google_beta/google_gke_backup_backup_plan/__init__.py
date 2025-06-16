r'''
# `google_gke_backup_backup_plan`

Refer to the Terraform Registry for docs: [`google_gke_backup_backup_plan`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan).
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


class GoogleGkeBackupBackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan google_gke_backup_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backup_config: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_schedule: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan google_gke_backup_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: The source cluster from which Backups will be created via this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cluster GoogleGkeBackupBackupPlan#cluster}
        :param location: The region of the Backup Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#location GoogleGkeBackupBackupPlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#name GoogleGkeBackupBackupPlan#name}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_config GoogleGkeBackupBackupPlan#backup_config}
        :param backup_schedule: backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_schedule GoogleGkeBackupBackupPlan#backup_schedule}
        :param deactivated: This flag indicates whether this BackupPlan has been deactivated. Setting this field to True locks the BackupPlan such that no further updates will be allowed (except deletes), including the deactivated field itself. It also prevents any new Backups from being created via this BackupPlan (including scheduled Backups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#deactivated GoogleGkeBackupBackupPlan#deactivated}
        :param description: User specified descriptive string for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#description GoogleGkeBackupBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#id GoogleGkeBackupBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#labels GoogleGkeBackupBackupPlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#project GoogleGkeBackupBackupPlan#project}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#retention_policy GoogleGkeBackupBackupPlan#retention_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#timeouts GoogleGkeBackupBackupPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0c8dc89ae7cfe2387c009df7f0d84dd1dfb69cca04d41b6370a7bc1eddf676)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeBackupBackupPlanConfig(
            cluster=cluster,
            location=location,
            name=name,
            backup_config=backup_config,
            backup_schedule=backup_schedule,
            deactivated=deactivated,
            description=description,
            id=id,
            labels=labels,
            project=project,
            retention_policy=retention_policy,
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
        '''Generates CDKTF code for importing a GoogleGkeBackupBackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeBackupBackupPlan to import.
        :param import_from_id: The id of the existing GoogleGkeBackupBackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeBackupBackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b6080c001753b4794284feeb086fb35a17857976918a4ad4082127ec6035a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupConfig")
    def put_backup_config(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_applications: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, include all namespaced resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#all_namespaces GoogleGkeBackupBackupPlan#all_namespaces}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#encryption_key GoogleGkeBackupBackupPlan#encryption_key}
        :param include_secrets: This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_secrets GoogleGkeBackupBackupPlan#include_secrets}
        :param include_volume_data: This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_volume_data GoogleGkeBackupBackupPlan#include_volume_data}
        :param permissive_mode: This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#permissive_mode GoogleGkeBackupBackupPlan#permissive_mode}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_applications GoogleGkeBackupBackupPlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_namespaces GoogleGkeBackupBackupPlan#selected_namespaces}
        '''
        value = GoogleGkeBackupBackupPlanBackupConfig(
            all_namespaces=all_namespaces,
            encryption_key=encryption_key,
            include_secrets=include_secrets,
            include_volume_data=include_volume_data,
            permissive_mode=permissive_mode,
            selected_applications=selected_applications,
            selected_namespaces=selected_namespaces,
        )

        return typing.cast(None, jsii.invoke(self, "putBackupConfig", [value]))

    @jsii.member(jsii_name="putBackupSchedule")
    def put_backup_schedule(
        self,
        *,
        cron_schedule: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rpo_config: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_schedule: A standard cron string that defines a repeating schedule for creating Backups via this BackupPlan. This is mutually exclusive with the rpoConfig field since at most one schedule can be defined for a BackupPlan. If this is defined, then backupRetainDays must also be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cron_schedule GoogleGkeBackupBackupPlan#cron_schedule}
        :param paused: This flag denotes whether automatic Backup creation is paused for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#paused GoogleGkeBackupBackupPlan#paused}
        :param rpo_config: rpo_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#rpo_config GoogleGkeBackupBackupPlan#rpo_config}
        '''
        value = GoogleGkeBackupBackupPlanBackupSchedule(
            cron_schedule=cron_schedule, paused=paused, rpo_config=rpo_config
        )

        return typing.cast(None, jsii.invoke(self, "putBackupSchedule", [value]))

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        backup_delete_lock_days: typing.Optional[jsii.Number] = None,
        backup_retain_days: typing.Optional[jsii.Number] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_delete_lock_days: Minimum age for a Backup created via this BackupPlan (in days). Must be an integer value between 0-90 (inclusive). A Backup created under this BackupPlan will not be deletable until it reaches Backup's (create time + backup_delete_lock_days). Updating this field of a BackupPlan does not affect existing Backups. Backups created after a successful update will inherit this new value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_delete_lock_days GoogleGkeBackupBackupPlan#backup_delete_lock_days}
        :param backup_retain_days: The default maximum age of a Backup created via this BackupPlan. This field MUST be an integer value >= 0 and <= 365. If specified, a Backup created under this BackupPlan will be automatically deleted after its age reaches (createTime + backupRetainDays). If not specified, Backups created under this BackupPlan will NOT be subject to automatic deletion. Updating this field does NOT affect existing Backups under it. Backups created AFTER a successful update will automatically pick up the new value. NOTE: backupRetainDays must be >= backupDeleteLockDays. If cronSchedule is defined, then this must be <= 360 * the creation interval. If rpo_config is defined, then this must be <= 360 * targetRpoMinutes/(1440minutes/day) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_retain_days GoogleGkeBackupBackupPlan#backup_retain_days}
        :param locked: This flag denotes whether the retention policy of this BackupPlan is locked. If set to True, no further update is allowed on this policy, including the locked field itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#locked GoogleGkeBackupBackupPlan#locked}
        '''
        value = GoogleGkeBackupBackupPlanRetentionPolicy(
            backup_delete_lock_days=backup_delete_lock_days,
            backup_retain_days=backup_retain_days,
            locked=locked,
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#create GoogleGkeBackupBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#delete GoogleGkeBackupBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#update GoogleGkeBackupBackupPlan#update}.
        '''
        value = GoogleGkeBackupBackupPlanTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackupConfig")
    def reset_backup_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupConfig", []))

    @jsii.member(jsii_name="resetBackupSchedule")
    def reset_backup_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupSchedule", []))

    @jsii.member(jsii_name="resetDeactivated")
    def reset_deactivated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeactivated", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

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
    @jsii.member(jsii_name="backupConfig")
    def backup_config(self) -> "GoogleGkeBackupBackupPlanBackupConfigOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupConfigOutputReference", jsii.get(self, "backupConfig"))

    @builtins.property
    @jsii.member(jsii_name="backupSchedule")
    def backup_schedule(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleOutputReference", jsii.get(self, "backupSchedule"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="protectedPodCount")
    def protected_pod_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protectedPodCount"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "GoogleGkeBackupBackupPlanRetentionPolicyOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateReason")
    def state_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateReason"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeBackupBackupPlanTimeoutsOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="backupConfigInput")
    def backup_config_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfig"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfig"], jsii.get(self, "backupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="backupScheduleInput")
    def backup_schedule_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupSchedule"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupSchedule"], jsii.get(self, "backupScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="deactivatedInput")
    def deactivated_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deactivatedInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanRetentionPolicy"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeBackupBackupPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeBackupBackupPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b783dee6d1562cd4388e0a330836d4605150ae79090e6836f9f07c9a4905eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deactivated")
    def deactivated(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deactivated"))

    @deactivated.setter
    def deactivated(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9218ab617d846612494663ad6460905f6c3a8b4514513e55127f9052b1eaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deactivated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee372e1e6d403f4c9488423b80bd78d819d6b87374291ac95d67405b3f2083a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__410df59a1d306c112cf4939712fbc8529b626a8c205a19ba463ad9315b17a2c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f69b3996ad9a0e656cc34a1b166997ef3641e56756e3bab647d57418d333f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3afbd74e007f2b2c3da96fd5741e2bacf1c084bb71335c1ebc6277462d61c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194eec322da177abe3875c94f0da81dd94f487fe3997a8e4f901e7d5f6aca677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b193a5059b8b106ca1ce4a0593aaeb6143fed086bacb4663fc0d3999630fffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "all_namespaces": "allNamespaces",
        "encryption_key": "encryptionKey",
        "include_secrets": "includeSecrets",
        "include_volume_data": "includeVolumeData",
        "permissive_mode": "permissiveMode",
        "selected_applications": "selectedApplications",
        "selected_namespaces": "selectedNamespaces",
    },
)
class GoogleGkeBackupBackupPlanBackupConfig:
    def __init__(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_applications: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, include all namespaced resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#all_namespaces GoogleGkeBackupBackupPlan#all_namespaces}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#encryption_key GoogleGkeBackupBackupPlan#encryption_key}
        :param include_secrets: This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_secrets GoogleGkeBackupBackupPlan#include_secrets}
        :param include_volume_data: This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_volume_data GoogleGkeBackupBackupPlan#include_volume_data}
        :param permissive_mode: This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#permissive_mode GoogleGkeBackupBackupPlan#permissive_mode}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_applications GoogleGkeBackupBackupPlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_namespaces GoogleGkeBackupBackupPlan#selected_namespaces}
        '''
        if isinstance(encryption_key, dict):
            encryption_key = GoogleGkeBackupBackupPlanBackupConfigEncryptionKey(**encryption_key)
        if isinstance(selected_applications, dict):
            selected_applications = GoogleGkeBackupBackupPlanBackupConfigSelectedApplications(**selected_applications)
        if isinstance(selected_namespaces, dict):
            selected_namespaces = GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces(**selected_namespaces)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ccac3b296215dcb721ce539fb906c1ee30ef6d296f4b595e76be407879443e)
            check_type(argname="argument all_namespaces", value=all_namespaces, expected_type=type_hints["all_namespaces"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument include_secrets", value=include_secrets, expected_type=type_hints["include_secrets"])
            check_type(argname="argument include_volume_data", value=include_volume_data, expected_type=type_hints["include_volume_data"])
            check_type(argname="argument permissive_mode", value=permissive_mode, expected_type=type_hints["permissive_mode"])
            check_type(argname="argument selected_applications", value=selected_applications, expected_type=type_hints["selected_applications"])
            check_type(argname="argument selected_namespaces", value=selected_namespaces, expected_type=type_hints["selected_namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_namespaces is not None:
            self._values["all_namespaces"] = all_namespaces
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if include_secrets is not None:
            self._values["include_secrets"] = include_secrets
        if include_volume_data is not None:
            self._values["include_volume_data"] = include_volume_data
        if permissive_mode is not None:
            self._values["permissive_mode"] = permissive_mode
        if selected_applications is not None:
            self._values["selected_applications"] = selected_applications
        if selected_namespaces is not None:
            self._values["selected_namespaces"] = selected_namespaces

    @builtins.property
    def all_namespaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, include all namespaced resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#all_namespaces GoogleGkeBackupBackupPlan#all_namespaces}
        '''
        result = self._values.get("all_namespaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfigEncryptionKey"]:
        '''encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#encryption_key GoogleGkeBackupBackupPlan#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfigEncryptionKey"], result)

    @builtins.property
    def include_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_secrets GoogleGkeBackupBackupPlan#include_secrets}
        '''
        result = self._values.get("include_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_volume_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#include_volume_data GoogleGkeBackupBackupPlan#include_volume_data}
        '''
        result = self._values.get("include_volume_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissive_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#permissive_mode GoogleGkeBackupBackupPlan#permissive_mode}
        '''
        result = self._values.get("permissive_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selected_applications(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications"]:
        '''selected_applications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_applications GoogleGkeBackupBackupPlan#selected_applications}
        '''
        result = self._values.get("selected_applications")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications"], result)

    @builtins.property
    def selected_namespaces(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces"]:
        '''selected_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#selected_namespaces GoogleGkeBackupBackupPlan#selected_namespaces}
        '''
        result = self._values.get("selected_namespaces")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"gcp_kms_encryption_key": "gcpKmsEncryptionKey"},
)
class GoogleGkeBackupBackupPlanBackupConfigEncryptionKey:
    def __init__(self, *, gcp_kms_encryption_key: builtins.str) -> None:
        '''
        :param gcp_kms_encryption_key: Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#gcp_kms_encryption_key GoogleGkeBackupBackupPlan#gcp_kms_encryption_key} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edd13929c8d986bbfcfd35ee1b2f15e2b89631c84eee885e1bd7df1655b9638)
            check_type(argname="argument gcp_kms_encryption_key", value=gcp_kms_encryption_key, expected_type=type_hints["gcp_kms_encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gcp_kms_encryption_key": gcp_kms_encryption_key,
        }

    @builtins.property
    def gcp_kms_encryption_key(self) -> builtins.str:
        '''Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#gcp_kms_encryption_key GoogleGkeBackupBackupPlan#gcp_kms_encryption_key}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("gcp_kms_encryption_key")
        assert result is not None, "Required property 'gcp_kms_encryption_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupConfigEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e91a3ed2f4188872aa8653798f8a9ddcb6b7f5ffed44a8cbf3270e564f3ccc12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="gcpKmsEncryptionKeyInput")
    def gcp_kms_encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpKmsEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpKmsEncryptionKey")
    def gcp_kms_encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpKmsEncryptionKey"))

    @gcp_kms_encryption_key.setter
    def gcp_kms_encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c391b842e5c6af782ecd1ab72027207fbaf8a8aa8d0502069b7c7209e3903327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpKmsEncryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d690a090b3ec8753ffcb091bbf160f512a4616a15b9a0e94fd012ee4c0053c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b03f278267f6e91d782cc9c7b3ddabe960843289ba827d3912c6b2b14eee5569)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionKey")
    def put_encryption_key(self, *, gcp_kms_encryption_key: builtins.str) -> None:
        '''
        :param gcp_kms_encryption_key: Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#gcp_kms_encryption_key GoogleGkeBackupBackupPlan#gcp_kms_encryption_key} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleGkeBackupBackupPlanBackupConfigEncryptionKey(
            gcp_kms_encryption_key=gcp_kms_encryption_key
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKey", [value]))

    @jsii.member(jsii_name="putSelectedApplications")
    def put_selected_applications(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaced_names GoogleGkeBackupBackupPlan#namespaced_names}
        '''
        value = GoogleGkeBackupBackupPlanBackupConfigSelectedApplications(
            namespaced_names=namespaced_names
        )

        return typing.cast(None, jsii.invoke(self, "putSelectedApplications", [value]))

    @jsii.member(jsii_name="putSelectedNamespaces")
    def put_selected_namespaces(
        self,
        *,
        namespaces: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaces GoogleGkeBackupBackupPlan#namespaces}
        '''
        value = GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces(
            namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putSelectedNamespaces", [value]))

    @jsii.member(jsii_name="resetAllNamespaces")
    def reset_all_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllNamespaces", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetIncludeSecrets")
    def reset_include_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSecrets", []))

    @jsii.member(jsii_name="resetIncludeVolumeData")
    def reset_include_volume_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeVolumeData", []))

    @jsii.member(jsii_name="resetPermissiveMode")
    def reset_permissive_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissiveMode", []))

    @jsii.member(jsii_name="resetSelectedApplications")
    def reset_selected_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedApplications", []))

    @jsii.member(jsii_name="resetSelectedNamespaces")
    def reset_selected_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedNamespaces", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(
        self,
    ) -> GoogleGkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference:
        return typing.cast(GoogleGkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplications")
    def selected_applications(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference", jsii.get(self, "selectedApplications"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespaces")
    def selected_namespaces(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference", jsii.get(self, "selectedNamespaces"))

    @builtins.property
    @jsii.member(jsii_name="allNamespacesInput")
    def all_namespaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSecretsInput")
    def include_secrets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeSecretsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeVolumeDataInput")
    def include_volume_data_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeVolumeDataInput"))

    @builtins.property
    @jsii.member(jsii_name="permissiveModeInput")
    def permissive_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permissiveModeInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplicationsInput")
    def selected_applications_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedApplications"], jsii.get(self, "selectedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespacesInput")
    def selected_namespaces_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces"], jsii.get(self, "selectedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="allNamespaces")
    def all_namespaces(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allNamespaces"))

    @all_namespaces.setter
    def all_namespaces(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d72c4a47c5fd9fb483aa8f70ac15bad6f148a6dfaf846c0f9945c90e088e24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeSecrets")
    def include_secrets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeSecrets"))

    @include_secrets.setter
    def include_secrets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab7b78ab86e11d9a9a6e343e45507f2ef2a4010fbed25e53907191ad8c805a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSecrets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeVolumeData")
    def include_volume_data(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeVolumeData"))

    @include_volume_data.setter
    def include_volume_data(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79de0b23022cd1842afb7386eb21fba03b282f6c3eb97b6ddbb685f0c8287e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeVolumeData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissiveMode")
    def permissive_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permissiveMode"))

    @permissive_mode.setter
    def permissive_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c50e18937972acf8004e263084708479ab4b82f91332297c7c2bbf86af82a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissiveMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfig]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05625f973fcbbc58e5226be76e7e85ef9e3b179097dc8bc8d4ee8a5642c59a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedApplications",
    jsii_struct_bases=[],
    name_mapping={"namespaced_names": "namespacedNames"},
)
class GoogleGkeBackupBackupPlanBackupConfigSelectedApplications:
    def __init__(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaced_names GoogleGkeBackupBackupPlan#namespaced_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cb4d4fbda97a38dd26b5627f67234895d510f2fb141ff2fb5925c04ea8f063)
            check_type(argname="argument namespaced_names", value=namespaced_names, expected_type=type_hints["namespaced_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaced_names": namespaced_names,
        }

    @builtins.property
    def namespaced_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames"]]:
        '''namespaced_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaced_names GoogleGkeBackupBackupPlan#namespaced_names}
        '''
        result = self._values.get("namespaced_names")
        assert result is not None, "Required property 'namespaced_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupConfigSelectedApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: The name of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#name GoogleGkeBackupBackupPlan#name}
        :param namespace: The namespace of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespace GoogleGkeBackupBackupPlan#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69ebc700927d9be88d0374ab7519bee1b3076dd8b1f82d73ac3022158b50bee)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#name GoogleGkeBackupBackupPlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''The namespace of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespace GoogleGkeBackupBackupPlan#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fd4e639b010d7be46cd80ebf09b3f397534661d165c4f0e5adbe8d67117bb9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9ae0ab7f31f29abebcfedfd6949e498407a508788760dc831fbff089f6a62b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192550a719945dc896b3d61da03f279fe36bff37b08f380c9fcdf49a0f90627e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a2a9eb9dae5f7e3f2489e01247aa24fea58f20d225f1d704e79a36ffaeed2af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba3cf72123068616497e3eb3ad88754e3a7ba7c9f5435d3000f8fb42b27230c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e082f19f8be04deeeee4464a469d9a5b6bbed11a9a9603e6964a1ef6ee5b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d53f8efa536fb8ba6f720357d33641e336282cac2d3400f3c173dba0efadce9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__378696cf0ac5056a35612f55db05fb73d4989ed44154db7a35d9dd65187cfd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325cb99d20a624c0b31f51f76f3d21a83b5cf4a9ec16416902bb91bf03f09e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bcb789c4739ccb714c61ef48da54cf81bd5c6ed8fa1cfa3725d47d54639fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5434f413449ff225ebf5fccefe9c4a35ed1c91acf13bd03e601d0e392a1419)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespacedNames")
    def put_namespaced_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0981bef1f0c77e057eaf4a26c6b717a3535f5ecdf18d96fb32ddd7d131234704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespacedNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="namespacedNames")
    def namespaced_names(
        self,
    ) -> GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList:
        return typing.cast(GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList, jsii.get(self, "namespacedNames"))

    @builtins.property
    @jsii.member(jsii_name="namespacedNamesInput")
    def namespaced_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "namespacedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedApplications]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedApplications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedApplications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a6e99c89d4a91f27fe96e0556e360f365ae87ee2220dcea77370687a727622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaces GoogleGkeBackupBackupPlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39305ce0336b919dc441345552bddb48d2a94bc0aa53273e657d5bbb4bfc7589)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#namespaces GoogleGkeBackupBackupPlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d6f670417cfa4bdae5668b2ab32318f927c7b1360ec969a3e4999aea0401e51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="namespacesInput")
    def namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaces")
    def namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namespaces"))

    @namespaces.setter
    def namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21efa3681deb90dca67a15191932d33d4262b48cad806ba9e7446f460b6b161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457a6b0b95e27c9ad12bb70f4b3f4b9cbe906fbcddd9aae5271db185808841ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "cron_schedule": "cronSchedule",
        "paused": "paused",
        "rpo_config": "rpoConfig",
    },
)
class GoogleGkeBackupBackupPlanBackupSchedule:
    def __init__(
        self,
        *,
        cron_schedule: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rpo_config: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_schedule: A standard cron string that defines a repeating schedule for creating Backups via this BackupPlan. This is mutually exclusive with the rpoConfig field since at most one schedule can be defined for a BackupPlan. If this is defined, then backupRetainDays must also be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cron_schedule GoogleGkeBackupBackupPlan#cron_schedule}
        :param paused: This flag denotes whether automatic Backup creation is paused for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#paused GoogleGkeBackupBackupPlan#paused}
        :param rpo_config: rpo_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#rpo_config GoogleGkeBackupBackupPlan#rpo_config}
        '''
        if isinstance(rpo_config, dict):
            rpo_config = GoogleGkeBackupBackupPlanBackupScheduleRpoConfig(**rpo_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409d5d54bc503434e7538f71afc1b1f43c692ba1c18ac38eff95b6fbe2b70508)
            check_type(argname="argument cron_schedule", value=cron_schedule, expected_type=type_hints["cron_schedule"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument rpo_config", value=rpo_config, expected_type=type_hints["rpo_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_schedule is not None:
            self._values["cron_schedule"] = cron_schedule
        if paused is not None:
            self._values["paused"] = paused
        if rpo_config is not None:
            self._values["rpo_config"] = rpo_config

    @builtins.property
    def cron_schedule(self) -> typing.Optional[builtins.str]:
        '''A standard cron string that defines a repeating schedule for creating Backups via this BackupPlan.

        This is mutually exclusive with the rpoConfig field since at most one
        schedule can be defined for a BackupPlan.
        If this is defined, then backupRetainDays must also be defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cron_schedule GoogleGkeBackupBackupPlan#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag denotes whether automatic Backup creation is paused for this BackupPlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#paused GoogleGkeBackupBackupPlan#paused}
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rpo_config(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig"]:
        '''rpo_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#rpo_config GoogleGkeBackupBackupPlan#rpo_config}
        '''
        result = self._values.get("rpo_config")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c969a9ef4532b2843c96bc30f52fb336031b49a63249eef0b3e3e14ca71bcfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRpoConfig")
    def put_rpo_config(
        self,
        *,
        target_rpo_minutes: jsii.Number,
        exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param target_rpo_minutes: Defines the target RPO for the BackupPlan in minutes, which means the target maximum data loss in time that is acceptable for this BackupPlan. This must be at least 60, i.e., 1 hour, and at most 86400, i.e., 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#target_rpo_minutes GoogleGkeBackupBackupPlan#target_rpo_minutes}
        :param exclusion_windows: exclusion_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#exclusion_windows GoogleGkeBackupBackupPlan#exclusion_windows}
        '''
        value = GoogleGkeBackupBackupPlanBackupScheduleRpoConfig(
            target_rpo_minutes=target_rpo_minutes, exclusion_windows=exclusion_windows
        )

        return typing.cast(None, jsii.invoke(self, "putRpoConfig", [value]))

    @jsii.member(jsii_name="resetCronSchedule")
    def reset_cron_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSchedule", []))

    @jsii.member(jsii_name="resetPaused")
    def reset_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaused", []))

    @jsii.member(jsii_name="resetRpoConfig")
    def reset_rpo_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRpoConfig", []))

    @builtins.property
    @jsii.member(jsii_name="rpoConfig")
    def rpo_config(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleRpoConfigOutputReference", jsii.get(self, "rpoConfig"))

    @builtins.property
    @jsii.member(jsii_name="cronScheduleInput")
    def cron_schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="pausedInput")
    def paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pausedInput"))

    @builtins.property
    @jsii.member(jsii_name="rpoConfigInput")
    def rpo_config_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfig"], jsii.get(self, "rpoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cronSchedule")
    def cron_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSchedule"))

    @cron_schedule.setter
    def cron_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491dd27ffbc8e987866014a480276829d50c5b8a9e87ed54c7e340cd31128da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paused")
    def paused(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "paused"))

    @paused.setter
    def paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefb111bc43b9ae52190a5afa4d7de6b547b9adc59569738bd34e8995cc6fecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227006c47dcfa37a2e2e6ba337ce673dc7e53c24399872249e492648cde0faf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "target_rpo_minutes": "targetRpoMinutes",
        "exclusion_windows": "exclusionWindows",
    },
)
class GoogleGkeBackupBackupPlanBackupScheduleRpoConfig:
    def __init__(
        self,
        *,
        target_rpo_minutes: jsii.Number,
        exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param target_rpo_minutes: Defines the target RPO for the BackupPlan in minutes, which means the target maximum data loss in time that is acceptable for this BackupPlan. This must be at least 60, i.e., 1 hour, and at most 86400, i.e., 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#target_rpo_minutes GoogleGkeBackupBackupPlan#target_rpo_minutes}
        :param exclusion_windows: exclusion_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#exclusion_windows GoogleGkeBackupBackupPlan#exclusion_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aaac0df4c9836530d0c802dac40f5a821e1fd707921a17fc17b843e860b054d)
            check_type(argname="argument target_rpo_minutes", value=target_rpo_minutes, expected_type=type_hints["target_rpo_minutes"])
            check_type(argname="argument exclusion_windows", value=exclusion_windows, expected_type=type_hints["exclusion_windows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_rpo_minutes": target_rpo_minutes,
        }
        if exclusion_windows is not None:
            self._values["exclusion_windows"] = exclusion_windows

    @builtins.property
    def target_rpo_minutes(self) -> jsii.Number:
        '''Defines the target RPO for the BackupPlan in minutes, which means the target maximum data loss in time that is acceptable for this BackupPlan.

        This must be
        at least 60, i.e., 1 hour, and at most 86400, i.e., 60 days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#target_rpo_minutes GoogleGkeBackupBackupPlan#target_rpo_minutes}
        '''
        result = self._values.get("target_rpo_minutes")
        assert result is not None, "Required property 'target_rpo_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def exclusion_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows"]]]:
        '''exclusion_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#exclusion_windows GoogleGkeBackupBackupPlan#exclusion_windows}
        '''
        result = self._values.get("exclusion_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupScheduleRpoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "start_time": "startTime",
        "daily": "daily",
        "days_of_week": "daysOfWeek",
        "single_occurrence_date": "singleOccurrenceDate",
    },
)
class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows:
    def __init__(
        self,
        *,
        duration: builtins.str,
        start_time: typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
        daily: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        days_of_week: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek", typing.Dict[builtins.str, typing.Any]]] = None,
        single_occurrence_date: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: Specifies duration of the window in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Restrictions for duration based on the recurrence type to allow some time for backup to happen: - single_occurrence_date: no restriction - daily window: duration < 24 hours - weekly window: - days of week includes all seven days of a week: duration < 24 hours - all other weekly window: duration < 168 hours (i.e., 24 * 7 hours) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#duration GoogleGkeBackupBackupPlan#duration}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#start_time GoogleGkeBackupBackupPlan#start_time}
        :param daily: The exclusion window occurs every day if set to "True". Specifying this field to "False" is an error. Only one of singleOccurrenceDate, daily and daysOfWeek may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#daily GoogleGkeBackupBackupPlan#daily}
        :param days_of_week: days_of_week block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#days_of_week GoogleGkeBackupBackupPlan#days_of_week}
        :param single_occurrence_date: single_occurrence_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#single_occurrence_date GoogleGkeBackupBackupPlan#single_occurrence_date}
        '''
        if isinstance(start_time, dict):
            start_time = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(**start_time)
        if isinstance(days_of_week, dict):
            days_of_week = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(**days_of_week)
        if isinstance(single_occurrence_date, dict):
            single_occurrence_date = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(**single_occurrence_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f689367754ededf44ddf5676afa1452bc5aff242a95f323fe9d9756628395c)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument single_occurrence_date", value=single_occurrence_date, expected_type=type_hints["single_occurrence_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
            "start_time": start_time,
        }
        if daily is not None:
            self._values["daily"] = daily
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if single_occurrence_date is not None:
            self._values["single_occurrence_date"] = single_occurrence_date

    @builtins.property
    def duration(self) -> builtins.str:
        '''Specifies duration of the window in seconds with up to nine fractional digits, terminated by 's'.

        Example: "3.5s". Restrictions for duration based on the
        recurrence type to allow some time for backup to happen:

        - single_occurrence_date:  no restriction
        - daily window: duration < 24 hours
        - weekly window:

          - days of week includes all seven days of a week: duration < 24 hours
          - all other weekly window: duration < 168 hours (i.e., 24 * 7 hours)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#duration GoogleGkeBackupBackupPlan#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#start_time GoogleGkeBackupBackupPlan#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime", result)

    @builtins.property
    def daily(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The exclusion window occurs every day if set to "True".

        Specifying this field to "False" is an error.
        Only one of singleOccurrenceDate, daily and daysOfWeek may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#daily GoogleGkeBackupBackupPlan#daily}
        '''
        result = self._values.get("daily")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def days_of_week(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek"]:
        '''days_of_week block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#days_of_week GoogleGkeBackupBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek"], result)

    @builtins.property
    def single_occurrence_date(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"]:
        '''single_occurrence_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#single_occurrence_date GoogleGkeBackupBackupPlan#single_occurrence_date}
        '''
        result = self._values.get("single_occurrence_date")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek",
    jsii_struct_bases=[],
    name_mapping={"days_of_week": "daysOfWeek"},
)
class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek:
    def __init__(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param days_of_week: A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#days_of_week GoogleGkeBackupBackupPlan#days_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe7ad407cfec998bed39ce912030627ec2328c9b3f85837c6fe625c60b60196)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#days_of_week GoogleGkeBackupBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a3e639a631903a4266a99deccb49860767f46c6d24e1be1a8d289cb74ca275)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245c40381ab31f8a62525a5e4df8ccaec0212c0b79f512c5794383b81fc9abc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad20321aa85e6a2aaf5b96fe264f780524c76ce2820bf09eddd38a5670ef558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__482c36be83a55351a82b4958268e1e465bdf6e791441960e74aca1aeb0080aca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb2988342c883936652b87855c1bda45d2067700ad026f7634bfb91c7834949)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1787495e0ac623b812f30e2378678fcda52733aca7875590f8cb2451e8dac9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f600b4dd16c9fd7392a6ebd2bf9ac1da2ec885f2f5bf4ac5a0fc7d9b908e9313)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4abb443ac7ce31431ac814e596b930ee78f134f0fc6c1f9ac0c42da4c9a8c140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b75c4eb899261c8a772b730151b1f705792d2827b33587696e873b96c602b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda99eff7d6b191c9751949aeab805eaf635485bc7b4e28cdf9d9a8e06966f13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDaysOfWeek")
    def put_days_of_week(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param days_of_week: A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#days_of_week GoogleGkeBackupBackupPlan#days_of_week}
        '''
        value = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(
            days_of_week=days_of_week
        )

        return typing.cast(None, jsii.invoke(self, "putDaysOfWeek", [value]))

    @jsii.member(jsii_name="putSingleOccurrenceDate")
    def put_single_occurrence_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#day GoogleGkeBackupBackupPlan#day}
        :param month: Month of a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#month GoogleGkeBackupBackupPlan#month}
        :param year: Year of the date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#year GoogleGkeBackupBackupPlan#year}
        '''
        value = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putSingleOccurrenceDate", [value]))

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#hours GoogleGkeBackupBackupPlan#hours}
        :param minutes: Minutes of hour of day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#minutes GoogleGkeBackupBackupPlan#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#nanos GoogleGkeBackupBackupPlan#nanos}
        :param seconds: Seconds of minutes of the time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#seconds GoogleGkeBackupBackupPlan#seconds}
        '''
        value = GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @jsii.member(jsii_name="resetDaily")
    def reset_daily(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaily", []))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetSingleOccurrenceDate")
    def reset_single_occurrence_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleOccurrenceDate", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(
        self,
    ) -> GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference:
        return typing.cast(GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference, jsii.get(self, "daysOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="singleOccurrenceDate")
    def single_occurrence_date(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference", jsii.get(self, "singleOccurrenceDate"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference":
        return typing.cast("GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dailyInput")
    def daily_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dailyInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="singleOccurrenceDateInput")
    def single_occurrence_date_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"], jsii.get(self, "singleOccurrenceDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime"]:
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daily")
    def daily(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "daily"))

    @daily.setter
    def daily(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e32696c65687f25c0971a9e1563a957c437161d7f8d1c469b20970e376582b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af6905af9366c8fd03222ae7c044df4dca557150b12c3e5e224868ef7a44eac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe3066365316bde403aabf55fda98c5c7a233e4b91517ee6cfb610b70b7a555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#day GoogleGkeBackupBackupPlan#day}
        :param month: Month of a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#month GoogleGkeBackupBackupPlan#month}
        :param year: Year of the date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#year GoogleGkeBackupBackupPlan#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78cad4dd123df7feeb568d08d32d93a0391fd5cacbfb2a17afeec28cd5fdc8ff)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#day GoogleGkeBackupBackupPlan#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#month GoogleGkeBackupBackupPlan#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#year GoogleGkeBackupBackupPlan#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cee57c6879abf8e5d095ebf3d491c763dc6e2c6dd775f5e0c108047b22ce5292)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e101bc5c9955289aa3f019c22881e3a3cf48fb9622daa4d788d7129ed1d2c6cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c331a5ea5da815ef134543ecf9f04dcb24b7188731c4f18d246e438d826151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d32ad819b7580c1464912deaf163058e78a267318493f06cef617db3265594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a04764b4993ea6ed185b42bfbbe6880e53573ca3f12d95606be598a8e6d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#hours GoogleGkeBackupBackupPlan#hours}
        :param minutes: Minutes of hour of day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#minutes GoogleGkeBackupBackupPlan#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#nanos GoogleGkeBackupBackupPlan#nanos}
        :param seconds: Seconds of minutes of the time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#seconds GoogleGkeBackupBackupPlan#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ea85a622239052635d6345000cbd0723cf9770def5ff214c9aec717ca229bc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#hours GoogleGkeBackupBackupPlan#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#minutes GoogleGkeBackupBackupPlan#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#nanos GoogleGkeBackupBackupPlan#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#seconds GoogleGkeBackupBackupPlan#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af550752ff7152935f839ca3cd04893270c5c562b8236b76ae9fd1648972690)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__8dc9540ea8285fef59d5af6dccd7d3ba92a8e00919b07f6d730aef8ea7d2768a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4403ea72b43fd13867d64aef1c7df59fba52e2187c6db23ce0aa8c310567617a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cab481076ea5c2d9efe88a57198ab8f3df0ebd086b38cbe89c535908dcd645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77baa6484048d8deedd28f073a0044971252c2994b3e1835509bd653828bee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3def0f1f793e6df0ba35a3dcdcdd7ecbde1db4ae2721aaa1a5c75f3dc1ae6ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupBackupPlanBackupScheduleRpoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanBackupScheduleRpoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f74e1ed13e1f322222b41848a3d29f805ce6b7e454791c214c32afacfaa0a259)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionWindows")
    def put_exclusion_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d075cc1c28f518986030dc6f35f09a6d7c203dd7fd4f00794f485d7578bd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionWindows", [value]))

    @jsii.member(jsii_name="resetExclusionWindows")
    def reset_exclusion_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionWindows", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionWindows")
    def exclusion_windows(
        self,
    ) -> GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList:
        return typing.cast(GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList, jsii.get(self, "exclusionWindows"))

    @builtins.property
    @jsii.member(jsii_name="exclusionWindowsInput")
    def exclusion_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]], jsii.get(self, "exclusionWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRpoMinutesInput")
    def target_rpo_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetRpoMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRpoMinutes")
    def target_rpo_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetRpoMinutes"))

    @target_rpo_minutes.setter
    def target_rpo_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58531cccc9cb2e569636210ea5d87456873adfaef3f15b5d0b27ed119896120a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRpoMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfig]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ef9bc97c11adfc1bc9fdeebc32a1d2e804f9249318f5c9ec17036c7444378a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster": "cluster",
        "location": "location",
        "name": "name",
        "backup_config": "backupConfig",
        "backup_schedule": "backupSchedule",
        "deactivated": "deactivated",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "retention_policy": "retentionPolicy",
        "timeouts": "timeouts",
    },
)
class GoogleGkeBackupBackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backup_config: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_schedule: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
        deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeBackupBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: The source cluster from which Backups will be created via this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cluster GoogleGkeBackupBackupPlan#cluster}
        :param location: The region of the Backup Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#location GoogleGkeBackupBackupPlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#name GoogleGkeBackupBackupPlan#name}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_config GoogleGkeBackupBackupPlan#backup_config}
        :param backup_schedule: backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_schedule GoogleGkeBackupBackupPlan#backup_schedule}
        :param deactivated: This flag indicates whether this BackupPlan has been deactivated. Setting this field to True locks the BackupPlan such that no further updates will be allowed (except deletes), including the deactivated field itself. It also prevents any new Backups from being created via this BackupPlan (including scheduled Backups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#deactivated GoogleGkeBackupBackupPlan#deactivated}
        :param description: User specified descriptive string for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#description GoogleGkeBackupBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#id GoogleGkeBackupBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#labels GoogleGkeBackupBackupPlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#project GoogleGkeBackupBackupPlan#project}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#retention_policy GoogleGkeBackupBackupPlan#retention_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#timeouts GoogleGkeBackupBackupPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_config, dict):
            backup_config = GoogleGkeBackupBackupPlanBackupConfig(**backup_config)
        if isinstance(backup_schedule, dict):
            backup_schedule = GoogleGkeBackupBackupPlanBackupSchedule(**backup_schedule)
        if isinstance(retention_policy, dict):
            retention_policy = GoogleGkeBackupBackupPlanRetentionPolicy(**retention_policy)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeBackupBackupPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b7cdee3b7382297d6fb20ab534fa87902039f82e67591de2158ac4ba55e6fe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument backup_config", value=backup_config, expected_type=type_hints["backup_config"])
            check_type(argname="argument backup_schedule", value=backup_schedule, expected_type=type_hints["backup_schedule"])
            check_type(argname="argument deactivated", value=deactivated, expected_type=type_hints["deactivated"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "location": location,
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
        if backup_config is not None:
            self._values["backup_config"] = backup_config
        if backup_schedule is not None:
            self._values["backup_schedule"] = backup_schedule
        if deactivated is not None:
            self._values["deactivated"] = deactivated
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
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
    def cluster(self) -> builtins.str:
        '''The source cluster from which Backups will be created via this BackupPlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#cluster GoogleGkeBackupBackupPlan#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Backup Plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#location GoogleGkeBackupBackupPlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The full name of the BackupPlan Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#name GoogleGkeBackupBackupPlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_config(self) -> typing.Optional[GoogleGkeBackupBackupPlanBackupConfig]:
        '''backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_config GoogleGkeBackupBackupPlan#backup_config}
        '''
        result = self._values.get("backup_config")
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupConfig], result)

    @builtins.property
    def backup_schedule(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule]:
        '''backup_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_schedule GoogleGkeBackupBackupPlan#backup_schedule}
        '''
        result = self._values.get("backup_schedule")
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule], result)

    @builtins.property
    def deactivated(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag indicates whether this BackupPlan has been deactivated.

        Setting this field to True locks the BackupPlan such that no further updates will be allowed
        (except deletes), including the deactivated field itself. It also prevents any new Backups
        from being created via this BackupPlan (including scheduled Backups).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#deactivated GoogleGkeBackupBackupPlan#deactivated}
        '''
        result = self._values.get("deactivated")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User specified descriptive string for this BackupPlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#description GoogleGkeBackupBackupPlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#id GoogleGkeBackupBackupPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Description: A set of custom labels supplied by the user.

        A list of key->value pairs.
        Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#labels GoogleGkeBackupBackupPlan#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#project GoogleGkeBackupBackupPlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["GoogleGkeBackupBackupPlanRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#retention_policy GoogleGkeBackupBackupPlan#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanRetentionPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeBackupBackupPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#timeouts GoogleGkeBackupBackupPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeBackupBackupPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup_delete_lock_days": "backupDeleteLockDays",
        "backup_retain_days": "backupRetainDays",
        "locked": "locked",
    },
)
class GoogleGkeBackupBackupPlanRetentionPolicy:
    def __init__(
        self,
        *,
        backup_delete_lock_days: typing.Optional[jsii.Number] = None,
        backup_retain_days: typing.Optional[jsii.Number] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_delete_lock_days: Minimum age for a Backup created via this BackupPlan (in days). Must be an integer value between 0-90 (inclusive). A Backup created under this BackupPlan will not be deletable until it reaches Backup's (create time + backup_delete_lock_days). Updating this field of a BackupPlan does not affect existing Backups. Backups created after a successful update will inherit this new value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_delete_lock_days GoogleGkeBackupBackupPlan#backup_delete_lock_days}
        :param backup_retain_days: The default maximum age of a Backup created via this BackupPlan. This field MUST be an integer value >= 0 and <= 365. If specified, a Backup created under this BackupPlan will be automatically deleted after its age reaches (createTime + backupRetainDays). If not specified, Backups created under this BackupPlan will NOT be subject to automatic deletion. Updating this field does NOT affect existing Backups under it. Backups created AFTER a successful update will automatically pick up the new value. NOTE: backupRetainDays must be >= backupDeleteLockDays. If cronSchedule is defined, then this must be <= 360 * the creation interval. If rpo_config is defined, then this must be <= 360 * targetRpoMinutes/(1440minutes/day) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_retain_days GoogleGkeBackupBackupPlan#backup_retain_days}
        :param locked: This flag denotes whether the retention policy of this BackupPlan is locked. If set to True, no further update is allowed on this policy, including the locked field itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#locked GoogleGkeBackupBackupPlan#locked}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f498d00bd0af6ff87ff2a35b5ef000185b91908248acaffe99b195fc1c167cc)
            check_type(argname="argument backup_delete_lock_days", value=backup_delete_lock_days, expected_type=type_hints["backup_delete_lock_days"])
            check_type(argname="argument backup_retain_days", value=backup_retain_days, expected_type=type_hints["backup_retain_days"])
            check_type(argname="argument locked", value=locked, expected_type=type_hints["locked"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_delete_lock_days is not None:
            self._values["backup_delete_lock_days"] = backup_delete_lock_days
        if backup_retain_days is not None:
            self._values["backup_retain_days"] = backup_retain_days
        if locked is not None:
            self._values["locked"] = locked

    @builtins.property
    def backup_delete_lock_days(self) -> typing.Optional[jsii.Number]:
        '''Minimum age for a Backup created via this BackupPlan (in days).

        Must be an integer value between 0-90 (inclusive).
        A Backup created under this BackupPlan will not be deletable
        until it reaches Backup's (create time + backup_delete_lock_days).
        Updating this field of a BackupPlan does not affect existing Backups.
        Backups created after a successful update will inherit this new value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_delete_lock_days GoogleGkeBackupBackupPlan#backup_delete_lock_days}
        '''
        result = self._values.get("backup_delete_lock_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_retain_days(self) -> typing.Optional[jsii.Number]:
        '''The default maximum age of a Backup created via this BackupPlan.

        This field MUST be an integer value >= 0 and <= 365. If specified,
        a Backup created under this BackupPlan will be automatically deleted
        after its age reaches (createTime + backupRetainDays).
        If not specified, Backups created under this BackupPlan will NOT be
        subject to automatic deletion. Updating this field does NOT affect
        existing Backups under it. Backups created AFTER a successful update
        will automatically pick up the new value.
        NOTE: backupRetainDays must be >= backupDeleteLockDays.
        If cronSchedule is defined, then this must be <= 360 * the creation interval.
        If rpo_config is defined, then this must be
        <= 360 * targetRpoMinutes/(1440minutes/day)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#backup_retain_days GoogleGkeBackupBackupPlan#backup_retain_days}
        '''
        result = self._values.get("backup_retain_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def locked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag denotes whether the retention policy of this BackupPlan is locked.

        If set to True, no further update is allowed on this policy, including
        the locked field itself.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#locked GoogleGkeBackupBackupPlan#locked}
        '''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62179972817943c2b6d29fa7ccc4764ec3dd595235c2f6ead7c57261b5e17f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupDeleteLockDays")
    def reset_backup_delete_lock_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupDeleteLockDays", []))

    @jsii.member(jsii_name="resetBackupRetainDays")
    def reset_backup_retain_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetainDays", []))

    @jsii.member(jsii_name="resetLocked")
    def reset_locked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocked", []))

    @builtins.property
    @jsii.member(jsii_name="backupDeleteLockDaysInput")
    def backup_delete_lock_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupDeleteLockDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetainDaysInput")
    def backup_retain_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetainDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="lockedInput")
    def locked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockedInput"))

    @builtins.property
    @jsii.member(jsii_name="backupDeleteLockDays")
    def backup_delete_lock_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupDeleteLockDays"))

    @backup_delete_lock_days.setter
    def backup_delete_lock_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa48c2d0b1800063a0d725042878c1584415d791c1aa27b9bbef39862867026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupDeleteLockDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupRetainDays")
    def backup_retain_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetainDays"))

    @backup_retain_days.setter
    def backup_retain_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2f32d402a98d14faacbb0d2c1ad76a26447c3c5251560a1e400ca9164f844a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetainDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locked")
    def locked(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "locked"))

    @locked.setter
    def locked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e72776c666c14650ef493c1e5ed523974d2b21dc71981869846f18d0d4be08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupBackupPlanRetentionPolicy]:
        return typing.cast(typing.Optional[GoogleGkeBackupBackupPlanRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupBackupPlanRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44855ea5c0cd92419b36c7ec08439b8fe26f239dc99493024b763624dea41f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeBackupBackupPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#create GoogleGkeBackupBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#delete GoogleGkeBackupBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#update GoogleGkeBackupBackupPlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9afaac3074b275142266fa5fb3deb647177f65aaad5e7d6db9b7a051ab2e869)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#create GoogleGkeBackupBackupPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#delete GoogleGkeBackupBackupPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_backup_plan#update GoogleGkeBackupBackupPlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupBackupPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupBackupPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupBackupPlan.GoogleGkeBackupBackupPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fa9f4292bb805e9de4b328c87c1c8b456e03c67dd98b1edd33509a9d55e914c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d44dc56f964383e67a6538a7bd21e8e6cf3b980613ba1f07f15c504d885b042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060fd1e06f5eceefec4a572ec642931d9a1e209bd49ee73f7cc292f55b569dda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c423186701891c457432db9513db3ad900961c901ab2ba3d839e3f83af628e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cd16dd3eb0286224833d839c1ce7cba288eb5f3eda0e8d1e6028b294be1724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeBackupBackupPlan",
    "GoogleGkeBackupBackupPlanBackupConfig",
    "GoogleGkeBackupBackupPlanBackupConfigEncryptionKey",
    "GoogleGkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference",
    "GoogleGkeBackupBackupPlanBackupConfigOutputReference",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedApplications",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces",
    "GoogleGkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference",
    "GoogleGkeBackupBackupPlanBackupSchedule",
    "GoogleGkeBackupBackupPlanBackupScheduleOutputReference",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfig",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference",
    "GoogleGkeBackupBackupPlanBackupScheduleRpoConfigOutputReference",
    "GoogleGkeBackupBackupPlanConfig",
    "GoogleGkeBackupBackupPlanRetentionPolicy",
    "GoogleGkeBackupBackupPlanRetentionPolicyOutputReference",
    "GoogleGkeBackupBackupPlanTimeouts",
    "GoogleGkeBackupBackupPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__aa0c8dc89ae7cfe2387c009df7f0d84dd1dfb69cca04d41b6370a7bc1eddf676(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backup_config: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_schedule: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__88b6080c001753b4794284feeb086fb35a17857976918a4ad4082127ec6035a4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b783dee6d1562cd4388e0a330836d4605150ae79090e6836f9f07c9a4905eb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9218ab617d846612494663ad6460905f6c3a8b4514513e55127f9052b1eaad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee372e1e6d403f4c9488423b80bd78d819d6b87374291ac95d67405b3f2083a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__410df59a1d306c112cf4939712fbc8529b626a8c205a19ba463ad9315b17a2c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f69b3996ad9a0e656cc34a1b166997ef3641e56756e3bab647d57418d333f1b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3afbd74e007f2b2c3da96fd5741e2bacf1c084bb71335c1ebc6277462d61c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194eec322da177abe3875c94f0da81dd94f487fe3997a8e4f901e7d5f6aca677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b193a5059b8b106ca1ce4a0593aaeb6143fed086bacb4663fc0d3999630fffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ccac3b296215dcb721ce539fb906c1ee30ef6d296f4b595e76be407879443e(
    *,
    all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selected_applications: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfigSelectedApplications, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_namespaces: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edd13929c8d986bbfcfd35ee1b2f15e2b89631c84eee885e1bd7df1655b9638(
    *,
    gcp_kms_encryption_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91a3ed2f4188872aa8653798f8a9ddcb6b7f5ffed44a8cbf3270e564f3ccc12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c391b842e5c6af782ecd1ab72027207fbaf8a8aa8d0502069b7c7209e3903327(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d690a090b3ec8753ffcb091bbf160f512a4616a15b9a0e94fd012ee4c0053c(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03f278267f6e91d782cc9c7b3ddabe960843289ba827d3912c6b2b14eee5569(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d72c4a47c5fd9fb483aa8f70ac15bad6f148a6dfaf846c0f9945c90e088e24e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab7b78ab86e11d9a9a6e343e45507f2ef2a4010fbed25e53907191ad8c805a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79de0b23022cd1842afb7386eb21fba03b282f6c3eb97b6ddbb685f0c8287e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c50e18937972acf8004e263084708479ab4b82f91332297c7c2bbf86af82a3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05625f973fcbbc58e5226be76e7e85ef9e3b179097dc8bc8d4ee8a5642c59a41(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cb4d4fbda97a38dd26b5627f67234895d510f2fb141ff2fb5925c04ea8f063(
    *,
    namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69ebc700927d9be88d0374ab7519bee1b3076dd8b1f82d73ac3022158b50bee(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd4e639b010d7be46cd80ebf09b3f397534661d165c4f0e5adbe8d67117bb9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9ae0ab7f31f29abebcfedfd6949e498407a508788760dc831fbff089f6a62b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192550a719945dc896b3d61da03f279fe36bff37b08f380c9fcdf49a0f90627e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2a9eb9dae5f7e3f2489e01247aa24fea58f20d225f1d704e79a36ffaeed2af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba3cf72123068616497e3eb3ad88754e3a7ba7c9f5435d3000f8fb42b27230c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e082f19f8be04deeeee4464a469d9a5b6bbed11a9a9603e6964a1ef6ee5b84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d53f8efa536fb8ba6f720357d33641e336282cac2d3400f3c173dba0efadce9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__378696cf0ac5056a35612f55db05fb73d4989ed44154db7a35d9dd65187cfd3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325cb99d20a624c0b31f51f76f3d21a83b5cf4a9ec16416902bb91bf03f09e11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bcb789c4739ccb714c61ef48da54cf81bd5c6ed8fa1cfa3725d47d54639fc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5434f413449ff225ebf5fccefe9c4a35ed1c91acf13bd03e601d0e392a1419(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0981bef1f0c77e057eaf4a26c6b717a3535f5ecdf18d96fb32ddd7d131234704(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a6e99c89d4a91f27fe96e0556e360f365ae87ee2220dcea77370687a727622(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedApplications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39305ce0336b919dc441345552bddb48d2a94bc0aa53273e657d5bbb4bfc7589(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6f670417cfa4bdae5668b2ab32318f927c7b1360ec969a3e4999aea0401e51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21efa3681deb90dca67a15191932d33d4262b48cad806ba9e7446f460b6b161(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457a6b0b95e27c9ad12bb70f4b3f4b9cbe906fbcddd9aae5271db185808841ce(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupConfigSelectedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409d5d54bc503434e7538f71afc1b1f43c692ba1c18ac38eff95b6fbe2b70508(
    *,
    cron_schedule: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rpo_config: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c969a9ef4532b2843c96bc30f52fb336031b49a63249eef0b3e3e14ca71bcfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491dd27ffbc8e987866014a480276829d50c5b8a9e87ed54c7e340cd31128da1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefb111bc43b9ae52190a5afa4d7de6b547b9adc59569738bd34e8995cc6fecf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227006c47dcfa37a2e2e6ba337ce673dc7e53c24399872249e492648cde0faf5(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaac0df4c9836530d0c802dac40f5a821e1fd707921a17fc17b843e860b054d(
    *,
    target_rpo_minutes: jsii.Number,
    exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f689367754ededf44ddf5676afa1452bc5aff242a95f323fe9d9756628395c(
    *,
    duration: builtins.str,
    start_time: typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
    daily: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    days_of_week: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek, typing.Dict[builtins.str, typing.Any]]] = None,
    single_occurrence_date: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe7ad407cfec998bed39ce912030627ec2328c9b3f85837c6fe625c60b60196(
    *,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a3e639a631903a4266a99deccb49860767f46c6d24e1be1a8d289cb74ca275(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245c40381ab31f8a62525a5e4df8ccaec0212c0b79f512c5794383b81fc9abc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad20321aa85e6a2aaf5b96fe264f780524c76ce2820bf09eddd38a5670ef558(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482c36be83a55351a82b4958268e1e465bdf6e791441960e74aca1aeb0080aca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb2988342c883936652b87855c1bda45d2067700ad026f7634bfb91c7834949(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1787495e0ac623b812f30e2378678fcda52733aca7875590f8cb2451e8dac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f600b4dd16c9fd7392a6ebd2bf9ac1da2ec885f2f5bf4ac5a0fc7d9b908e9313(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abb443ac7ce31431ac814e596b930ee78f134f0fc6c1f9ac0c42da4c9a8c140(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b75c4eb899261c8a772b730151b1f705792d2827b33587696e873b96c602b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda99eff7d6b191c9751949aeab805eaf635485bc7b4e28cdf9d9a8e06966f13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e32696c65687f25c0971a9e1563a957c437161d7f8d1c469b20970e376582b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af6905af9366c8fd03222ae7c044df4dca557150b12c3e5e224868ef7a44eac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe3066365316bde403aabf55fda98c5c7a233e4b91517ee6cfb610b70b7a555(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78cad4dd123df7feeb568d08d32d93a0391fd5cacbfb2a17afeec28cd5fdc8ff(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee57c6879abf8e5d095ebf3d491c763dc6e2c6dd775f5e0c108047b22ce5292(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e101bc5c9955289aa3f019c22881e3a3cf48fb9622daa4d788d7129ed1d2c6cb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c331a5ea5da815ef134543ecf9f04dcb24b7188731c4f18d246e438d826151(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d32ad819b7580c1464912deaf163058e78a267318493f06cef617db3265594(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a04764b4993ea6ed185b42bfbbe6880e53573ca3f12d95606be598a8e6d4d(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ea85a622239052635d6345000cbd0723cf9770def5ff214c9aec717ca229bc(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af550752ff7152935f839ca3cd04893270c5c562b8236b76ae9fd1648972690(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc9540ea8285fef59d5af6dccd7d3ba92a8e00919b07f6d730aef8ea7d2768a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4403ea72b43fd13867d64aef1c7df59fba52e2187c6db23ce0aa8c310567617a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cab481076ea5c2d9efe88a57198ab8f3df0ebd086b38cbe89c535908dcd645(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77baa6484048d8deedd28f073a0044971252c2994b3e1835509bd653828bee1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3def0f1f793e6df0ba35a3dcdcdd7ecbde1db4ae2721aaa1a5c75f3dc1ae6ed4(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74e1ed13e1f322222b41848a3d29f805ce6b7e454791c214c32afacfaa0a259(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d075cc1c28f518986030dc6f35f09a6d7c203dd7fd4f00794f485d7578bd25(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58531cccc9cb2e569636210ea5d87456873adfaef3f15b5d0b27ed119896120a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ef9bc97c11adfc1bc9fdeebc32a1d2e804f9249318f5c9ec17036c7444378a(
    value: typing.Optional[GoogleGkeBackupBackupPlanBackupScheduleRpoConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b7cdee3b7382297d6fb20ab534fa87902039f82e67591de2158ac4ba55e6fe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backup_config: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_schedule: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeBackupBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f498d00bd0af6ff87ff2a35b5ef000185b91908248acaffe99b195fc1c167cc(
    *,
    backup_delete_lock_days: typing.Optional[jsii.Number] = None,
    backup_retain_days: typing.Optional[jsii.Number] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62179972817943c2b6d29fa7ccc4764ec3dd595235c2f6ead7c57261b5e17f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa48c2d0b1800063a0d725042878c1584415d791c1aa27b9bbef39862867026(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2f32d402a98d14faacbb0d2c1ad76a26447c3c5251560a1e400ca9164f844a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e72776c666c14650ef493c1e5ed523974d2b21dc71981869846f18d0d4be08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44855ea5c0cd92419b36c7ec08439b8fe26f239dc99493024b763624dea41f30(
    value: typing.Optional[GoogleGkeBackupBackupPlanRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9afaac3074b275142266fa5fb3deb647177f65aaad5e7d6db9b7a051ab2e869(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa9f4292bb805e9de4b328c87c1c8b456e03c67dd98b1edd33509a9d55e914c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d44dc56f964383e67a6538a7bd21e8e6cf3b980613ba1f07f15c504d885b042(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060fd1e06f5eceefec4a572ec642931d9a1e209bd49ee73f7cc292f55b569dda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c423186701891c457432db9513db3ad900961c901ab2ba3d839e3f83af628e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cd16dd3eb0286224833d839c1ce7cba288eb5f3eda0e8d1e6028b294be1724(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupBackupPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_gke_backup_backup_plan`

Refer to the Terraform Registry for docs: [`google_gke_backup_backup_plan`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan).
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


class GkeBackupBackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan google_gke_backup_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        backup_config: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_schedule: typing.Optional[typing.Union["GkeBackupBackupPlanBackupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["GkeBackupBackupPlanRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeBackupBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan google_gke_backup_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: The source cluster from which Backups will be created via this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cluster GkeBackupBackupPlan#cluster}
        :param location: The region of the Backup Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#location GkeBackupBackupPlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#name GkeBackupBackupPlan#name}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_config GkeBackupBackupPlan#backup_config}
        :param backup_schedule: backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_schedule GkeBackupBackupPlan#backup_schedule}
        :param deactivated: This flag indicates whether this BackupPlan has been deactivated. Setting this field to True locks the BackupPlan such that no further updates will be allowed (except deletes), including the deactivated field itself. It also prevents any new Backups from being created via this BackupPlan (including scheduled Backups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#deactivated GkeBackupBackupPlan#deactivated}
        :param description: User specified descriptive string for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#description GkeBackupBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#id GkeBackupBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#labels GkeBackupBackupPlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#project GkeBackupBackupPlan#project}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#retention_policy GkeBackupBackupPlan#retention_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#timeouts GkeBackupBackupPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d365f7e9987d7729b1f43b96f442782fae040655a29dacfce586ede86ff63de1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeBackupBackupPlanConfig(
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
        '''Generates CDKTF code for importing a GkeBackupBackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeBackupBackupPlan to import.
        :param import_from_id: The id of the existing GkeBackupBackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeBackupBackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bf6055d9436465e3427bee2021db1eed11377460c45909b9c035514d9d3495)
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
        encryption_key: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_applications: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, include all namespaced resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#all_namespaces GkeBackupBackupPlan#all_namespaces}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#encryption_key GkeBackupBackupPlan#encryption_key}
        :param include_secrets: This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_secrets GkeBackupBackupPlan#include_secrets}
        :param include_volume_data: This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_volume_data GkeBackupBackupPlan#include_volume_data}
        :param permissive_mode: This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#permissive_mode GkeBackupBackupPlan#permissive_mode}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_applications GkeBackupBackupPlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_namespaces GkeBackupBackupPlan#selected_namespaces}
        '''
        value = GkeBackupBackupPlanBackupConfig(
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
        rpo_config: typing.Optional[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_schedule: A standard cron string that defines a repeating schedule for creating Backups via this BackupPlan. This is mutually exclusive with the rpoConfig field since at most one schedule can be defined for a BackupPlan. If this is defined, then backupRetainDays must also be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cron_schedule GkeBackupBackupPlan#cron_schedule}
        :param paused: This flag denotes whether automatic Backup creation is paused for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#paused GkeBackupBackupPlan#paused}
        :param rpo_config: rpo_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#rpo_config GkeBackupBackupPlan#rpo_config}
        '''
        value = GkeBackupBackupPlanBackupSchedule(
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
        :param backup_delete_lock_days: Minimum age for a Backup created via this BackupPlan (in days). Must be an integer value between 0-90 (inclusive). A Backup created under this BackupPlan will not be deletable until it reaches Backup's (create time + backup_delete_lock_days). Updating this field of a BackupPlan does not affect existing Backups. Backups created after a successful update will inherit this new value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_delete_lock_days GkeBackupBackupPlan#backup_delete_lock_days}
        :param backup_retain_days: The default maximum age of a Backup created via this BackupPlan. This field MUST be an integer value >= 0 and <= 365. If specified, a Backup created under this BackupPlan will be automatically deleted after its age reaches (createTime + backupRetainDays). If not specified, Backups created under this BackupPlan will NOT be subject to automatic deletion. Updating this field does NOT affect existing Backups under it. Backups created AFTER a successful update will automatically pick up the new value. NOTE: backupRetainDays must be >= backupDeleteLockDays. If cronSchedule is defined, then this must be <= 360 * the creation interval. If rpo_config is defined, then this must be <= 360 * targetRpoMinutes/(1440minutes/day) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_retain_days GkeBackupBackupPlan#backup_retain_days}
        :param locked: This flag denotes whether the retention policy of this BackupPlan is locked. If set to True, no further update is allowed on this policy, including the locked field itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#locked GkeBackupBackupPlan#locked}
        '''
        value = GkeBackupBackupPlanRetentionPolicy(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#create GkeBackupBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#delete GkeBackupBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#update GkeBackupBackupPlan#update}.
        '''
        value = GkeBackupBackupPlanTimeouts(
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
    def backup_config(self) -> "GkeBackupBackupPlanBackupConfigOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupConfigOutputReference", jsii.get(self, "backupConfig"))

    @builtins.property
    @jsii.member(jsii_name="backupSchedule")
    def backup_schedule(self) -> "GkeBackupBackupPlanBackupScheduleOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupScheduleOutputReference", jsii.get(self, "backupSchedule"))

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
    def retention_policy(self) -> "GkeBackupBackupPlanRetentionPolicyOutputReference":
        return typing.cast("GkeBackupBackupPlanRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

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
    def timeouts(self) -> "GkeBackupBackupPlanTimeoutsOutputReference":
        return typing.cast("GkeBackupBackupPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="backupConfigInput")
    def backup_config_input(self) -> typing.Optional["GkeBackupBackupPlanBackupConfig"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfig"], jsii.get(self, "backupConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="backupScheduleInput")
    def backup_schedule_input(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupSchedule"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupSchedule"], jsii.get(self, "backupScheduleInput"))

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
    ) -> typing.Optional["GkeBackupBackupPlanRetentionPolicy"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeBackupBackupPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeBackupBackupPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85b9477ec8833741d7efaa5ce3d430ff155373b89aff06a29cfb90a92666fcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3961fe53dba9e44f32a0fc74ec003e8b7fb3a3b0823ac766fcbc89c5525ebb16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deactivated", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25dc3773bad2e61d53f64c244f9695865ed0c7d9396f6924bf5a3360cabf036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb69cfefdff7dd6e69d7249c7eef3da68ae22b32631ab296449308308ad69d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebac30a61cecc8bdc186c3afd5b1838eba00f057f764cca1b146e4530d00d1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43c3da025ba04f1f12a0e6f436e86ebd24cf46a9214bcf372f1b284ba2967e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0cda817470a342ca8b50d8e5b849d2451cefdc7cd40aba9f23135af6bd288e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdaf015db88f4660762ca752b65a4f88e9d86f3d174e695fc4de960fcf9e2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfig",
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
class GkeBackupBackupPlanBackupConfig:
    def __init__(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_key: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_applications: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GkeBackupBackupPlanBackupConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, include all namespaced resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#all_namespaces GkeBackupBackupPlan#all_namespaces}
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#encryption_key GkeBackupBackupPlan#encryption_key}
        :param include_secrets: This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_secrets GkeBackupBackupPlan#include_secrets}
        :param include_volume_data: This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_volume_data GkeBackupBackupPlan#include_volume_data}
        :param permissive_mode: This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#permissive_mode GkeBackupBackupPlan#permissive_mode}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_applications GkeBackupBackupPlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_namespaces GkeBackupBackupPlan#selected_namespaces}
        '''
        if isinstance(encryption_key, dict):
            encryption_key = GkeBackupBackupPlanBackupConfigEncryptionKey(**encryption_key)
        if isinstance(selected_applications, dict):
            selected_applications = GkeBackupBackupPlanBackupConfigSelectedApplications(**selected_applications)
        if isinstance(selected_namespaces, dict):
            selected_namespaces = GkeBackupBackupPlanBackupConfigSelectedNamespaces(**selected_namespaces)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c6552aac644d4fde2f3f35c44dc6159a830d5eb55ebe22dfbe7ae649022807)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#all_namespaces GkeBackupBackupPlan#all_namespaces}
        '''
        result = self._values.get("all_namespaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupConfigEncryptionKey"]:
        '''encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#encryption_key GkeBackupBackupPlan#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfigEncryptionKey"], result)

    @builtins.property
    def include_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether Kubernetes Secret resources should be included when they fall into the scope of Backups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_secrets GkeBackupBackupPlan#include_secrets}
        '''
        result = self._values.get("include_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_volume_data(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether volume data should be backed up when PVCs are included in the scope of a Backup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#include_volume_data GkeBackupBackupPlan#include_volume_data}
        '''
        result = self._values.get("include_volume_data")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissive_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag specifies whether Backups will not fail when Backup for GKE detects Kubernetes configuration that is non-standard or requires additional setup to restore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#permissive_mode GkeBackupBackupPlan#permissive_mode}
        '''
        result = self._values.get("permissive_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selected_applications(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupConfigSelectedApplications"]:
        '''selected_applications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_applications GkeBackupBackupPlan#selected_applications}
        '''
        result = self._values.get("selected_applications")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfigSelectedApplications"], result)

    @builtins.property
    def selected_namespaces(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupConfigSelectedNamespaces"]:
        '''selected_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#selected_namespaces GkeBackupBackupPlan#selected_namespaces}
        '''
        result = self._values.get("selected_namespaces")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfigSelectedNamespaces"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"gcp_kms_encryption_key": "gcpKmsEncryptionKey"},
)
class GkeBackupBackupPlanBackupConfigEncryptionKey:
    def __init__(self, *, gcp_kms_encryption_key: builtins.str) -> None:
        '''
        :param gcp_kms_encryption_key: Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#gcp_kms_encryption_key GkeBackupBackupPlan#gcp_kms_encryption_key} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fffbe6b92a2298b775a851d1da78f651c0005a119331b43ded0d803e35d45ee)
            check_type(argname="argument gcp_kms_encryption_key", value=gcp_kms_encryption_key, expected_type=type_hints["gcp_kms_encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gcp_kms_encryption_key": gcp_kms_encryption_key,
        }

    @builtins.property
    def gcp_kms_encryption_key(self) -> builtins.str:
        '''Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#gcp_kms_encryption_key GkeBackupBackupPlan#gcp_kms_encryption_key}

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
        return "GkeBackupBackupPlanBackupConfigEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9f643da319e1dc071b7b4ae40065a630ee73229b7d35da7009bcceb352fba2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6924c601b2281d9c3b6afcfaae58812983b541e61ca4e07144f19ba02f339bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpKmsEncryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9af3c3421b80e3d81f0bafc65298569b332f393e482256f2f5fd0cff2950b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75e02239f8b80911efc4e25dfff5c1932061d89facf03826ce52314a1d6623ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEncryptionKey")
    def put_encryption_key(self, *, gcp_kms_encryption_key: builtins.str) -> None:
        '''
        :param gcp_kms_encryption_key: Google Cloud KMS encryption key. Format: projects/* /locations/* /keyRings/* /cryptoKeys/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#gcp_kms_encryption_key GkeBackupBackupPlan#gcp_kms_encryption_key} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GkeBackupBackupPlanBackupConfigEncryptionKey(
            gcp_kms_encryption_key=gcp_kms_encryption_key
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionKey", [value]))

    @jsii.member(jsii_name="putSelectedApplications")
    def put_selected_applications(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaced_names GkeBackupBackupPlan#namespaced_names}
        '''
        value = GkeBackupBackupPlanBackupConfigSelectedApplications(
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
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaces GkeBackupBackupPlan#namespaces}
        '''
        value = GkeBackupBackupPlanBackupConfigSelectedNamespaces(
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
    ) -> GkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference:
        return typing.cast(GkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplications")
    def selected_applications(
        self,
    ) -> "GkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference", jsii.get(self, "selectedApplications"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespaces")
    def selected_namespaces(
        self,
    ) -> "GkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference", jsii.get(self, "selectedNamespaces"))

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
    ) -> typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey], jsii.get(self, "encryptionKeyInput"))

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
    ) -> typing.Optional["GkeBackupBackupPlanBackupConfigSelectedApplications"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfigSelectedApplications"], jsii.get(self, "selectedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespacesInput")
    def selected_namespaces_input(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupConfigSelectedNamespaces"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupConfigSelectedNamespaces"], jsii.get(self, "selectedNamespacesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__668235f65797ca49e5b7a251fe1713edd47d5bf27b58577496d04af8f00d2a71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac1fa2ca6ef6d75a3d9fc0cf81cf0d1e2e24a2d68c1b198a6829508e006c24a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9585f84a23da6a92882631425f904f4ed57f90ec4d8f36984f1b37a55eb51157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed48df76f658316f21d029ccc86e6f2038953214832ecd7ce0c8af43082018f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissiveMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeBackupBackupPlanBackupConfig]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc4b895ae710edf83ab9d6eb8410033ee3179469ca3561cf9d5dc1f8ff4b734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedApplications",
    jsii_struct_bases=[],
    name_mapping={"namespaced_names": "namespacedNames"},
)
class GkeBackupBackupPlanBackupConfigSelectedApplications:
    def __init__(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaced_names GkeBackupBackupPlan#namespaced_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6702d6e41caf7ef4eb21ed69ff095735184afab3641c9dcc914ba7a5c0a82922)
            check_type(argname="argument namespaced_names", value=namespaced_names, expected_type=type_hints["namespaced_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaced_names": namespaced_names,
        }

    @builtins.property
    def namespaced_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames"]]:
        '''namespaced_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaced_names GkeBackupBackupPlan#namespaced_names}
        '''
        result = self._values.get("namespaced_names")
        assert result is not None, "Required property 'namespaced_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupConfigSelectedApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: The name of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#name GkeBackupBackupPlan#name}
        :param namespace: The namespace of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespace GkeBackupBackupPlan#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac269452265c7a356836e4bda3d34bcb54244692ca47298c4b02ddec9b574cdf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#name GkeBackupBackupPlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''The namespace of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespace GkeBackupBackupPlan#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f7f1cbedfe197202c660b028e28a824ee19c2c719734002500cd2d4f2b20af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6beed3481765c2221cc9fd97cf9e2007b3a70e7fc64ed9f5c3a1420e7e1eef81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a1310545a94e198ca5f1e1772d5e6fd1c210da58a0f20134fa892eefeaf613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7d6d42f8527c4f9a0271b0058fed00721600d077d307aec77a37018f12572a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d59a5e7c19b8388a38754a142fb4dac4ceabbeace0be0594e1d5d52862046f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610f6b0aa8212f603aaa92aa73e1a33026e9d8a74bb18f37fc479ec12221915f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbba4bb94698996fbbc4580e1531bfc68efc803b58678a3d4fe220aa2205646c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac9f240485576c6a396bad907576a5b26f134b17a3aebc29a6be37af7aba975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6578c8225f6e515e269a7f20cee5be016d29dd6f5a783c44fa7654b6be93cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4872109e2e69d7fb2759cb623170340d9350fca1ace2a34b15fa2542669e9699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38928ec2953f39b3fd5e91c24c136bdc65fea7b2928f1a7c27799064fa44ea41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespacedNames")
    def put_namespaced_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f860150ed36cce6cb9e9e90414b9fa6421718e1395454373d83a92998f265320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespacedNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="namespacedNames")
    def namespaced_names(
        self,
    ) -> GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList:
        return typing.cast(GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList, jsii.get(self, "namespacedNames"))

    @builtins.property
    @jsii.member(jsii_name="namespacedNamesInput")
    def namespaced_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "namespacedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupConfigSelectedApplications]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfigSelectedApplications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupConfigSelectedApplications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32da7b5712b50826dca034f121d05eed54520b365624b315ad843ff0fd5b5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GkeBackupBackupPlanBackupConfigSelectedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaces GkeBackupBackupPlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa94c6c8178e72116bce855f2727cd93c24fab6cb0ac0171701d88fba0637878)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#namespaces GkeBackupBackupPlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupConfigSelectedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f7b612a6f83bf05dcc07f352e45d70d8b7aa4fe405339743655f7e5d81ca385)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdd0eca45af15821bbf2e3b7b7b0779b62c991492bf4d18523f11f136b026332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupConfigSelectedNamespaces]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfigSelectedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupConfigSelectedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c23242fa647c857d4a23acc6efc17cb1202aa3eb972110aa088760536dfd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "cron_schedule": "cronSchedule",
        "paused": "paused",
        "rpo_config": "rpoConfig",
    },
)
class GkeBackupBackupPlanBackupSchedule:
    def __init__(
        self,
        *,
        cron_schedule: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rpo_config: typing.Optional[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cron_schedule: A standard cron string that defines a repeating schedule for creating Backups via this BackupPlan. This is mutually exclusive with the rpoConfig field since at most one schedule can be defined for a BackupPlan. If this is defined, then backupRetainDays must also be defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cron_schedule GkeBackupBackupPlan#cron_schedule}
        :param paused: This flag denotes whether automatic Backup creation is paused for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#paused GkeBackupBackupPlan#paused}
        :param rpo_config: rpo_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#rpo_config GkeBackupBackupPlan#rpo_config}
        '''
        if isinstance(rpo_config, dict):
            rpo_config = GkeBackupBackupPlanBackupScheduleRpoConfig(**rpo_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993c0e4b597feea9a15cef0b204096cfea22b258ae2b2b03f15b340b237482a3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cron_schedule GkeBackupBackupPlan#cron_schedule}
        '''
        result = self._values.get("cron_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag denotes whether automatic Backup creation is paused for this BackupPlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#paused GkeBackupBackupPlan#paused}
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rpo_config(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfig"]:
        '''rpo_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#rpo_config GkeBackupBackupPlan#rpo_config}
        '''
        result = self._values.get("rpo_config")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94a8109f2a0b365639d4b0694142b53fd6bdf4f4fd01ab1cd5da85a62a7b585a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRpoConfig")
    def put_rpo_config(
        self,
        *,
        target_rpo_minutes: jsii.Number,
        exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param target_rpo_minutes: Defines the target RPO for the BackupPlan in minutes, which means the target maximum data loss in time that is acceptable for this BackupPlan. This must be at least 60, i.e., 1 hour, and at most 86400, i.e., 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#target_rpo_minutes GkeBackupBackupPlan#target_rpo_minutes}
        :param exclusion_windows: exclusion_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#exclusion_windows GkeBackupBackupPlan#exclusion_windows}
        '''
        value = GkeBackupBackupPlanBackupScheduleRpoConfig(
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
    def rpo_config(self) -> "GkeBackupBackupPlanBackupScheduleRpoConfigOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupScheduleRpoConfigOutputReference", jsii.get(self, "rpoConfig"))

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
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfig"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfig"], jsii.get(self, "rpoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cronSchedule")
    def cron_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSchedule"))

    @cron_schedule.setter
    def cron_schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e6c8291f8b82c03e555601e597c7850710436ddd333e85ab1cf07b851daf5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c3a645aa7a5078001d5c6bcf9bd1be4407b43a6fffe082fc0d62f87feb08146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeBackupBackupPlanBackupSchedule]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bd36df758e4f82c8c18e81f6f1ac5f30b6bff542c1a47ffb2b7d89051c3204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "target_rpo_minutes": "targetRpoMinutes",
        "exclusion_windows": "exclusionWindows",
    },
)
class GkeBackupBackupPlanBackupScheduleRpoConfig:
    def __init__(
        self,
        *,
        target_rpo_minutes: jsii.Number,
        exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param target_rpo_minutes: Defines the target RPO for the BackupPlan in minutes, which means the target maximum data loss in time that is acceptable for this BackupPlan. This must be at least 60, i.e., 1 hour, and at most 86400, i.e., 60 days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#target_rpo_minutes GkeBackupBackupPlan#target_rpo_minutes}
        :param exclusion_windows: exclusion_windows block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#exclusion_windows GkeBackupBackupPlan#exclusion_windows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461ca1216c514fc7dd4346450731f70a94b40b90e613f5d3bb05836cae680fb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#target_rpo_minutes GkeBackupBackupPlan#target_rpo_minutes}
        '''
        result = self._values.get("target_rpo_minutes")
        assert result is not None, "Required property 'target_rpo_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def exclusion_windows(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows"]]]:
        '''exclusion_windows block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#exclusion_windows GkeBackupBackupPlan#exclusion_windows}
        '''
        result = self._values.get("exclusion_windows")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupScheduleRpoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "start_time": "startTime",
        "daily": "daily",
        "days_of_week": "daysOfWeek",
        "single_occurrence_date": "singleOccurrenceDate",
    },
)
class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows:
    def __init__(
        self,
        *,
        duration: builtins.str,
        start_time: typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime", typing.Dict[builtins.str, typing.Any]],
        daily: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        days_of_week: typing.Optional[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek", typing.Dict[builtins.str, typing.Any]]] = None,
        single_occurrence_date: typing.Optional[typing.Union["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param duration: Specifies duration of the window in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Restrictions for duration based on the recurrence type to allow some time for backup to happen: - single_occurrence_date: no restriction - daily window: duration < 24 hours - weekly window: - days of week includes all seven days of a week: duration < 24 hours - all other weekly window: duration < 168 hours (i.e., 24 * 7 hours) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#duration GkeBackupBackupPlan#duration}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#start_time GkeBackupBackupPlan#start_time}
        :param daily: The exclusion window occurs every day if set to "True". Specifying this field to "False" is an error. Only one of singleOccurrenceDate, daily and daysOfWeek may be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#daily GkeBackupBackupPlan#daily}
        :param days_of_week: days_of_week block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#days_of_week GkeBackupBackupPlan#days_of_week}
        :param single_occurrence_date: single_occurrence_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#single_occurrence_date GkeBackupBackupPlan#single_occurrence_date}
        '''
        if isinstance(start_time, dict):
            start_time = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(**start_time)
        if isinstance(days_of_week, dict):
            days_of_week = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(**days_of_week)
        if isinstance(single_occurrence_date, dict):
            single_occurrence_date = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(**single_occurrence_date)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a311c37dd09ea21b939dff70760332c8298c3335dc9c0586616067560718777)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#duration GkeBackupBackupPlan#duration}
        '''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(
        self,
    ) -> "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#start_time GkeBackupBackupPlan#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime", result)

    @builtins.property
    def daily(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The exclusion window occurs every day if set to "True".

        Specifying this field to "False" is an error.
        Only one of singleOccurrenceDate, daily and daysOfWeek may be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#daily GkeBackupBackupPlan#daily}
        '''
        result = self._values.get("daily")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def days_of_week(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek"]:
        '''days_of_week block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#days_of_week GkeBackupBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek"], result)

    @builtins.property
    def single_occurrence_date(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"]:
        '''single_occurrence_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#single_occurrence_date GkeBackupBackupPlan#single_occurrence_date}
        '''
        result = self._values.get("single_occurrence_date")
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek",
    jsii_struct_bases=[],
    name_mapping={"days_of_week": "daysOfWeek"},
)
class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek:
    def __init__(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param days_of_week: A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#days_of_week GkeBackupBackupPlan#days_of_week}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342bf3a6ba8a86a679ece8b9ef009359d2727796d4959f0f3036e32dc7ecb0e9)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#days_of_week GkeBackupBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20dd308e17f6d7afb60b28d311e96de3d8b6c983ced9274b771dc1b1a31a730)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23d2a90c7f87a86da2afe4ab7ee05c3079edcc91ae2ceb41a1c068645daf0a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e256186705c1493eabbb7b349701d60992079ee78f5269cd8977b81b9496a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8feabebd11792091d6c97bd4445d78d3f99e4cebc9af054a89f83b9d5de2f73f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6db52499d44e34ed1b678fcdf1db00af39404cd08363ac72f53fbf2c638962e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0f3f6b31b72ed8c970ea194e916f6475408ed8e6a964e33015b47994b7b6d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fa4ace15237e80696c0f19e0f888f27280382b9c174778dc6b8b34a36e3617d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__769c7444650a20a68748e01881f8f8345a0d6a52d95ba7d2d918e3371cd4f2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b877d18f28cdc0933197676192a281c9a7b6a9d7c3d8cb48ac8a21ba516d177c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08bc6b720825df545cae69142b957ff11d1dfb2629b9624ea8cead0e9cbc6779)
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
        :param days_of_week: A list of days of week. Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#days_of_week GkeBackupBackupPlan#days_of_week}
        '''
        value = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek(
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
        :param day: Day of a month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#day GkeBackupBackupPlan#day}
        :param month: Month of a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#month GkeBackupBackupPlan#month}
        :param year: Year of the date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#year GkeBackupBackupPlan#year}
        '''
        value = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(
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
        :param hours: Hours of day in 24 hour format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#hours GkeBackupBackupPlan#hours}
        :param minutes: Minutes of hour of day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#minutes GkeBackupBackupPlan#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#nanos GkeBackupBackupPlan#nanos}
        :param seconds: Seconds of minutes of the time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#seconds GkeBackupBackupPlan#seconds}
        '''
        value = GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(
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
    ) -> GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference:
        return typing.cast(GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference, jsii.get(self, "daysOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="singleOccurrenceDate")
    def single_occurrence_date(
        self,
    ) -> "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference", jsii.get(self, "singleOccurrenceDate"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference":
        return typing.cast("GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference", jsii.get(self, "startTime"))

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
    ) -> typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="singleOccurrenceDateInput")
    def single_occurrence_date_input(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate"], jsii.get(self, "singleOccurrenceDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime"]:
        return typing.cast(typing.Optional["GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime"], jsii.get(self, "startTimeInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__95d7e8e975f0536d11fa2f5bd2ca63880a7609503e05a09a65d88333174431cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daily", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562248e9eaa9e11bba8f7388e48511d96e70a6687bef3ac5a6852f57321f1947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d92504cf1212f7621577cd396e23dd74dfbf107004b8175ca0c26c79a206ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#day GkeBackupBackupPlan#day}
        :param month: Month of a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#month GkeBackupBackupPlan#month}
        :param year: Year of the date. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#year GkeBackupBackupPlan#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411fbc6ca3d805c5cf6dda15b10eaa54e1fbb1ed0c7f589747ab5be3423606cc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#day GkeBackupBackupPlan#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#month GkeBackupBackupPlan#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#year GkeBackupBackupPlan#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d14aef306a35b9dcabd07e4dbe55db920b4f4ffeaa512adabac8d900ae281ef8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2027837a3fa23b16940f62cc1a8cf5e943c1c50767e9d14e78d94c8d90092e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fdc20cd0f31dfdfe795fbfa852674bb1863bb5a107c4d725884e03d3445f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bff863120daffe27a0aea6898c6f52d0d212b83a61b55268b83775687d6d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb986b1fec7b0317d48f6b16f9f30b26447d75413c153dd0b27d8c1b6cc8747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#hours GkeBackupBackupPlan#hours}
        :param minutes: Minutes of hour of day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#minutes GkeBackupBackupPlan#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#nanos GkeBackupBackupPlan#nanos}
        :param seconds: Seconds of minutes of the time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#seconds GkeBackupBackupPlan#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d8912efd38cf8f1abc7b1b68c59dea087b414dacbabecaf67f5742801b2632)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#hours GkeBackupBackupPlan#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#minutes GkeBackupBackupPlan#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#nanos GkeBackupBackupPlan#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#seconds GkeBackupBackupPlan#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac7cc47751308e2959459db57553275a3286c02af86dae7e971ef7cc5c68cdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccf9e44f639ceaa659b73e6b1d576e638d0155dbf0d7a57d14aee74b82250c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ec382cb6c392b2fbb456a161da4906fbc6288e4607a09810c84a4abf24bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4716984cf80218a92060cfce9af0ee45d8c8e461f4c062e2d1a0819cab2c0c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177268bebe0280c375e9814ba55dea45737a9e4397512a2bdbf53413191d0458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc3667d7a3f3bb047cab3e0f5621d8dc015c2481efc198476d18aed942fd962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupBackupPlanBackupScheduleRpoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanBackupScheduleRpoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35fa2e34a0fcbd8096e0fecfb2e6fdafe85d5ac8dee19492b0107b61d06b8afe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionWindows")
    def put_exclusion_windows(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c24addc299a2a98a4be7d11346c69f9d349d01f87b2ce26cfe5ce4af0401cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionWindows", [value]))

    @jsii.member(jsii_name="resetExclusionWindows")
    def reset_exclusion_windows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionWindows", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionWindows")
    def exclusion_windows(
        self,
    ) -> GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList:
        return typing.cast(GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList, jsii.get(self, "exclusionWindows"))

    @builtins.property
    @jsii.member(jsii_name="exclusionWindowsInput")
    def exclusion_windows_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]], jsii.get(self, "exclusionWindowsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9c003e30c39b5337fe147b3571e6482aedfd2b344e17fa13fec09f563a1202b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRpoMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfig]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b73d03c8d314329999f962c59d5404d8d912fe3221c2b84be223a8f725e523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanConfig",
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
class GkeBackupBackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_config: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_schedule: typing.Optional[typing.Union[GkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
        deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["GkeBackupBackupPlanRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GkeBackupBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: The source cluster from which Backups will be created via this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cluster GkeBackupBackupPlan#cluster}
        :param location: The region of the Backup Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#location GkeBackupBackupPlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#name GkeBackupBackupPlan#name}
        :param backup_config: backup_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_config GkeBackupBackupPlan#backup_config}
        :param backup_schedule: backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_schedule GkeBackupBackupPlan#backup_schedule}
        :param deactivated: This flag indicates whether this BackupPlan has been deactivated. Setting this field to True locks the BackupPlan such that no further updates will be allowed (except deletes), including the deactivated field itself. It also prevents any new Backups from being created via this BackupPlan (including scheduled Backups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#deactivated GkeBackupBackupPlan#deactivated}
        :param description: User specified descriptive string for this BackupPlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#description GkeBackupBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#id GkeBackupBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#labels GkeBackupBackupPlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#project GkeBackupBackupPlan#project}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#retention_policy GkeBackupBackupPlan#retention_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#timeouts GkeBackupBackupPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backup_config, dict):
            backup_config = GkeBackupBackupPlanBackupConfig(**backup_config)
        if isinstance(backup_schedule, dict):
            backup_schedule = GkeBackupBackupPlanBackupSchedule(**backup_schedule)
        if isinstance(retention_policy, dict):
            retention_policy = GkeBackupBackupPlanRetentionPolicy(**retention_policy)
        if isinstance(timeouts, dict):
            timeouts = GkeBackupBackupPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e1e7501f743f664eabe96e9c551872530864057deafaf152470870746356f1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#cluster GkeBackupBackupPlan#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Backup Plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#location GkeBackupBackupPlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The full name of the BackupPlan Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#name GkeBackupBackupPlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_config(self) -> typing.Optional[GkeBackupBackupPlanBackupConfig]:
        '''backup_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_config GkeBackupBackupPlan#backup_config}
        '''
        result = self._values.get("backup_config")
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupConfig], result)

    @builtins.property
    def backup_schedule(self) -> typing.Optional[GkeBackupBackupPlanBackupSchedule]:
        '''backup_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_schedule GkeBackupBackupPlan#backup_schedule}
        '''
        result = self._values.get("backup_schedule")
        return typing.cast(typing.Optional[GkeBackupBackupPlanBackupSchedule], result)

    @builtins.property
    def deactivated(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag indicates whether this BackupPlan has been deactivated.

        Setting this field to True locks the BackupPlan such that no further updates will be allowed
        (except deletes), including the deactivated field itself. It also prevents any new Backups
        from being created via this BackupPlan (including scheduled Backups).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#deactivated GkeBackupBackupPlan#deactivated}
        '''
        result = self._values.get("deactivated")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User specified descriptive string for this BackupPlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#description GkeBackupBackupPlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#id GkeBackupBackupPlan#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#labels GkeBackupBackupPlan#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#project GkeBackupBackupPlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional["GkeBackupBackupPlanRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#retention_policy GkeBackupBackupPlan#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["GkeBackupBackupPlanRetentionPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeBackupBackupPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#timeouts GkeBackupBackupPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeBackupBackupPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "backup_delete_lock_days": "backupDeleteLockDays",
        "backup_retain_days": "backupRetainDays",
        "locked": "locked",
    },
)
class GkeBackupBackupPlanRetentionPolicy:
    def __init__(
        self,
        *,
        backup_delete_lock_days: typing.Optional[jsii.Number] = None,
        backup_retain_days: typing.Optional[jsii.Number] = None,
        locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param backup_delete_lock_days: Minimum age for a Backup created via this BackupPlan (in days). Must be an integer value between 0-90 (inclusive). A Backup created under this BackupPlan will not be deletable until it reaches Backup's (create time + backup_delete_lock_days). Updating this field of a BackupPlan does not affect existing Backups. Backups created after a successful update will inherit this new value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_delete_lock_days GkeBackupBackupPlan#backup_delete_lock_days}
        :param backup_retain_days: The default maximum age of a Backup created via this BackupPlan. This field MUST be an integer value >= 0 and <= 365. If specified, a Backup created under this BackupPlan will be automatically deleted after its age reaches (createTime + backupRetainDays). If not specified, Backups created under this BackupPlan will NOT be subject to automatic deletion. Updating this field does NOT affect existing Backups under it. Backups created AFTER a successful update will automatically pick up the new value. NOTE: backupRetainDays must be >= backupDeleteLockDays. If cronSchedule is defined, then this must be <= 360 * the creation interval. If rpo_config is defined, then this must be <= 360 * targetRpoMinutes/(1440minutes/day) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_retain_days GkeBackupBackupPlan#backup_retain_days}
        :param locked: This flag denotes whether the retention policy of this BackupPlan is locked. If set to True, no further update is allowed on this policy, including the locked field itself. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#locked GkeBackupBackupPlan#locked}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9881199f93bf223b7b84510430b1066715538a2f450d2554020254328a7afe)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_delete_lock_days GkeBackupBackupPlan#backup_delete_lock_days}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#backup_retain_days GkeBackupBackupPlan#backup_retain_days}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#locked GkeBackupBackupPlan#locked}
        '''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b70f0a06ec1123e7557962f398d9c74c9094ba13e80f3ffbebcc6b1acb60966b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdcd28123afb0f60d20457d64d4df24781a35d1bf259f78b5bfcbcfec4bb81c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupDeleteLockDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupRetainDays")
    def backup_retain_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetainDays"))

    @backup_retain_days.setter
    def backup_retain_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4e7f0ee7ab944d23b95b560984b5403170f290554e3f527ab523325f659a5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d57a64517e2c1f8a9561709657c82dafa48071314fff6c6005d25f17ac818cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locked", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeBackupBackupPlanRetentionPolicy]:
        return typing.cast(typing.Optional[GkeBackupBackupPlanRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupBackupPlanRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a607789d3f62ebaf6e33bf2e291150665fca4b83dc412a7531dac2b96fb0537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeBackupBackupPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#create GkeBackupBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#delete GkeBackupBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#update GkeBackupBackupPlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31cd7a17ee7470cd8881d65686abe3261ba8092241c76733529a5f2451de5a0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#create GkeBackupBackupPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#delete GkeBackupBackupPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_backup_plan#update GkeBackupBackupPlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupBackupPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupBackupPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupBackupPlan.GkeBackupBackupPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e686025067c2c88df9dee677bb0dd54a587867947c92132e8072b7b49ecc61d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c9f0a086f78f20e2bfa787ee89ae31eb3a89ba0ee25cc619f7db847228acb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c334aa4e010d02e2da5b41b12cc2a646b9169a73384672a875dd68e370cd9fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d276d9d36fbc9a4bd848e8532f228e334e9e3ad76f871e50f03b3cef5dc72cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41526e487593b4cc8c265622bee3d439e867a65b92889d8d26b8fd40185d97b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeBackupBackupPlan",
    "GkeBackupBackupPlanBackupConfig",
    "GkeBackupBackupPlanBackupConfigEncryptionKey",
    "GkeBackupBackupPlanBackupConfigEncryptionKeyOutputReference",
    "GkeBackupBackupPlanBackupConfigOutputReference",
    "GkeBackupBackupPlanBackupConfigSelectedApplications",
    "GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames",
    "GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesList",
    "GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNamesOutputReference",
    "GkeBackupBackupPlanBackupConfigSelectedApplicationsOutputReference",
    "GkeBackupBackupPlanBackupConfigSelectedNamespaces",
    "GkeBackupBackupPlanBackupConfigSelectedNamespacesOutputReference",
    "GkeBackupBackupPlanBackupSchedule",
    "GkeBackupBackupPlanBackupScheduleOutputReference",
    "GkeBackupBackupPlanBackupScheduleRpoConfig",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeekOutputReference",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsList",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsOutputReference",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDateOutputReference",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime",
    "GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTimeOutputReference",
    "GkeBackupBackupPlanBackupScheduleRpoConfigOutputReference",
    "GkeBackupBackupPlanConfig",
    "GkeBackupBackupPlanRetentionPolicy",
    "GkeBackupBackupPlanRetentionPolicyOutputReference",
    "GkeBackupBackupPlanTimeouts",
    "GkeBackupBackupPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d365f7e9987d7729b1f43b96f442782fae040655a29dacfce586ede86ff63de1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    backup_config: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_schedule: typing.Optional[typing.Union[GkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[GkeBackupBackupPlanRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeBackupBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a4bf6055d9436465e3427bee2021db1eed11377460c45909b9c035514d9d3495(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85b9477ec8833741d7efaa5ce3d430ff155373b89aff06a29cfb90a92666fcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3961fe53dba9e44f32a0fc74ec003e8b7fb3a3b0823ac766fcbc89c5525ebb16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25dc3773bad2e61d53f64c244f9695865ed0c7d9396f6924bf5a3360cabf036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb69cfefdff7dd6e69d7249c7eef3da68ae22b32631ab296449308308ad69d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebac30a61cecc8bdc186c3afd5b1838eba00f057f764cca1b146e4530d00d1fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43c3da025ba04f1f12a0e6f436e86ebd24cf46a9214bcf372f1b284ba2967e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0cda817470a342ca8b50d8e5b849d2451cefdc7cd40aba9f23135af6bd288e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdaf015db88f4660762ca752b65a4f88e9d86f3d174e695fc4de960fcf9e2a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c6552aac644d4fde2f3f35c44dc6159a830d5eb55ebe22dfbe7ae649022807(
    *,
    all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_key: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfigEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    include_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_volume_data: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissive_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selected_applications: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfigSelectedApplications, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_namespaces: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfigSelectedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fffbe6b92a2298b775a851d1da78f651c0005a119331b43ded0d803e35d45ee(
    *,
    gcp_kms_encryption_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f643da319e1dc071b7b4ae40065a630ee73229b7d35da7009bcceb352fba2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6924c601b2281d9c3b6afcfaae58812983b541e61ca4e07144f19ba02f339bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9af3c3421b80e3d81f0bafc65298569b332f393e482256f2f5fd0cff2950b0(
    value: typing.Optional[GkeBackupBackupPlanBackupConfigEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e02239f8b80911efc4e25dfff5c1932061d89facf03826ce52314a1d6623ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668235f65797ca49e5b7a251fe1713edd47d5bf27b58577496d04af8f00d2a71(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac1fa2ca6ef6d75a3d9fc0cf81cf0d1e2e24a2d68c1b198a6829508e006c24a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9585f84a23da6a92882631425f904f4ed57f90ec4d8f36984f1b37a55eb51157(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed48df76f658316f21d029ccc86e6f2038953214832ecd7ce0c8af43082018f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc4b895ae710edf83ab9d6eb8410033ee3179469ca3561cf9d5dc1f8ff4b734(
    value: typing.Optional[GkeBackupBackupPlanBackupConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6702d6e41caf7ef4eb21ed69ff095735184afab3641c9dcc914ba7a5c0a82922(
    *,
    namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac269452265c7a356836e4bda3d34bcb54244692ca47298c4b02ddec9b574cdf(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f7f1cbedfe197202c660b028e28a824ee19c2c719734002500cd2d4f2b20af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6beed3481765c2221cc9fd97cf9e2007b3a70e7fc64ed9f5c3a1420e7e1eef81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a1310545a94e198ca5f1e1772d5e6fd1c210da58a0f20134fa892eefeaf613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d6d42f8527c4f9a0271b0058fed00721600d077d307aec77a37018f12572a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d59a5e7c19b8388a38754a142fb4dac4ceabbeace0be0594e1d5d52862046f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610f6b0aa8212f603aaa92aa73e1a33026e9d8a74bb18f37fc479ec12221915f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbba4bb94698996fbbc4580e1531bfc68efc803b58678a3d4fe220aa2205646c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac9f240485576c6a396bad907576a5b26f134b17a3aebc29a6be37af7aba975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6578c8225f6e515e269a7f20cee5be016d29dd6f5a783c44fa7654b6be93cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4872109e2e69d7fb2759cb623170340d9350fca1ace2a34b15fa2542669e9699(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38928ec2953f39b3fd5e91c24c136bdc65fea7b2928f1a7c27799064fa44ea41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f860150ed36cce6cb9e9e90414b9fa6421718e1395454373d83a92998f265320(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32da7b5712b50826dca034f121d05eed54520b365624b315ad843ff0fd5b5eb(
    value: typing.Optional[GkeBackupBackupPlanBackupConfigSelectedApplications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa94c6c8178e72116bce855f2727cd93c24fab6cb0ac0171701d88fba0637878(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7b612a6f83bf05dcc07f352e45d70d8b7aa4fe405339743655f7e5d81ca385(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd0eca45af15821bbf2e3b7b7b0779b62c991492bf4d18523f11f136b026332(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c23242fa647c857d4a23acc6efc17cb1202aa3eb972110aa088760536dfd1e(
    value: typing.Optional[GkeBackupBackupPlanBackupConfigSelectedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993c0e4b597feea9a15cef0b204096cfea22b258ae2b2b03f15b340b237482a3(
    *,
    cron_schedule: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rpo_config: typing.Optional[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a8109f2a0b365639d4b0694142b53fd6bdf4f4fd01ab1cd5da85a62a7b585a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e6c8291f8b82c03e555601e597c7850710436ddd333e85ab1cf07b851daf5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3a645aa7a5078001d5c6bcf9bd1be4407b43a6fffe082fc0d62f87feb08146(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bd36df758e4f82c8c18e81f6f1ac5f30b6bff542c1a47ffb2b7d89051c3204(
    value: typing.Optional[GkeBackupBackupPlanBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461ca1216c514fc7dd4346450731f70a94b40b90e613f5d3bb05836cae680fb(
    *,
    target_rpo_minutes: jsii.Number,
    exclusion_windows: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a311c37dd09ea21b939dff70760332c8298c3335dc9c0586616067560718777(
    *,
    duration: builtins.str,
    start_time: typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime, typing.Dict[builtins.str, typing.Any]],
    daily: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    days_of_week: typing.Optional[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek, typing.Dict[builtins.str, typing.Any]]] = None,
    single_occurrence_date: typing.Optional[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342bf3a6ba8a86a679ece8b9ef009359d2727796d4959f0f3036e32dc7ecb0e9(
    *,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20dd308e17f6d7afb60b28d311e96de3d8b6c983ced9274b771dc1b1a31a730(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d2a90c7f87a86da2afe4ab7ee05c3079edcc91ae2ceb41a1c068645daf0a22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e256186705c1493eabbb7b349701d60992079ee78f5269cd8977b81b9496a972(
    value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsDaysOfWeek],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8feabebd11792091d6c97bd4445d78d3f99e4cebc9af054a89f83b9d5de2f73f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6db52499d44e34ed1b678fcdf1db00af39404cd08363ac72f53fbf2c638962e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0f3f6b31b72ed8c970ea194e916f6475408ed8e6a964e33015b47994b7b6d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa4ace15237e80696c0f19e0f888f27280382b9c174778dc6b8b34a36e3617d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769c7444650a20a68748e01881f8f8345a0d6a52d95ba7d2d918e3371cd4f2b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b877d18f28cdc0933197676192a281c9a7b6a9d7c3d8cb48ac8a21ba516d177c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bc6b720825df545cae69142b957ff11d1dfb2629b9624ea8cead0e9cbc6779(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d7e8e975f0536d11fa2f5bd2ca63880a7609503e05a09a65d88333174431cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562248e9eaa9e11bba8f7388e48511d96e70a6687bef3ac5a6852f57321f1947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d92504cf1212f7621577cd396e23dd74dfbf107004b8175ca0c26c79a206ac1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411fbc6ca3d805c5cf6dda15b10eaa54e1fbb1ed0c7f589747ab5be3423606cc(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14aef306a35b9dcabd07e4dbe55db920b4f4ffeaa512adabac8d900ae281ef8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2027837a3fa23b16940f62cc1a8cf5e943c1c50767e9d14e78d94c8d90092e02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fdc20cd0f31dfdfe795fbfa852674bb1863bb5a107c4d725884e03d3445f78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bff863120daffe27a0aea6898c6f52d0d212b83a61b55268b83775687d6d73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb986b1fec7b0317d48f6b16f9f30b26447d75413c153dd0b27d8c1b6cc8747(
    value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsSingleOccurrenceDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d8912efd38cf8f1abc7b1b68c59dea087b414dacbabecaf67f5742801b2632(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac7cc47751308e2959459db57553275a3286c02af86dae7e971ef7cc5c68cdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf9e44f639ceaa659b73e6b1d576e638d0155dbf0d7a57d14aee74b82250c87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ec382cb6c392b2fbb456a161da4906fbc6288e4607a09810c84a4abf24bf9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4716984cf80218a92060cfce9af0ee45d8c8e461f4c062e2d1a0819cab2c0c45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177268bebe0280c375e9814ba55dea45737a9e4397512a2bdbf53413191d0458(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc3667d7a3f3bb047cab3e0f5621d8dc015c2481efc198476d18aed942fd962(
    value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindowsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fa2e34a0fcbd8096e0fecfb2e6fdafe85d5ac8dee19492b0107b61d06b8afe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c24addc299a2a98a4be7d11346c69f9d349d01f87b2ce26cfe5ce4af0401cd1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupBackupPlanBackupScheduleRpoConfigExclusionWindows, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c003e30c39b5337fe147b3571e6482aedfd2b344e17fa13fec09f563a1202b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b73d03c8d314329999f962c59d5404d8d912fe3221c2b84be223a8f725e523(
    value: typing.Optional[GkeBackupBackupPlanBackupScheduleRpoConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e1e7501f743f664eabe96e9c551872530864057deafaf152470870746356f1(
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
    backup_config: typing.Optional[typing.Union[GkeBackupBackupPlanBackupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_schedule: typing.Optional[typing.Union[GkeBackupBackupPlanBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    deactivated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[GkeBackupBackupPlanRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GkeBackupBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9881199f93bf223b7b84510430b1066715538a2f450d2554020254328a7afe(
    *,
    backup_delete_lock_days: typing.Optional[jsii.Number] = None,
    backup_retain_days: typing.Optional[jsii.Number] = None,
    locked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70f0a06ec1123e7557962f398d9c74c9094ba13e80f3ffbebcc6b1acb60966b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcd28123afb0f60d20457d64d4df24781a35d1bf259f78b5bfcbcfec4bb81c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4e7f0ee7ab944d23b95b560984b5403170f290554e3f527ab523325f659a5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d57a64517e2c1f8a9561709657c82dafa48071314fff6c6005d25f17ac818cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a607789d3f62ebaf6e33bf2e291150665fca4b83dc412a7531dac2b96fb0537(
    value: typing.Optional[GkeBackupBackupPlanRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31cd7a17ee7470cd8881d65686abe3261ba8092241c76733529a5f2451de5a0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e686025067c2c88df9dee677bb0dd54a587867947c92132e8072b7b49ecc61d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9f0a086f78f20e2bfa787ee89ae31eb3a89ba0ee25cc619f7db847228acb3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c334aa4e010d02e2da5b41b12cc2a646b9169a73384672a875dd68e370cd9fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d276d9d36fbc9a4bd848e8532f228e334e9e3ad76f871e50f03b3cef5dc72cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41526e487593b4cc8c265622bee3d439e867a65b92889d8d26b8fd40185d97b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupBackupPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

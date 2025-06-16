r'''
# `google_gke_backup_restore_plan`

Refer to the Terraform Registry for docs: [`google_gke_backup_restore_plan`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan).
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


class GoogleGkeBackupRestorePlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan google_gke_backup_restore_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_plan: builtins.str,
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        restore_config: typing.Union["GoogleGkeBackupRestorePlanRestoreConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan google_gke_backup_restore_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_plan: A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#backup_plan GoogleGkeBackupRestorePlan#backup_plan}
        :param cluster: The source cluster from which Restores will be created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster GoogleGkeBackupRestorePlan#cluster}
        :param location: The region of the Restore Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#location GoogleGkeBackupRestorePlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#name GoogleGkeBackupRestorePlan#name}
        :param restore_config: restore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_config GoogleGkeBackupRestorePlan#restore_config}
        :param description: User specified descriptive string for this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#description GoogleGkeBackupRestorePlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#id GoogleGkeBackupRestorePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#labels GoogleGkeBackupRestorePlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#project GoogleGkeBackupRestorePlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#timeouts GoogleGkeBackupRestorePlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa0de077a2bfd6d8332250d005d26a8dc7befc3f2cc9a0a9425c4ccb3549177)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeBackupRestorePlanConfig(
            backup_plan=backup_plan,
            cluster=cluster,
            location=location,
            name=name,
            restore_config=restore_config,
            description=description,
            id=id,
            labels=labels,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleGkeBackupRestorePlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleGkeBackupRestorePlan to import.
        :param import_from_id: The id of the existing GoogleGkeBackupRestorePlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleGkeBackupRestorePlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d64fb3872f5fa03eff0cc56b1d7d2591afa594f70390236eb5c4c325f7c0e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRestoreConfig")
    def put_restore_config(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_resource_conflict_policy: typing.Optional[builtins.str] = None,
        cluster_resource_restore_scope: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_namespaces: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
        no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_order: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_applications: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_data_restore_policy: typing.Optional[builtins.str] = None,
        volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, restore all namespaced resources in the Backup. Setting this field to False will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_namespaces GoogleGkeBackupRestorePlan#all_namespaces}
        :param cluster_resource_conflict_policy: Defines the behavior for handling the situation where cluster-scoped resources being restored already exist in the target cluster. This MUST be set to a value other than 'CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED' if 'clusterResourceRestoreScope' is anyting other than 'noGroupKinds'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#clusterresourceconflictpolicy for more information on each policy option. Possible values: ["USE_EXISTING_VERSION", "USE_BACKUP_VERSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_conflict_policy GoogleGkeBackupRestorePlan#cluster_resource_conflict_policy}
        :param cluster_resource_restore_scope: cluster_resource_restore_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_restore_scope GoogleGkeBackupRestorePlan#cluster_resource_restore_scope}
        :param excluded_namespaces: excluded_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_namespaces GoogleGkeBackupRestorePlan#excluded_namespaces}
        :param namespaced_resource_restore_mode: Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster. This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_resource_restore_mode GoogleGkeBackupRestorePlan#namespaced_resource_restore_mode}
        :param no_namespaces: Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_namespaces GoogleGkeBackupRestorePlan#no_namespaces}
        :param restore_order: restore_order block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_order GoogleGkeBackupRestorePlan#restore_order}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_applications GoogleGkeBackupRestorePlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_namespaces GoogleGkeBackupRestorePlan#selected_namespaces}
        :param transformation_rules: transformation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#transformation_rules GoogleGkeBackupRestorePlan#transformation_rules}
        :param volume_data_restore_policy: Specifies the mechanism to be used to restore volume data. This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy GoogleGkeBackupRestorePlan#volume_data_restore_policy}
        :param volume_data_restore_policy_bindings: volume_data_restore_policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy_bindings GoogleGkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfig(
            all_namespaces=all_namespaces,
            cluster_resource_conflict_policy=cluster_resource_conflict_policy,
            cluster_resource_restore_scope=cluster_resource_restore_scope,
            excluded_namespaces=excluded_namespaces,
            namespaced_resource_restore_mode=namespaced_resource_restore_mode,
            no_namespaces=no_namespaces,
            restore_order=restore_order,
            selected_applications=selected_applications,
            selected_namespaces=selected_namespaces,
            transformation_rules=transformation_rules,
            volume_data_restore_policy=volume_data_restore_policy,
            volume_data_restore_policy_bindings=volume_data_restore_policy_bindings,
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#create GoogleGkeBackupRestorePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#delete GoogleGkeBackupRestorePlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#update GoogleGkeBackupRestorePlan#update}.
        '''
        value = GoogleGkeBackupRestorePlanTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="restoreConfig")
    def restore_config(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigOutputReference", jsii.get(self, "restoreConfig"))

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
    def timeouts(self) -> "GoogleGkeBackupRestorePlanTimeoutsOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="backupPlanInput")
    def backup_plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPlanInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

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
    @jsii.member(jsii_name="restoreConfigInput")
    def restore_config_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfig"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfig"], jsii.get(self, "restoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeBackupRestorePlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeBackupRestorePlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPlan"))

    @backup_plan.setter
    def backup_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534db98eebe83e4029f6bb3ba1f01d8e8818adde0ba34ba55af1e1eca6dbbaa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052ddff8a5d01b2021d894af94e63c021e9552e682362634ef5f2a06864cd070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da85e223114316ac06fe1bd301ebe829b491a617957aa575a14a241ac70587f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8065c30a54f414b37bc9b1b07fa892bdea4624567f9eb9501767e2f4cb5e723f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8168c9ec757ac3b797c99113d238c716caceade2e3458d8b6e977681091e6ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc50768c258041e323f54767ea9d9e3d9ebeef45960c3749df81913a9c034f03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e216104f68eed160108b2817851310d944f45a1e0e46db921ee8d9be79fb21f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db2e41dc4bdec1bf1729f4f031c1bf4f4abd9994e4ecbf19b208a53997ac1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_plan": "backupPlan",
        "cluster": "cluster",
        "location": "location",
        "name": "name",
        "restore_config": "restoreConfig",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleGkeBackupRestorePlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_plan: builtins.str,
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        restore_config: typing.Union["GoogleGkeBackupRestorePlanRestoreConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_plan: A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#backup_plan GoogleGkeBackupRestorePlan#backup_plan}
        :param cluster: The source cluster from which Restores will be created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster GoogleGkeBackupRestorePlan#cluster}
        :param location: The region of the Restore Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#location GoogleGkeBackupRestorePlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#name GoogleGkeBackupRestorePlan#name}
        :param restore_config: restore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_config GoogleGkeBackupRestorePlan#restore_config}
        :param description: User specified descriptive string for this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#description GoogleGkeBackupRestorePlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#id GoogleGkeBackupRestorePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#labels GoogleGkeBackupRestorePlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#project GoogleGkeBackupRestorePlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#timeouts GoogleGkeBackupRestorePlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(restore_config, dict):
            restore_config = GoogleGkeBackupRestorePlanRestoreConfig(**restore_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeBackupRestorePlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fee7d8ca261f1bff59915583cd279138a4717b57ed8e16f942b8fbbc5982ab)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_plan", value=backup_plan, expected_type=type_hints["backup_plan"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument restore_config", value=restore_config, expected_type=type_hints["restore_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_plan": backup_plan,
            "cluster": cluster,
            "location": location,
            "name": name,
            "restore_config": restore_config,
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
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
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
    def backup_plan(self) -> builtins.str:
        '''A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#backup_plan GoogleGkeBackupRestorePlan#backup_plan}
        '''
        result = self._values.get("backup_plan")
        assert result is not None, "Required property 'backup_plan' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The source cluster from which Restores will be created via this RestorePlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster GoogleGkeBackupRestorePlan#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Restore Plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#location GoogleGkeBackupRestorePlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The full name of the BackupPlan Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#name GoogleGkeBackupRestorePlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def restore_config(self) -> "GoogleGkeBackupRestorePlanRestoreConfig":
        '''restore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_config GoogleGkeBackupRestorePlan#restore_config}
        '''
        result = self._values.get("restore_config")
        assert result is not None, "Required property 'restore_config' is missing"
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfig", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User specified descriptive string for this RestorePlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#description GoogleGkeBackupRestorePlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#id GoogleGkeBackupRestorePlan#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#labels GoogleGkeBackupRestorePlan#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#project GoogleGkeBackupRestorePlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeBackupRestorePlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#timeouts GoogleGkeBackupRestorePlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfig",
    jsii_struct_bases=[],
    name_mapping={
        "all_namespaces": "allNamespaces",
        "cluster_resource_conflict_policy": "clusterResourceConflictPolicy",
        "cluster_resource_restore_scope": "clusterResourceRestoreScope",
        "excluded_namespaces": "excludedNamespaces",
        "namespaced_resource_restore_mode": "namespacedResourceRestoreMode",
        "no_namespaces": "noNamespaces",
        "restore_order": "restoreOrder",
        "selected_applications": "selectedApplications",
        "selected_namespaces": "selectedNamespaces",
        "transformation_rules": "transformationRules",
        "volume_data_restore_policy": "volumeDataRestorePolicy",
        "volume_data_restore_policy_bindings": "volumeDataRestorePolicyBindings",
    },
)
class GoogleGkeBackupRestorePlanRestoreConfig:
    def __init__(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_resource_conflict_policy: typing.Optional[builtins.str] = None,
        cluster_resource_restore_scope: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_namespaces: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
        no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_order: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_applications: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_data_restore_policy: typing.Optional[builtins.str] = None,
        volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, restore all namespaced resources in the Backup. Setting this field to False will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_namespaces GoogleGkeBackupRestorePlan#all_namespaces}
        :param cluster_resource_conflict_policy: Defines the behavior for handling the situation where cluster-scoped resources being restored already exist in the target cluster. This MUST be set to a value other than 'CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED' if 'clusterResourceRestoreScope' is anyting other than 'noGroupKinds'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#clusterresourceconflictpolicy for more information on each policy option. Possible values: ["USE_EXISTING_VERSION", "USE_BACKUP_VERSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_conflict_policy GoogleGkeBackupRestorePlan#cluster_resource_conflict_policy}
        :param cluster_resource_restore_scope: cluster_resource_restore_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_restore_scope GoogleGkeBackupRestorePlan#cluster_resource_restore_scope}
        :param excluded_namespaces: excluded_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_namespaces GoogleGkeBackupRestorePlan#excluded_namespaces}
        :param namespaced_resource_restore_mode: Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster. This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_resource_restore_mode GoogleGkeBackupRestorePlan#namespaced_resource_restore_mode}
        :param no_namespaces: Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_namespaces GoogleGkeBackupRestorePlan#no_namespaces}
        :param restore_order: restore_order block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_order GoogleGkeBackupRestorePlan#restore_order}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_applications GoogleGkeBackupRestorePlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_namespaces GoogleGkeBackupRestorePlan#selected_namespaces}
        :param transformation_rules: transformation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#transformation_rules GoogleGkeBackupRestorePlan#transformation_rules}
        :param volume_data_restore_policy: Specifies the mechanism to be used to restore volume data. This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy GoogleGkeBackupRestorePlan#volume_data_restore_policy}
        :param volume_data_restore_policy_bindings: volume_data_restore_policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy_bindings GoogleGkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        if isinstance(cluster_resource_restore_scope, dict):
            cluster_resource_restore_scope = GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(**cluster_resource_restore_scope)
        if isinstance(excluded_namespaces, dict):
            excluded_namespaces = GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces(**excluded_namespaces)
        if isinstance(restore_order, dict):
            restore_order = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder(**restore_order)
        if isinstance(selected_applications, dict):
            selected_applications = GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications(**selected_applications)
        if isinstance(selected_namespaces, dict):
            selected_namespaces = GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces(**selected_namespaces)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26591ff026abee2ecba2670bdd4d217f2bb4849bf9caa3c4d7f1b99c22100f13)
            check_type(argname="argument all_namespaces", value=all_namespaces, expected_type=type_hints["all_namespaces"])
            check_type(argname="argument cluster_resource_conflict_policy", value=cluster_resource_conflict_policy, expected_type=type_hints["cluster_resource_conflict_policy"])
            check_type(argname="argument cluster_resource_restore_scope", value=cluster_resource_restore_scope, expected_type=type_hints["cluster_resource_restore_scope"])
            check_type(argname="argument excluded_namespaces", value=excluded_namespaces, expected_type=type_hints["excluded_namespaces"])
            check_type(argname="argument namespaced_resource_restore_mode", value=namespaced_resource_restore_mode, expected_type=type_hints["namespaced_resource_restore_mode"])
            check_type(argname="argument no_namespaces", value=no_namespaces, expected_type=type_hints["no_namespaces"])
            check_type(argname="argument restore_order", value=restore_order, expected_type=type_hints["restore_order"])
            check_type(argname="argument selected_applications", value=selected_applications, expected_type=type_hints["selected_applications"])
            check_type(argname="argument selected_namespaces", value=selected_namespaces, expected_type=type_hints["selected_namespaces"])
            check_type(argname="argument transformation_rules", value=transformation_rules, expected_type=type_hints["transformation_rules"])
            check_type(argname="argument volume_data_restore_policy", value=volume_data_restore_policy, expected_type=type_hints["volume_data_restore_policy"])
            check_type(argname="argument volume_data_restore_policy_bindings", value=volume_data_restore_policy_bindings, expected_type=type_hints["volume_data_restore_policy_bindings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_namespaces is not None:
            self._values["all_namespaces"] = all_namespaces
        if cluster_resource_conflict_policy is not None:
            self._values["cluster_resource_conflict_policy"] = cluster_resource_conflict_policy
        if cluster_resource_restore_scope is not None:
            self._values["cluster_resource_restore_scope"] = cluster_resource_restore_scope
        if excluded_namespaces is not None:
            self._values["excluded_namespaces"] = excluded_namespaces
        if namespaced_resource_restore_mode is not None:
            self._values["namespaced_resource_restore_mode"] = namespaced_resource_restore_mode
        if no_namespaces is not None:
            self._values["no_namespaces"] = no_namespaces
        if restore_order is not None:
            self._values["restore_order"] = restore_order
        if selected_applications is not None:
            self._values["selected_applications"] = selected_applications
        if selected_namespaces is not None:
            self._values["selected_namespaces"] = selected_namespaces
        if transformation_rules is not None:
            self._values["transformation_rules"] = transformation_rules
        if volume_data_restore_policy is not None:
            self._values["volume_data_restore_policy"] = volume_data_restore_policy
        if volume_data_restore_policy_bindings is not None:
            self._values["volume_data_restore_policy_bindings"] = volume_data_restore_policy_bindings

    @builtins.property
    def all_namespaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, restore all namespaced resources in the Backup. Setting this field to False will result in an error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_namespaces GoogleGkeBackupRestorePlan#all_namespaces}
        '''
        result = self._values.get("all_namespaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cluster_resource_conflict_policy(self) -> typing.Optional[builtins.str]:
        '''Defines the behavior for handling the situation where cluster-scoped resources being restored already exist in the target cluster.

        This MUST be set to a value other than 'CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED'
        if 'clusterResourceRestoreScope' is anyting other than 'noGroupKinds'.
        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#clusterresourceconflictpolicy
        for more information on each policy option. Possible values: ["USE_EXISTING_VERSION", "USE_BACKUP_VERSION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_conflict_policy GoogleGkeBackupRestorePlan#cluster_resource_conflict_policy}
        '''
        result = self._values.get("cluster_resource_conflict_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_resource_restore_scope(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope"]:
        '''cluster_resource_restore_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#cluster_resource_restore_scope GoogleGkeBackupRestorePlan#cluster_resource_restore_scope}
        '''
        result = self._values.get("cluster_resource_restore_scope")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope"], result)

    @builtins.property
    def excluded_namespaces(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces"]:
        '''excluded_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_namespaces GoogleGkeBackupRestorePlan#excluded_namespaces}
        '''
        result = self._values.get("excluded_namespaces")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces"], result)

    @builtins.property
    def namespaced_resource_restore_mode(self) -> typing.Optional[builtins.str]:
        '''Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster.

        This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED'
        if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'.
        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode
        for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_resource_restore_mode GoogleGkeBackupRestorePlan#namespaced_resource_restore_mode}
        '''
        result = self._values.get("namespaced_resource_restore_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_namespaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_namespaces GoogleGkeBackupRestorePlan#no_namespaces}
        '''
        result = self._values.get("no_namespaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restore_order(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder"]:
        '''restore_order block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#restore_order GoogleGkeBackupRestorePlan#restore_order}
        '''
        result = self._values.get("restore_order")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder"], result)

    @builtins.property
    def selected_applications(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications"]:
        '''selected_applications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_applications GoogleGkeBackupRestorePlan#selected_applications}
        '''
        result = self._values.get("selected_applications")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications"], result)

    @builtins.property
    def selected_namespaces(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces"]:
        '''selected_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_namespaces GoogleGkeBackupRestorePlan#selected_namespaces}
        '''
        result = self._values.get("selected_namespaces")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces"], result)

    @builtins.property
    def transformation_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules"]]]:
        '''transformation_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#transformation_rules GoogleGkeBackupRestorePlan#transformation_rules}
        '''
        result = self._values.get("transformation_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules"]]], result)

    @builtins.property
    def volume_data_restore_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the mechanism to be used to restore volume data.

        This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED'
        if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'.
        If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'.
        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy
        for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy GoogleGkeBackupRestorePlan#volume_data_restore_policy}
        '''
        result = self._values.get("volume_data_restore_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_data_restore_policy_bindings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]]:
        '''volume_data_restore_policy_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_data_restore_policy_bindings GoogleGkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        result = self._values.get("volume_data_restore_policy_bindings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope",
    jsii_struct_bases=[],
    name_mapping={
        "all_group_kinds": "allGroupKinds",
        "excluded_group_kinds": "excludedGroupKinds",
        "no_group_kinds": "noGroupKinds",
        "selected_group_kinds": "selectedGroupKinds",
    },
)
class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope:
    def __init__(
        self,
        *,
        all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_group_kinds: If True, all valid cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_group_kinds GoogleGkeBackupRestorePlan#all_group_kinds}
        :param excluded_group_kinds: excluded_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_group_kinds GoogleGkeBackupRestorePlan#excluded_group_kinds}
        :param no_group_kinds: If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_group_kinds GoogleGkeBackupRestorePlan#no_group_kinds}
        :param selected_group_kinds: selected_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_group_kinds GoogleGkeBackupRestorePlan#selected_group_kinds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64a80d572de46dac8f19f4955faf535f1686e0a67a2d4e3e9aa8c49e33d89e31)
            check_type(argname="argument all_group_kinds", value=all_group_kinds, expected_type=type_hints["all_group_kinds"])
            check_type(argname="argument excluded_group_kinds", value=excluded_group_kinds, expected_type=type_hints["excluded_group_kinds"])
            check_type(argname="argument no_group_kinds", value=no_group_kinds, expected_type=type_hints["no_group_kinds"])
            check_type(argname="argument selected_group_kinds", value=selected_group_kinds, expected_type=type_hints["selected_group_kinds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_group_kinds is not None:
            self._values["all_group_kinds"] = all_group_kinds
        if excluded_group_kinds is not None:
            self._values["excluded_group_kinds"] = excluded_group_kinds
        if no_group_kinds is not None:
            self._values["no_group_kinds"] = no_group_kinds
        if selected_group_kinds is not None:
            self._values["selected_group_kinds"] = selected_group_kinds

    @builtins.property
    def all_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, all valid cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_group_kinds GoogleGkeBackupRestorePlan#all_group_kinds}
        '''
        result = self._values.get("all_group_kinds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def excluded_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds"]]]:
        '''excluded_group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_group_kinds GoogleGkeBackupRestorePlan#excluded_group_kinds}
        '''
        result = self._values.get("excluded_group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds"]]], result)

    @builtins.property
    def no_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_group_kinds GoogleGkeBackupRestorePlan#no_group_kinds}
        '''
        result = self._values.get("no_group_kinds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selected_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]]:
        '''selected_group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_group_kinds GoogleGkeBackupRestorePlan#selected_group_kinds}
        '''
        result = self._values.get("selected_group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b79f85a1564afdf539b46142ee63ab6e22b8b1d7e2995befd5c92d554e53985)
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_kind", value=resource_kind, expected_type=type_hints["resource_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a415e444bc6c183c5b7356ad11fc7a92bc2799bfcc07edd54dbfa2d51828739)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ca3be97a3fe5c1b0048600283564d50c6a06c9ed6d8b858c1bb70229ef4226)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb065756ce15bbaf2f4ccd3b0263a44643bc18a4959aa88c7528cf7a463de4d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28a7746d51201a590af0a7100d7f846406b802b511542a6ec189ec1f6faf5e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09eb4981674704ab7e2c221bd229fd4103b6f8ea7dfaca332873870268d0a1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205f409a382cc24c8927e9335d099563ddf4fe4fe8f146baeb77e4dba46763ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d722153db71b2f0951f6bf863a939ebfee8c75112a1165400eb982f141a8f2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceKind")
    def reset_resource_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceKind", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceKindInput")
    def resource_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003ff44d00478531cf83279cf31a37d043196eef9628e0861fdd784b9133b2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6892790604152b205e0933806ae8381cbcae6bd18141dadb1412504999fd601e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea8c716035508fe0f056fbc8036c1c70665a2f77eeca54eac76097b181e7bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c870335c934ee45b8a99e963ba6e15505b4400faa4e1f1ad453fcc6f0a2eb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedGroupKinds")
    def put_excluded_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebd001702374ff8bf14dd3c1d43f5bb3a996f82c12a29044e7ab1bcd4b9bb26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedGroupKinds", [value]))

    @jsii.member(jsii_name="putSelectedGroupKinds")
    def put_selected_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2c8d95a8a08e1ff02fbf3ed2fde2eb7f43f36a3237d662f58f1593320b4480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectedGroupKinds", [value]))

    @jsii.member(jsii_name="resetAllGroupKinds")
    def reset_all_group_kinds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllGroupKinds", []))

    @jsii.member(jsii_name="resetExcludedGroupKinds")
    def reset_excluded_group_kinds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedGroupKinds", []))

    @jsii.member(jsii_name="resetNoGroupKinds")
    def reset_no_group_kinds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoGroupKinds", []))

    @jsii.member(jsii_name="resetSelectedGroupKinds")
    def reset_selected_group_kinds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedGroupKinds", []))

    @builtins.property
    @jsii.member(jsii_name="excludedGroupKinds")
    def excluded_group_kinds(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList, jsii.get(self, "excludedGroupKinds"))

    @builtins.property
    @jsii.member(jsii_name="selectedGroupKinds")
    def selected_group_kinds(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList", jsii.get(self, "selectedGroupKinds"))

    @builtins.property
    @jsii.member(jsii_name="allGroupKindsInput")
    def all_group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allGroupKindsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedGroupKindsInput")
    def excluded_group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]], jsii.get(self, "excludedGroupKindsInput"))

    @builtins.property
    @jsii.member(jsii_name="noGroupKindsInput")
    def no_group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noGroupKindsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedGroupKindsInput")
    def selected_group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]], jsii.get(self, "selectedGroupKindsInput"))

    @builtins.property
    @jsii.member(jsii_name="allGroupKinds")
    def all_group_kinds(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allGroupKinds"))

    @all_group_kinds.setter
    def all_group_kinds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533f2e164e751a6812514fd3594e7d875b8b845d1feb74b9eda5341b3fb44f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allGroupKinds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noGroupKinds")
    def no_group_kinds(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noGroupKinds"))

    @no_group_kinds.setter
    def no_group_kinds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0896fcc28aaf48c95a3d9ff3713a06ee94ca835f13d9c3a998c520b21084cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGroupKinds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29115c6f975e6c8f62ba8fdf1ee9c5b088407452f2148d873acf3482a5f02965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347732ebf52e7c44338604eb2a11330b2abf4038f847076c0c06a465fff65d4f)
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_kind", value=resource_kind, expected_type=type_hints["resource_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9435c9ad1912c63a19b36843f7a5737dc401dea9d97c0999362e9404d268e4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c7afbb03cb25a76afb03a95b844b741b827b200b2bd67f1900be38f3a13d96)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7723dbb66714fdb5f475e56b51c69b359a74ac807a0b06f0221c168f9ba1fd9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8592acc49a98cef675e06cb5466357a4c9b7406ca726c5b0abaea3f62ae3542a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0088ddc74df0581740f2205dce163322e95bcf7bd222f5d1f5a3dd74aef7acee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52ce14b3dcf5aaa3fec18e785a74343b5d5250fc160b8453521492b11d27a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b720a72002c12528fad4b37578260a648c87c9f2dec99d39fa61837d005d7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceKind")
    def reset_resource_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceKind", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceKindInput")
    def resource_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0cc1bf60d32f7e91b1b281d9b6d9be4a210ec6b2e44d604fcd64ce483f73e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7da7a5327acef9c93a4c66f7bb0b9cdd176a23939edfc0ff91a17eb3bfb51244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ce64bd6fba0aeff01a034f39eadf67d0336f25ed2716f11d4efe6f80120985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df257cab736572653c9d55847320a5e4706466436c45f35185562eb85d85aeb)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f19b50f1708064c3c749308dc9fc3b897f89a6d7ae86605213cfb686dfe827d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e78b39177cdb7834e3932bca692923dbf8d7b75255c1a5228abbe440ad674f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8bcc377a55db5be7a44b64d35f482d89753169ccb3f4de14858e4a4c254a1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0511464f777f0996fad4eae06c80b8032b6bfe1eb7109fe8e3a97ba67c434bc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterResourceRestoreScope")
    def put_cluster_resource_restore_scope(
        self,
        *,
        all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_group_kinds: If True, all valid cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#all_group_kinds GoogleGkeBackupRestorePlan#all_group_kinds}
        :param excluded_group_kinds: excluded_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#excluded_group_kinds GoogleGkeBackupRestorePlan#excluded_group_kinds}
        :param no_group_kinds: If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#no_group_kinds GoogleGkeBackupRestorePlan#no_group_kinds}
        :param selected_group_kinds: selected_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#selected_group_kinds GoogleGkeBackupRestorePlan#selected_group_kinds}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(
            all_group_kinds=all_group_kinds,
            excluded_group_kinds=excluded_group_kinds,
            no_group_kinds=no_group_kinds,
            selected_group_kinds=selected_group_kinds,
        )

        return typing.cast(None, jsii.invoke(self, "putClusterResourceRestoreScope", [value]))

    @jsii.member(jsii_name="putExcludedNamespaces")
    def put_excluded_namespaces(
        self,
        *,
        namespaces: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces(
            namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedNamespaces", [value]))

    @jsii.member(jsii_name="putRestoreOrder")
    def put_restore_order(
        self,
        *,
        group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param group_kind_dependencies: group_kind_dependencies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kind_dependencies GoogleGkeBackupRestorePlan#group_kind_dependencies}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder(
            group_kind_dependencies=group_kind_dependencies
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreOrder", [value]))

    @jsii.member(jsii_name="putSelectedApplications")
    def put_selected_applications(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_names GoogleGkeBackupRestorePlan#namespaced_names}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications(
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
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces(
            namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putSelectedNamespaces", [value]))

    @jsii.member(jsii_name="putTransformationRules")
    def put_transformation_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53357cb39616213db81c3d072de4611abc6cac190587d96267971be119500cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransformationRules", [value]))

    @jsii.member(jsii_name="putVolumeDataRestorePolicyBindings")
    def put_volume_data_restore_policy_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6647f6bfd5840d44159579bef4871ebc801b538d4d409793dc20f7657e4f8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeDataRestorePolicyBindings", [value]))

    @jsii.member(jsii_name="resetAllNamespaces")
    def reset_all_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllNamespaces", []))

    @jsii.member(jsii_name="resetClusterResourceConflictPolicy")
    def reset_cluster_resource_conflict_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterResourceConflictPolicy", []))

    @jsii.member(jsii_name="resetClusterResourceRestoreScope")
    def reset_cluster_resource_restore_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterResourceRestoreScope", []))

    @jsii.member(jsii_name="resetExcludedNamespaces")
    def reset_excluded_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedNamespaces", []))

    @jsii.member(jsii_name="resetNamespacedResourceRestoreMode")
    def reset_namespaced_resource_restore_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespacedResourceRestoreMode", []))

    @jsii.member(jsii_name="resetNoNamespaces")
    def reset_no_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoNamespaces", []))

    @jsii.member(jsii_name="resetRestoreOrder")
    def reset_restore_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreOrder", []))

    @jsii.member(jsii_name="resetSelectedApplications")
    def reset_selected_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedApplications", []))

    @jsii.member(jsii_name="resetSelectedNamespaces")
    def reset_selected_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectedNamespaces", []))

    @jsii.member(jsii_name="resetTransformationRules")
    def reset_transformation_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransformationRules", []))

    @jsii.member(jsii_name="resetVolumeDataRestorePolicy")
    def reset_volume_data_restore_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeDataRestorePolicy", []))

    @jsii.member(jsii_name="resetVolumeDataRestorePolicyBindings")
    def reset_volume_data_restore_policy_bindings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeDataRestorePolicyBindings", []))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceRestoreScope")
    def cluster_resource_restore_scope(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference, jsii.get(self, "clusterResourceRestoreScope"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespaces")
    def excluded_namespaces(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference, jsii.get(self, "excludedNamespaces"))

    @builtins.property
    @jsii.member(jsii_name="restoreOrder")
    def restore_order(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference", jsii.get(self, "restoreOrder"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplications")
    def selected_applications(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference", jsii.get(self, "selectedApplications"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespaces")
    def selected_namespaces(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference", jsii.get(self, "selectedNamespaces"))

    @builtins.property
    @jsii.member(jsii_name="transformationRules")
    def transformation_rules(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesList":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesList", jsii.get(self, "transformationRules"))

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicyBindings")
    def volume_data_restore_policy_bindings(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList", jsii.get(self, "volumeDataRestorePolicyBindings"))

    @builtins.property
    @jsii.member(jsii_name="allNamespacesInput")
    def all_namespaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceConflictPolicyInput")
    def cluster_resource_conflict_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterResourceConflictPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceRestoreScopeInput")
    def cluster_resource_restore_scope_input(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope], jsii.get(self, "clusterResourceRestoreScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespacesInput")
    def excluded_namespaces_input(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces], jsii.get(self, "excludedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="namespacedResourceRestoreModeInput")
    def namespaced_resource_restore_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespacedResourceRestoreModeInput"))

    @builtins.property
    @jsii.member(jsii_name="noNamespacesInput")
    def no_namespaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreOrderInput")
    def restore_order_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder"], jsii.get(self, "restoreOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplicationsInput")
    def selected_applications_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications"], jsii.get(self, "selectedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespacesInput")
    def selected_namespaces_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces"], jsii.get(self, "selectedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationRulesInput")
    def transformation_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRules"]]], jsii.get(self, "transformationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicyBindingsInput")
    def volume_data_restore_policy_bindings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]], jsii.get(self, "volumeDataRestorePolicyBindingsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicyInput")
    def volume_data_restore_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeDataRestorePolicyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ef0538083a6f868158949b8950d36f008fd3eacd21195e217b41cb97ca6fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterResourceConflictPolicy")
    def cluster_resource_conflict_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceConflictPolicy"))

    @cluster_resource_conflict_policy.setter
    def cluster_resource_conflict_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69e85a9d64da5812fc908c3f5caf218af0db165f88181a08536c87db143d8d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterResourceConflictPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespacedResourceRestoreMode")
    def namespaced_resource_restore_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespacedResourceRestoreMode"))

    @namespaced_resource_restore_mode.setter
    def namespaced_resource_restore_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd22f5a4f1d4c9b837a24c4bdce1ecde03bec49f7a4e51ebc9d8101d1feeb71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespacedResourceRestoreMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noNamespaces")
    def no_namespaces(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noNamespaces"))

    @no_namespaces.setter
    def no_namespaces(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94676835ffc9afcecb2a71717c6e697ebfdf54a26883dc18ec4536b5ea320683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicy")
    def volume_data_restore_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeDataRestorePolicy"))

    @volume_data_restore_policy.setter
    def volume_data_restore_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da7677bd1468f1933def4ce5e3d64bf0197a6f61c61a4e4e38c3e801ce9a099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeDataRestorePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfig]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9b61a69a9133097db1edb319ab1da82617f43c3aeb70d293c25edc4a9c3aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder",
    jsii_struct_bases=[],
    name_mapping={"group_kind_dependencies": "groupKindDependencies"},
)
class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder:
    def __init__(
        self,
        *,
        group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param group_kind_dependencies: group_kind_dependencies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kind_dependencies GoogleGkeBackupRestorePlan#group_kind_dependencies}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb19674a01e96d63fdf98719acc14d4813c26b1f14f4f6213e6b9d07ca5a3df8)
            check_type(argname="argument group_kind_dependencies", value=group_kind_dependencies, expected_type=type_hints["group_kind_dependencies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_kind_dependencies": group_kind_dependencies,
        }

    @builtins.property
    def group_kind_dependencies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies"]]:
        '''group_kind_dependencies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kind_dependencies GoogleGkeBackupRestorePlan#group_kind_dependencies}
        '''
        result = self._values.get("group_kind_dependencies")
        assert result is not None, "Required property 'group_kind_dependencies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies",
    jsii_struct_bases=[],
    name_mapping={"requiring": "requiring", "satisfying": "satisfying"},
)
class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies:
    def __init__(
        self,
        *,
        requiring: typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring", typing.Dict[builtins.str, typing.Any]],
        satisfying: typing.Union["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param requiring: requiring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#requiring GoogleGkeBackupRestorePlan#requiring}
        :param satisfying: satisfying block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#satisfying GoogleGkeBackupRestorePlan#satisfying}
        '''
        if isinstance(requiring, dict):
            requiring = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(**requiring)
        if isinstance(satisfying, dict):
            satisfying = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(**satisfying)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1208c60d0f428e9bd9c2b1c89195a515f85c05302f0a02c86672e2acedfa3b1)
            check_type(argname="argument requiring", value=requiring, expected_type=type_hints["requiring"])
            check_type(argname="argument satisfying", value=satisfying, expected_type=type_hints["satisfying"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "requiring": requiring,
            "satisfying": satisfying,
        }

    @builtins.property
    def requiring(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring":
        '''requiring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#requiring GoogleGkeBackupRestorePlan#requiring}
        '''
        result = self._values.get("requiring")
        assert result is not None, "Required property 'requiring' is missing"
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring", result)

    @builtins.property
    def satisfying(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying":
        '''satisfying block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#satisfying GoogleGkeBackupRestorePlan#satisfying}
        '''
        result = self._values.get("satisfying")
        assert result is not None, "Required property 'satisfying' is missing"
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__779d1f443ac4575d3d648e46ac464461f212919e7211c485dc99151e98f991d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96624e4961b377dff603817bf4ffee0ad2c9ab29f4eef80359de321b444e634)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed954f4c788a55d0e154e2effae7a79a8a8a97333554aeaf5145e67d511479ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a70b90d954baad866fbcb890cdeb7b9638cf15a8e26b0f6692256b62cda3a875)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6232f84ea225cd1d0bc527b860a2673b5098fca22b75ce0fb20b8d088dddbdcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0339f92c96c514d157e4dc839538474fcb1a284ad696bc7b7a9a74a05bcbe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6111129d79990b4978486abb96be3963ed3ee600acefddc64ada5efa147a3011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequiring")
    def put_requiring(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(
            resource_group=resource_group, resource_kind=resource_kind
        )

        return typing.cast(None, jsii.invoke(self, "putRequiring", [value]))

    @jsii.member(jsii_name="putSatisfying")
    def put_satisfying(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(
            resource_group=resource_group, resource_kind=resource_kind
        )

        return typing.cast(None, jsii.invoke(self, "putSatisfying", [value]))

    @builtins.property
    @jsii.member(jsii_name="requiring")
    def requiring(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference", jsii.get(self, "requiring"))

    @builtins.property
    @jsii.member(jsii_name="satisfying")
    def satisfying(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference", jsii.get(self, "satisfying"))

    @builtins.property
    @jsii.member(jsii_name="requiringInput")
    def requiring_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring"], jsii.get(self, "requiringInput"))

    @builtins.property
    @jsii.member(jsii_name="satisfyingInput")
    def satisfying_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying"], jsii.get(self, "satisfyingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf4f06c298325846f35112379c1a2b82e63e25bb93697453aec5367541dcbc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb53a8b5ec7c57bf906adf2915085a7432a29ccd6c6f1b03ab428c04d7d8bb1)
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_kind", value=resource_kind, expected_type=type_hints["resource_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4bd6e16f4ca264255bc370e7a161ae6544d295aa2e476fc184c8f3c266331e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceKind")
    def reset_resource_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceKind", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceKindInput")
    def resource_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38391f791b4fc8481e69698566d754fe5de8c972e1d8dccfa7add9add895c93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543a3331171aa78ca71015f8a6f77fe1feffaac1148b57d91dec5879b5c688a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845a43c79cb6edb3908d4570366a9280303ae1ecbddd12b1c2b1f5199de68bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a60c611d10b1efb25d9b1f03b9c573ae256a2aa4830915e6c9a0a4d75fe9a55)
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_kind", value=resource_kind, expected_type=type_hints["resource_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f62aea3ab18bb13aea768d080d3d2b63a672d57d71e0698d507423bfe081c3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceKind")
    def reset_resource_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceKind", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceKindInput")
    def resource_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8413db42e44031c2bd86707187675239c5a2fb1350ad7a683f3b2c8d8f7ffc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f124072b1d1d663eacd851276c74656c466e940a3220a1ba753b1641b314baec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cdabf0065913081dc0a6c2be1c4b08c3de40e18237db3274da08fef3369982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e563f2e45d832348a655bef38637ca1e2c5fe88daa5c27e3daff165e58105352)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupKindDependencies")
    def put_group_kind_dependencies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a707ad55ed842c8e70c65c3972dcd8dbe33025ad0c3b26d2b785362fe64d7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupKindDependencies", [value]))

    @builtins.property
    @jsii.member(jsii_name="groupKindDependencies")
    def group_kind_dependencies(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList, jsii.get(self, "groupKindDependencies"))

    @builtins.property
    @jsii.member(jsii_name="groupKindDependenciesInput")
    def group_kind_dependencies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]], jsii.get(self, "groupKindDependenciesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5b6eeb8a94697d9b46bd367a589ca5d7fb6cf69148cc12e123270d6536854c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications",
    jsii_struct_bases=[],
    name_mapping={"namespaced_names": "namespacedNames"},
)
class GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications:
    def __init__(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_names GoogleGkeBackupRestorePlan#namespaced_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081ec2f0a27c796615b9d7bdc648635930af29ce43214422157578f8d566748b)
            check_type(argname="argument namespaced_names", value=namespaced_names, expected_type=type_hints["namespaced_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaced_names": namespaced_names,
        }

    @builtins.property
    def namespaced_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames"]]:
        '''namespaced_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaced_names GoogleGkeBackupRestorePlan#namespaced_names}
        '''
        result = self._values.get("namespaced_names")
        assert result is not None, "Required property 'namespaced_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: The name of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#name GoogleGkeBackupRestorePlan#name}
        :param namespace: The namespace of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespace GoogleGkeBackupRestorePlan#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff065486faa11592b395832d5c8360266fd8ddf4a4b899677e85513bbe82e87)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#name GoogleGkeBackupRestorePlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''The namespace of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespace GoogleGkeBackupRestorePlan#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcca24d4268aeac112138a51bac5266f9b1f605961e34e7877c32fbd466a56b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdb645bfffa29d8a5e00ad7162853573467e21f982b875b184fddf0e4140274)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cb8fdcfc8a1ff0d81eb267d45f32255724da46d1116d71998076539e39eb42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9bfb63cff3b6c706db2f7b0268a6761f4576bdbf96d211a78caabc85443d3b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a6cc28418a42f6476877ef4d9a6da0449e8dfe4d6633975480d99961ba836f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19340aececf229125b05ac99e5446b3cf595f364c167530b18c3a6c5a559c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f9321f9e8e18a6a61afabd426cd833522d513b43d99ca83862bcfd30f84fe4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68db6c0d4716881d26db708de93cbd9338899a2d592e9a3a6dbbdfe084d43477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee03272bb8343247dbd5db59a1b3edabb12ec02e9fd9435705711cdee101af3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3247f19d2527eb232a91bd5dfeb07d6d5bf7a719c750146feab839a416186b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2119b635ee927d66ed4ab91c25574bf416d31ad9a1614202954284e688011b14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespacedNames")
    def put_namespaced_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c44f13d332e19a14b2862c8c8f9ef01fead3e1181d170cd6fc0abed403ad012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespacedNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="namespacedNames")
    def namespaced_names(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList, jsii.get(self, "namespacedNames"))

    @builtins.property
    @jsii.member(jsii_name="namespacedNamesInput")
    def namespaced_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "namespacedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c53a709e47accc7bf07a0ae21a80374c4fa6b8434bbf4ab47a7fb6bbd7437a0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32276926fd5f77a3da36358094af13fe9249f189545315b4ed7bba13b39159d)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1428cd155071c165cc7e9496891bd5a796b0b6c6c8fe2640d1df403dc0b43041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56607d4469bcb83d41b62690e699e75eb57df1de878ecfa61fcb97121eb2f2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a9ed708433de9967648dc7e716c149fa732111494fbc3eaa7c46fedc827bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRules",
    jsii_struct_bases=[],
    name_mapping={
        "field_actions": "fieldActions",
        "description": "description",
        "resource_filter": "resourceFilter",
    },
)
class GoogleGkeBackupRestorePlanRestoreConfigTransformationRules:
    def __init__(
        self,
        *,
        field_actions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        resource_filter: typing.Optional[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param field_actions: field_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#field_actions GoogleGkeBackupRestorePlan#field_actions}
        :param description: The description is a user specified string description of the transformation rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#description GoogleGkeBackupRestorePlan#description}
        :param resource_filter: resource_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_filter GoogleGkeBackupRestorePlan#resource_filter}
        '''
        if isinstance(resource_filter, dict):
            resource_filter = GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(**resource_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222d5fa0d212a3f99ce28539e376d6c9fe04666dfa527c62eb52038e43f9bd92)
            check_type(argname="argument field_actions", value=field_actions, expected_type=type_hints["field_actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_filter", value=resource_filter, expected_type=type_hints["resource_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_actions": field_actions,
        }
        if description is not None:
            self._values["description"] = description
        if resource_filter is not None:
            self._values["resource_filter"] = resource_filter

    @builtins.property
    def field_actions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions"]]:
        '''field_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#field_actions GoogleGkeBackupRestorePlan#field_actions}
        '''
        result = self._values.get("field_actions")
        assert result is not None, "Required property 'field_actions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description is a user specified string description of the transformation rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#description GoogleGkeBackupRestorePlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_filter(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"]:
        '''resource_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_filter GoogleGkeBackupRestorePlan#resource_filter}
        '''
        result = self._values.get("resource_filter")
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigTransformationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions",
    jsii_struct_bases=[],
    name_mapping={
        "op": "op",
        "from_path": "fromPath",
        "path": "path",
        "value": "value",
    },
)
class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions:
    def __init__(
        self,
        *,
        op: builtins.str,
        from_path: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param op: Specifies the operation to perform. Possible values: ["REMOVE", "MOVE", "COPY", "ADD", "TEST", "REPLACE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#op GoogleGkeBackupRestorePlan#op}
        :param from_path: A string containing a JSON Pointer value that references the location in the target document to move the value from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#from_path GoogleGkeBackupRestorePlan#from_path}
        :param path: A string containing a JSON-Pointer value that references a location within the target document where the operation is performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#path GoogleGkeBackupRestorePlan#path}
        :param value: A string that specifies the desired value in string format to use for transformation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#value GoogleGkeBackupRestorePlan#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46fea2dd00d0a58de6ffa2013879041a322bfb699dd95670e0a3efb2f15dd0c)
            check_type(argname="argument op", value=op, expected_type=type_hints["op"])
            check_type(argname="argument from_path", value=from_path, expected_type=type_hints["from_path"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "op": op,
        }
        if from_path is not None:
            self._values["from_path"] = from_path
        if path is not None:
            self._values["path"] = path
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def op(self) -> builtins.str:
        '''Specifies the operation to perform. Possible values: ["REMOVE", "MOVE", "COPY", "ADD", "TEST", "REPLACE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#op GoogleGkeBackupRestorePlan#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_path(self) -> typing.Optional[builtins.str]:
        '''A string containing a JSON Pointer value that references the location in the target document to move the value from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#from_path GoogleGkeBackupRestorePlan#from_path}
        '''
        result = self._values.get("from_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''A string containing a JSON-Pointer value that references a location within the target document where the operation is performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#path GoogleGkeBackupRestorePlan#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A string that specifies the desired value in string format to use for transformation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#value GoogleGkeBackupRestorePlan#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a20c48b7d6968b1d20b957f974b4eb2807f4ea5f8602850971573c34fa3e62e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9c5269dc6b3fe94b2815ccffa2f17ccdff4b17e00a0de786aadb7edf0123c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7b747fc76ea76ad398e5acceeb7efa08a451ce05fde50efd785ef0cc1a15fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af7662b8c6901381a50294763788fa57e4e4a0190675907a774f72e20f53ee67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09cb067c7a2a28bb3b1574c7711e71f402a61273009df2ecf6490c4607946629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abf530f9e7f2f5e8255f326c37a4dedd65105a63a8e9a5d553a5b31418b4509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9352021e3d1eeff05fb93a8d1d56571330fedd6a060c37796ac4d587a967472)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFromPath")
    def reset_from_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromPath", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="fromPathInput")
    def from_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromPathInput"))

    @builtins.property
    @jsii.member(jsii_name="opInput")
    def op_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="fromPath")
    def from_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromPath"))

    @from_path.setter
    def from_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb75000cc8460bc3ae71c0fb0598983285d814eac8303bcc383b2b82e418990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497555d20eed72db76c4df88f8f915bbdeeddd5460dd7a4c345603441d9c02ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0f69311b7d312f6968ffef64e09e96d217d0c49a7354150622182973df9d9bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68779815f425e66e9f5eef8942be150c0fef7994e37d12e2c04a0b9f8e2b701d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf869a9e53ab892d59609b82e8ad1341e847bf135274426243165e37e2422ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b87f01277a85cd0005c4fccdad1cef7734c0935c97534397f3282f180e4ad7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d53ddb78f5c54cd30cbf8d0df1ddf3ed9ca860dcd4b27a4cab877a1e87b7aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8fb739d621a06ef69dc2ff323ef860daac4b7243923826d9e0be50e1c85b4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a83d92ef43797aced074c9ec0830f52e86e43b071568b179268e9741595b948)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37185b5e9dc026a56900832db4d598b70d26b86ff206a8a6eecf6b3a6e81ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9181b5131431ec3eb9ea847346183ba40e5cb9d176f734754bf7a40f03418dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f34e7b45c3b5bf8664130bb798801d01770f25f96bba82d7a08fb8563794a0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFieldActions")
    def put_field_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a714918b81ea6a61e3d15731f091c47bebe27dd843e5f8259e2258d25503e08a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldActions", [value]))

    @jsii.member(jsii_name="putResourceFilter")
    def put_resource_filter(
        self,
        *,
        group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        json_path: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_kinds: group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kinds GoogleGkeBackupRestorePlan#group_kinds}
        :param json_path: This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#json_path GoogleGkeBackupRestorePlan#json_path}
        :param namespaces: (Filtering parameter) Any resource subject to transformation must be contained within one of the listed Kubernetes Namespace in the Backup. If this field is not provided, no namespace filtering will be performed (all resources in all Namespaces, including all cluster-scoped resources, will be candidates for transformation). To mix cluster-scoped and namespaced resources in the same rule, use an empty string ("") as one of the target namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        value = GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(
            group_kinds=group_kinds, json_path=json_path, namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putResourceFilter", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetResourceFilter")
    def reset_resource_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceFilter", []))

    @builtins.property
    @jsii.member(jsii_name="fieldActions")
    def field_actions(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList, jsii.get(self, "fieldActions"))

    @builtins.property
    @jsii.member(jsii_name="resourceFilter")
    def resource_filter(
        self,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference":
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference", jsii.get(self, "resourceFilter"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldActionsInput")
    def field_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]], jsii.get(self, "fieldActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceFilterInput")
    def resource_filter_input(
        self,
    ) -> typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"]:
        return typing.cast(typing.Optional["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"], jsii.get(self, "resourceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336f0507b1af7a8717d754fe336cbf214ba1f62e0b7c086835b8459e453c27ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820079928eb0d4ef53fe33c74092c982669b0d228645896463dcd076e281c57c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "group_kinds": "groupKinds",
        "json_path": "jsonPath",
        "namespaces": "namespaces",
    },
)
class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter:
    def __init__(
        self,
        *,
        group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        json_path: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_kinds: group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kinds GoogleGkeBackupRestorePlan#group_kinds}
        :param json_path: This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#json_path GoogleGkeBackupRestorePlan#json_path}
        :param namespaces: (Filtering parameter) Any resource subject to transformation must be contained within one of the listed Kubernetes Namespace in the Backup. If this field is not provided, no namespace filtering will be performed (all resources in all Namespaces, including all cluster-scoped resources, will be candidates for transformation). To mix cluster-scoped and namespaced resources in the same rule, use an empty string ("") as one of the target namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d92be6a15540acd6060bc0f3363b3fca2605e72dd5a70f2a1503c042178c2d)
            check_type(argname="argument group_kinds", value=group_kinds, expected_type=type_hints["group_kinds"])
            check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_kinds is not None:
            self._values["group_kinds"] = group_kinds
        if json_path is not None:
            self._values["json_path"] = json_path
        if namespaces is not None:
            self._values["namespaces"] = namespaces

    @builtins.property
    def group_kinds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds"]]]:
        '''group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#group_kinds GoogleGkeBackupRestorePlan#group_kinds}
        '''
        result = self._values.get("group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds"]]], result)

    @builtins.property
    def json_path(self) -> typing.Optional[builtins.str]:
        '''This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#json_path GoogleGkeBackupRestorePlan#json_path}
        '''
        result = self._values.get("json_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(Filtering parameter) Any resource subject to transformation must be contained within one of the listed Kubernetes Namespace in the Backup.

        If this field is not provided, no namespace filtering will
        be performed (all resources in all Namespaces, including all
        cluster-scoped resources, will be candidates for transformation).
        To mix cluster-scoped and namespaced resources in the same rule,
        use an empty string ("") as one of the target namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#namespaces GoogleGkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c4895a3226398e8c85f3a2c3c40da0f054dff6337060bae6fcb890897517d1)
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_kind", value=resource_kind, expected_type=type_hints["resource_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_group GoogleGkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#resource_kind GoogleGkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1fa2ee95b4fbcd6e8bbb44ccfd04e9bbff6407d844d6532e2c4641674eadf76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e25d9c31954217b4bc1da46cc94640dd54732470cf2e800af44383a34f4075f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e27fdd29378edb292d03c65e4276a7ab9e9d87f0a72800a4b1c6e5410bd735f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92924bccc06126d463fb82b3c429f384b8625911239ec5a063460db042c02d51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b71ca1a9f19b9cf60ce16e458a14ad5becf9684953eac054a61d3a9258bf6c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fc6d9f71641d7af165260b2ffc5c415d8ae1d05db6f2d645262213f0545757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2849e066d3ef32cb542b764f397d42f1f62c8158cc623aa13d2205d91bb1169b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceKind")
    def reset_resource_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceKind", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceKindInput")
    def resource_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ef7afc6f6b6b37ab6be45c7ad3bff25cc6c59ace3bde0420173f5f8c7664d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3986ab6a66b0fe4857a7c51cd8eb0ae73a48ce15b703d1242405f88785af9580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68ced68351603bf85bd8570bc36eb3dd37debb40720a868097211a7c6fabca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc0d3d78ccf2f1dcbf1db4eba7ea35b67ab4043370a291e0185a45c1bbf8cd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupKinds")
    def put_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a7ed9ec7cf391ce5b5d7148283fa9ce6bda2dea2d523bc495680cdb51ad6fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupKinds", [value]))

    @jsii.member(jsii_name="resetGroupKinds")
    def reset_group_kinds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupKinds", []))

    @jsii.member(jsii_name="resetJsonPath")
    def reset_json_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonPath", []))

    @jsii.member(jsii_name="resetNamespaces")
    def reset_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespaces", []))

    @builtins.property
    @jsii.member(jsii_name="groupKinds")
    def group_kinds(
        self,
    ) -> GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList:
        return typing.cast(GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList, jsii.get(self, "groupKinds"))

    @builtins.property
    @jsii.member(jsii_name="groupKindsInput")
    def group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]], jsii.get(self, "groupKindsInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPathInput")
    def json_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jsonPathInput"))

    @builtins.property
    @jsii.member(jsii_name="namespacesInput")
    def namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonPath")
    def json_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jsonPath"))

    @json_path.setter
    def json_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53aec3ed0d5649bc7bf41a61abcd00c656b1f8ea4fa8a9a379bf9db56ea0c46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaces")
    def namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namespaces"))

    @namespaces.setter
    def namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422241e96f4d589072d73901f0ebabbe4e43bfab66bf74555971e17193a847dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter]:
        return typing.cast(typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e9fe78989122aeafb3f732b0bcb93c2d356fe6b09ab92d750624d77a4074a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "volume_type": "volumeType"},
)
class GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings:
    def __init__(self, *, policy: builtins.str, volume_type: builtins.str) -> None:
        '''
        :param policy: Specifies the mechanism to be used to restore this volume data. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#policy GoogleGkeBackupRestorePlan#policy}
        :param volume_type: The volume type, as determined by the PVC's bound PV, to apply the policy to. Possible values: ["GCE_PERSISTENT_DISK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_type GoogleGkeBackupRestorePlan#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c471f0b973899d91350de98757e409c9cdb27cf764f1153ea956d398c35a4f88)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "volume_type": volume_type,
        }

    @builtins.property
    def policy(self) -> builtins.str:
        '''Specifies the mechanism to be used to restore this volume data.

        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy
        for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#policy GoogleGkeBackupRestorePlan#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''The volume type, as determined by the PVC's bound PV, to apply the policy to. Possible values: ["GCE_PERSISTENT_DISK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#volume_type GoogleGkeBackupRestorePlan#volume_type}
        '''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0042744262e99456691719d3a7a87b83577375414ae48f2571a6ef246b9a115e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c1a665c84e534763868c8e74907d7265ae3cf4070af2ecec40b5e07089e533)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b5b268ac5b217d15bc3a1451a4fdb6fa034dff15856b663b20d9bbd72549fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d56906d430f9104cf83b927195c7680f0fd03ace0f43d437d3952f8a936c7b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__209e3b0b1e4f5478c1eab2810ca126b674848499d86b7208a980fad4230a0cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf03fe97a8e7c887e59f61abd01a18ecd8a63979ec97d23f41caa813a5e21661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__504682852981cfcbdc11dbc6d690a38b362fdf27bd3bf8dc0b532de61b5a18ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bce634eb2be7f86792bfb65e7367bf044e23b98a8f7f9df4e10477eac5eb091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e02e18bdace23b591e9b9aa5ed046a240a1bdfe7747447cdfacbe1bca8e965f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2a471b194176db04f9a86a4973d4a4728356044add1e8047549e67f6aa3857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeBackupRestorePlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#create GoogleGkeBackupRestorePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#delete GoogleGkeBackupRestorePlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#update GoogleGkeBackupRestorePlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b75910b81f473922cfe81b2597e5f298365da2e1547894b751390763db75472)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#create GoogleGkeBackupRestorePlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#delete GoogleGkeBackupRestorePlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_gke_backup_restore_plan#update GoogleGkeBackupRestorePlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeBackupRestorePlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeBackupRestorePlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeBackupRestorePlan.GoogleGkeBackupRestorePlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8107b4a05139d81098dadd0541d837b70f221e6839cf4e076ac4c56b6e337c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0c3b5d0701eb2207954ed549774d931d9c9431ebc8cb29f384547462d3bce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba315baa802b669d5104b53f995a21983408a195c9039b06bc20325e53b08eb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee813e6ebb1c8f9b78b51b18bcbfac34ac8c9ce128a49d6245de8616efe37db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b485673b10d8450afc84cbab116503906f4000ddc8eff471abe505d4db1cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleGkeBackupRestorePlan",
    "GoogleGkeBackupRestorePlanConfig",
    "GoogleGkeBackupRestorePlanRestoreConfig",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList",
    "GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces",
    "GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces",
    "GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRules",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesList",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference",
    "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings",
    "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList",
    "GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference",
    "GoogleGkeBackupRestorePlanTimeouts",
    "GoogleGkeBackupRestorePlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1fa0de077a2bfd6d8332250d005d26a8dc7befc3f2cc9a0a9425c4ccb3549177(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_plan: builtins.str,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    restore_config: typing.Union[GoogleGkeBackupRestorePlanRestoreConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c6d64fb3872f5fa03eff0cc56b1d7d2591afa594f70390236eb5c4c325f7c0e4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534db98eebe83e4029f6bb3ba1f01d8e8818adde0ba34ba55af1e1eca6dbbaa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052ddff8a5d01b2021d894af94e63c021e9552e682362634ef5f2a06864cd070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da85e223114316ac06fe1bd301ebe829b491a617957aa575a14a241ac70587f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8065c30a54f414b37bc9b1b07fa892bdea4624567f9eb9501767e2f4cb5e723f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8168c9ec757ac3b797c99113d238c716caceade2e3458d8b6e977681091e6ff9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc50768c258041e323f54767ea9d9e3d9ebeef45960c3749df81913a9c034f03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e216104f68eed160108b2817851310d944f45a1e0e46db921ee8d9be79fb21f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db2e41dc4bdec1bf1729f4f031c1bf4f4abd9994e4ecbf19b208a53997ac1a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fee7d8ca261f1bff59915583cd279138a4717b57ed8e16f942b8fbbc5982ab(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_plan: builtins.str,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    restore_config: typing.Union[GoogleGkeBackupRestorePlanRestoreConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26591ff026abee2ecba2670bdd4d217f2bb4849bf9caa3c4d7f1b99c22100f13(
    *,
    all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cluster_resource_conflict_policy: typing.Optional[builtins.str] = None,
    cluster_resource_restore_scope: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_namespaces: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
    namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
    no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore_order: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_applications: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_namespaces: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    volume_data_restore_policy: typing.Optional[builtins.str] = None,
    volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64a80d572de46dac8f19f4955faf535f1686e0a67a2d4e3e9aa8c49e33d89e31(
    *,
    all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b79f85a1564afdf539b46142ee63ab6e22b8b1d7e2995befd5c92d554e53985(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a415e444bc6c183c5b7356ad11fc7a92bc2799bfcc07edd54dbfa2d51828739(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ca3be97a3fe5c1b0048600283564d50c6a06c9ed6d8b858c1bb70229ef4226(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb065756ce15bbaf2f4ccd3b0263a44643bc18a4959aa88c7528cf7a463de4d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a7746d51201a590af0a7100d7f846406b802b511542a6ec189ec1f6faf5e87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eb4981674704ab7e2c221bd229fd4103b6f8ea7dfaca332873870268d0a1c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f409a382cc24c8927e9335d099563ddf4fe4fe8f146baeb77e4dba46763ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d722153db71b2f0951f6bf863a939ebfee8c75112a1165400eb982f141a8f2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003ff44d00478531cf83279cf31a37d043196eef9628e0861fdd784b9133b2d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6892790604152b205e0933806ae8381cbcae6bd18141dadb1412504999fd601e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea8c716035508fe0f056fbc8036c1c70665a2f77eeca54eac76097b181e7bdc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c870335c934ee45b8a99e963ba6e15505b4400faa4e1f1ad453fcc6f0a2eb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ebd001702374ff8bf14dd3c1d43f5bb3a996f82c12a29044e7ab1bcd4b9bb26(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2c8d95a8a08e1ff02fbf3ed2fde2eb7f43f36a3237d662f58f1593320b4480(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533f2e164e751a6812514fd3594e7d875b8b845d1feb74b9eda5341b3fb44f37(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0896fcc28aaf48c95a3d9ff3713a06ee94ca835f13d9c3a998c520b21084cfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29115c6f975e6c8f62ba8fdf1ee9c5b088407452f2148d873acf3482a5f02965(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347732ebf52e7c44338604eb2a11330b2abf4038f847076c0c06a465fff65d4f(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9435c9ad1912c63a19b36843f7a5737dc401dea9d97c0999362e9404d268e4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c7afbb03cb25a76afb03a95b844b741b827b200b2bd67f1900be38f3a13d96(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7723dbb66714fdb5f475e56b51c69b359a74ac807a0b06f0221c168f9ba1fd9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8592acc49a98cef675e06cb5466357a4c9b7406ca726c5b0abaea3f62ae3542a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0088ddc74df0581740f2205dce163322e95bcf7bd222f5d1f5a3dd74aef7acee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52ce14b3dcf5aaa3fec18e785a74343b5d5250fc160b8453521492b11d27a5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b720a72002c12528fad4b37578260a648c87c9f2dec99d39fa61837d005d7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0cc1bf60d32f7e91b1b281d9b6d9be4a210ec6b2e44d604fcd64ce483f73e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7da7a5327acef9c93a4c66f7bb0b9cdd176a23939edfc0ff91a17eb3bfb51244(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ce64bd6fba0aeff01a034f39eadf67d0336f25ed2716f11d4efe6f80120985(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df257cab736572653c9d55847320a5e4706466436c45f35185562eb85d85aeb(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f19b50f1708064c3c749308dc9fc3b897f89a6d7ae86605213cfb686dfe827d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78b39177cdb7834e3932bca692923dbf8d7b75255c1a5228abbe440ad674f68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8bcc377a55db5be7a44b64d35f482d89753169ccb3f4de14858e4a4c254a1bb(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigExcludedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0511464f777f0996fad4eae06c80b8032b6bfe1eb7109fe8e3a97ba67c434bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53357cb39616213db81c3d072de4611abc6cac190587d96267971be119500cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6647f6bfd5840d44159579bef4871ebc801b538d4d409793dc20f7657e4f8b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ef0538083a6f868158949b8950d36f008fd3eacd21195e217b41cb97ca6fda(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69e85a9d64da5812fc908c3f5caf218af0db165f88181a08536c87db143d8d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd22f5a4f1d4c9b837a24c4bdce1ecde03bec49f7a4e51ebc9d8101d1feeb71d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94676835ffc9afcecb2a71717c6e697ebfdf54a26883dc18ec4536b5ea320683(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da7677bd1468f1933def4ce5e3d64bf0197a6f61c61a4e4e38c3e801ce9a099(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9b61a69a9133097db1edb319ab1da82617f43c3aeb70d293c25edc4a9c3aef(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb19674a01e96d63fdf98719acc14d4813c26b1f14f4f6213e6b9d07ca5a3df8(
    *,
    group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1208c60d0f428e9bd9c2b1c89195a515f85c05302f0a02c86672e2acedfa3b1(
    *,
    requiring: typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring, typing.Dict[builtins.str, typing.Any]],
    satisfying: typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779d1f443ac4575d3d648e46ac464461f212919e7211c485dc99151e98f991d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96624e4961b377dff603817bf4ffee0ad2c9ab29f4eef80359de321b444e634(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed954f4c788a55d0e154e2effae7a79a8a8a97333554aeaf5145e67d511479ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70b90d954baad866fbcb890cdeb7b9638cf15a8e26b0f6692256b62cda3a875(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6232f84ea225cd1d0bc527b860a2673b5098fca22b75ce0fb20b8d088dddbdcf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0339f92c96c514d157e4dc839538474fcb1a284ad696bc7b7a9a74a05bcbe2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6111129d79990b4978486abb96be3963ed3ee600acefddc64ada5efa147a3011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf4f06c298325846f35112379c1a2b82e63e25bb93697453aec5367541dcbc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb53a8b5ec7c57bf906adf2915085a7432a29ccd6c6f1b03ab428c04d7d8bb1(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bd6e16f4ca264255bc370e7a161ae6544d295aa2e476fc184c8f3c266331e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38391f791b4fc8481e69698566d754fe5de8c972e1d8dccfa7add9add895c93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543a3331171aa78ca71015f8a6f77fe1feffaac1148b57d91dec5879b5c688a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845a43c79cb6edb3908d4570366a9280303ae1ecbddd12b1c2b1f5199de68bbe(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a60c611d10b1efb25d9b1f03b9c573ae256a2aa4830915e6c9a0a4d75fe9a55(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f62aea3ab18bb13aea768d080d3d2b63a672d57d71e0698d507423bfe081c3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8413db42e44031c2bd86707187675239c5a2fb1350ad7a683f3b2c8d8f7ffc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f124072b1d1d663eacd851276c74656c466e940a3220a1ba753b1641b314baec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cdabf0065913081dc0a6c2be1c4b08c3de40e18237db3274da08fef3369982(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563f2e45d832348a655bef38637ca1e2c5fe88daa5c27e3daff165e58105352(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a707ad55ed842c8e70c65c3972dcd8dbe33025ad0c3b26d2b785362fe64d7aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5b6eeb8a94697d9b46bd367a589ca5d7fb6cf69148cc12e123270d6536854c(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigRestoreOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081ec2f0a27c796615b9d7bdc648635930af29ce43214422157578f8d566748b(
    *,
    namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff065486faa11592b395832d5c8360266fd8ddf4a4b899677e85513bbe82e87(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcca24d4268aeac112138a51bac5266f9b1f605961e34e7877c32fbd466a56b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdb645bfffa29d8a5e00ad7162853573467e21f982b875b184fddf0e4140274(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cb8fdcfc8a1ff0d81eb267d45f32255724da46d1116d71998076539e39eb42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9bfb63cff3b6c706db2f7b0268a6761f4576bdbf96d211a78caabc85443d3b2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6cc28418a42f6476877ef4d9a6da0449e8dfe4d6633975480d99961ba836f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19340aececf229125b05ac99e5446b3cf595f364c167530b18c3a6c5a559c4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f9321f9e8e18a6a61afabd426cd833522d513b43d99ca83862bcfd30f84fe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68db6c0d4716881d26db708de93cbd9338899a2d592e9a3a6dbbdfe084d43477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee03272bb8343247dbd5db59a1b3edabb12ec02e9fd9435705711cdee101af3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3247f19d2527eb232a91bd5dfeb07d6d5bf7a719c750146feab839a416186b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2119b635ee927d66ed4ab91c25574bf416d31ad9a1614202954284e688011b14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c44f13d332e19a14b2862c8c8f9ef01fead3e1181d170cd6fc0abed403ad012(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53a709e47accc7bf07a0ae21a80374c4fa6b8434bbf4ab47a7fb6bbd7437a0f(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedApplications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32276926fd5f77a3da36358094af13fe9249f189545315b4ed7bba13b39159d(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1428cd155071c165cc7e9496891bd5a796b0b6c6c8fe2640d1df403dc0b43041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56607d4469bcb83d41b62690e699e75eb57df1de878ecfa61fcb97121eb2f2a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8a9ed708433de9967648dc7e716c149fa732111494fbc3eaa7c46fedc827bf(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigSelectedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222d5fa0d212a3f99ce28539e376d6c9fe04666dfa527c62eb52038e43f9bd92(
    *,
    field_actions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    resource_filter: typing.Optional[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46fea2dd00d0a58de6ffa2013879041a322bfb699dd95670e0a3efb2f15dd0c(
    *,
    op: builtins.str,
    from_path: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20c48b7d6968b1d20b957f974b4eb2807f4ea5f8602850971573c34fa3e62e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9c5269dc6b3fe94b2815ccffa2f17ccdff4b17e00a0de786aadb7edf0123c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7b747fc76ea76ad398e5acceeb7efa08a451ce05fde50efd785ef0cc1a15fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7662b8c6901381a50294763788fa57e4e4a0190675907a774f72e20f53ee67(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cb067c7a2a28bb3b1574c7711e71f402a61273009df2ecf6490c4607946629(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abf530f9e7f2f5e8255f326c37a4dedd65105a63a8e9a5d553a5b31418b4509(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9352021e3d1eeff05fb93a8d1d56571330fedd6a060c37796ac4d587a967472(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb75000cc8460bc3ae71c0fb0598983285d814eac8303bcc383b2b82e418990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497555d20eed72db76c4df88f8f915bbdeeddd5460dd7a4c345603441d9c02ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f69311b7d312f6968ffef64e09e96d217d0c49a7354150622182973df9d9bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68779815f425e66e9f5eef8942be150c0fef7994e37d12e2c04a0b9f8e2b701d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf869a9e53ab892d59609b82e8ad1341e847bf135274426243165e37e2422ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b87f01277a85cd0005c4fccdad1cef7734c0935c97534397f3282f180e4ad7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d53ddb78f5c54cd30cbf8d0df1ddf3ed9ca860dcd4b27a4cab877a1e87b7aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8fb739d621a06ef69dc2ff323ef860daac4b7243923826d9e0be50e1c85b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a83d92ef43797aced074c9ec0830f52e86e43b071568b179268e9741595b948(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37185b5e9dc026a56900832db4d598b70d26b86ff206a8a6eecf6b3a6e81ffb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9181b5131431ec3eb9ea847346183ba40e5cb9d176f734754bf7a40f03418dd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f34e7b45c3b5bf8664130bb798801d01770f25f96bba82d7a08fb8563794a0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a714918b81ea6a61e3d15731f091c47bebe27dd843e5f8259e2258d25503e08a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336f0507b1af7a8717d754fe336cbf214ba1f62e0b7c086835b8459e453c27ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820079928eb0d4ef53fe33c74092c982669b0d228645896463dcd076e281c57c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d92be6a15540acd6060bc0f3363b3fca2605e72dd5a70f2a1503c042178c2d(
    *,
    group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    json_path: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c4895a3226398e8c85f3a2c3c40da0f054dff6337060bae6fcb890897517d1(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fa2ee95b4fbcd6e8bbb44ccfd04e9bbff6407d844d6532e2c4641674eadf76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e25d9c31954217b4bc1da46cc94640dd54732470cf2e800af44383a34f4075f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e27fdd29378edb292d03c65e4276a7ab9e9d87f0a72800a4b1c6e5410bd735f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92924bccc06126d463fb82b3c429f384b8625911239ec5a063460db042c02d51(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71ca1a9f19b9cf60ce16e458a14ad5becf9684953eac054a61d3a9258bf6c79(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fc6d9f71641d7af165260b2ffc5c415d8ae1d05db6f2d645262213f0545757(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2849e066d3ef32cb542b764f397d42f1f62c8158cc623aa13d2205d91bb1169b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ef7afc6f6b6b37ab6be45c7ad3bff25cc6c59ace3bde0420173f5f8c7664d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3986ab6a66b0fe4857a7c51cd8eb0ae73a48ce15b703d1242405f88785af9580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68ced68351603bf85bd8570bc36eb3dd37debb40720a868097211a7c6fabca4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc0d3d78ccf2f1dcbf1db4eba7ea35b67ab4043370a291e0185a45c1bbf8cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7ed9ec7cf391ce5b5d7148283fa9ce6bda2dea2d523bc495680cdb51ad6fdf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53aec3ed0d5649bc7bf41a61abcd00c656b1f8ea4fa8a9a379bf9db56ea0c46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422241e96f4d589072d73901f0ebabbe4e43bfab66bf74555971e17193a847dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e9fe78989122aeafb3f732b0bcb93c2d356fe6b09ab92d750624d77a4074a0(
    value: typing.Optional[GoogleGkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c471f0b973899d91350de98757e409c9cdb27cf764f1153ea956d398c35a4f88(
    *,
    policy: builtins.str,
    volume_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0042744262e99456691719d3a7a87b83577375414ae48f2571a6ef246b9a115e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c1a665c84e534763868c8e74907d7265ae3cf4070af2ecec40b5e07089e533(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b5b268ac5b217d15bc3a1451a4fdb6fa034dff15856b663b20d9bbd72549fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d56906d430f9104cf83b927195c7680f0fd03ace0f43d437d3952f8a936c7b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209e3b0b1e4f5478c1eab2810ca126b674848499d86b7208a980fad4230a0cab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf03fe97a8e7c887e59f61abd01a18ecd8a63979ec97d23f41caa813a5e21661(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504682852981cfcbdc11dbc6d690a38b362fdf27bd3bf8dc0b532de61b5a18ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bce634eb2be7f86792bfb65e7367bf044e23b98a8f7f9df4e10477eac5eb091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e02e18bdace23b591e9b9aa5ed046a240a1bdfe7747447cdfacbe1bca8e965f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2a471b194176db04f9a86a4973d4a4728356044add1e8047549e67f6aa3857(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b75910b81f473922cfe81b2597e5f298365da2e1547894b751390763db75472(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8107b4a05139d81098dadd0541d837b70f221e6839cf4e076ac4c56b6e337c2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0c3b5d0701eb2207954ed549774d931d9c9431ebc8cb29f384547462d3bce4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba315baa802b669d5104b53f995a21983408a195c9039b06bc20325e53b08eb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee813e6ebb1c8f9b78b51b18bcbfac34ac8c9ce128a49d6245de8616efe37db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b485673b10d8450afc84cbab116503906f4000ddc8eff471abe505d4db1cbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeBackupRestorePlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

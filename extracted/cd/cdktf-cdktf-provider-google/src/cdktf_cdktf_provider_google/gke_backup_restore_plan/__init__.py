r'''
# `google_gke_backup_restore_plan`

Refer to the Terraform Registry for docs: [`google_gke_backup_restore_plan`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan).
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


class GkeBackupRestorePlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan google_gke_backup_restore_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_plan: builtins.str,
        cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        restore_config: typing.Union["GkeBackupRestorePlanRestoreConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeBackupRestorePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan google_gke_backup_restore_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_plan: A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#backup_plan GkeBackupRestorePlan#backup_plan}
        :param cluster: The source cluster from which Restores will be created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster GkeBackupRestorePlan#cluster}
        :param location: The region of the Restore Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#location GkeBackupRestorePlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#name GkeBackupRestorePlan#name}
        :param restore_config: restore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_config GkeBackupRestorePlan#restore_config}
        :param description: User specified descriptive string for this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#description GkeBackupRestorePlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#id GkeBackupRestorePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#labels GkeBackupRestorePlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#project GkeBackupRestorePlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#timeouts GkeBackupRestorePlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad89cc045f0f3ee1896bd0e63ee2276121546e5dce44301e6ba115606244f43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeBackupRestorePlanConfig(
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
        '''Generates CDKTF code for importing a GkeBackupRestorePlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeBackupRestorePlan to import.
        :param import_from_id: The id of the existing GkeBackupRestorePlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeBackupRestorePlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49128d317449e7386e2706a015b7561183f9087b37dba540a5fbf8f96ef1768f)
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
        cluster_resource_restore_scope: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_namespaces: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigExcludedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
        no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_order: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrder", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_applications: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_data_restore_policy: typing.Optional[builtins.str] = None,
        volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, restore all namespaced resources in the Backup. Setting this field to False will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_namespaces GkeBackupRestorePlan#all_namespaces}
        :param cluster_resource_conflict_policy: Defines the behavior for handling the situation where cluster-scoped resources being restored already exist in the target cluster. This MUST be set to a value other than 'CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED' if 'clusterResourceRestoreScope' is anyting other than 'noGroupKinds'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#clusterresourceconflictpolicy for more information on each policy option. Possible values: ["USE_EXISTING_VERSION", "USE_BACKUP_VERSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_conflict_policy GkeBackupRestorePlan#cluster_resource_conflict_policy}
        :param cluster_resource_restore_scope: cluster_resource_restore_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_restore_scope GkeBackupRestorePlan#cluster_resource_restore_scope}
        :param excluded_namespaces: excluded_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_namespaces GkeBackupRestorePlan#excluded_namespaces}
        :param namespaced_resource_restore_mode: Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster. This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_resource_restore_mode GkeBackupRestorePlan#namespaced_resource_restore_mode}
        :param no_namespaces: Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_namespaces GkeBackupRestorePlan#no_namespaces}
        :param restore_order: restore_order block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_order GkeBackupRestorePlan#restore_order}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_applications GkeBackupRestorePlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_namespaces GkeBackupRestorePlan#selected_namespaces}
        :param transformation_rules: transformation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#transformation_rules GkeBackupRestorePlan#transformation_rules}
        :param volume_data_restore_policy: Specifies the mechanism to be used to restore volume data. This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy GkeBackupRestorePlan#volume_data_restore_policy}
        :param volume_data_restore_policy_bindings: volume_data_restore_policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy_bindings GkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        value = GkeBackupRestorePlanRestoreConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#create GkeBackupRestorePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#delete GkeBackupRestorePlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#update GkeBackupRestorePlan#update}.
        '''
        value = GkeBackupRestorePlanTimeouts(
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
    def restore_config(self) -> "GkeBackupRestorePlanRestoreConfigOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigOutputReference", jsii.get(self, "restoreConfig"))

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
    def timeouts(self) -> "GkeBackupRestorePlanTimeoutsOutputReference":
        return typing.cast("GkeBackupRestorePlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfig"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfig"], jsii.get(self, "restoreConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeBackupRestorePlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeBackupRestorePlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPlan"))

    @backup_plan.setter
    def backup_plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7f28fa71ec7fe4616d42db63a02a10144dc35fd51528fa7091af186e6762fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPlan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ed8c7ea2c0a044d98e7617c3f524b89170ad1b598151710bae67320b21534f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7972b6bb1027523e28a424884efcb2d99f5afab6c199dd686bef0545c6b4bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee63dab6ca679be0a15a6c714b5312883cf9ce76a2efc56e199bd0cd7aca05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050a03dd82c5e6108e9434282866f8f18921dd4502a63917d02452d799f9a1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb5b8e2ee854f1671089c4c0c809626d6042a49b5d6c45f94b237c5e9d33c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2976fa88935fbff976ed79d1305188dafd02d345e64ec23b7c5b8a99ced58bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e223b65c21b5845bf0c9f72e47b75808fcfee0f5fb8bfaa3e9b4e3f13cfdcca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanConfig",
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
class GkeBackupRestorePlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        restore_config: typing.Union["GkeBackupRestorePlanRestoreConfig", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeBackupRestorePlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_plan: A reference to the BackupPlan from which Backups may be used as the source for Restores created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#backup_plan GkeBackupRestorePlan#backup_plan}
        :param cluster: The source cluster from which Restores will be created via this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster GkeBackupRestorePlan#cluster}
        :param location: The region of the Restore Plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#location GkeBackupRestorePlan#location}
        :param name: The full name of the BackupPlan Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#name GkeBackupRestorePlan#name}
        :param restore_config: restore_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_config GkeBackupRestorePlan#restore_config}
        :param description: User specified descriptive string for this RestorePlan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#description GkeBackupRestorePlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#id GkeBackupRestorePlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Description: A set of custom labels supplied by the user. A list of key->value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#labels GkeBackupRestorePlan#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#project GkeBackupRestorePlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#timeouts GkeBackupRestorePlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(restore_config, dict):
            restore_config = GkeBackupRestorePlanRestoreConfig(**restore_config)
        if isinstance(timeouts, dict):
            timeouts = GkeBackupRestorePlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e75bf6d329a32735f1d3c88ddbdfd54c6670f1377cc538b095450f89265631e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#backup_plan GkeBackupRestorePlan#backup_plan}
        '''
        result = self._values.get("backup_plan")
        assert result is not None, "Required property 'backup_plan' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> builtins.str:
        '''The source cluster from which Restores will be created via this RestorePlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster GkeBackupRestorePlan#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The region of the Restore Plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#location GkeBackupRestorePlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The full name of the BackupPlan Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#name GkeBackupRestorePlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def restore_config(self) -> "GkeBackupRestorePlanRestoreConfig":
        '''restore_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_config GkeBackupRestorePlan#restore_config}
        '''
        result = self._values.get("restore_config")
        assert result is not None, "Required property 'restore_config' is missing"
        return typing.cast("GkeBackupRestorePlanRestoreConfig", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User specified descriptive string for this RestorePlan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#description GkeBackupRestorePlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#id GkeBackupRestorePlan#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#labels GkeBackupRestorePlan#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#project GkeBackupRestorePlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeBackupRestorePlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#timeouts GkeBackupRestorePlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeBackupRestorePlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfig",
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
class GkeBackupRestorePlanRestoreConfig:
    def __init__(
        self,
        *,
        all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_resource_conflict_policy: typing.Optional[builtins.str] = None,
        cluster_resource_restore_scope: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope", typing.Dict[builtins.str, typing.Any]]] = None,
        excluded_namespaces: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigExcludedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
        no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_order: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrder", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_applications: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedApplications", typing.Dict[builtins.str, typing.Any]]] = None,
        selected_namespaces: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedNamespaces", typing.Dict[builtins.str, typing.Any]]] = None,
        transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        volume_data_restore_policy: typing.Optional[builtins.str] = None,
        volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_namespaces: If True, restore all namespaced resources in the Backup. Setting this field to False will result in an error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_namespaces GkeBackupRestorePlan#all_namespaces}
        :param cluster_resource_conflict_policy: Defines the behavior for handling the situation where cluster-scoped resources being restored already exist in the target cluster. This MUST be set to a value other than 'CLUSTER_RESOURCE_CONFLICT_POLICY_UNSPECIFIED' if 'clusterResourceRestoreScope' is anyting other than 'noGroupKinds'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#clusterresourceconflictpolicy for more information on each policy option. Possible values: ["USE_EXISTING_VERSION", "USE_BACKUP_VERSION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_conflict_policy GkeBackupRestorePlan#cluster_resource_conflict_policy}
        :param cluster_resource_restore_scope: cluster_resource_restore_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_restore_scope GkeBackupRestorePlan#cluster_resource_restore_scope}
        :param excluded_namespaces: excluded_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_namespaces GkeBackupRestorePlan#excluded_namespaces}
        :param namespaced_resource_restore_mode: Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster. This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_resource_restore_mode GkeBackupRestorePlan#namespaced_resource_restore_mode}
        :param no_namespaces: Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_namespaces GkeBackupRestorePlan#no_namespaces}
        :param restore_order: restore_order block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_order GkeBackupRestorePlan#restore_order}
        :param selected_applications: selected_applications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_applications GkeBackupRestorePlan#selected_applications}
        :param selected_namespaces: selected_namespaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_namespaces GkeBackupRestorePlan#selected_namespaces}
        :param transformation_rules: transformation_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#transformation_rules GkeBackupRestorePlan#transformation_rules}
        :param volume_data_restore_policy: Specifies the mechanism to be used to restore volume data. This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED' if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'. If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy GkeBackupRestorePlan#volume_data_restore_policy}
        :param volume_data_restore_policy_bindings: volume_data_restore_policy_bindings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy_bindings GkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        if isinstance(cluster_resource_restore_scope, dict):
            cluster_resource_restore_scope = GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(**cluster_resource_restore_scope)
        if isinstance(excluded_namespaces, dict):
            excluded_namespaces = GkeBackupRestorePlanRestoreConfigExcludedNamespaces(**excluded_namespaces)
        if isinstance(restore_order, dict):
            restore_order = GkeBackupRestorePlanRestoreConfigRestoreOrder(**restore_order)
        if isinstance(selected_applications, dict):
            selected_applications = GkeBackupRestorePlanRestoreConfigSelectedApplications(**selected_applications)
        if isinstance(selected_namespaces, dict):
            selected_namespaces = GkeBackupRestorePlanRestoreConfigSelectedNamespaces(**selected_namespaces)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb7e74156fb6fe2cd1235fcf09d70ed0598399628896801a6d014e088d39c51)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_namespaces GkeBackupRestorePlan#all_namespaces}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_conflict_policy GkeBackupRestorePlan#cluster_resource_conflict_policy}
        '''
        result = self._values.get("cluster_resource_conflict_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_resource_restore_scope(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope"]:
        '''cluster_resource_restore_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#cluster_resource_restore_scope GkeBackupRestorePlan#cluster_resource_restore_scope}
        '''
        result = self._values.get("cluster_resource_restore_scope")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope"], result)

    @builtins.property
    def excluded_namespaces(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigExcludedNamespaces"]:
        '''excluded_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_namespaces GkeBackupRestorePlan#excluded_namespaces}
        '''
        result = self._values.get("excluded_namespaces")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigExcludedNamespaces"], result)

    @builtins.property
    def namespaced_resource_restore_mode(self) -> typing.Optional[builtins.str]:
        '''Defines the behavior for handling the situation where sets of namespaced resources being restored already exist in the target cluster.

        This MUST be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED'
        if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'.
        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#namespacedresourcerestoremode
        for more information on each mode. Possible values: ["DELETE_AND_RESTORE", "FAIL_ON_CONFLICT", "MERGE_SKIP_ON_CONFLICT", "MERGE_REPLACE_VOLUME_ON_CONFLICT", "MERGE_REPLACE_ON_CONFLICT"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_resource_restore_mode GkeBackupRestorePlan#namespaced_resource_restore_mode}
        '''
        result = self._values.get("namespaced_resource_restore_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_namespaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not restore any namespaced resources if set to "True". Specifying this field to "False" is not allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_namespaces GkeBackupRestorePlan#no_namespaces}
        '''
        result = self._values.get("no_namespaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restore_order(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrder"]:
        '''restore_order block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#restore_order GkeBackupRestorePlan#restore_order}
        '''
        result = self._values.get("restore_order")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrder"], result)

    @builtins.property
    def selected_applications(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedApplications"]:
        '''selected_applications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_applications GkeBackupRestorePlan#selected_applications}
        '''
        result = self._values.get("selected_applications")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedApplications"], result)

    @builtins.property
    def selected_namespaces(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedNamespaces"]:
        '''selected_namespaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_namespaces GkeBackupRestorePlan#selected_namespaces}
        '''
        result = self._values.get("selected_namespaces")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedNamespaces"], result)

    @builtins.property
    def transformation_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRules"]]]:
        '''transformation_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#transformation_rules GkeBackupRestorePlan#transformation_rules}
        '''
        result = self._values.get("transformation_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRules"]]], result)

    @builtins.property
    def volume_data_restore_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the mechanism to be used to restore volume data.

        This should be set to a value other than 'NAMESPACED_RESOURCE_RESTORE_MODE_UNSPECIFIED'
        if the 'namespacedResourceRestoreScope' is anything other than 'noNamespaces'.
        If not specified, it will be treated as 'NO_VOLUME_DATA_RESTORATION'.
        See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy
        for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy GkeBackupRestorePlan#volume_data_restore_policy}
        '''
        result = self._values.get("volume_data_restore_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_data_restore_policy_bindings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]]:
        '''volume_data_restore_policy_bindings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_data_restore_policy_bindings GkeBackupRestorePlan#volume_data_restore_policy_bindings}
        '''
        result = self._values.get("volume_data_restore_policy_bindings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope",
    jsii_struct_bases=[],
    name_mapping={
        "all_group_kinds": "allGroupKinds",
        "excluded_group_kinds": "excludedGroupKinds",
        "no_group_kinds": "noGroupKinds",
        "selected_group_kinds": "selectedGroupKinds",
    },
)
class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope:
    def __init__(
        self,
        *,
        all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_group_kinds: If True, all valid cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_group_kinds GkeBackupRestorePlan#all_group_kinds}
        :param excluded_group_kinds: excluded_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_group_kinds GkeBackupRestorePlan#excluded_group_kinds}
        :param no_group_kinds: If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_group_kinds GkeBackupRestorePlan#no_group_kinds}
        :param selected_group_kinds: selected_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_group_kinds GkeBackupRestorePlan#selected_group_kinds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8ea71596c1f3de8991804463b1d98820375cf27939db4ef91cc8dbc47900ef)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_group_kinds GkeBackupRestorePlan#all_group_kinds}
        '''
        result = self._values.get("all_group_kinds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def excluded_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds"]]]:
        '''excluded_group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_group_kinds GkeBackupRestorePlan#excluded_group_kinds}
        '''
        result = self._values.get("excluded_group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds"]]], result)

    @builtins.property
    def no_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_group_kinds GkeBackupRestorePlan#no_group_kinds}
        '''
        result = self._values.get("no_group_kinds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selected_group_kinds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]]:
        '''selected_group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_group_kinds GkeBackupRestorePlan#selected_group_kinds}
        '''
        result = self._values.get("selected_group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9109aa51256fd6c72dc2d9753f4495669bad6fd3b1063c470dc50eb790d88803)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cf6d201cd2af60ce7520a3023a21a0e28ec58236ef2884c38aaeac2784ceec0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036a2bce31a5854206ca300c617185a175b752c7f56e364278c25d9f7924eec5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004951226e9b920f9fa837873a987f509e2cf68c6e32b012b7ef3409a032eeec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1c531408a611df66a92f80166e8a070460955c61b13cdc74d0148502feb925c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37319873576aefb1f1bd235816408a8ffab15065a54020d850c571649943cb64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf22d27bd1424cfd03241dc76d775fee6cc2a265139981d7bd2656db4a75e10a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61510443305b26354358d2aa112a48ce28e33daf493709c7164b18e72ce7a052)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b42148f73ba1c971d1ace75480c51cede851d950a7a63ed8e95c55371e433111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac270f1a03d5a4682df7d3dd8039b584e7723de973c244a0d9c0e8c45577d27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1e8e3c6cf33adb6f01275dac04121def1f66fa1d7cff47e1715035f57a9dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__576e902cecdc043a7a3d59bf5218701c068d2cbb3ddb0e83a1c9dcbb33de7662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludedGroupKinds")
    def put_excluded_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497f13fa1be18d0a42261d99464f5af7d3580c82cb3671ac6b5cbabc38088046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedGroupKinds", [value]))

    @jsii.member(jsii_name="putSelectedGroupKinds")
    def put_selected_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__501941f3d79ff17992d317ce384113142fc3f072741131342590bca12e4f0c39)
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
    ) -> GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList:
        return typing.cast(GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList, jsii.get(self, "excludedGroupKinds"))

    @builtins.property
    @jsii.member(jsii_name="selectedGroupKinds")
    def selected_group_kinds(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList":
        return typing.cast("GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList", jsii.get(self, "selectedGroupKinds"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]], jsii.get(self, "excludedGroupKindsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds"]]], jsii.get(self, "selectedGroupKindsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__07a311d805fce0e6218cacb3aae797ca0279176b8dd054b2d34758e86ba50cac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2397419c940a9f3ae890d537d0d48ac98bad9eba80ea6934eb9c7b1b68665231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noGroupKinds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5917d1dafeb9f59208ad0a0023d4eb6e0bea06f549526eb5be22318f6259f155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbde8c35d83581cc7703a335b92436bada9cf826f1bcbb2f62a3e5ee51fc9e21)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb66caab0b2116f17a78250d1ea511e8e044bb8b01c379e7eeb52d7e4188b54d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a389f8ca4066794c349a9abca42e717516b090c2d4629d276ae3455de8f07543)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac54843bf85b2e71edf616b57d624e65abd0c8a1db700ddc00f521c89f48cfb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0caf2d2cd9e24606ebd1d0f5e8cf0ba9a5d4a489b8b563dcf2fe8797ad6b5e4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f07439bfbb0b8c0cf96f916efc2055c7e8a7ef09261932f4afdbed4871c1876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051efd8976409242bb64da74130742a7c83e660db8fe88d5266b18f17f38c36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a196c8f960b19bf8e726eb85d352ad20141294859a77f5064823e317cf21986)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38f4ac5879707382a0c18c169c3e48092658dfa10143668af27ce95f50346131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe842b85bc53b7b1aa9635c240056c5b20cf4873f59a3df4ce15da6d0a4f08e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0bb7b3081676558ba5e17b200fbdac4d7601813ee1ffa0781fe12819e3f5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigExcludedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GkeBackupRestorePlanRestoreConfigExcludedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dc3e4351294ce19c609bc6dd59d7dd2586dcb4416141fff28f81879b15f9b2)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigExcludedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__135b8021e80b41c7a34ede0b5d18ad2b995b3832f0b0f017b1a8e3d061014987)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1f3d2a38052a3783858a124aa0d8ef185e3bb20efb6bf12c6190da0ed97fec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aaaadc028f1db34b91f30d0e4563b3d61665a6ce201e27de314f66f3152f947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b6ca9437ba528b4a4cc14d005e25edf3e4f26bbe26780c146ad8689b7efc0b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putClusterResourceRestoreScope")
    def put_cluster_resource_restore_scope(
        self,
        *,
        all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all_group_kinds: If True, all valid cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#all_group_kinds GkeBackupRestorePlan#all_group_kinds}
        :param excluded_group_kinds: excluded_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#excluded_group_kinds GkeBackupRestorePlan#excluded_group_kinds}
        :param no_group_kinds: If True, no cluster-scoped resources will be restored. Mutually exclusive to any other field in 'clusterResourceRestoreScope'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#no_group_kinds GkeBackupRestorePlan#no_group_kinds}
        :param selected_group_kinds: selected_group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#selected_group_kinds GkeBackupRestorePlan#selected_group_kinds}
        '''
        value = GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope(
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
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        value = GkeBackupRestorePlanRestoreConfigExcludedNamespaces(
            namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putExcludedNamespaces", [value]))

    @jsii.member(jsii_name="putRestoreOrder")
    def put_restore_order(
        self,
        *,
        group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param group_kind_dependencies: group_kind_dependencies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kind_dependencies GkeBackupRestorePlan#group_kind_dependencies}
        '''
        value = GkeBackupRestorePlanRestoreConfigRestoreOrder(
            group_kind_dependencies=group_kind_dependencies
        )

        return typing.cast(None, jsii.invoke(self, "putRestoreOrder", [value]))

    @jsii.member(jsii_name="putSelectedApplications")
    def put_selected_applications(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_names GkeBackupRestorePlan#namespaced_names}
        '''
        value = GkeBackupRestorePlanRestoreConfigSelectedApplications(
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
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        value = GkeBackupRestorePlanRestoreConfigSelectedNamespaces(
            namespaces=namespaces
        )

        return typing.cast(None, jsii.invoke(self, "putSelectedNamespaces", [value]))

    @jsii.member(jsii_name="putTransformationRules")
    def put_transformation_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa572b1f44ce48b4eedcef31cab9d4c3230a3ba630cf4aa1112ff35b897f9ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransformationRules", [value]))

    @jsii.member(jsii_name="putVolumeDataRestorePolicyBindings")
    def put_volume_data_restore_policy_bindings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032d8adfd0e6aa6789b8b4faa62e10ebac6496f1776374b85f166a7dd85140ee)
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
    ) -> GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference:
        return typing.cast(GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference, jsii.get(self, "clusterResourceRestoreScope"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespaces")
    def excluded_namespaces(
        self,
    ) -> GkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference:
        return typing.cast(GkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference, jsii.get(self, "excludedNamespaces"))

    @builtins.property
    @jsii.member(jsii_name="restoreOrder")
    def restore_order(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference", jsii.get(self, "restoreOrder"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplications")
    def selected_applications(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference", jsii.get(self, "selectedApplications"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespaces")
    def selected_namespaces(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference", jsii.get(self, "selectedNamespaces"))

    @builtins.property
    @jsii.member(jsii_name="transformationRules")
    def transformation_rules(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigTransformationRulesList":
        return typing.cast("GkeBackupRestorePlanRestoreConfigTransformationRulesList", jsii.get(self, "transformationRules"))

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicyBindings")
    def volume_data_restore_policy_bindings(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList":
        return typing.cast("GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList", jsii.get(self, "volumeDataRestorePolicyBindings"))

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
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope], jsii.get(self, "clusterResourceRestoreScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedNamespacesInput")
    def excluded_namespaces_input(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces], jsii.get(self, "excludedNamespacesInput"))

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
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrder"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrder"], jsii.get(self, "restoreOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedApplicationsInput")
    def selected_applications_input(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedApplications"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedApplications"], jsii.get(self, "selectedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectedNamespacesInput")
    def selected_namespaces_input(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedNamespaces"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigSelectedNamespaces"], jsii.get(self, "selectedNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="transformationRulesInput")
    def transformation_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRules"]]], jsii.get(self, "transformationRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicyBindingsInput")
    def volume_data_restore_policy_bindings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings"]]], jsii.get(self, "volumeDataRestorePolicyBindingsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fbdea38595d5d1f89bc3164995b2c94c9da503f03879c3147a9c7fc491c56df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterResourceConflictPolicy")
    def cluster_resource_conflict_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceConflictPolicy"))

    @cluster_resource_conflict_policy.setter
    def cluster_resource_conflict_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9799e9ff1c94ba87f8558971eba8c3e1243db0ea02b2f2a211ab1e59a2f773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterResourceConflictPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespacedResourceRestoreMode")
    def namespaced_resource_restore_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespacedResourceRestoreMode"))

    @namespaced_resource_restore_mode.setter
    def namespaced_resource_restore_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2830856b094e904634a944365d446c4cbad545bea5cbd40cf79b177494080b37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3870e2b7b9723416e27f1a8b50cdc35316f10f3d934ad0c958cff5da60c93c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noNamespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeDataRestorePolicy")
    def volume_data_restore_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeDataRestorePolicy"))

    @volume_data_restore_policy.setter
    def volume_data_restore_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58a221ac3d00ba452671abc446f9e671812c91130380c0f453d0b1e9ffc2699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeDataRestorePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeBackupRestorePlanRestoreConfig]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eab4b75b6ccf46f2d04fdcc00110592b66785916edb955d1a7f8b96ebba09e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrder",
    jsii_struct_bases=[],
    name_mapping={"group_kind_dependencies": "groupKindDependencies"},
)
class GkeBackupRestorePlanRestoreConfigRestoreOrder:
    def __init__(
        self,
        *,
        group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param group_kind_dependencies: group_kind_dependencies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kind_dependencies GkeBackupRestorePlan#group_kind_dependencies}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933db51e4a21a13998b39026f25d295a63a9d64d9a5527cd05fbaa128a0ce59f)
            check_type(argname="argument group_kind_dependencies", value=group_kind_dependencies, expected_type=type_hints["group_kind_dependencies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_kind_dependencies": group_kind_dependencies,
        }

    @builtins.property
    def group_kind_dependencies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies"]]:
        '''group_kind_dependencies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kind_dependencies GkeBackupRestorePlan#group_kind_dependencies}
        '''
        result = self._values.get("group_kind_dependencies")
        assert result is not None, "Required property 'group_kind_dependencies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigRestoreOrder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies",
    jsii_struct_bases=[],
    name_mapping={"requiring": "requiring", "satisfying": "satisfying"},
)
class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies:
    def __init__(
        self,
        *,
        requiring: typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring", typing.Dict[builtins.str, typing.Any]],
        satisfying: typing.Union["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param requiring: requiring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#requiring GkeBackupRestorePlan#requiring}
        :param satisfying: satisfying block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#satisfying GkeBackupRestorePlan#satisfying}
        '''
        if isinstance(requiring, dict):
            requiring = GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(**requiring)
        if isinstance(satisfying, dict):
            satisfying = GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(**satisfying)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df8d2f23e72a4c6ac13bf7a07a3432875d73c100fad0b5eb54aa55eead5fe10)
            check_type(argname="argument requiring", value=requiring, expected_type=type_hints["requiring"])
            check_type(argname="argument satisfying", value=satisfying, expected_type=type_hints["satisfying"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "requiring": requiring,
            "satisfying": satisfying,
        }

    @builtins.property
    def requiring(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring":
        '''requiring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#requiring GkeBackupRestorePlan#requiring}
        '''
        result = self._values.get("requiring")
        assert result is not None, "Required property 'requiring' is missing"
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring", result)

    @builtins.property
    def satisfying(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying":
        '''satisfying block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#satisfying GkeBackupRestorePlan#satisfying}
        '''
        result = self._values.get("satisfying")
        assert result is not None, "Required property 'satisfying' is missing"
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a8ca9b02729a9151968c26cc66ec47e4e4ccc0609287c4f78201d5bf105092)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1286401cb7876054f19f03248e9fbc6b0c5e2fac9da5e5eb8687de434a2d24e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174abae8434490ec293f2e57f3400b2b9f51a203ebe62b327413541380c822b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bdcfd0af4e1f256d60ae95f7e22ef5bb96b95d9e34d853896145aa8f46df5bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__813e6350eea00f94991cb8261f413b91285c2c9f2913c28e407e79042e069421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504e5dbd40b4599379153205b982ecc682919701d7e877efecd3083e98ba7a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__939b8cfa33464acb9e9dc451f123e352ca0f1a8a1d55cbb34820aa22de5c00e7)
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
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        value = GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(
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
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        value = GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(
            resource_group=resource_group, resource_kind=resource_kind
        )

        return typing.cast(None, jsii.invoke(self, "putSatisfying", [value]))

    @builtins.property
    @jsii.member(jsii_name="requiring")
    def requiring(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference", jsii.get(self, "requiring"))

    @builtins.property
    @jsii.member(jsii_name="satisfying")
    def satisfying(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference", jsii.get(self, "satisfying"))

    @builtins.property
    @jsii.member(jsii_name="requiringInput")
    def requiring_input(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring"], jsii.get(self, "requiringInput"))

    @builtins.property
    @jsii.member(jsii_name="satisfyingInput")
    def satisfying_input(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying"], jsii.get(self, "satisfyingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b24fda49df62a6c568b1b428bb9b312bfe8a1ffaff6850f087d5dd05241e46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b4eb1e7be63ee43d5353ca5fb863f2ffb3c8d7a7bb12a4fb4adf54193cded3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a3de790efde0a1bc338e7d8f877ca28b9df89d0e1dabbeb22ab0d6578de13f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc9707e227bfb3b0dc3f20f1d723be02d45a843cce876e2d2178c30bb2bbd962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64814d92b4899989529c60e929a69e094486a58c266301a8d4d5bbb69f6f2d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82a65c6908e6e27818dbac31b64b11b13f6966da263f280e2db66a2c1c53dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd565965b0ab37b3decd97c45f3dbb44623ae479611492bb48a56453035a9cbd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7ca7898f57908dcc9e0c11aee188733ab266f3b20d7a8e096f56622439871b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b22897b4b865b5c4847459563490279d80c3e9b644f4032481cfc52380a78c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6ab6c629387c01a71a5994544a8623e2f82209348d5f3403da7a53c1bdebf5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83025d8c9c87d6504ae82401f6864aff6645e0012c6d5e7527688317a202c97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6093af2509b1a1bd994e5646368428004c99d7727fdb1f095324cd7e4d25329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupKindDependencies")
    def put_group_kind_dependencies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0935e22d58cac0ad5c90559c3680d0be40b9e30234258b4d67dc603113822e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroupKindDependencies", [value]))

    @builtins.property
    @jsii.member(jsii_name="groupKindDependencies")
    def group_kind_dependencies(
        self,
    ) -> GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList:
        return typing.cast(GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList, jsii.get(self, "groupKindDependencies"))

    @builtins.property
    @jsii.member(jsii_name="groupKindDependenciesInput")
    def group_kind_dependencies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]], jsii.get(self, "groupKindDependenciesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrder]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrder], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f76620c6fda3317c3bdb78d4eba190bda9a7080bfae4c526904fffa29dc58a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedApplications",
    jsii_struct_bases=[],
    name_mapping={"namespaced_names": "namespacedNames"},
)
class GkeBackupRestorePlanRestoreConfigSelectedApplications:
    def __init__(
        self,
        *,
        namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param namespaced_names: namespaced_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_names GkeBackupRestorePlan#namespaced_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0526ba18388a7bf7858aa99c645e95286f3d72f5a83c16df78bed647fe721be0)
            check_type(argname="argument namespaced_names", value=namespaced_names, expected_type=type_hints["namespaced_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaced_names": namespaced_names,
        }

    @builtins.property
    def namespaced_names(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames"]]:
        '''namespaced_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaced_names GkeBackupRestorePlan#namespaced_names}
        '''
        result = self._values.get("namespaced_names")
        assert result is not None, "Required property 'namespaced_names' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigSelectedApplications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames:
    def __init__(self, *, name: builtins.str, namespace: builtins.str) -> None:
        '''
        :param name: The name of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#name GkeBackupRestorePlan#name}
        :param namespace: The namespace of a Kubernetes Resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespace GkeBackupRestorePlan#namespace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde7e93656eb8844a64a416058a4dd27cef9ffabcee5f62928589f443335dd72)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "namespace": namespace,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#name GkeBackupRestorePlan#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''The namespace of a Kubernetes Resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespace GkeBackupRestorePlan#namespace}
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f767ab0b488ddc33cf560e4ff2de4bbe21378fc9cac8be92a060c08ed91fe2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd249f1f711bf6e3f6389da68eca49710efd60d296dfbd3cbbdb390d83ee86a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4ad185ae1c5cf154f3c31360ca794eb6a1c2dda44c1c2b3a2b53601e9bdb43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9628e523ebac8b8d38f21d7e0f4e0243438c72cdc917a45c2f7c1553105f84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8310c8247e88e9d1c9fe0b70327fd07bcde3273a8fd74eb66d8ea0418f82a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c21b22de2db8f8fc983758b169fdc3524eadee54c2c25b4bf51098635ecd40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5afc96becc66e6b87732c60db7be0b43a28ad412789d71750e9a21f3bc466709)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17e0799da4a5397f3c70b616c90a37caa6af6b3962e105703fea9560fbd53bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8e4f590eedba056997895a3703388e0f561594dc5e475e1e6fcc4f9a8d7853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34be89bb717264e4e94dd832edf9df52bd37a20ea4f4c5914eba4fea7012a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a5a09e3c571d403f5290378b1027034c0c763d59f54df87780fd2916e937734)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNamespacedNames")
    def put_namespaced_names(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd3e4286f24b14cefa6b6ab553a2bcee37bbb6d3d23a9e29e4821d3f269187d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNamespacedNames", [value]))

    @builtins.property
    @jsii.member(jsii_name="namespacedNames")
    def namespaced_names(
        self,
    ) -> GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList:
        return typing.cast(GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList, jsii.get(self, "namespacedNames"))

    @builtins.property
    @jsii.member(jsii_name="namespacedNamesInput")
    def namespaced_names_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]], jsii.get(self, "namespacedNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedApplications]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedApplications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedApplications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb48644d61dea11aeb5ef556639b547a06f8005b870098dafb44f716294d782a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedNamespaces",
    jsii_struct_bases=[],
    name_mapping={"namespaces": "namespaces"},
)
class GkeBackupRestorePlanRestoreConfigSelectedNamespaces:
    def __init__(self, *, namespaces: typing.Sequence[builtins.str]) -> None:
        '''
        :param namespaces: A list of Kubernetes Namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e216ba11109cb63a4f4cf4f472fc3c43d21fbeb2d60b6d05bf8e119be9d67a9)
            check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespaces": namespaces,
        }

    @builtins.property
    def namespaces(self) -> typing.List[builtins.str]:
        '''A list of Kubernetes Namespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        assert result is not None, "Required property 'namespaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigSelectedNamespaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0fcd4819dc298d1c7cf8aaaf2e61952de4461090b9b418a741c50cecdafd6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15236b350d6097689cc4709f42b294dcbc539cb04c6ce9c1e53b9bbe61a1fd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedNamespaces]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedNamespaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedNamespaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6efa8e41897546776767376b1c530cf68744a8feca3c9966f10460b1350d6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRules",
    jsii_struct_bases=[],
    name_mapping={
        "field_actions": "fieldActions",
        "description": "description",
        "resource_filter": "resourceFilter",
    },
)
class GkeBackupRestorePlanRestoreConfigTransformationRules:
    def __init__(
        self,
        *,
        field_actions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        resource_filter: typing.Optional[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param field_actions: field_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#field_actions GkeBackupRestorePlan#field_actions}
        :param description: The description is a user specified string description of the transformation rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#description GkeBackupRestorePlan#description}
        :param resource_filter: resource_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_filter GkeBackupRestorePlan#resource_filter}
        '''
        if isinstance(resource_filter, dict):
            resource_filter = GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(**resource_filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed30063c115cf88963d3128c9eaf0287b240f4e1b3dae0f6525a791ed86b02f4)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions"]]:
        '''field_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#field_actions GkeBackupRestorePlan#field_actions}
        '''
        result = self._values.get("field_actions")
        assert result is not None, "Required property 'field_actions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description is a user specified string description of the transformation rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#description GkeBackupRestorePlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_filter(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"]:
        '''resource_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_filter GkeBackupRestorePlan#resource_filter}
        '''
        result = self._values.get("resource_filter")
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigTransformationRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions",
    jsii_struct_bases=[],
    name_mapping={
        "op": "op",
        "from_path": "fromPath",
        "path": "path",
        "value": "value",
    },
)
class GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions:
    def __init__(
        self,
        *,
        op: builtins.str,
        from_path: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param op: Specifies the operation to perform. Possible values: ["REMOVE", "MOVE", "COPY", "ADD", "TEST", "REPLACE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#op GkeBackupRestorePlan#op}
        :param from_path: A string containing a JSON Pointer value that references the location in the target document to move the value from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#from_path GkeBackupRestorePlan#from_path}
        :param path: A string containing a JSON-Pointer value that references a location within the target document where the operation is performed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#path GkeBackupRestorePlan#path}
        :param value: A string that specifies the desired value in string format to use for transformation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#value GkeBackupRestorePlan#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94e565452511b04f21e48b3dc01e1acfc0592676bde2f2fa44c68f4ee33d8ba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#op GkeBackupRestorePlan#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_path(self) -> typing.Optional[builtins.str]:
        '''A string containing a JSON Pointer value that references the location in the target document to move the value from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#from_path GkeBackupRestorePlan#from_path}
        '''
        result = self._values.get("from_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''A string containing a JSON-Pointer value that references a location within the target document where the operation is performed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#path GkeBackupRestorePlan#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A string that specifies the desired value in string format to use for transformation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#value GkeBackupRestorePlan#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__746b1e08bc9cbbba358f6b3b9fc9c8576fcb7a2cf986166784982826e5273633)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a0a87c2e402f0769bd38a148f1d4b37ed0fb81f076baf2f7d2192dcc38d427b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1aa9eca38f012bbb257e6787cf9428b901311bd8c6c98563988fe65f4e8553)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c766a62b7d78f0237c6b6918fc9f06130454b1cf4dc4505a5456a4b26fafc00d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11abceeb611db34fcf170027271187d3d0765e91261df0f892ba5e10564a8035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d97ff0ebc7154d980242edc8b6384e496e5ba1d57d8a55ed7a79bd6f7e999e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a5ce6335c794daf0fbe36b644b2214afd20eeb518e57d9c3e5fe3e393c36b1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d838957475b7ff3c3232d18d41d8fc166569c40be0859773c97676bac253489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761cf67b062e38ac2c6243457020ef4089be944c132459c48764ee93621dbefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a136cc8cd51e32488d8e5de91040f4f1dd074303874f85d225a89ec9497d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37aea1f5982025cdf00f03327665bf5b3c6152dc7e04a38eb7ac670043c8caa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3a24be12a28c0275f32a1c0907757b9cf28a39581136c923655ed9fbc9083c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigTransformationRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6b8221cdb572bbc79e9897eac64f261f24ff59a16c3d348d80635c1965ff482)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d34b266bed7cebd70887d5b6570e4046b07d6e87773b8108afd2113c6b35f0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1a41573ece0d69ae967336914dbeb799b8e2a968ced987180a65a0407cd7c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d221e698ef0adadaad3dfe0849850b82b1fbca5c55ee95a1fa2bbd528a97f32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c0752d2dd7fc06078b8ca3a45e6ed17af9d0a24e163f2a923554ac49a71f47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edf7983d51c09d78fad1803031b5354ae591d1fe4d78e00b910b426b7738c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae63420b3a6c52856872885a2747a1d5b0d0de25394128664f646317662df3a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFieldActions")
    def put_field_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bcf10f8e61daa08b371189b8856a7fb010e466d035098827dc1b403015b2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldActions", [value]))

    @jsii.member(jsii_name="putResourceFilter")
    def put_resource_filter(
        self,
        *,
        group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        json_path: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_kinds: group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kinds GkeBackupRestorePlan#group_kinds}
        :param json_path: This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#json_path GkeBackupRestorePlan#json_path}
        :param namespaces: (Filtering parameter) Any resource subject to transformation must be contained within one of the listed Kubernetes Namespace in the Backup. If this field is not provided, no namespace filtering will be performed (all resources in all Namespaces, including all cluster-scoped resources, will be candidates for transformation). To mix cluster-scoped and namespaced resources in the same rule, use an empty string ("") as one of the target namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        value = GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(
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
    ) -> GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList:
        return typing.cast(GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList, jsii.get(self, "fieldActions"))

    @builtins.property
    @jsii.member(jsii_name="resourceFilter")
    def resource_filter(
        self,
    ) -> "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference":
        return typing.cast("GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference", jsii.get(self, "resourceFilter"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldActionsInput")
    def field_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]], jsii.get(self, "fieldActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceFilterInput")
    def resource_filter_input(
        self,
    ) -> typing.Optional["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"]:
        return typing.cast(typing.Optional["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter"], jsii.get(self, "resourceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a77012450b499fa821de5d70c522cd30f98901ca2966e5e4ddb7f53e83369d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24d701f9c8d2b6e1006221e2a5140230fda5773ad64198ac8aee142b210e5d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "group_kinds": "groupKinds",
        "json_path": "jsonPath",
        "namespaces": "namespaces",
    },
)
class GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter:
    def __init__(
        self,
        *,
        group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        json_path: typing.Optional[builtins.str] = None,
        namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param group_kinds: group_kinds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kinds GkeBackupRestorePlan#group_kinds}
        :param json_path: This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#json_path GkeBackupRestorePlan#json_path}
        :param namespaces: (Filtering parameter) Any resource subject to transformation must be contained within one of the listed Kubernetes Namespace in the Backup. If this field is not provided, no namespace filtering will be performed (all resources in all Namespaces, including all cluster-scoped resources, will be candidates for transformation). To mix cluster-scoped and namespaced resources in the same rule, use an empty string ("") as one of the target namespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1ae33a316fe673554d58021a5790952182cd4b1b569382b0b596e922ba8d77)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds"]]]:
        '''group_kinds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#group_kinds GkeBackupRestorePlan#group_kinds}
        '''
        result = self._values.get("group_kinds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds"]]], result)

    @builtins.property
    def json_path(self) -> typing.Optional[builtins.str]:
        '''This is a JSONPath expression that matches specific fields of candidate resources and it operates as a filtering parameter (resources that are not matched with this expression will not be candidates for transformation).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#json_path GkeBackupRestorePlan#json_path}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#namespaces GkeBackupRestorePlan#namespaces}
        '''
        result = self._values.get("namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds",
    jsii_struct_bases=[],
    name_mapping={"resource_group": "resourceGroup", "resource_kind": "resourceKind"},
)
class GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds:
    def __init__(
        self,
        *,
        resource_group: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource_group: API Group string of a Kubernetes resource, e.g. "apiextensions.k8s.io", "storage.k8s.io", etc. Use empty string for core group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        :param resource_kind: Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28a89c9e703637369080fe5b43629b42c1113481e773b9a4b4c6bd47ad17204)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_group GkeBackupRestorePlan#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        '''Kind of a Kubernetes resource, e.g. "CustomResourceDefinition", "StorageClass", etc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#resource_kind GkeBackupRestorePlan#resource_kind}
        '''
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aa77e10faf862d605233984af52f9773483e84afb6568e91bbd99951075bd47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12d63b7754660203f7e91cb718154c57e3f9420c1806907e175dee488e6393c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de45572f9f97e0dde2de7800fa03dae7c1c9966147712e04560fd89e979cfdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2158c40782b46190c86e101e28a3406783cf829ddd1ac31f22a3f208c769ca6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__920b5c210fb46871ade0b87f3b41ea0ef8e3c18056ec7ad0f35eaf211ce8af00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a1e027ef94c55372ae05e8f505824f803ed97dae9624042044d547b4dade74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e4bb84c010176efa3641c52cdab66c04f8379aed1aa8247335d0e51c1ba2a64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__989093f3fcb7826dfb185b8b8866c8c5bd32e8b375c909aedc7769be759409ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceKind")
    def resource_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceKind"))

    @resource_kind.setter
    def resource_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27be054b27a3025f8360ac3bc078f0b41db4f21062095f5ae03475eefabab110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3182636f433dc081e200885dca494ce54218e5950e62d4952d78edfa38fc2273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33ba971e3ba596343cc1238abdf424b2d0c20bf85d429d3877b7655a8010745a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroupKinds")
    def put_group_kinds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8324c6ccfa60658d318fe945b2ba76b4406f223b0c462f361e83f065874b07fc)
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
    ) -> GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList:
        return typing.cast(GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList, jsii.get(self, "groupKinds"))

    @builtins.property
    @jsii.member(jsii_name="groupKindsInput")
    def group_kinds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]], jsii.get(self, "groupKindsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5324cb4b870b6e44465ba6489f3daca522eab02b4e75dc12af9cab5ef7faaadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespaces")
    def namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namespaces"))

    @namespaces.setter
    def namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bae8cd9ad5dddf0929363779de88d210eee30afb7441c7a07bb98ca43acfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaces", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter]:
        return typing.cast(typing.Optional[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfd494b941816162d3dee1b9f9124df9db9b2b5ce23770e18cff0dba7cae377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "volume_type": "volumeType"},
)
class GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings:
    def __init__(self, *, policy: builtins.str, volume_type: builtins.str) -> None:
        '''
        :param policy: Specifies the mechanism to be used to restore this volume data. See https://cloud.google.com/kubernetes-engine/docs/add-on/backup-for-gke/reference/rest/v1/RestoreConfig#VolumeDataRestorePolicy for more information on each policy option. Possible values: ["RESTORE_VOLUME_DATA_FROM_BACKUP", "REUSE_VOLUME_HANDLE_FROM_BACKUP", "NO_VOLUME_DATA_RESTORATION"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#policy GkeBackupRestorePlan#policy}
        :param volume_type: The volume type, as determined by the PVC's bound PV, to apply the policy to. Possible values: ["GCE_PERSISTENT_DISK"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_type GkeBackupRestorePlan#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f00614a25597cbdc208fd3ea9acf8ee139167be62696b50746e65c0e9f54e8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#policy GkeBackupRestorePlan#policy}
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_type(self) -> builtins.str:
        '''The volume type, as determined by the PVC's bound PV, to apply the policy to. Possible values: ["GCE_PERSISTENT_DISK"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#volume_type GkeBackupRestorePlan#volume_type}
        '''
        result = self._values.get("volume_type")
        assert result is not None, "Required property 'volume_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__663081e681809800f1d51164bdbcbb3a39559be143269bcb496b5adbc014a0a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669eeabb725da79584023bac2e4f5001eec62dba7f0f129bc1fad7eff20a7d0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b459770726d54356cc2dc9e1e207c184efb94bd4288b153e401239bdceacb8a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d69d15b935ab71eb508741f4f89c7857fe0b61a20c543218e83a70164243665)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c82b5fd5aad9f28c5300c8c28ab25e123db765ba92f12ef8d8c08178b5a439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cd8c39d84d12adcf0f2a9737ecc9e43badddf999342ff5e08552f5e54a1d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a461aff857c9bbf7a67dda05e986ff366f774d0638078027a00a4343a6d78f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__458d6aef3f1e59e9aac4139df6574b32ad71e6b7067d3f1f8d21361f6347a835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a323822b804c29aa4dc0d5bd3181afecf477bdd966beb3c1e6d9fd2f2547bf02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0fe504dd7cd725f84927b25af1fa63b4248e58e7e3626140ca9464d2092896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeBackupRestorePlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#create GkeBackupRestorePlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#delete GkeBackupRestorePlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#update GkeBackupRestorePlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ee245e638c98fea4e5a4a520b24fbedbcc9c169bf3c55aa0a8265bdae44acc)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#create GkeBackupRestorePlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#delete GkeBackupRestorePlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gke_backup_restore_plan#update GkeBackupRestorePlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeBackupRestorePlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeBackupRestorePlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeBackupRestorePlan.GkeBackupRestorePlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d8349164bdffd63e08cafcd40b726d92bfaa34117fc5a295641084fc3daa66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__695c01b9465efe4a0c03731e6070de22387fbb8635d7b6f66209b0ec6b52bec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acb45096b631186172313cf59ca98da271e8dd48f49263e55938e92e41d6dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa037767d34a9d7a829868a8b5877b5caca0ae02c05beddcdd060410425938b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801beb4d497feab9ba2528c7e6cf048561a4357b4fc018f9d2334205265b035e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeBackupRestorePlan",
    "GkeBackupRestorePlanConfig",
    "GkeBackupRestorePlanRestoreConfig",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsList",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKindsOutputReference",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeOutputReference",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsList",
    "GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKindsOutputReference",
    "GkeBackupRestorePlanRestoreConfigExcludedNamespaces",
    "GkeBackupRestorePlanRestoreConfigExcludedNamespacesOutputReference",
    "GkeBackupRestorePlanRestoreConfigOutputReference",
    "GkeBackupRestorePlanRestoreConfigRestoreOrder",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesList",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesOutputReference",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiringOutputReference",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfyingOutputReference",
    "GkeBackupRestorePlanRestoreConfigRestoreOrderOutputReference",
    "GkeBackupRestorePlanRestoreConfigSelectedApplications",
    "GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames",
    "GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesList",
    "GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNamesOutputReference",
    "GkeBackupRestorePlanRestoreConfigSelectedApplicationsOutputReference",
    "GkeBackupRestorePlanRestoreConfigSelectedNamespaces",
    "GkeBackupRestorePlanRestoreConfigSelectedNamespacesOutputReference",
    "GkeBackupRestorePlanRestoreConfigTransformationRules",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsList",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActionsOutputReference",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesList",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesOutputReference",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsList",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKindsOutputReference",
    "GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterOutputReference",
    "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings",
    "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsList",
    "GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindingsOutputReference",
    "GkeBackupRestorePlanTimeouts",
    "GkeBackupRestorePlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__fad89cc045f0f3ee1896bd0e63ee2276121546e5dce44301e6ba115606244f43(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_plan: builtins.str,
    cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    restore_config: typing.Union[GkeBackupRestorePlanRestoreConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeBackupRestorePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__49128d317449e7386e2706a015b7561183f9087b37dba540a5fbf8f96ef1768f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7f28fa71ec7fe4616d42db63a02a10144dc35fd51528fa7091af186e6762fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ed8c7ea2c0a044d98e7617c3f524b89170ad1b598151710bae67320b21534f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7972b6bb1027523e28a424884efcb2d99f5afab6c199dd686bef0545c6b4bc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee63dab6ca679be0a15a6c714b5312883cf9ce76a2efc56e199bd0cd7aca05b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050a03dd82c5e6108e9434282866f8f18921dd4502a63917d02452d799f9a1f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb5b8e2ee854f1671089c4c0c809626d6042a49b5d6c45f94b237c5e9d33c30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2976fa88935fbff976ed79d1305188dafd02d345e64ec23b7c5b8a99ced58bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e223b65c21b5845bf0c9f72e47b75808fcfee0f5fb8bfaa3e9b4e3f13cfdcca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e75bf6d329a32735f1d3c88ddbdfd54c6670f1377cc538b095450f89265631e(
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
    restore_config: typing.Union[GkeBackupRestorePlanRestoreConfig, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeBackupRestorePlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb7e74156fb6fe2cd1235fcf09d70ed0598399628896801a6d014e088d39c51(
    *,
    all_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cluster_resource_conflict_policy: typing.Optional[builtins.str] = None,
    cluster_resource_restore_scope: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope, typing.Dict[builtins.str, typing.Any]]] = None,
    excluded_namespaces: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigExcludedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
    namespaced_resource_restore_mode: typing.Optional[builtins.str] = None,
    no_namespaces: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore_order: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrder, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_applications: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigSelectedApplications, typing.Dict[builtins.str, typing.Any]]] = None,
    selected_namespaces: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigSelectedNamespaces, typing.Dict[builtins.str, typing.Any]]] = None,
    transformation_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    volume_data_restore_policy: typing.Optional[builtins.str] = None,
    volume_data_restore_policy_bindings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8ea71596c1f3de8991804463b1d98820375cf27939db4ef91cc8dbc47900ef(
    *,
    all_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    excluded_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    no_group_kinds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selected_group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9109aa51256fd6c72dc2d9753f4495669bad6fd3b1063c470dc50eb790d88803(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf6d201cd2af60ce7520a3023a21a0e28ec58236ef2884c38aaeac2784ceec0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036a2bce31a5854206ca300c617185a175b752c7f56e364278c25d9f7924eec5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004951226e9b920f9fa837873a987f509e2cf68c6e32b012b7ef3409a032eeec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c531408a611df66a92f80166e8a070460955c61b13cdc74d0148502feb925c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37319873576aefb1f1bd235816408a8ffab15065a54020d850c571649943cb64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf22d27bd1424cfd03241dc76d775fee6cc2a265139981d7bd2656db4a75e10a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61510443305b26354358d2aa112a48ce28e33daf493709c7164b18e72ce7a052(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42148f73ba1c971d1ace75480c51cede851d950a7a63ed8e95c55371e433111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac270f1a03d5a4682df7d3dd8039b584e7723de973c244a0d9c0e8c45577d27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1e8e3c6cf33adb6f01275dac04121def1f66fa1d7cff47e1715035f57a9dd6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576e902cecdc043a7a3d59bf5218701c068d2cbb3ddb0e83a1c9dcbb33de7662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497f13fa1be18d0a42261d99464f5af7d3580c82cb3671ac6b5cbabc38088046(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeExcludedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501941f3d79ff17992d317ce384113142fc3f072741131342590bca12e4f0c39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a311d805fce0e6218cacb3aae797ca0279176b8dd054b2d34758e86ba50cac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2397419c940a9f3ae890d537d0d48ac98bad9eba80ea6934eb9c7b1b68665231(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5917d1dafeb9f59208ad0a0023d4eb6e0bea06f549526eb5be22318f6259f155(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbde8c35d83581cc7703a335b92436bada9cf826f1bcbb2f62a3e5ee51fc9e21(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb66caab0b2116f17a78250d1ea511e8e044bb8b01c379e7eeb52d7e4188b54d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a389f8ca4066794c349a9abca42e717516b090c2d4629d276ae3455de8f07543(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac54843bf85b2e71edf616b57d624e65abd0c8a1db700ddc00f521c89f48cfb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0caf2d2cd9e24606ebd1d0f5e8cf0ba9a5d4a489b8b563dcf2fe8797ad6b5e4b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f07439bfbb0b8c0cf96f916efc2055c7e8a7ef09261932f4afdbed4871c1876(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051efd8976409242bb64da74130742a7c83e660db8fe88d5266b18f17f38c36c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a196c8f960b19bf8e726eb85d352ad20141294859a77f5064823e317cf21986(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f4ac5879707382a0c18c169c3e48092658dfa10143668af27ce95f50346131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe842b85bc53b7b1aa9635c240056c5b20cf4873f59a3df4ce15da6d0a4f08e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0bb7b3081676558ba5e17b200fbdac4d7601813ee1ffa0781fe12819e3f5da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigClusterResourceRestoreScopeSelectedGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dc3e4351294ce19c609bc6dd59d7dd2586dcb4416141fff28f81879b15f9b2(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135b8021e80b41c7a34ede0b5d18ad2b995b3832f0b0f017b1a8e3d061014987(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f3d2a38052a3783858a124aa0d8ef185e3bb20efb6bf12c6190da0ed97fec8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aaaadc028f1db34b91f30d0e4563b3d61665a6ce201e27de314f66f3152f947(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigExcludedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6ca9437ba528b4a4cc14d005e25edf3e4f26bbe26780c146ad8689b7efc0b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa572b1f44ce48b4eedcef31cab9d4c3230a3ba630cf4aa1112ff35b897f9ce7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032d8adfd0e6aa6789b8b4faa62e10ebac6496f1776374b85f166a7dd85140ee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdea38595d5d1f89bc3164995b2c94c9da503f03879c3147a9c7fc491c56df9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9799e9ff1c94ba87f8558971eba8c3e1243db0ea02b2f2a211ab1e59a2f773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2830856b094e904634a944365d446c4cbad545bea5cbd40cf79b177494080b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3870e2b7b9723416e27f1a8b50cdc35316f10f3d934ad0c958cff5da60c93c61(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58a221ac3d00ba452671abc446f9e671812c91130380c0f453d0b1e9ffc2699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eab4b75b6ccf46f2d04fdcc00110592b66785916edb955d1a7f8b96ebba09e0(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933db51e4a21a13998b39026f25d295a63a9d64d9a5527cd05fbaa128a0ce59f(
    *,
    group_kind_dependencies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df8d2f23e72a4c6ac13bf7a07a3432875d73c100fad0b5eb54aa55eead5fe10(
    *,
    requiring: typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring, typing.Dict[builtins.str, typing.Any]],
    satisfying: typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a8ca9b02729a9151968c26cc66ec47e4e4ccc0609287c4f78201d5bf105092(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1286401cb7876054f19f03248e9fbc6b0c5e2fac9da5e5eb8687de434a2d24e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174abae8434490ec293f2e57f3400b2b9f51a203ebe62b327413541380c822b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdcfd0af4e1f256d60ae95f7e22ef5bb96b95d9e34d853896145aa8f46df5bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813e6350eea00f94991cb8261f413b91285c2c9f2913c28e407e79042e069421(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504e5dbd40b4599379153205b982ecc682919701d7e877efecd3083e98ba7a3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939b8cfa33464acb9e9dc451f123e352ca0f1a8a1d55cbb34820aa22de5c00e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b24fda49df62a6c568b1b428bb9b312bfe8a1ffaff6850f087d5dd05241e46b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b4eb1e7be63ee43d5353ca5fb863f2ffb3c8d7a7bb12a4fb4adf54193cded3(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a3de790efde0a1bc338e7d8f877ca28b9df89d0e1dabbeb22ab0d6578de13f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9707e227bfb3b0dc3f20f1d723be02d45a843cce876e2d2178c30bb2bbd962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64814d92b4899989529c60e929a69e094486a58c266301a8d4d5bbb69f6f2d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82a65c6908e6e27818dbac31b64b11b13f6966da263f280e2db66a2c1c53dae(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesRequiring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd565965b0ab37b3decd97c45f3dbb44623ae479611492bb48a56453035a9cbd(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ca7898f57908dcc9e0c11aee188733ab266f3b20d7a8e096f56622439871b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b22897b4b865b5c4847459563490279d80c3e9b644f4032481cfc52380a78c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6ab6c629387c01a71a5994544a8623e2f82209348d5f3403da7a53c1bdebf5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83025d8c9c87d6504ae82401f6864aff6645e0012c6d5e7527688317a202c97d(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependenciesSatisfying],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6093af2509b1a1bd994e5646368428004c99d7727fdb1f095324cd7e4d25329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0935e22d58cac0ad5c90559c3680d0be40b9e30234258b4d67dc603113822e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigRestoreOrderGroupKindDependencies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f76620c6fda3317c3bdb78d4eba190bda9a7080bfae4c526904fffa29dc58a1(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigRestoreOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0526ba18388a7bf7858aa99c645e95286f3d72f5a83c16df78bed647fe721be0(
    *,
    namespaced_names: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde7e93656eb8844a64a416058a4dd27cef9ffabcee5f62928589f443335dd72(
    *,
    name: builtins.str,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f767ab0b488ddc33cf560e4ff2de4bbe21378fc9cac8be92a060c08ed91fe2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd249f1f711bf6e3f6389da68eca49710efd60d296dfbd3cbbdb390d83ee86a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4ad185ae1c5cf154f3c31360ca794eb6a1c2dda44c1c2b3a2b53601e9bdb43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9628e523ebac8b8d38f21d7e0f4e0243438c72cdc917a45c2f7c1553105f84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8310c8247e88e9d1c9fe0b70327fd07bcde3273a8fd74eb66d8ea0418f82a9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c21b22de2db8f8fc983758b169fdc3524eadee54c2c25b4bf51098635ecd40(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afc96becc66e6b87732c60db7be0b43a28ad412789d71750e9a21f3bc466709(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e0799da4a5397f3c70b616c90a37caa6af6b3962e105703fea9560fbd53bc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8e4f590eedba056997895a3703388e0f561594dc5e475e1e6fcc4f9a8d7853(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34be89bb717264e4e94dd832edf9df52bd37a20ea4f4c5914eba4fea7012a82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5a09e3c571d403f5290378b1027034c0c763d59f54df87780fd2916e937734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd3e4286f24b14cefa6b6ab553a2bcee37bbb6d3d23a9e29e4821d3f269187d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigSelectedApplicationsNamespacedNames, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb48644d61dea11aeb5ef556639b547a06f8005b870098dafb44f716294d782a(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedApplications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e216ba11109cb63a4f4cf4f472fc3c43d21fbeb2d60b6d05bf8e119be9d67a9(
    *,
    namespaces: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0fcd4819dc298d1c7cf8aaaf2e61952de4461090b9b418a741c50cecdafd6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15236b350d6097689cc4709f42b294dcbc539cb04c6ce9c1e53b9bbe61a1fd80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6efa8e41897546776767376b1c530cf68744a8feca3c9966f10460b1350d6ec(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigSelectedNamespaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed30063c115cf88963d3128c9eaf0287b240f4e1b3dae0f6525a791ed86b02f4(
    *,
    field_actions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    resource_filter: typing.Optional[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94e565452511b04f21e48b3dc01e1acfc0592676bde2f2fa44c68f4ee33d8ba(
    *,
    op: builtins.str,
    from_path: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746b1e08bc9cbbba358f6b3b9fc9c8576fcb7a2cf986166784982826e5273633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0a87c2e402f0769bd38a148f1d4b37ed0fb81f076baf2f7d2192dcc38d427b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1aa9eca38f012bbb257e6787cf9428b901311bd8c6c98563988fe65f4e8553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c766a62b7d78f0237c6b6918fc9f06130454b1cf4dc4505a5456a4b26fafc00d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11abceeb611db34fcf170027271187d3d0765e91261df0f892ba5e10564a8035(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d97ff0ebc7154d980242edc8b6384e496e5ba1d57d8a55ed7a79bd6f7e999e1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5ce6335c794daf0fbe36b644b2214afd20eeb518e57d9c3e5fe3e393c36b1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d838957475b7ff3c3232d18d41d8fc166569c40be0859773c97676bac253489(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761cf67b062e38ac2c6243457020ef4089be944c132459c48764ee93621dbefc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a136cc8cd51e32488d8e5de91040f4f1dd074303874f85d225a89ec9497d7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37aea1f5982025cdf00f03327665bf5b3c6152dc7e04a38eb7ac670043c8caa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3a24be12a28c0275f32a1c0907757b9cf28a39581136c923655ed9fbc9083c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b8221cdb572bbc79e9897eac64f261f24ff59a16c3d348d80635c1965ff482(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d34b266bed7cebd70887d5b6570e4046b07d6e87773b8108afd2113c6b35f0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1a41573ece0d69ae967336914dbeb799b8e2a968ced987180a65a0407cd7c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d221e698ef0adadaad3dfe0849850b82b1fbca5c55ee95a1fa2bbd528a97f32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0752d2dd7fc06078b8ca3a45e6ed17af9d0a24e163f2a923554ac49a71f47d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edf7983d51c09d78fad1803031b5354ae591d1fe4d78e00b910b426b7738c81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae63420b3a6c52856872885a2747a1d5b0d0de25394128664f646317662df3a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bcf10f8e61daa08b371189b8856a7fb010e466d035098827dc1b403015b2c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesFieldActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a77012450b499fa821de5d70c522cd30f98901ca2966e5e4ddb7f53e83369d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24d701f9c8d2b6e1006221e2a5140230fda5773ad64198ac8aee142b210e5d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1ae33a316fe673554d58021a5790952182cd4b1b569382b0b596e922ba8d77(
    *,
    group_kinds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    json_path: typing.Optional[builtins.str] = None,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28a89c9e703637369080fe5b43629b42c1113481e773b9a4b4c6bd47ad17204(
    *,
    resource_group: typing.Optional[builtins.str] = None,
    resource_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa77e10faf862d605233984af52f9773483e84afb6568e91bbd99951075bd47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12d63b7754660203f7e91cb718154c57e3f9420c1806907e175dee488e6393c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de45572f9f97e0dde2de7800fa03dae7c1c9966147712e04560fd89e979cfdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2158c40782b46190c86e101e28a3406783cf829ddd1ac31f22a3f208c769ca6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920b5c210fb46871ade0b87f3b41ea0ef8e3c18056ec7ad0f35eaf211ce8af00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a1e027ef94c55372ae05e8f505824f803ed97dae9624042044d547b4dade74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4bb84c010176efa3641c52cdab66c04f8379aed1aa8247335d0e51c1ba2a64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989093f3fcb7826dfb185b8b8866c8c5bd32e8b375c909aedc7769be759409ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27be054b27a3025f8360ac3bc078f0b41db4f21062095f5ae03475eefabab110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3182636f433dc081e200885dca494ce54218e5950e62d4952d78edfa38fc2273(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ba971e3ba596343cc1238abdf424b2d0c20bf85d429d3877b7655a8010745a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8324c6ccfa60658d318fe945b2ba76b4406f223b0c462f361e83f065874b07fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilterGroupKinds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5324cb4b870b6e44465ba6489f3daca522eab02b4e75dc12af9cab5ef7faaadd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bae8cd9ad5dddf0929363779de88d210eee30afb7441c7a07bb98ca43acfc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfd494b941816162d3dee1b9f9124df9db9b2b5ce23770e18cff0dba7cae377(
    value: typing.Optional[GkeBackupRestorePlanRestoreConfigTransformationRulesResourceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f00614a25597cbdc208fd3ea9acf8ee139167be62696b50746e65c0e9f54e8(
    *,
    policy: builtins.str,
    volume_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663081e681809800f1d51164bdbcbb3a39559be143269bcb496b5adbc014a0a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669eeabb725da79584023bac2e4f5001eec62dba7f0f129bc1fad7eff20a7d0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b459770726d54356cc2dc9e1e207c184efb94bd4288b153e401239bdceacb8a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d69d15b935ab71eb508741f4f89c7857fe0b61a20c543218e83a70164243665(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c82b5fd5aad9f28c5300c8c28ab25e123db765ba92f12ef8d8c08178b5a439(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cd8c39d84d12adcf0f2a9737ecc9e43badddf999342ff5e08552f5e54a1d96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a461aff857c9bbf7a67dda05e986ff366f774d0638078027a00a4343a6d78f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458d6aef3f1e59e9aac4139df6574b32ad71e6b7067d3f1f8d21361f6347a835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a323822b804c29aa4dc0d5bd3181afecf477bdd966beb3c1e6d9fd2f2547bf02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0fe504dd7cd725f84927b25af1fa63b4248e58e7e3626140ca9464d2092896(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanRestoreConfigVolumeDataRestorePolicyBindings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ee245e638c98fea4e5a4a520b24fbedbcc9c169bf3c55aa0a8265bdae44acc(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d8349164bdffd63e08cafcd40b726d92bfaa34117fc5a295641084fc3daa66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695c01b9465efe4a0c03731e6070de22387fbb8635d7b6f66209b0ec6b52bec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acb45096b631186172313cf59ca98da271e8dd48f49263e55938e92e41d6dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa037767d34a9d7a829868a8b5877b5caca0ae02c05beddcdd060410425938b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801beb4d497feab9ba2528c7e6cf048561a4357b4fc018f9d2334205265b035e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeBackupRestorePlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

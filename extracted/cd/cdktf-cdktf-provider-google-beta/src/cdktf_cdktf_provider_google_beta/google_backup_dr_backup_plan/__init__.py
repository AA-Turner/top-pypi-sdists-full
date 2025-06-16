r'''
# `google_backup_dr_backup_plan`

Refer to the Terraform Registry for docs: [`google_backup_dr_backup_plan`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan).
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


class GoogleBackupDrBackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan google_backup_dr_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_plan_id: builtins.str,
        backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBackupDrBackupPlanBackupRules", typing.Dict[builtins.str, typing.Any]]]],
        backup_vault: builtins.str,
        location: builtins.str,
        resource_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBackupDrBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan google_backup_dr_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_plan_id: The ID of the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_plan_id GoogleBackupDrBackupPlan#backup_plan_id}
        :param backup_rules: backup_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_rules GoogleBackupDrBackupPlan#backup_rules}
        :param backup_vault: Backup vault where the backups gets stored using this Backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_vault GoogleBackupDrBackupPlan#backup_vault}
        :param location: The location for the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#location GoogleBackupDrBackupPlan#location}
        :param resource_type: The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance" and "storage.googleapis.com/Bucket". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#resource_type GoogleBackupDrBackupPlan#resource_type}
        :param description: The description allows for additional details about 'BackupPlan' and its use cases to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#description GoogleBackupDrBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#id GoogleBackupDrBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#project GoogleBackupDrBackupPlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#timeouts GoogleBackupDrBackupPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d894deb8d452c8c80fb073fde09ec9e5fbdc926253a4b9a24332dce3ff00fec8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBackupDrBackupPlanConfig(
            backup_plan_id=backup_plan_id,
            backup_rules=backup_rules,
            backup_vault=backup_vault,
            location=location,
            resource_type=resource_type,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleBackupDrBackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBackupDrBackupPlan to import.
        :param import_from_id: The id of the existing GoogleBackupDrBackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBackupDrBackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca1102b8c4b760b8108f77f12bb86faaf415a465dcafb8094ac882606ca94a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupRules")
    def put_backup_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBackupDrBackupPlanBackupRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4e68f05f2c53afae924b07a47e4c2fee57fdf0494f961e4f7f2708f248b751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackupRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#create GoogleBackupDrBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#delete GoogleBackupDrBackupPlan#delete}.
        '''
        value = GoogleBackupDrBackupPlanTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="backupRules")
    def backup_rules(self) -> "GoogleBackupDrBackupPlanBackupRulesList":
        return typing.cast("GoogleBackupDrBackupPlanBackupRulesList", jsii.get(self, "backupRules"))

    @builtins.property
    @jsii.member(jsii_name="backupVaultServiceAccount")
    def backup_vault_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupVaultServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBackupDrBackupPlanTimeoutsOutputReference":
        return typing.cast("GoogleBackupDrBackupPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="backupPlanIdInput")
    def backup_plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupPlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRulesInput")
    def backup_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBackupDrBackupPlanBackupRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBackupDrBackupPlanBackupRules"]]], jsii.get(self, "backupRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="backupVaultInput")
    def backup_vault_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backupVaultInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBackupDrBackupPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBackupDrBackupPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))

    @backup_plan_id.setter
    def backup_plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfad1805bdb2463861a4b41d08c5c52a5feb851f1cf355c78f6eace623beef3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPlanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupVault"))

    @backup_vault.setter
    def backup_vault(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cc9983d75f8f8aa25797abb9509ea7254335a9fc45e852244b719240e37206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupVault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f4ec8137764258869fbb6557de7a0a660ad1746d74ad332e28951eda130bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cdb377c54bb31ea9f9a44fda59e9669836d87d85c15ed2c6d0356cae67e77c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e88fee3852a9e757715cee396187bd01a8ca4df14fb69d46e585f25258e992c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbbd6d1951f0e5c4daea358a391d42e9181a76f4b86fea103f3301ba3fdd5be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77231b5ff947ac00d4415abb9ae94d1b832c29cf5ba7141783512db3d3be5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRules",
    jsii_struct_bases=[],
    name_mapping={
        "backup_retention_days": "backupRetentionDays",
        "rule_id": "ruleId",
        "standard_schedule": "standardSchedule",
    },
)
class GoogleBackupDrBackupPlanBackupRules:
    def __init__(
        self,
        *,
        backup_retention_days: jsii.Number,
        rule_id: builtins.str,
        standard_schedule: typing.Union["GoogleBackupDrBackupPlanBackupRulesStandardSchedule", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param backup_retention_days: Configures the duration for which backup data will be kept. The value should be greater than or equal to minimum enforced retention of the backup vault. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_retention_days GoogleBackupDrBackupPlan#backup_retention_days}
        :param rule_id: The unique ID of this 'BackupRule'. The 'rule_id' is unique per 'BackupPlan'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#rule_id GoogleBackupDrBackupPlan#rule_id}
        :param standard_schedule: standard_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#standard_schedule GoogleBackupDrBackupPlan#standard_schedule}
        '''
        if isinstance(standard_schedule, dict):
            standard_schedule = GoogleBackupDrBackupPlanBackupRulesStandardSchedule(**standard_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3081e9b3c9245c6a2adc59518801a8f11d6869d985c7bc984ff667e7dc4aeb)
            check_type(argname="argument backup_retention_days", value=backup_retention_days, expected_type=type_hints["backup_retention_days"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument standard_schedule", value=standard_schedule, expected_type=type_hints["standard_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_retention_days": backup_retention_days,
            "rule_id": rule_id,
            "standard_schedule": standard_schedule,
        }

    @builtins.property
    def backup_retention_days(self) -> jsii.Number:
        '''Configures the duration for which backup data will be kept.

        The value should be greater than or equal to minimum enforced retention of the backup vault.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_retention_days GoogleBackupDrBackupPlan#backup_retention_days}
        '''
        result = self._values.get("backup_retention_days")
        assert result is not None, "Required property 'backup_retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_id(self) -> builtins.str:
        '''The unique ID of this 'BackupRule'. The 'rule_id' is unique per 'BackupPlan'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#rule_id GoogleBackupDrBackupPlan#rule_id}
        '''
        result = self._values.get("rule_id")
        assert result is not None, "Required property 'rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_schedule(
        self,
    ) -> "GoogleBackupDrBackupPlanBackupRulesStandardSchedule":
        '''standard_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#standard_schedule GoogleBackupDrBackupPlan#standard_schedule}
        '''
        result = self._values.get("standard_schedule")
        assert result is not None, "Required property 'standard_schedule' is missing"
        return typing.cast("GoogleBackupDrBackupPlanBackupRulesStandardSchedule", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanBackupRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBackupDrBackupPlanBackupRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d53f18ad78e06ffcde8c8bc74350b0f3a5d5ea63ae0fc2cc37eb282b796bfd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBackupDrBackupPlanBackupRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2610b4c671e0cf4217277a2a821d651532c6c28cba1821252dea80644b7402e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBackupDrBackupPlanBackupRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82c0bf83ba82f5cdca0f64a3a417951ea8298107f133781a8cbc45dcbec6e61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0f715ba280b81af34840dde6d48e8aa3433368b9aa26c27aeb370b20415ff3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7546aa0a9b20a1d74f5270fba066231d6f2a5f31b0f0cc99b63edc4bd47a9d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da12e99e35b49624f225bf45a96fc00363f60fd325be384cf27e024d4df07734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBackupDrBackupPlanBackupRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2f9123706c31f0a4f2000aba087c2d0edabc9675b39eb82e48c85ed46166706)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStandardSchedule")
    def put_standard_schedule(
        self,
        *,
        recurrence_type: builtins.str,
        time_zone: builtins.str,
        backup_window: typing.Optional[typing.Union["GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hourly_frequency: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        week_day_of_month: typing.Optional[typing.Union["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: RecurrenceType enumerates the applicable periodicity for the schedule. Possible values: ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#recurrence_type GoogleBackupDrBackupPlan#recurrence_type}
        :param time_zone: The time zone to be used when interpreting the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#time_zone GoogleBackupDrBackupPlan#time_zone}
        :param backup_window: backup_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_window GoogleBackupDrBackupPlan#backup_window}
        :param days_of_month: Specifies days of months like 1, 5, or 14 on which jobs will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_month GoogleBackupDrBackupPlan#days_of_month}
        :param days_of_week: Specifies days of week like MONDAY or TUESDAY, on which jobs will run. This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_week GoogleBackupDrBackupPlan#days_of_week}
        :param hourly_frequency: Specifies frequency for hourly backups. An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined. This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#hourly_frequency GoogleBackupDrBackupPlan#hourly_frequency}
        :param months: Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#months GoogleBackupDrBackupPlan#months}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_day_of_month GoogleBackupDrBackupPlan#week_day_of_month}
        '''
        value = GoogleBackupDrBackupPlanBackupRulesStandardSchedule(
            recurrence_type=recurrence_type,
            time_zone=time_zone,
            backup_window=backup_window,
            days_of_month=days_of_month,
            days_of_week=days_of_week,
            hourly_frequency=hourly_frequency,
            months=months,
            week_day_of_month=week_day_of_month,
        )

        return typing.cast(None, jsii.invoke(self, "putStandardSchedule", [value]))

    @builtins.property
    @jsii.member(jsii_name="standardSchedule")
    def standard_schedule(
        self,
    ) -> "GoogleBackupDrBackupPlanBackupRulesStandardScheduleOutputReference":
        return typing.cast("GoogleBackupDrBackupPlanBackupRulesStandardScheduleOutputReference", jsii.get(self, "standardSchedule"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDaysInput")
    def backup_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="standardScheduleInput")
    def standard_schedule_input(
        self,
    ) -> typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardSchedule"]:
        return typing.cast(typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardSchedule"], jsii.get(self, "standardScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDays")
    def backup_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionDays"))

    @backup_retention_days.setter
    def backup_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07c4d3de0c4108a84436c7a2a525c425a647e6867547b51e4c363a7250a0f27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca81e34b85b56cca9a7c231233a6a41b9da85dd565b4d78377574f26d66ed5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanBackupRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanBackupRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanBackupRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ff2b175765b71d7abdb95e81ef4ec7352c19af5efe5b0ba19f43212be67678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "recurrence_type": "recurrenceType",
        "time_zone": "timeZone",
        "backup_window": "backupWindow",
        "days_of_month": "daysOfMonth",
        "days_of_week": "daysOfWeek",
        "hourly_frequency": "hourlyFrequency",
        "months": "months",
        "week_day_of_month": "weekDayOfMonth",
    },
)
class GoogleBackupDrBackupPlanBackupRulesStandardSchedule:
    def __init__(
        self,
        *,
        recurrence_type: builtins.str,
        time_zone: builtins.str,
        backup_window: typing.Optional[typing.Union["GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hourly_frequency: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        week_day_of_month: typing.Optional[typing.Union["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: RecurrenceType enumerates the applicable periodicity for the schedule. Possible values: ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#recurrence_type GoogleBackupDrBackupPlan#recurrence_type}
        :param time_zone: The time zone to be used when interpreting the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#time_zone GoogleBackupDrBackupPlan#time_zone}
        :param backup_window: backup_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_window GoogleBackupDrBackupPlan#backup_window}
        :param days_of_month: Specifies days of months like 1, 5, or 14 on which jobs will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_month GoogleBackupDrBackupPlan#days_of_month}
        :param days_of_week: Specifies days of week like MONDAY or TUESDAY, on which jobs will run. This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_week GoogleBackupDrBackupPlan#days_of_week}
        :param hourly_frequency: Specifies frequency for hourly backups. An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined. This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#hourly_frequency GoogleBackupDrBackupPlan#hourly_frequency}
        :param months: Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#months GoogleBackupDrBackupPlan#months}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_day_of_month GoogleBackupDrBackupPlan#week_day_of_month}
        '''
        if isinstance(backup_window, dict):
            backup_window = GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(**backup_window)
        if isinstance(week_day_of_month, dict):
            week_day_of_month = GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(**week_day_of_month)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adb35b48928da35c26e3c0a5d69a967ca192402cde074adee15e00d6de5fcf4)
            check_type(argname="argument recurrence_type", value=recurrence_type, expected_type=type_hints["recurrence_type"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument backup_window", value=backup_window, expected_type=type_hints["backup_window"])
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument hourly_frequency", value=hourly_frequency, expected_type=type_hints["hourly_frequency"])
            check_type(argname="argument months", value=months, expected_type=type_hints["months"])
            check_type(argname="argument week_day_of_month", value=week_day_of_month, expected_type=type_hints["week_day_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recurrence_type": recurrence_type,
            "time_zone": time_zone,
        }
        if backup_window is not None:
            self._values["backup_window"] = backup_window
        if days_of_month is not None:
            self._values["days_of_month"] = days_of_month
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if hourly_frequency is not None:
            self._values["hourly_frequency"] = hourly_frequency
        if months is not None:
            self._values["months"] = months
        if week_day_of_month is not None:
            self._values["week_day_of_month"] = week_day_of_month

    @builtins.property
    def recurrence_type(self) -> builtins.str:
        '''RecurrenceType enumerates the applicable periodicity for the schedule. Possible values: ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#recurrence_type GoogleBackupDrBackupPlan#recurrence_type}
        '''
        result = self._values.get("recurrence_type")
        assert result is not None, "Required property 'recurrence_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone to be used when interpreting the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#time_zone GoogleBackupDrBackupPlan#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_window(
        self,
    ) -> typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow"]:
        '''backup_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_window GoogleBackupDrBackupPlan#backup_window}
        '''
        result = self._values.get("backup_window")
        return typing.cast(typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow"], result)

    @builtins.property
    def days_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Specifies days of months like 1, 5, or 14 on which jobs will run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_month GoogleBackupDrBackupPlan#days_of_month}
        '''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies days of week like MONDAY or TUESDAY, on which jobs will run.

        This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#days_of_week GoogleBackupDrBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hourly_frequency(self) -> typing.Optional[jsii.Number]:
        '''Specifies frequency for hourly backups.

        An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined.
        This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#hourly_frequency GoogleBackupDrBackupPlan#hourly_frequency}
        '''
        result = self._values.get("hourly_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def months(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#months GoogleBackupDrBackupPlan#months}
        '''
        result = self._values.get("months")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def week_day_of_month(
        self,
    ) -> typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"]:
        '''week_day_of_month block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_day_of_month GoogleBackupDrBackupPlan#week_day_of_month}
        '''
        result = self._values.get("week_day_of_month")
        return typing.cast(typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanBackupRulesStandardSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow",
    jsii_struct_bases=[],
    name_mapping={
        "start_hour_of_day": "startHourOfDay",
        "end_hour_of_day": "endHourOfDay",
    },
)
class GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow:
    def __init__(
        self,
        *,
        start_hour_of_day: jsii.Number,
        end_hour_of_day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_hour_of_day: The hour of the day (0-23) when the window starts, for example, if the value of the start hour of the day is 6, that means the backup window starts at 6:00. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#start_hour_of_day GoogleBackupDrBackupPlan#start_hour_of_day}
        :param end_hour_of_day: The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00. The end hour of the day should be greater than the start Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#end_hour_of_day GoogleBackupDrBackupPlan#end_hour_of_day}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d085f515f20a6b5d1c20666160c6f33e0b55862ac1dd35f020ae21a659df639b)
            check_type(argname="argument start_hour_of_day", value=start_hour_of_day, expected_type=type_hints["start_hour_of_day"])
            check_type(argname="argument end_hour_of_day", value=end_hour_of_day, expected_type=type_hints["end_hour_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "start_hour_of_day": start_hour_of_day,
        }
        if end_hour_of_day is not None:
            self._values["end_hour_of_day"] = end_hour_of_day

    @builtins.property
    def start_hour_of_day(self) -> jsii.Number:
        '''The hour of the day (0-23) when the window starts, for example, if the value of the start hour of the day is 6, that means the backup window starts at 6:00.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#start_hour_of_day GoogleBackupDrBackupPlan#start_hour_of_day}
        '''
        result = self._values.get("start_hour_of_day")
        assert result is not None, "Required property 'start_hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_hour_of_day(self) -> typing.Optional[jsii.Number]:
        '''The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00.

        The end hour of the day should be greater than the start

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#end_hour_of_day GoogleBackupDrBackupPlan#end_hour_of_day}
        '''
        result = self._values.get("end_hour_of_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5e33a8733c4b280e8eebfdea4076190e563813155e5b9a94474a4b8885a073a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndHourOfDay")
    def reset_end_hour_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndHourOfDay", []))

    @builtins.property
    @jsii.member(jsii_name="endHourOfDayInput")
    def end_hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endHourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="startHourOfDayInput")
    def start_hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startHourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="endHourOfDay")
    def end_hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endHourOfDay"))

    @end_hour_of_day.setter
    def end_hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a93f584fd2e466d7b023afeae017d5f360211012c6a534c69e81cce21bd596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endHourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startHourOfDay")
    def start_hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHourOfDay"))

    @start_hour_of_day.setter
    def start_hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c91b82b6d11fd218713a40775e6848e5882ad2c59a6117d013a8afd35b72d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow]:
        return typing.cast(typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ff16e24d105a9ce6c2808fd10cb92f3840e3080daa08cd2c4412024d7582c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBackupDrBackupPlanBackupRulesStandardScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb8d327a7f83f9c915de45b21d1bd8c3a7ffe2fd5261eeb2cc54ba68a206b089)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackupWindow")
    def put_backup_window(
        self,
        *,
        start_hour_of_day: jsii.Number,
        end_hour_of_day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_hour_of_day: The hour of the day (0-23) when the window starts, for example, if the value of the start hour of the day is 6, that means the backup window starts at 6:00. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#start_hour_of_day GoogleBackupDrBackupPlan#start_hour_of_day}
        :param end_hour_of_day: The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00. The end hour of the day should be greater than the start Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#end_hour_of_day GoogleBackupDrBackupPlan#end_hour_of_day}
        '''
        value = GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(
            start_hour_of_day=start_hour_of_day, end_hour_of_day=end_hour_of_day
        )

        return typing.cast(None, jsii.invoke(self, "putBackupWindow", [value]))

    @jsii.member(jsii_name="putWeekDayOfMonth")
    def put_week_day_of_month(
        self,
        *,
        day_of_week: builtins.str,
        week_of_month: builtins.str,
    ) -> None:
        '''
        :param day_of_week: Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#day_of_week GoogleBackupDrBackupPlan#day_of_week}
        :param week_of_month: WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_of_month GoogleBackupDrBackupPlan#week_of_month}
        '''
        value = GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(
            day_of_week=day_of_week, week_of_month=week_of_month
        )

        return typing.cast(None, jsii.invoke(self, "putWeekDayOfMonth", [value]))

    @jsii.member(jsii_name="resetBackupWindow")
    def reset_backup_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupWindow", []))

    @jsii.member(jsii_name="resetDaysOfMonth")
    def reset_days_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfMonth", []))

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetHourlyFrequency")
    def reset_hourly_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourlyFrequency", []))

    @jsii.member(jsii_name="resetMonths")
    def reset_months(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonths", []))

    @jsii.member(jsii_name="resetWeekDayOfMonth")
    def reset_week_day_of_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekDayOfMonth", []))

    @builtins.property
    @jsii.member(jsii_name="backupWindow")
    def backup_window(
        self,
    ) -> GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference:
        return typing.cast(GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference, jsii.get(self, "backupWindow"))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonth")
    def week_day_of_month(
        self,
    ) -> "GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference":
        return typing.cast("GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference", jsii.get(self, "weekDayOfMonth"))

    @builtins.property
    @jsii.member(jsii_name="backupWindowInput")
    def backup_window_input(
        self,
    ) -> typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow]:
        return typing.cast(typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow], jsii.get(self, "backupWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="hourlyFrequencyInput")
    def hourly_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourlyFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="monthsInput")
    def months_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "monthsInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceTypeInput")
    def recurrence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonthInput")
    def week_day_of_month_input(
        self,
    ) -> typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"]:
        return typing.cast(typing.Optional["GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"], jsii.get(self, "weekDayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab4d898ce15c8e640b12dee6022eba49befd5d6388f939579ec3b10895eb44c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a26ec9cc418c759c457ba67710e98a2b94881f972c749d72648a7a81ac1e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourlyFrequency")
    def hourly_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourlyFrequency"))

    @hourly_frequency.setter
    def hourly_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6965a8a35fa7369dd604743d4e2dd6e5376111ff5db78e2b638091ae256167b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourlyFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580d3e2ac0800a3c04f0e5699a14e8989a8dfd41932465dcce75dcd29a0228a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b37a3a549294c9d67aee2de66349738685724014e25e0d6851ca89e493966f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77757260316dbd1bbcc538af49e54c23464086ae08f1b6dd2d5ae4c9d6220aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardSchedule]:
        return typing.cast(typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af85fab69b976967d0aa32803947b2333e1963efa80df5f39a404a990d69c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "week_of_month": "weekOfMonth"},
)
class GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        week_of_month: builtins.str,
    ) -> None:
        '''
        :param day_of_week: Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#day_of_week GoogleBackupDrBackupPlan#day_of_week}
        :param week_of_month: WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_of_month GoogleBackupDrBackupPlan#week_of_month}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02107dc3b989a63e3d7cf9254aef7a6df900f6f96e84e7a36ca4cbd3358ac382)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument week_of_month", value=week_of_month, expected_type=type_hints["week_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "week_of_month": week_of_month,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#day_of_week GoogleBackupDrBackupPlan#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_of_month(self) -> builtins.str:
        '''WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#week_of_month GoogleBackupDrBackupPlan#week_of_month}
        '''
        result = self._values.get("week_of_month")
        assert result is not None, "Required property 'week_of_month' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1a71daf93cd7a13420fba2b53171193806aaae25667080c25df985812dde8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="weekOfMonthInput")
    def week_of_month_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weekOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d864d3c7567d99933521aadedd31b10c2b0c11337bedfefa24cd62f598c5cab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfMonth")
    def week_of_month(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weekOfMonth"))

    @week_of_month.setter
    def week_of_month(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01f9c40e43527e9a58542bcc4648ca9db69a5972acb5270926334cdeaabb0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth]:
        return typing.cast(typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce2d00e11382618b030c7a98d2f432930d3a171dc728935686446f79a81074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "backup_plan_id": "backupPlanId",
        "backup_rules": "backupRules",
        "backup_vault": "backupVault",
        "location": "location",
        "resource_type": "resourceType",
        "description": "description",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleBackupDrBackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_plan_id: builtins.str,
        backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
        backup_vault: builtins.str,
        location: builtins.str,
        resource_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBackupDrBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_plan_id: The ID of the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_plan_id GoogleBackupDrBackupPlan#backup_plan_id}
        :param backup_rules: backup_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_rules GoogleBackupDrBackupPlan#backup_rules}
        :param backup_vault: Backup vault where the backups gets stored using this Backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_vault GoogleBackupDrBackupPlan#backup_vault}
        :param location: The location for the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#location GoogleBackupDrBackupPlan#location}
        :param resource_type: The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance" and "storage.googleapis.com/Bucket". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#resource_type GoogleBackupDrBackupPlan#resource_type}
        :param description: The description allows for additional details about 'BackupPlan' and its use cases to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#description GoogleBackupDrBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#id GoogleBackupDrBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#project GoogleBackupDrBackupPlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#timeouts GoogleBackupDrBackupPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleBackupDrBackupPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a3ea94f9ab4615d5c5667d8d98ca5d58a12261520a9a6a335f669be3fd277f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument backup_plan_id", value=backup_plan_id, expected_type=type_hints["backup_plan_id"])
            check_type(argname="argument backup_rules", value=backup_rules, expected_type=type_hints["backup_rules"])
            check_type(argname="argument backup_vault", value=backup_vault, expected_type=type_hints["backup_vault"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_plan_id": backup_plan_id,
            "backup_rules": backup_rules,
            "backup_vault": backup_vault,
            "location": location,
            "resource_type": resource_type,
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
    def backup_plan_id(self) -> builtins.str:
        '''The ID of the backup plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_plan_id GoogleBackupDrBackupPlan#backup_plan_id}
        '''
        result = self._values.get("backup_plan_id")
        assert result is not None, "Required property 'backup_plan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]]:
        '''backup_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_rules GoogleBackupDrBackupPlan#backup_rules}
        '''
        result = self._values.get("backup_rules")
        assert result is not None, "Required property 'backup_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]], result)

    @builtins.property
    def backup_vault(self) -> builtins.str:
        '''Backup vault where the backups gets stored using this Backup plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#backup_vault GoogleBackupDrBackupPlan#backup_vault}
        '''
        result = self._values.get("backup_vault")
        assert result is not None, "Required property 'backup_vault' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the backup plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#location GoogleBackupDrBackupPlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance" and "storage.googleapis.com/Bucket".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#resource_type GoogleBackupDrBackupPlan#resource_type}
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description allows for additional details about 'BackupPlan' and its use cases to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#description GoogleBackupDrBackupPlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#id GoogleBackupDrBackupPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#project GoogleBackupDrBackupPlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBackupDrBackupPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#timeouts GoogleBackupDrBackupPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBackupDrBackupPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleBackupDrBackupPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#create GoogleBackupDrBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#delete GoogleBackupDrBackupPlan#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3829bb237160f37c1d9e073f5ccee04c1c1f1767571d3382423e524d68dd7a8d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#create GoogleBackupDrBackupPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_backup_dr_backup_plan#delete GoogleBackupDrBackupPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBackupDrBackupPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBackupDrBackupPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBackupDrBackupPlan.GoogleBackupDrBackupPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ffe5edf32f7e5b38c480a50bf926dae1a2a4a279710d859edacef1631cd92fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5359b80d801631cdd0f3bd25dbede04dc66492d6d8e77960bc9fd3cba4d284fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f1f7396a52bb1df35cceab3793e18ded944cc325d786da4d121e94fb072d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc3fce59b55bd9f17e1a67bc55c35cdce1fa8702adf87adb9877ad0bdac38f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBackupDrBackupPlan",
    "GoogleBackupDrBackupPlanBackupRules",
    "GoogleBackupDrBackupPlanBackupRulesList",
    "GoogleBackupDrBackupPlanBackupRulesOutputReference",
    "GoogleBackupDrBackupPlanBackupRulesStandardSchedule",
    "GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow",
    "GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference",
    "GoogleBackupDrBackupPlanBackupRulesStandardScheduleOutputReference",
    "GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth",
    "GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference",
    "GoogleBackupDrBackupPlanConfig",
    "GoogleBackupDrBackupPlanTimeouts",
    "GoogleBackupDrBackupPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d894deb8d452c8c80fb073fde09ec9e5fbdc926253a4b9a24332dce3ff00fec8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_plan_id: builtins.str,
    backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
    backup_vault: builtins.str,
    location: builtins.str,
    resource_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBackupDrBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3ca1102b8c4b760b8108f77f12bb86faaf415a465dcafb8094ac882606ca94a5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4e68f05f2c53afae924b07a47e4c2fee57fdf0494f961e4f7f2708f248b751(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfad1805bdb2463861a4b41d08c5c52a5feb851f1cf355c78f6eace623beef3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cc9983d75f8f8aa25797abb9509ea7254335a9fc45e852244b719240e37206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f4ec8137764258869fbb6557de7a0a660ad1746d74ad332e28951eda130bda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdb377c54bb31ea9f9a44fda59e9669836d87d85c15ed2c6d0356cae67e77c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e88fee3852a9e757715cee396187bd01a8ca4df14fb69d46e585f25258e992c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbbd6d1951f0e5c4daea358a391d42e9181a76f4b86fea103f3301ba3fdd5be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77231b5ff947ac00d4415abb9ae94d1b832c29cf5ba7141783512db3d3be5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3081e9b3c9245c6a2adc59518801a8f11d6869d985c7bc984ff667e7dc4aeb(
    *,
    backup_retention_days: jsii.Number,
    rule_id: builtins.str,
    standard_schedule: typing.Union[GoogleBackupDrBackupPlanBackupRulesStandardSchedule, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d53f18ad78e06ffcde8c8bc74350b0f3a5d5ea63ae0fc2cc37eb282b796bfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2610b4c671e0cf4217277a2a821d651532c6c28cba1821252dea80644b7402e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82c0bf83ba82f5cdca0f64a3a417951ea8298107f133781a8cbc45dcbec6e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f715ba280b81af34840dde6d48e8aa3433368b9aa26c27aeb370b20415ff3e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7546aa0a9b20a1d74f5270fba066231d6f2a5f31b0f0cc99b63edc4bd47a9d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da12e99e35b49624f225bf45a96fc00363f60fd325be384cf27e024d4df07734(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBackupDrBackupPlanBackupRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f9123706c31f0a4f2000aba087c2d0edabc9675b39eb82e48c85ed46166706(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07c4d3de0c4108a84436c7a2a525c425a647e6867547b51e4c363a7250a0f27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca81e34b85b56cca9a7c231233a6a41b9da85dd565b4d78377574f26d66ed5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ff2b175765b71d7abdb95e81ef4ec7352c19af5efe5b0ba19f43212be67678(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanBackupRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adb35b48928da35c26e3c0a5d69a967ca192402cde074adee15e00d6de5fcf4(
    *,
    recurrence_type: builtins.str,
    time_zone: builtins.str,
    backup_window: typing.Optional[typing.Union[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    hourly_frequency: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Sequence[builtins.str]] = None,
    week_day_of_month: typing.Optional[typing.Union[GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d085f515f20a6b5d1c20666160c6f33e0b55862ac1dd35f020ae21a659df639b(
    *,
    start_hour_of_day: jsii.Number,
    end_hour_of_day: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e33a8733c4b280e8eebfdea4076190e563813155e5b9a94474a4b8885a073a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a93f584fd2e466d7b023afeae017d5f360211012c6a534c69e81cce21bd596(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c91b82b6d11fd218713a40775e6848e5882ad2c59a6117d013a8afd35b72d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ff16e24d105a9ce6c2808fd10cb92f3840e3080daa08cd2c4412024d7582c2(
    value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleBackupWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8d327a7f83f9c915de45b21d1bd8c3a7ffe2fd5261eeb2cc54ba68a206b089(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab4d898ce15c8e640b12dee6022eba49befd5d6388f939579ec3b10895eb44c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a26ec9cc418c759c457ba67710e98a2b94881f972c749d72648a7a81ac1e95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6965a8a35fa7369dd604743d4e2dd6e5376111ff5db78e2b638091ae256167b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580d3e2ac0800a3c04f0e5699a14e8989a8dfd41932465dcce75dcd29a0228a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b37a3a549294c9d67aee2de66349738685724014e25e0d6851ca89e493966f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77757260316dbd1bbcc538af49e54c23464086ae08f1b6dd2d5ae4c9d6220aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af85fab69b976967d0aa32803947b2333e1963efa80df5f39a404a990d69c21(
    value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02107dc3b989a63e3d7cf9254aef7a6df900f6f96e84e7a36ca4cbd3358ac382(
    *,
    day_of_week: builtins.str,
    week_of_month: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1a71daf93cd7a13420fba2b53171193806aaae25667080c25df985812dde8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d864d3c7567d99933521aadedd31b10c2b0c11337bedfefa24cd62f598c5cab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01f9c40e43527e9a58542bcc4648ca9db69a5972acb5270926334cdeaabb0f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce2d00e11382618b030c7a98d2f432930d3a171dc728935686446f79a81074(
    value: typing.Optional[GoogleBackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a3ea94f9ab4615d5c5667d8d98ca5d58a12261520a9a6a335f669be3fd277f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_plan_id: builtins.str,
    backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
    backup_vault: builtins.str,
    location: builtins.str,
    resource_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBackupDrBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3829bb237160f37c1d9e073f5ccee04c1c1f1767571d3382423e524d68dd7a8d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffe5edf32f7e5b38c480a50bf926dae1a2a4a279710d859edacef1631cd92fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5359b80d801631cdd0f3bd25dbede04dc66492d6d8e77960bc9fd3cba4d284fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f1f7396a52bb1df35cceab3793e18ded944cc325d786da4d121e94fb072d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc3fce59b55bd9f17e1a67bc55c35cdce1fa8702adf87adb9877ad0bdac38f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBackupDrBackupPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

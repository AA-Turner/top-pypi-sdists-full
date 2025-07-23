r'''
# `google_backup_dr_backup_plan`

Refer to the Terraform Registry for docs: [`google_backup_dr_backup_plan`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan).
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


class BackupDrBackupPlan(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlan",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan google_backup_dr_backup_plan}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        backup_plan_id: builtins.str,
        backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupDrBackupPlanBackupRules", typing.Dict[builtins.str, typing.Any]]]],
        backup_vault: builtins.str,
        location: builtins.str,
        resource_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BackupDrBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan google_backup_dr_backup_plan} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param backup_plan_id: The ID of the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_plan_id BackupDrBackupPlan#backup_plan_id}
        :param backup_rules: backup_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_rules BackupDrBackupPlan#backup_rules}
        :param backup_vault: Backup vault where the backups gets stored using this Backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_vault BackupDrBackupPlan#backup_vault}
        :param location: The location for the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#location BackupDrBackupPlan#location}
        :param resource_type: The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance", "compute.googleapis.com/Disk", and "storage.googleapis.com/Bucket". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#resource_type BackupDrBackupPlan#resource_type}
        :param description: The description allows for additional details about 'BackupPlan' and its use cases to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#description BackupDrBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#id BackupDrBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#project BackupDrBackupPlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#timeouts BackupDrBackupPlan#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8aefd0c070dbf07b92051d68cd409a8fada1ad1c96510844006a5d03493f4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BackupDrBackupPlanConfig(
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
        '''Generates CDKTF code for importing a BackupDrBackupPlan resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BackupDrBackupPlan to import.
        :param import_from_id: The id of the existing BackupDrBackupPlan that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BackupDrBackupPlan to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3543a17107e6ac26e5cbf9929a888faa67c419a09e3e0551019c1e38f0b2b67)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackupRules")
    def put_backup_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BackupDrBackupPlanBackupRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2bcbfc02b5a74f78d36cbf974a0dc4d5f8c9c325fe63041500f559bdd197ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBackupRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#create BackupDrBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#delete BackupDrBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#update BackupDrBackupPlan#update}.
        '''
        value = BackupDrBackupPlanTimeouts(create=create, delete=delete, update=update)

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
    def backup_rules(self) -> "BackupDrBackupPlanBackupRulesList":
        return typing.cast("BackupDrBackupPlanBackupRulesList", jsii.get(self, "backupRules"))

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
    def timeouts(self) -> "BackupDrBackupPlanTimeoutsOutputReference":
        return typing.cast("BackupDrBackupPlanTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupDrBackupPlanBackupRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BackupDrBackupPlanBackupRules"]]], jsii.get(self, "backupRulesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupDrBackupPlanTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BackupDrBackupPlanTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))

    @backup_plan_id.setter
    def backup_plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2f8263d575106cb6c5e9f8d6b94693814de1d75faf0c94069da148aaf3a6db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupPlanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backupVault"))

    @backup_vault.setter
    def backup_vault(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e85441cd7dc0cd058b286854672fe4a0352ee93b3632bb52ae023ec8b95881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupVault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c399d92617a35c6fb8df9f7b2f05cf4fb9cb2673ce8af15dac0ed93b9ad48c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29dd42ac80810f31645c5973a19935f193a3d5b23b0078738818c8308f96f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09619401f14e8d2b8457534c33b2ae3554bd7e9aacc3c34df8cf84da4033b1fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6fd6df75d70b056b5940c91be0f09788aff6b8c1128dae010f3a3ccca46156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c791a524ee0b5002090c0af9a7899bba213538ef28e8cb28f53747c03dc296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRules",
    jsii_struct_bases=[],
    name_mapping={
        "backup_retention_days": "backupRetentionDays",
        "rule_id": "ruleId",
        "standard_schedule": "standardSchedule",
    },
)
class BackupDrBackupPlanBackupRules:
    def __init__(
        self,
        *,
        backup_retention_days: jsii.Number,
        rule_id: builtins.str,
        standard_schedule: typing.Union["BackupDrBackupPlanBackupRulesStandardSchedule", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param backup_retention_days: Configures the duration for which backup data will be kept. The value should be greater than or equal to minimum enforced retention of the backup vault. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_retention_days BackupDrBackupPlan#backup_retention_days}
        :param rule_id: The unique ID of this 'BackupRule'. The 'rule_id' is unique per 'BackupPlan'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#rule_id BackupDrBackupPlan#rule_id}
        :param standard_schedule: standard_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#standard_schedule BackupDrBackupPlan#standard_schedule}
        '''
        if isinstance(standard_schedule, dict):
            standard_schedule = BackupDrBackupPlanBackupRulesStandardSchedule(**standard_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7f0155692fd8cbd2326117ec828cce889f1a8144df5c61dcd21d7f9522caa2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_retention_days BackupDrBackupPlan#backup_retention_days}
        '''
        result = self._values.get("backup_retention_days")
        assert result is not None, "Required property 'backup_retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_id(self) -> builtins.str:
        '''The unique ID of this 'BackupRule'. The 'rule_id' is unique per 'BackupPlan'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#rule_id BackupDrBackupPlan#rule_id}
        '''
        result = self._values.get("rule_id")
        assert result is not None, "Required property 'rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standard_schedule(self) -> "BackupDrBackupPlanBackupRulesStandardSchedule":
        '''standard_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#standard_schedule BackupDrBackupPlan#standard_schedule}
        '''
        result = self._values.get("standard_schedule")
        assert result is not None, "Required property 'standard_schedule' is missing"
        return typing.cast("BackupDrBackupPlanBackupRulesStandardSchedule", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanBackupRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupDrBackupPlanBackupRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0b2d68a7f4a988353c1e53fbd791d0bdc7a9edcba3106216fcc901a501fb7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BackupDrBackupPlanBackupRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05e704dc4c5e883d31447ea9f6a773d51b277b5a025893df8c349755eae02e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BackupDrBackupPlanBackupRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6339a8f850558f5c30d34d3e57d736b7f1ca0668aca63db0de6ca27dba2d2574)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de5b1c50e87936f66e87a414fd57ae14711663af1581f8c87ff825f19374278c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3a0029a929c0a7426dd7df364e09c0a9b186031e15a68edc48ed49ab07fc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38aa8077f4481d33dea3cd9e2ab8f8711b45258523ec884e4a8b63885941bfc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupDrBackupPlanBackupRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f508cdd17beeb76082262785427b05faed048dc8c84cd9ee25327414ced4fa70)
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
        backup_window: typing.Optional[typing.Union["BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hourly_frequency: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        week_day_of_month: typing.Optional[typing.Union["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: RecurrenceType enumerates the applicable periodicity for the schedule. Possible values: ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#recurrence_type BackupDrBackupPlan#recurrence_type}
        :param time_zone: The time zone to be used when interpreting the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#time_zone BackupDrBackupPlan#time_zone}
        :param backup_window: backup_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_window BackupDrBackupPlan#backup_window}
        :param days_of_month: Specifies days of months like 1, 5, or 14 on which jobs will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_month BackupDrBackupPlan#days_of_month}
        :param days_of_week: Specifies days of week like MONDAY or TUESDAY, on which jobs will run. This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_week BackupDrBackupPlan#days_of_week}
        :param hourly_frequency: Specifies frequency for hourly backups. An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined. This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#hourly_frequency BackupDrBackupPlan#hourly_frequency}
        :param months: Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#months BackupDrBackupPlan#months}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_day_of_month BackupDrBackupPlan#week_day_of_month}
        '''
        value = BackupDrBackupPlanBackupRulesStandardSchedule(
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
    ) -> "BackupDrBackupPlanBackupRulesStandardScheduleOutputReference":
        return typing.cast("BackupDrBackupPlanBackupRulesStandardScheduleOutputReference", jsii.get(self, "standardSchedule"))

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
    ) -> typing.Optional["BackupDrBackupPlanBackupRulesStandardSchedule"]:
        return typing.cast(typing.Optional["BackupDrBackupPlanBackupRulesStandardSchedule"], jsii.get(self, "standardScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDays")
    def backup_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionDays"))

    @backup_retention_days.setter
    def backup_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782596732df6a889eb578ed35017cc042a506036c9438c195c705bb4839c60fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be44cbe31435d263731aeeb1ceeb292a7847e847055c1dd4f35e02ce1dab146d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanBackupRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanBackupRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanBackupRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd8e5e138d09582c440c3e64a8a015236802b8e66132cfce2abed6522aa2ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardSchedule",
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
class BackupDrBackupPlanBackupRulesStandardSchedule:
    def __init__(
        self,
        *,
        recurrence_type: builtins.str,
        time_zone: builtins.str,
        backup_window: typing.Optional[typing.Union["BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
        hourly_frequency: typing.Optional[jsii.Number] = None,
        months: typing.Optional[typing.Sequence[builtins.str]] = None,
        week_day_of_month: typing.Optional[typing.Union["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: RecurrenceType enumerates the applicable periodicity for the schedule. Possible values: ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#recurrence_type BackupDrBackupPlan#recurrence_type}
        :param time_zone: The time zone to be used when interpreting the schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#time_zone BackupDrBackupPlan#time_zone}
        :param backup_window: backup_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_window BackupDrBackupPlan#backup_window}
        :param days_of_month: Specifies days of months like 1, 5, or 14 on which jobs will run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_month BackupDrBackupPlan#days_of_month}
        :param days_of_week: Specifies days of week like MONDAY or TUESDAY, on which jobs will run. This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_week BackupDrBackupPlan#days_of_week}
        :param hourly_frequency: Specifies frequency for hourly backups. An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined. This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#hourly_frequency BackupDrBackupPlan#hourly_frequency}
        :param months: Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#months BackupDrBackupPlan#months}
        :param week_day_of_month: week_day_of_month block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_day_of_month BackupDrBackupPlan#week_day_of_month}
        '''
        if isinstance(backup_window, dict):
            backup_window = BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(**backup_window)
        if isinstance(week_day_of_month, dict):
            week_day_of_month = BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(**week_day_of_month)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f6cb1fe5b0ae96243d6eaf952bb5cb2726930185f50e307e014d3ec20a60b5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#recurrence_type BackupDrBackupPlan#recurrence_type}
        '''
        result = self._values.get("recurrence_type")
        assert result is not None, "Required property 'recurrence_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone to be used when interpreting the schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#time_zone BackupDrBackupPlan#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_window(
        self,
    ) -> typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow"]:
        '''backup_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_window BackupDrBackupPlan#backup_window}
        '''
        result = self._values.get("backup_window")
        return typing.cast(typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow"], result)

    @builtins.property
    def days_of_month(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Specifies days of months like 1, 5, or 14 on which jobs will run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_month BackupDrBackupPlan#days_of_month}
        '''
        result = self._values.get("days_of_month")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies days of week like MONDAY or TUESDAY, on which jobs will run.

        This is required for 'recurrence_type', 'WEEKLY' and is not applicable otherwise. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#days_of_week BackupDrBackupPlan#days_of_week}
        '''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hourly_frequency(self) -> typing.Optional[jsii.Number]:
        '''Specifies frequency for hourly backups.

        An hourly frequency of 2 means jobs will run every 2 hours from start time till end time defined.
        This is required for 'recurrence_type', 'HOURLY' and is not applicable otherwise.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#hourly_frequency BackupDrBackupPlan#hourly_frequency}
        '''
        result = self._values.get("hourly_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def months(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies values of months Possible values: ["MONTH_UNSPECIFIED", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#months BackupDrBackupPlan#months}
        '''
        result = self._values.get("months")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def week_day_of_month(
        self,
    ) -> typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"]:
        '''week_day_of_month block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_day_of_month BackupDrBackupPlan#week_day_of_month}
        '''
        result = self._values.get("week_day_of_month")
        return typing.cast(typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanBackupRulesStandardSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow",
    jsii_struct_bases=[],
    name_mapping={
        "start_hour_of_day": "startHourOfDay",
        "end_hour_of_day": "endHourOfDay",
    },
)
class BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow:
    def __init__(
        self,
        *,
        start_hour_of_day: jsii.Number,
        end_hour_of_day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_hour_of_day: The hour of the day (0-23) when the window starts, for example, if the value of the start hour of the day is 6, that means the backup window starts at 6:00. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#start_hour_of_day BackupDrBackupPlan#start_hour_of_day}
        :param end_hour_of_day: The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00. The end hour of the day should be greater than the start Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#end_hour_of_day BackupDrBackupPlan#end_hour_of_day}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd15ec2f4e67d14b6742a7b07a63248c9e5d7dd08e34fedd36414f3b4cf6d83b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#start_hour_of_day BackupDrBackupPlan#start_hour_of_day}
        '''
        result = self._values.get("start_hour_of_day")
        assert result is not None, "Required property 'start_hour_of_day' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_hour_of_day(self) -> typing.Optional[jsii.Number]:
        '''The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00.

        The end hour of the day should be greater than the start

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#end_hour_of_day BackupDrBackupPlan#end_hour_of_day}
        '''
        result = self._values.get("end_hour_of_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__392ec604943ebe8da995af45f2f2d61c0ac47fc0f1dd76a73295d1a3bb2504a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb1485773937d9f21adcfb36aaf3c23827039d8972746d52f9792e78d711cdfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endHourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startHourOfDay")
    def start_hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHourOfDay"))

    @start_hour_of_day.setter
    def start_hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3646cca28a72f0b5bf353a9241ef34b9b774c4df212d26837cc510ae6a2d7b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow]:
        return typing.cast(typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd38597f141ed812f9b577f24c39f7148627a66a04c2e94440177def340ac355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BackupDrBackupPlanBackupRulesStandardScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d012866cdc547e52bb19c64d9682866b7bab62a75a2af3d2df3c3d3fd17bec4)
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
        :param start_hour_of_day: The hour of the day (0-23) when the window starts, for example, if the value of the start hour of the day is 6, that means the backup window starts at 6:00. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#start_hour_of_day BackupDrBackupPlan#start_hour_of_day}
        :param end_hour_of_day: The hour of the day (1-24) when the window ends, for example, if the value of end hour of the day is 10, that means the backup window end time is 10:00. The end hour of the day should be greater than the start Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#end_hour_of_day BackupDrBackupPlan#end_hour_of_day}
        '''
        value = BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow(
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
        :param day_of_week: Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#day_of_week BackupDrBackupPlan#day_of_week}
        :param week_of_month: WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_of_month BackupDrBackupPlan#week_of_month}
        '''
        value = BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(
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
    ) -> BackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference:
        return typing.cast(BackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference, jsii.get(self, "backupWindow"))

    @builtins.property
    @jsii.member(jsii_name="weekDayOfMonth")
    def week_day_of_month(
        self,
    ) -> "BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference":
        return typing.cast("BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference", jsii.get(self, "weekDayOfMonth"))

    @builtins.property
    @jsii.member(jsii_name="backupWindowInput")
    def backup_window_input(
        self,
    ) -> typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow]:
        return typing.cast(typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow], jsii.get(self, "backupWindowInput"))

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
    ) -> typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"]:
        return typing.cast(typing.Optional["BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth"], jsii.get(self, "weekDayOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af1c2ef6e5a75d30d95de05845c9695c260c3e5295f6f2fb37b6ba57c4a2d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c932f76ac75e7567dfa4eb7beb4e1f5c13a3019bb7dd38ae9429e1fd20366a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourlyFrequency")
    def hourly_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourlyFrequency"))

    @hourly_frequency.setter
    def hourly_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4f426e546725410f9d6de33a7e5c9388c51d4c36a6a43234d42d416ced3f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourlyFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @months.setter
    def months(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e569fc583e92424e31adac11293c9edf587fb1768fb052de749cfb1396f1687c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "months", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c17fb3a3363e7d604c1f5a3dd024a589e5d06d9bd4af2d0688970d8f2e1d239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da6cd95e843c3372d40d49b926d7a02375e176b589d30fa2b3a4599eb2994a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupDrBackupPlanBackupRulesStandardSchedule]:
        return typing.cast(typing.Optional[BackupDrBackupPlanBackupRulesStandardSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupDrBackupPlanBackupRulesStandardSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5019bbc86d8a91532bec0441bce5ad96138b0770984057f1d3e224668c28442a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "week_of_month": "weekOfMonth"},
)
class BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        week_of_month: builtins.str,
    ) -> None:
        '''
        :param day_of_week: Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#day_of_week BackupDrBackupPlan#day_of_week}
        :param week_of_month: WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_of_month BackupDrBackupPlan#week_of_month}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afe53c2846f67fa332f8a676de92de5f6ccbe1eb36ec7874183bb2d61ca9748)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument week_of_month", value=week_of_month, expected_type=type_hints["week_of_month"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "week_of_month": week_of_month,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Specifies the day of the week. Possible values: ["DAY_OF_WEEK_UNSPECIFIED", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#day_of_week BackupDrBackupPlan#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def week_of_month(self) -> builtins.str:
        '''WeekOfMonth enumerates possible weeks in the month, e.g. the first, third, or last week of the month. Possible values: ["WEEK_OF_MONTH_UNSPECIFIED", "FIRST", "SECOND", "THIRD", "FOURTH", "LAST"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#week_of_month BackupDrBackupPlan#week_of_month}
        '''
        result = self._values.get("week_of_month")
        assert result is not None, "Required property 'week_of_month' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ec4bb2d3f0602bf740eac31b6aa704ab1a7450961254a0be0ac40c51a990f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7525bf43e5aa2389af4c1d65ceb34516f484dcfd4637c1e1fa297620f2cf5708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfMonth")
    def week_of_month(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weekOfMonth"))

    @week_of_month.setter
    def week_of_month(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb44e30bca8cbfc224cb293d5259a10a5174010f705014c8b17487b5631a606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth]:
        return typing.cast(typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3da0f982fa4719c27170f628ee5959474bf1ecd89c3b17c10a1e0cd12496928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanConfig",
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
class BackupDrBackupPlanConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
        backup_vault: builtins.str,
        location: builtins.str,
        resource_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BackupDrBackupPlanTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param backup_plan_id: The ID of the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_plan_id BackupDrBackupPlan#backup_plan_id}
        :param backup_rules: backup_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_rules BackupDrBackupPlan#backup_rules}
        :param backup_vault: Backup vault where the backups gets stored using this Backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_vault BackupDrBackupPlan#backup_vault}
        :param location: The location for the backup plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#location BackupDrBackupPlan#location}
        :param resource_type: The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance", "compute.googleapis.com/Disk", and "storage.googleapis.com/Bucket". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#resource_type BackupDrBackupPlan#resource_type}
        :param description: The description allows for additional details about 'BackupPlan' and its use cases to be provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#description BackupDrBackupPlan#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#id BackupDrBackupPlan#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#project BackupDrBackupPlan#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#timeouts BackupDrBackupPlan#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BackupDrBackupPlanTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109f2c5a3520bb88925c5586edb2f8d1f1ed9f7186814015703cc297dba34322)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_plan_id BackupDrBackupPlan#backup_plan_id}
        '''
        result = self._values.get("backup_plan_id")
        assert result is not None, "Required property 'backup_plan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]]:
        '''backup_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_rules BackupDrBackupPlan#backup_rules}
        '''
        result = self._values.get("backup_rules")
        assert result is not None, "Required property 'backup_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]], result)

    @builtins.property
    def backup_vault(self) -> builtins.str:
        '''Backup vault where the backups gets stored using this Backup plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#backup_vault BackupDrBackupPlan#backup_vault}
        '''
        result = self._values.get("backup_vault")
        assert result is not None, "Required property 'backup_vault' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the backup plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#location BackupDrBackupPlan#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''The resource type to which the 'BackupPlan' will be applied. Examples include, "compute.googleapis.com/Instance", "compute.googleapis.com/Disk", and "storage.googleapis.com/Bucket".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#resource_type BackupDrBackupPlan#resource_type}
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description allows for additional details about 'BackupPlan' and its use cases to be provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#description BackupDrBackupPlan#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#id BackupDrBackupPlan#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#project BackupDrBackupPlan#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BackupDrBackupPlanTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#timeouts BackupDrBackupPlan#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BackupDrBackupPlanTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BackupDrBackupPlanTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#create BackupDrBackupPlan#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#delete BackupDrBackupPlan#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#update BackupDrBackupPlan#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd3dc40a8f8509fc8db3152a62be48c7e8410e3c4c0bd78c368dd9e0d046158)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#create BackupDrBackupPlan#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#delete BackupDrBackupPlan#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/backup_dr_backup_plan#update BackupDrBackupPlan#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupDrBackupPlanTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupDrBackupPlanTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.backupDrBackupPlan.BackupDrBackupPlanTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e06ae55a888511faeaea5b6c0f57f84862ade64519c90f1b2f0936176a46fb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b13636b168d41c4b8fa480c3499469f0cfcc63644b6de2132b159bde5107f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36fd94fda27efb9b36883f8318409c93e085f0b5d25f4bc903656f3426c47ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74566e853b4fe66cb35805a51c65bcb0542eebc3f942840a10439d6254e982c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b489cd619db84a8fd31d48259d99baeed196a027a89d873a9518a99e454982bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BackupDrBackupPlan",
    "BackupDrBackupPlanBackupRules",
    "BackupDrBackupPlanBackupRulesList",
    "BackupDrBackupPlanBackupRulesOutputReference",
    "BackupDrBackupPlanBackupRulesStandardSchedule",
    "BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow",
    "BackupDrBackupPlanBackupRulesStandardScheduleBackupWindowOutputReference",
    "BackupDrBackupPlanBackupRulesStandardScheduleOutputReference",
    "BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth",
    "BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonthOutputReference",
    "BackupDrBackupPlanConfig",
    "BackupDrBackupPlanTimeouts",
    "BackupDrBackupPlanTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5f8aefd0c070dbf07b92051d68cd409a8fada1ad1c96510844006a5d03493f4e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    backup_plan_id: builtins.str,
    backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
    backup_vault: builtins.str,
    location: builtins.str,
    resource_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BackupDrBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f3543a17107e6ac26e5cbf9929a888faa67c419a09e3e0551019c1e38f0b2b67(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2bcbfc02b5a74f78d36cbf974a0dc4d5f8c9c325fe63041500f559bdd197ae(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2f8263d575106cb6c5e9f8d6b94693814de1d75faf0c94069da148aaf3a6db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e85441cd7dc0cd058b286854672fe4a0352ee93b3632bb52ae023ec8b95881(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c399d92617a35c6fb8df9f7b2f05cf4fb9cb2673ce8af15dac0ed93b9ad48c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29dd42ac80810f31645c5973a19935f193a3d5b23b0078738818c8308f96f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09619401f14e8d2b8457534c33b2ae3554bd7e9aacc3c34df8cf84da4033b1fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6fd6df75d70b056b5940c91be0f09788aff6b8c1128dae010f3a3ccca46156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c791a524ee0b5002090c0af9a7899bba213538ef28e8cb28f53747c03dc296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7f0155692fd8cbd2326117ec828cce889f1a8144df5c61dcd21d7f9522caa2(
    *,
    backup_retention_days: jsii.Number,
    rule_id: builtins.str,
    standard_schedule: typing.Union[BackupDrBackupPlanBackupRulesStandardSchedule, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa0b2d68a7f4a988353c1e53fbd791d0bdc7a9edcba3106216fcc901a501fb7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05e704dc4c5e883d31447ea9f6a773d51b277b5a025893df8c349755eae02e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6339a8f850558f5c30d34d3e57d736b7f1ca0668aca63db0de6ca27dba2d2574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5b1c50e87936f66e87a414fd57ae14711663af1581f8c87ff825f19374278c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3a0029a929c0a7426dd7df364e09c0a9b186031e15a68edc48ed49ab07fc24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38aa8077f4481d33dea3cd9e2ab8f8711b45258523ec884e4a8b63885941bfc2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BackupDrBackupPlanBackupRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f508cdd17beeb76082262785427b05faed048dc8c84cd9ee25327414ced4fa70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782596732df6a889eb578ed35017cc042a506036c9438c195c705bb4839c60fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be44cbe31435d263731aeeb1ceeb292a7847e847055c1dd4f35e02ce1dab146d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd8e5e138d09582c440c3e64a8a015236802b8e66132cfce2abed6522aa2ce6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanBackupRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f6cb1fe5b0ae96243d6eaf952bb5cb2726930185f50e307e014d3ec20a60b5(
    *,
    recurrence_type: builtins.str,
    time_zone: builtins.str,
    backup_window: typing.Optional[typing.Union[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    days_of_month: typing.Optional[typing.Sequence[jsii.Number]] = None,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    hourly_frequency: typing.Optional[jsii.Number] = None,
    months: typing.Optional[typing.Sequence[builtins.str]] = None,
    week_day_of_month: typing.Optional[typing.Union[BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd15ec2f4e67d14b6742a7b07a63248c9e5d7dd08e34fedd36414f3b4cf6d83b(
    *,
    start_hour_of_day: jsii.Number,
    end_hour_of_day: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392ec604943ebe8da995af45f2f2d61c0ac47fc0f1dd76a73295d1a3bb2504a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1485773937d9f21adcfb36aaf3c23827039d8972746d52f9792e78d711cdfb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3646cca28a72f0b5bf353a9241ef34b9b774c4df212d26837cc510ae6a2d7b5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd38597f141ed812f9b577f24c39f7148627a66a04c2e94440177def340ac355(
    value: typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleBackupWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d012866cdc547e52bb19c64d9682866b7bab62a75a2af3d2df3c3d3fd17bec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af1c2ef6e5a75d30d95de05845c9695c260c3e5295f6f2fb37b6ba57c4a2d14(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c932f76ac75e7567dfa4eb7beb4e1f5c13a3019bb7dd38ae9429e1fd20366a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4f426e546725410f9d6de33a7e5c9388c51d4c36a6a43234d42d416ced3f8c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e569fc583e92424e31adac11293c9edf587fb1768fb052de749cfb1396f1687c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c17fb3a3363e7d604c1f5a3dd024a589e5d06d9bd4af2d0688970d8f2e1d239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da6cd95e843c3372d40d49b926d7a02375e176b589d30fa2b3a4599eb2994a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5019bbc86d8a91532bec0441bce5ad96138b0770984057f1d3e224668c28442a(
    value: typing.Optional[BackupDrBackupPlanBackupRulesStandardSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afe53c2846f67fa332f8a676de92de5f6ccbe1eb36ec7874183bb2d61ca9748(
    *,
    day_of_week: builtins.str,
    week_of_month: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ec4bb2d3f0602bf740eac31b6aa704ab1a7450961254a0be0ac40c51a990f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7525bf43e5aa2389af4c1d65ceb34516f484dcfd4637c1e1fa297620f2cf5708(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb44e30bca8cbfc224cb293d5259a10a5174010f705014c8b17487b5631a606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3da0f982fa4719c27170f628ee5959474bf1ecd89c3b17c10a1e0cd12496928(
    value: typing.Optional[BackupDrBackupPlanBackupRulesStandardScheduleWeekDayOfMonth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109f2c5a3520bb88925c5586edb2f8d1f1ed9f7186814015703cc297dba34322(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    backup_plan_id: builtins.str,
    backup_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BackupDrBackupPlanBackupRules, typing.Dict[builtins.str, typing.Any]]]],
    backup_vault: builtins.str,
    location: builtins.str,
    resource_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BackupDrBackupPlanTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd3dc40a8f8509fc8db3152a62be48c7e8410e3c4c0bd78c368dd9e0d046158(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e06ae55a888511faeaea5b6c0f57f84862ade64519c90f1b2f0936176a46fb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b13636b168d41c4b8fa480c3499469f0cfcc63644b6de2132b159bde5107f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36fd94fda27efb9b36883f8318409c93e085f0b5d25f4bc903656f3426c47ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74566e853b4fe66cb35805a51c65bcb0542eebc3f942840a10439d6254e982c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b489cd619db84a8fd31d48259d99baeed196a027a89d873a9518a99e454982bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BackupDrBackupPlanTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

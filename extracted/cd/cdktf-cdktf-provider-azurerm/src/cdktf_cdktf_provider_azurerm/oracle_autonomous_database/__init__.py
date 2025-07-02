r'''
# `azurerm_oracle_autonomous_database`

Refer to the Terraform Registry for docs: [`azurerm_oracle_autonomous_database`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database).
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


class OracleAutonomousDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database azurerm_oracle_autonomous_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_password: builtins.str,
        auto_scaling_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        auto_scaling_for_storage_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        backup_retention_period_in_days: jsii.Number,
        character_set: builtins.str,
        compute_count: jsii.Number,
        compute_model: builtins.str,
        data_storage_size_in_tbs: jsii.Number,
        db_version: builtins.str,
        db_workload: builtins.str,
        display_name: builtins.str,
        license_model: builtins.str,
        location: builtins.str,
        mtls_connection_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        national_character_set: builtins.str,
        resource_group_name: builtins.str,
        subnet_id: builtins.str,
        virtual_network_id: builtins.str,
        customer_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        long_term_backup_schedule: typing.Optional[typing.Union["OracleAutonomousDatabaseLongTermBackupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OracleAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database azurerm_oracle_autonomous_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#admin_password OracleAutonomousDatabase#admin_password}.
        :param auto_scaling_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_enabled OracleAutonomousDatabase#auto_scaling_enabled}.
        :param auto_scaling_for_storage_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_for_storage_enabled OracleAutonomousDatabase#auto_scaling_for_storage_enabled}.
        :param backup_retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#backup_retention_period_in_days OracleAutonomousDatabase#backup_retention_period_in_days}.
        :param character_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#character_set OracleAutonomousDatabase#character_set}.
        :param compute_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_count OracleAutonomousDatabase#compute_count}.
        :param compute_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_model OracleAutonomousDatabase#compute_model}.
        :param data_storage_size_in_tbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#data_storage_size_in_tbs OracleAutonomousDatabase#data_storage_size_in_tbs}.
        :param db_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_version OracleAutonomousDatabase#db_version}.
        :param db_workload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_workload OracleAutonomousDatabase#db_workload}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#display_name OracleAutonomousDatabase#display_name}.
        :param license_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#license_model OracleAutonomousDatabase#license_model}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#location OracleAutonomousDatabase#location}.
        :param mtls_connection_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#mtls_connection_required OracleAutonomousDatabase#mtls_connection_required}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#name OracleAutonomousDatabase#name}.
        :param national_character_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#national_character_set OracleAutonomousDatabase#national_character_set}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#resource_group_name OracleAutonomousDatabase#resource_group_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#subnet_id OracleAutonomousDatabase#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#virtual_network_id OracleAutonomousDatabase#virtual_network_id}.
        :param customer_contacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#customer_contacts OracleAutonomousDatabase#customer_contacts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#id OracleAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_term_backup_schedule: long_term_backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#long_term_backup_schedule OracleAutonomousDatabase#long_term_backup_schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#tags OracleAutonomousDatabase#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#timeouts OracleAutonomousDatabase#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a6b9361df9a91ea45a4133a36f84cb4a141450c8d0439488f9216864d10fec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OracleAutonomousDatabaseConfig(
            admin_password=admin_password,
            auto_scaling_enabled=auto_scaling_enabled,
            auto_scaling_for_storage_enabled=auto_scaling_for_storage_enabled,
            backup_retention_period_in_days=backup_retention_period_in_days,
            character_set=character_set,
            compute_count=compute_count,
            compute_model=compute_model,
            data_storage_size_in_tbs=data_storage_size_in_tbs,
            db_version=db_version,
            db_workload=db_workload,
            display_name=display_name,
            license_model=license_model,
            location=location,
            mtls_connection_required=mtls_connection_required,
            name=name,
            national_character_set=national_character_set,
            resource_group_name=resource_group_name,
            subnet_id=subnet_id,
            virtual_network_id=virtual_network_id,
            customer_contacts=customer_contacts,
            id=id,
            long_term_backup_schedule=long_term_backup_schedule,
            tags=tags,
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
        '''Generates CDKTF code for importing a OracleAutonomousDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OracleAutonomousDatabase to import.
        :param import_from_id: The id of the existing OracleAutonomousDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OracleAutonomousDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca79d79cf99e732d98ddf400f9f35db48269da5bc7a10e3db67f0eda177193f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLongTermBackupSchedule")
    def put_long_term_backup_schedule(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        repeat_cadence: builtins.str,
        retention_period_in_days: jsii.Number,
        time_of_backup: builtins.str,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#enabled OracleAutonomousDatabase#enabled}.
        :param repeat_cadence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#repeat_cadence OracleAutonomousDatabase#repeat_cadence}.
        :param retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#retention_period_in_days OracleAutonomousDatabase#retention_period_in_days}.
        :param time_of_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#time_of_backup OracleAutonomousDatabase#time_of_backup}.
        '''
        value = OracleAutonomousDatabaseLongTermBackupSchedule(
            enabled=enabled,
            repeat_cadence=repeat_cadence,
            retention_period_in_days=retention_period_in_days,
            time_of_backup=time_of_backup,
        )

        return typing.cast(None, jsii.invoke(self, "putLongTermBackupSchedule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#create OracleAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#delete OracleAutonomousDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#read OracleAutonomousDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#update OracleAutonomousDatabase#update}.
        '''
        value = OracleAutonomousDatabaseTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCustomerContacts")
    def reset_customer_contacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerContacts", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLongTermBackupSchedule")
    def reset_long_term_backup_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongTermBackupSchedule", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="longTermBackupSchedule")
    def long_term_backup_schedule(
        self,
    ) -> "OracleAutonomousDatabaseLongTermBackupScheduleOutputReference":
        return typing.cast("OracleAutonomousDatabaseLongTermBackupScheduleOutputReference", jsii.get(self, "longTermBackupSchedule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OracleAutonomousDatabaseTimeoutsOutputReference":
        return typing.cast("OracleAutonomousDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingEnabledInput")
    def auto_scaling_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoScalingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingForStorageEnabledInput")
    def auto_scaling_for_storage_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoScalingForStorageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriodInDaysInput")
    def backup_retention_period_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionPeriodInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="characterSetInput")
    def character_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "characterSetInput"))

    @builtins.property
    @jsii.member(jsii_name="computeCountInput")
    def compute_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="computeModelInput")
    def compute_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeModelInput"))

    @builtins.property
    @jsii.member(jsii_name="customerContactsInput")
    def customer_contacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customerContactsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbsInput")
    def data_storage_size_in_tbs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataStorageSizeInTbsInput"))

    @builtins.property
    @jsii.member(jsii_name="dbVersionInput")
    def db_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="dbWorkloadInput")
    def db_workload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbWorkloadInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseModelInput")
    def license_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseModelInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="longTermBackupScheduleInput")
    def long_term_backup_schedule_input(
        self,
    ) -> typing.Optional["OracleAutonomousDatabaseLongTermBackupSchedule"]:
        return typing.cast(typing.Optional["OracleAutonomousDatabaseLongTermBackupSchedule"], jsii.get(self, "longTermBackupScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="mtlsConnectionRequiredInput")
    def mtls_connection_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mtlsConnectionRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nationalCharacterSetInput")
    def national_character_set_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nationalCharacterSetInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleAutonomousDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OracleAutonomousDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135fa7f1df2ab34cde5e15408f068022f898ab2f5fa4e85c6c156767878218d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoScalingEnabled")
    def auto_scaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoScalingEnabled"))

    @auto_scaling_enabled.setter
    def auto_scaling_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7be559d68dafa7015182f3876dbb08a13114bd4f5efd6f30cbfcb609ebc95f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoScalingForStorageEnabled")
    def auto_scaling_for_storage_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoScalingForStorageEnabled"))

    @auto_scaling_for_storage_enabled.setter
    def auto_scaling_for_storage_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bb166bf89d019131fd563213c4a92dc7375cc63b31fe3b92bf4dd7f7a5d2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingForStorageEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriodInDays")
    def backup_retention_period_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionPeriodInDays"))

    @backup_retention_period_in_days.setter
    def backup_retention_period_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbc393752e5a618853b8a90e42bb3fb9ac81a9609b6a0e499ee60482304f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionPeriodInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="characterSet")
    def character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "characterSet"))

    @character_set.setter
    def character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1638563dd4d404c70ce7b7f39df1dc627b2d29b5ee27695d37b6e2933acda3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "characterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @compute_count.setter
    def compute_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2008d4de58932eea191e789c8a1fc0f32b9a97c18c7aa9681f7735e8d1dde99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeModel")
    def compute_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeModel"))

    @compute_model.setter
    def compute_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b036547ff3b1b41dd375a91dbc875aa688a02b673ab09f85390dde69f547d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customerContacts"))

    @customer_contacts.setter
    def customer_contacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a105cecfbcd59d5a244348bb15ec389a854b95795388108594eba6ab6a2dfdcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerContacts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeInTbs")
    def data_storage_size_in_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeInTbs"))

    @data_storage_size_in_tbs.setter
    def data_storage_size_in_tbs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a217dcc051d39d11dc29db210ddc0d730989c68378f35081ae17fa32bd289d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStorageSizeInTbs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbVersion")
    def db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbVersion"))

    @db_version.setter
    def db_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c847984141fe8962e3538396f3c264973c0d474f6c547b622d2ee82bc95dcfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbWorkload")
    def db_workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbWorkload"))

    @db_workload.setter
    def db_workload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cd50d723ff5da449c95a17dcbf43042a4966b0c8825153de96a6c97d62e8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbWorkload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075eb9d4421477a0e4a40425e8323f949136deaa88c2733cd15b798177a00d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5312c5165e29069991660bb9a8949836bd55b1ff5bee22bc1a256e1e4dfdfc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseModel"))

    @license_model.setter
    def license_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb87e04cbacf0396097209e4e28ae3f455eef184397a1c78bee3d37939bb700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ed4286352ea70a78193a3f1d7388646e9e095cab1b242838f36ee20932d8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtlsConnectionRequired")
    def mtls_connection_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mtlsConnectionRequired"))

    @mtls_connection_required.setter
    def mtls_connection_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d55d1057f2417ea596a67956e65243f54ea0b55763c9bc72e73e96fb733b9fcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtlsConnectionRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f790f98277cf775ce8d1dec647e4124344989eb727adae069941a8d9d5717d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nationalCharacterSet")
    def national_character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nationalCharacterSet"))

    @national_character_set.setter
    def national_character_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea985248d72cd21b17d00569e0a356fd6e93ac3e36e4153e615eafac94632356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nationalCharacterSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60a3e71759b48b28feb53e2e3247711ec75e6fa8f0bcdaf043ba693930130e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fd9a5fba57ba1e0c204a5b8b09e2275080490906fc40a84910efee2daf8969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a9a55c94d4e6a00d88d05ab78ea37e2821661b411d327be3b729edb1011c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e352dee95acb7eed4ed492a3639b9a689ad7a71abc146d0b241e29ac9873352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "admin_password": "adminPassword",
        "auto_scaling_enabled": "autoScalingEnabled",
        "auto_scaling_for_storage_enabled": "autoScalingForStorageEnabled",
        "backup_retention_period_in_days": "backupRetentionPeriodInDays",
        "character_set": "characterSet",
        "compute_count": "computeCount",
        "compute_model": "computeModel",
        "data_storage_size_in_tbs": "dataStorageSizeInTbs",
        "db_version": "dbVersion",
        "db_workload": "dbWorkload",
        "display_name": "displayName",
        "license_model": "licenseModel",
        "location": "location",
        "mtls_connection_required": "mtlsConnectionRequired",
        "name": "name",
        "national_character_set": "nationalCharacterSet",
        "resource_group_name": "resourceGroupName",
        "subnet_id": "subnetId",
        "virtual_network_id": "virtualNetworkId",
        "customer_contacts": "customerContacts",
        "id": "id",
        "long_term_backup_schedule": "longTermBackupSchedule",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class OracleAutonomousDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_password: builtins.str,
        auto_scaling_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        auto_scaling_for_storage_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        backup_retention_period_in_days: jsii.Number,
        character_set: builtins.str,
        compute_count: jsii.Number,
        compute_model: builtins.str,
        data_storage_size_in_tbs: jsii.Number,
        db_version: builtins.str,
        db_workload: builtins.str,
        display_name: builtins.str,
        license_model: builtins.str,
        location: builtins.str,
        mtls_connection_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        national_character_set: builtins.str,
        resource_group_name: builtins.str,
        subnet_id: builtins.str,
        virtual_network_id: builtins.str,
        customer_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        long_term_backup_schedule: typing.Optional[typing.Union["OracleAutonomousDatabaseLongTermBackupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OracleAutonomousDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#admin_password OracleAutonomousDatabase#admin_password}.
        :param auto_scaling_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_enabled OracleAutonomousDatabase#auto_scaling_enabled}.
        :param auto_scaling_for_storage_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_for_storage_enabled OracleAutonomousDatabase#auto_scaling_for_storage_enabled}.
        :param backup_retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#backup_retention_period_in_days OracleAutonomousDatabase#backup_retention_period_in_days}.
        :param character_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#character_set OracleAutonomousDatabase#character_set}.
        :param compute_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_count OracleAutonomousDatabase#compute_count}.
        :param compute_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_model OracleAutonomousDatabase#compute_model}.
        :param data_storage_size_in_tbs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#data_storage_size_in_tbs OracleAutonomousDatabase#data_storage_size_in_tbs}.
        :param db_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_version OracleAutonomousDatabase#db_version}.
        :param db_workload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_workload OracleAutonomousDatabase#db_workload}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#display_name OracleAutonomousDatabase#display_name}.
        :param license_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#license_model OracleAutonomousDatabase#license_model}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#location OracleAutonomousDatabase#location}.
        :param mtls_connection_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#mtls_connection_required OracleAutonomousDatabase#mtls_connection_required}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#name OracleAutonomousDatabase#name}.
        :param national_character_set: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#national_character_set OracleAutonomousDatabase#national_character_set}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#resource_group_name OracleAutonomousDatabase#resource_group_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#subnet_id OracleAutonomousDatabase#subnet_id}.
        :param virtual_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#virtual_network_id OracleAutonomousDatabase#virtual_network_id}.
        :param customer_contacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#customer_contacts OracleAutonomousDatabase#customer_contacts}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#id OracleAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_term_backup_schedule: long_term_backup_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#long_term_backup_schedule OracleAutonomousDatabase#long_term_backup_schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#tags OracleAutonomousDatabase#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#timeouts OracleAutonomousDatabase#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(long_term_backup_schedule, dict):
            long_term_backup_schedule = OracleAutonomousDatabaseLongTermBackupSchedule(**long_term_backup_schedule)
        if isinstance(timeouts, dict):
            timeouts = OracleAutonomousDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d34e3ac75e73d28aeec5f59ab50a5993155bc63b3cde63986300637325a5c5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument auto_scaling_enabled", value=auto_scaling_enabled, expected_type=type_hints["auto_scaling_enabled"])
            check_type(argname="argument auto_scaling_for_storage_enabled", value=auto_scaling_for_storage_enabled, expected_type=type_hints["auto_scaling_for_storage_enabled"])
            check_type(argname="argument backup_retention_period_in_days", value=backup_retention_period_in_days, expected_type=type_hints["backup_retention_period_in_days"])
            check_type(argname="argument character_set", value=character_set, expected_type=type_hints["character_set"])
            check_type(argname="argument compute_count", value=compute_count, expected_type=type_hints["compute_count"])
            check_type(argname="argument compute_model", value=compute_model, expected_type=type_hints["compute_model"])
            check_type(argname="argument data_storage_size_in_tbs", value=data_storage_size_in_tbs, expected_type=type_hints["data_storage_size_in_tbs"])
            check_type(argname="argument db_version", value=db_version, expected_type=type_hints["db_version"])
            check_type(argname="argument db_workload", value=db_workload, expected_type=type_hints["db_workload"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mtls_connection_required", value=mtls_connection_required, expected_type=type_hints["mtls_connection_required"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument national_character_set", value=national_character_set, expected_type=type_hints["national_character_set"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
            check_type(argname="argument customer_contacts", value=customer_contacts, expected_type=type_hints["customer_contacts"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument long_term_backup_schedule", value=long_term_backup_schedule, expected_type=type_hints["long_term_backup_schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_password": admin_password,
            "auto_scaling_enabled": auto_scaling_enabled,
            "auto_scaling_for_storage_enabled": auto_scaling_for_storage_enabled,
            "backup_retention_period_in_days": backup_retention_period_in_days,
            "character_set": character_set,
            "compute_count": compute_count,
            "compute_model": compute_model,
            "data_storage_size_in_tbs": data_storage_size_in_tbs,
            "db_version": db_version,
            "db_workload": db_workload,
            "display_name": display_name,
            "license_model": license_model,
            "location": location,
            "mtls_connection_required": mtls_connection_required,
            "name": name,
            "national_character_set": national_character_set,
            "resource_group_name": resource_group_name,
            "subnet_id": subnet_id,
            "virtual_network_id": virtual_network_id,
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
        if customer_contacts is not None:
            self._values["customer_contacts"] = customer_contacts
        if id is not None:
            self._values["id"] = id
        if long_term_backup_schedule is not None:
            self._values["long_term_backup_schedule"] = long_term_backup_schedule
        if tags is not None:
            self._values["tags"] = tags
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
    def admin_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#admin_password OracleAutonomousDatabase#admin_password}.'''
        result = self._values.get("admin_password")
        assert result is not None, "Required property 'admin_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_scaling_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_enabled OracleAutonomousDatabase#auto_scaling_enabled}.'''
        result = self._values.get("auto_scaling_enabled")
        assert result is not None, "Required property 'auto_scaling_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def auto_scaling_for_storage_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#auto_scaling_for_storage_enabled OracleAutonomousDatabase#auto_scaling_for_storage_enabled}.'''
        result = self._values.get("auto_scaling_for_storage_enabled")
        assert result is not None, "Required property 'auto_scaling_for_storage_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def backup_retention_period_in_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#backup_retention_period_in_days OracleAutonomousDatabase#backup_retention_period_in_days}.'''
        result = self._values.get("backup_retention_period_in_days")
        assert result is not None, "Required property 'backup_retention_period_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def character_set(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#character_set OracleAutonomousDatabase#character_set}.'''
        result = self._values.get("character_set")
        assert result is not None, "Required property 'character_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_count OracleAutonomousDatabase#compute_count}.'''
        result = self._values.get("compute_count")
        assert result is not None, "Required property 'compute_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def compute_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#compute_model OracleAutonomousDatabase#compute_model}.'''
        result = self._values.get("compute_model")
        assert result is not None, "Required property 'compute_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_storage_size_in_tbs(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#data_storage_size_in_tbs OracleAutonomousDatabase#data_storage_size_in_tbs}.'''
        result = self._values.get("data_storage_size_in_tbs")
        assert result is not None, "Required property 'data_storage_size_in_tbs' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def db_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_version OracleAutonomousDatabase#db_version}.'''
        result = self._values.get("db_version")
        assert result is not None, "Required property 'db_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_workload(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#db_workload OracleAutonomousDatabase#db_workload}.'''
        result = self._values.get("db_workload")
        assert result is not None, "Required property 'db_workload' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#display_name OracleAutonomousDatabase#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_model(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#license_model OracleAutonomousDatabase#license_model}.'''
        result = self._values.get("license_model")
        assert result is not None, "Required property 'license_model' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#location OracleAutonomousDatabase#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mtls_connection_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#mtls_connection_required OracleAutonomousDatabase#mtls_connection_required}.'''
        result = self._values.get("mtls_connection_required")
        assert result is not None, "Required property 'mtls_connection_required' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#name OracleAutonomousDatabase#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def national_character_set(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#national_character_set OracleAutonomousDatabase#national_character_set}.'''
        result = self._values.get("national_character_set")
        assert result is not None, "Required property 'national_character_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#resource_group_name OracleAutonomousDatabase#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#subnet_id OracleAutonomousDatabase#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#virtual_network_id OracleAutonomousDatabase#virtual_network_id}.'''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_contacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#customer_contacts OracleAutonomousDatabase#customer_contacts}.'''
        result = self._values.get("customer_contacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#id OracleAutonomousDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_term_backup_schedule(
        self,
    ) -> typing.Optional["OracleAutonomousDatabaseLongTermBackupSchedule"]:
        '''long_term_backup_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#long_term_backup_schedule OracleAutonomousDatabase#long_term_backup_schedule}
        '''
        result = self._values.get("long_term_backup_schedule")
        return typing.cast(typing.Optional["OracleAutonomousDatabaseLongTermBackupSchedule"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#tags OracleAutonomousDatabase#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OracleAutonomousDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#timeouts OracleAutonomousDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OracleAutonomousDatabaseTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleAutonomousDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabaseLongTermBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "repeat_cadence": "repeatCadence",
        "retention_period_in_days": "retentionPeriodInDays",
        "time_of_backup": "timeOfBackup",
    },
)
class OracleAutonomousDatabaseLongTermBackupSchedule:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        repeat_cadence: builtins.str,
        retention_period_in_days: jsii.Number,
        time_of_backup: builtins.str,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#enabled OracleAutonomousDatabase#enabled}.
        :param repeat_cadence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#repeat_cadence OracleAutonomousDatabase#repeat_cadence}.
        :param retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#retention_period_in_days OracleAutonomousDatabase#retention_period_in_days}.
        :param time_of_backup: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#time_of_backup OracleAutonomousDatabase#time_of_backup}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd9f9b67caa86156a7751cfce7a5547e06912432094d9e5e506a19a07428131)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument repeat_cadence", value=repeat_cadence, expected_type=type_hints["repeat_cadence"])
            check_type(argname="argument retention_period_in_days", value=retention_period_in_days, expected_type=type_hints["retention_period_in_days"])
            check_type(argname="argument time_of_backup", value=time_of_backup, expected_type=type_hints["time_of_backup"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "repeat_cadence": repeat_cadence,
            "retention_period_in_days": retention_period_in_days,
            "time_of_backup": time_of_backup,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#enabled OracleAutonomousDatabase#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def repeat_cadence(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#repeat_cadence OracleAutonomousDatabase#repeat_cadence}.'''
        result = self._values.get("repeat_cadence")
        assert result is not None, "Required property 'repeat_cadence' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_period_in_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#retention_period_in_days OracleAutonomousDatabase#retention_period_in_days}.'''
        result = self._values.get("retention_period_in_days")
        assert result is not None, "Required property 'retention_period_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_of_backup(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#time_of_backup OracleAutonomousDatabase#time_of_backup}.'''
        result = self._values.get("time_of_backup")
        assert result is not None, "Required property 'time_of_backup' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleAutonomousDatabaseLongTermBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleAutonomousDatabaseLongTermBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabaseLongTermBackupScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f521b358a7c1d2fe632d4dc6e3f656d1a9a1d688b3bd79963beb02cebcb6b6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="repeatCadenceInput")
    def repeat_cadence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repeatCadenceInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInDaysInput")
    def retention_period_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOfBackupInput")
    def time_of_backup_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeOfBackupInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3bfbbb9d1bf286b0b969444f24f661b273accc850ca5be6143c361d1f3e85e27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repeatCadence")
    def repeat_cadence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repeatCadence"))

    @repeat_cadence.setter
    def repeat_cadence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10bed0edf6b94bebb5d79ed8c3ab12a200dc2b4cbb2cb033c4c596f2ecba288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repeatCadence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInDays")
    def retention_period_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodInDays"))

    @retention_period_in_days.setter
    def retention_period_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794be9d70c5d8898d31da3d6edee1cad261bb4b1ea906fe65d1f3f0fe1cea944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOfBackup")
    def time_of_backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOfBackup"))

    @time_of_backup.setter
    def time_of_backup(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bd44c505fc0b4e2b3884395f1be808edfdc040c5ae66ff30e4dab952b19252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeOfBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OracleAutonomousDatabaseLongTermBackupSchedule]:
        return typing.cast(typing.Optional[OracleAutonomousDatabaseLongTermBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OracleAutonomousDatabaseLongTermBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73010eb61337f02d68984ee44efcd7b3dbdeb40719c662deb446f06974357538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class OracleAutonomousDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#create OracleAutonomousDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#delete OracleAutonomousDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#read OracleAutonomousDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#update OracleAutonomousDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874b4250858adda1a396c7100809ec9ce6460e01ff9bb6556cd13933bd24e628)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#create OracleAutonomousDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#delete OracleAutonomousDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#read OracleAutonomousDatabase#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/oracle_autonomous_database#update OracleAutonomousDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleAutonomousDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleAutonomousDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.oracleAutonomousDatabase.OracleAutonomousDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa4af0585a84f58c006583935a0d05b22f91f491a34f7ac068113f2365716f78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9471d412d35f1933f6d38ea5b6c8972ed7bacfc313458b47287f2207c0966dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fada85aef52e7a2975b546f4deb95a3e91367460825afb145b88881eea2312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f1f9be41fc0d5b430737f8f5a94634c51065af5c47473f56a38a62f373476d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7bb5d9b6876fa15c5187974875eeb3859d5e7a101d2192a900812082a88d631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleAutonomousDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleAutonomousDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleAutonomousDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0550d11b0101e0b98e39aaeff7c2581f29911bfee15c74dcad76fffc27cf5d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OracleAutonomousDatabase",
    "OracleAutonomousDatabaseConfig",
    "OracleAutonomousDatabaseLongTermBackupSchedule",
    "OracleAutonomousDatabaseLongTermBackupScheduleOutputReference",
    "OracleAutonomousDatabaseTimeouts",
    "OracleAutonomousDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__20a6b9361df9a91ea45a4133a36f84cb4a141450c8d0439488f9216864d10fec(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_password: builtins.str,
    auto_scaling_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    auto_scaling_for_storage_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    backup_retention_period_in_days: jsii.Number,
    character_set: builtins.str,
    compute_count: jsii.Number,
    compute_model: builtins.str,
    data_storage_size_in_tbs: jsii.Number,
    db_version: builtins.str,
    db_workload: builtins.str,
    display_name: builtins.str,
    license_model: builtins.str,
    location: builtins.str,
    mtls_connection_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    national_character_set: builtins.str,
    resource_group_name: builtins.str,
    subnet_id: builtins.str,
    virtual_network_id: builtins.str,
    customer_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    long_term_backup_schedule: typing.Optional[typing.Union[OracleAutonomousDatabaseLongTermBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OracleAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ca79d79cf99e732d98ddf400f9f35db48269da5bc7a10e3db67f0eda177193f0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135fa7f1df2ab34cde5e15408f068022f898ab2f5fa4e85c6c156767878218d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7be559d68dafa7015182f3876dbb08a13114bd4f5efd6f30cbfcb609ebc95f9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bb166bf89d019131fd563213c4a92dc7375cc63b31fe3b92bf4dd7f7a5d2a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dbc393752e5a618853b8a90e42bb3fb9ac81a9609b6a0e499ee60482304f32(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1638563dd4d404c70ce7b7f39df1dc627b2d29b5ee27695d37b6e2933acda3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2008d4de58932eea191e789c8a1fc0f32b9a97c18c7aa9681f7735e8d1dde99a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b036547ff3b1b41dd375a91dbc875aa688a02b673ab09f85390dde69f547d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a105cecfbcd59d5a244348bb15ec389a854b95795388108594eba6ab6a2dfdcc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a217dcc051d39d11dc29db210ddc0d730989c68378f35081ae17fa32bd289d4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c847984141fe8962e3538396f3c264973c0d474f6c547b622d2ee82bc95dcfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cd50d723ff5da449c95a17dcbf43042a4966b0c8825153de96a6c97d62e8a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075eb9d4421477a0e4a40425e8323f949136deaa88c2733cd15b798177a00d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5312c5165e29069991660bb9a8949836bd55b1ff5bee22bc1a256e1e4dfdfc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb87e04cbacf0396097209e4e28ae3f455eef184397a1c78bee3d37939bb700(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ed4286352ea70a78193a3f1d7388646e9e095cab1b242838f36ee20932d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55d1057f2417ea596a67956e65243f54ea0b55763c9bc72e73e96fb733b9fcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f790f98277cf775ce8d1dec647e4124344989eb727adae069941a8d9d5717d18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea985248d72cd21b17d00569e0a356fd6e93ac3e36e4153e615eafac94632356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60a3e71759b48b28feb53e2e3247711ec75e6fa8f0bcdaf043ba693930130e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fd9a5fba57ba1e0c204a5b8b09e2275080490906fc40a84910efee2daf8969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a9a55c94d4e6a00d88d05ab78ea37e2821661b411d327be3b729edb1011c2b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e352dee95acb7eed4ed492a3639b9a689ad7a71abc146d0b241e29ac9873352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d34e3ac75e73d28aeec5f59ab50a5993155bc63b3cde63986300637325a5c5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_password: builtins.str,
    auto_scaling_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    auto_scaling_for_storage_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    backup_retention_period_in_days: jsii.Number,
    character_set: builtins.str,
    compute_count: jsii.Number,
    compute_model: builtins.str,
    data_storage_size_in_tbs: jsii.Number,
    db_version: builtins.str,
    db_workload: builtins.str,
    display_name: builtins.str,
    license_model: builtins.str,
    location: builtins.str,
    mtls_connection_required: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    national_character_set: builtins.str,
    resource_group_name: builtins.str,
    subnet_id: builtins.str,
    virtual_network_id: builtins.str,
    customer_contacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    long_term_backup_schedule: typing.Optional[typing.Union[OracleAutonomousDatabaseLongTermBackupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[OracleAutonomousDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd9f9b67caa86156a7751cfce7a5547e06912432094d9e5e506a19a07428131(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    repeat_cadence: builtins.str,
    retention_period_in_days: jsii.Number,
    time_of_backup: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f521b358a7c1d2fe632d4dc6e3f656d1a9a1d688b3bd79963beb02cebcb6b6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfbbb9d1bf286b0b969444f24f661b273accc850ca5be6143c361d1f3e85e27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10bed0edf6b94bebb5d79ed8c3ab12a200dc2b4cbb2cb033c4c596f2ecba288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794be9d70c5d8898d31da3d6edee1cad261bb4b1ea906fe65d1f3f0fe1cea944(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bd44c505fc0b4e2b3884395f1be808edfdc040c5ae66ff30e4dab952b19252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73010eb61337f02d68984ee44efcd7b3dbdeb40719c662deb446f06974357538(
    value: typing.Optional[OracleAutonomousDatabaseLongTermBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874b4250858adda1a396c7100809ec9ce6460e01ff9bb6556cd13933bd24e628(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4af0585a84f58c006583935a0d05b22f91f491a34f7ac068113f2365716f78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9471d412d35f1933f6d38ea5b6c8972ed7bacfc313458b47287f2207c0966dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fada85aef52e7a2975b546f4deb95a3e91367460825afb145b88881eea2312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f1f9be41fc0d5b430737f8f5a94634c51065af5c47473f56a38a62f373476d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7bb5d9b6876fa15c5187974875eeb3859d5e7a101d2192a900812082a88d631(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0550d11b0101e0b98e39aaeff7c2581f29911bfee15c74dcad76fffc27cf5d5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OracleAutonomousDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

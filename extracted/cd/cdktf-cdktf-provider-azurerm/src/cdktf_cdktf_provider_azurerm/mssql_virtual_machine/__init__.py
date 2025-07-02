r'''
# `azurerm_mssql_virtual_machine`

Refer to the Terraform Registry for docs: [`azurerm_mssql_virtual_machine`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine).
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


class MssqlVirtualMachine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine azurerm_mssql_virtual_machine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        virtual_machine_id: builtins.str,
        assessment: typing.Optional[typing.Union["MssqlVirtualMachineAssessment", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_backup: typing.Optional[typing.Union["MssqlVirtualMachineAutoBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_patching: typing.Optional[typing.Union["MssqlVirtualMachineAutoPatching", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key_vault_credential: typing.Optional[typing.Union["MssqlVirtualMachineKeyVaultCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        r_services_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_connectivity_port: typing.Optional[jsii.Number] = None,
        sql_connectivity_type: typing.Optional[builtins.str] = None,
        sql_connectivity_update_password: typing.Optional[builtins.str] = None,
        sql_connectivity_update_username: typing.Optional[builtins.str] = None,
        sql_instance: typing.Optional[typing.Union["MssqlVirtualMachineSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_license_type: typing.Optional[builtins.str] = None,
        sql_virtual_machine_group_id: typing.Optional[builtins.str] = None,
        storage_configuration: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wsfc_domain_credential: typing.Optional[typing.Union["MssqlVirtualMachineWsfcDomainCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine azurerm_mssql_virtual_machine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#virtual_machine_id MssqlVirtualMachine#virtual_machine_id}.
        :param assessment: assessment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#assessment MssqlVirtualMachine#assessment}
        :param auto_backup: auto_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_backup MssqlVirtualMachine#auto_backup}
        :param auto_patching: auto_patching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_patching MssqlVirtualMachine#auto_patching}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#id MssqlVirtualMachine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_vault_credential: key_vault_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_credential MssqlVirtualMachine#key_vault_credential}
        :param r_services_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#r_services_enabled MssqlVirtualMachine#r_services_enabled}.
        :param sql_connectivity_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_port MssqlVirtualMachine#sql_connectivity_port}.
        :param sql_connectivity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_type MssqlVirtualMachine#sql_connectivity_type}.
        :param sql_connectivity_update_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_password MssqlVirtualMachine#sql_connectivity_update_password}.
        :param sql_connectivity_update_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_username MssqlVirtualMachine#sql_connectivity_update_username}.
        :param sql_instance: sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_instance MssqlVirtualMachine#sql_instance}
        :param sql_license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_license_type MssqlVirtualMachine#sql_license_type}.
        :param sql_virtual_machine_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_virtual_machine_group_id MssqlVirtualMachine#sql_virtual_machine_group_id}.
        :param storage_configuration: storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_configuration MssqlVirtualMachine#storage_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#tags MssqlVirtualMachine#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#timeouts MssqlVirtualMachine#timeouts}
        :param wsfc_domain_credential: wsfc_domain_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#wsfc_domain_credential MssqlVirtualMachine#wsfc_domain_credential}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__623ee4980fcb19a68aee3d59f10e6949802218c892655776f7e4ad0c1dedeac2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlVirtualMachineConfig(
            virtual_machine_id=virtual_machine_id,
            assessment=assessment,
            auto_backup=auto_backup,
            auto_patching=auto_patching,
            id=id,
            key_vault_credential=key_vault_credential,
            r_services_enabled=r_services_enabled,
            sql_connectivity_port=sql_connectivity_port,
            sql_connectivity_type=sql_connectivity_type,
            sql_connectivity_update_password=sql_connectivity_update_password,
            sql_connectivity_update_username=sql_connectivity_update_username,
            sql_instance=sql_instance,
            sql_license_type=sql_license_type,
            sql_virtual_machine_group_id=sql_virtual_machine_group_id,
            storage_configuration=storage_configuration,
            tags=tags,
            timeouts=timeouts,
            wsfc_domain_credential=wsfc_domain_credential,
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
        '''Generates CDKTF code for importing a MssqlVirtualMachine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlVirtualMachine to import.
        :param import_from_id: The id of the existing MssqlVirtualMachine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlVirtualMachine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9d08a79fea667eeb2c3f8e5cf081da44bc5330a035af00feca81500ffa943b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAssessment")
    def put_assessment(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_immediately: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedule: typing.Optional[typing.Union["MssqlVirtualMachineAssessmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#enabled MssqlVirtualMachine#enabled}.
        :param run_immediately: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#run_immediately MssqlVirtualMachine#run_immediately}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#schedule MssqlVirtualMachine#schedule}
        '''
        value = MssqlVirtualMachineAssessment(
            enabled=enabled, run_immediately=run_immediately, schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putAssessment", [value]))

    @jsii.member(jsii_name="putAutoBackup")
    def put_auto_backup(
        self,
        *,
        retention_period_in_days: jsii.Number,
        storage_account_access_key: builtins.str,
        storage_blob_endpoint: builtins.str,
        encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_password: typing.Optional[builtins.str] = None,
        manual_schedule: typing.Optional[typing.Union["MssqlVirtualMachineAutoBackupManualSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        system_databases_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#retention_period_in_days MssqlVirtualMachine#retention_period_in_days}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_account_access_key MssqlVirtualMachine#storage_account_access_key}.
        :param storage_blob_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_blob_endpoint MssqlVirtualMachine#storage_blob_endpoint}.
        :param encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_enabled MssqlVirtualMachine#encryption_enabled}.
        :param encryption_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_password MssqlVirtualMachine#encryption_password}.
        :param manual_schedule: manual_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#manual_schedule MssqlVirtualMachine#manual_schedule}
        :param system_databases_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_databases_backup_enabled MssqlVirtualMachine#system_databases_backup_enabled}.
        '''
        value = MssqlVirtualMachineAutoBackup(
            retention_period_in_days=retention_period_in_days,
            storage_account_access_key=storage_account_access_key,
            storage_blob_endpoint=storage_blob_endpoint,
            encryption_enabled=encryption_enabled,
            encryption_password=encryption_password,
            manual_schedule=manual_schedule,
            system_databases_backup_enabled=system_databases_backup_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoBackup", [value]))

    @jsii.member(jsii_name="putAutoPatching")
    def put_auto_patching(
        self,
        *,
        day_of_week: builtins.str,
        maintenance_window_duration_in_minutes: jsii.Number,
        maintenance_window_starting_hour: jsii.Number,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.
        :param maintenance_window_duration_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_duration_in_minutes MssqlVirtualMachine#maintenance_window_duration_in_minutes}.
        :param maintenance_window_starting_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_starting_hour MssqlVirtualMachine#maintenance_window_starting_hour}.
        '''
        value = MssqlVirtualMachineAutoPatching(
            day_of_week=day_of_week,
            maintenance_window_duration_in_minutes=maintenance_window_duration_in_minutes,
            maintenance_window_starting_hour=maintenance_window_starting_hour,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoPatching", [value]))

    @jsii.member(jsii_name="putKeyVaultCredential")
    def put_key_vault_credential(
        self,
        *,
        key_vault_url: builtins.str,
        name: builtins.str,
        service_principal_name: builtins.str,
        service_principal_secret: builtins.str,
    ) -> None:
        '''
        :param key_vault_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_url MssqlVirtualMachine#key_vault_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#name MssqlVirtualMachine#name}.
        :param service_principal_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_name MssqlVirtualMachine#service_principal_name}.
        :param service_principal_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_secret MssqlVirtualMachine#service_principal_secret}.
        '''
        value = MssqlVirtualMachineKeyVaultCredential(
            key_vault_url=key_vault_url,
            name=name,
            service_principal_name=service_principal_name,
            service_principal_secret=service_principal_secret,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultCredential", [value]))

    @jsii.member(jsii_name="putSqlInstance")
    def put_sql_instance(
        self,
        *,
        adhoc_workloads_optimization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collation: typing.Optional[builtins.str] = None,
        instant_file_initialization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lock_pages_in_memory_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_dop: typing.Optional[jsii.Number] = None,
        max_server_memory_mb: typing.Optional[jsii.Number] = None,
        min_server_memory_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param adhoc_workloads_optimization_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#adhoc_workloads_optimization_enabled MssqlVirtualMachine#adhoc_workloads_optimization_enabled}.
        :param collation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#collation MssqlVirtualMachine#collation}.
        :param instant_file_initialization_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#instant_file_initialization_enabled MssqlVirtualMachine#instant_file_initialization_enabled}.
        :param lock_pages_in_memory_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#lock_pages_in_memory_enabled MssqlVirtualMachine#lock_pages_in_memory_enabled}.
        :param max_dop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_dop MssqlVirtualMachine#max_dop}.
        :param max_server_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_server_memory_mb MssqlVirtualMachine#max_server_memory_mb}.
        :param min_server_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#min_server_memory_mb MssqlVirtualMachine#min_server_memory_mb}.
        '''
        value = MssqlVirtualMachineSqlInstance(
            adhoc_workloads_optimization_enabled=adhoc_workloads_optimization_enabled,
            collation=collation,
            instant_file_initialization_enabled=instant_file_initialization_enabled,
            lock_pages_in_memory_enabled=lock_pages_in_memory_enabled,
            max_dop=max_dop,
            max_server_memory_mb=max_server_memory_mb,
            min_server_memory_mb=min_server_memory_mb,
        )

        return typing.cast(None, jsii.invoke(self, "putSqlInstance", [value]))

    @jsii.member(jsii_name="putStorageConfiguration")
    def put_storage_configuration(
        self,
        *,
        disk_type: builtins.str,
        storage_workload_type: builtins.str,
        data_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationDataSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        log_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationLogSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        system_db_on_data_disk_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        temp_db_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationTempDbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#disk_type MssqlVirtualMachine#disk_type}.
        :param storage_workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_workload_type MssqlVirtualMachine#storage_workload_type}.
        :param data_settings: data_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_settings MssqlVirtualMachine#data_settings}
        :param log_settings: log_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_settings MssqlVirtualMachine#log_settings}
        :param system_db_on_data_disk_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_db_on_data_disk_enabled MssqlVirtualMachine#system_db_on_data_disk_enabled}.
        :param temp_db_settings: temp_db_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#temp_db_settings MssqlVirtualMachine#temp_db_settings}
        '''
        value = MssqlVirtualMachineStorageConfiguration(
            disk_type=disk_type,
            storage_workload_type=storage_workload_type,
            data_settings=data_settings,
            log_settings=log_settings,
            system_db_on_data_disk_enabled=system_db_on_data_disk_enabled,
            temp_db_settings=temp_db_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putStorageConfiguration", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#create MssqlVirtualMachine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#delete MssqlVirtualMachine#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#read MssqlVirtualMachine#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#update MssqlVirtualMachine#update}.
        '''
        value = MssqlVirtualMachineTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWsfcDomainCredential")
    def put_wsfc_domain_credential(
        self,
        *,
        cluster_bootstrap_account_password: builtins.str,
        cluster_operator_account_password: builtins.str,
        sql_service_account_password: builtins.str,
    ) -> None:
        '''
        :param cluster_bootstrap_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_bootstrap_account_password MssqlVirtualMachine#cluster_bootstrap_account_password}.
        :param cluster_operator_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_operator_account_password MssqlVirtualMachine#cluster_operator_account_password}.
        :param sql_service_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_service_account_password MssqlVirtualMachine#sql_service_account_password}.
        '''
        value = MssqlVirtualMachineWsfcDomainCredential(
            cluster_bootstrap_account_password=cluster_bootstrap_account_password,
            cluster_operator_account_password=cluster_operator_account_password,
            sql_service_account_password=sql_service_account_password,
        )

        return typing.cast(None, jsii.invoke(self, "putWsfcDomainCredential", [value]))

    @jsii.member(jsii_name="resetAssessment")
    def reset_assessment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssessment", []))

    @jsii.member(jsii_name="resetAutoBackup")
    def reset_auto_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoBackup", []))

    @jsii.member(jsii_name="resetAutoPatching")
    def reset_auto_patching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPatching", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyVaultCredential")
    def reset_key_vault_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultCredential", []))

    @jsii.member(jsii_name="resetRServicesEnabled")
    def reset_r_services_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRServicesEnabled", []))

    @jsii.member(jsii_name="resetSqlConnectivityPort")
    def reset_sql_connectivity_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlConnectivityPort", []))

    @jsii.member(jsii_name="resetSqlConnectivityType")
    def reset_sql_connectivity_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlConnectivityType", []))

    @jsii.member(jsii_name="resetSqlConnectivityUpdatePassword")
    def reset_sql_connectivity_update_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlConnectivityUpdatePassword", []))

    @jsii.member(jsii_name="resetSqlConnectivityUpdateUsername")
    def reset_sql_connectivity_update_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlConnectivityUpdateUsername", []))

    @jsii.member(jsii_name="resetSqlInstance")
    def reset_sql_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlInstance", []))

    @jsii.member(jsii_name="resetSqlLicenseType")
    def reset_sql_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlLicenseType", []))

    @jsii.member(jsii_name="resetSqlVirtualMachineGroupId")
    def reset_sql_virtual_machine_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlVirtualMachineGroupId", []))

    @jsii.member(jsii_name="resetStorageConfiguration")
    def reset_storage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWsfcDomainCredential")
    def reset_wsfc_domain_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWsfcDomainCredential", []))

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
    @jsii.member(jsii_name="assessment")
    def assessment(self) -> "MssqlVirtualMachineAssessmentOutputReference":
        return typing.cast("MssqlVirtualMachineAssessmentOutputReference", jsii.get(self, "assessment"))

    @builtins.property
    @jsii.member(jsii_name="autoBackup")
    def auto_backup(self) -> "MssqlVirtualMachineAutoBackupOutputReference":
        return typing.cast("MssqlVirtualMachineAutoBackupOutputReference", jsii.get(self, "autoBackup"))

    @builtins.property
    @jsii.member(jsii_name="autoPatching")
    def auto_patching(self) -> "MssqlVirtualMachineAutoPatchingOutputReference":
        return typing.cast("MssqlVirtualMachineAutoPatchingOutputReference", jsii.get(self, "autoPatching"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCredential")
    def key_vault_credential(
        self,
    ) -> "MssqlVirtualMachineKeyVaultCredentialOutputReference":
        return typing.cast("MssqlVirtualMachineKeyVaultCredentialOutputReference", jsii.get(self, "keyVaultCredential"))

    @builtins.property
    @jsii.member(jsii_name="sqlInstance")
    def sql_instance(self) -> "MssqlVirtualMachineSqlInstanceOutputReference":
        return typing.cast("MssqlVirtualMachineSqlInstanceOutputReference", jsii.get(self, "sqlInstance"))

    @builtins.property
    @jsii.member(jsii_name="storageConfiguration")
    def storage_configuration(
        self,
    ) -> "MssqlVirtualMachineStorageConfigurationOutputReference":
        return typing.cast("MssqlVirtualMachineStorageConfigurationOutputReference", jsii.get(self, "storageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MssqlVirtualMachineTimeoutsOutputReference":
        return typing.cast("MssqlVirtualMachineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="wsfcDomainCredential")
    def wsfc_domain_credential(
        self,
    ) -> "MssqlVirtualMachineWsfcDomainCredentialOutputReference":
        return typing.cast("MssqlVirtualMachineWsfcDomainCredentialOutputReference", jsii.get(self, "wsfcDomainCredential"))

    @builtins.property
    @jsii.member(jsii_name="assessmentInput")
    def assessment_input(self) -> typing.Optional["MssqlVirtualMachineAssessment"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineAssessment"], jsii.get(self, "assessmentInput"))

    @builtins.property
    @jsii.member(jsii_name="autoBackupInput")
    def auto_backup_input(self) -> typing.Optional["MssqlVirtualMachineAutoBackup"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineAutoBackup"], jsii.get(self, "autoBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="autoPatchingInput")
    def auto_patching_input(self) -> typing.Optional["MssqlVirtualMachineAutoPatching"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineAutoPatching"], jsii.get(self, "autoPatchingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultCredentialInput")
    def key_vault_credential_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineKeyVaultCredential"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineKeyVaultCredential"], jsii.get(self, "keyVaultCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="rServicesEnabledInput")
    def r_services_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rServicesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityPortInput")
    def sql_connectivity_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sqlConnectivityPortInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityTypeInput")
    def sql_connectivity_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlConnectivityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityUpdatePasswordInput")
    def sql_connectivity_update_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlConnectivityUpdatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityUpdateUsernameInput")
    def sql_connectivity_update_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlConnectivityUpdateUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInstanceInput")
    def sql_instance_input(self) -> typing.Optional["MssqlVirtualMachineSqlInstance"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineSqlInstance"], jsii.get(self, "sqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlLicenseTypeInput")
    def sql_license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlLicenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineGroupIdInput")
    def sql_virtual_machine_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlVirtualMachineGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageConfigurationInput")
    def storage_configuration_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfiguration"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfiguration"], jsii.get(self, "storageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlVirtualMachineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachineIdInput")
    def virtual_machine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMachineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="wsfcDomainCredentialInput")
    def wsfc_domain_credential_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineWsfcDomainCredential"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineWsfcDomainCredential"], jsii.get(self, "wsfcDomainCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdfbb6b572a71ff78faf6a74e27d9357fb600fe0703de701d485c47f3505331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rServicesEnabled")
    def r_services_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rServicesEnabled"))

    @r_services_enabled.setter
    def r_services_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f2d5dce46cf00e1359343958c82900c901f0eeb7acc29099caee3e4fed611e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rServicesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityPort")
    def sql_connectivity_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sqlConnectivityPort"))

    @sql_connectivity_port.setter
    def sql_connectivity_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc928ad140e541f75df20d4a037f9a7382c9932ef32a8aa073ba0256ef109758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlConnectivityPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityType")
    def sql_connectivity_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlConnectivityType"))

    @sql_connectivity_type.setter
    def sql_connectivity_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd9146600e12fadb26f7c481632d6f7a5ddac6d86b6f51cdc503958515d49e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlConnectivityType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityUpdatePassword")
    def sql_connectivity_update_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlConnectivityUpdatePassword"))

    @sql_connectivity_update_password.setter
    def sql_connectivity_update_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63610aedebe74fd52536615cab066e7294608cac457459b1a6d0959dacabb3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlConnectivityUpdatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlConnectivityUpdateUsername")
    def sql_connectivity_update_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlConnectivityUpdateUsername"))

    @sql_connectivity_update_username.setter
    def sql_connectivity_update_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b51d4bd929d76b96336e09f320edb61d065530e4e3310ba133e3989b32cdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlConnectivityUpdateUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlLicenseType")
    def sql_license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlLicenseType"))

    @sql_license_type.setter
    def sql_license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ae2b9ada029b6acae7250e84c29966f0b32626d218054cfdd3f8fa026eb49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlLicenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlVirtualMachineGroupId")
    def sql_virtual_machine_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlVirtualMachineGroupId"))

    @sql_virtual_machine_group_id.setter
    def sql_virtual_machine_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16de0ccd44bf288d5c1d38f61d3f371a7cf009966db9aa28163faa348987eb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlVirtualMachineGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f1ec5c83bb86c8db7c7509e1cddb5ace6edc93418446627e2092e4dd9feda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualMachineId")
    def virtual_machine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualMachineId"))

    @virtual_machine_id.setter
    def virtual_machine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905fb0f639e1a808d8e4c0108c89be64bcdf800868aee744791e54bdfe8b443f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMachineId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAssessment",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "run_immediately": "runImmediately",
        "schedule": "schedule",
    },
)
class MssqlVirtualMachineAssessment:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        run_immediately: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedule: typing.Optional[typing.Union["MssqlVirtualMachineAssessmentSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#enabled MssqlVirtualMachine#enabled}.
        :param run_immediately: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#run_immediately MssqlVirtualMachine#run_immediately}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#schedule MssqlVirtualMachine#schedule}
        '''
        if isinstance(schedule, dict):
            schedule = MssqlVirtualMachineAssessmentSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3d787f9e113f33854596b4a1ef33bfae0a6356e31a51f16c7bea237d385d08)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument run_immediately", value=run_immediately, expected_type=type_hints["run_immediately"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if run_immediately is not None:
            self._values["run_immediately"] = run_immediately
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#enabled MssqlVirtualMachine#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def run_immediately(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#run_immediately MssqlVirtualMachine#run_immediately}.'''
        result = self._values.get("run_immediately")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def schedule(self) -> typing.Optional["MssqlVirtualMachineAssessmentSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#schedule MssqlVirtualMachine#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["MssqlVirtualMachineAssessmentSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAssessment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAssessmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAssessmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52a73f94be47079cb580722e84e639d54635fcac492bad3a854f7d23c7e1a88c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        day_of_week: builtins.str,
        start_time: builtins.str,
        monthly_occurrence: typing.Optional[jsii.Number] = None,
        weekly_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#start_time MssqlVirtualMachine#start_time}.
        :param monthly_occurrence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#monthly_occurrence MssqlVirtualMachine#monthly_occurrence}.
        :param weekly_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#weekly_interval MssqlVirtualMachine#weekly_interval}.
        '''
        value = MssqlVirtualMachineAssessmentSchedule(
            day_of_week=day_of_week,
            start_time=start_time,
            monthly_occurrence=monthly_occurrence,
            weekly_interval=weekly_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetRunImmediately")
    def reset_run_immediately(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunImmediately", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "MssqlVirtualMachineAssessmentScheduleOutputReference":
        return typing.cast("MssqlVirtualMachineAssessmentScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="runImmediatelyInput")
    def run_immediately_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runImmediatelyInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineAssessmentSchedule"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineAssessmentSchedule"], jsii.get(self, "scheduleInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f107d0e08a01728ac6e6aad87ccb79de3457057bbcbe985d07193d40cad2e51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runImmediately")
    def run_immediately(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runImmediately"))

    @run_immediately.setter
    def run_immediately(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70075df0f441d5fc08eba5fe33fce4c2d5816b099b05b359684d3cd28c521878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runImmediately", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineAssessment]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAssessment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAssessment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9010001f0cea37f041ecfba876cf7e235a9fb0ce6efd4c56717e374d5b21f69b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAssessmentSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "start_time": "startTime",
        "monthly_occurrence": "monthlyOccurrence",
        "weekly_interval": "weeklyInterval",
    },
)
class MssqlVirtualMachineAssessmentSchedule:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        start_time: builtins.str,
        monthly_occurrence: typing.Optional[jsii.Number] = None,
        weekly_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#start_time MssqlVirtualMachine#start_time}.
        :param monthly_occurrence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#monthly_occurrence MssqlVirtualMachine#monthly_occurrence}.
        :param weekly_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#weekly_interval MssqlVirtualMachine#weekly_interval}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65966c353a81ffdfc4190aa5ae0ad183cb92724c40bea3fcf92292058066f911)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument monthly_occurrence", value=monthly_occurrence, expected_type=type_hints["monthly_occurrence"])
            check_type(argname="argument weekly_interval", value=weekly_interval, expected_type=type_hints["weekly_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "start_time": start_time,
        }
        if monthly_occurrence is not None:
            self._values["monthly_occurrence"] = monthly_occurrence
        if weekly_interval is not None:
            self._values["weekly_interval"] = weekly_interval

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.'''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#start_time MssqlVirtualMachine#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monthly_occurrence(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#monthly_occurrence MssqlVirtualMachine#monthly_occurrence}.'''
        result = self._values.get("monthly_occurrence")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weekly_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#weekly_interval MssqlVirtualMachine#weekly_interval}.'''
        result = self._values.get("weekly_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAssessmentSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAssessmentScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAssessmentScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a43e0b6daa46bf9e2b5d7917b6bfffb02fca27b02c40ca609988dca3164a7fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMonthlyOccurrence")
    def reset_monthly_occurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlyOccurrence", []))

    @jsii.member(jsii_name="resetWeeklyInterval")
    def reset_weekly_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyInterval", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyOccurrenceInput")
    def monthly_occurrence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthlyOccurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyIntervalInput")
    def weekly_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weeklyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755088e15082401f9936faa3c8c3454ef9ad3183ac3bb5801692bed0860d8bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthlyOccurrence")
    def monthly_occurrence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monthlyOccurrence"))

    @monthly_occurrence.setter
    def monthly_occurrence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0a29d8aa72917e45b5cba921e9b1540fa4fca5a78a05947a6cf83b5ecd824fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlyOccurrence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711918cb01b6d518164d861e5029d0f7e0671efbb599ac8ddaaa42e010ef5522)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklyInterval")
    def weekly_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weeklyInterval"))

    @weekly_interval.setter
    def weekly_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353f877484f6fcd98eeff6a477f391d003084675f8e6c4259b4216db6c3c1483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklyInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineAssessmentSchedule]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAssessmentSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAssessmentSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c58950e0c9bf1e81f2c1c707133d8e8a2ee4141c611984f85800b24aa591ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoBackup",
    jsii_struct_bases=[],
    name_mapping={
        "retention_period_in_days": "retentionPeriodInDays",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_blob_endpoint": "storageBlobEndpoint",
        "encryption_enabled": "encryptionEnabled",
        "encryption_password": "encryptionPassword",
        "manual_schedule": "manualSchedule",
        "system_databases_backup_enabled": "systemDatabasesBackupEnabled",
    },
)
class MssqlVirtualMachineAutoBackup:
    def __init__(
        self,
        *,
        retention_period_in_days: jsii.Number,
        storage_account_access_key: builtins.str,
        storage_blob_endpoint: builtins.str,
        encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encryption_password: typing.Optional[builtins.str] = None,
        manual_schedule: typing.Optional[typing.Union["MssqlVirtualMachineAutoBackupManualSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        system_databases_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param retention_period_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#retention_period_in_days MssqlVirtualMachine#retention_period_in_days}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_account_access_key MssqlVirtualMachine#storage_account_access_key}.
        :param storage_blob_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_blob_endpoint MssqlVirtualMachine#storage_blob_endpoint}.
        :param encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_enabled MssqlVirtualMachine#encryption_enabled}.
        :param encryption_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_password MssqlVirtualMachine#encryption_password}.
        :param manual_schedule: manual_schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#manual_schedule MssqlVirtualMachine#manual_schedule}
        :param system_databases_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_databases_backup_enabled MssqlVirtualMachine#system_databases_backup_enabled}.
        '''
        if isinstance(manual_schedule, dict):
            manual_schedule = MssqlVirtualMachineAutoBackupManualSchedule(**manual_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c7f8d0aa819ef18ce404a48227109b56b062bf29d20aeba2c4f0626e4a09d6)
            check_type(argname="argument retention_period_in_days", value=retention_period_in_days, expected_type=type_hints["retention_period_in_days"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_blob_endpoint", value=storage_blob_endpoint, expected_type=type_hints["storage_blob_endpoint"])
            check_type(argname="argument encryption_enabled", value=encryption_enabled, expected_type=type_hints["encryption_enabled"])
            check_type(argname="argument encryption_password", value=encryption_password, expected_type=type_hints["encryption_password"])
            check_type(argname="argument manual_schedule", value=manual_schedule, expected_type=type_hints["manual_schedule"])
            check_type(argname="argument system_databases_backup_enabled", value=system_databases_backup_enabled, expected_type=type_hints["system_databases_backup_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_period_in_days": retention_period_in_days,
            "storage_account_access_key": storage_account_access_key,
            "storage_blob_endpoint": storage_blob_endpoint,
        }
        if encryption_enabled is not None:
            self._values["encryption_enabled"] = encryption_enabled
        if encryption_password is not None:
            self._values["encryption_password"] = encryption_password
        if manual_schedule is not None:
            self._values["manual_schedule"] = manual_schedule
        if system_databases_backup_enabled is not None:
            self._values["system_databases_backup_enabled"] = system_databases_backup_enabled

    @builtins.property
    def retention_period_in_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#retention_period_in_days MssqlVirtualMachine#retention_period_in_days}.'''
        result = self._values.get("retention_period_in_days")
        assert result is not None, "Required property 'retention_period_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage_account_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_account_access_key MssqlVirtualMachine#storage_account_access_key}.'''
        result = self._values.get("storage_account_access_key")
        assert result is not None, "Required property 'storage_account_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_blob_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_blob_endpoint MssqlVirtualMachine#storage_blob_endpoint}.'''
        result = self._values.get("storage_blob_endpoint")
        assert result is not None, "Required property 'storage_blob_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_enabled MssqlVirtualMachine#encryption_enabled}.'''
        result = self._values.get("encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encryption_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#encryption_password MssqlVirtualMachine#encryption_password}.'''
        result = self._values.get("encryption_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_schedule(
        self,
    ) -> typing.Optional["MssqlVirtualMachineAutoBackupManualSchedule"]:
        '''manual_schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#manual_schedule MssqlVirtualMachine#manual_schedule}
        '''
        result = self._values.get("manual_schedule")
        return typing.cast(typing.Optional["MssqlVirtualMachineAutoBackupManualSchedule"], result)

    @builtins.property
    def system_databases_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_databases_backup_enabled MssqlVirtualMachine#system_databases_backup_enabled}.'''
        result = self._values.get("system_databases_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAutoBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoBackupManualSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "full_backup_frequency": "fullBackupFrequency",
        "full_backup_start_hour": "fullBackupStartHour",
        "full_backup_window_in_hours": "fullBackupWindowInHours",
        "log_backup_frequency_in_minutes": "logBackupFrequencyInMinutes",
        "days_of_week": "daysOfWeek",
    },
)
class MssqlVirtualMachineAutoBackupManualSchedule:
    def __init__(
        self,
        *,
        full_backup_frequency: builtins.str,
        full_backup_start_hour: jsii.Number,
        full_backup_window_in_hours: jsii.Number,
        log_backup_frequency_in_minutes: jsii.Number,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param full_backup_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_frequency MssqlVirtualMachine#full_backup_frequency}.
        :param full_backup_start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_start_hour MssqlVirtualMachine#full_backup_start_hour}.
        :param full_backup_window_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_window_in_hours MssqlVirtualMachine#full_backup_window_in_hours}.
        :param log_backup_frequency_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_backup_frequency_in_minutes MssqlVirtualMachine#log_backup_frequency_in_minutes}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#days_of_week MssqlVirtualMachine#days_of_week}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c914c25666720764b4c7f8ffbd32c3b3f4e2151532700aa46da22a302ac8d4b3)
            check_type(argname="argument full_backup_frequency", value=full_backup_frequency, expected_type=type_hints["full_backup_frequency"])
            check_type(argname="argument full_backup_start_hour", value=full_backup_start_hour, expected_type=type_hints["full_backup_start_hour"])
            check_type(argname="argument full_backup_window_in_hours", value=full_backup_window_in_hours, expected_type=type_hints["full_backup_window_in_hours"])
            check_type(argname="argument log_backup_frequency_in_minutes", value=log_backup_frequency_in_minutes, expected_type=type_hints["log_backup_frequency_in_minutes"])
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "full_backup_frequency": full_backup_frequency,
            "full_backup_start_hour": full_backup_start_hour,
            "full_backup_window_in_hours": full_backup_window_in_hours,
            "log_backup_frequency_in_minutes": log_backup_frequency_in_minutes,
        }
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week

    @builtins.property
    def full_backup_frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_frequency MssqlVirtualMachine#full_backup_frequency}.'''
        result = self._values.get("full_backup_frequency")
        assert result is not None, "Required property 'full_backup_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def full_backup_start_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_start_hour MssqlVirtualMachine#full_backup_start_hour}.'''
        result = self._values.get("full_backup_start_hour")
        assert result is not None, "Required property 'full_backup_start_hour' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def full_backup_window_in_hours(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_window_in_hours MssqlVirtualMachine#full_backup_window_in_hours}.'''
        result = self._values.get("full_backup_window_in_hours")
        assert result is not None, "Required property 'full_backup_window_in_hours' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def log_backup_frequency_in_minutes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_backup_frequency_in_minutes MssqlVirtualMachine#log_backup_frequency_in_minutes}.'''
        result = self._values.get("log_backup_frequency_in_minutes")
        assert result is not None, "Required property 'log_backup_frequency_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#days_of_week MssqlVirtualMachine#days_of_week}.'''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAutoBackupManualSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAutoBackupManualScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoBackupManualScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed3a64eb938adbe50649fffb2c397fe60cbd543c83d052c5550ebae001351a0)
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
    @jsii.member(jsii_name="fullBackupFrequencyInput")
    def full_backup_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullBackupFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupStartHourInput")
    def full_backup_start_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fullBackupStartHourInput"))

    @builtins.property
    @jsii.member(jsii_name="fullBackupWindowInHoursInput")
    def full_backup_window_in_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fullBackupWindowInHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="logBackupFrequencyInMinutesInput")
    def log_backup_frequency_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logBackupFrequencyInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83639ee816361388b8d04ec4b3798ea8bcc2a377e3a92a0a7203a32c41c2108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullBackupFrequency")
    def full_backup_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullBackupFrequency"))

    @full_backup_frequency.setter
    def full_backup_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83a5c022cdb579095ccfe47f7964aaa59ac748e75ad9881a018f0215390a659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullBackupFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullBackupStartHour")
    def full_backup_start_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fullBackupStartHour"))

    @full_backup_start_hour.setter
    def full_backup_start_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7bf715930c8b54c792a42fc01c90a5e42d33b41893c117743b971703bc1e2a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullBackupStartHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fullBackupWindowInHours")
    def full_backup_window_in_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fullBackupWindowInHours"))

    @full_backup_window_in_hours.setter
    def full_backup_window_in_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85c570c5a0827587a8f7e6319c36ef12db5f892912e6667f0b41cd08d559236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullBackupWindowInHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logBackupFrequencyInMinutes")
    def log_backup_frequency_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logBackupFrequencyInMinutes"))

    @log_backup_frequency_in_minutes.setter
    def log_backup_frequency_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ab94fbeb2739641f86d23b2730934f68f8f90d23891f554c892da47a5c9ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logBackupFrequencyInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046fbbe8657c1dcff3c1d9751481f670576f87223412490e8b6f57c7f782983b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MssqlVirtualMachineAutoBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda49876c65724f561edfc4948a4168ea6f24f9c1be0a628216b1ae30a6f41b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManualSchedule")
    def put_manual_schedule(
        self,
        *,
        full_backup_frequency: builtins.str,
        full_backup_start_hour: jsii.Number,
        full_backup_window_in_hours: jsii.Number,
        log_backup_frequency_in_minutes: jsii.Number,
        days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param full_backup_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_frequency MssqlVirtualMachine#full_backup_frequency}.
        :param full_backup_start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_start_hour MssqlVirtualMachine#full_backup_start_hour}.
        :param full_backup_window_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#full_backup_window_in_hours MssqlVirtualMachine#full_backup_window_in_hours}.
        :param log_backup_frequency_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_backup_frequency_in_minutes MssqlVirtualMachine#log_backup_frequency_in_minutes}.
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#days_of_week MssqlVirtualMachine#days_of_week}.
        '''
        value = MssqlVirtualMachineAutoBackupManualSchedule(
            full_backup_frequency=full_backup_frequency,
            full_backup_start_hour=full_backup_start_hour,
            full_backup_window_in_hours=full_backup_window_in_hours,
            log_backup_frequency_in_minutes=log_backup_frequency_in_minutes,
            days_of_week=days_of_week,
        )

        return typing.cast(None, jsii.invoke(self, "putManualSchedule", [value]))

    @jsii.member(jsii_name="resetEncryptionEnabled")
    def reset_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionEnabled", []))

    @jsii.member(jsii_name="resetEncryptionPassword")
    def reset_encryption_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionPassword", []))

    @jsii.member(jsii_name="resetManualSchedule")
    def reset_manual_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualSchedule", []))

    @jsii.member(jsii_name="resetSystemDatabasesBackupEnabled")
    def reset_system_databases_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDatabasesBackupEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="manualSchedule")
    def manual_schedule(
        self,
    ) -> MssqlVirtualMachineAutoBackupManualScheduleOutputReference:
        return typing.cast(MssqlVirtualMachineAutoBackupManualScheduleOutputReference, jsii.get(self, "manualSchedule"))

    @builtins.property
    @jsii.member(jsii_name="encryptionEnabledInput")
    def encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionPasswordInput")
    def encryption_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="manualScheduleInput")
    def manual_schedule_input(
        self,
    ) -> typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule], jsii.get(self, "manualScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInDaysInput")
    def retention_period_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKeyInput")
    def storage_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageBlobEndpointInput")
    def storage_blob_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageBlobEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDatabasesBackupEnabledInput")
    def system_databases_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemDatabasesBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionEnabled")
    def encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptionEnabled"))

    @encryption_enabled.setter
    def encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccd15811f8751e294fba545c3fb5d82ad2da52b6a21cd2282658d51238967ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionPassword")
    def encryption_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionPassword"))

    @encryption_password.setter
    def encryption_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a9f70218c76cabd878d30ff4ca0d977dac5dd6dabdc528f5cdf619d29cd3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodInDays")
    def retention_period_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodInDays"))

    @retention_period_in_days.setter
    def retention_period_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a16ea496f7ba6dc701eb0e200430656b75b463e242d12492b0f369d5af11f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1633a6b63b11230183af55d1029805301563be7e60b9eeda1766fb5aa038826c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageBlobEndpoint")
    def storage_blob_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageBlobEndpoint"))

    @storage_blob_endpoint.setter
    def storage_blob_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3ae520f169c9f802acc85ecf5633e206168aa7402957e1449a8a992596fe7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageBlobEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDatabasesBackupEnabled")
    def system_databases_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "systemDatabasesBackupEnabled"))

    @system_databases_backup_enabled.setter
    def system_databases_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4385fd85a454abfa7985ef0c480c42314b9b57b2ef68f1144af939c0442b324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDatabasesBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineAutoBackup]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAutoBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8f26b16ef256dd5503a4e2a2f8be87bcca14edde644f5bd0814eaa82d5d4ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoPatching",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "maintenance_window_duration_in_minutes": "maintenanceWindowDurationInMinutes",
        "maintenance_window_starting_hour": "maintenanceWindowStartingHour",
    },
)
class MssqlVirtualMachineAutoPatching:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        maintenance_window_duration_in_minutes: jsii.Number,
        maintenance_window_starting_hour: jsii.Number,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.
        :param maintenance_window_duration_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_duration_in_minutes MssqlVirtualMachine#maintenance_window_duration_in_minutes}.
        :param maintenance_window_starting_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_starting_hour MssqlVirtualMachine#maintenance_window_starting_hour}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253d0b3eaf9033787fc78918e8baf57f9918729e7aa465f1bc7e9817dd03da3f)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument maintenance_window_duration_in_minutes", value=maintenance_window_duration_in_minutes, expected_type=type_hints["maintenance_window_duration_in_minutes"])
            check_type(argname="argument maintenance_window_starting_hour", value=maintenance_window_starting_hour, expected_type=type_hints["maintenance_window_starting_hour"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "maintenance_window_duration_in_minutes": maintenance_window_duration_in_minutes,
            "maintenance_window_starting_hour": maintenance_window_starting_hour,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#day_of_week MssqlVirtualMachine#day_of_week}.'''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_window_duration_in_minutes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_duration_in_minutes MssqlVirtualMachine#maintenance_window_duration_in_minutes}.'''
        result = self._values.get("maintenance_window_duration_in_minutes")
        assert result is not None, "Required property 'maintenance_window_duration_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def maintenance_window_starting_hour(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#maintenance_window_starting_hour MssqlVirtualMachine#maintenance_window_starting_hour}.'''
        result = self._values.get("maintenance_window_starting_hour")
        assert result is not None, "Required property 'maintenance_window_starting_hour' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineAutoPatching(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineAutoPatchingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineAutoPatchingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc387a59fc87b60550a7259e73f0b0daa6bbd024850bf82b1a934b9251d5a767)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDurationInMinutesInput")
    def maintenance_window_duration_in_minutes_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maintenanceWindowDurationInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowStartingHourInput")
    def maintenance_window_starting_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maintenanceWindowStartingHourInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62da7df436f33922aac67439f1e2892e51db13786c5861afb58270c348bf798c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDurationInMinutes")
    def maintenance_window_duration_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maintenanceWindowDurationInMinutes"))

    @maintenance_window_duration_in_minutes.setter
    def maintenance_window_duration_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f64ce2831a3c80ae7257fe7d0af4157f4aef3ed19baa8df43927b66a49ac91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowDurationInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowStartingHour")
    def maintenance_window_starting_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maintenanceWindowStartingHour"))

    @maintenance_window_starting_hour.setter
    def maintenance_window_starting_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eaa296617755e7b2fb90f169d47a41a09fc65423ba25a05d05298fb424654db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowStartingHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineAutoPatching]:
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoPatching], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineAutoPatching],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be012b61299b5582755caa8a9eaa7d5f9b1ae6453977631460abc926b4cb6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "virtual_machine_id": "virtualMachineId",
        "assessment": "assessment",
        "auto_backup": "autoBackup",
        "auto_patching": "autoPatching",
        "id": "id",
        "key_vault_credential": "keyVaultCredential",
        "r_services_enabled": "rServicesEnabled",
        "sql_connectivity_port": "sqlConnectivityPort",
        "sql_connectivity_type": "sqlConnectivityType",
        "sql_connectivity_update_password": "sqlConnectivityUpdatePassword",
        "sql_connectivity_update_username": "sqlConnectivityUpdateUsername",
        "sql_instance": "sqlInstance",
        "sql_license_type": "sqlLicenseType",
        "sql_virtual_machine_group_id": "sqlVirtualMachineGroupId",
        "storage_configuration": "storageConfiguration",
        "tags": "tags",
        "timeouts": "timeouts",
        "wsfc_domain_credential": "wsfcDomainCredential",
    },
)
class MssqlVirtualMachineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        virtual_machine_id: builtins.str,
        assessment: typing.Optional[typing.Union[MssqlVirtualMachineAssessment, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_backup: typing.Optional[typing.Union[MssqlVirtualMachineAutoBackup, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_patching: typing.Optional[typing.Union[MssqlVirtualMachineAutoPatching, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key_vault_credential: typing.Optional[typing.Union["MssqlVirtualMachineKeyVaultCredential", typing.Dict[builtins.str, typing.Any]]] = None,
        r_services_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sql_connectivity_port: typing.Optional[jsii.Number] = None,
        sql_connectivity_type: typing.Optional[builtins.str] = None,
        sql_connectivity_update_password: typing.Optional[builtins.str] = None,
        sql_connectivity_update_username: typing.Optional[builtins.str] = None,
        sql_instance: typing.Optional[typing.Union["MssqlVirtualMachineSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_license_type: typing.Optional[builtins.str] = None,
        sql_virtual_machine_group_id: typing.Optional[builtins.str] = None,
        storage_configuration: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MssqlVirtualMachineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        wsfc_domain_credential: typing.Optional[typing.Union["MssqlVirtualMachineWsfcDomainCredential", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param virtual_machine_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#virtual_machine_id MssqlVirtualMachine#virtual_machine_id}.
        :param assessment: assessment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#assessment MssqlVirtualMachine#assessment}
        :param auto_backup: auto_backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_backup MssqlVirtualMachine#auto_backup}
        :param auto_patching: auto_patching block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_patching MssqlVirtualMachine#auto_patching}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#id MssqlVirtualMachine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_vault_credential: key_vault_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_credential MssqlVirtualMachine#key_vault_credential}
        :param r_services_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#r_services_enabled MssqlVirtualMachine#r_services_enabled}.
        :param sql_connectivity_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_port MssqlVirtualMachine#sql_connectivity_port}.
        :param sql_connectivity_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_type MssqlVirtualMachine#sql_connectivity_type}.
        :param sql_connectivity_update_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_password MssqlVirtualMachine#sql_connectivity_update_password}.
        :param sql_connectivity_update_username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_username MssqlVirtualMachine#sql_connectivity_update_username}.
        :param sql_instance: sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_instance MssqlVirtualMachine#sql_instance}
        :param sql_license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_license_type MssqlVirtualMachine#sql_license_type}.
        :param sql_virtual_machine_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_virtual_machine_group_id MssqlVirtualMachine#sql_virtual_machine_group_id}.
        :param storage_configuration: storage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_configuration MssqlVirtualMachine#storage_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#tags MssqlVirtualMachine#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#timeouts MssqlVirtualMachine#timeouts}
        :param wsfc_domain_credential: wsfc_domain_credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#wsfc_domain_credential MssqlVirtualMachine#wsfc_domain_credential}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(assessment, dict):
            assessment = MssqlVirtualMachineAssessment(**assessment)
        if isinstance(auto_backup, dict):
            auto_backup = MssqlVirtualMachineAutoBackup(**auto_backup)
        if isinstance(auto_patching, dict):
            auto_patching = MssqlVirtualMachineAutoPatching(**auto_patching)
        if isinstance(key_vault_credential, dict):
            key_vault_credential = MssqlVirtualMachineKeyVaultCredential(**key_vault_credential)
        if isinstance(sql_instance, dict):
            sql_instance = MssqlVirtualMachineSqlInstance(**sql_instance)
        if isinstance(storage_configuration, dict):
            storage_configuration = MssqlVirtualMachineStorageConfiguration(**storage_configuration)
        if isinstance(timeouts, dict):
            timeouts = MssqlVirtualMachineTimeouts(**timeouts)
        if isinstance(wsfc_domain_credential, dict):
            wsfc_domain_credential = MssqlVirtualMachineWsfcDomainCredential(**wsfc_domain_credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d912e43980043aaffa1740f7100f2ffd8c98a028a259a588cc483118efffd0b7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument virtual_machine_id", value=virtual_machine_id, expected_type=type_hints["virtual_machine_id"])
            check_type(argname="argument assessment", value=assessment, expected_type=type_hints["assessment"])
            check_type(argname="argument auto_backup", value=auto_backup, expected_type=type_hints["auto_backup"])
            check_type(argname="argument auto_patching", value=auto_patching, expected_type=type_hints["auto_patching"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_vault_credential", value=key_vault_credential, expected_type=type_hints["key_vault_credential"])
            check_type(argname="argument r_services_enabled", value=r_services_enabled, expected_type=type_hints["r_services_enabled"])
            check_type(argname="argument sql_connectivity_port", value=sql_connectivity_port, expected_type=type_hints["sql_connectivity_port"])
            check_type(argname="argument sql_connectivity_type", value=sql_connectivity_type, expected_type=type_hints["sql_connectivity_type"])
            check_type(argname="argument sql_connectivity_update_password", value=sql_connectivity_update_password, expected_type=type_hints["sql_connectivity_update_password"])
            check_type(argname="argument sql_connectivity_update_username", value=sql_connectivity_update_username, expected_type=type_hints["sql_connectivity_update_username"])
            check_type(argname="argument sql_instance", value=sql_instance, expected_type=type_hints["sql_instance"])
            check_type(argname="argument sql_license_type", value=sql_license_type, expected_type=type_hints["sql_license_type"])
            check_type(argname="argument sql_virtual_machine_group_id", value=sql_virtual_machine_group_id, expected_type=type_hints["sql_virtual_machine_group_id"])
            check_type(argname="argument storage_configuration", value=storage_configuration, expected_type=type_hints["storage_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument wsfc_domain_credential", value=wsfc_domain_credential, expected_type=type_hints["wsfc_domain_credential"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "virtual_machine_id": virtual_machine_id,
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
        if assessment is not None:
            self._values["assessment"] = assessment
        if auto_backup is not None:
            self._values["auto_backup"] = auto_backup
        if auto_patching is not None:
            self._values["auto_patching"] = auto_patching
        if id is not None:
            self._values["id"] = id
        if key_vault_credential is not None:
            self._values["key_vault_credential"] = key_vault_credential
        if r_services_enabled is not None:
            self._values["r_services_enabled"] = r_services_enabled
        if sql_connectivity_port is not None:
            self._values["sql_connectivity_port"] = sql_connectivity_port
        if sql_connectivity_type is not None:
            self._values["sql_connectivity_type"] = sql_connectivity_type
        if sql_connectivity_update_password is not None:
            self._values["sql_connectivity_update_password"] = sql_connectivity_update_password
        if sql_connectivity_update_username is not None:
            self._values["sql_connectivity_update_username"] = sql_connectivity_update_username
        if sql_instance is not None:
            self._values["sql_instance"] = sql_instance
        if sql_license_type is not None:
            self._values["sql_license_type"] = sql_license_type
        if sql_virtual_machine_group_id is not None:
            self._values["sql_virtual_machine_group_id"] = sql_virtual_machine_group_id
        if storage_configuration is not None:
            self._values["storage_configuration"] = storage_configuration
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if wsfc_domain_credential is not None:
            self._values["wsfc_domain_credential"] = wsfc_domain_credential

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
    def virtual_machine_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#virtual_machine_id MssqlVirtualMachine#virtual_machine_id}.'''
        result = self._values.get("virtual_machine_id")
        assert result is not None, "Required property 'virtual_machine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assessment(self) -> typing.Optional[MssqlVirtualMachineAssessment]:
        '''assessment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#assessment MssqlVirtualMachine#assessment}
        '''
        result = self._values.get("assessment")
        return typing.cast(typing.Optional[MssqlVirtualMachineAssessment], result)

    @builtins.property
    def auto_backup(self) -> typing.Optional[MssqlVirtualMachineAutoBackup]:
        '''auto_backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_backup MssqlVirtualMachine#auto_backup}
        '''
        result = self._values.get("auto_backup")
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoBackup], result)

    @builtins.property
    def auto_patching(self) -> typing.Optional[MssqlVirtualMachineAutoPatching]:
        '''auto_patching block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#auto_patching MssqlVirtualMachine#auto_patching}
        '''
        result = self._values.get("auto_patching")
        return typing.cast(typing.Optional[MssqlVirtualMachineAutoPatching], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#id MssqlVirtualMachine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_credential(
        self,
    ) -> typing.Optional["MssqlVirtualMachineKeyVaultCredential"]:
        '''key_vault_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_credential MssqlVirtualMachine#key_vault_credential}
        '''
        result = self._values.get("key_vault_credential")
        return typing.cast(typing.Optional["MssqlVirtualMachineKeyVaultCredential"], result)

    @builtins.property
    def r_services_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#r_services_enabled MssqlVirtualMachine#r_services_enabled}.'''
        result = self._values.get("r_services_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sql_connectivity_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_port MssqlVirtualMachine#sql_connectivity_port}.'''
        result = self._values.get("sql_connectivity_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sql_connectivity_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_type MssqlVirtualMachine#sql_connectivity_type}.'''
        result = self._values.get("sql_connectivity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_connectivity_update_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_password MssqlVirtualMachine#sql_connectivity_update_password}.'''
        result = self._values.get("sql_connectivity_update_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_connectivity_update_username(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_connectivity_update_username MssqlVirtualMachine#sql_connectivity_update_username}.'''
        result = self._values.get("sql_connectivity_update_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_instance(self) -> typing.Optional["MssqlVirtualMachineSqlInstance"]:
        '''sql_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_instance MssqlVirtualMachine#sql_instance}
        '''
        result = self._values.get("sql_instance")
        return typing.cast(typing.Optional["MssqlVirtualMachineSqlInstance"], result)

    @builtins.property
    def sql_license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_license_type MssqlVirtualMachine#sql_license_type}.'''
        result = self._values.get("sql_license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_virtual_machine_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_virtual_machine_group_id MssqlVirtualMachine#sql_virtual_machine_group_id}.'''
        result = self._values.get("sql_virtual_machine_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_configuration(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfiguration"]:
        '''storage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_configuration MssqlVirtualMachine#storage_configuration}
        '''
        result = self._values.get("storage_configuration")
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#tags MssqlVirtualMachine#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MssqlVirtualMachineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#timeouts MssqlVirtualMachine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlVirtualMachineTimeouts"], result)

    @builtins.property
    def wsfc_domain_credential(
        self,
    ) -> typing.Optional["MssqlVirtualMachineWsfcDomainCredential"]:
        '''wsfc_domain_credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#wsfc_domain_credential MssqlVirtualMachine#wsfc_domain_credential}
        '''
        result = self._values.get("wsfc_domain_credential")
        return typing.cast(typing.Optional["MssqlVirtualMachineWsfcDomainCredential"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineKeyVaultCredential",
    jsii_struct_bases=[],
    name_mapping={
        "key_vault_url": "keyVaultUrl",
        "name": "name",
        "service_principal_name": "servicePrincipalName",
        "service_principal_secret": "servicePrincipalSecret",
    },
)
class MssqlVirtualMachineKeyVaultCredential:
    def __init__(
        self,
        *,
        key_vault_url: builtins.str,
        name: builtins.str,
        service_principal_name: builtins.str,
        service_principal_secret: builtins.str,
    ) -> None:
        '''
        :param key_vault_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_url MssqlVirtualMachine#key_vault_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#name MssqlVirtualMachine#name}.
        :param service_principal_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_name MssqlVirtualMachine#service_principal_name}.
        :param service_principal_secret: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_secret MssqlVirtualMachine#service_principal_secret}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5580dfb8359475a3bcf909ef1ca890849cbe3a6328b9ec12b349be0ecd64032f)
            check_type(argname="argument key_vault_url", value=key_vault_url, expected_type=type_hints["key_vault_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_principal_name", value=service_principal_name, expected_type=type_hints["service_principal_name"])
            check_type(argname="argument service_principal_secret", value=service_principal_secret, expected_type=type_hints["service_principal_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_vault_url": key_vault_url,
            "name": name,
            "service_principal_name": service_principal_name,
            "service_principal_secret": service_principal_secret,
        }

    @builtins.property
    def key_vault_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#key_vault_url MssqlVirtualMachine#key_vault_url}.'''
        result = self._values.get("key_vault_url")
        assert result is not None, "Required property 'key_vault_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#name MssqlVirtualMachine#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_principal_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_name MssqlVirtualMachine#service_principal_name}.'''
        result = self._values.get("service_principal_name")
        assert result is not None, "Required property 'service_principal_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_principal_secret(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#service_principal_secret MssqlVirtualMachine#service_principal_secret}.'''
        result = self._values.get("service_principal_secret")
        assert result is not None, "Required property 'service_principal_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineKeyVaultCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineKeyVaultCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineKeyVaultCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eaa50e70febb691bfa449feb048616fb267a68067e6d4146f6713ad8136410b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyVaultUrlInput")
    def key_vault_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalNameInput")
    def service_principal_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalNameInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalSecretInput")
    def service_principal_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultUrl")
    def key_vault_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultUrl"))

    @key_vault_url.setter
    def key_vault_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95aa817463759b675de42f4a0cfebebe239eb185d7aaf30be39fcc6657e6e5d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5296404075e9bad720be5e0a4735494176c1ff64bf626ffe2c9c57059bfb11c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalName")
    def service_principal_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalName"))

    @service_principal_name.setter
    def service_principal_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07999f471447b75b992d34a1a3e04b7aaa000367420783a8e3adecf954ae573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalSecret")
    def service_principal_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalSecret"))

    @service_principal_secret.setter
    def service_principal_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c81df2df9734e199692a628d7cbbc8107b90c2dbc00d0fd3a9765732fd94a5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineKeyVaultCredential]:
        return typing.cast(typing.Optional[MssqlVirtualMachineKeyVaultCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineKeyVaultCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e32ead818404413ed54318bd288d80ca4070676edf9ab2215d2775ae0e27c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineSqlInstance",
    jsii_struct_bases=[],
    name_mapping={
        "adhoc_workloads_optimization_enabled": "adhocWorkloadsOptimizationEnabled",
        "collation": "collation",
        "instant_file_initialization_enabled": "instantFileInitializationEnabled",
        "lock_pages_in_memory_enabled": "lockPagesInMemoryEnabled",
        "max_dop": "maxDop",
        "max_server_memory_mb": "maxServerMemoryMb",
        "min_server_memory_mb": "minServerMemoryMb",
    },
)
class MssqlVirtualMachineSqlInstance:
    def __init__(
        self,
        *,
        adhoc_workloads_optimization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        collation: typing.Optional[builtins.str] = None,
        instant_file_initialization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        lock_pages_in_memory_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_dop: typing.Optional[jsii.Number] = None,
        max_server_memory_mb: typing.Optional[jsii.Number] = None,
        min_server_memory_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param adhoc_workloads_optimization_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#adhoc_workloads_optimization_enabled MssqlVirtualMachine#adhoc_workloads_optimization_enabled}.
        :param collation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#collation MssqlVirtualMachine#collation}.
        :param instant_file_initialization_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#instant_file_initialization_enabled MssqlVirtualMachine#instant_file_initialization_enabled}.
        :param lock_pages_in_memory_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#lock_pages_in_memory_enabled MssqlVirtualMachine#lock_pages_in_memory_enabled}.
        :param max_dop: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_dop MssqlVirtualMachine#max_dop}.
        :param max_server_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_server_memory_mb MssqlVirtualMachine#max_server_memory_mb}.
        :param min_server_memory_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#min_server_memory_mb MssqlVirtualMachine#min_server_memory_mb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3ee2b8e52e16faef2fb6ec01e15f4e6debbff3e805e13dae2c78a16ed63ea0)
            check_type(argname="argument adhoc_workloads_optimization_enabled", value=adhoc_workloads_optimization_enabled, expected_type=type_hints["adhoc_workloads_optimization_enabled"])
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument instant_file_initialization_enabled", value=instant_file_initialization_enabled, expected_type=type_hints["instant_file_initialization_enabled"])
            check_type(argname="argument lock_pages_in_memory_enabled", value=lock_pages_in_memory_enabled, expected_type=type_hints["lock_pages_in_memory_enabled"])
            check_type(argname="argument max_dop", value=max_dop, expected_type=type_hints["max_dop"])
            check_type(argname="argument max_server_memory_mb", value=max_server_memory_mb, expected_type=type_hints["max_server_memory_mb"])
            check_type(argname="argument min_server_memory_mb", value=min_server_memory_mb, expected_type=type_hints["min_server_memory_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if adhoc_workloads_optimization_enabled is not None:
            self._values["adhoc_workloads_optimization_enabled"] = adhoc_workloads_optimization_enabled
        if collation is not None:
            self._values["collation"] = collation
        if instant_file_initialization_enabled is not None:
            self._values["instant_file_initialization_enabled"] = instant_file_initialization_enabled
        if lock_pages_in_memory_enabled is not None:
            self._values["lock_pages_in_memory_enabled"] = lock_pages_in_memory_enabled
        if max_dop is not None:
            self._values["max_dop"] = max_dop
        if max_server_memory_mb is not None:
            self._values["max_server_memory_mb"] = max_server_memory_mb
        if min_server_memory_mb is not None:
            self._values["min_server_memory_mb"] = min_server_memory_mb

    @builtins.property
    def adhoc_workloads_optimization_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#adhoc_workloads_optimization_enabled MssqlVirtualMachine#adhoc_workloads_optimization_enabled}.'''
        result = self._values.get("adhoc_workloads_optimization_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#collation MssqlVirtualMachine#collation}.'''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instant_file_initialization_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#instant_file_initialization_enabled MssqlVirtualMachine#instant_file_initialization_enabled}.'''
        result = self._values.get("instant_file_initialization_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def lock_pages_in_memory_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#lock_pages_in_memory_enabled MssqlVirtualMachine#lock_pages_in_memory_enabled}.'''
        result = self._values.get("lock_pages_in_memory_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_dop(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_dop MssqlVirtualMachine#max_dop}.'''
        result = self._values.get("max_dop")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_server_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#max_server_memory_mb MssqlVirtualMachine#max_server_memory_mb}.'''
        result = self._values.get("max_server_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_server_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#min_server_memory_mb MssqlVirtualMachine#min_server_memory_mb}.'''
        result = self._values.get("min_server_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineSqlInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineSqlInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineSqlInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6896572280cde4eb27960599667543ca33421c9c83c1c327276ce0297bbe4956)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdhocWorkloadsOptimizationEnabled")
    def reset_adhoc_workloads_optimization_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdhocWorkloadsOptimizationEnabled", []))

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetInstantFileInitializationEnabled")
    def reset_instant_file_initialization_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstantFileInitializationEnabled", []))

    @jsii.member(jsii_name="resetLockPagesInMemoryEnabled")
    def reset_lock_pages_in_memory_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockPagesInMemoryEnabled", []))

    @jsii.member(jsii_name="resetMaxDop")
    def reset_max_dop(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDop", []))

    @jsii.member(jsii_name="resetMaxServerMemoryMb")
    def reset_max_server_memory_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxServerMemoryMb", []))

    @jsii.member(jsii_name="resetMinServerMemoryMb")
    def reset_min_server_memory_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinServerMemoryMb", []))

    @builtins.property
    @jsii.member(jsii_name="adhocWorkloadsOptimizationEnabledInput")
    def adhoc_workloads_optimization_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adhocWorkloadsOptimizationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="instantFileInitializationEnabledInput")
    def instant_file_initialization_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "instantFileInitializationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="lockPagesInMemoryEnabledInput")
    def lock_pages_in_memory_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lockPagesInMemoryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDopInput")
    def max_dop_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDopInput"))

    @builtins.property
    @jsii.member(jsii_name="maxServerMemoryMbInput")
    def max_server_memory_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxServerMemoryMbInput"))

    @builtins.property
    @jsii.member(jsii_name="minServerMemoryMbInput")
    def min_server_memory_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minServerMemoryMbInput"))

    @builtins.property
    @jsii.member(jsii_name="adhocWorkloadsOptimizationEnabled")
    def adhoc_workloads_optimization_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adhocWorkloadsOptimizationEnabled"))

    @adhoc_workloads_optimization_enabled.setter
    def adhoc_workloads_optimization_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076cf527a8f787fd4eca00e8f3bd510acf64eb30d7a2bc67be117dff86b833d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adhocWorkloadsOptimizationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8ef8f7dad2c8c6edc538c94cfebb7f6ed5e59d052df08d01271ee4db02f648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instantFileInitializationEnabled")
    def instant_file_initialization_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "instantFileInitializationEnabled"))

    @instant_file_initialization_enabled.setter
    def instant_file_initialization_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ac068e0bc2ece76ac62e5dfa994f289d64be5ef3c8a5cfa87751fe6130aa9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instantFileInitializationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockPagesInMemoryEnabled")
    def lock_pages_in_memory_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lockPagesInMemoryEnabled"))

    @lock_pages_in_memory_enabled.setter
    def lock_pages_in_memory_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1d4b6d3600ad700e1a7ad4aec96effc680373475543d3a105bf3df0bd71492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockPagesInMemoryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDop")
    def max_dop(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDop"))

    @max_dop.setter
    def max_dop(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de615e1ace8d6cd871c8a6436554ee8ccdb699daa6a4cdeb4e8bfc1895c1083c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxServerMemoryMb")
    def max_server_memory_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxServerMemoryMb"))

    @max_server_memory_mb.setter
    def max_server_memory_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e7753a1395b283b3cf5a21dfb70d71940ed9d5ca9949df96837c48b01f7b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxServerMemoryMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minServerMemoryMb")
    def min_server_memory_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minServerMemoryMb"))

    @min_server_memory_mb.setter
    def min_server_memory_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd4075e5b0921215860fd5358aea9b317161dd959587cb5bb5cb686b4c6ca90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minServerMemoryMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlVirtualMachineSqlInstance]:
        return typing.cast(typing.Optional[MssqlVirtualMachineSqlInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineSqlInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860c5fff2836ccd862684c930560acc6897515a26dec42c80b51278d88a29889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "disk_type": "diskType",
        "storage_workload_type": "storageWorkloadType",
        "data_settings": "dataSettings",
        "log_settings": "logSettings",
        "system_db_on_data_disk_enabled": "systemDbOnDataDiskEnabled",
        "temp_db_settings": "tempDbSettings",
    },
)
class MssqlVirtualMachineStorageConfiguration:
    def __init__(
        self,
        *,
        disk_type: builtins.str,
        storage_workload_type: builtins.str,
        data_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationDataSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        log_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationLogSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        system_db_on_data_disk_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        temp_db_settings: typing.Optional[typing.Union["MssqlVirtualMachineStorageConfigurationTempDbSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#disk_type MssqlVirtualMachine#disk_type}.
        :param storage_workload_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_workload_type MssqlVirtualMachine#storage_workload_type}.
        :param data_settings: data_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_settings MssqlVirtualMachine#data_settings}
        :param log_settings: log_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_settings MssqlVirtualMachine#log_settings}
        :param system_db_on_data_disk_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_db_on_data_disk_enabled MssqlVirtualMachine#system_db_on_data_disk_enabled}.
        :param temp_db_settings: temp_db_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#temp_db_settings MssqlVirtualMachine#temp_db_settings}
        '''
        if isinstance(data_settings, dict):
            data_settings = MssqlVirtualMachineStorageConfigurationDataSettings(**data_settings)
        if isinstance(log_settings, dict):
            log_settings = MssqlVirtualMachineStorageConfigurationLogSettings(**log_settings)
        if isinstance(temp_db_settings, dict):
            temp_db_settings = MssqlVirtualMachineStorageConfigurationTempDbSettings(**temp_db_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950e4f57d8d376327abcc6277f24a28c36192f1be2935e3e2a927fc18ded6856)
            check_type(argname="argument disk_type", value=disk_type, expected_type=type_hints["disk_type"])
            check_type(argname="argument storage_workload_type", value=storage_workload_type, expected_type=type_hints["storage_workload_type"])
            check_type(argname="argument data_settings", value=data_settings, expected_type=type_hints["data_settings"])
            check_type(argname="argument log_settings", value=log_settings, expected_type=type_hints["log_settings"])
            check_type(argname="argument system_db_on_data_disk_enabled", value=system_db_on_data_disk_enabled, expected_type=type_hints["system_db_on_data_disk_enabled"])
            check_type(argname="argument temp_db_settings", value=temp_db_settings, expected_type=type_hints["temp_db_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disk_type": disk_type,
            "storage_workload_type": storage_workload_type,
        }
        if data_settings is not None:
            self._values["data_settings"] = data_settings
        if log_settings is not None:
            self._values["log_settings"] = log_settings
        if system_db_on_data_disk_enabled is not None:
            self._values["system_db_on_data_disk_enabled"] = system_db_on_data_disk_enabled
        if temp_db_settings is not None:
            self._values["temp_db_settings"] = temp_db_settings

    @builtins.property
    def disk_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#disk_type MssqlVirtualMachine#disk_type}.'''
        result = self._values.get("disk_type")
        assert result is not None, "Required property 'disk_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_workload_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#storage_workload_type MssqlVirtualMachine#storage_workload_type}.'''
        result = self._values.get("storage_workload_type")
        assert result is not None, "Required property 'storage_workload_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_settings(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfigurationDataSettings"]:
        '''data_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_settings MssqlVirtualMachine#data_settings}
        '''
        result = self._values.get("data_settings")
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfigurationDataSettings"], result)

    @builtins.property
    def log_settings(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfigurationLogSettings"]:
        '''log_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_settings MssqlVirtualMachine#log_settings}
        '''
        result = self._values.get("log_settings")
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfigurationLogSettings"], result)

    @builtins.property
    def system_db_on_data_disk_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#system_db_on_data_disk_enabled MssqlVirtualMachine#system_db_on_data_disk_enabled}.'''
        result = self._values.get("system_db_on_data_disk_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def temp_db_settings(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfigurationTempDbSettings"]:
        '''temp_db_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#temp_db_settings MssqlVirtualMachine#temp_db_settings}
        '''
        result = self._values.get("temp_db_settings")
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfigurationTempDbSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineStorageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationDataSettings",
    jsii_struct_bases=[],
    name_mapping={"default_file_path": "defaultFilePath", "luns": "luns"},
)
class MssqlVirtualMachineStorageConfigurationDataSettings:
    def __init__(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858100d0dcd46401b7e72e8e31a141ed9b549911b269706a4d5f534e7cff85f0)
            check_type(argname="argument default_file_path", value=default_file_path, expected_type=type_hints["default_file_path"])
            check_type(argname="argument luns", value=luns, expected_type=type_hints["luns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_file_path": default_file_path,
            "luns": luns,
        }

    @builtins.property
    def default_file_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.'''
        result = self._values.get("default_file_path")
        assert result is not None, "Required property 'default_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def luns(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.'''
        result = self._values.get("luns")
        assert result is not None, "Required property 'luns' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineStorageConfigurationDataSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineStorageConfigurationDataSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationDataSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf976631ff581673c53e828b508b73c48fd4c70f09c1786d23b71345dfb73f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultFilePathInput")
    def default_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="lunsInput")
    def luns_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "lunsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultFilePath")
    def default_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultFilePath"))

    @default_file_path.setter
    def default_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea7415c75b19ea21877812b958126481461bea2cf8ce950dbe10d19dd51182e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="luns")
    def luns(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "luns"))

    @luns.setter
    def luns(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37a9e796e3a61551e2b30d1dd12b3124fd192d9d6fdc3efc1edba117f74f189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "luns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dcca988033dc563e459b8fbeefdedb3ffdc1ff6dc6cd04c4b75b5d92fd7ca16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationLogSettings",
    jsii_struct_bases=[],
    name_mapping={"default_file_path": "defaultFilePath", "luns": "luns"},
)
class MssqlVirtualMachineStorageConfigurationLogSettings:
    def __init__(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9af0ce3af6b05652c856a25a6fe1050694f56bd2af12b29f7cf0ab18b717891)
            check_type(argname="argument default_file_path", value=default_file_path, expected_type=type_hints["default_file_path"])
            check_type(argname="argument luns", value=luns, expected_type=type_hints["luns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_file_path": default_file_path,
            "luns": luns,
        }

    @builtins.property
    def default_file_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.'''
        result = self._values.get("default_file_path")
        assert result is not None, "Required property 'default_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def luns(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.'''
        result = self._values.get("luns")
        assert result is not None, "Required property 'luns' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineStorageConfigurationLogSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineStorageConfigurationLogSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationLogSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9da0424c1a3a09a4f933b027b1268bc1c11ebd005418acf065666b29f220c31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="defaultFilePathInput")
    def default_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="lunsInput")
    def luns_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "lunsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultFilePath")
    def default_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultFilePath"))

    @default_file_path.setter
    def default_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142850354998ac0b4fa22edda224c1a7072682509c0e7471294ad2ed0484f72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="luns")
    def luns(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "luns"))

    @luns.setter
    def luns(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b471ff9de1f0bd67aa74f14f55e52cc20b8e7fbed9a6d9ff8f588587113aec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "luns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88fc8615ee5bf4cde07730d59755867e1d8b7929a8fefa29589c95a8797a134b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MssqlVirtualMachineStorageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab9f96cd17244d63b5975fca480abc0b877314d78d2d6722c281b0bfcb49c715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataSettings")
    def put_data_settings(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        '''
        value = MssqlVirtualMachineStorageConfigurationDataSettings(
            default_file_path=default_file_path, luns=luns
        )

        return typing.cast(None, jsii.invoke(self, "putDataSettings", [value]))

    @jsii.member(jsii_name="putLogSettings")
    def put_log_settings(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        '''
        value = MssqlVirtualMachineStorageConfigurationLogSettings(
            default_file_path=default_file_path, luns=luns
        )

        return typing.cast(None, jsii.invoke(self, "putLogSettings", [value]))

    @jsii.member(jsii_name="putTempDbSettings")
    def put_temp_db_settings(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
        data_file_count: typing.Optional[jsii.Number] = None,
        data_file_growth_in_mb: typing.Optional[jsii.Number] = None,
        data_file_size_mb: typing.Optional[jsii.Number] = None,
        log_file_growth_mb: typing.Optional[jsii.Number] = None,
        log_file_size_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        :param data_file_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_count MssqlVirtualMachine#data_file_count}.
        :param data_file_growth_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_growth_in_mb MssqlVirtualMachine#data_file_growth_in_mb}.
        :param data_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_size_mb MssqlVirtualMachine#data_file_size_mb}.
        :param log_file_growth_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_growth_mb MssqlVirtualMachine#log_file_growth_mb}.
        :param log_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_size_mb MssqlVirtualMachine#log_file_size_mb}.
        '''
        value = MssqlVirtualMachineStorageConfigurationTempDbSettings(
            default_file_path=default_file_path,
            luns=luns,
            data_file_count=data_file_count,
            data_file_growth_in_mb=data_file_growth_in_mb,
            data_file_size_mb=data_file_size_mb,
            log_file_growth_mb=log_file_growth_mb,
            log_file_size_mb=log_file_size_mb,
        )

        return typing.cast(None, jsii.invoke(self, "putTempDbSettings", [value]))

    @jsii.member(jsii_name="resetDataSettings")
    def reset_data_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSettings", []))

    @jsii.member(jsii_name="resetLogSettings")
    def reset_log_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogSettings", []))

    @jsii.member(jsii_name="resetSystemDbOnDataDiskEnabled")
    def reset_system_db_on_data_disk_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDbOnDataDiskEnabled", []))

    @jsii.member(jsii_name="resetTempDbSettings")
    def reset_temp_db_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTempDbSettings", []))

    @builtins.property
    @jsii.member(jsii_name="dataSettings")
    def data_settings(
        self,
    ) -> MssqlVirtualMachineStorageConfigurationDataSettingsOutputReference:
        return typing.cast(MssqlVirtualMachineStorageConfigurationDataSettingsOutputReference, jsii.get(self, "dataSettings"))

    @builtins.property
    @jsii.member(jsii_name="logSettings")
    def log_settings(
        self,
    ) -> MssqlVirtualMachineStorageConfigurationLogSettingsOutputReference:
        return typing.cast(MssqlVirtualMachineStorageConfigurationLogSettingsOutputReference, jsii.get(self, "logSettings"))

    @builtins.property
    @jsii.member(jsii_name="tempDbSettings")
    def temp_db_settings(
        self,
    ) -> "MssqlVirtualMachineStorageConfigurationTempDbSettingsOutputReference":
        return typing.cast("MssqlVirtualMachineStorageConfigurationTempDbSettingsOutputReference", jsii.get(self, "tempDbSettings"))

    @builtins.property
    @jsii.member(jsii_name="dataSettingsInput")
    def data_settings_input(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings], jsii.get(self, "dataSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskTypeInput")
    def disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "diskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="logSettingsInput")
    def log_settings_input(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings], jsii.get(self, "logSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageWorkloadTypeInput")
    def storage_workload_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageWorkloadTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDbOnDataDiskEnabledInput")
    def system_db_on_data_disk_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "systemDbOnDataDiskEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tempDbSettingsInput")
    def temp_db_settings_input(
        self,
    ) -> typing.Optional["MssqlVirtualMachineStorageConfigurationTempDbSettings"]:
        return typing.cast(typing.Optional["MssqlVirtualMachineStorageConfigurationTempDbSettings"], jsii.get(self, "tempDbSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="diskType")
    def disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diskType"))

    @disk_type.setter
    def disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5c81988c28fd2b8e240c48e03d8a4b8aed0cd08dd7a98736594ecb86987ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageWorkloadType")
    def storage_workload_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageWorkloadType"))

    @storage_workload_type.setter
    def storage_workload_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50967f3044bf3e590f98f57e586584b7a199556422e6391fd38db149d12cf23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageWorkloadType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDbOnDataDiskEnabled")
    def system_db_on_data_disk_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "systemDbOnDataDiskEnabled"))

    @system_db_on_data_disk_enabled.setter
    def system_db_on_data_disk_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263231c5bee1393c3dc38ff951a78b32155817eb2ddc2a08ecf6c956a2d27fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDbOnDataDiskEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfiguration]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineStorageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30925d963778049f5c18056648204421113a73429f41f7689d0d0d1a62039a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationTempDbSettings",
    jsii_struct_bases=[],
    name_mapping={
        "default_file_path": "defaultFilePath",
        "luns": "luns",
        "data_file_count": "dataFileCount",
        "data_file_growth_in_mb": "dataFileGrowthInMb",
        "data_file_size_mb": "dataFileSizeMb",
        "log_file_growth_mb": "logFileGrowthMb",
        "log_file_size_mb": "logFileSizeMb",
    },
)
class MssqlVirtualMachineStorageConfigurationTempDbSettings:
    def __init__(
        self,
        *,
        default_file_path: builtins.str,
        luns: typing.Sequence[jsii.Number],
        data_file_count: typing.Optional[jsii.Number] = None,
        data_file_growth_in_mb: typing.Optional[jsii.Number] = None,
        data_file_size_mb: typing.Optional[jsii.Number] = None,
        log_file_growth_mb: typing.Optional[jsii.Number] = None,
        log_file_size_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_file_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.
        :param luns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.
        :param data_file_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_count MssqlVirtualMachine#data_file_count}.
        :param data_file_growth_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_growth_in_mb MssqlVirtualMachine#data_file_growth_in_mb}.
        :param data_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_size_mb MssqlVirtualMachine#data_file_size_mb}.
        :param log_file_growth_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_growth_mb MssqlVirtualMachine#log_file_growth_mb}.
        :param log_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_size_mb MssqlVirtualMachine#log_file_size_mb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b645d4b20c120641ff15febf95cf264f2878ebd29397575b52d8fdebb3615b)
            check_type(argname="argument default_file_path", value=default_file_path, expected_type=type_hints["default_file_path"])
            check_type(argname="argument luns", value=luns, expected_type=type_hints["luns"])
            check_type(argname="argument data_file_count", value=data_file_count, expected_type=type_hints["data_file_count"])
            check_type(argname="argument data_file_growth_in_mb", value=data_file_growth_in_mb, expected_type=type_hints["data_file_growth_in_mb"])
            check_type(argname="argument data_file_size_mb", value=data_file_size_mb, expected_type=type_hints["data_file_size_mb"])
            check_type(argname="argument log_file_growth_mb", value=log_file_growth_mb, expected_type=type_hints["log_file_growth_mb"])
            check_type(argname="argument log_file_size_mb", value=log_file_size_mb, expected_type=type_hints["log_file_size_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_file_path": default_file_path,
            "luns": luns,
        }
        if data_file_count is not None:
            self._values["data_file_count"] = data_file_count
        if data_file_growth_in_mb is not None:
            self._values["data_file_growth_in_mb"] = data_file_growth_in_mb
        if data_file_size_mb is not None:
            self._values["data_file_size_mb"] = data_file_size_mb
        if log_file_growth_mb is not None:
            self._values["log_file_growth_mb"] = log_file_growth_mb
        if log_file_size_mb is not None:
            self._values["log_file_size_mb"] = log_file_size_mb

    @builtins.property
    def default_file_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#default_file_path MssqlVirtualMachine#default_file_path}.'''
        result = self._values.get("default_file_path")
        assert result is not None, "Required property 'default_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def luns(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#luns MssqlVirtualMachine#luns}.'''
        result = self._values.get("luns")
        assert result is not None, "Required property 'luns' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def data_file_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_count MssqlVirtualMachine#data_file_count}.'''
        result = self._values.get("data_file_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_file_growth_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_growth_in_mb MssqlVirtualMachine#data_file_growth_in_mb}.'''
        result = self._values.get("data_file_growth_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_file_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#data_file_size_mb MssqlVirtualMachine#data_file_size_mb}.'''
        result = self._values.get("data_file_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_file_growth_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_growth_mb MssqlVirtualMachine#log_file_growth_mb}.'''
        result = self._values.get("log_file_growth_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_file_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#log_file_size_mb MssqlVirtualMachine#log_file_size_mb}.'''
        result = self._values.get("log_file_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineStorageConfigurationTempDbSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineStorageConfigurationTempDbSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineStorageConfigurationTempDbSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8045630e494a12836c8db84cb333eb947c8d2badc3b3cdfaacff77effc244e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataFileCount")
    def reset_data_file_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFileCount", []))

    @jsii.member(jsii_name="resetDataFileGrowthInMb")
    def reset_data_file_growth_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFileGrowthInMb", []))

    @jsii.member(jsii_name="resetDataFileSizeMb")
    def reset_data_file_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFileSizeMb", []))

    @jsii.member(jsii_name="resetLogFileGrowthMb")
    def reset_log_file_growth_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogFileGrowthMb", []))

    @jsii.member(jsii_name="resetLogFileSizeMb")
    def reset_log_file_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogFileSizeMb", []))

    @builtins.property
    @jsii.member(jsii_name="dataFileCountInput")
    def data_file_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataFileCountInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFileGrowthInMbInput")
    def data_file_growth_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataFileGrowthInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFileSizeMbInput")
    def data_file_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataFileSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultFilePathInput")
    def default_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="logFileGrowthMbInput")
    def log_file_growth_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logFileGrowthMbInput"))

    @builtins.property
    @jsii.member(jsii_name="logFileSizeMbInput")
    def log_file_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "logFileSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="lunsInput")
    def luns_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "lunsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFileCount")
    def data_file_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataFileCount"))

    @data_file_count.setter
    def data_file_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb46c203a56c3ca8a1734b5c2e003eb67e1a461eae8133a9b4a40f3637e21ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFileCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFileGrowthInMb")
    def data_file_growth_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataFileGrowthInMb"))

    @data_file_growth_in_mb.setter
    def data_file_growth_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed7528160327b58da00d573c6293b68e15ad00534cb00006b63cbb2068944dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFileGrowthInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFileSizeMb")
    def data_file_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataFileSizeMb"))

    @data_file_size_mb.setter
    def data_file_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3154e0b43db0539ac6c3bbfb552dae67f96e87437705ba172c08d2c156d95673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFileSizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultFilePath")
    def default_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultFilePath"))

    @default_file_path.setter
    def default_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e167ec09be4472a22bd5e59539df8da9707dd27799580f7b7956d606b3be30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logFileGrowthMb")
    def log_file_growth_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logFileGrowthMb"))

    @log_file_growth_mb.setter
    def log_file_growth_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c38449a6df5deefe735623f96f042dc67dac31e7f5199089e4af074fff9bd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logFileGrowthMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logFileSizeMb")
    def log_file_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logFileSizeMb"))

    @log_file_size_mb.setter
    def log_file_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d05ad3a443600d29f0e603cae1fe566a13c8b4511ba31549467e211fb6ae81b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logFileSizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="luns")
    def luns(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "luns"))

    @luns.setter
    def luns(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c75d1e3ede39334c05c42522ac1b7180067ea8c837686508974cc0bd4a725a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "luns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineStorageConfigurationTempDbSettings]:
        return typing.cast(typing.Optional[MssqlVirtualMachineStorageConfigurationTempDbSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineStorageConfigurationTempDbSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e044c064cfd51a372f56f3795c243f1de4b6c46777cd0459d1f939f3e62c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MssqlVirtualMachineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#create MssqlVirtualMachine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#delete MssqlVirtualMachine#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#read MssqlVirtualMachine#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#update MssqlVirtualMachine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe78fc0939d2ee1f76d7dc80971996522b53eb232536a5620815c6c33faa7f8c)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#create MssqlVirtualMachine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#delete MssqlVirtualMachine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#read MssqlVirtualMachine#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#update MssqlVirtualMachine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4846ebad9a6a0928d3dcd08d950790ca17953d74cddad9240aaa5c0b0bf1c53c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0884f944503e8aaa386d2e3d60c152d1df88b3dc16c4750b7ab03c14c99c023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e777784d90988817b32c63b5aab25fb653ebf9a7aabcacc3e9d9b4a0fa962c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507bd3d43845b5d6165a35b9d789501250926e56d498d0e7e44b4c525e134c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b46981f60c100deb10e928ac648f206884e9930d3e703d6c500fd70b854449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8175611941d7bf6fc9482d4fade650327e7f1b097776fa6287954e7e81d6fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineWsfcDomainCredential",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_bootstrap_account_password": "clusterBootstrapAccountPassword",
        "cluster_operator_account_password": "clusterOperatorAccountPassword",
        "sql_service_account_password": "sqlServiceAccountPassword",
    },
)
class MssqlVirtualMachineWsfcDomainCredential:
    def __init__(
        self,
        *,
        cluster_bootstrap_account_password: builtins.str,
        cluster_operator_account_password: builtins.str,
        sql_service_account_password: builtins.str,
    ) -> None:
        '''
        :param cluster_bootstrap_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_bootstrap_account_password MssqlVirtualMachine#cluster_bootstrap_account_password}.
        :param cluster_operator_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_operator_account_password MssqlVirtualMachine#cluster_operator_account_password}.
        :param sql_service_account_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_service_account_password MssqlVirtualMachine#sql_service_account_password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee9e19189f0bb953e19bd1b82c177d785f100482dc0f3bee6efcff5bcc04e15)
            check_type(argname="argument cluster_bootstrap_account_password", value=cluster_bootstrap_account_password, expected_type=type_hints["cluster_bootstrap_account_password"])
            check_type(argname="argument cluster_operator_account_password", value=cluster_operator_account_password, expected_type=type_hints["cluster_operator_account_password"])
            check_type(argname="argument sql_service_account_password", value=sql_service_account_password, expected_type=type_hints["sql_service_account_password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_bootstrap_account_password": cluster_bootstrap_account_password,
            "cluster_operator_account_password": cluster_operator_account_password,
            "sql_service_account_password": sql_service_account_password,
        }

    @builtins.property
    def cluster_bootstrap_account_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_bootstrap_account_password MssqlVirtualMachine#cluster_bootstrap_account_password}.'''
        result = self._values.get("cluster_bootstrap_account_password")
        assert result is not None, "Required property 'cluster_bootstrap_account_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_operator_account_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#cluster_operator_account_password MssqlVirtualMachine#cluster_operator_account_password}.'''
        result = self._values.get("cluster_operator_account_password")
        assert result is not None, "Required property 'cluster_operator_account_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_service_account_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_virtual_machine#sql_service_account_password MssqlVirtualMachine#sql_service_account_password}.'''
        result = self._values.get("sql_service_account_password")
        assert result is not None, "Required property 'sql_service_account_password' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlVirtualMachineWsfcDomainCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlVirtualMachineWsfcDomainCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlVirtualMachine.MssqlVirtualMachineWsfcDomainCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02cb7451f6e51d473e7d1c6b5e43ad7d69347cdd566de3d4a793fd6c537f09f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clusterBootstrapAccountPasswordInput")
    def cluster_bootstrap_account_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterBootstrapAccountPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterOperatorAccountPasswordInput")
    def cluster_operator_account_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterOperatorAccountPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServiceAccountPasswordInput")
    def sql_service_account_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlServiceAccountPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterBootstrapAccountPassword")
    def cluster_bootstrap_account_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterBootstrapAccountPassword"))

    @cluster_bootstrap_account_password.setter
    def cluster_bootstrap_account_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01c418d29cae771abfc581d3a1a9f5c57fcf2b19dcacf98d4a4abd8b768dca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterBootstrapAccountPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterOperatorAccountPassword")
    def cluster_operator_account_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterOperatorAccountPassword"))

    @cluster_operator_account_password.setter
    def cluster_operator_account_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fefbe67ba9f493e11747458012c3a4f433b19e5715bab5f16a42b504c16ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterOperatorAccountPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlServiceAccountPassword")
    def sql_service_account_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlServiceAccountPassword"))

    @sql_service_account_password.setter
    def sql_service_account_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c37ab439b1d840efa764068dd4b738ff1c8a64a9a7162618c2607f10793e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlServiceAccountPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MssqlVirtualMachineWsfcDomainCredential]:
        return typing.cast(typing.Optional[MssqlVirtualMachineWsfcDomainCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlVirtualMachineWsfcDomainCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7d25487f10ac289b32237a8f2a9a26ba168a6a9cce48e0b929dc81add90420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlVirtualMachine",
    "MssqlVirtualMachineAssessment",
    "MssqlVirtualMachineAssessmentOutputReference",
    "MssqlVirtualMachineAssessmentSchedule",
    "MssqlVirtualMachineAssessmentScheduleOutputReference",
    "MssqlVirtualMachineAutoBackup",
    "MssqlVirtualMachineAutoBackupManualSchedule",
    "MssqlVirtualMachineAutoBackupManualScheduleOutputReference",
    "MssqlVirtualMachineAutoBackupOutputReference",
    "MssqlVirtualMachineAutoPatching",
    "MssqlVirtualMachineAutoPatchingOutputReference",
    "MssqlVirtualMachineConfig",
    "MssqlVirtualMachineKeyVaultCredential",
    "MssqlVirtualMachineKeyVaultCredentialOutputReference",
    "MssqlVirtualMachineSqlInstance",
    "MssqlVirtualMachineSqlInstanceOutputReference",
    "MssqlVirtualMachineStorageConfiguration",
    "MssqlVirtualMachineStorageConfigurationDataSettings",
    "MssqlVirtualMachineStorageConfigurationDataSettingsOutputReference",
    "MssqlVirtualMachineStorageConfigurationLogSettings",
    "MssqlVirtualMachineStorageConfigurationLogSettingsOutputReference",
    "MssqlVirtualMachineStorageConfigurationOutputReference",
    "MssqlVirtualMachineStorageConfigurationTempDbSettings",
    "MssqlVirtualMachineStorageConfigurationTempDbSettingsOutputReference",
    "MssqlVirtualMachineTimeouts",
    "MssqlVirtualMachineTimeoutsOutputReference",
    "MssqlVirtualMachineWsfcDomainCredential",
    "MssqlVirtualMachineWsfcDomainCredentialOutputReference",
]

publication.publish()

def _typecheckingstub__623ee4980fcb19a68aee3d59f10e6949802218c892655776f7e4ad0c1dedeac2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    virtual_machine_id: builtins.str,
    assessment: typing.Optional[typing.Union[MssqlVirtualMachineAssessment, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_backup: typing.Optional[typing.Union[MssqlVirtualMachineAutoBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_patching: typing.Optional[typing.Union[MssqlVirtualMachineAutoPatching, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key_vault_credential: typing.Optional[typing.Union[MssqlVirtualMachineKeyVaultCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    r_services_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sql_connectivity_port: typing.Optional[jsii.Number] = None,
    sql_connectivity_type: typing.Optional[builtins.str] = None,
    sql_connectivity_update_password: typing.Optional[builtins.str] = None,
    sql_connectivity_update_username: typing.Optional[builtins.str] = None,
    sql_instance: typing.Optional[typing.Union[MssqlVirtualMachineSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_license_type: typing.Optional[builtins.str] = None,
    sql_virtual_machine_group_id: typing.Optional[builtins.str] = None,
    storage_configuration: typing.Optional[typing.Union[MssqlVirtualMachineStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wsfc_domain_credential: typing.Optional[typing.Union[MssqlVirtualMachineWsfcDomainCredential, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2d9d08a79fea667eeb2c3f8e5cf081da44bc5330a035af00feca81500ffa943b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdfbb6b572a71ff78faf6a74e27d9357fb600fe0703de701d485c47f3505331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f2d5dce46cf00e1359343958c82900c901f0eeb7acc29099caee3e4fed611e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc928ad140e541f75df20d4a037f9a7382c9932ef32a8aa073ba0256ef109758(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd9146600e12fadb26f7c481632d6f7a5ddac6d86b6f51cdc503958515d49e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63610aedebe74fd52536615cab066e7294608cac457459b1a6d0959dacabb3cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b51d4bd929d76b96336e09f320edb61d065530e4e3310ba133e3989b32cdab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ae2b9ada029b6acae7250e84c29966f0b32626d218054cfdd3f8fa026eb49b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16de0ccd44bf288d5c1d38f61d3f371a7cf009966db9aa28163faa348987eb48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f1ec5c83bb86c8db7c7509e1cddb5ace6edc93418446627e2092e4dd9feda6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905fb0f639e1a808d8e4c0108c89be64bcdf800868aee744791e54bdfe8b443f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3d787f9e113f33854596b4a1ef33bfae0a6356e31a51f16c7bea237d385d08(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    run_immediately: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    schedule: typing.Optional[typing.Union[MssqlVirtualMachineAssessmentSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a73f94be47079cb580722e84e639d54635fcac492bad3a854f7d23c7e1a88c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f107d0e08a01728ac6e6aad87ccb79de3457057bbcbe985d07193d40cad2e51d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70075df0f441d5fc08eba5fe33fce4c2d5816b099b05b359684d3cd28c521878(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9010001f0cea37f041ecfba876cf7e235a9fb0ce6efd4c56717e374d5b21f69b(
    value: typing.Optional[MssqlVirtualMachineAssessment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65966c353a81ffdfc4190aa5ae0ad183cb92724c40bea3fcf92292058066f911(
    *,
    day_of_week: builtins.str,
    start_time: builtins.str,
    monthly_occurrence: typing.Optional[jsii.Number] = None,
    weekly_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a43e0b6daa46bf9e2b5d7917b6bfffb02fca27b02c40ca609988dca3164a7fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755088e15082401f9936faa3c8c3454ef9ad3183ac3bb5801692bed0860d8bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0a29d8aa72917e45b5cba921e9b1540fa4fca5a78a05947a6cf83b5ecd824fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711918cb01b6d518164d861e5029d0f7e0671efbb599ac8ddaaa42e010ef5522(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353f877484f6fcd98eeff6a477f391d003084675f8e6c4259b4216db6c3c1483(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c58950e0c9bf1e81f2c1c707133d8e8a2ee4141c611984f85800b24aa591ab(
    value: typing.Optional[MssqlVirtualMachineAssessmentSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c7f8d0aa819ef18ce404a48227109b56b062bf29d20aeba2c4f0626e4a09d6(
    *,
    retention_period_in_days: jsii.Number,
    storage_account_access_key: builtins.str,
    storage_blob_endpoint: builtins.str,
    encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encryption_password: typing.Optional[builtins.str] = None,
    manual_schedule: typing.Optional[typing.Union[MssqlVirtualMachineAutoBackupManualSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    system_databases_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c914c25666720764b4c7f8ffbd32c3b3f4e2151532700aa46da22a302ac8d4b3(
    *,
    full_backup_frequency: builtins.str,
    full_backup_start_hour: jsii.Number,
    full_backup_window_in_hours: jsii.Number,
    log_backup_frequency_in_minutes: jsii.Number,
    days_of_week: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed3a64eb938adbe50649fffb2c397fe60cbd543c83d052c5550ebae001351a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83639ee816361388b8d04ec4b3798ea8bcc2a377e3a92a0a7203a32c41c2108(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83a5c022cdb579095ccfe47f7964aaa59ac748e75ad9881a018f0215390a659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7bf715930c8b54c792a42fc01c90a5e42d33b41893c117743b971703bc1e2a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85c570c5a0827587a8f7e6319c36ef12db5f892912e6667f0b41cd08d559236(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ab94fbeb2739641f86d23b2730934f68f8f90d23891f554c892da47a5c9ea4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046fbbe8657c1dcff3c1d9751481f670576f87223412490e8b6f57c7f782983b(
    value: typing.Optional[MssqlVirtualMachineAutoBackupManualSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda49876c65724f561edfc4948a4168ea6f24f9c1be0a628216b1ae30a6f41b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd15811f8751e294fba545c3fb5d82ad2da52b6a21cd2282658d51238967ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a9f70218c76cabd878d30ff4ca0d977dac5dd6dabdc528f5cdf619d29cd3b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a16ea496f7ba6dc701eb0e200430656b75b463e242d12492b0f369d5af11f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1633a6b63b11230183af55d1029805301563be7e60b9eeda1766fb5aa038826c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3ae520f169c9f802acc85ecf5633e206168aa7402957e1449a8a992596fe7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4385fd85a454abfa7985ef0c480c42314b9b57b2ef68f1144af939c0442b324(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8f26b16ef256dd5503a4e2a2f8be87bcca14edde644f5bd0814eaa82d5d4ec(
    value: typing.Optional[MssqlVirtualMachineAutoBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253d0b3eaf9033787fc78918e8baf57f9918729e7aa465f1bc7e9817dd03da3f(
    *,
    day_of_week: builtins.str,
    maintenance_window_duration_in_minutes: jsii.Number,
    maintenance_window_starting_hour: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc387a59fc87b60550a7259e73f0b0daa6bbd024850bf82b1a934b9251d5a767(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62da7df436f33922aac67439f1e2892e51db13786c5861afb58270c348bf798c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f64ce2831a3c80ae7257fe7d0af4157f4aef3ed19baa8df43927b66a49ac91(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eaa296617755e7b2fb90f169d47a41a09fc65423ba25a05d05298fb424654db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be012b61299b5582755caa8a9eaa7d5f9b1ae6453977631460abc926b4cb6b4(
    value: typing.Optional[MssqlVirtualMachineAutoPatching],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d912e43980043aaffa1740f7100f2ffd8c98a028a259a588cc483118efffd0b7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_machine_id: builtins.str,
    assessment: typing.Optional[typing.Union[MssqlVirtualMachineAssessment, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_backup: typing.Optional[typing.Union[MssqlVirtualMachineAutoBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_patching: typing.Optional[typing.Union[MssqlVirtualMachineAutoPatching, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key_vault_credential: typing.Optional[typing.Union[MssqlVirtualMachineKeyVaultCredential, typing.Dict[builtins.str, typing.Any]]] = None,
    r_services_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sql_connectivity_port: typing.Optional[jsii.Number] = None,
    sql_connectivity_type: typing.Optional[builtins.str] = None,
    sql_connectivity_update_password: typing.Optional[builtins.str] = None,
    sql_connectivity_update_username: typing.Optional[builtins.str] = None,
    sql_instance: typing.Optional[typing.Union[MssqlVirtualMachineSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_license_type: typing.Optional[builtins.str] = None,
    sql_virtual_machine_group_id: typing.Optional[builtins.str] = None,
    storage_configuration: typing.Optional[typing.Union[MssqlVirtualMachineStorageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MssqlVirtualMachineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    wsfc_domain_credential: typing.Optional[typing.Union[MssqlVirtualMachineWsfcDomainCredential, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5580dfb8359475a3bcf909ef1ca890849cbe3a6328b9ec12b349be0ecd64032f(
    *,
    key_vault_url: builtins.str,
    name: builtins.str,
    service_principal_name: builtins.str,
    service_principal_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eaa50e70febb691bfa449feb048616fb267a68067e6d4146f6713ad8136410b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95aa817463759b675de42f4a0cfebebe239eb185d7aaf30be39fcc6657e6e5d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5296404075e9bad720be5e0a4735494176c1ff64bf626ffe2c9c57059bfb11c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07999f471447b75b992d34a1a3e04b7aaa000367420783a8e3adecf954ae573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81df2df9734e199692a628d7cbbc8107b90c2dbc00d0fd3a9765732fd94a5f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e32ead818404413ed54318bd288d80ca4070676edf9ab2215d2775ae0e27c27(
    value: typing.Optional[MssqlVirtualMachineKeyVaultCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3ee2b8e52e16faef2fb6ec01e15f4e6debbff3e805e13dae2c78a16ed63ea0(
    *,
    adhoc_workloads_optimization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    collation: typing.Optional[builtins.str] = None,
    instant_file_initialization_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    lock_pages_in_memory_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_dop: typing.Optional[jsii.Number] = None,
    max_server_memory_mb: typing.Optional[jsii.Number] = None,
    min_server_memory_mb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6896572280cde4eb27960599667543ca33421c9c83c1c327276ce0297bbe4956(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076cf527a8f787fd4eca00e8f3bd510acf64eb30d7a2bc67be117dff86b833d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8ef8f7dad2c8c6edc538c94cfebb7f6ed5e59d052df08d01271ee4db02f648(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ac068e0bc2ece76ac62e5dfa994f289d64be5ef3c8a5cfa87751fe6130aa9e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1d4b6d3600ad700e1a7ad4aec96effc680373475543d3a105bf3df0bd71492(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de615e1ace8d6cd871c8a6436554ee8ccdb699daa6a4cdeb4e8bfc1895c1083c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e7753a1395b283b3cf5a21dfb70d71940ed9d5ca9949df96837c48b01f7b3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd4075e5b0921215860fd5358aea9b317161dd959587cb5bb5cb686b4c6ca90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860c5fff2836ccd862684c930560acc6897515a26dec42c80b51278d88a29889(
    value: typing.Optional[MssqlVirtualMachineSqlInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950e4f57d8d376327abcc6277f24a28c36192f1be2935e3e2a927fc18ded6856(
    *,
    disk_type: builtins.str,
    storage_workload_type: builtins.str,
    data_settings: typing.Optional[typing.Union[MssqlVirtualMachineStorageConfigurationDataSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    log_settings: typing.Optional[typing.Union[MssqlVirtualMachineStorageConfigurationLogSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    system_db_on_data_disk_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    temp_db_settings: typing.Optional[typing.Union[MssqlVirtualMachineStorageConfigurationTempDbSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858100d0dcd46401b7e72e8e31a141ed9b549911b269706a4d5f534e7cff85f0(
    *,
    default_file_path: builtins.str,
    luns: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf976631ff581673c53e828b508b73c48fd4c70f09c1786d23b71345dfb73f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea7415c75b19ea21877812b958126481461bea2cf8ce950dbe10d19dd51182e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37a9e796e3a61551e2b30d1dd12b3124fd192d9d6fdc3efc1edba117f74f189(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dcca988033dc563e459b8fbeefdedb3ffdc1ff6dc6cd04c4b75b5d92fd7ca16(
    value: typing.Optional[MssqlVirtualMachineStorageConfigurationDataSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9af0ce3af6b05652c856a25a6fe1050694f56bd2af12b29f7cf0ab18b717891(
    *,
    default_file_path: builtins.str,
    luns: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9da0424c1a3a09a4f933b027b1268bc1c11ebd005418acf065666b29f220c31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142850354998ac0b4fa22edda224c1a7072682509c0e7471294ad2ed0484f72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b471ff9de1f0bd67aa74f14f55e52cc20b8e7fbed9a6d9ff8f588587113aec7(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fc8615ee5bf4cde07730d59755867e1d8b7929a8fefa29589c95a8797a134b(
    value: typing.Optional[MssqlVirtualMachineStorageConfigurationLogSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9f96cd17244d63b5975fca480abc0b877314d78d2d6722c281b0bfcb49c715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5c81988c28fd2b8e240c48e03d8a4b8aed0cd08dd7a98736594ecb86987ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50967f3044bf3e590f98f57e586584b7a199556422e6391fd38db149d12cf23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263231c5bee1393c3dc38ff951a78b32155817eb2ddc2a08ecf6c956a2d27fdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30925d963778049f5c18056648204421113a73429f41f7689d0d0d1a62039a3c(
    value: typing.Optional[MssqlVirtualMachineStorageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b645d4b20c120641ff15febf95cf264f2878ebd29397575b52d8fdebb3615b(
    *,
    default_file_path: builtins.str,
    luns: typing.Sequence[jsii.Number],
    data_file_count: typing.Optional[jsii.Number] = None,
    data_file_growth_in_mb: typing.Optional[jsii.Number] = None,
    data_file_size_mb: typing.Optional[jsii.Number] = None,
    log_file_growth_mb: typing.Optional[jsii.Number] = None,
    log_file_size_mb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8045630e494a12836c8db84cb333eb947c8d2badc3b3cdfaacff77effc244e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb46c203a56c3ca8a1734b5c2e003eb67e1a461eae8133a9b4a40f3637e21ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed7528160327b58da00d573c6293b68e15ad00534cb00006b63cbb2068944dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3154e0b43db0539ac6c3bbfb552dae67f96e87437705ba172c08d2c156d95673(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e167ec09be4472a22bd5e59539df8da9707dd27799580f7b7956d606b3be30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c38449a6df5deefe735623f96f042dc67dac31e7f5199089e4af074fff9bd3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d05ad3a443600d29f0e603cae1fe566a13c8b4511ba31549467e211fb6ae81b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c75d1e3ede39334c05c42522ac1b7180067ea8c837686508974cc0bd4a725a3(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e044c064cfd51a372f56f3795c243f1de4b6c46777cd0459d1f939f3e62c8c(
    value: typing.Optional[MssqlVirtualMachineStorageConfigurationTempDbSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe78fc0939d2ee1f76d7dc80971996522b53eb232536a5620815c6c33faa7f8c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4846ebad9a6a0928d3dcd08d950790ca17953d74cddad9240aaa5c0b0bf1c53c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0884f944503e8aaa386d2e3d60c152d1df88b3dc16c4750b7ab03c14c99c023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e777784d90988817b32c63b5aab25fb653ebf9a7aabcacc3e9d9b4a0fa962c2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507bd3d43845b5d6165a35b9d789501250926e56d498d0e7e44b4c525e134c9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b46981f60c100deb10e928ac648f206884e9930d3e703d6c500fd70b854449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8175611941d7bf6fc9482d4fade650327e7f1b097776fa6287954e7e81d6fe1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlVirtualMachineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee9e19189f0bb953e19bd1b82c177d785f100482dc0f3bee6efcff5bcc04e15(
    *,
    cluster_bootstrap_account_password: builtins.str,
    cluster_operator_account_password: builtins.str,
    sql_service_account_password: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cb7451f6e51d473e7d1c6b5e43ad7d69347cdd566de3d4a793fd6c537f09f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01c418d29cae771abfc581d3a1a9f5c57fcf2b19dcacf98d4a4abd8b768dca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fefbe67ba9f493e11747458012c3a4f433b19e5715bab5f16a42b504c16ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c37ab439b1d840efa764068dd4b738ff1c8a64a9a7162618c2607f10793e8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7d25487f10ac289b32237a8f2a9a26ba168a6a9cce48e0b929dc81add90420(
    value: typing.Optional[MssqlVirtualMachineWsfcDomainCredential],
) -> None:
    """Type checking stubs"""
    pass
